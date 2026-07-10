# Plan de correction — Completer le pivot Nautilus (multi-fold reel + robustesse) et reconcilier l'etat machine

> Plan de correction (`fix`) produit a la suite d'un audit d'implementation du
> chantier mainline actif `PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS`
> (2026-07-10). L'audit a confirme que le coeur de l'adapter Nautilus (Briques
> N1-N5, contrats, migrations, golden-case, retrait du cluster natif) est reel,
> teste et fonctionnel, mais que deux livrables methodologiques declares `DONE`
> dans `Implementation/Active/tracking.json` n'existent pas sur disque, et que
> l'Exit criterion central du chantier (boucle multi-fold reelle) n'est pas
> atteint. Ce document ne reecrit pas le plan d'origine ; il le complete et
> corrige l'etat machine qui le decrit faussement comme termine.

---

## 0. Bandeau de statut (a verifier avant toute promotion)

| Question | Reponse |
| --- | --- |
| Un chantier actif couvre-t-il deja ce perimetre (`DONE`, `ACTIVE`, ou `SUPERSEDED`) ? | Oui — `PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS` est `ACTIVE` (checkpoint `active_workstream_id`). Ce plan-ci est un `fix` subordonne qui le complete, il ne le remplace pas et ne cree pas de chantier mainline concurrent. |
| Un verrou de gouvernance actif bloque-t-il ce chantier ? | Non nouveau. Le verrou d'origine (extension au-dela du MVP) a deja ete leve par les decisions D1-D6 pour ce perimetre. Ce plan reste dans le meme perimetre autorise (adapter Nautilus, `procedures/` inchange). Aucune nouvelle levee humaine requise pour les phases de code ; seule la Phase 0 (reconciliation de l'etat machine) doit preceder. |
| Ce plan a-t-il besoin d'une decision humaine explicite pour lever un verrou avant d'etre routable via `/start` ? | Non. La seule decision de conception (C1 : sort des deux relocalisations) est **tranchee** le 2026-07-10 : relocalisations acceptees telles quelles, `metrics/` supprime (section 4, section 10). |
| Ce plan remplace-t-il un document ou chantier existant ? | Non. Il complete `PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS` (qui reste `ACTIVE`) et corrige `Implementation/Active/tracking.json` / `.ai/checkpoint.json` la ou ils affirment un `DONE` faux. |

> Ce plan reste `TRIAGED` / `NON_DEMARRE` tant qu'il n'a pas ete passe a
> `/evaluate` (code-architecture-evaluator) et que la decision C1 n'est pas
> tranchee.

---

## Audit IA de promotion

- [x] Plan relu dans le contexte du cockpit actif (`AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json`, `Implementation/Active/HOOK.md`, `Implementation/Active/tracking.json`).
- [x] Bandeau de statut (section 0) rempli et verifie contre l'etat machine reel (2026-07-10), pas suppose.
- [x] Ecrit comme NOUVEAU fichier dans `.ai/backlog/fixes/` ; ne modifie pas le plan d'origine en place.
- [x] Chantier classe `fix` — corrige/complete un chantier mainline actif sans le remplacer ni ouvrir un second mainline concurrent.
- [x] Autorite normative identifiee : `Protocole/` (`EBTA-DOC-1.1`), en particulier SOP 04 (walk-forward) et SOP 05 (robustesse), prime sur ce document et sur Nautilus.
- [x] Perimetre de fichiers autorises et interdits explicite (section 1, section 8).
- [x] Aucune modification hors perimetre requise, hormis la reconciliation `tracking.json`/`checkpoint.json` traitee comme Phase 0.
- [x] Prerequis factuels identifies : venv Nautilus present et fonctionnel (verifie — package Nautilus mono-fold build `PASS` 2026-07-10) ; `procedures/walk_forward.py::validate_walk_forward_schedule()` et `procedures/robustness.py` existants et a reutiliser.
- [x] Etat des lieux (section 4) verifie ligne par ligne contre le disque et `git` reel (audit 2026-07-10).

## Triage

