# HOOK - Reprise EBTA Engine Core autonome

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - PLAN_DE_REPRISE_IMPLEMENTATION |
| Date de creation | 2026-06-24 |
| Objectif | Construire un moteur EBTA autonome avant branchement a BACKTRADER ou a tout autre pipeline reel. |
| Autorite normative | `Protocole/` gele en `EBTA-DOC-1.0` |
| Fichier source principal | `Protocole/PAQUET D'EXECUTION EBTA.md` |
| Historique runtime | `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |
| Regle de gel | Ne pas modifier les documents geles du dossier `Protocole/` pour implementer le runtime. |

## Decision d'architecture

Le protocole EBTA doit devenir l'autorite contractuelle de la refonte du moteur
EBTA.

La refonte ne doit pas commencer par une integration directe dans BACKTRADER,
car cela melangerait :

- les regles normatives EBTA ;
- les contrats machine-readable a stabiliser ;
- la dette et les conventions existantes du repo BACKTRADER ;
- la future refonte de l'architecture BACKTRADER.

Decision retenue :

```text
Protocole EBTA gele
        |
        v
EBTA Engine Core autonome
        |
        v
Adapters
  - backtrader
  - notebook / research sandbox
  - futur moteur paper/live
```

BACKTRADER devra devenir un producteur et consommateur d'artefacts conformes au
moteur EBTA, pas le proprietaire de la logique EBTA.

## Objectif du moteur autonome

Construire un noyau executable qui transforme `EBTA-DOC-1.0` en contrats
verifiables :

- schemas JSON / JSONL ;
- taxonomie des statuts ;
- checklists de gates ;
- generation de manifestes ;
- verification de hashes ;
- validation des invariants `INV-001` a `INV-016` ;
- fixtures minimales valides et invalides ;
- tests automatises.

Le moteur autonome doit rester concret : il doit fonctionner sur des artefacts
de recherche EBTA realistes, meme minimaux. Il ne doit pas devenir une
specification abstraite sans donnees de test.

## Non-objectifs

- Ne pas refondre BACKTRADER pendant la phase 1.
- Ne pas modifier les SOP ou le protocole gele pour faciliter le code.
- Ne pas inventer de nouvelles regles methodologiques.
- Ne pas deplacer la source de verite normative hors de `Protocole/`.
- Ne pas brancher le runtime a des notebooks comme source de logique metier.

## Gouvernance des sources de verite

`Implementation/` est intimement lie a `Protocole/`, mais n'a pas la meme
autorite.

Hierarchie d'autorite :

| Rang | Source | Autorite |
| --- | --- | --- |
| 1 | `Protocole/MANIFESTE DE GEL EBTA.md` | Version documentaire active, hashes et statut du gel. |
| 2 | `Protocole/PROTOCOLE EBTA.md` | Carte generale, ordre des gates et interdictions principales. |
| 3 | `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md` | Source de verite decisionnelle : proprietaires, statuts, decisions, moments de preenregistrement. |
| 4 | SOP proprietaires | Autorite technique detaillee sur leur domaine. |
| 5 | `Protocole/PAQUET D'EXECUTION EBTA.md` | Cahier des charges operationnel pour schemas, journaux, manifestes et invariants. |
| 6 | `Implementation/` | Traduction executable et tests ; ne cree aucune regle normative. |
| 7 | Adaptateurs externes | Mapping entre un pipeline reel et les artefacts EBTA. |

Regle centrale :

```text
Si Implementation contredit Protocole, Implementation est faux.
Si Protocole est ambigu, Implementation bloque ou documente l'ambiguite.
Si un besoin d'Implementation exige une nouvelle regle, ouvrir une evolution
documentaire avant de coder cette regle comme norme.
```

## Historique evolutif de l'implementation

`Implementation/` est evolutif et doit avoir son propre journal.

Fichier officiel :

`Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`

Ce journal suit les changements du runtime :

- structure du dossier ;
- schemas ;
- validateurs ;
- fixtures ;
- tests ;
- generateurs de manifestes ;
- conventions de paquets ;
- decisions techniques ;
- mappings d'adaptateurs.

Il ne journalise pas les changements normatifs du protocole. Si un changement
runtime implique une modification normative, l'entree doit etre marquee
`NORMATIVE_CHANGE_REQUIRED` et le changement doit etre promu vers
`Protocole/HISTORIQUE DES VERSIONS EBTA.md` apres decision explicite.

