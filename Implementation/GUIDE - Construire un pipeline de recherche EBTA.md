# GUIDE - Construire un pipeline de recherche EBTA

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - GUIDE_IMPLEMENTATION_PIPELINE |
| Version runtime cible | EBTA-ENGINE-0.1.0 |
| Autorite normative | `Protocole/` gele en `EBTA-DOC-1.0` |
| Contrats executables | `Implementation/ebta_engine/` |
| Impact protocole | NONE |

## Fonction de ce guide

Ce fichier explique comment construire ou refondre un pipeline de recherche en
utilisant ensemble :

- `Protocole/` comme source normative scientifique ;
- `Implementation/ebta_engine/` comme contrat executable et banc de controle ;
- un futur moteur de backtest comme producteur d'artefacts EBTA.

Le pipeline de recherche ne doit pas seulement calculer une performance ni
seulement produire des fichiers de sortie. Il doit mettre en place les blocs de
recherche imposes par le protocole, puis produire les preuves verifiables que
ces blocs ont fonctionne dans le bon ordre.

## Separation des roles

| Couche | Role | Ne doit pas faire |
| --- | --- | --- |
| `Protocole/` | Definit les regles scientifiques : gates, SOP, decisions normatives, ordre Train/Test/OOS, WRC, OOS, live. | Ne doit pas etre modifie pour faciliter le code. |
| `Implementation/ebta_engine/` | Encode les contrats machine-readable : schemas, validateurs, manifestes, invariants, gates, fixtures. | Ne doit pas inventer de nouvelle norme. |
| Pipeline de recherche | Charge les donnees, construit les features, execute les strategies, calcule les resultats, produit les artefacts EBTA. | Ne doit pas contourner les validations EBTA. |
| Adaptateur | Mappe un pipeline externe vers les artefacts EBTA. | Ne doit pas importer les conventions externes dans le noyau EBTA. |

## Idee centrale

Une IA ne doit pas recevoir seulement :

```text
Construis un moteur de backtest avec le protocole EBTA.
```

Elle doit recevoir :

```text
Construis ou refonds un pipeline de recherche qui produit un paquet EBTA
conforme aux contrats `Implementation/ebta_engine/`, puis valide ce paquet avec
la quality gate EBTA. Le protocole reste l'autorite normative.
```

Le protocole dit quoi respecter.

`Implementation/` dit comment prouver que c'est respecte.

## Architecture cible d'un pipeline EBTA

```text
Donnees point-in-time
        |
        v
Configuration preregistree
        |
        v
Generateur de folds Train/Test/OOS
        |
        v
Moteur de recherche candidates
        |
        v
Registre append-only des experiences
        |
        v
Selection locale + WRC Test
        |
        v
Robustesse pre-OOS + paquet PRE_OOS_SEALED
        |
        v
Ouverture OOS journalisee
        |
        v
Estimation OOS + gate economique
        |
        v
Paquet VALIDATION_READY / DEPLOYMENT_CERTIFIED
        |
        v
Validation par Implementation/ebta_engine
```

## Blocs de recherche obligatoires

Un pipeline EBTA doit etre construit comme une suite de blocs de recherche. Les
artefacts ne sont que les preuves produites par ces blocs.