| Champ | Valeur |
| --- | --- |
| Track | fix |
| Lifecycle | TRIAGED |
| Scope | Livrer les deux briques methodologiques manquantes du pivot Nautilus (`data/walk_forward.py::WalkForwardSplitter` — SOP 04 ; `risk/robustness.py` calculateur de scenarios — SOP 05), transformer le `research_package` Nautilus mono-fold actuel en une vraie boucle multi-fold walk-forward avec split Train/Test/OOS reel via `run_segment()`, et reconcilier `Implementation/Active/tracking.json`/`.ai/checkpoint.json` pour qu'ils cessent de declarer `DONE` des livrables absents. |
| Non-goals | Ne pas modifier `Protocole/`, `procedures/`, `validators/`, `governance/`, `manifests/` ; ne pas creer de seconde implementation d'une procedure existante ; ne pas reintroduire le cluster natif retire ; ne pas importer `nautilus_trader` hors `adapters/` ; ne pas ajouter de dependance (NumPy compris) ; ne pas ouvrir OOS avant scellement + G-BIAS PASS ; ne pas utiliser une metrique Nautilus comme verdict EBTA. |
| Source | Audit d'implementation demande par l'humain le 2026-07-10 (« audite l'implementation du plan Nautilus, corrige si necessaire »), puis instruction « orchestre la correction via un plan de correction d'abord, que tu passeras a /evaluate ensuite ». |
| Exit criteria | (1) `data/walk_forward.py::WalkForwardSplitter` et `risk/robustness.py` existent, sont testes, et alimentent respectivement `procedures/walk_forward.py::validate_walk_forward_schedule()` et `procedures/robustness.py` sans les modifier. (2) Un `research_package/` est produit par une boucle multi-fold reelle (K >= 2 folds construits par `WalkForwardSplitter`, split Train/Test/OOS effectif, `run_segment()` appele par fold, concatenation OOS) et valide `PASS` par `validate_package_dir()`. (3) `tracking.json`/`checkpoint.json` ne contiennent plus aucun `DONE` sans livrable correspondant sur disque. (4) Suite runtime complete `PASS`, zero modification de `procedures/`, `validators/`, `governance/`, `manifests/`, `Protocole/`. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | NON_DEMARRE |
| Date de creation | 2026-07-10 |
| Date d'activation | - |
| Autorite normative | `Protocole/` (`EBTA-DOC-1.1`), en particulier SOP 04, SOP 05, SOP 07, SOP 12, SOP 13 |
| Autorite executable | `Implementation/ebta_engine/` (traduction subordonnee) |
| Changement normatif attendu | Aucun |
| Dependances externes | `nautilus_trader==1.230.0` (deja installe, venv reproductible existant), confine a `adapters/` — aucune nouvelle dependance |

---

## 1. Role de ce document et non-objectifs

| Element | Role |
| --- | --- |
| `Protocole/` | Autorite normative absolue. Inchange. |
| `Implementation/ebta_engine/procedures/`, `validators/`, `governance/`, `manifests/` | Traduction executable de la norme. Inchanges — ce fix les *alimente*, ne les modifie pas. |
| `Implementation/ebta_engine/adapters/nautilus_*.py` | Frontiere Nautilus existante, a etendre pour la boucle multi-fold. |
| `Implementation/examples/minimal_pilot_pipeline/build_research_package.py` | **Dans le perimetre autorise** : assembleur generique du `research_package`, aujourd'hui hardcode mono-fold (`walk_forward_schedule[0]` a plusieurs endroits). A etendre pour accepter K folds (hors `procedures/`, non normatif). Ajoute au perimetre suite a l'audit `/evaluate` (R1). |
| `research_package/` | Artefact de preuve final, a produire en version multi-fold reelle. |
| Ce plan | Carte de correction : quelles briques manquantes ecrire, ou, comment recabler le package en walk-forward reel, et comment remettre l'etat machine au vrai. |

Non-objectifs :

- ne pas reecrire `Protocole/` ni aucune SOP ;
- ne pas introduire de regle, seuil ou statut absent des SOP ;
- ne pas dupliquer une procedure existante (`validate_walk_forward_schedule`, `robustness`, `economic_gate`, `wrc`, `oos_confidence_interval`, `complexity_selection`, `candidate_matrix`) sous un nouveau chemin ;
- ne pas faire d'une metrique Nautilus une source de verdict ;
- ne pas importer `nautilus_trader` hors `adapters/` et de son point d'entree d'execution.

---

## 2. Contexte obligatoire a lire avant de coder

1. `AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json`, `Implementation/Active/HOOK.md`, `Implementation/Active/tracking.json` — etat machine (et son inexactitude a corriger).
2. `.ai/backlog/mainline/PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md` — le plan complete par ce fix (surtout sections 4, 5, 8 : contrats, invariants, NO GO).
3. `Protocole/` SOP 04 (walk-forward : purge, embargo, warm-up, non-recouvrement OOS), SOP 05 (robustesse : scenarios CENTRAL/PLAUSIBLE_BASE/EXTREME), SOP 07 (detrending/zero-centering), SOP 12 (scellement), SOP 13 (G-BIAS).
4. `Implementation/PROCEDURE_CALCULATION_MAP.md` — mapping SOP -> `procedures/`, a ne jamais dupliquer.
5. Code existant a reutiliser (verifie 2026-07-10) : `procedures/walk_forward.py::validate_walk_forward_schedule()`, `procedures/robustness.py`, `procedures/economic_gate.py`, `procedures/complexity_selection.py`, `procedures/candidate_matrix.py`, `procedures/wrc.py`, `procedures/oos_confidence_interval.py`, `adapters/nautilus_mapping.py::run_segment()`/`run_multifold_segments()`, `strategies/contracts.py::SimulationResult`.
6. Skill `nautilus-docs-research` — avant tout nouvel appel `nautilus_trader` non deja verifie.

**Hierarchie d'autorite** :

```text
1. Protocole/MANIFESTE DE GEL EBTA.md
2. Protocole/PROTOCOLE EBTA.md
3. Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md
4. SOP 01-13
5. Protocole/PAQUET D'EXECUTION EBTA.md
6. Implementation/ (dont ce plan)
7. Adaptateurs externes (NautilusTrader)
```

Regle : si le code contredit `Protocole/`, c'est le code qui a tort. Si une regle manque, bloquer / retourner `INCONCLUSIVE` plutot que deviner.

---

## 3. Table des gates

Ce fix ne change ni l'ordre ni le sens d'aucune gate. Il retablit seulement que
les gates `G4`/`G5`/`G6`/`G9`/`G10` s'appliquent a *chaque fold reel* d'une
vraie boucle walk-forward, et non a un fold unique herite du pilote minimal. La
table des gates de reference reste celle du plan d'origine (section 3) ; se
reporter a `.ai/backlog/mainline/PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md`.

---

## 4. Etat des lieux (avant/apres) — reutiliser avant de recreer

### Ce qui existe deja et fonctionne (verifie 2026-07-10)

| Module | Chemin | Role reel (verifie) | Suffisant ? |
| --- | --- | --- | --- |
| Contrats | `strategies/contracts.py` | `SimulationResult`, `CostModel`, `InstrumentConfig`, `Candidate` ; expose aussi `SimulationResult.economic_gate_evidence()` et `detrending_inputs()` | ✅ Reutiliser tel quel |
| Adapter mapping | `adapters/nautilus_mapping.py` | `map_ohlcv_to_bars`, `build_instrument`, `map_cost_model_to_venue`, `run_segment`, `extract_simulation_result`, `run_multifold_segments` | ✅ Reutiliser ; etendre l'appelant, pas ces fonctions |
| Pont strategie | `adapters/nautilus_strategy_bridge.py` | `GenericPayloadStrategy` unique | ✅ Inchange |
| CLI segment | `adapters/nautilus_segment_cli.py` | Frontiere subprocess (isolation venv / MAX_PATH) | ✅ Inchange |
| Validation calendrier | `procedures/walk_forward.py::validate_walk_forward_schedule()` | Valide un calendrier deja construit (overlap, purge, embargo) | ✅ A appeler apres construction, jamais dupliquer |
| Validation robustesse | `procedures/robustness.py` | Valide un verdict deja classifie (CENTRAL/PLAUSIBLE_BASE/EXTREME) | ✅ A alimenter, jamais dupliquer |
| Gate economique | `procedures/economic_gate.py` | Agrege des flags deja calcules | ✅ Alimente par `SimulationResult.economic_gate_evidence()` |
| Package Nautilus | `package_builder/nautilus_research_package.py` | Build un package Nautilus-alimente **mono-fold** (herite `FOLD-001` du pilote) | ⚠️ A recabler en multi-fold reel (Phase 3) |
| Package pilote | `examples/minimal_pilot_pipeline/build_research_package.py` | Assemblage generique (un seul fold dans le pilote) | ✅ Machinerie d'assemblage reutilisee ; le multi-fold vient de l'appelant Nautilus |

### Divergences constatees (relocalisations fonctionnelles — decision C1 tranchee 2026-07-10 : ACCEPTEES)

| Livrable annonce par le plan | Etat reel | Verdict acte (C1) |
| --- | --- | --- |
| `strategies/generator.py` (boucle multi-fold) | N'existe pas ; la boucle est `adapters/nautilus_mapping.py::run_multifold_segments()` (boucle sur folds deja declares, ne les construit pas) | **ACCEPTE** : `run_multifold_segments()` reste la boucle d'execution ; la construction de folds manquante est ajoutee par `WalkForwardSplitter` (Phase 1). Pas de `strategies/generator.py`. |
| `metrics/economic_gate.py` (calcul brut) | N'existe pas ; remplace par la methode `SimulationResult.economic_gate_evidence()` ([contracts.py:160](../../Implementation/ebta_engine/strategies/contracts.py)) | **ACCEPTE** : methode sur le contrat conservee. Consequence : le package `metrics/` (vide, `__pycache__` seul) est **supprime** definitivement (Phase 4), pas recree. |

### Ce qui manque reellement (declare DONE, absent du disque)

| Brique manquante | Module a creer | Source | A reutiliser (pas dupliquer) |
| --- | --- | --- | --- |
| Construction des folds depuis les barres (purge, embargo, warm-up, non-recouvrement OOS) | `data/walk_forward.py::WalkForwardSplitter` | SOP 04 | `procedures/walk_forward.py::validate_walk_forward_schedule()` (validation du calendrier produit) |
| Calcul des scenarios de stress classifies | `risk/robustness.py` | SOP 05 | `procedures/robustness.py` (validateur de verdict) |
| Boucle multi-fold reelle branchee sur Nautilus (split Train/Test/OOS, WRC par fold, concat OOS) | recablage de `package_builder/nautilus_research_package.py` (+ eventuel `strategies/generator.py` selon C1) | SOP 03, 04, 06, 10 | `run_segment`/`run_multifold_segments`, `complexity_selection`, `candidate_matrix`, `wrc`, `oos_confidence_interval` |

### Hygiene a traiter

- Dossiers-packages devenus vides (seulement `__pycache__` orphelins) apres retrait du cluster natif : `risk/`, `metrics/`, `backtest/`, `features/`, `trading_signals/`.
  - `risk/` est **recree** (Phase 2 : `risk/robustness.py` + `risk/__init__.py`).
  - `metrics/`, `backtest/`, `features/`, `trading_signals/` sont **supprimes** (Phase 4), y compris leurs `__pycache__` orphelins — aucun code ne les reutilise (decision C1 : economique = methode de contrat).

---

## 5. Decision d'architecture

Principe directeur : ce fix ne change pas la frontiere « moteur Nautilus aveugle
au protocole / couche de controle EBTA » deja posee par le plan d'origine. Il la
complete a l'endroit ou elle a ete court-circuitee : aujourd'hui le package
Nautilus contourne la boucle walk-forward en reutilisant le squelette statique
mono-fold du pilote. La correction consiste a faire remonter la construction des
folds (SOP 04) et des scenarios de robustesse (SOP 05) dans la couche de
controle EBTA, puis a piloter `run_segment()` par fold reel.

- Raison 1 — sans `WalkForwardSplitter`, l'invariant SOP 04 (jamais de Test/OOS dans Train) n'est jamais exerce : un fold unique herite du pilote ne teste pas la separation temporelle.
- Raison 2 — sans `risk/robustness.py`, `procedures/robustness.py` valide un verdict statique du pilote, pas des scenarios reellement derives des `SimulationResult` Nautilus : le gate G5 est alors decoratif.
- Raison 3 — le contrat entre couches (`SimulationResult`) existe deja et est teste ; aucun nouveau contrat n'est requis, seulement de nouveaux producteurs (folds, scenarios) et un orchestrateur multi-fold reel.

### Frontieres explicites

| Couche | Elle fait | Elle NE fait PAS |
| --- | --- | --- |
| `WalkForwardSplitter` (nouveau) | Decoupe `list[OhlcvBar]` en K folds `{train_bars, test_bars, oos_bars}` avec purge/embargo/warm-up SOP 04, produit le calendrier passe a `validate_walk_forward_schedule()` | Executer Nautilus ; connaitre WRC/gates ; transmettre autre chose que `train_bars` au generateur de candidates |
| `risk/robustness.py` (nouveau) | Deriver les scenarios CENTRAL/PLAUSIBLE_BASE/EXTREME depuis les `SimulationResult`, produire le verdict classifie attendu par `procedures/robustness.py` | Recalculer WRC ou l'IC OOS ; decider PASS/FAIL du gate (c'est `procedures/robustness.py`) |
| Orchestrateur multi-fold | Boucler sur les folds, appeler `run_segment()` par Test_k puis OOS_k (si gates franchies), concatener l'OOS global, brancher `procedures/` | Calculer PnL/fills/NAV (Nautilus) ; trancher un gate (procedures) |