Regle pratique :

- changement runtime pur : journaliser dans l'historique EBTA Engine ;
- clarification documentaire : journaliser dans l'historique EBTA Engine, puis
  ouvrir une note de clarification ;
- changement normatif : bloquer l'implementation et ouvrir le processus de
  version documentaire EBTA.

## Gouvernance de modification

Toute modification doit etre classee avant execution.

| Type | Exemple | Autorise dans `Implementation/` ? | Impact documentaire |
| --- | --- | --- | --- |
| `IMPLEMENTATION_DETAIL` | Nom de module, fonction utilitaire, format d'erreur, organisation interne. | Oui. | Aucun si la norme est respectee. |
| `CONTRACT_ENCODING` | Encodage JSON d'un champ deja defini dans le paquet d'execution. | Oui. | Doit citer la source normative. |
| `TEST_FIXTURE` | Exemple valide ou invalide pour un invariant. | Oui. | Aucun, sauf si la fixture revele une ambiguite. |
| `DOCUMENTATION_CLARIFICATION_NEEDED` | Champ minimal defini mais type exact non precise. | Oui seulement avec note d'ecart. | A remonter dans une note d'impact. |
| `NORMATIVE_CHANGE_REQUIRED` | Nouveau statut, nouveau gate, seuil modifie, ordre de gate change. | Non. | Nouvelle version documentaire obligatoire. |
| `ADAPTER_MAPPING` | Mapping BACKTRADER vers artefacts EBTA. | Oui apres noyau stable. | Aucun si le contrat EBTA ne change pas. |

Avant chaque changement significatif, produire une courte analyse :

```text
Change type:
Normative source:
Files touched:
Expected impact:
No-divergence check:
Verification command:
```

Toute modification acceptee du runtime doit ensuite etre journalisee dans
`Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`, sauf micro-correction
locale sans effet sur contrat, comportement, structure ou gouvernance.

## Regle anti-divergence

`Implementation/` ne doit jamais dupliquer une decision normative sans pointeur
vers sa source.

Chaque schema, validateur ou invariant doit inclure, dans son fichier ou sa
documentation voisine :

- l'ID ou la section normative source ;
- la SOP proprietaire si applicable ;
- le type de traduction (`CONTRACT_ENCODING`, `INVARIANT_CHECK`,
  `MANIFEST_CHECK`, `GATE_CHECK`) ;
- le comportement en cas d'information manquante.

Exemples :

| Artefact runtime | Source minimale obligatoire |
| --- | --- |
| `config.schema.json` | `PAQUET D'EXECUTION EBTA.md` section 3.1 + template de configuration. |
| `experiment_registry_event.schema.json` | `PAQUET D'EXECUTION EBTA.md` section 3.2 + SOP 03. |
| `oos_access_event.schema.json` | `PAQUET D'EXECUTION EBTA.md` section 3.3 + SOP 10. |
| `reproducibility_manifest.schema.json` | `PAQUET D'EXECUTION EBTA.md` section 5 + SOP 12. |
| `invariant_validator.py` | `PAQUET D'EXECUTION EBTA.md` section 6 + SOP proprietaire par invariant. |

Si une regle doit etre reprise dans le code, preferer une constante nommee avec
un commentaire source plutot qu'une valeur dispersee.

## Matrice d'impact obligatoire

Avant de modifier un artefact runtime partage, verifier les impacts suivants :

| Modification | Impacts a verifier |
| --- | --- |
| Schema de configuration | Fixtures, validateurs de config, format de paquet, manifestes, futurs adaptateurs. |
| Schema du registre JSONL | Append-only chain, invariants candidates, manifestes, adaptateurs de recherche. |
| Schema du journal OOS | Invariants OOS, gate d'ouverture, post-mortem, manifestes SOP 10 / SOP 12. |
| Taxonomie de statuts runtime | Rapports de gate, invariants, mapping BACKTRADER, compatibilite avec le registre normatif. |
| Validateur d'invariants | Fixtures invalides, rapports, mapping `INV-* -> SOP`, niveau `FAIL` / `INCONCLUSIVE`. |
| Generateur de manifeste | Tous les chemins de paquets, hashes, tests de reproductibilite, integration future. |
| Adapter BACKTRADER | Contrat EBTA, gouvernance BACKTRADER, risques de duplication de sources de verite. |

