# Brouillon — Lot 6 : CI GitHub, verdict independant

Track : fix
Lifecycle : INTAKE
Scope : Creer `.github/workflows/` avec un job GitHub Actions limite a la
suite `unittest` stdlib et a la validation de schema JSON de
`checkpoint.json`/`tracking.json` (jsonschema installe cote runner
uniquement), sans simuler l'environnement Nautilus en CI. Pousser sur
`origin/main` pour observer un premier run PASS, puis un commit
volontairement cassant pour observer un echec CI reel et visible, puis le
revert pour laisser `main` propre.
Non-goals : Ne simule pas le venv Nautilus en CI (couvert localement par le
`pre-push` du lot 2). N'ajoute aucune dependance runtime au moteur EBTA.
Ne remplace ni le hook `pre-push` ni les preuves `bug_hunter`/
`adversarial_tester`/`plan_conformance` — c'est un verdict supplementaire,
independant, pas un substitut.
Source : Sous-chantier 6/6 de `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE`,
Phase 5bis. Recommandation implicite issue de la decision humaine du
2026-08-07 (chantier mere, section 10 : "Mecanisation des tests : hook
pre-push ET CI GitHub"). Depend du lot 3 (`DONE`) : le premier run CI ne
doit pas etre rouge des le depart.
Exit criteria : (1) `.github/workflows/` existe avec un job dont l'echec est
visible sur le depot distant ; (2) un push normal (etat propre) declenche un
run CI qui aboutit en succes ; (3) un commit volontairement cassant, pousse
sur le remote, declenche un echec de CI GitHub observable (via `gh run
list`/`gh run view`) ; (4) le commit cassant est revert et `main` retrouve
un etat CI vert.

## Autorisation deja donnee (ne pas redemander)

L'utilisateur a explicitement autorise le push git sur `origin/main` pour ce
lot specifiquement, afin d'observer un echec de CI reel sur un commit
volontairement cassant. Le remote existant
(`https://github.com/LucBrice/EBTA---David-Aronson.git`) est deja configure
et `gh` CLI est authentifie (`LucBrice`, verifie par `gh auth status`).

## Boucle `/evaluate` d'intake (2 passes, convergee)

**Passe 1** — Verification de l'etat du remote : `origin/main` et `main`
local pointent tous deux sur `fb7413a` (avant tout commit de ce chantier),
et la branche de travail actuelle (`worktree-agent-afc4593100cea4dbd`) en
est un descendant lineaire direct (`git merge-base` confirme). Le push sera
donc un fast-forward simple, sans conflit. Decision : pousser via
`git push origin HEAD:main`.

**Passe 2** — Verification de la portee minimale du job CI : seules deux
commandes deja documentees dans `CLAUDE.md` sont necessaires
(`python -m unittest discover ...` et la validation de schema via
`jsonschema`), aucune commande nouvelle a inventer. Version Python a
epingler : 3.13 (coherente avec l'environnement local, verifie par le
chemin de l'interpreteur systeme). Convergence a 2 passes sur 6 autorisees.