### Contrat d'interface

Aucun nouveau contrat. `SimulationResult` (existant, `strategies/contracts.py`)
reste l'unique objet echange. `WalkForwardSplitter` produit une structure de
folds interne alimentant `validate_walk_forward_schedule()` selon le schema
`walk_forward_declaration.schema.json` existant (aucune migration de schema).

### Decisions deja actees

| Decision | Justification |
| --- | --- |
| Reutiliser `run_multifold_segments()` comme boucle d'execution, y ajouter en amont la construction de folds `WalkForwardSplitter` | Evite un `strategies/generator.py` concurrent ; la boucle existe deja, seul le producteur de folds manque |
| `risk/robustness.py` produit un verdict, `procedures/robustness.py` le valide | Respecte la separation calcul/validation deja etablie pour l'economique |
| Le split Train/Test/OOS reste entierement cote EBTA ; `run_segment()` ne recoit jamais l'etiquette de segment | Invariant 6 du plan d'origine (aucune fuite de segment dans Nautilus) |

### Structure cible

```text
Implementation/
  examples/minimal_pilot_pipeline/
    build_research_package.py     # ETENDU -- assembleur accepte K folds (R1)
  ebta_engine/
    data/
      walk_forward.py        # NOUVEAU -- WalkForwardSplitter (SOP 04)
      local_ohlcv.py          # EXISTANT
    risk/
      __init__.py             # RECREE
      robustness.py           # NOUVEAU -- calcul scenarios de stress (SOP 05)
    adapters/
      nautilus_mapping.py      # EXISTANT -- run_segment / run_multifold_segments reutilises
    package_builder/
      nautilus_research_package.py  # RECABLE -- vraie boucle multi-fold
    metrics/                 # SUPPRIME (C1 : economique = methode de contrat)
    backtest/, features/, trading_signals/  # SUPPRIMES (packages fantomes post-retrait natif)
    procedures/, validators/, governance/, manifests/, schemas/  # INCHANGES
```

