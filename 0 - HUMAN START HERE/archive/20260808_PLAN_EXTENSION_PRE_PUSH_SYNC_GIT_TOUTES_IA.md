# Brouillon — Regularisation retroactive : extension du hook pre-push et regle AGENTS.md

## Ce qui s'est passe

Le 2026-08-08, dans la continuite du chantier
`EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE` (cloture le meme jour), l'utilisateur
a demande que le garde-fou de synchronisation git ne concerne pas seulement
Claude Code mais **toute IA travaillant sur ce depot** (Codex compris). Un
hook `.claude/settings.local.json` (`TaskCompleted`) avait ete pose pour
Claude specifiquement ; il a fallu identifier que ce mecanisme est propre a
un seul outil et ne peut pas couvrir les autres.

Decision prise par Conseil des 5 (mode `decision`) : etendre le hook
`pre-push` deja existant (seul mecanisme du depot qui se declenche pour
n'importe quel outil lancant `git push`), avec un modele a deux vitesses :
avertissement systematique non bloquant sur un simple retard vs
`origin/main`, blocage dur uniquement sur un push non fast-forward (force ou
divergence non fetchee — le seul cas que git ne protege pas nativement).
Plus une regle explicite dans `AGENTS.md` (le bootstrap officiel lu par
toute IA, pas seulement Claude) pour couvrir le moment ou une IA demarre un
travail sur une base perimee, qu'aucun hook git ne peut detecter avant coup.

Le code a ete ecrit, teste (242 tests, 0 erreur), committe (`4229d43`,
`150a673`) et pousse **sans passer par `/start`** — directement en
conversation, avec confirmation explicite de l'utilisateur a chaque etape
(choix de severite, commit, push). L'utilisateur a ensuite demande une
regularisation retroactive via le protocole complet, pour beneficier des
memes garanties (bug-hunter, adversarial-tester, plan-conformance-audit)
que tout autre chantier de ce depot.

## Ce que ce document demande

Router ce travail deja termine comme un chantier `fix` retroactif, sur le
meme modele que les precedents deja enregistres a posteriori dans ce depot
(`PLAN_CORRECTION_NAUTILUS_MULTIFOLD_ROBUSTESSE`,
`PLAN_EXPERIENCE_CONTROLEE_DISCRIMINATION_GATES`) : le travail est deja fait
et verifie, mais n'avait jamais ete enregistre comme workstream independant
au moment de son execution.

Perimetre reel deja modifie :
- `Implementation/Active/pre_push_hook.py`
- `Implementation/Active/INSTALL_GIT_HOOK.md`
- `AGENTS.md`
- `Implementation/ebta_engine/tests/test_git_hooks.py`

Aucune autre modification n'est demandee par ce document : il s'agit de
tracabilite, pas de nouveau code (au-dela des corrections issues du
bug-hunter/adversarial-tester reels qui seront executes pendant ce
routage).