Une modification runtime qui change le sens d'un statut, d'un gate, d'un
invariant ou d'une preuve attendue est presumee normative jusqu'a preuve du
contraire.

## Notes d'ecart et decisions d'implementation

Creer un dossier dedie si necessaire :

```text
Implementation/decisions/
  YYYY-MM-DD-<slug>.md
```

Utiliser ce format :

```text
# Decision d'implementation - <titre>

Date:
Type:
Source normative:
Contexte:
Decision:
Impact:
Verification:
Statut: ACCEPTED | SUPERSEDED | BLOCKED_NORMATIVE
```

Ces notes ne remplacent pas `HISTORIQUE DES VERSIONS EBTA.md`.

- Si la decision est purement technique, elle reste dans `Implementation/`.
- Si elle modifie ou clarifie une norme, elle doit etre promue vers le processus
  documentaire officiel.
- Si elle contredit `Protocole/`, elle est invalide.

## Procedure de promotion vers le protocole

Si le runtime revele un besoin documentaire :

1. classer le point comme `DOCUMENTATION_CLARIFICATION_NEEDED` ou
   `NORMATIVE_CHANGE_REQUIRED` ;
2. identifier les SOP proprietaires avec le registre normatif ;
3. consulter la matrice de coherence ;
4. evaluer les impacts sur protocole principal, registre, paquet d'execution,
   template, historique et manifeste ;
5. ne modifier `Protocole/` qu'apres decision explicite d'ouvrir une nouvelle
   version documentaire ou une correction documentaire controlee ;
6. recalculer les hashes concernes si un document gele change.

Le runtime ne doit jamais normaliser silencieusement une ambiguite
methodologique.

## Sources normatives a lire au debut d'une session

1. `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md`
2. `Protocole/MANIFESTE DE GEL EBTA.md`
3. `Protocole/PAQUET D'EXECUTION EBTA.md`
4. `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md`
5. SOP proprietaires selon le module traite.

## Structure cible proposee

```text
Implementation/
  HOOK - Reprise EBTA Engine Core autonome.md
  HISTORIQUE DES VERSIONS EBTA ENGINE.md
  ebta_engine/
    schemas/
      config.schema.json
      experiment_registry_event.schema.json
      oos_access_event.schema.json
      reproducibility_manifest.schema.json
    validators/
      config_validator.py
      registry_validator.py
      oos_access_validator.py
      manifest_validator.py
      invariant_validator.py
    manifests/
      manifest_builder.py
      hash_utils.py
    fixtures/
      valid_minimal/
      invalid_invariants/
    tests/
      test_schemas.py
      test_manifest_hashes.py
      test_invariants.py
    README.md
```

Cette structure peut etre ajustee selon le langage retenu, mais les frontieres
doivent rester stables :

- `schemas/` decrit les artefacts attendus ;
- `validators/` applique les contrats ;
- `manifests/` construit et verifie les empreintes ;
- `fixtures/` fournit des cas executables ;
- `tests/` prouve que les invariants sont verifiables.

## Plan de travail

## Avancement runtime

| Phase | Statut | Preuve runtime | Tests de non-divergence |
| --- | --- | --- | --- |
| Phase 0 - Cadrage du runtime | DONE | `Implementation/ebta_engine/README.md`, `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` |
| Phase 0bis - Maintenabilite | DONE | `Implementation/TRACEABILITY_MATRIX.md`, `Implementation/ebta_engine/migrations/README.md`, `Implementation/ebta_engine/persistence.py` | `test_traceability.py`, `test_protocol_manifest_hashes.py` |
| Phase 1 - Schemas machine-readable | DONE | `Implementation/ebta_engine/schemas/`, fixtures valides et invalides | `test_schemas.py` |
| Phase 2 - Manifeste et hashes | DONE | `Implementation/ebta_engine/manifests/`, manifeste de package fixture | `test_manifest_hashes.py`, `test_package_validator.py` |
| Phase 3 - Invariants EBTA | DONE | `Implementation/ebta_engine/validators/invariant_validator.py`, `fixtures/invalid_invariants/all_invalid_cases.json` | `test_invariants.py` |
| Phase 4 - Gates et rapports | DONE | `Implementation/ebta_engine/validators/gate_validator.py`, `fixtures/valid_minimal/reports/gates.json` | `test_gates.py`, `test_package_validator.py` |
| Phase 5 - Format de paquet EBTA | DONE | `fixtures/valid_minimal/` avec config, registres, rapports, series, manifeste genere en test | `test_package_validator.py` |
| Phase 6 - Adapter BACKTRADER | LOCAL_CONTRACT_DONE_BACKTRADER_REPO_UNTOUCHED | `Implementation/ebta_engine/adapters/backtrader_mapping.py` mappe un payload externe vers des artefacts EBTA sans lire/ecrire le repo BACKTRADER | `test_backtrader_adapter.py` |

