#!/usr/bin/env python
"""Pre-push hook: run the canonical EBTA runtime test suite before any push.

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


def main():
    # A pre-push hook receives ref update lines on stdin (local ref, local
    # sha1, remote ref, remote sha1), one per pushed ref. This hook does not
    # need their content (it always runs the full suite, not a per-commit
    # diff), but the git hook protocol expects stdin to be read; draining it
    # avoids a broken-pipe warning on some git/OS combinations.
    sys.stdin.read()

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
