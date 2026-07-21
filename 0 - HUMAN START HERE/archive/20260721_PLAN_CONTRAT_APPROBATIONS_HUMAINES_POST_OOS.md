# Brouillon raffine — Contrat des approbations humaines pre-OOS

Date : 2026-07-21  
Parent : `PLAN_HORODATAGE_TRANSVERSAL_ET_ATTESTATIONS`  
Decision humaine : `3A`

## Objectif

Supprimer les approbations/reviewers fabriques par le chemin de production et
les remplacer par des inputs de preuve explicites, optionnels et auditables.
Sans preuve externe valide : scellement non PASS, autorisation OOS `DENIED`,
gates concernes `INCONCLUSIVE` et manifeste sans reviewer/approval invente.

## Perimetre exact

Inclus :

- `independent_registry_review` et `independent_pre_oos_approval` dans les gates ;
- `pre_oos_seal.independent_approval` et l'autorisation OOS ;
- `reviewers` et `approvals` du manifeste de reproductibilite ;
- contrat optionnel `pre_oos_human_evidence` ;
- voie `TEST_FIXTURE` explicite reservee aux tests.

Exclus par decision du 2026-07-17 : cycle post-OOS/live, `kill_switch`,
`live_approval`, `incident_log`, `retention_policy`, `live_version_id`,
`lifecycle_archive`. Aucun schema ni `Protocole/` ne change.

## Test multi-lot

`SINGLE`. Le contrat, sa propagation vers scellement/OOS/gates/manifeste et ses
tests de contraste forment une seule chaine causale. Aucun livrable autonome ne
peut etre ferme separement.

## Etat courant verifie

- Le builder ecrit litteralement `independent_registry_review=True` et
  `independent_pre_oos_approval=True`.
- `_pre_oos_sealing_report()` consomme la valeur fixture
  `pre_oos_seal.independent_approval`.
- `_oos_access_request()` recopie encore cette meme valeur.
- `manifest_builder.py` fabrique `independent_reviewer` et
  `runtime_fixture_approval`.
- Le rapport G-BIAS existant est hors de ce remplacement : son contrat propre
  reste gouverne par le chantier G-BIAS deja clos. Il ne peut cependant pas
  remplacer l'approbation OOS independante ajoutee ici.

## Architecture cible

### Contrat optionnel

`pilot_inputs["pre_oos_human_evidence"]` peut contenir :

- `registry_review` ;
- `pre_oos_approval`.

Chaque preuve doit porter `evidence_id`, `reviewer_id`, `status=APPROVED`,
`evidence_scope=EXTERNAL`, `approved_at` UTC et une reference/source non vide.
Une entree absente, incomplete, non approuvee ou de scope inconnu ne lève aucun
gate. Les champs inconnus ne doivent pas devenir une autorite implicite.

### Fixtures de test

`evidence_scope=TEST_FIXTURE` est refuse en production. Une option d'appel
explicite, non serialisee et nommee comme telle, peut l'autoriser uniquement
pour les tests. Le package/manifeste doit conserver le scope pour qu'une fixture
ne puisse pas etre confondue avec une preuve externe.

### Propagation

- Scellement : `independent_approval` derive de `pre_oos_approval`.
- OOS : `independent_approval` derive de la meme preuve scellee, jamais du JSON
  fixture historique.
- Gates : preuve valide => `PASS`; absence/invalide => `INCONCLUSIVE`.
- Manifeste : reviewers et approvals derives des preuves valides ; tableaux
  vides si aucune preuve.
- Le builder Nautilus accepte l'input explicite en frontiere ; par defaut il
  n'en fournit aucun et doit rester `DENIED` sans execution OOS.

## Phases

1. Definir/valider le contrat sans schema global nouveau.
2. Propager vers scellement, autorisation OOS, gates et manifeste.
3. Adapter les fixtures de tests via l'option `TEST_FIXTURE` explicite.
4. Prouver le contraste absent/invalide/externe/test-fixture et lancer la suite.

## Fichiers pressentis

- `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
- `Implementation/ebta_engine/manifests/manifest_builder.py`
- tests du pilote, manifeste et builder Nautilus
- fixture d'input uniquement pour retirer la valeur morte ou la marquer fixture
- historique runtime.

Interdits : `Protocole/`, schemas, validateurs, BACKTRADER, champs post-OOS/live.

## Exit criteria

1. Absence de `pre_oos_human_evidence` => scellement non PASS, OOS `DENIED`,
   zero appel runner OOS, gates d'approbation non PASS, manifeste vide.
2. Preuves externes valides => reviewer/approval exacts propages sans valeur
   fabriquee et autorisation seulement si tous les autres gates passent.
3. `TEST_FIXTURE` est refuse par defaut et accepte uniquement par une option de
   test explicite ; son scope reste visible.
4. Aucun litteral `True`, `independent_reviewer` ou `runtime_fixture_approval`
   ne subsiste comme preuve de production dans le perimetre.
5. Aucun champ post-OOS/live, schema, validateur ou Protocole modifie.
6. Tests cibles, suite venv, bug-hunter et plan-conformance PASS.

## Audit `/evaluate` du brouillon

### Passe 1 — 2026-07-21

- Ajout de l'autorisation OOS et du scellement au chemin causal : corriger les
  gates seuls aurait laisse l'OOS autorise par la fixture historique.
- Le manifeste doit lire la preuve scellee depuis la config, pas accepter des
  arguments humains paralleles qui creeraient deux sources de verite.
- G-BIAS reste hors scope ; sa revue ne vaut pas approbation OOS.

### Passe 2 — 2026-07-21

- La voie fixture doit etre une option runtime non serialisee, sinon un fichier
  d'input pourrait auto-autoriser la production.
- Les tableaux vides du manifeste sont valides sans changement de schema.
- La meme fonction de validation doit alimenter scellement, gates et manifeste
  afin d'eviter des verdicts divergents.

Aucun nouveau blind spot majeur : convergence obtenue.
