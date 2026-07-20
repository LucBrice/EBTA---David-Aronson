# Brouillon - Chantier mere Lot 3 : horodatage transversal et attestations

## Role

Sous-chantier 3/4 de
`EPIC_MATURITE_MOTEUR_CAMPAGNE_RECHERCHE`. Ce document coordonne sans coder
trois corrections independantes : horodatage runtime, derivation des
attestations mecaniques et contrat des approbations humaines/post-OOS.

## Test multi-lot

Verdict : `MULTI_LOT`.

1. Chaque composante a un Exit criteria autonome : timestamps runtime reels ;
   gates mecaniques derives ; approbations humaines explicites et non fabriquees.
2. Leur ordre peut changer sans changer leur sens.
3. La decision humaine sur les approbations n'empeche pas de corriger les
   timestamps ni les gates mecaniques.

IDs enfants prevus :

1. `PLAN_CHRONOLOGIE_ET_HORODATAGE_EVENEMENTS_RUNTIME`
2. `PLAN_DERIVATION_ATTESTATIONS_MECANIQUES`
3. `PLAN_CONTRAT_APPROBATIONS_HUMAINES_POST_OOS`

## Constats verifies le 2026-07-20

### A. Horodatage

- Le scellement pre-OOS est deja correct :
  `procedures/sealing.py` capture l'UTC en production et accepte une horloge
  injectee pour fixture. Ne pas le recreer.
- `_write_registry()` emet encore `timestamp: 2026-01-01T00:00:00Z` pour les
  evenements generes.
- Le builder Nautilus herite les timestamps fixture de `pilot_inputs.json` pour
  les acces OOS, la reproduction et le monitoring. Seul l'acces OOS est cree
  pendant ce build et releve donc de l'horloge runtime. Reproduction et
  consultations de monitoring sont des preuves externes/post-OOS : les
  horodater automatiquement pendant le build fabriquerait une fausse preuve.
- `bias_gate.py` et `incident_logger.py` capturent deja l'heure UTC, mais sans
  injection uniforme pour les fixtures ; ce point est a evaluer dans le plan
  enfant, sans elargir automatiquement le scope.
- Angle mort critique : `build_nautilus_inputs()` execute les segments OOS avant
  que `pilot.build_package()` ne calcule le WRC, la robustesse, le scellement et
  `authorize_oos_access()`. Ajouter seulement un timestamp apres coup
  fabriquerait une chronologie conforme en apparence. Le Lot 1 doit donc traiter
  l'ordre d'execution avec l'horodatage : aucune invocation du runner OOS avant
  scellement et autorisation reels. Un gate non-PASS doit produire un acces
  refuse et aucun resultat OOS, meme si le package global devient rouge.

### B. Attestations mecaniques

`build_research_package.py::_write_reports()` contient encore des facades
mecaniques ou d'existence d'artefact :

- `live_version_id = "LIVE-PILOT-001"` ;
- `kill_switch = True`, `live_approval = True` ;
- `lifecycle_archive = True`, `incident_log = True`, `retention_policy = True`.

Parmi ces champs, `live_version_id` et `kill_switch` peuvent etre derives du
rapport live existant. `lifecycle_archive`, `incident_log` et
`retention_policy` doivent deriver d'artefacts reels ; en leur absence, leur
verdict mecanique est `INCONCLUSIVE`. `live_approval` est humain et sort de ce
lot mecanique.

Les autres champs de gates deja derives (G1, G3-G12 couverts par les lots
precedents) ne doivent pas etre rouverts.

### C. Approbations humaines

- `manifest_builder.py::build_manifest()` fabrique toujours
  `reviewers=["independent_reviewer"]` et
  `approvals=["runtime_fixture_approval"]`.
- `pilot_inputs.json` contient des identites/approbations fixture valides pour
  le pilote minimal, mais le builder Nautilus les recopie dans un package reel.
- `_write_reports()` force `independent_registry_review=True` et
  `independent_pre_oos_approval=True` ; `_procedure_reports()` transmet
  `live_approval=True` ; `incubation_approval` est actuellement assimilee au
  statut de reproduction alors que G11 la nomme comme approbation distincte.
