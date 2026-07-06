# Plan d'implementation - Moteur de backtest natif EBTA

## Audit IA de promotion

- [x] Plan relu dans le contexte du cockpit EBTA (`AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json`, `Implementation/Active/HOOK.md`, `Implementation/Active/tracking.json`).
- [x] Changement classe comme chantier `mainline` remplacant `STEP_3_BACKTRADER_INTEGRATION`.
- [x] Aucun changement de `Protocole/` requis pour l'activation du chantier.
- [x] BACKTRADER reste `REFERENCE_ONLY` tant que sa gouvernance locale et la provenance des donnees XAUUSD/NASDAQ ne sont pas documentees.
- [x] Les phases d'implementation restent bloquees par les prerequis factuels et la gouvernance IA explicite decrits en Phase -1 et Phase 0-BIS.

## Triage IA

| Champ | Valeur |
| --- | --- |
| Track | `mainline` |
| Lifecycle | `ACTIVE` |
| Scope | Refonte de l'integration BACKTRADER vers un moteur de backtest natif EBTA, avec BACKTRADER comme reference de reecriture uniquement. |
| Non-goals | Pas de modification de `Protocole/`; pas de copie runtime de BACKTRADER; pas de maintien du pipeline sectionnel BACKTRADER; pas d'application web avant MVP moteur; pas d'ouverture OOS opportuniste. |
| Source | Discussion utilisateur/Codex du 2026-07-02 autour de `STEP_3_BACKTRADER_INTEGRATION`. |
| Exit criteria | Un `research_package EBTA` complet est produit par le moteur natif pour XAUUSD et NASDAQ avec les payloads E, F, G, H, I decomposes en candidates EBTA, puis valide par les validateurs EBTA existants. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | DONE - PHASES_MINUS_1_TO_8_EXECUTEES |
| Date de creation | 2026-07-02 |
| Date d'activation | 2026-07-02 |
| Runtime cible | `EBTA-ENGINE-0.1.x` |
| Autorite normative | `Protocole/` gele en `EBTA-DOC-1.1` |
| Autorite executable | `Implementation/ebta_engine/` |
| Changement protocolaire | Aucun attendu |
| Repo BACKTRADER | Reference externe, lecture/audit seulement avant decision explicite |

## Resultat d'execution 2026-07-02

| Champ | Valeur |
| --- | --- |
| Phases executees | Phase -1 a Phase 8 |
| Package natif | `Implementation/research_packages/native_mvp` |
| Validation package | `PASS` via `python -m ebta_engine.package_builder.native_research_package` |
| Tests runtime | `PASS - 93 tests` via `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` |
| Protocole | Non modifie |
| BACKTRADER | Lu en reference seulement, non modifie |
| Phase 9 | Reportee hors de cette execution |

## Decisions humaines d'execution

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-02 | `1A` - Autorisation de lire BACKTRADER en lecture seule au chemin `D:\TRADING\ENTREPRISE\0 - Phase de lancement\Strategie de trading\0 - Backtest\BACKTRADER`. | BACKTRADER reste `REFERENCE_ONLY`, sans modification du repository et sans dependance runtime EBTA. |
| 2026-07-02 | `2B` - Source de donnees MVP fournie : `D:\TRADING\ENTREPRISE\0 - Phase de lancement\Strategie de trading\0 - Backtest\Data`. | La provenance XAUUSD/NASDAQ doit etre documentee depuis ce dossier ; BACKTRADER peut etre audite pour les loaders et conventions historiques seulement apres lecture de sa gouvernance. |
| 2026-07-02 | `3A` - Autorisation explicite de modifier `Implementation/` jusqu'a la Phase 8 de ce plan, sans modifier `Protocole/`. | Cette decision leve le verrou de `.ai/governance/AI_MODIFICATION_CHECKLIST.md` pour les changements de runtime strictement subordonnes au protocole gelee `EBTA-DOC-1.1`. |

## Decision d'architecture

EBTA devient le moteur natif complet de recherche et de backtest.

BACKTRADER ne doit plus etre considere comme un moteur a integrer durablement. Il
devient une source de reference historique et technique pour identifier des
composants utiles, notamment :