---

## 6. Decoupage en phases

### Phase 0 - Reconciliation de l'etat machine et decision de relocalisation

Objectif : remettre `tracking.json`/`checkpoint.json` au vrai et trancher le sort des deux relocalisations avant toute phase de code.

Classification : GOVERNANCE

Constat (preuve) :

- `Implementation/Active/tracking.json` marque `NAUTILUS_P5_T3_MULTIFOLD_ORCHESTRATION` et les Phases 5/6 `DONE`, en listant `strategies/generator.py`, `data/walk_forward.py`, `risk/robustness.py`, `metrics/economic_gate.py` comme livres — 2 n'existent pas (verifie sur disque 2026-07-10).
- La Definition of Done du plan d'origine (section 12) est entierement decochee et la Cloture (section 13) est vide, ce qui contredit le `DONE` du tracking.

Actions :

- Corriger `Implementation/Active/tracking.json` : requalifier la partie multi-fold/robustesse de `NAUTILUS_P5_T3` et l'Exit criterion multi-fold comme non atteints (statut a re-derver mecaniquement via `.ai/tools/tasks_from_plan.ps1` a partir de ce plan, ou manuellement selon `tracking.schema.json`).
- Mettre `.ai/checkpoint.json` en coherence (chantier Nautilus reste `ACTIVE`, ce fix reference comme sous-chantier de correction).
- Trancher la decision C1 (section 10) : accepter les relocalisations `run_multifold_segments()` et `economic_gate_evidence()`, ou realigner sur les noms du plan.

