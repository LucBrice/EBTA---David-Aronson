# Brouillon - Lot F : preuves d'invariants derivees et scellement horodate

## Demande

Corriger `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
afin que `reports/invariant_evidence.json` ne fabrique plus les valeurs
`pre_oos_sealed_at`, `oos_openings[].wrc_local_status`,
`transformation_fits` et `decision_events`.

Ce lot est le sous-chantier `PLAN_CORRECTION_INVARIANT_EVIDENCE_LOT_F` de
`EPIC_ATTESTATIONS_RESIDUELLES_R3`. Il est `SINGLE` : les quatre derivations
forment un seul flux coherent d'assemblage et de validation du meme artefact.

## Decision humaine du 2026-07-20

- En production, la date de scellement doit etre capturee automatiquement en
  UTC au moment ou `validate_pre_oos_seal()` confirme un scellement reussi.
- Une IA ou un humain ne saisit pas cette date comme preuve d'une recherche
  reelle.
- Les tests et le pilote reproductible peuvent injecter une horloge fixe,
  explicitement identifiee comme fixture.
- L'automatisation de tous les autres jalons methodologiques est un chantier
  transversal distinct. Lot F etablit seulement le patron pour le scellement.
- `Protocole/` reste intact ; aucune nouvelle regle, gate ou valeur de verdict
  n'est introduite.

## Etat reel verifie

- `_write_reports()` ecrit encore `pre_oos_sealed_at` avec le literal
  `2023-01-01T00:00:00Z`.
- `_write_reports()` ecrit encore `wrc_local_status: PASS` pour chaque fold.
- `_write_reports()` ecrit encore une transformation `scaler/Train_k` qui ne
  vient pas du rapport `ml_manifest`.
- `_write_reports()` ecrit encore un evenement de decision date de 2023 qui ne
  vient pas de `data_availability_checks`.
- `validate_pre_oos_seal()` retourne seulement `artifact_type`, `status` et
  `violations`.
- Le pilote courant contient un seul fold et un seul verdict WRC agrege. Il ne
  fournit pas un rapport WRC local distinct pour chaque fold d'un calendrier
  multi-fold.

## Architecture attendue

1. Etendre `validate_pre_oos_seal()` avec une dependance d'horloge optionnelle
   `clock: Callable[[], datetime] | None = None`. L'horloge par defaut capture
   l'heure UTC du runtime. Une horloge injectee rend les tests et fixtures
   deterministes. Toute valeur retournee par l'horloge doit etre timezone-aware
   et normalisee en ISO-8601 UTC suffixe `Z`.
2. Ajouter `sealed_at` et la provenance de l'horloge au rapport uniquement si
   le scellement est `PASS`. Un echec de scellement ne produit pas de faux
   jalon date.
3. Faire propager `procedure_reports["sealing"]["sealed_at"]` vers
   `invariant_evidence["pre_oos_sealed_at"]`.
4. Deriver `transformation_fits` de
   `procedure_reports["ml_manifest"]["transformations"]`.
5. Deriver `decision_events` de
   `pilot_inputs["data_availability_checks"]` en renommant `available_at` vers
   `data_available_at` et en conservant `decision_at`.
6. Pour le pilote mono-fold courant, mapper le verdict WRC reel sur l'unique
   `fold_id`. Si plusieurs folds sont fournis sans rapports WRC locaux par
   fold, produire `wrc_local_status: INCONCLUSIVE` pour chaque ouverture :
   `INV-003` doit alors etre non passant. Ne jamais dupliquer silencieusement
   un verdict agrege comme preuve locale et ne jamais emettre une liste vide,
   car le validateur courant la considererait a tort comme passante.
7. Ajouter dans `pre_oos_seal` des inputs pilote une cle
   `fixture_sealed_at`, utilisee uniquement par le builder d'exemple pour
   construire l'horloge injectee. Elle doit preceder l'acces OOS du pilote et
   ne doit pas etre passee comme un `sealed_at` libre a la procedure.
8. Dans `invariant_evidence`, utiliser `sealing.get("sealed_at")` : un
   scellement en echec reste representable par une preuve manquante/non
   concluante au lieu de provoquer un timestamp fabrique ou un `KeyError`.

## Perimetre envisage

Autorises :

- `Implementation/ebta_engine/procedures/sealing.py`
- `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
- `Implementation/examples/minimal_pilot_pipeline/inputs/pilot_inputs.json`
- `Implementation/examples/minimal_pilot_pipeline/research_package/`
- `Implementation/ebta_engine/tests/test_procedure_governance.py`
- `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py`
- `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`
- plan Lot F, epic parent et `.ai/checkpoint.json` via `plan.ps1`

