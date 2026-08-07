# Brouillon — Lot 4 : passage `adversarial-tester` outille sur `governance/`

Track : fix
Lifecycle : INTAKE
Scope : Executer reellement `.agents/skills/adversarial-tester/SKILL.md`
(provocation d'entrees hostiles, pas une simple lecture) sur les 10 fichiers
Python de `Implementation/ebta_engine/governance/`, corriger tout
`FALSE_SUCCESS`/`SILENT_FALLBACK` confirme, et produire le rapport au format
exige par le lot 1 (`PLAN_SUBSTANTIATION_PREUVES_WORKFLOW_READY`, deja DONE).
Non-goals : Ne modifie aucun fichier hors `governance/*.py` et ses tests
associes. Ne modifie aucun seuil, statut ou methode normative EBTA. Ne
supprime ni n'affaiblit aucun test existant pour faire passer la suite.
Source : Sous-chantier 4/6 de `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE`,
Phase 2. Recommandation 4 de l'audit source
`0 - HUMAN START HERE/archive/20260807_AUDIT_ROBUSTESSE_ARCHITECTURE_FACE_ERREURS_IA_2026-08-07.md`.
Depend du lot 1 (deja `DONE`) qui definit le format de preuve recevable.
Exit criteria : (1) les 10 fichiers `.py` de `governance/` ont chacun ete
soumis a au moins un scenario hostile reellement execute (pas seulement lu) ;
(2) tout `FALSE_SUCCESS`/`SILENT_FALLBACK` confirme est corrige et couvert
par un test de regression explicite ; (3) `python -m unittest discover -s
Implementation/ebta_engine/tests -t Implementation` retourne `0 error` (le
compte de tests peut augmenter si des tests de regression sont ajoutes) ;
(4) le rapport respecte le format de preuve substantifie par le lot 1
(reference `chemin#ancre` vers un fichier reel du depot).

## Travail deja effectue avant redaction du plan (a reporter tel quel dans le plan final)

Conformement a `.agents/skills/epic-orchestrator/SKILL.md` etape 1
("revalider dans le code reel avant de rediger le plan"), l'analyse
adversariale reelle a deja ete conduite par execution directe (pas lecture
seule) sur les 10 fichiers de `governance/` :

- `bias_gate.py`, `oos_access_guard.py`, `preregistration_checker.py`,
  `registry_completeness_checker.py`, `candidate_family_checker.py`,
  `metric_lock_checker.py`, `robustness_gate_checker.py` : 11 scenarios
  hostiles executes reellement (evidence absente/None/vide, reviewer
  manquant, incident LEVEL_4 ouvert, acces OOS non autorise, flags falsy,
  champ `None` des deux cotes d'une comparaison de verrou, stress-test
  post-hoc non declare) — tous `PASS_ADVERSARIAL`, aucun defaut trouve.
- `human_evidence.py` : 5 scenarios hostiles (payload absent, valeur truthy
  non strictement `True` pour `independence_attested`, `subject_id`
  incorrect, cle inconnue) — tous `PASS_ADVERSARIAL`.
- `bias_registry.py` : donnees statiques + deux lookups triviaux,
  `get_bias_risk` leve `KeyError` sur un id inconnu (fail-closed) — pas de
  scenario hostile pertinent au-dela de cette verification.
- `incident_logger.py` : **1 `SILENT_FALLBACK` confirme et corrige** —
  `load_incidents()` sur un fichier de log absent retournait `[]`,
  indiscernable d'un log verifie et genuinement vide. Confirme par
  execution directe (`load_incidents(chemin_absent)` -> `[]` avant
  correctif). Aucun appelant de production n'existe aujourd'hui pour
  `load_incidents`/`load_open_incidents` (verifie par grep exhaustif) —
  risque latent, pas encore exploite, mais le module est expose dans
  `governance/__init__.py.__all__` et designe comme detecteur de plusieurs
  biais dans `bias_registry.py`. Correctif : nouvelle exception
  `IncidentLogNotFound`, levee explicitement si le chemin n'existe pas ;
  un fichier existant et vide continue de retourner `[]` (etat verifie).
  Aucun appelant/test existant ne dependait du comportement precedent
  (grep confirme, aucun test pour ce module avant ce lot). Deux tests de
  regression ajoutes dans `test_governance_bias.py` (le fichier de test
  existant pour ce module, pas un nouveau fichier).

## Boucle `/evaluate` d'intake (2 passes, convergee)

**Passe 1** — Verification que le correctif `IncidentLogNotFound` ne casse
aucun appelant existant : grep exhaustif de `load_incidents`/
`load_open_incidents` dans tout `Implementation/` confirme zero appelant de
production, et les trois tests existants de `test_governance_bias.py` qui
utilisent ces fonctions appellent toujours `append_incident` avant
`load_incidents` (le fichier existe donc toujours a ce point). Precedent
retenu comme reference de conception : `package_validator.py:48`
(`missing_paths`) traite deja un `registry.jsonl`/`oos_access_log.jsonl`
manquant comme un echec explicite, jamais comme une liste vide silencieuse —
le correctif aligne `incident_logger.py` sur cette convention deja etablie
ailleurs dans le meme depot, il ne l'invente pas.

**Passe 2** — Verification que le perimetre reste borne a `governance/` et
ses tests (pas de fichier hors de ce perimetre modifie). Confirmation que le
format de preuve (lot 1) est respecte : le rapport sera redige dans le plan
final lui-meme (section 13), reference par `chemin#ancre`. Convergence a
2 passes sur 6 autorisees, aucun angle mort majeur trouve.