- payloads experimentaux E, F, G, H, I ;
- logique de chargement des donnees locales ;
- features, filtres, signaux, risk, sizing, execution et reporting existants ;
- erreurs et apprentissages historiques a ne pas reproduire.

La trajectoire cible est :

```text
Protocole/
  -> autorite normative EBTA

Implementation/ebta_engine/
  -> moteur natif, procedures, validateurs, gouvernance, schemas, tests

Implementation/notebooks/
  -> cockpit Jupyter reproductible, non normatif

research_package/
  -> paquet de preuve EBTA complet
```

## Decisions deja actees

- EBTA portera tout a terme; BACKTRADER doit devenir inutile pour executer une
  recherche EBTA.
- Les noms de dossiers natifs resteront proches de BACKTRADER quand cela aide la
  comprehension : `data`, `features`, `strategies`, `trading_signals`,
  `backtest`, `risk`, `metrics`, `viz`.
- Le MVP ne doit pas commencer par une application web dediee.
- Le cockpit initial peut rester en Jupyter, a condition que le notebook orchestre
  le moteur sans contenir la logique metier principale.
- Le premier objectif concret est un `research_package EBTA` complet, pas une
  simple demonstration de backtest.
- Les payloads E, F, G, H, I doivent etre decomposes car ils representent des
  combinaisons d'une meme famille strategique, notamment avec filtres horaires et
  filtre de biais.
- Le MVP doit couvrir au moins deux actifs : XAUUSD et NASDAQ.
- La matrice multi-actifs x payloads est obligatoire; une selection winner-only
  est interdite.

## Definition EBTA d'un payload experimental

Dans ce plan, une "strategie" ne designe pas seulement un nom de module. Elle
designe une combinaison preenregistree de degres de liberte.

Forme cible :

```text
StrategyPayload =
  asset
  timeframe
  strategy_family
  direction
  entry_level
  entry_criterion
  bias_filter
  time_filter
  session
  exit_criterion
  risk_model
  sizing_model
  parameters
  payload_version
  payload_hash
```

Chaque combinaison evaluee devient une candidate EBTA traçable dans le registre
et dans la candidate matrix.

## Perimetre MVP

### Actifs

```text
XAUUSD
NASDAQ
```

### Payloads de reference

```text
E
F
G
H
I
```

### Couverture minimale

```text
2 actifs x 5 payloads = 10 candidates minimum
```

Si la decomposition des payloads E-I revele des sous-combinaisons distinctes, le
nombre de candidates doit augmenter. Le MVP ne doit pas reduire la matrice a un
seul gagnant.

## Architecture cible dans Implementation

Structure proposee :

```text
Implementation/ebta_engine/
  data/
  features/
  strategies/
  trading_signals/
  backtest/
  risk/
  metrics/
  package_builder/
  procedures/             # existe deja
  validators/             # existe deja
  governance/             # existe deja
  schemas/                # existe deja
  manifests/              # existe deja
  tests/                  # existe deja

Implementation/notebooks/  # cockpit Jupyter, separe du package Python (voir Phase 8)

Implementation/research_packages/  # paquets reels generes hors fixtures, gitignore (voir Phase 7)
```