Regle d'execution actuelle : le repo BACKTRADER n'est pas modifie dans cette
iteration. La Phase 6 est donc limitee au contrat local d'adaptateur et aux
erreurs contractuelles explicites; le branchement reel sera une phase separee
apres validation du noyau autonome et lecture de la gouvernance BACKTRADER.

### Phase 0 - Cadrage du runtime

Objectif : figer la frontiere entre protocole, runtime et adaptateurs.

Livrables :

- README technique du runtime ;
- choix du langage et des dependances minimales ;
- convention de version du runtime ;
- convention de chemins des artefacts EBTA ;
- definition du format d'un dossier de recherche EBTA minimal.
- gouvernance runtime : sources de verite, classification des changements,
  matrice d'impact et procedure anti-divergence.
- historique runtime : journaliser les changements evolutifs de
  `Implementation/` sans concurrencer l'historique du protocole.

Critere de sortie :

- une session future peut comprendre ou placer les schemas, fixtures et tests
  sans relire tout l'historique de discussion.
- une session future sait distinguer une decision d'implementation d'un
  changement normatif.

### Phase 0bis - Maintenabilite du runtime

Objectif : fermer les angles morts de maintenabilite avant de coder les schemas,
validateurs, manifestes et adaptateurs.

Cette phase doit garantir que le runtime EBTA restera evolutif sans creer de
source de verite concurrente, sans casser les artefacts existants et sans
importer la dette d'un pipeline externe.

Livrables :

- politique de version et de compatibilite du runtime ;
- strategie de migration des schemas ;
- quality gate obligatoire pour toute modification de `Implementation/` ;
- matrice de tracabilite runtime vers sources normatives ;
- modele de persistance des artefacts EBTA ;
- frontiere de confiance des adaptateurs.

#### 0bis.1 - Politique de version et compatibilite

Definir une table de compatibilite :

```text
EBTA-DOC version -> EBTA-ENGINE version -> schema versions -> supported package stages
```

Regles minimales :

- `EBTA-DOC-*` reste la version normative.
- `EBTA-ENGINE-*` versionne uniquement le runtime.
- Chaque schema machine-readable possede un `schema_version`.
- Une evolution backward-compatible incremente une version mineure.
- Une evolution cassante exige une version majeure ou une migration explicite.
- Un runtime ne doit pas valider silencieusement un paquet cree pour une version
  non supportee.

#### 0bis.2 - Strategie de migration des schemas

Creer une strategie avant le premier schema stable :

```text
Implementation/ebta_engine/migrations/
```

Regles minimales :

- tout artefact persistant porte sa version de schema ;
- les migrations sont deterministes, testees et journalisees ;
- les migrations ne changent pas la signification normative d'un champ ;
- toute perte d'information est bloquante sauf decision explicite ;
- les tests doivent verifier la lecture d'artefacts d'anciennes versions
  supportees.

#### 0bis.3 - Quality gate obligatoire

Definir une commande ou sequence minimale avant toute modification acceptee du
runtime.

Gate minimale attendue :

- validation des schemas ;
- validation des fixtures valides et invalides ;
- tests du generateur de manifeste et des hashes ;
- tests des invariants disponibles ;
- verification de la matrice de tracabilite ;
- verification que l'historique runtime a ete mis a jour si necessaire.

Tant que l'outillage n'existe pas, documenter la verification manuelle
equivalente dans l'entree d'historique.

#### 0bis.4 - Matrice de tracabilite

Creer un artefact de tracabilite avant la croissance du code :

```text
Implementation/TRACEABILITY_MATRIX.md
```

La matrice doit relier :

- artefact runtime ;
- source normative exacte ;
- SOP proprietaire ou DN-ID si applicable ;
- type de traduction ;
- tests couvrant l'artefact ;
- statut de couverture.

