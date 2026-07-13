# Plan d'implementation — Experience controlee de discrimination des gates Nautilus (candidat gagnant vs perdant)

> Ce plan repond a une question posee en aval de la cloture du chantier
> `PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS` (2026-07-10) et de sa
> correction (`PLAN_CORRECTION_NAUTILUS_MULTIFOLD_ROBUSTESSE`) : l'audit
> d'implementation de ces deux plans a confirme que la boucle multi-fold
> Nautilus tourne reellement (K=2 folds, `validate_package_dir()` PASS), mais
> a aussi releve (reserve M4 de l'audit) que ce PASS ne prouve que la
> **plomberie**, pas la **discrimination** : le package MVP utilise des couts
> nuls, des rendements OOS plats, et une grille de robustesse quasi
> permissive (`minimum_mean_return: -1.0`, tout passe). Rien ne prouve
> aujourd'hui que les gates rejetteraient reellement un mauvais candidat.
> Ce plan cadre une experience a verite connue (un candidat synthetique
> gagnant, un candidat synthetique perdant) pour verifier cela sur le
> pipeline Nautilus MVP reel, sans modifier ce pipeline ni la norme.

---

## 0. Bandeau de statut (a verifier avant toute promotion)

| Question | Reponse |
| --- | --- |
| Un chantier actif couvre-t-il deja ce perimetre (`DONE`, `ACTIVE`, ou `SUPERSEDED`) ? | Non. `PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS` est `DONE` (checkpoint `active_workstream_id: null`) ; ce plan est une experience de validation complementaire, distincte, classee `annexe`. |
| Un verrou de gouvernance actif bloque-t-il ce chantier ? | Non. Aucun verrou de `Implementation/Active/HOOK.md` ne concerne une extension de validation post-cloture. Ce plan ne modifie ni n'etend le perimetre MVP livre. |
| Ce plan a-t-il besoin d'une decision humaine explicite pour lever un verrou avant d'etre routable via `/start` ? | Non. Il n'existe pas de brouillon dans `0 - HUMAN START HERE/` : ce plan est redige directement a la demande humaine formulee en conversation le 2026-07-10 (« lancer une experience controlee pour voir si ca marche vraiment »), selon le meme precedent que `PLAN_CORRECTION_NAUTILUS_MULTIFOLD_ROBUSTESSE.md`. Passe a `/evaluate` (`code-architecture-evaluator`) le 2026-07-10 (4 corrections appliquees, section 14), execute jusqu'au bout et cloture `DONE` le meme jour — verifie independamment (110->116 tests PASS, deux executions reelles via le venv Nautilus donnant des resultats numeriquement identiques). N'a jamais ete enregistre comme workstream dans `.ai/checkpoint.json` (meme precedent que le plan de correction) : sa cloture se fait dans ce document, pas via `.ai/tools/plan.ps1 close`. |
| Ce plan remplace-t-il un document ou chantier existant ? | Non. Il ne remplace rien et ne rouvre pas `PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS` (reste `DONE`). |

---

## Audit IA de promotion

- [x] Plan relu dans le contexte du cockpit actif (`AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json`, `Implementation/Active/HOOK.md`, `Implementation/Active/tracking.json`).
- [x] Bandeau de statut (section 0) rempli et verifie contre l'etat machine reel (chantier Nautilus `DONE`, aucun verrou actif), pas suppose.
- [x] Ecrit comme NOUVEAU fichier dans `.ai/backlog/annexes/` ; ne modifie aucun plan existant.
- [x] Chantier classe `annexe` — experience de validation complementaire, ne fait pas partie de la mainline et ne corrige aucun etat faux (contrairement au `fix` precedent).
- [x] Autorite normative identifiee : `Protocole/` (`EBTA-DOC-1.1`), en particulier SOP 08 (gate economique) et SOP 05 (robustesse), prime sur ce document.
- [x] Perimetre de fichiers autorises et interdits explicite (section 1, section 8).
- [x] Aucune modification hors perimetre requise.
- [x] Prerequis factuels verifies sur le code reel (2026-07-10) : voir section 4 — `economic_gate_report()` n'agrege que des booleens deja calcules par l'appelant, il ne les calcule pas lui-meme ; `nautilus_research_package.py` les code aujourd'hui en dur a `True` (verifie ligne par ligne, section 4).
- [x] Etat des lieux (section 4) verifie contre le code reel pour eviter de dupliquer `procedures/economic_gate.py`, `procedures/robustness.py`, ou le pont de strategie Nautilus.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | annexe |
| Lifecycle | DONE |
| Scope | Construire une experience a verite connue (un candidat synthetique structurellement gagnant, un candidat synthetique structurellement perdant, memes `entry_criterion`/`exit_criterion`/pont de strategie que la production) executee via le pipeline Nautilus MVP reel deja livre (`WalkForwardSplitter`, `run_multifold_segments`, `risk/robustness.py`, `GenericPayloadStrategy`), avec des seuils de gate economique et de robustesse **reellement calcules** (pas les booleens `True` codes en dur actuels), pour prouver que `procedures/economic_gate.py` et `procedures/robustness.py` rejettent effectivement le candidat perdant et acceptent le candidat gagnant. |
| Non-goals | Ne pas modifier `procedures/`, `validators/`, `governance/`, `manifests/`, `Protocole/` ; ne pas modifier `adapters/nautilus_strategy_bridge.py::GenericPayloadStrategy` (reutiliser tel quel, memes regles de declenchement) ; ne pas modifier le chemin de production `package_builder/nautilus_research_package.py` (l'experience vit dans son propre module) ; ne pas faire des seuils de cette experience une decision de calibration SOP de production (ils sont explicitement locaux et synthetiques) ; ne pas rouvrir ou re-cloturer le chantier Nautilus ; ne pas re-tester WRC/SPA/Romano-Wolf (deja couverts par les tests unitaires existants de `procedures/wrc.py`) — cette experience cible specifiquement la discrimination du gate economique et de la robustesse. |
| Source | Conversation humaine du 2026-07-10, en suite directe de l'audit d'implementation des plans Nautilus (reserve M4 : « le PASS ne prouve que la mecanique, pas la selectivite »). Instruction humaine : « lancer une experience controlee dessus pour voir si ca marche vraiment ». |
| Exit criteria | (1) Un test de regression deterministe (sans dependance `nautilus_trader`, execute par la suite runtime standard) prouve que, sur des `SimulationResult` a verite connue, le candidat gagnant obtient `economic_gate_report()["global_status"] == "PASS"` et le candidat perdant obtient `"REJECTED_ECONOMIC"` (ou un verdict de robustesse bloquant), avec des seuils non triviaux (pas `-1.0`/`True` fixes). (2) Une execution reelle via le venv Nautilus (`adapters/nautilus_env/venv`) confirme, sur des donnees OHLCV synthetiques deterministes, que le candidat gagnant produit un rendement moyen positif et le candidat perdant un rendement moyen negatif, et que les deux verdicts de gate correspondent. (3) Zero modification de `procedures/`, `validators/`, `governance/`, `manifests/`, `Protocole/`, et zero modification du chemin de production `nautilus_research_package.py`. (4) Suite runtime complete reste PASS. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | DONE |
| Date de creation | 2026-07-10 |
| Date d'activation | 2026-07-10 |
| Autorite normative | `Protocole/` (`EBTA-DOC-1.1`), en particulier SOP 05 (robustesse), SOP 08 (gate economique) |
| Autorite executable | `Implementation/ebta_engine/` (traduction executable subordonnee) |
| Changement normatif attendu | Aucun |
| Dependances externes | `nautilus_trader==1.230.0` (deja installe, venv reproductible existant `Implementation/adapters/nautilus_env/venv`), confine a l'usage existant de `adapters/` — aucune nouvelle dependance |

---

## 1. Role de ce document et non-objectifs

| Element | Role |
| --- | --- |
| `Protocole/` | Autorite normative absolue. Inchange. |
| `Implementation/ebta_engine/procedures/economic_gate.py`, `procedures/robustness.py` | Validateurs de verdict deja existants et testes. Inchanges — cette experience les *alimente* avec des preuves reellement calculees, ne les modifie pas. |
| `Implementation/ebta_engine/adapters/nautilus_mapping.py`, `nautilus_strategy_bridge.py` | Frontiere Nautilus existante et deja livree. Reutilisee telle quelle, sans modification. |
| `Implementation/ebta_engine/package_builder/nautilus_research_package.py` | Chemin de production MVP. Non modifie par cette experience — l'ecart identifie (booleens de gate economique code en dur) y reste documente comme limite connue, corrige uniquement dans le module d'experience, pas en production. |
| Ce plan | Carte d'une experience de validation isolee : deux candidats synthetiques a verite connue, executes sur le pipeline reel, pour prouver que les gates discriminent. |

Non-objectifs :

- ne pas reecrire `Protocole/` ni aucune SOP ;
- ne pas introduire de seuil de production (les seuils de cette experience sont explicitement synthetiques et locaux) ;
- ne pas dupliquer `procedures/economic_gate.py::economic_gate_report()` ni `procedures/robustness.py::pre_oos_robustness_verdict()` — seulement leur fournir des preuves reellement calculees en amont ;
- ne pas modifier `GenericPayloadStrategy` pour lui faire interpreter differemment un `entry_criterion` selon son contenu (verifie : elle entre long des que `rule_id` est non vide, peu importe sa valeur — section 4) ;
- ne pas faire de cette experience une preuve de performance commerciale d'une vraie strategie EBTA — c'est un test de plomberie de gate, pas une recherche de strategie.

---

## 2. Contexte obligatoire a lire avant de coder

1. `AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json` — etat machine ; confirmer `active_workstream_id: null` et le chantier Nautilus `DONE` avant de commencer.
2. `.ai/archive/20260710_PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md` et `.ai/backlog/fixes/PLAN_CORRECTION_NAUTILUS_MULTIFOLD_ROBUSTESSE.md` — le pipeline que cette experience exerce, sans le modifier.
3. `Protocole/` SOP 05 (robustesse : classifications CENTRAL/PLAUSIBLE_BASE/EXTREME, jamais de seuil invente), SOP 08 (gate economique : hurdle de rendement, drawdown, capacite, couts, execution).
4. Code existant a reutiliser (verifie 2026-07-10, ne jamais dupliquer) :
   - `Implementation/ebta_engine/data/walk_forward.py::WalkForwardSplitter` — construction des folds.
   - `Implementation/ebta_engine/adapters/nautilus_mapping.py::run_multifold_segments()`, `run_segment()` — execution Nautilus par segment, aucune fuite d'etiquette.
   - `Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py::GenericPayloadStrategy` — **entre long des que `entry_criterion.rule_id` est non vide (peu importe la regle), tient `exit_criterion.parameters.horizon_bars` barres, puis solde** (verifie lignes 45-58 : la logique ne lit jamais le contenu semantique de la regle, seulement sa presence). Consequence directe pour ce plan : la discrimination gagnant/perdant ne peut pas venir d'une regle d'entree "plus intelligente" sans modifier ce fichier (hors perimetre) — elle doit venir des **donnees de prix** (une serie qui monte pendant toute la fenetre de detention pour le gagnant, une serie qui baisse pour le perdant), a `entry_criterion`/`exit_criterion`/cout identiques.
   - `Implementation/ebta_engine/risk/robustness.py::compute_robustness_scenarios()` — discrimine deja reellement selon `minimum_mean_return`/`maximum_total_costs` du `scenario_grid` fourni (verifie : compare `mean_return` reel au seuil, section 4). Aucun changement requis ici, seulement fournir un `scenario_grid` non trivial.
   - `Implementation/ebta_engine/procedures/economic_gate.py::economic_gate_report()` — **n'agrege que des booleens deja fournis par l'appelant** (`return_hurdle_pass`, `drawdown_pass`, `capacity_pass`, `costs_pass`, `execution_pass`) ; il ne les calcule jamais lui-meme depuis `thresholds`/`observed_values` (verifie lignes 13-27 : boucle sur les cles booleennes deja presentes dans `evidence`, ne compare jamais `observed_values` a `thresholds`). Consequence : `nautilus_research_package.py` (production) code ces cinq booleens en dur a `True`, quel que soit le resultat reel (voir `nautilus_research_package.py:243-247`) — c'est la cause directe de la reserve M4 de l'audit. Cette experience doit calculer ces booleens honnetement dans son propre module, sans toucher au fichier de production.
   - `Implementation/ebta_engine/tests/test_nautilus_research_package.py::_write_fixture_data()` — patron existant pour generer un CSV OHLCV synthetique deterministe dans un dossier `NASDAQ 1m`/`XAUUSD 1m` (a reutiliser pour construire une serie montante et une serie descendante, pas a reecrire depuis zero).
5. Skill `nautilus-docs-research` — non requis a priori : aucune nouvelle API Nautilus n'est invoquee, `GenericPayloadStrategy` et `run_segment()` sont deja verifies et reutilises tels quels.

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

## 3. Table des gates concernees

Ce plan n'ajoute, ne retire et ne reordonne aucune gate. Il exerce reellement
deux gates deja existantes de la table de reference (voir plan Nautilus
archive, section 3) avec des preuves calculees plutot que codees en dur :

| Ordre | Gate | Ce que cette experience verifie |
| --- | --- | --- |
| G5 | Robustesse pre-OOS | `risk/robustness.py` classe et rejette (`REJECTED_ECONOMIC`/`blocking`) le scenario perdant avec un seuil non trivial |
| G6 / G10 | Execution/capacite et gate economique | `economic_gate.py::economic_gate_report()` retourne `PASS` pour le gagnant et `REJECTED_ECONOMIC` pour le perdant, une fois les booleens calcules honnetement |

---

## 4. Etat des lieux (avant/apres) — reutiliser avant de recreer

### Ce qui existe deja et fonctionne (verifie 2026-07-10)

| Module | Chemin | Role reel (verifie) | Suffisant ? |
| --- | --- | --- | --- |
| Contrats | `strategies/contracts.py` | `SimulationResult`, `CostModel`, `InstrumentConfig`, `Candidate`, `SimulationResult.economic_gate_evidence()` | ✅ Reutiliser tel quel |
| Construction des folds | `data/walk_forward.py::WalkForwardSplitter` | Decoupe Train/Test/OOS avec purge/embargo/warmup, K>=2 impose | ✅ Reutiliser tel quel |
| Boucle d'execution | `adapters/nautilus_mapping.py::run_multifold_segments()` / `run_segment()` | Boucle sur folds/candidates, aucune fuite de segment | ✅ Reutiliser tel quel |
| Pont de strategie | `adapters/nautilus_strategy_bridge.py::GenericPayloadStrategy` | Entre long des que `rule_id` non vide, tient `horizon_bars` barres, solde. Ne discrimine jamais par le contenu de la regle (verifie section 2). | ✅ Reutiliser tel quel — implique que la discrimination vient des donnees de prix, pas de la regle |
| Robustesse | `risk/robustness.py::compute_robustness_scenarios()` | Compare reellement `mean_return`/`total_costs` a `minimum_mean_return`/`maximum_total_costs` du `scenario_grid` fourni | ✅ Reutiliser tel quel — deja discriminant si le seuil est reel |
| Validateur de robustesse | `procedures/robustness.py::pre_oos_robustness_verdict()` | Valide un verdict deja classifie | ✅ Inchange |
| Validateur economique | `procedures/economic_gate.py::economic_gate_report()` | **N'agrege que des booleens deja fournis**, ne les calcule jamais depuis `thresholds`/`observed_values` (verifie lignes 13-27) | ✅ Inchange — mais le calcul des booleens doit exister quelque part |

### Ce qui manque reellement (l'ecart identifie par l'audit, reserve M4)

| Manque | Ou il se voit aujourd'hui | Ce que cette experience ajoute (sans toucher la production) |
| --- | --- | --- |
| Calcul honnete des cinq booleens du gate economique (`return_hurdle_pass`, `drawdown_pass`, `capacity_pass`, `costs_pass`, `execution_pass`) depuis `observed_values` vs `thresholds` | `package_builder/nautilus_research_package.py:243-247` — code en dur `True` pour les cinq | Nouvelle fonction locale a l'experience (ex. `compute_economic_pass_flags()`), qui compare reellement rendement/couts/drawdown observes aux seuils synthetiques declares, sans modifier `nautilus_research_package.py` ni `procedures/economic_gate.py` |
| Donnees OHLCV synthetiques a tendance opposee garantie sur toute la fenetre de detention | Absent — les fixtures existantes (`test_nautilus_research_package.py`) sont plates ou quasi plates | Deux series CSV deterministes : une strictement montante, une strictement descendante, memes horaires, meme volume |
| Seuils de gate non triviaux dans un `scenario_grid`/`thresholds` | `_nautilus_robustness_grid()` de production utilise `minimum_mean_return: -1.0` (tout passe) | `scenario_grid`/`thresholds` locaux a l'experience avec un seuil strictement positif, documente comme synthetique |

---

## 5. Decision d'architecture

Principe directeur : l'experience est un **harnais de test isole**, jamais un
chemin de production alternatif. Elle appelle exactement les memes fonctions
que `nautilus_research_package.py` (WalkForwardSplitter, run_multifold_segments,
GenericPayloadStrategy, compute_robustness_scenarios, economic_gate_evidence,
economic_gate_report, pre_oos_robustness_verdict), mais avec (a) des donnees
synthetiques a verite connue au lieu des CSV reels, et (b) un calcul honnete
des booleens de gate economique au lieu du `True` code en dur de production.

- Raison 1 — reproduire l'ecart de production tel quel serait circulaire : si l'experience copiait le `True` code en dur de `nautilus_research_package.py`, elle "prouverait" un PASS peu importe les donnees, ce qui est precisement le defaut a demontrer.
- Raison 2 — ne pas toucher `nautilus_research_package.py` : corriger le calcul des booleens en production est un changement distinct (hors perimetre de ce plan, a proposer separement si l'experience confirme le besoin), pas une consequence automatique de ce test.
- Raison 3 — la discrimination doit venir des donnees, pas d'une regle de strategie sur mesure : `GenericPayloadStrategy` reste inchangee (section 2), donc le seul levier disponible et honnete est le prix lui-meme.

### Frontieres explicites

| Couche | Elle fait | Elle NE fait PAS |
| --- | --- | --- |
| Module d'experience (nouveau) | Construit 2 series OHLCV synthetiques opposees, definit seuils non triviaux, calcule les 5 booleens du gate economique depuis les resultats reels, appelle le pipeline existant tel quel | Modifier `procedures/`, `adapters/`, `package_builder/nautilus_research_package.py` ; interpreter differemment `entry_criterion` |
| Pipeline Nautilus MVP (existant, reutilise) | Fold, execution, extraction, robustesse, agregation economique — exactement comme en production | Savoir qu'il est appele depuis une experience plutot que la production |

### Contrat d'interface

Aucun nouveau contrat de donnees. Seule addition : une fonction pure locale a
l'experience (pas dans `procedures/`), qui prend le `SimulationResult` complet
en entree plutot que des scalaires deja agreges par un appelant non
specifie — evite toute duplication de derivation entre la Phase 2 et la
Phase 3 :

```python
def compute_economic_pass_flags(
    result: SimulationResult,
    *,
    thresholds: dict[str, float],
) -> dict[str, bool]:
    """Calcule honnetement les 5 booleens attendus par economic_gate_report().

    Derivation explicite depuis SimulationResult (aucun champ drawdown
    n'existe sur ce contrat - verifie strategies/contracts.py:114-126) :
      - mean_return   = mean(result.daily_returns)
      - total_costs   = result.total_costs
      - max_drawdown  = plus grande baisse pic-a-creux observee sur
                        result.nav, calculee comme
                        max((peak - value) / peak) pour peak = max
                        cumulatif de result.nav jusqu'a l'indice courant.

    thresholds attendus (tous obligatoires, aucune valeur par defaut -
    seuil absent = leve ValueError plutot que deviner, coherent avec
    l'invariant "bloquer plutot que deviner") :
      - minimum_mean_return (float)
      - maximum_total_costs (float)
      - maximum_drawdown (float, fraction positive, ex. 0.20 pour 20%)

    Seuils fournis explicitement par l'appelant (synthetiques ici) ;
    ne decide jamais du gate lui-meme (role de procedures/economic_gate.py).
    capacity_pass et execution_pass restent True dans le perimetre MVP de
    cette experience (pas de contrainte de capacite ni d'echec d'execution
    a modeliser ici) - documente comme limite explicite, pas un oubli."""
```

### Structure cible

```text
Implementation/
  examples/
    controlled_experiments/
      gate_discrimination_experiment.py   # NOUVEAU -- orchestre l'experience reelle (venv Nautilus)
  ebta_engine/
    tests/
      fixtures/
        gate_discrimination/               # NOUVEAU -- CSV synthetiques montant/descendant
      test_gate_discrimination_experiment.py  # NOUVEAU -- regression deterministe (fake runner, suite standard)
    procedures/, validators/, governance/, manifests/, adapters/, package_builder/  # INCHANGES
```

---

## 6. Decoupage en phases

### Phase 1 - Donnees synthetiques et calcul honnete des booleens economiques

Objectif : construire les deux series de prix a verite connue et la fonction de calcul des booleens, sans toucher au pipeline existant.

Classification : TEST_FIXTURE

Actions :

- Construire deux series CSV synthetiques (patron `_write_fixture_data()` existant, `tests/test_nautilus_research_package.py`) : une serie NASDAQ strictement montante sur toute la fenetre de detention prevue, une serie XAUUSD strictement descendante sur la meme fenetre — memes horodatages, meme volume, memes `CostModel`/`InstrumentConfig` que la production (`_nautilus_cost_model()`, `_instrument_config()`).
- **Fixer des valeurs concretes des maintenant (ne pas les laisser a l'appreciation de l'implementeur)** : `test_size=5`, `oos_size=5`, `train_size=5`, `purge_days=0`, `embargo_days=0`, `warmup_days=0`, `exit_criterion.parameters.horizon_bars=3` (strictement inferieur a `test_size`/`oos_size` pour garantir que `GenericPayloadStrategy` ferme sa position dans le segment, cf. `nautilus_strategy_bridge.py:57-58` — un `horizon_bars >= test_size` laisserait la position ouverte a la fin du segment, faussant silencieusement `daily_returns`). Pente de prix synthetique : `+0.5%`/barre pour la serie montante, `-0.5%`/barre pour la serie descendante, sur au moins `train_size + test_size + oos_size + purge_days + embargo_days` barres par fold.
- Ecrire `compute_economic_pass_flags()` (fonction pure, locale a l'experience, signature section 5) : derive rendement moyen / couts totaux / drawdown directement depuis un `SimulationResult`, puis compare aux seuils explicites non triviaux.
- Definir un `scenario_grid` de robustesse local avec un `minimum_mean_return` strictement positif (pas `-1.0`).

Livrables :

- `tests/fixtures/gate_discrimination/` (2 CSV).
- `compute_economic_pass_flags()` testee unitairement (cas gagnant, cas perdant, cas limite).

Critere de sortie :

- Test unitaire : `compute_economic_pass_flags()` retourne tous les booleens `True` pour des valeurs conformes au seuil, au moins un `False` pour des valeurs non conformes — PASS.
- Suite runtime complete reste PASS.

### Phase 2 - Regression deterministe de discrimination (suite standard, sans venv)

Objectif : prouver mecaniquement, avec un runner de segment factice mais des `SimulationResult` a verite connue (rendements positifs/negatifs deterministes), que le pipeline complet (folds -> robustesse -> gate economique) discrimine.

Classification : IMPLEMENTATION_DETAIL

Actions :

- Ecrire `tests/test_gate_discrimination_experiment.py` : construit 2 folds via `WalkForwardSplitter`, execute le candidat gagnant et le candidat perdant via `run_multifold_segments()` avec un runner factice retournant des `SimulationResult` a rendements deterministes (positifs pour le gagnant, negatifs et couteux pour le perdant).
- Appliquer `compute_robustness_scenarios()` (Phase 1) avec le `scenario_grid` non trivial, puis `pre_oos_robustness_verdict()`.
- Appliquer `compute_economic_pass_flags()` (Phase 1) sur l'OOS de chaque candidat, puis `SimulationResult.economic_gate_evidence()` et `procedures/economic_gate.py::economic_gate_report()`.
- Asserter : candidat gagnant -> `economic_gate_report()["global_status"] == "PASS"` et robustesse `PASS` ; candidat perdant -> `"REJECTED_ECONOMIC"` et/ou robustesse `FAIL`/scenario bloquant.
- **Ajouter un test de contraste permanent dans le meme fichier** (pas une verification manuelle jetable) : rejoue exactement le meme `SimulationResult` perdant, mais avec les 5 booleens codes en dur a `True` (reproduisant tel quel le comportement actuel de production, `nautilus_research_package.py:243-247`) au lieu de `compute_economic_pass_flags()`, et asserte que `economic_gate_report()["global_status"] == "PASS"` dans ce cas — ce test de contraste prouve mecaniquement, et de maniere rejouable indefiniment, que le calcul honnete (et lui seul) est ce qui permet la detection : sans lui, le meme candidat perdant passerait silencieusement.

Livrables :

- `tests/test_gate_discrimination_experiment.py`, integre a `python -m unittest discover`, incluant le test de contraste ci-dessus.

Critere de sortie :

- Le test de discrimination PASSE (gagnant `PASS`, perdant `REJECTED_ECONOMIC`/robustesse bloquante).
- Le test de contraste PASSE et demontre que le meme candidat perdant, avec les booleens de production codes en dur, obtient `PASS` — preuve mecanique et permanente que la detection vient du calcul honnete, pas d'un artefact du seuil choisi.
- Suite runtime complete reste PASS.

### Phase 3 - Execution reelle via le venv Nautilus

Objectif : confirmer sur le moteur Nautilus reel (pas un fake) que les donnees de prix synthetiques produisent bien un rendement moyen positif pour le gagnant et negatif pour le perdant, et que les gates reagissent en consequence.

Classification : ADAPTER_MAPPING

Actions :

- Ecrire `examples/controlled_experiments/gate_discrimination_experiment.py` : assemble les deux candidats (memes `entry_criterion`/`exit_criterion`, memes cout/instrument que la production), les deux series de prix (Phase 1), execute chacun via `run_segment()` reel (pas de runner factice) sur Test puis OOS, calcule les booleens (Phase 1), produit un rapport JSON (`status`, `mean_return` par candidat, `economic_status`, `robustness_status`).
- **Invocation** : ce script vit sous `examples/`, qui n'a aucun `__init__.py` dans tout le depot (verifie) et n'est donc pas un package important par `-m` — a l'inverse de `ebta_engine/package_builder/nautilus_research_package.py` qui, lui, est invoque via `-m ebta_engine.package_builder.nautilus_research_package` parce qu'il est dans le package `ebta_engine`. Suivre exactement le meme precedent que `examples/minimal_pilot_pipeline/build_research_package.py` ([CLAUDE.md:82](../../../CLAUDE.md)) : executer comme script direct, jamais via `-m`.

Livrables :

- `examples/controlled_experiments/gate_discrimination_experiment.py`.
- Rapport d'execution reel (sortie console + fichier JSON), archive comme preuve dans ce plan (section 13).

Critere de sortie :

- Rendement moyen OOS reel : positif pour le gagnant, negatif pour le perdant (valeurs exactes consignees en section 13).
- `economic_status`/`robustness_status` : `PASS` pour le gagnant, `REJECTED_ECONOMIC` ou verdict bloquant pour le perdant.
- Aucune modification de `nautilus_research_package.py` ni des dossiers proteges.

---

## 7. Artefacts produits

| Etape | Fichier/sortie | Format | Regle source |
| --- | --- | --- | --- |
| Fixtures | `tests/fixtures/gate_discrimination/*.csv` | CSV | Patron existant `_write_fixture_data()` |
| Rapport d'experience reelle | Sortie de `gate_discrimination_experiment.py` (console + JSON) | JSON | SOP 05, SOP 08 |

---

## 8. Invariants absolus et NO GO

### Invariants

1. `GenericPayloadStrategy` reste inchangee — la discrimination vient uniquement des donnees de prix.
2. `procedures/economic_gate.py` et `procedures/robustness.py` restent les seules autorites de verdict — l'experience ne decide jamais elle-meme du PASS/FAIL, elle ne fait que fournir des preuves honnetes.
3. Aucune fuite d'etiquette de segment vers Nautilus (invariant deja garanti par `run_segment()`/`run_multifold_segments()`, reutilises tels quels).
4. Les seuils synthetiques de cette experience ne sont jamais presentes comme une decision de calibration de production.

### NO GO

- Modifier `procedures/`, `validators/`, `governance/`, `manifests/`, `Protocole/`.
- Modifier `adapters/nautilus_strategy_bridge.py`, `adapters/nautilus_mapping.py`, ou `package_builder/nautilus_research_package.py`.
- Coder en dur un verdict de gate au lieu de le laisser calculer par `procedures/`.
- Presenter un resultat de plomberie (donnees synthetiques) comme une preuve de performance d'une strategie EBTA reelle.
- Declarer l'exit criterion atteint sans les deux preuves (Phase 2 deterministe ET Phase 3 reelle via venv).

---

## 9. Verification a chaque etape

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
git diff --stat -- Implementation\ebta_engine\procedures Implementation\ebta_engine\validators Implementation\ebta_engine\governance Implementation\ebta_engine\manifests Implementation\ebta_engine\package_builder Protocole
```

Execution reelle (Phase 3, depuis `Implementation/`, script direct — jamais `-m`, voir section 6 Phase 3) :

```powershell
.\adapters\nautilus_env\venv\Scripts\python.exe .\examples\controlled_experiments\gate_discrimination_experiment.py
```

**Regle transversale bloquante** : la suite runtime doit rester PASS avant de
demarrer chaque phase suivante.

**Premier lot executable propose** :

```text
Phase 1 - Donnees synthetiques et calcul honnete des booleens economiques
```

---

## 10. Journal des decisions humaines (autorisations)

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-10 | Demande d'une experience controlee pour verifier que les gates Nautilus discriminent reellement un candidat gagnant d'un candidat perdant | Autorise la redaction de ce plan `annexe` ; n'autorise pas encore l'execution des phases de code (attend confirmation humaine, puis eventuellement `/evaluate`) |
| 2026-07-10 | Directive `/goal` avec fichier colle demandant l'execution de bout en bout sans intervention humaine | Autorise l'execution des Phases 1 a 3, la production du rapport reel et la cloture factuelle du plan, sans modifier les dossiers proteges ni le chemin de production Nautilus. |

---

## 11. Risques et blocages connus

| Risque | Impact | Mitigation |
| --- | --- | --- |
| Le calcul honnete des booleens economiques revele que la production (`nautilus_research_package.py`) devrait aussi etre corrigee | Decision hors perimetre de ce plan | Documenter la constatation en section 13 comme suite a prevoir, ne pas corriger la production dans ce plan sans nouvelle decision humaine |
| Rendement OOS synthetique proche de zero malgre la tendance | Discrimination faible ou ambigue | Choisir une pente de prix suffisamment marquee (ex. +0.5%/jour vs -0.5%/jour) pour garantir un ecart net des couts |
| Le fake runner (Phase 2) masque un comportement reel different de Nautilus (Phase 3) | Faux sentiment de securite si seule la Phase 2 est executee | Exit criteria exige explicitement les deux preuves (section Triage) |

---

## 12. Definition of Done

- [x] Phases 1 a 3 validees individuellement (section 9).
- [x] Exit criteria de la section Triage atteint (test deterministe PASS + execution reelle venv confirmee).
- [x] Aucune modification de `procedures/`, `validators/`, `governance/`, `manifests/`, `Protocole/`, `package_builder/nautilus_research_package.py`, `adapters/`.
- [x] Aucune regression sur la suite runtime.
- [x] Checklist `.ai/governance/AI_MODIFICATION_CHECKLIST.md` executee.

---

## 13. Cloture

A remplir au moment de `/close` :

| Champ | Valeur |
| --- | --- |
| Resultat final | DONE - L'experience controlee discrimine reellement un candidat gagnant NASDAQ d'un candidat perdant XAUUSD. Le gagnant obtient `economic_status: PASS` et `robustness_status: PASS`; le perdant obtient `economic_status: REJECTED_ECONOMIC` et `robustness_status: FAIL`. |
| Ecarts par rapport au plan initial | Deux ajustements factuels seulement : (1) le script direct a du ajouter `Implementation/` a `sys.path` pour importer `ebta_engine`; (2) l'execution reelle utilise le runner subprocess Nautilus deja existant pour eviter l'erreur de logger Rust observee lors de plusieurs `BacktestEngine` dans un meme processus. Le seuil synthetique local a ete fixe a `minimum_mean_return: 0.0001`, strictement positif, car le rendement reel du gagnant est positif mais inferieur a `0.0005`. |
| Suites a prevoir | Ouvrir un chantier separe si l'on veut corriger le chemin de production `package_builder/nautilus_research_package.py`, qui code encore les cinq flags economiques a `True`. Ce plan a prouve le trou via un test de contraste permanent, sans modifier la production. |

### Resultat d'execution (a dupliquer a chaque session d'execution significative)

| Champ | Valeur |
| --- | --- |
| Date | 2026-07-10 |
| Phases executees | Phases 1, 2 et 3 executees dans l'ordre. |
| Artefact produit | `Implementation/ebta_engine/tests/fixtures/gate_discrimination/` ; `Implementation/ebta_engine/tests/test_gate_discrimination_experiment.py` ; `Implementation/examples/controlled_experiments/gate_discrimination_experiment.py` ; `Implementation/examples/controlled_experiments/gate_discrimination_report.json`. |
| Validation | Phase 1 : `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` PASS, 114 tests. Phase 2 : meme commande PASS, 116 tests. Phase 3 : meme commande PASS, 116 tests, puis `.\adapters\nautilus_env\venv\Scripts\python.exe .\examples\controlled_experiments\gate_discrimination_experiment.py` depuis `Implementation/` PASS. Resultats reels : gagnant NASDAQ `test_mean_return=0.0004180022504795657`, `oos_mean_return=0.00042886485315944483`, `economic_status=PASS`, `robustness_status=PASS`; perdant XAUUSD `test_mean_return=-0.00038207337444350737`, `oos_mean_return=-0.0003734014743262745`, `economic_status=REJECTED_ECONOMIC`, `robustness_status=FAIL`. |
| Ecart par rapport au plan | Aucun ecart de perimetre. Les dossiers interdits et le chemin de production Nautilus sont restes inchanges ; `git diff --stat -- Implementation\ebta_engine\procedures Implementation\ebta_engine\validators Implementation\ebta_engine\governance Implementation\ebta_engine\manifests Implementation\ebta_engine\package_builder Protocole` ne retourne aucun fichier. |

---

## 14. Journal d'audits post-hoc

| Date de l'audit | Ce qui a ete corrige | Pourquoi |
| --- | --- | --- |
| 2026-07-10 | Creation de ce plan a la suite de l'audit d'implementation Nautilus (reserve M4 : gates permissifs, jamais testes en rejet) | L'audit a confirme la plomberie multi-fold mais pas la capacite reelle des gates a rejeter un mauvais candidat |
| 2026-07-10 (`/evaluate`, `code-architecture-evaluator`) | R1 : invocation Phase 3 corrigee de `-m examples.controlled_experiments...` (package inexistant) en script direct | `examples/` n'a aucun `__init__.py` dans tout le depot ; seul precedent existant (`minimal_pilot_pipeline`) s'invoque comme script direct, jamais via `-m` |
| 2026-07-10 (`/evaluate`) | R2 : signature de `compute_economic_pass_flags()` corrigee pour prendre un `SimulationResult` complet et deriver explicitement le drawdown depuis `nav` (formule precisee) | `SimulationResult` n'a aucun champ `drawdown` (verifie `strategies/contracts.py:114-126`) ; aucun code existant ne le derive ; laisser cette derivation implicite aurait recree l'ambiguite de contrat que le plan Nautilus original s'interdisait |
| 2026-07-10 (`/evaluate`) | R3 : Phase 1 fixe des valeurs concretes (tailles de fenetre, `horizon_bars=3` < `test_size`/`oos_size`, pente de prix) au lieu de les laisser a l'appreciation de l'implementeur | Un `horizon_bars >= test_size` laisserait `GenericPayloadStrategy` avec une position ouverte en fin de segment, faussant silencieusement le resultat sans qu'aucune erreur ne soit levee |
| 2026-07-10 (`/evaluate`) | R4 : Phase 2 remplace la verification manuelle jetable par un test de contraste permanent (memes donnees perdantes, booleens de production codes en dur, assertion que `PASS` sortirait quand meme) | Une verification "ponctuelle pendant l'ecriture, non conservee" n'est pas rejouable et ne prouve rien apres coup — c'est le meme defaut methodologique qui a produit la fausse cloture `DONE` du plan Nautilus original |