- Une approbation humaine ne peut pas etre deduite d'un calcul. En son absence,
  le gate doit etre `INCONCLUSIVE`/non autorise selon le contrat existant, jamais
  `PASS` par defaut.

## Enfants et ordre

### Enfant 1 - Chronologie et horodatage runtime

Separer le chemin pre-OOS (registre, Test, WRC, robustesse, scellement,
autorisation) du chemin OOS. Capturer l'UTC au moment des transitions reellement
executees (enregistrement avant Test ; acces immediatement avant lecture OOS),
avec horloge injectable pour les fixtures. Aucun OOS ne s'execute si
l'autorisation est refusee ; le succes de cet enfant est l'honnetete de la
chronologie, pas un package `PASS`.

Conserver les timestamps de marche/disponibilite issus des donnees et les
timestamps de reproduction/monitoring fournis par leurs producteurs externes ;
ils ne sont pas des timestamps de creation du package.

### Enfant 2 - Attestations mecaniques

Remplacer uniquement `live_version_id`, `kill_switch` et les preuves G14 par des
valeurs/statuts issus des rapports ou artefacts existants. Un artefact absent
rend le champ `INCONCLUSIVE`, pas `False` arbitraire ni `True`.

### Enfant 3 - Approbations humaines/post-OOS

Definir l'entree explicite qui porte reviewer, approbation, horodatage et preuve.
Les fixtures peuvent injecter une attestation clairement marquee fixture. Le
chemin Nautilus reel ne doit jamais heriter silencieusement cette attestation.
Ce lot possede `independent_registry_review`, `independent_pre_oos_approval`,
`incubation_approval`, `live_approval`, les reviewers/approvals du manifeste et
les timestamps externes reproduction/monitoring. La liste exacte des
approbations a exiger reste une decision humaine avant code.

## Perimetre du chantier mere

Ce document ne modifie que lui-meme et le cockpit via `plan.ps1`. Chaque enfant
definit son propre perimetre ferme, ses tests et son historique runtime.

Interdits : modifier `Protocole/`, ajouter des statuts/schemas sans decision,
fusionner les enfants, ou convertir une absence d'approbation en `PASS`.

## Exit criteria du chantier mere

- Les trois enfants sont `DONE`, ou l'enfant humain est explicitement differe
  par decision documentee.
- Aucun timestamp fixture n'est presente comme timestamp d'un run Nautilus reel.
- Aucun runner OOS n'est appele avant WRC/robustesse/scellement/autorisation ; un
  refus d'acces ne laisse aucune serie OOS fabriquee.
- Aucun champ de gate du perimetre ne reste un `True`/identifiant fabrique quand
  une preuve mecanique est requise.
- Les approbations humaines sont explicites, horodatees et tracables ; leur
  absence ne produit jamais `PASS`.
- Suite runtime, bug-hunter global et audit de conformite du chantier mere PASS.

## Decisions humaines requises

Avant l'enfant 3, choisir le perimetre des attestations humaines obligatoires :
revue independante du registre, approbation pre-OOS, approbation d'incubation,
approbation live, reviewer/approvals du manifeste et approbation d'archivage.

## Journal `/evaluate`

- 2026-07-20 - Passe 1 : separation corrigee entre timestamps crees par le run
  (registre/acces OOS), timestamps de donnees, et preuves externes
  (reproduction/monitoring). Les approbations independantes/live ont ete retirees
  du lot mecanique et rattachees au contrat humain ; le lot mecanique est limite
  aux preuves live/G14 objectivement derivables.
- 2026-07-20 - Passe 2 : angle mort critique d'ordonnancement ajoute au premier
  enfant. Le builder Nautilus calcule actuellement l'OOS avant les gates et le
  scellement ; un simple horodatage aurait cree une facade chronologique. Le
  critere impose maintenant une orchestration pre-OOS/OOS verifiable et accepte
  un package rouge si l'acces est legitimement refuse.
- 2026-07-20 - Passe 3 : aucun nouvel angle mort majeur. Convergence actee avec
  quatre frontieres explicites : donnees temporelles conservees, transitions du
  run horodatees au bon moment, preuves externes non fabriquees, attestations
  mecaniques derivees. Aucune modification de schema ou de `Protocole/` n'est
  autorisee par ce chantier mere.
