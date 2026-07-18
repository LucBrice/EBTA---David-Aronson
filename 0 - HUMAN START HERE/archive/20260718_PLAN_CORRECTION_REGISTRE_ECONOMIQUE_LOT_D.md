# Note d'intake - Lot D : G2/G3/G4/G5/G7-residuel/G10 derives de preuves reelles

> Statut : `INTAKE`, non executable directement. Sous-chantier 1/4 de
> `EPIC_ATTESTATIONS_RESIDUELLES_R3`. Ce lot doit etre route comme
> `PLAN_CORRECTION_REGISTRE_ECONOMIQUE_LOT_D` avec un `routing_reason`
> commencant par `Sous-chantier 1/4 de EPIC_ATTESTATIONS_RESIDUELLES_R3`.

## 1. Objectif

Corriger le chemin d'assemblage du package EBTA pour que les champs residuels
des gates G2/G3/G4/G5/G7/G10 derives par
`Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
ne soient plus des litteraux `True` non prouves.

Le lot doit aussi corriger le bug de calcul G2 identifie dans le chantier
mere : `review_registry_lineage(candidate_ids, candidate_ids)` est
structurellement tautologique. La correction retenue pour ce lot est un
controle de presence et coherence : lire les candidates reellement
enregistrees depuis `registry.jsonl` deja ecrit sur disque, puis comparer ces
candidates aux candidates influentes de `reports/candidate_matrix.json`.

Ce choix ne transforme pas `independent_registry_review` en preuve humaine
independante : ce champ reste hors perimetre par decision humaine du
2026-07-16 reconduite le 2026-07-17. Le rapport `registry_review.json`
devient seulement non tautologique pour les champs G2 mecaniques
`registry_initialized`, `candidate_catalog` et `local_matrix`.

## 2. Revalidation dans le code reel

Verifications faites avant redaction :

- `build_package()` ecrit `registry.jsonl` avec `_write_registry()` avant
  `_write_reports()`, donc `_write_reports()` peut reutiliser le registre
  ecrit sans reorganiser tout le pipeline.
- `_write_reports()` met encore `registry_initialized`, `candidate_catalog`,
  `local_matrix`, `selection_rule`, `train_only_calibration_log`,
  `wrc_report`, `wrc_family_matrix`, `robustness_report`,
  `robustness_matrix`, `test_reports`, `economic_report`,
  `statistical_gate_report` et `economic_gate_report` a `True` en litteral.
- `_procedure_reports()` calcule deja `search_space`, `optimization_log`,
  `complexity_selection`, `candidate_matrix`, `wrc`, `robustness`,
  `economic` et `registry_review`.
- `registry_lineage.py::review_registry_lineage()` detecte correctement une
  candidate influente manquante si les deux listes donnees sont distinctes.
  Le bug est dans l'appelant actuel, pas dans la logique de comparaison de
  base.
- `gate_validator.py::_requirement_satisfied()` n'accepte `PASS` que pour
  les valeurs de verdict `PASS/FAIL/INCONCLUSIVE`. Il n'a pas besoin d'etre
  modifie pour ce lot.
- `Implementation/ebta_engine/package_builder/nautilus_research_package.py`
  charge le builder pilote et appelle `pilot.build_package()`. La correction
  du builder pilote impacte donc aussi la construction Nautilus, mais la
  regeneration persistante de `Implementation/research_packages/nautilus_mvp`
  reste reservee a la phase finale du chantier mere.
- La chaine `test_reports` n'a pas de producteur explicite trouve dans
  `Implementation/` ou `Protocole/PAQUET D'EXECUTION EBTA.md`. Pour ce lot,
  elle doit devenir un verdict technique minimal (`PASS` ou `INCONCLUSIVE`)
  derive de la presence/coherence des rapports Test deja produits en memoire
  (`candidate_matrix`, `wrc`, `robustness`, `economic`), pas rester un
  litteral `True`. Cette derivation ne doit pas etre presentee comme une
  nouvelle procedure normative appelee `test_reports`.

## 3. Perimetre propose

Fichiers autorises :