| Bloc | Fonction dans le pipeline | Source normative | Preuves attendues |
| --- | --- | --- | --- |
| Bloc 1 - Intention de recherche | Definir hypothese, famille, univers, actifs, periode, frequence, criteres d'echec et point d'arret. | Protocole sections 2, 8; SOP 03; SOP 12 | `config.json`, template hashe, identifiants projet/famille/hypothese |
| Bloc 2 - Donnees point-in-time | Charger uniquement des donnees disponibles au moment des decisions, avec publication, ingestion, latence et anti-leakage. | Protocole sections 3, 8; SOP 09A | snapshots, timestamps, rapport anti-leakage |
| Bloc 3 - Segmentation Walk-Forward | Construire les folds `Train_k`, `Test_k`, `OOS_k`, purge, embargo et calendrier non chevauchant. | Protocole section 3; SOP 04 | calendrier des folds, preuve INV-001, config de purge/embargo |
| Bloc 4 - Univers de candidates | Generer et identifier toutes les candidates qui peuvent influencer une decision. | SOP 03; SOP 06; DN-005 a DN-008 | `registry.jsonl`, catalogue candidates, matrice locale |
| Bloc 5 - Calibration Train | Calibrer parametres et transformations uniquement sur `Train_k`. | SOP 06; SOP 09A; DN-026 | logs de fit, preuves INV-006 |
| Bloc 6 - Selection et inference Test | Appliquer la regle de selection preenregistree et le WRC local avant toute ouverture OOS. | Protocole section 6; SOP 02; SOP 06 | `reports/wrc.json`, statut WRC, selected candidate |
| Bloc 7 - Robustesse pre-OOS | Executer les stress-tests decisionnels avant observation OOS. | SOP 05; DN-030 | `reports/robustness.json`, matrice de robustesse |
| Bloc 8 - Execution tradable | Transformer signaux en ordres, fills, positions, couts, capacite, sizing et NAV. | Protocole section 7; SOP 08; SOP 09B | `reports/execution.json`, `reports/economic.json` |
| Bloc 9 - Scellement PRE_OOS | Geler code, config, donnees, registre, rapports Test et robustesse avant ouverture OOS. | SOP 10; SOP 12; DN-032, DN-038 | manifeste, hashes, approbation reviewer |
| Bloc 10 - Controle d'acces OOS | Ouvrir l'OOS une seule fois, avec autorisation et journalisation. | SOP 10 | `oos_access_log.jsonl`, preuve INV-002, INV-003 |
| Bloc 11 - Estimation OOS | Estimer passivement la serie OOS globale, complete et detrendee, sans reselection. | SOP 01; SOP 07; SOP 08 | `series/oos_primary_returns.json`, `reports/oos.json` |
| Bloc 12 - Gate economique separe | Evaluer NAV nette, couts, risque, capacite et executabilite sans remplacer le gate statistique. | Protocole sections 5, 7; SOP 08; SOP 09B | `reports/economic.json`, preuve INV-010 |
| Bloc 13 - Reproductibilite | Produire environnement, commandes, seeds, reviewers, hashes et paquet de validation. | SOP 12 | `reports/reproduction.json`, `manifests/reproducibility_manifest.json` |
| Bloc 14 - Incubation/live | Passer a paper/live seulement apres `VALIDATION_READY` puis `DEPLOYMENT_CERTIFIED`. | SOP 11; SOP 12 | preuves INV-014, INV-015, rapports monitoring |
| Bloc 15 - Cycle de vie | Journaliser incidents, suspensions, reprises, retraits et archivage. | SOP 11; SOP 12 | archive, incident log, retention policy |

Un backtester EBTA n'est donc pas seulement un moteur `data -> signals ->
performance`. C'est un moteur de recherche gouverne :

```text
intention -> donnees PIT -> folds -> candidates -> Train -> Test/WRC ->
robustesse -> execution tradable -> PRE_OOS_SEALED -> OOS -> gates ->
reproductibilite -> incubation/live -> archive
```

`Implementation/ebta_engine/` verifie que ces blocs laissent des preuves
coherentes, mais ne remplace pas la construction de ces blocs.

## Artefacts que le pipeline doit produire

Un pipeline EBTA doit produire au minimum un dossier de recherche conforme a ce
modele :

```text
research_package/
  config.json
  registry.jsonl
  oos_access_log.jsonl
  reports/
    gates.json
    wrc.json
    robustness.json
    oos.json
    economic.json
    execution.json
    reproduction.json
    invariant_evidence.json
  series/
    oos_primary_returns.json
  manifests/
    reproducibility_manifest.json