Objectif : pouvoir detecter rapidement un contrat code sans source normative,
ou une decision normative sans couverture runtime.

#### 0bis.5 - Modele de persistance

Definir les regles de persistance avant les registres JSONL reels.

Points obligatoires :

- append-only physique pour les journaux critiques ;
- ecriture atomique ou strategie de fichier temporaire puis remplacement ;
- comportement en cas de crash partiel ;
- idempotence des operations de validation ;
- verrouillage ou prevention des ecritures concurrentes ;
- backup et restauration minimale ;
- separation entre artefacts sources, artefacts generes et rapports.

Tout choix de base de donnees future doit rester subordonne au contrat EBTA. La
base de donnees ne devient pas source normative.

#### 0bis.6 - Frontiere de confiance des adaptateurs

Definir la frontiere de confiance avant tout adapter, notamment BACKTRADER.

Regles minimales :

- un adapter lit des sorties externes comme donnees non fiables ;
- un adapter transforme vers les artefacts EBTA sans changer la norme ;
- les chemins lus/ecrits sont explicites et auditables ;
- les erreurs de mapping sont contractuelles, pas corrigees silencieusement ;
- les commandes ou processus externes doivent etre journalisables ;
- les conventions du pipeline externe ne doivent pas etre importees dans le
  noyau EBTA.

Critere de sortie :

- les six decisions de maintenabilite ci-dessus sont documentees dans le README
  technique du runtime ou dans des artefacts dedies ;
- l'historique runtime contient l'entree de gouvernance correspondante ;
- aucune ligne de code de validation normative n'est ecrite avant cette phase.

### Phase 1 - Schemas machine-readable

Objectif : encoder les schemas minimaux definis par le paquet d'execution.

Livrables :

- schema JSON de configuration ;
- schema JSONL du registre append-only ;
- schema JSONL du journal d'acces OOS ;
- schema JSON du manifeste de reproductibilite ;
- fixtures valides minimales ;
- fixtures invalides par champ manquant ou mauvais type.

Sources principales :

- `PAQUET D'EXECUTION EBTA.md`, section 3 ;
- `TEMPLATE - Configuration préenregistrée d'une recherche EBTA.md` ;
- SOP 03, SOP 10, SOP 12.

Critere de sortie :

- les schemas rejettent les artefacts structurellement invalides et acceptent un
  paquet EBTA minimal valide.

### Phase 2 - Manifeste et hashes

Objectif : produire et verifier un manifeste de paquet EBTA.

Livrables :

- calcul SHA-256 des artefacts ;
- manifeste reproductible ;
- verification des chemins et hashes ;
- test de detection d'un fichier modifie apres generation.

Sources principales :

- `MANIFESTE DE GEL EBTA.md` pour le principe ;
- SOP 12 pour les paquets `PRE_OOS_SEALED`, `VALIDATION_READY`,
  `DEPLOYMENT_CERTIFIED`, `LIFECYCLE_ARCHIVED`.

Critere de sortie :

- modifier un artefact fixture apres generation du manifeste provoque un echec
  explicite.

### Phase 3 - Invariants EBTA

Objectif : rendre executables les invariants `INV-001` a `INV-016`.

Livrables :

- moteur de validation d'invariants ;
- table de mapping `INV-* -> SOP proprietaire -> artefacts requis` ;
- fixtures invalides par invariant ;
- rapport de validation lisible.

Sources principales :

- `PAQUET D'EXECUTION EBTA.md`, section 6 ;
- registre normatif ;
- SOP 01, 02, 03, 04, 05, 09A, 10, 11, 12 selon l'invariant.

Critere de sortie :

- chaque invariant possede au moins un test positif et un test negatif, ou une
  note `DEFERRED_REQUIRES_PIPELINE_DATA` si l'invariant ne peut pas etre teste
  sans artefact de pipeline concret.

### Phase 4 - Gates et rapports

Objectif : transformer les checklists G0 a G14 en controles executables ou
semi-executables.

Livrables :

- modele de rapport de gate ;
- validation des preuves minimales par gate ;
- separation entre `PASS`, `FAIL`, `INCONCLUSIVE`, `NOT_VALIDATED`,
  `REJECTED_ECONOMIC` et statuts locaux ;
- exemples de rapports de gate.