Interdits :

- `Protocole/`
- `Implementation/ebta_engine/validators/invariant_validator.py`
- `Implementation/ebta_engine/validators/gate_validator.py`
- `Implementation/research_packages/nautilus_mvp/` avant la Phase 4 de l'epic
- nouveaux statuts, seuils ou assouplissements d'invariants
- automatisation de tous les jalons EBTA dans ce lot

## Phases proposees

### Phase 1 - Contrat de scellement automatique

- Ajouter l'horloge runtime UTC et l'injection de fixture.
- Horodater uniquement un scellement `PASS`.
- Tester la capture automatique, l'injection deterministe et l'absence de
  timestamp sur `FAIL`.
- Tester le rejet d'une horloge injectee qui retourne un `datetime` sans
  timezone.

### Phase 2 - Derivations de invariant_evidence

- Propager `sealed_at` depuis `sealing`.
- Deriver WRC, transformations et evenements de decision depuis leurs sources
  reelles.
- Ajouter un test de contraste prouvant que les valeurs sources modifiees se
  retrouvent dans l'artefact et qu'aucun literal historique ne subsiste.
- Ajouter un test de garde multi-fold pour interdire une fausse preuve WRC
  locale et verifier que les statuts deviennent `INCONCLUSIVE`.

### Phase 3 - Regeneration pilote et audits

- Regenerer le package pilote minimal.
- Executer les tests cibles puis la suite runtime complete.
- Executer bug-hunter et plan-conformance-audit avant `/close`.
- Clore Lot F puis rendre la main a la Phase 4 de l'epic.

## Exit criteria

1. `sealing.json` contient un `sealed_at` UTC derive de l'horloge au moment du
   scellement `PASS` et identifie sa provenance runtime ou fixture.
2. Un scellement `FAIL` ne contient pas de `sealed_at`.
3. `invariant_evidence.json::pre_oos_sealed_at` est strictement egal au
   `sealed_at` de `sealing.json`.
4. Les transformations et evenements de decision sont strictement derives des
   sources existantes, sans literal de substitution.
5. Le verdict WRC de l'ouverture mono-fold est le verdict WRC reel ; un
   calendrier multi-fold sans WRC locaux produit des statuts `INCONCLUSIVE`
   et `INV-003` n'est pas `PASS`.
6. Les tests de contraste, la suite runtime, le build pilote, bug-hunter et
   plan-conformance-audit passent.

## NO GO

- Utiliser une date courante directement dans `_write_reports()`.
- Accepter un `sealed_at` libre fourni par une IA pour une execution reelle.
- Dater un scellement avant que ses controles aient reussi.
- Repliquer un verdict WRC agrege sur plusieurs folds et le presenter comme
  une preuve locale.
- Modifier un validateur pour rendre l'artefact fabrique acceptable.

## Journal d'audit du brouillon

| Passe | Resultat | Corrections |
| --- | --- | --- |
| 1 | Problematique moderee, architecture viable | Signature d'horloge fermee ; normalisation UTC et rejet des dates naives ; cle `fixture_sealed_at` separee ; scellement FAIL sans timestamp ; multi-fold fixe a `INCONCLUSIVE` plutot qu'une liste vide ou un verdict agrege duplique. |
| 2 | Convergence, risque modere et perimetre coherent | Verification des appelants reels : seuls le builder pilote et les tests appellent `validate_pre_oos_seal()` ; aucun JSON-Schema de rapport de scellement n'est modifie ; le fallback multi-fold rend `INV-003` non passant au lieu d'inventer une preuve. Aucun nouveau blind spot majeur. |