Livrables :

- `tracking.json` et `checkpoint.json` sans `DONE` sans livrable correspondant.
- Decision C1 tracee (section 10).

Critere de sortie :

- `python -m json.tool Implementation\Active\tracking.json` et `python -m json.tool .ai\checkpoint.json` PASS.
- Validation schema des deux fichiers PASS.
- Aucune tache marquee `DONE` ne reference un fichier absent du disque (verification par inspection).

### Phase 1 - Brique SOP 04 : WalkForwardSplitter

Objectif : construire les folds walk-forward depuis les barres, alimentant le validateur de calendrier existant sans le modifier.

Classification : IMPLEMENTATION_DETAIL

Actions :

- Ecrire `data/walk_forward.py::WalkForwardSplitter` : decoupe `list[OhlcvBar]` en K folds avec purge, embargo, warm-up et non-recouvrement OOS conformes SOP 04.
- Produire le calendrier au format attendu par `procedures/walk_forward.py::validate_walk_forward_schedule()` et le valider (jamais dupliquer la validation).
- Ne transmettre que `train_bars` au generateur de candidates (invariant SOP 04).

Livrables :

- `data/walk_forward.py::WalkForwardSplitter` teste (voir Annexe 6bis).
- `tests/test_walk_forward_splitter.py` (`unittest.TestCase`) : purge, embargo, warm-up, non-recouvrement OOS, K >= 2, calendrier accepte par `validate_walk_forward_schedule()`.

Critere de sortie :

- `WalkForwardSplitter` produit K >= 2 folds sur une serie synthetique ; `validate_walk_forward_schedule()` accepte le calendrier produit — PASS.
- Test prouvant qu'aucune barre Test/OOS n'apparait dans `train_bars` — PASS.
- Suite runtime complete reste PASS.

### Phase 2 - Brique SOP 05 : calculateur de robustesse

Objectif : deriver les scenarios de stress classifies depuis les `SimulationResult`, alimentant `procedures/robustness.py` sans le modifier.

Classification : IMPLEMENTATION_DETAIL

Actions :

- Ecrire `risk/robustness.py` : calcul des scenarios CENTRAL/PLAUSIBLE_BASE/EXTREME a partir des `SimulationResult`, production de la **liste** de scenarios (cles `stress_id`/`classification`/`scenario_verdict`/`blocking`) attendue par `procedures/robustness.py::pre_oos_robustness_verdict()` (voir Annexe 6bis, R3).
- Fixer le nombre de `run_segment()` par scenario et confirmer qu'ils portent **sur Test uniquement** (jamais OOS avant scellement) ; integrer ce cout au budget `K x (M+1)`.
- Recreer `risk/__init__.py` (dossier vide apres retrait natif).

Livrables :

- `risk/robustness.py` teste (voir Annexe 6bis).
- `tests/test_risk_robustness.py` : scenarios classifies corrects sur cas connu, verdict consomme sans modification par `procedures/robustness.py`.

Critere de sortie :

- `procedures/robustness.py` valide un verdict produit par `risk/robustness.py` sur un cas synthetique a verite connue — PASS.
- Aucune regle de classification absente des SOP inventee (si un seuil manque, bloquer / `INCONCLUSIVE`).
- Suite runtime complete reste PASS.

> **Correction /evaluate (R1/R4)** : la « Phase 3 » d'origine etait sous-dimensionnee — elle presentait comme un simple « recablage » la construction de la boucle scientifique EBTA qui n'a jamais existe (le package actuel reinjecte WRC/OOS/scellement/robustesse depuis le squelette **statique** du pilote, [nautilus_research_package.py:113-138](../../Implementation/ebta_engine/package_builder/nautilus_research_package.py)). Elle est scindee en 3a/3b/3c, avec la strategie d'execution tranchee en tete.

### Phase 3a - Assembleur multi-fold et strategie d'execution

Objectif : lever les deux bloqueurs de la boucle reelle avant d'ecrire la boucle : l'assembleur pilote hardcode mono-fold, et le cout d'execution K x (M+1).

Classification : ADAPTER_MAPPING

Constat (preuve) :

- L'assembleur `pilot.build_package()` est hardcode mono-fold : `pilot_inputs["walk_forward_schedule"][0]` a [build_research_package.py:164,342,434,504](../../Implementation/examples/minimal_pilot_pipeline/build_research_package.py). Une boucle K >= 2 est impossible sans le lever.
- Chaque `run_segment()` passe par un subprocess Nautilus isole avec `timeout=120` ([nautilus_research_package.py:225-254](../../Implementation/ebta_engine/package_builder/nautilus_research_package.py)) ; K x M x (Test+OOS) multiplie les spawns process.

Actions :

- Etendre `examples/minimal_pilot_pipeline/build_research_package.py::build_package()` pour accepter un `walk_forward_schedule` a K entrees et assembler les artefacts multi-fold (concat OOS incluse), sans toucher `procedures/`.
- Trancher la strategie d'execution : reutilisation d'un `BacktestEngine` via `engine.reset()` entre segments d'un meme fold (Brique N4 le prevoit deja) OU subprocess par segment, en s'appuyant sur la mesure du spike Phase 2 d'origine ; documenter le choix et l'extrapolation `K x (M+1)`.

