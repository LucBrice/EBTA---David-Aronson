#!/usr/bin/env python
"""Pre-push hook: run the canonical EBTA runtime test suite before any push,
and guard against pushing a rewritten/diverged history.

Install as .git/hooks/pre-push (see Implementation/Active/INSTALL_GIT_HOOK.md).

Why this hook exists, and why it is a separate hook from pre-commit
(EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE.md, Phase 3): the pre-commit hook
only activates when an AI-cockpit file is staged, so a commit that only
touches Implementation/ - the exact risk this whole chantier prioritizes,
a coding agent's implementation mistake - never triggers it. The runtime
suite (~50s as of Lot 3) is too slow to run on every commit (commits happen
often) but is acceptable on every push (pushes happen rarely). This hook
runs unconditionally on every push, regardless of which files changed,
closing that gap.

Sync-state check (Council of Five decision, logged in this chantier's
follow-up governance): git already refuses, natively, a plain non-force push
that is not a fast-forward of the remote ref - a hook duplicating that adds
no safety, only friction, and risks stalling an autonomous agent mid-task on
a benign case (e.g. a worktree branch built on an ancestor of main that main
has since moved past on an unrelated path). So this hook does NOT block on
mere staleness. It only hard-blocks the one case git does not protect
against on its own: a ref update that is not a fast-forward of the remote's
current state, which only happens via --force/--force-with-lease. Ordinary
staleness relative to origin/main is reported as a non-blocking warning -
informational only, never stops the push.

This hook is local and can be bypassed with `git push --no-verify` - see
Implementation/Active/INSTALL_GIT_HOOK.md for why that is not a substitute
for the independent CI verdict (PLAN_CI_GITHUB_VERDICT_INDEPENDANT).
"""
import subprocess
import sys

TEST_COMMAND = [
    sys.executable,
    "-m",
    "unittest",
    "discover",
    "-s",
    "Implementation/ebta_engine/tests",
    "-t",
    "Implementation",
]

ZERO_SHA = "0" * 40


def read_pushed_refs():
    """Parse pre-push stdin: one line per pushed ref, formatted as
    '<local ref> <local sha1> <remote ref> <remote sha1>'.
    """
    refs = []
    for line in sys.stdin.read().splitlines():
        parts = line.split()
        if len(parts) == 4:
            refs.append(tuple(parts))
    return refs


def _is_ancestor(candidate_sha, descendant_sha):
    """True if candidate_sha is an ancestor of descendant_sha in this repo.

    Returns False (treated as "not a safe fast-forward") if either object is
    unresolvable locally - this happens precisely when the remote has
    commits this clone never fetched, which is exactly the situation this
    check exists to catch, so failing closed here is correct.
    """
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", candidate_sha, descendant_sha],
        capture_output=True,
    )
    return result.returncode == 0


def check_non_fastforward(refs):
    """Hard-block any ref update that is not a fast-forward of the remote's
    current state. A plain (non-force) push in this situation is already
    refused by git itself; this only fires for pushes that bypass that
    protection (--force/--force-with-lease) or an already-diverged history.
    Returns True if any pushed ref is blocked.
    """
    blocked = False
    for local_ref, local_sha, remote_ref, remote_sha in refs:
        if remote_sha == ZERO_SHA or local_sha == ZERO_SHA:
            continue  # new branch or branch deletion: nothing to rewrite
        if not _is_ancestor(remote_sha, local_sha):
            print()
            print("=" * 72)
            print(f"[EBTA pre-push] BLOCKED: {remote_ref} serait mis a jour de")
            print("  facon non fast-forward (historique reecrit ou divergent).")
            print(f"  local  : {local_sha}")
            print(f"  remote : {remote_sha}")
            print()
            print("  Ceci n'arrive que via un push force (--force/--force-with-lease)")
            print("  ou une divergence non fetchee. Verifie que cette reecriture")
            print("  d'historique est volontaire avant de la pousser.")
            print("=" * 72)
            print()
            blocked = True
    return blocked


def warn_if_behind_origin_main():
    """Non-blocking: warn if HEAD is behind origin/main. Informational only
    - see the module docstring for why this does not block the push.
    """
    subprocess.run(["git", "fetch", "origin", "--quiet"], capture_output=True)
    result = subprocess.run(
        ["git", "rev-list", "--count", "HEAD..origin/main"],
        capture_output=True,
        text=True,
    )
    behind = result.stdout.strip()
    if result.returncode == 0 and behind not in ("", "0"):
        print()
        print(f"[EBTA pre-push] AVERTISSEMENT: HEAD a {behind} commit(s) de retard")
        print("  sur origin/main. Push non bloque, mais verifie que ce n'est pas")
        print("  le signe d'un travail construit sur une base perimee.")
        print()


def main():
    refs = read_pushed_refs()

    warn_if_behind_origin_main()

    if check_non_fastforward(refs):
        return 1

    print("[EBTA pre-push] Running the canonical runtime test suite before push...")
    result = subprocess.run(TEST_COMMAND)
    if result.returncode != 0:
        print()
        print("=" * 72)
        print("[EBTA pre-push] BLOCKED: the runtime test suite did not pass.")
        print(f"  command: {' '.join(TEST_COMMAND)}")
        print()
        print("  Action requise: corriger la suite avant de pousser, ou")
        print("  utiliser 'git push --no-verify' en urgence documentee")
        print("  (voir Implementation/Active/INSTALL_GIT_HOOK.md).")
        print("=" * 72)
        print()
        return 1

    print("[EBTA pre-push] Runtime test suite passed. Proceeding with push.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