```

Ces noms sont le contrat actuel du runtime. Ils peuvent evoluer via version de
schema, mais pas par interpretation implicite du pipeline.

## Responsabilites pratiques par module

| Module pipeline | Responsabilite EBTA | Artefacts produits |
| --- | --- | --- |
| Preregistration | Collecter hypothese, univers, calendrier, folds, budgets, seeds, gates, execution, robustesse. | `config.json` |
| Data layer | Charger des donnees point-in-time et journaliser disponibilite, publication, ingestion. | `config.json`, `reports/gates.json`, preuves anti-leakage |
| Splitter Walk-Forward | Construire `Train_k`, `Test_k`, `OOS_k` non chevauchants avec purge/embargo. | config, evidence invariants |
| Research engine | Evaluer candidates, enregistrer runs, echecs, sorties. | `registry.jsonl` |
| Selection/Test | Appliquer selection locale et WRC avant OOS. | `reports/wrc.json`, `reports/gates.json` |
| Robustesse | Executer les stress-tests pre-OOS. | `reports/robustness.json` |
| Execution model | Simuler signaux, ordres, fills, couts, capacite, NAV. | `reports/execution.json`, `reports/economic.json` |
| OOS controller | Verrouiller le paquet, autoriser l'ouverture OOS, journaliser les acces. | `oos_access_log.jsonl`, manifeste |
| OOS estimator | Calculer la serie primaire et le rapport OOS. | `series/oos_primary_returns.json`, `reports/oos.json` |
| Reproducibility | Generer hashes, environnement, commandes, reviewers. | `manifests/reproducibility_manifest.json`, `reports/reproduction.json` |
| EBTA validator | Verifier schemas, gates, invariants, hashes. | rapport de validation runtime |

## Role de `Implementation/ebta_engine`

Le runtime EBTA actuel sert a quatre choses.

### 1. Definir les formats attendus

Les schemas dans `Implementation/ebta_engine/schemas/` disent quels champs
minimaux doivent exister pour :

- configuration ;
- registre d'experiences ;
- journal d'acces OOS ;
- manifeste de reproductibilite.

### 2. Construire et verifier les empreintes

`Implementation/ebta_engine/manifests/` calcule les SHA-256 des artefacts et
verifie qu'un fichier n'a pas change apres generation du manifeste.

### 3. Verifier les gates et invariants

`Implementation/ebta_engine/validators/` verifie :

- gates G0 a G14 ;
- invariants `INV-001` a `INV-016` ;
- schemas et JSONL ;
- paquet EBTA complet.

### 4. Encadrer les adaptateurs

`Implementation/ebta_engine/adapters/backtrader_mapping.py` montre la frontiere
attendue : un pipeline externe fournit des sorties non fiables, l'adaptateur les
mappe vers des artefacts EBTA, puis le noyau EBTA valide.

## Workflow de construction recommande

### Etape 1 - Lire les sources

1. Lire `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md`.
2. Lire `Protocole/PROTOCOLE EBTA.md`.
3. Lire `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md`.
4. Lire `Protocole/PAQUET D'EXECUTION EBTA.md`.
5. Lire `Implementation/ebta_engine/README.md`.
6. Lire `Implementation/TRACEABILITY_MATRIX.md`.

### Etape 2 - Construire les blocs de recherche avant l'optimisation

Avant d'optimiser une strategie, le pipeline doit savoir executer les blocs de
recherche EBTA dans le bon ordre :

- preregistration ;
- donnees point-in-time ;
- segmentation Walk-Forward ;
- registre candidates ;
- calibration Train ;
- selection et inference Test ;
- robustesse pre-OOS ;
- execution tradable ;
- scellement et controle OOS ;
- estimation OOS ;
- gates statistique/economique ;
- reproductibilite.

Chaque bloc doit ensuite produire les preuves correspondantes :

- une configuration preregistree ;
- un registre append-only ;
- un journal d'acces OOS ;
- des rapports de gates ;
- une serie OOS primaire ;
- un manifeste.

Si ces blocs n'existent pas, le pipeline n'est pas encore EBTA. Si les blocs
existent mais ne produisent pas les artefacts, le pipeline n'est pas encore
auditable.

### Etape 3 - Valider le paquet

Commande de quality gate :

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
```

Pour un paquet produit par un pipeline, utiliser le validateur de paquet :

```python
from pathlib import Path
from ebta_engine.validators.package_validator import validate_package_dir

