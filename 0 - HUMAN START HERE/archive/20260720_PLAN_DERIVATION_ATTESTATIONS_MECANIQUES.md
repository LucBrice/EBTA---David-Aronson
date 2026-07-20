# Brouillon - Derivation des attestations mecaniques

## Objectif

Supprimer les constantes de gates qui peuvent etre derivees objectivement des
rapports et artefacts du package, sans fabriquer les approbations humaines qui
appartiennent au sous-chantier suivant.

## Classification et test multi-lot

`IMPLEMENTATION_DETAIL`, `SINGLE_CHANTIER`. Les trois sorties visees alimentent
le meme `gates.json` et partagent le meme contrat : preuve presente et validee
=> valeur/PASS; preuve absente => `INCONCLUSIVE` ou `FAIL` explicite.

## Defauts confirmes

`_write_reports()` code en dur :

- `live_version_id = "LIVE-PILOT-001"` au lieu de lire le rapport live ;
- `kill_switch = True` au lieu de deriver `kill_switch_tested` ;
- `lifecycle_archive`, `incident_log`, `retention_policy = True` alors que le
  package `VALIDATION_READY` ne contient aucun artefact G14.

Les constantes `independent_registry_review`, `independent_pre_oos_approval`,
`live_approval`, reviewers et approvals ne sont pas mecaniques : elles restent
hors perimetre et seront traitees par
`PLAN_CONTRAT_APPROBATIONS_HUMAINES_POST_OOS`.

## Architecture cible

1. Deriver `live_version_id` depuis `live_deployment_report.live_version_id` ;
   absence/chaine vide => `INCONCLUSIVE`.
2. Deriver `kill_switch` depuis `live_deployment_report.kill_switch_tested` :
   `True => PASS`, `False => FAIL`, absent => `INCONCLUSIVE`.
3. Passer `package_shape` au producteur de gates. Un mapping declaratif optionnel
   `gate_evidence_paths` associe chaque exigence G14 a un chemin deja inclus
   dans `artifact_paths`; le producer ne devine aucun nom de fichier. Mapping
   absent, chemin non declare ou fichier absent => `INCONCLUSIVE`. Un chemin
   absolu ou contenant une traversee hors `package_dir` est rejete.
4. Pour le package courant `VALIDATION_READY`, les trois champs G14 doivent etre
   `INCONCLUSIVE`, ce qui rend G14 `INCONCLUSIVE` sans invalider techniquement
   le build par une constante mensongere.
5. Ajouter un test de contraste : retirer/alterer chaque preuve fait perdre le
   PASS; un helper G14 sur artefacts temporaires declares prouve la branche PASS.
6. Accepter que le pilote `VALIDATION_READY` termine avec un rapport package
   `FAIL` cause uniquement par G14 `INCONCLUSIVE`. Le build doit rester complet,
   sans schema/manifest/semantic error; il est interdit de restaurer `PASS` avec
   une exemption de stage non encodee dans le contrat actuel.

## Perimetre pressenti

- `Implementation/examples/minimal_pilot_pipeline/build_research_package.py` ;
- `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py` ;
- historique moteur.

Pas de schema, Protocole, manifest reviewers/approvals, procedure lifecycle,
preuve humaine, nouveau fichier d'archive/incident, R5/R6 ou code Nautilus.

## Exit criteria

- Aucune des cinq sorties mecaniques visees n'est codee en dur.
- Le package courant expose G14 `INCONCLUSIVE` faute d'artefacts.
- Une preuve absente/false ne produit jamais `PASS`.
- Un jeu d'artefacts G14 temporaire declare produit les trois PASS mecaniques.
- Suite complete et Pyrefly PASS; le pilote se construit integralement et son
  unique gate non vert attendu est G14 `INCONCLUSIVE`.

## Journal `/evaluate`

- Passe 1 (2026-07-20) : suppression de l'hypothese contradictoire d'un pilote
  global PASS sans preuves G14; mapping declaratif retenu pour ne pas inventer
  les chemins lifecycle/incident/retention absents des contrats actuels.
- Passe 2 (2026-07-20) : ajout de la frontiere de securite sur les chemins du
  mapping et distinction `False => FAIL` / absent => `INCONCLUSIVE` pour le
  kill-switch. Aucun nouvel angle mort majeur; convergence atteinte.