- `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
  pour ajouter des helpers de derivation de gate et brancher les champs D.
- `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py` pour
  verifier les champs D contre les rapports reels et contraster un registre
  incomplet.
- `Implementation/TRACEABILITY_MATRIX.md` si une ligne de tracabilite doit
  etre precisee pour le mapping gates/residual attestations.
- `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` pour journaliser
  le changement runtime significatif.

Fichiers interdits :

- `Protocole/` et SOP : aucune modification normative.
- `Implementation/ebta_engine/validators/gate_validator.py` :
  `GATE_REQUIREMENTS` et `VERDICT_VALUES` restent inchanges.
- `Implementation/ebta_engine/validators/package_validator.py` : pas de
  deplacement du verdict vers le validateur.
- `Implementation/research_packages/nautilus_mvp/` : regeneration reservee
  a la phase finale du chantier mere.
- Lots C/A2/B archives : ne pas rouvrir.

## 4. Strategie d'implementation

1. Ajouter un lecteur local de `registry.jsonl` dans
   `build_research_package.py`, limite aux evenements
   `REGISTER_CANDIDATE`, avec extraction stable des `candidate_id` reels.
2. Modifier `_procedure_reports()` pour recevoir le `package_dir` ou les
   candidates enregistrees et appeler `review_registry_lineage()` avec :
   - `registered_candidates` = candidates lues depuis `registry.jsonl`;
   - `influential_candidates` = `candidate_matrix["candidate_ids"]`;
   - `lineage_events` = evenements de lineage si presents, sinon liste vide.
3. Ajouter de petits helpers `_g2_*`, `_g3_*`, `_g4_*`, `_g5_*`, `_g10_*`
   qui retournent `PASS`, `FAIL` ou `INCONCLUSIVE` selon les rapports reels.
4. Brancher les champs dans `gates.json` :
   - G2 : `registry_initialized`, `candidate_catalog`, `local_matrix`;
   - G3 : `selection_rule`, `train_only_calibration_log`;
   - G4 : `wrc_report`, `wrc_family_matrix`;
   - G5 : `robustness_report`, `robustness_matrix`;
   - G10 : `economic_report`, `statistical_gate_report`,
     `economic_gate_report`.
5. Remplacer `test_reports: True` par un helper de presence/coherence des
   rapports Test. Le helper retourne `PASS` seulement si les rapports Test
   attendus sont presents et portent les champs minimaux requis ; sinon
   `INCONCLUSIVE`.

## 5. Tests requis

- Ajouter un test ciblant le cas de registre incomplet via le nouveau helper
  de lecture/derivation : un `registry.jsonl` valide mais sans une candidate
  presente dans `candidate_matrix["candidate_ids"]` doit produire
  `registry_review.status == "FAIL"` et un champ G2 derive non `PASS`.
- Ajouter un test de mapping gates Lot D dans
  `test_minimal_pilot_pipeline.py` : les champs G3/G4/G5/G10 doivent egales
  les statuts ou presences des rapports reels, pas `True`.
- Lancer :

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_minimal_pilot_pipeline.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_research_package.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
python Implementation\examples\minimal_pilot_pipeline\build_research_package.py
```

## 6. Decisions et limites

- `test_reports` est traite comme un verdict de presence/coherence des
  rapports Test existants, faute de producteur normatif ou runtime explicite.
  Si une source precise est decouverte avant implementation, elle doit etre
  branchee et documentee au lieu de conserver cette derivation minimale.
- Le lot ne cree pas une notion normative nouvelle de candidate
  "influente". Il reutilise les candidates de `candidate_matrix`, deja
  l'artefact runtime qui represente la famille Test complete.
- Un basculement vers `FAIL` ou `INCONCLUSIVE` apres correction est
  acceptable si les preuves reelles le justifient.

## 7. Journal d'audit

| Date | Passe | Resultat |
| --- | --- | --- |
| 2026-07-18 | Redaction initiale | Brouillon cree apres revalidation du code reel et du chantier mere. |
| 2026-07-18 | `/evaluate` passe 1 | Correction du plan : `test_reports` ne doit pas rester `True`, et le test registre incomplet doit cibler un helper avant validation package plutot qu'une mutation post-build trop tardive. |
| 2026-07-18 | `/evaluate` passe 2 | Ajout du test Nautilus cible, car `nautilus_research_package.py` reutilise `pilot.build_package()` ; convergence sans nouveau blind spot majeur. |