Sources principales :

- `PAQUET D'EXECUTION EBTA.md`, section 2 et section 4 ;
- `REGISTRE DES DECISIONS NORMATIVES EBTA.md`.

Critere de sortie :

- un paquet fixture peut recevoir un rapport de validation par gate avec les
  manques identifies.

### Phase 5 - Format de paquet de recherche EBTA

Objectif : stabiliser la structure d'un dossier de recherche EBTA avant
integration a BACKTRADER.

Livrables :

- arborescence standard d'un paquet `PRE_OOS_SEALED` minimal ;
- arborescence standard d'un paquet `VALIDATION_READY` minimal ;
- conventions de noms pour configurations, registres, journaux, rapports et
  series ;
- fixture complete de recherche factice.

Critere de sortie :

- le runtime peut valider un dossier EBTA minimal de bout en bout sans
  BACKTRADER.

### Phase 6 - Adapter BACKTRADER

Objectif : brancher BACKTRADER seulement apres stabilisation du noyau EBTA.

Livrables :

- mapping `BACKTRADER outputs -> EBTA artifacts` ;
- adaptateur de lecture/ecriture ;
- gates EBTA dans le pipeline BACKTRADER ;
- strategie de migration des conventions redondantes ;
- tests d'integration.

Regle :

- lire d'abord la gouvernance BACKTRADER actuelle avant toute modification du
  repo BACKTRADER.
- ne pas importer la dette BACKTRADER dans le contrat EBTA.

Critere de sortie :

- BACKTRADER produit des artefacts conformes au runtime EBTA ou echoue avec des
  erreurs contractuelles explicites.

## Lot suivant recommande

Le lot initial Phase 0 -> Phase 5 est clos localement pour
`EBTA-ENGINE-0.1.0`. La Phase 6 est close uniquement au niveau du contrat local :
l'adaptateur BACKTRADER sait mapper un payload externe vers des artefacts EBTA,
mais le repo BACKTRADER n'a pas ete lu ni modifie.

La prochaine decision de travail doit donc choisir une cible concrete :

1. creer un pipeline pilote minimal dans ce repo qui produit un vrai
   `research_package/` valide par `validate_package_dir()` ;
2. ou ouvrir le repo BACKTRADER, lire sa gouvernance locale, puis brancher
   l'adaptateur comme producteur/consommateur d'artefacts EBTA conformes.

Dans les deux cas, la definition de fini reste :

- aucun changement dans `Protocole/` ;
- un paquet EBTA produit ou mappe depuis une sortie de pipeline ;
- validation par `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` ;
- journalisation dans `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`.

## Politique de modification documentaire

Les documents de `Protocole/` sont geles.

Si l'implementation revele une ambiguite :

1. ne pas corriger directement le protocole ;
2. creer une note d'implementation dans `Implementation/`;
3. classer l'ambiguite :
   - `IMPLEMENTATION_DETAIL` ;
   - `DOCUMENTATION_CLARIFICATION_NEEDED` ;
   - `NORMATIVE_CHANGE_REQUIRED`.
4. ouvrir une nouvelle version documentaire uniquement si une decision
   normative doit changer.

## Etat de reprise

Etat courant verifie :

- `EBTA-DOC-1.0` est gele ;
- `EBTA-ENGINE-0.1.0` existe comme noyau autonome Python standard-library first ;
- les schemas, fixtures, validateurs, manifestes, invariants, gates, persistance
  et tests de non-divergence existent dans `Implementation/ebta_engine/` ;
- `Implementation/TRACEABILITY_MATRIX.md` relie les artefacts runtime a leurs
  sources normatives et tests ;
- la decision d'architecture reste : runtime autonome d'abord, adaptateurs
  ensuite ;
- l'adaptateur BACKTRADER est seulement un contrat local
  `LOCAL_CONTRACT_DONE_BACKTRADER_REPO_UNTOUCHED`.

Prochaine action concrete :

```text
Choisir la cible suivante : pipeline pilote minimal dans ce repo, ou integration
BACKTRADER apres lecture de sa gouvernance locale.

Ne pas recommencer Phase 0 / Phase 0bis : elles sont terminees.
Ne pas modifier Protocole/ pour brancher un pipeline.
Utiliser Implementation/ebta_engine comme banc de controle et journaliser le lot
dans l'historique EBTA Engine.
```