Livrables :

- `build_package()` multi-fold teste (fold unique => resultat identique a l'existant, non-regression).
- Note de decision execution + extrapolation temps.

Critere de sortie :

- `build_package()` accepte K >= 2 folds et reste identique a l'existant pour K = 1 — PASS (test de non-regression).
- Strategie d'execution documentee, budget temps `K x (M+1)` sous le `timeout` par segment.

### Phase 3b - Boucle scientifique reelle par fold

Objectif : ecrire la vraie boucle EBTA par fold, remplacant la reinjection statique.

Classification : ADAPTER_MAPPING

Actions :

- Recabler `package_builder/nautilus_research_package.py` pour : appeler `WalkForwardSplitter` (Phase 1), boucler sur K folds via `run_multifold_segments()` (relocalisation acceptee C1), generer les candidates sur `train_bars`, evaluer `Test_k`, selectionner la complexite (`complexity_selection`), construire la matrice (`candidate_matrix`), passer WRC (`wrc`), sceller, gate G-BIAS, puis evaluer `OOS_k` seulement si les gates sont franchies (sinon `NO_MODEL` conserve dans l'OOS global).
- Conserver l'isolation venv/subprocess existante (`nautilus_segment_cli.py`).

Livrables :

- `package_builder/nautilus_research_package.py` recable multi-fold.
- `tests/test_nautilus_multifold_package.py` : build multi-fold (K >= 2, `segment_runner` fake pour la suite hors-venv, sur le patron `_fake_segment_runner` existant), `NO_MODEL` conserve dans l'OOS global, aucune fuite de segment vers `run_segment()`.

Critere de sortie :

- WRC, scellement, G-BIAS, concat OOS s'executent reellement par fold (plus de reinjection statique du pilote) — verifie par test.
- Tests `NO_MODEL` conserve et absence de fuite de segment — PASS.

### Phase 3c - Cablage robustesse et economique multi-fold

Objectif : brancher `risk/robustness.py` (Phase 2) et `SimulationResult.economic_gate_evidence()` sur les donnees Nautilus multi-fold reelles.

Classification : ADAPTER_MAPPING

Actions :

- Alimenter `procedures/robustness.py` via `risk/robustness.py` avec des scenarios reellement derives des `SimulationResult` multi-fold (jamais un reformatage statique).
- Alimenter `procedures/economic_gate.py` via `SimulationResult.economic_gate_evidence()` sur donnees multi-fold.

Livrables :

- `reports/robustness.json` et `reports/economic.json` derives de donnees Nautilus multi-fold reelles.

Critere de sortie :

- `research_package/` produit par une boucle multi-fold reelle (K >= 2) valide `PASS` par `validate_package_dir()` — via le venv Nautilus reel.
- Detrending, WRC, IC OOS, gate economique, robustesse tournent sur donnees Nautilus multi-fold sans modification de signature.

### Phase 4 - Cloture et coherence finale

Objectif : verifier l'Exit criterion complet et fermer honnetement l'etat machine.

Classification : GOVERNANCE

Actions :

- Cocher la Definition of Done du plan d'origine (section 12) et remplir sa Cloture (section 13) uniquement si tout est reellement PASS.
- Mettre a jour `tracking.json`/`checkpoint.json` : phases de ce fix `DONE` seulement apres preuve executable.
- Nettoyer les dossiers/`__pycache__` orphelins (`backtest/`, `features/`, `trading_signals/`).
- Executer la checklist post-modification `.ai/governance/AI_MODIFICATION_CHECKLIST.md`.

Livrables :

- Etat machine coherent (aucun `DONE` sans livrable).
- Package multi-fold `PASS` reproductible.

Critere de sortie :

- Toutes les commandes de la section 9 PASS.
- Zero modification de `procedures/`, `validators/`, `governance/`, `manifests/`, `Protocole/` sur l'ensemble du fix (verifie par `git diff --stat`).

## 6bis. Annexe — Specifications techniques

### WalkForwardSplitter (`data/walk_forward.py`, Phase 1)

**Role** : SOP 04 — construction des folds.

```python
def build_folds(
    bars: list[OhlcvBar],
    *,
    n_folds: int,          # K >= 2
    train_size: int,
    test_size: int,
    oos_size: int,
    purge_days: int,        # R2 : noms *_days (lus par validate_walk_forward_schedule)
    embargo_days: int,
    warmup_days: int,
) -> list[dict]:
    """Retourne K folds {fold_id, train_bars, test_bars, oos_bars}.
    Aucune barre Test/OOS ne peut apparaitre dans train_bars.
    Le calendrier produit doit exposer purge_days/embargo_days/warmup_days
    et passer procedures/walk_forward.py::validate_walk_forward_schedule()."""
```

- **R2 (correction /evaluate)** : `validate_walk_forward_schedule()` lit exactement `purge_days`, `embargo_days`, `warmup_days` ([walk_forward.py:40-42,110](../../Implementation/ebta_engine/procedures/walk_forward.py)) — le splitter doit emettre ces cles, jamais `purge`/`embargo`/`warmup`.
- **Invariants interdits a violer** : recouvrement OOS entre folds ; barre future dans Train ; purge/embargo ignores.
- **Test** : `tests/test_walk_forward_splitter.py`.

### risk/robustness.py (Phase 2)

**Role** : SOP 05 — scenarios de stress classifies.

```python
def compute_robustness_scenarios(
    results_by_scenario: dict[str, list[SimulationResult]],
    *,
    scenario_grid: dict,
) -> list[dict]:
    """Produit la liste de scenarios consommee (non recalculee) par
    procedures/robustness.py::pre_oos_robustness_verdict(). Chaque dict doit
    contenir au minimum les cles lues par le validateur :
      - stress_id            (str)
      - classification       (str) : CENTRAL | PLAUSIBLE_BASE | EXTREME
      - scenario_verdict     (str) : verdict derive des SimulationResult
      - blocking             (bool)
      - influential_variant  (bool, optionnel)
    """
```

- **R3 (correction /evaluate)** : ces cles sont exactement celles lues par `pre_oos_robustness_verdict()` ([robustness.py:50-54,82,101-103](../../Implementation/ebta_engine/procedures/robustness.py)). Sortie = **liste** de dicts (pas un dict unique).
- **Runs par scenario** : chaque scenario (variation couts/slippage/latence) = un ou plusieurs `run_segment()` **sur Test uniquement** — jamais sur OOS avant scellement (invariant SOP 05/10). Le nombre exact de runs par scenario est fixe en Phase 2 et compte dans le budget `K x (M+1)`.
- **Invariants interdits a violer** : recalculer WRC/IC OOS ; trancher le gate (role de `procedures/robustness.py`) ; inventer un seuil absent de SOP 05 ; deriver un scenario depuis des barres OOS avant scellement.
- **Test** : `tests/test_risk_robustness.py`.

---

## 7. Artefacts produits

Memes artefacts que le plan d'origine (section 7), mais produits par une boucle
multi-fold reelle. Nouveaux artefacts propres a ce fix :

| Etape | Fichier/sortie | Format | Regle source |
| --- | --- | --- | --- |
| Construction folds | calendrier multi-fold passe a `validate_walk_forward_schedule()` -> `reports/fold_schedule.json` (K >= 2) | JSON | SOP 04 |
| Robustesse reelle | `reports/robustness.json` alimente par `risk/robustness.py` | JSON | SOP 05 |
| Etat machine corrige | `Implementation/Active/tracking.json`, `.ai/checkpoint.json` | JSON schema-contraint | Gouvernance `.ai/` |

---

## 8. Invariants absolus et NO GO

### Invariants

Reprennent integralement ceux du plan d'origine (section 8, invariants 1-8),
avec ce fix responsable de les rendre reellement exerces :

1. Jamais de Test/OOS dans Train — desormais garanti par `WalkForwardSplitter` (et non plus contourne par un fold unique).
2. `run_segment()` ne recoit jamais l'etiquette de segment (invariant 6 d'origine).
3. `NO_MODEL` conserve dans l'OOS global.
4. Zero-centering sur Test, interdit sur OOS (`assert_not_oos_zero_centering()`).
5. La distribution bootstrap WRC n'est jamais reutilisee pour l'IC OOS.

### NO GO

- Modifier `procedures/`, `validators/`, `governance/`, `manifests/`, `Protocole/`.
- Creer une seconde implementation de `validate_walk_forward_schedule`, `robustness`, `economic_gate`, `wrc`, `oos_confidence_interval`, `complexity_selection`, `candidate_matrix`.
- Reintroduire un import du cluster natif retire.
- Importer `nautilus_trader` hors `adapters/`.
- Ajouter une dependance (NumPy compris).
- Produire un package mono-fold en le declarant multi-fold.
- Marquer une tache `DONE` sans livrable sur disque.
- Coder une regle de fold ou de robustesse absente de SOP 04 / SOP 05.

---

## 9. Verification a chaque etape

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
python -m json.tool Implementation\Active\tracking.json
python -m json.tool .ai\checkpoint.json
python -c "import json, jsonschema; jsonschema.validate(json.load(open('.ai/checkpoint.json', encoding='utf-8')), json.load(open('.ai/checkpoint.schema.json', encoding='utf-8')))"
python -c "import json, jsonschema; jsonschema.validate(json.load(open('Implementation/Active/tracking.json', encoding='utf-8')), json.load(open('Implementation/Active/tracking.schema.json', encoding='utf-8')))"
git diff --stat -- Implementation\ebta_engine\procedures Implementation\ebta_engine\validators Implementation\ebta_engine\governance Implementation\ebta_engine\manifests Protocole
```

Build multi-fold reel (via venv Nautilus) :

```powershell
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m ebta_engine.package_builder.nautilus_research_package
```

Validation du package produit :

```python
from pathlib import Path
from ebta_engine.validators.package_validator import validate_package_dir
report = validate_package_dir(Path("Implementation/research_packages/nautilus_mvp"))
print(report["status"])  # attendu : PASS, sur >= 2 folds
```

**Regle transversale bloquante** : la suite runtime doit rester PASS avant de
demarrer chaque phase suivante.

**Premier lot executable propose** :

```text
Phase 0 - Reconciliation de l'etat machine et decision de relocalisation
```

---

## 10. Journal des decisions humaines (autorisations)

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-10 | Audit Nautilus demande, correction orchestree via un plan de correction passe ensuite a `/evaluate` | Autorise la redaction de ce plan `fix` ; n'autorise pas encore l'execution des phases de code (attend directive `/start`) |
| 2026-07-10 | C1 **tranchee** : ACCEPTER les relocalisations `run_multifold_segments()` (boucle) et `SimulationResult.economic_gate_evidence()` (methode de contrat) telles quelles | Pas de `strategies/generator.py` ni `metrics/economic_gate.py` ; `metrics/` supprime. Justification : les deux sont fonctionnels/testes ; realigner serait du churn et ressusciterait un package `metrics/` inutile. Aucun invariant/NO GO viole. |

---

## 11. Risques et blocages connus

| Risque | Impact | Mitigation |
| --- | --- | --- |
| Encodage incorrect d'une regle SOP 04/05 (purge/embargo/scenario) | Fold ou robustesse invalides silencieusement | Lecture SOP 04/05 obligatoire ; alimenter les validateurs existants qui rejetteront un calendrier/verdict non conforme ; bloquer plutot que deviner |
| Volume `K x (M+1)` reel avec K >= 2 folds x M=16 | Temps d'execution multiplie | Reutiliser la mesure du spike Phase 2 d'origine ; `streaming=True` disponible si necessaire |
| MAX_PATH / chargement `.pyd` | Nautilus non fonctionnel depuis le chemin reel | Convention `subst` + venv reproductible deja en place (inchangee) |
| Reecriture `tracking.json`/`checkpoint.json` introduisant une incoherence de schema | Etat machine invalide | Validation schema apres chaque edition (section 9) |

---

## 12. Definition of Done

- [x] Phases 0 a 4 validees individuellement (section 9).
- [x] Exit criteria de la section Triage atteint (K >= 2 folds reels, `validate_package_dir()` PASS, `WalkForwardSplitter` + `risk/robustness.py` testes et branches, etat machine sans `DONE` faux).
- [x] Aucune modification de `procedures/`, `validators/`, `governance/`, `manifests/`, `Protocole/`.
- [x] Aucune regression sur la suite runtime.
- [x] Definition of Done et Cloture du plan d'origine remplies coherentes avec la realite.
- [x] Checklist `.ai/governance/AI_MODIFICATION_CHECKLIST.md` executee.

---

## 13. Cloture

A remplir au moment de `/close` :

| Champ | Valeur |
| --- | --- |
| Resultat final | DONE - Phases 0 a 4 executees. `WalkForwardSplitter` SOP 04, `risk/robustness.py` SOP 05 et boucle Nautilus K=2 multi-fold reelle sont presents sur disque, testes et branches dans le `research_package` pilote. |
| Ecarts par rapport au plan initial | C1 conservee : `run_multifold_segments()` et `SimulationResult.economic_gate_evidence()` restent les localisations acceptees. Aucun `strategies/generator.py` ni `metrics/economic_gate.py` n'a ete cree. La commande venv de build doit etre lancee depuis `Implementation\` avec `.\adapters\nautilus_env\venv\Scripts\python.exe -m ebta_engine.package_builder.nautilus_research_package`. |
| Suites a prevoir | Hors perimetre de cette correction : augmenter K, les fenetres temporelles et la grille de stress pour une campagne de recherche production, apres preregistration explicite. Aucun blocage residuel pour clore le chantier Nautilus MVP. |

---

## 14. Journal d'audits post-hoc

| Date de l'audit | Ce qui a ete corrige | Pourquoi |
| --- | --- | --- |
| 2026-07-10 | Creation de ce plan `fix` a la suite de l'audit du chantier Nautilus | `tracking.json` declarait `DONE` 2 livrables absents (`data/walk_forward.py`, `risk/robustness.py`) et un Exit criterion multi-fold non atteint (package Nautilus mono-fold) ; 2 autres livrables relocalises sans traçabilite |
| 2026-07-10 (`/evaluate`) | R1 : Phase 3 scindee en 3a/3b/3c ; assembleur pilote mono-fold (`build_research_package.py`) ajoute au perimetre autorise | La « Phase 3 » presentait comme un recablage la construction de la boucle scientifique EBTA jamais ecrite, et ignorait le couplage dur a `pilot.build_package()` hardcode `[0]` |
| 2026-07-10 (`/evaluate`) | R2 : contrat `WalkForwardSplitter` corrige en `purge_days`/`embargo_days`/`warmup_days` | Noms exacts lus par `validate_walk_forward_schedule()` — sans le suffixe le calendrier est rejete |
| 2026-07-10 (`/evaluate`) | R3 : sortie `risk/robustness.py` figee en liste de dicts `{stress_id, classification, scenario_verdict, blocking}`, runs par scenario sur Test uniquement | Cles exactes lues par `pre_oos_robustness_verdict()` ; eviter un reformatage statique (meme defaut qu'aujourd'hui) |
| 2026-07-10 (`/evaluate`) | R4 : strategie d'execution (engine reutilise vs subprocess) tranchee en tete de Phase 3a | `timeout=120` par segment + K x (M+1) spawns process = risque de timeout non adresse |
| 2026-07-10 (`/evaluate`) | R5 + C1 : `metrics/` supprime (economique = methode de contrat), `backtest/`/`features/`/`trading_signals/` supprimes | Packages fantomes post-retrait natif ; aucun code ne les reutilise |