Placement des notebooks tranche : `Implementation/notebooks/`, separe du
package Python `Implementation/ebta_engine/` (voir Phase 8 et "Questions
tranchees").

## Phases d'implementation

### Phase -1 - Deblocage des prerequis factuels (bloquant, avant toute autre phase)

Objectif : lever les deux hypotheses implicites qui bloquent l'execution du
plan avant meme la Phase 0, identifiees par audit d'architecture du
2026-07-02.

Constat :

- `Implementation/EXTERNAL_ENGINE_PROCEDURE_MAPPING.md` declare
  `External repo access: FORBIDDEN_IN_THIS_LOT` et precise avoir ete redige
  sans lire ni acceder au repository BACKTRADER. Cette contrainte n'a jamais
  ete levee. La Phase 1 de ce plan presuppose pourtant un audit direct des
  dossiers `data/`, `features/`, `strategies/`, `trading_signals/`,
  `backtest/`, `risk/`, `metrics/`, `viz/` de ce repository.
- Aucun fichier de donnees XAUUSD/NASDAQ n'existe dans ce repo. Ni la source
  (broker, vendor, export local), ni le format brut, ni la licence, ni la
  fenetre temporelle disponible ne sont documentes.

Actions :

- obtenir une decision humaine explicite autorisant l'acces au repository
  BACKTRADER et documentant son chemin reel ;
- documenter la source, le format, la licence et la couverture temporelle des
  donnees XAUUSD/NASDAQ.

Livrables :

- decision humaine tracee (chemin BACKTRADER autorise) ;
- fiche de provenance des donnees XAUUSD/NASDAQ.

Critere de sortie :

- la Phase 1 et la Phase 2 deviennent executables sans hypothese implicite ;
- sans ce lot, aucune phase suivante ne doit demarrer.

### Phase 0 - Stabiliser la decision d'architecture

Objectif : transformer ce draft en plan executable.

Actions :

- confirmer que ce plan remplace l'ancienne logique "moteur externe -> EBTA
  juge" ;
- classer BACKTRADER en `REFERENCE_ONLY` ;
- identifier les fichiers EBTA a mettre a jour lors du passage en plan actif ;
- renommer `Implementation/EXTERNAL_ENGINE_PROCEDURE_MAPPING.md` en
  `Implementation/NATIVE_ENGINE_PROCEDURE_MAPPING.md` et reecrire son contenu
  pour decrire le contrat reel du moteur natif (le moteur produit lui-meme
  les artefacts, il n'y a plus de "moteur externe" a mapper) ; ne pas
  conserver de copie separee de l'ancienne version "external engine" dans
  l'arborescence active, l'historique git suffit a tracer l'ancienne
  formulation ; ce plan cite ce document comme reference unique au lieu de
  dupliquer sa table en Phase 6 ;
- decider explicitement du sort de
  `Implementation/ebta_engine/adapters/backtrader_mapping.py` (deja present
  dans le repo) : `MIGRATE`, `ADAPT`, `REWRITE` ou `REJECT` ; trancher dans le
  meme mouvement le sort de
  `Implementation/ebta_engine/tests/test_backtrader_adapter.py`, qui importe
  directement ce module et casse la suite de tests si `REJECT` ou `REWRITE`
  est choisi sans que ce test soit lui-meme supprime, reecrit ou adapte en
  consequence ;
- identifier les documents d'entree humaine qui referencent BACKTRADER comme
  moteur actif et doivent etre mis a jour en meme temps que ce plan devient
  actif : `Implementation/0-CARTE_DU_CODE_EBTA.md`,
  `Implementation/GUIDE - Construire un pipeline de recherche EBTA.md`.

Livrables :

- decision d'architecture dans ce plan ;
- liste `MIGRATE`, `ADAPT`, `REWRITE`, `REJECT` par composant BACKTRADER ;
- aucun changement de `Protocole/`.

Critere de sortie :

- le plan est suffisamment clair pour etre promu comme chantier actif sans
  modifier la doctrine EBTA.

### Phase 0-BIS - Levee du verrou de gouvernance

Objectif : aligner la couche d'etat machine (`.ai/checkpoint.json`,
`Implementation/Active/tracking.json`, `HOOK.md`) et la couche de gouvernance
IA (`.ai/governance/AI_MODIFICATION_CHECKLIST.md`) sur ce plan, avant toute
phase d'implementation. Sans cette phase, les Phases 2 a 8 modifient du code
d'implementation en violation d'une regle de gouvernance active du repo et le
suivi machine-readable continue de pointer vers une strategie deja
remplacee.

Actions :

- tracer, dans un registre de decision approprie (voir
  `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md` si applicable, sinon
  un registre non-normatif equivalent cote `Implementation/` ou `.ai/`), la
  decision humaine explicite qui autorise les Phases 2 a 8 comme
  "modification de code d'implementation" au sens de
  `.ai/governance/AI_MODIFICATION_CHECKLIST.md` (section "Modifications
  interdites sans decision explicite") ; sans cette trace, chaque phase
  d'implementation viole une regle de gouvernance active du repo ;
- mettre a jour `.ai/checkpoint.json` (`active_workstream_id`, entree
  `workstreams[]` pour ce plan, `risks[R2]`) et
  `Implementation/Active/tracking.json` + `HOOK.md`, pour remplacer l'etat
  actuel qui pointe vers `STEP_3_BACKTRADER_INTEGRATION` (strategie "adapter
  externe -> EBTA juge") par l'etat du plan natif ;
- clore `.ai/backlog/mainline/EPIC_reprise_et_integration_backtrader.md`
  (lifecycle -> `SUPERSEDED`, `is_active` -> `false`, `closure_reason`
  referencant ce plan comme remplacant).

Livrables :

- entree de registre de decision tracant l'autorisation humaine explicite ;
- `.ai/checkpoint.json` et `Implementation/Active/tracking.json` valides
  contre leur schema (commandes deja listees dans `CLAUDE.md`) et coherents
  avec ce plan ;
- `HOOK.md` mis a jour ;
- `EPIC_reprise_et_integration_backtrader.md` marque `SUPERSEDED`.

Critere de sortie :

- aucune contradiction entre `.ai/checkpoint.json`, `tracking.json`,
  `HOOK.md` et ce plan ;
- la regle de gouvernance sur le code d'implementation est explicitement
  levee ;
- la suite de tests reste `PASS` apres le tri du module adapter et de son
  test (voir Phase 0).

### Phase 1 - Audit cible BACKTRADER

Objectif : localiser les payloads E, F, G, H, I et les donnees XAUUSD/NASDAQ.

Actions :

- lire la gouvernance BACKTRADER avant toute exploration de code ;
- auditer les dossiers BACKTRADER suivants en lecture seule :
  - `data`;
  - `features`;
  - `strategies`;
  - `trading_signals`;
  - `backtest`;
  - `risk`;
  - `metrics`;
  - `viz` seulement pour inventaire, sans priorite MVP ;
- localiser les definitions ou configurations des payloads E-I ;
- localiser les sources, formats et loaders des donnees XAUUSD/NASDAQ ;
- identifier les dependances au pipeline sectionnel BACKTRADER ;
- documenter explicitement dans `PAYLOAD_DECOMPOSITION_E_TO_I.md` que les
  identifiants de payloads E, F, G, H, I proviennent d'une discussion
  utilisateur/Codex externe du 2026-07-02 et non d'un artefact deja present
  dans le repo EBTA, jusqu'a confirmation par l'audit BACKTRADER reel prevu
  dans cette meme phase.

Livrables :

- `PAYLOAD_DECOMPOSITION_E_TO_I.md` ;
- `BACKTRADER_DATA_SOURCE_AUDIT.md` ;
- matrice des composants : `MIGRATE`, `ADAPT`, `REWRITE`, `REJECT` ;
- liste des elements interdits : pipeline S1-S9, verdicts BACKTRADER, stubs,
  conventions non EBTA.

Critere de sortie :

- EBTA sait quoi reecrire sans dependre de BACKTRADER au runtime.

### Phase 2 - Couche data native EBTA

Objectif : charger XAUUSD et NASDAQ localement dans un format canonique EBTA.

Actions :

- creer `Implementation/ebta_engine/data/` ;
- definir le format canonique OHLCV et metadata ;
- gerer timezone/UTC ;
- produire des checksums ;
- documenter la disponibilite point-in-time ;
- verifier que les donnees chargees ne contiennent pas d'information future ;
- pour le MVP, charger un sous-ensemble deterministe et documente (fenetre de
  dates fixe, identique a chaque execution) plutot que l'integralite des
  donnees locales disponibles ; ce sous-ensemble sert a prouver que le
  pipeline produit un `research_package/` valide rapidement et de facon
  reproductible ; le passage a l'integralite des donnees locales est une
  decision separee, prise seulement une fois le pipeline prouve sur ce
  sous-ensemble, pour ne pas melanger validation d'architecture et ouverture
  de recherche reelle.

Livrables :

- loader natif EBTA ;
- tests unitaires data ;
- `reports/data_availability.json` produit pour le package ;
- fixtures minimales XAUUSD/NASDAQ si necessaire.

Critere de sortie :

- les deux actifs MVP sont chargeables et auditables par EBTA.

### Phase 3 - Payload generator et candidate matrix

Objectif : transformer E-I en candidates EBTA completes.

Actions :

- creer `Implementation/ebta_engine/strategies/` ;
- creer ou completer `Implementation/ebta_engine/trading_signals/` ;
- definir `StrategyPayload` et l'enregistrer comme schema versionne dans
  `Implementation/ebta_engine/schemas/`, avec une entree dans
  `Implementation/ebta_engine/migrations/` si un schema anterieur existe deja ;
- definir le generateur de payloads ;
- produire toutes les combinaisons asset x payload ;
- emettre les evenements `registry.jsonl` ;
- produire `reports/candidate_matrix.json`.

Livrables :

- decomposition executable des payloads E-I ;
- generation minimale de 10 candidates ;
- tests de couverture multi-actifs x payloads ;
- rejet explicite si une combinaison attendue manque.

Critere de sortie :

- la candidate matrix respecte la logique EBTA de famille candidate complete.

### Phase 4 - Features et signaux causaux

Objectif : produire des signaux causaux pour chaque candidate.

Actions :

- creer `Implementation/ebta_engine/features/` ;
- reecrire les features utiles depuis BACKTRADER comme reference ;
- implementer les filtres horaires et de biais ;
- verifier l'alignement temporel ;
- eliminer toute dependance a l'etat cache du pipeline BACKTRADER ;
- produire un `SignalDecisionFrame` par candidate.

Livrables :

- features natives EBTA ;
- signaux par candidate ;
- tests no-lookahead ;
- tests cache/signature si un cache est introduit.

Critere de sortie :

- les signaux peuvent etre recalcules de facon deterministe depuis les donnees
  locales et le payload preenregistre.

### Phase 5 - Backtest, risk, execution

Objectif : executer les candidates sans stub ni convention BACKTRADER.

Actions :

- creer `Implementation/ebta_engine/backtest/` ;
- creer `Implementation/ebta_engine/risk/` ;
- implementer fills, couts, frictions, sizing, risk model et exits ;
- produire PnL, NAV, exposition, couts et series de rendements ;
- conserver les erreurs de contrat explicites.

Livrables :

- moteur de backtest natif minimal ;
- `reports/execution.json` ;
- `reports/economic.json` ;
- series de rendement requises par les procedures EBTA ;
- tests anti-stub PnL.

Critere de sortie :

- chaque candidate produit une trace d'execution exploitable par les procedures
  EBTA.

### Phase 6 - Connexion aux procedures EBTA existantes

Objectif : brancher le moteur natif sur les procedures deja presentes dans
`Implementation/ebta_engine/procedures/`.

Procedures concernees (liste complete : les 13 modules d'origine plus les 9
modules omis par erreur, tous deja presents dans
`Implementation/ebta_engine/procedures/`) :

```text
search_space.py
walk_forward.py
candidate_matrix.py
optimization.py
complexity_selection.py
wrc.py
robustness.py
returns.py
economic_gate.py
data_availability.py
oos_access.py
oos_confidence_interval.py
reproduction_report.py
bootstrap.py
detrending.py
zero_centering.py
lifecycle.py
sealing.py
monitoring.py
registry_lineage.py
ml_manifest.py
incubation_report.py
```

Actions :

- alimenter les artefacts attendus par les procedures ;
- respecter les schemas existants ;
- ne pas creer de nouveau gate ou seuil ;
- utiliser les validateurs existants comme source de verdict runtime.

Livrables :

- pipeline natif vers artefacts EBTA ;
- tests d'integration procedures ;
- erreurs explicites si un artefact manque.

Critere de sortie :

- le moteur natif produit des sorties consommables par les validateurs EBTA sans
  adaptation manuelle.

### Phase 7 - Research package complet

Objectif : produire un paquet EBTA complet depuis le moteur natif.

Actions :

- creer `Implementation/ebta_engine/package_builder/` ou etendre proprement le
  pilote minimal existant ; `package_builder/` orchestre uniquement, toute
  ecriture bas niveau reste dans `persistence.py` (pas de duplication d'I/O) ;
- produire la structure `research_package/` ;
- integrer manifests, hashes et reproduction report ;
- executer `validate_package_dir()` ;
- adopter une convention de nommage/emplacement distincte pour un
  `research_package/` partiel produit pendant les Phases 3 a 6 (`draft`) et un
  paquet complet valide (`final`), afin qu'un paquet incomplet ne soit jamais
  confondu avec une preuve EBTA valide ;
- produire les paquets reels (non-fixtures) dans
  `Implementation/research_packages/`, un repertoire dedie, distinct de
  `Implementation/examples/minimal_pilot_pipeline/research_package/` (qui
  reste une fixture de regression, petite et committee) et distinct de
  `Implementation/ebta_engine/fixtures/` (fixtures de test) ; ajouter
  `Implementation/research_packages/` a `Implementation/.gitignore`, car les
  paquets reels contiennent des series issues de donnees reelles et sont
  regenerables de facon deterministe depuis les donnees, le payload et les
  procedures — ils n'ont pas besoin d'etre versionnes dans git.

Sortie attendue :

```text
research_package/
  config.json
  registry.jsonl
  oos_access_log.jsonl
  reports/
    candidate_matrix.json
    optimization_log.json
    complexity_selection.json
    data_availability.json
    fold_schedule.json
    wrc.json
    execution.json
    economic.json
    robustness.json
    reproduction.json
    g_bias.json
  series/
  manifests/
```

Critere de sortie :

- le paquet est valide par les validateurs EBTA ;
- la couverture XAUUSD/NASDAQ x E-I est prouvee ;
- G-BIAS est compatible ;
- aucun verdict ne vient de BACKTRADER ou d'un notebook.

### Phase 8 - Notebooks Jupyter rigoureux

Objectif : fournir un cockpit de suivi et d'audit sans mettre la logique metier
dans les notebooks.

Placement : `Implementation/notebooks/`, separe du package Python
`Implementation/ebta_engine/` (voir "Architecture cible dans Implementation").

Structure proposee :

```text
Implementation/notebooks/
  00_preflight.ipynb
  01_payload_decomposition_E_to_I.ipynb
  02_data_audit_XAUUSD_NASDAQ.ipynb
  03_candidate_matrix_build.ipynb
  04_native_backtest_run.ipynb
  05_research_package_validation.ipynb
```

Regles :

- le notebook appelle les modules Python du runtime ;
- le notebook ne decide pas des verdicts ;
- execution de haut en bas obligatoire ;
- les parametres viennent d'une configuration preenregistree ;
- automatisation future possible via execution programmatique de notebook.

Critere de sortie :

- un utilisateur peut suivre la rigueur EBTA dans Jupyter sans casser la
  reproductibilite.

### Phase 9 - Interface web reportee

Objectif : ne pas construire de plateforme web avant que le moteur natif soit
capable de produire un package complet.

Trajectoire future :

```text
Jupyter strict
-> notebooks automatises
-> dashboard leger eventuel
-> plateforme web complete
```

La plateforme future devra servir a :

- lancer des runs ;
- suivre leur statut ;
- historiser les packages ;
- comparer les matrices ;
- afficher les gates ;
- inspecter les erreurs de contrat ;
- visualiser les artefacts.

Elle ne devra jamais produire les verdicts EBTA elle-meme.

## Validation

Regle transversale (bloquante entre chaque phase, pas seulement en fin de
plan) :

- `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`
  doit rester `PASS` (87 tests au 2026-07-01) avant de demarrer chaque phase
  suivante ; une phase qui casse la suite existante ne peut pas etre
  consideree terminee.

Note de portabilite : `Implementation/ebta_engine/tests/test_protocol_manifest_hashes.py`
resout `Protocole/` par chemin relatif (`Path(__file__).resolve().parents[3]`,
pas de chemin Windows en dur), mais compare un SHA-256 octet pour octet sur
les fichiers geles de `Protocole/` ; ce hash est donc sensible a la
normalisation de fin de ligne (CRLF/LF) selon la configuration git de
l'environnement de checkout. Le dernier resultat trace
(`.ai/checkpoint.json`, 2026-07-01) est un `PASS` obtenu sur environnement
Windows/PowerShell ; la portabilite sur un checkout non-Windows n'est pas
verifiee. Ce plan ne corrige pas ce point ; une decision separee doit
confirmer si c'est un choix assume (repo travaille exclusivement sous
Windows) ou si un ticket distinct doit neutraliser la sensibilite aux fins de
ligne.

Commandes de reference :

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
python Implementation\examples\minimal_pilot_pipeline\build_research_package.py
python -m json.tool Implementation\Active\tracking.json
python -m json.tool .ai\checkpoint.json
git diff --check -- Implementation Protocole .ai
```

Validations specifiques a ajouter :

- tests de decomposition E-I ;
- tests de couverture XAUUSD/NASDAQ x payloads ;
- tests no-lookahead ;
- tests anti-stub PnL ;
- tests de generation `research_package/` complet ;
- tests de rejet winner-only ;
- tests de rejet OOS pre-scellement.

## NO GO

- Copier BACKTRADER comme dependance runtime.
- Maintenir le pipeline sectionnel BACKTRADER comme architecture.
- Utiliser les sections S1-S9 comme source de verite EBTA.
- Produire seulement le meilleur payload.
- Omettre une combinaison asset x payload evaluee.
- Ouvrir OOS avant scellement.
- Faire d'un notebook une source de verdict.
- Faire de `viz` une source de verdict.
- Modifier `Protocole/` pour accommoder BACKTRADER.
- Coder une regle methodologique absente des SOP.
- Ajouter une dependance technique avant decision explicite.

## Premier lot executable propose

Le premier lot a executer apres validation de ce draft :

```text
LOT 1 - Audit cible BACKTRADER E-I et donnees XAUUSD/NASDAQ
```

Objectifs :

- lire la gouvernance BACKTRADER ;
- localiser les payloads E, F, G, H, I ;
- decomposer les payloads en dimensions EBTA ;
- localiser les donnees XAUUSD/NASDAQ ;
- produire une table de mapping vers `StrategyPayload` et `candidate_matrix`.

Sorties attendues :

- `PAYLOAD_DECOMPOSITION_E_TO_I.md` ;
- `BACKTRADER_DATA_SOURCE_AUDIT.md` ;
- liste des composants BACKTRADER a reecrire ;
- liste des composants BACKTRADER a rejeter.

Critere de sortie :

- EBTA possede une specification suffisante pour commencer la reecriture native
  sans importer BACKTRADER comme dependance.

## Questions tranchees (2026-07-02)

Les trois questions ouvertes precedentes sont tranchees. Le detail de chaque
decision est deja integre dans la phase concernee ci-dessus ; ce qui suit en
est le resume et la justification.

1. `Implementation/EXTERNAL_ENGINE_PROCEDURE_MAPPING.md` → **renomme en
   `Implementation/NATIVE_ENGINE_PROCEDURE_MAPPING.md`, contenu reecrit**
   (voir Phase 0). Justification : une fois le moteur natif operationnel, ce
   document ne decrit plus une realite existante — il n'y a plus de "moteur
   externe" a mapper. Le conserver tel quel sous son nom et son cadrage
   actuels serait ecrire un document obsolete des sa creation. L'ancienne
   version reste retrouvable via l'historique git ; aucune copie separee
   n'est maintenue dans l'arborescence active.
2. Repertoire dedie pour les paquets reels → **oui,
   `Implementation/research_packages/`, ajoute au `.gitignore`** (voir
   Phase 7). Justification : distinct des fixtures de test et du pilote
   minimal (petits, deterministes, committes a dessein), les paquets reels
   contiennent des series issues de donnees de marche et sont regenerables a
   la demande ; les committer polluerait l'historique git sans y ajouter de
   preuve non reproductible.
3. Perimetre de donnees pour le MVP → **sous-ensemble deterministe et
   documente, pas l'integralite des donnees locales** (voir Phase 2).
   Justification : le MVP doit prouver que le pipeline produit un
   `research_package/` valide de facon rapide et reproductible ; passer a
   l'integralite des donnees est une decision distincte, prise seulement
   apres cette preuve, pour ne pas melanger validation d'architecture et
   ouverture de recherche reelle.