report = validate_package_dir(Path("research_package"))
print(report["status"])
print(report["gate_report"])
print(report["invariant_results"])
```

Le pipeline est acceptable seulement si les erreurs sont corrigees ou documentees
comme `INCONCLUSIVE` avec preuve manquante explicite.

## Comment refondre un pipeline existant

Pour un pipeline existant, ne pas commencer par changer toute l'architecture.

Ordre recommande :

1. Identifier ses sorties actuelles : trades, fills, NAV, metrics, logs,
   configurations.
2. Mapper chaque sortie vers un artefact EBTA attendu.
3. Ajouter les artefacts manquants sans modifier encore la logique alpha.
4. Generer un paquet EBTA minimal.
5. Lancer les validateurs EBTA.
6. Corriger les erreurs contractuelles.
7. Seulement ensuite refondre les etapes internes qui violent les SOP.

## Mode d'intervention face a un repo

Quand une IA arrive dans un repo, elle doit d'abord identifier le cas de travail.

| Cas | Question directrice | Strategie |
| --- | --- | --- |
| Construire de zero | Aucun pipeline de recherche exploitable n'existe. | Creer les blocs EBTA dans l'ordre, puis les artefacts et tests. |
| Refondre / migrer | Un pipeline existe mais n'est pas EBTA ou n'est pas auditable. | Cartographier l'existant, ajouter les artefacts EBTA, puis corriger les blocs qui divergent. |
| Auditer et corriger | Un pipeline pretend deja suivre EBTA. | Verifier preuves, gates, invariants, ordre des blocs, puis corriger les ecarts. |

### Cas 1 - Construire de zero

Objectif : construire un pipeline EBTA natif.

Ordre de travail :

1. Creer le modele de paquet `research_package/`.
2. Implementer le bloc de preregistration et `config.json`.
3. Implementer la couche donnees point-in-time.
4. Implementer la segmentation Walk-Forward.
5. Implementer le registre append-only.
6. Implementer le moteur de candidates.
7. Implementer Train/Test/WRC.
8. Implementer robustesse pre-OOS.
9. Implementer execution tradable et gate economique.
10. Implementer scellement `PRE_OOS_SEALED` et journal OOS.
11. Implementer estimation OOS et series primaires.
12. Implementer manifestes, reproduction et validation EBTA.

Definition de fini :

- un paquet EBTA minimal est produit ;
- `validate_package_dir()` retourne `PASS` ;
- les tests du pipeline prouvent au moins un cas valide et des cas invalides
  critiques.

### Cas 2 - Refondre ou migrer un pipeline existant

Objectif : transformer un pipeline deja utile en producteur d'artefacts EBTA.

Ne pas commencer par reecrire les signaux ou la logique alpha. Commencer par
cartographier.

Audit initial :

| Element existant | Question EBTA |
| --- | --- |
| Config actuelle | Peut-elle devenir `config.json` preenregistre ? |
| Donnees | Sont-elles point-in-time avec timestamps de disponibilite ? |
| Splits | Correspondent-ils a `Train_k`, `Test_k`, `OOS_k` sans chevauchement ? |
| Optimisation | Est-elle limitee a Train/Test sans regarder OOS ? |
| Tests multiples | Le WRC local couvre-t-il la famille complete ? |
| Logs | Peuvent-ils alimenter `registry.jsonl` et `oos_access_log.jsonl` ? |
| Resultats | Produisent-ils serie primaire, NAV, couts, rapports et manifeste ? |

Ordre de migration :

1. Ajouter une couche de mapping vers les artefacts EBTA.
2. Produire un paquet EBTA avec les sorties actuelles.
3. Lancer `validate_package_dir()`.
4. Classer les ecarts :
   - `MISSING_ARTIFACT` ;
   - `INVALID_CONTRACT` ;
   - `PIPELINE_ORDER_VIOLATION` ;
   - `NORMATIVE_AMBIGUITY` ;
   - `OUT_OF_SCOPE_DEBT`.
5. Corriger d'abord les ecarts qui touchent l'ordre EBTA : OOS, WRC, registre,
   leakage, manifestes.
6. Garder les refontes de performance ou d'architecture interne pour apres la
   mise en conformite contractuelle.

Definition de fini :

- le pipeline existant produit un `research_package/` ;
- les violations EBTA sont corrigees ou marquees explicitement ;
- la dette externe ne fuit pas dans `Implementation/ebta_engine/`.

### Cas 3 - Auditer et corriger un pipeline qui se dit EBTA

Objectif : verifier que la conformite EBTA est reelle, pas declarative.

Procedure :

1. Localiser le paquet ou les sorties de recherche.
2. Verifier la presence des blocs de recherche, pas seulement des fichiers.
3. Verifier les artefacts avec les schemas.
4. Verifier les gates G0 a G14.
5. Verifier les invariants INV-001 a INV-016.
6. Verifier les hashes et la reproductibilite.
7. Verifier que l'OOS n'a pas ete consulte avant scellement.
8. Verifier que les echecs, runs perdants et candidates influentes sont
   conserves.
9. Produire un rapport d'audit classe par severite.
10. Corriger uniquement les ecarts qui ne changent pas la norme.

Classification des constats :

| Severite | Sens |
| --- | --- |
| BLOCKER | Violation d'ordre EBTA, OOS contamine, WRC manquant, registre non opposable, leakage. |
| MAJOR | Preuve manquante pour gate ou invariant, hash absent, rapport incomplet. |
| MINOR | Convention de nommage, documentation runtime, ergonomie du paquet. |
| NORMATIVE_QUESTION | Le code exige une regle absente ou ambigue dans `Protocole/`. |

Definition de fini :

- chaque constat a une preuve ;
- chaque correction est testee ;
- aucune correction ne modifie implicitement le protocole ;
- les tests EBTA et les tests du pipeline passent.

## Cle de decision pour une IA

Avant de coder, choisir une seule route :

```text
Si aucun pipeline exploitable -> construire de zero.
Si pipeline utile mais non EBTA -> refondre/migrer.
Si pipeline pretend etre EBTA -> auditer/corriger.
```

Si le repo contient un pipeline externe comme BACKTRADER, l'IA doit d'abord lire
sa gouvernance locale, puis travailler par adaptateur. Elle ne doit pas deplacer
les conventions du repo externe dans le noyau EBTA.

## Questions qu'une IA doit se poser en construisant le pipeline

- Quelle SOP possede cette regle ?
- Quel DN-ID justifie ce comportement ?
- Quel artefact prouve cette decision ?
- Ce champ est-il une norme ou un parametre configurable ?
- L'OOS est-il ouvert seulement apres `PRE_OOS_SEALED` ?
- Le WRC local `PASS` precede-t-il l'ouverture OOS ?
- Le gate economique est-il separe du gate statistique ?
- Le manifeste peut-il detecter une modification apres coup ?
- Les erreurs sont-elles contractuelles et explicites ?

## Prompt de depart pour une IA

```text
Construis ou refonds un pipeline de recherche EBTA.

