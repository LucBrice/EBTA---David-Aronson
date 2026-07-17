# Brouillon intake — Lot B : G6 execution/NAV reconstructible

## Demande

Executer le Lot B de l'EPIC `EPIC_CLOTURE_ATTESTATIONS_RESIDUELLES_GATES`
apres GO humain du 2026-07-17.

Decision humaine actee : appliquer l'Option 3 stricte.

- `PASS` seulement si la preuve execution/NAV est reconstructible avec
  `total_orders > 0`, `oos_total_orders > 0`, NAV presente, positive et non
  plate.
- `INCONCLUSIVE` si la preuve est insuffisante ou non reconstructible.
- `FAIL` si une contradiction ou une violation explicite est observee.

NotebookLM/livre a ete utilise comme appui de lecture, pas comme source
normative du repo. L'autorite normative reste `Protocole/` ; la decision
humaine ci-dessus leve le verrou identifie dans l'EPIC.

## Constat verifie dans le code

- `Implementation/ebta_engine/package_builder/nautilus_research_package.py`
  ecrit encore `inputs["execution_report"]["status"] = "PASS"` et
  `nav_reconciliation = "PASS"` alors que `_total_orders(...)` existe deja au
  meme endroit.
- `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
  ecrit encore les quatre champs G6 de `gates.json` (`execution_report`,
  `cost_model`, `capacity_grid`, `nav_reconciliation`) a `True`.
- `Implementation/ebta_engine/tests/test_nautilus_research_package.py` prouve
  seulement le cas nominal `total_orders > 0` et `oos_total_orders > 0` ; il
  manque une non-regression qui empeche un zero-trade ou une NAV non prouvee
  de passer.
- `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py` ne verifie
  pas encore que les champs G6 derivent des rapports `execution`/`economic`.

## Source protocolaire

- `Protocole/PAQUET D'EXECUTION EBTA.md` : G6 exige une execution,
  couts/capacite/sizing, NAV reconciliee et une chaine
  `signal -> ordre -> fill -> position -> P&L` reconstructible.
- `Protocole/SOP 08 - Mesures de performance et serie de rendement de
  reference.md` : une NAV non reconstructible ou non reconciliable ne doit pas
  etre acceptee silencieusement.
- `Protocole/SOP 09B - Modele d'execution frictions capacite et sizing.md` :
  les ordres, fills, positions, couts et NAV doivent rester auditables.

## Perimetre propose

Autorises :

- `Implementation/ebta_engine/package_builder/nautilus_research_package.py`
- `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
- `Implementation/examples/minimal_pilot_pipeline/inputs/pilot_inputs.json`
  seulement si le pilote a besoin d'une preuve NAV minimale explicite.
- `Implementation/ebta_engine/tests/test_nautilus_research_package.py`
- `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py`
- ce brouillon et son plan restructure dans `.ai/backlog/fixes/`
- `.ai/checkpoint.json` uniquement via `.ai/tools/plan.ps1`

Interdits :

- `Protocole/`
- `Implementation/ebta_engine/validators/gate_validator.py`
- `Implementation/ebta_engine/manifests/`
- `Implementation/ebta_engine/governance/`
- les plans deja clos Lot C et Lot A2
- BACKTRADER

## Architecture visee

1. Ajouter dans `nautilus_research_package.py` une evaluation locale du statut
   execution/NAV a partir des resultats `SimulationResult` deja produits.
2. Construire `inputs["execution_report"]` avec ce statut calcule, sans
   introduire de nouveau verdict ni de dependance externe.
3. Propager dans le pilote les champs G6 de `gates.json` depuis les rapports
   reels :
   - `execution_report` depuis `procedure_reports["execution"]["status"]`.
   - `nav_reconciliation` depuis
     `procedure_reports["execution"]["nav_reconciliation"]`.
   - `cost_model` via une conversion explicite en verdict gate :
     `PASS` si le modele de cout scelle existe et si le rapport d'execution ne
     contredit pas le modele declare ; `INCONCLUSIVE` si la preuve manque ;
     `FAIL` si le modele declare et le rapport d'execution se contredisent.
   - `capacity_grid` via une conversion explicite en verdict gate :
     `PASS` si la grille existe et que le rapport economique ne signale pas
     `capacity_pass`/`capacity_grid` dans ses echecs ; `INCONCLUSIVE` si la
     grille ou la preuve manque ; `FAIL` si une violation explicite de
     capacite est encodee. Ne jamais injecter directement `economic_status`
     dans `gates.json`, car `REJECTED_ECONOMIC` est une chaine non vide que
     `gate_validator.py` considererait presente par erreur.
4. Ajouter des tests de non-regression pour le cas nominal et les cas
   insuffisants/contradictoires.

## Non-objectifs

- Ne pas changer la doctrine EBTA ni les SOP.
- Ne pas inventer un nouveau statut de gate.
- Ne pas rendre G6 `PASS` seulement parce qu'un champ est present.
- Ne pas masquer un package sans trade ou sans NAV derriere `PASS`.
- Ne pas ouvrir de chantier Nautilus API ; aucun nouvel appel
  `nautilus_trader` n'est attendu dans ce lot.

## Exit criteria

- Le Lot B est route comme workstream `fix`, audite deux fois avant et deux
  fois apres promotion.
- `execution_report.status` et `nav_reconciliation` ne sont plus codes en dur
  a `PASS` dans le package Nautilus.
- Les quatre champs G6 de `gates.json` ne sont plus des litteraux `True`.
- Un cas zero-trade/OOS sans ordre ou NAV non prouvee ne peut pas produire un
  G6 `PASS`.
- Les tests cibles, la suite runtime, le build pilote, pyrefly, bug-hunter et
  plan-conformance-audit passent avant cloture.

## Journal d'audit d'architecture

| Date | Passe | Resultat | Correction appliquee |
| --- | --- | --- | --- |
| 2026-07-17 | Intake pass 1 | Angle mort detecte : `economic_status = REJECTED_ECONOMIC` ne peut pas etre injecte brut dans G6, car `gate_validator.py` ne connait que `PASS`/`FAIL`/`INCONCLUSIVE` et traite les autres chaines non vides comme presentes. | Section Architecture durcie : `cost_model` et `capacity_grid` doivent passer par une conversion explicite en verdict gate, sans reutiliser `economic_status` brut. |
| 2026-07-17 | Intake pass 2 | Convergence : le brouillon cite le verrou leve, le code fautif, le validateur cible et les conversions necessaires ; aucun nouveau module, statut, schema ou appel Nautilus n'est propose. | Aucune correction supplementaire requise avant reecriture selon le gabarit backlog. |