Sources obligatoires :
- Protocole/0-README - Comprendre et maintenir le protocole EBTA.md
- Protocole/PROTOCOLE EBTA.md
- Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md
- Protocole/PAQUET D'EXECUTION EBTA.md
- Implementation/ebta_engine/README.md
- Implementation/TRACEABILITY_MATRIX.md
- Implementation/GUIDE - Construire un pipeline de recherche EBTA.md

Regles :
- Protocole/ reste l'autorite normative.
- Implementation/ebta_engine/ definit les contrats executables.
- Le pipeline doit produire un dossier research_package conforme.
- Le pipeline doit passer les validations schemas, manifestes, gates et
  invariants.
- Ne pas inventer de statut, gate, seuil ou definition methodologique.
- Si une regle manque, bloquer ou marquer INCONCLUSIVE avec preuve manquante.

Livrable attendu :
- architecture du pipeline ;
- blocs de recherche EBTA et responsabilites ;
- mapping des modules vers artefacts EBTA ;
- generation des artefacts ;
- validation par package_validator ;
- tests automatises.
```

## Politique de migration de schema

Les fichiers `.ai/checkpoint.json`, `Implementation/Active/tracking.json` et les
schemas dans `Implementation/ebta_engine/schemas/` portent tous un champ
`schema_version`. Ce champ suit le versioning semantique `MAJEUR.MINEUR.PATCH`.

### Convention de versioning

| Type de changement | Impact sur version | Exemple |
| --- | --- | --- |
| Champ obligatoire ajoute ou supprime | MAJEUR (cassant) | `1.0.0` → `2.0.0` |
| Champ optionnel ajoute | MINEUR (compatible) | `1.0.0` → `1.1.0` |
| Renommage de champ | MAJEUR (cassant) | `1.0.0` → `2.0.0` |
| Correction de valeur enum | MAJEUR si suppressif, MINEUR si additif | selon cas |
| Correction documentaire pure | PATCH | `1.0.0` → `1.0.1` |

### Regles de compatibilite pour une IA reprenant le relais

1. **Version identique** : reprise normale.
2. **MINEUR superieur** : l'IA peut lire le fichier ; les champs optionnels
   inconnus sont ignores.
3. **MAJEUR superieur** : l'IA **doit refuser de demarrer** et alerter
   l'utilisateur. Elle ne doit jamais silencieusement ignorer un schema
   incompatible.

### Procedure de migration

Lorsqu'un changement de schema est necessaire :

1. Classifier le changement (voir tableau ci-dessus).
2. Si le changement est `NORMATIVE_CHANGE_REQUIRED`, bloquer et ouvrir une
   procedure documentaire dans `Protocole/` avant de coder.
3. Incrementer `schema_version` dans le fichier schema concerne.
4. Migrer le fichier live correspondant (checkpoint, tracking, artefact) par
   overwrite — jamais silencieusement.
5. Journaliser la migration dans
   `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` avec :
   - la version avant/apres ;
   - les champs impactes ;
   - la justification normative.
6. Relancer la suite de validation complete.

### Responsabilite

L'IA qui effectue le changement de schema est responsable de la migration du
fichier live. Cette migration ne peut pas etre deleguee a l'utilisateur sans
notification explicite.

---

## Prochaine etape pratique

La prochaine etape n'est pas de modifier le protocole.

La prochaine etape est de choisir une cible :

1. creer un pipeline pilote minimal dans ce repo pour produire un vrai
   `research_package` ;
2. ou ouvrir le repo BACKTRADER, lire sa gouvernance, puis construire un
   adaptateur qui transforme ses sorties en artefacts EBTA.

Dans les deux cas, `Implementation/ebta_engine/` doit rester le banc de controle.
