# Plan courant multi-IA EBTA

## Role de ce fichier

Ce fichier est la source unique de verite humaine et conceptuelle pour la
reprise multi-IA dans ce repo.

Regle stricte : ne pas creer de variantes datees ou versionnees. Toute IA doit
lire puis ecraser ce fichier et `.ai/checkpoint.json` quand une etape
importante est validee ou avant de quitter.

## Etat actuel

| Champ | Valeur |
| --- | --- |
| Derniere mise a jour | 2026-06-29 |
| Statut global | ACTIF - STRATEGIE_ACTIF_RUNTIME_VALIDEE |
| Autorite normative | `Protocole/` gele en `EBTA-DOC-1.0` |
| Runtime actif | `Implementation/` / `EBTA-ENGINE-0.1.0` |
| Hook runtime actif | Variable declaree dans `.ai/checkpoint.json` : `active_paths.active_hook_path` |
| Suivi runtime actif | Variable declaree dans `.ai/checkpoint.json` : `active_paths.active_tracking_path` |
| Chemins actifs courants | `Implementation/Active/HOOK.md` + `Implementation/Active/tracking.json` |
| SSoT de relais multi-IA | `.ai/current_plan.md` + `.ai/checkpoint.json` |
| Regle agent repo | `AGENTS.md` |

## Regles de reprise obligatoires

1. Lire d'abord `.ai/current_plan.md` et `.ai/checkpoint.json`.
2. Lire ensuite les chemins actifs declares dans `.ai/checkpoint.json`.
3. Traiter le hook et son JSON de suivi comme des variables operationnelles :
   ils peuvent changer a chaque nouveau lot d'implementation.
4. Pour toute action significative dans `Implementation/`, appliquer le Gardien EBTA :
   `Protocole/` reste normatif, `Implementation/` reste une traduction executable.
5. Ne pas modifier `BACKTRADER` avant lecture de sa gouvernance locale et sans
   demande explicite dans ce lot.
6. Ne pas creer d'autres fichiers de relais, plans dates, checkpoints dates ou
   copies concurrentes.
7. Avant une reponse finale, si l'etat du repo a change, mettre a jour
   `.ai/current_plan.md` et `.ai/checkpoint.json` par overwrite.

## Synthese de l'etat verifie

Le runtime EBTA local est avance jusqu'a `STEP_2_LOCAL_PILOT_PIPELINE`.
Le pipeline pilote local est considere termine dans `Implementation/Active/tracking.json`
et dans `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` :

- `STEP_0_ARCHIVE_OBSOLETE` : complet ;
- `STEP_1_CHECKPOINT` : complet ;
- `STEP_2_LOCAL_PILOT_PIPELINE` : complet ;
- prochaine etape declaree : `STEP_3_BACKTRADER_INTEGRATION`.

La prochaine etape ne doit pas demarrer par du code. Elle demarre par la lecture
des entrees de gouvernance BACKTRADER indiquees par l'utilisateur :

- `D:\TRADING\ENTREPRISE\0 - Phase de lancement\Strategie de trading\0 - Backtest\BACKTRADER\.agents`
- `D:\TRADING\ENTREPRISE\0 - Phase de lancement\Strategie de trading\0 - Backtest\BACKTRADER\CLAUDE.md`

## Objectif actif

Encoder dans `Implementation/` la clarification `strategie x actif` deja
validee dans `Protocole/`, puis revenir a la reprise BACKTRADER sans la
demarrer automatiquement.

Classification retenue : `CONTRACT_ENCODING`.

Regle de travail :

- ne pas modifier davantage `Protocole/` dans ce lot ;
- maintenir `Implementation/` comme derive executable, pas comme source de
  doctrine concurrente.

## Plan operationnel propose

### Phase E - Clarifier strategie x actif dans Protocole/

Statut : termine.

Objectif : rendre explicite, dans le protocole principal et les SOP
proprietaires, que l'actif devient un axe de selection statistique lorsque le
processus peut choisir le meilleur couple `strategie x actif`.

Taches :

- auditer `PROTOCOLE EBTA.md`, `SOP 03`, `SOP 08`, `SOP 09A`, le registre des
  decisions normatives et la matrice de coherence ;
- classer la demande entre clarification documentaire simple et changement
  normatif ;
- produire une proposition de patch ciblee sans l'appliquer tant que le `GO`
  n'est pas donne ;
- preciser les formulations attendues :
  - strategie multi-actifs fixe = candidate de portefeuille ;
  - strategie appliquee separement a plusieurs actifs avec selection du meilleur
    actif = une candidate par couple `strategie x actif` ;
  - `asset_universe` preenregistre et point-in-time ;
  - WRC sur la famille complete des couples evalues lorsque l'actif est
    selectionnable ;
  - serie primaire = serie quotidienne du portefeuille ou du couple tradable,
    jamais moyenne opportuniste de resultats par actif ;
- apres `GO`, appliquer les corrections documentaires, mettre a jour les
  references transversales requises, recalculer le manifeste si necessaire et
  executer les validations de non-divergence ;
- seulement ensuite, planifier le lot `Implementation/` pour encoder
  `asset_universe`, axe `asset`, fixtures multi-actifs et tests de rejet.

Livrables attendus avant `GO` :

- diagnostic court : clarification ou changement normatif ;
- liste exacte des fichiers et sections a modifier ;
- texte propose ou diff preview ;
- risques de coherence avec SOP 02, SOP 03, SOP 08, SOP 09A et le registre.

Definition de fini apres `GO` :

- `PROTOCOLE EBTA.md` explicite la place des couples `strategie x actif` dans
  la famille de candidates ;
- `SOP 03` rend la regle de comptage opposable ;
- `SOP 08` distingue couple tradable, portefeuille multi-actifs et agregations
  interdites ;
- `SOP 09A` relie explicitement `asset_universe` aux contraintes
  point-in-time ;
- registre/matrice/manifeste/historique sont mis a jour selon le classement ;
- `git diff --check -- Protocole .ai` passe.

Resultat valide :

- clarification appliquee dans `PROTOCOLE EBTA.md`, `SOP 03`, `SOP 08`,
  `SOP 09A`, `REGISTRE DES DECISIONS NORMATIVES EBTA.md` et
  `MATRICE DE COHERENCE DES SOP EBTA.md` ;
- entree ajoutee dans `HISTORIQUE DES VERSIONS EBTA.md` ;
- hashes affectes recalcules dans `MANIFESTE DE GEL EBTA.md` ;
- aucune modification `Implementation/` fonctionnelle ;
- validations : `git diff --check -- Protocole .ai` PASS,
  `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`
  PASS avec 59 tests.

### Phase F - Encoder strategie x actif dans Implementation/

Statut : termine.

Objectif : rendre executable la clarification documentaire : lorsque l'actif
est selectionnable, chaque couple `strategie x actif` est une candidate et la
WRC doit couvrir la famille complete des couples applicables.

Resultat valide :

- `search_space.py` expose `asset_universe`, `asset_selection_axis`,
  `asset_selection_rule`, `asset_candidate_count` et `candidate_asset_map` ;
- `candidate_matrix.py` valide le mapping candidat-actif et rejette un actif
  declare non couvert ;
- `invariant_validator.py` ajoute `INV-017` pour rejeter une WRC incomplete par
  couple `strategie x actif` ;
- `config.schema.json` et `pit_data_declaration.schema.json` acceptent les
  metadonnees d'univers d'actifs ;
- le pipeline pilote local passe a 8 candidates (`EURUSD`, `XAUUSD`) ;
- `test_minimal_pilot_pipeline.py` couvre le rejet si les candidates d'un actif
  evalue sont absentes de la WRC ;
- `TRACEABILITY_MATRIX.md`, `PROCEDURE_CALCULATION_MAP.md`,
  `HISTORIQUE DES VERSIONS EBTA ENGINE.md`, `Implementation/Active/HOOK.md` et
  `Implementation/Active/tracking.json` sont alignes.

Validations :

- `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`
  PASS avec 64 tests ;
- `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py`
  PASS, package `PASS` ;
- `python -m json.tool .ai\checkpoint.json` PASS ;
- `python -m json.tool Implementation\Active\tracking.json` PASS.
- `git diff --check -- Implementation Protocole .ai AGENTS.md .agents` PASS
  avec alertes CRLF uniquement sur les artefacts `research_package` generes.

### Phase A - Stabiliser le relais multi-IA

Statut : termine.

Objectif : rendre la reprise instantanee par une IA suivante sans ajouter de
bruit documentaire.

Taches :

- creer les deux fichiers SSoT `.ai/current_plan.md` et `.ai/checkpoint.json` ;
- inscrire les regles de lecture prioritaire et d'overwrite ;
- valider la syntaxe JSON du checkpoint ;
- relancer les validations EBTA de base apres creation.

Definition de fini :

- `python -m json.tool .ai\checkpoint.json` passe ;
- `python -m json.tool Implementation\Active\tracking.json` passe ;
- `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`
  passe avec 52 tests ;
- `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py`
  retourne `status: PASS` ;
- `git diff --check -- Implementation Protocole .ai` passe.

### Phase A2 - Inscrire la regle automatique de relais

Statut : termine.

Objectif : rendre la regle visible au demarrage de tout agent compatible avec
les instructions repo.

Decision :

- `AGENTS.md` est cree a la racine comme bootstrap court ;
- la regle impose la lecture prioritaire de `.ai/current_plan.md` et
  `.ai/checkpoint.json` ;
- la regle ne fige plus le hook actif ni son JSON de suivi ; elle demande de
  lire les chemins actifs declares dans `.ai/checkpoint.json` ;
- la regle impose la mise a jour des deux fichiers avant reponse finale si
  l'etat a change ;
- `AGENTS.md` ne duplique pas le plan runtime et ne remplace pas
  `Implementation/Active/tracking.json`.
- validation finale : `python -m json.tool .ai\checkpoint.json` passe et
  `git diff --check -- Implementation Protocole .ai AGENTS.md` passe.
- correction : les chemins de hook/tracking actifs sont des variables declarees
  dans `.ai/checkpoint.json`, pas des constantes inscrites en dur dans
  `AGENTS.md`.

### Phase B - Reprise de `STEP_3_BACKTRADER_INTEGRATION`

Statut : pending.

Objectif : preparer l'integration BACKTRADER sans importer sa dette ou ses
conventions comme norme EBTA.

Preconditions :

- Phase A terminee ;
- gouvernance BACKTRADER lue ;
- frontiere EBTA runtime -> adaptateur confirmee ;
- aucune modification dans le repo BACKTRADER sans demande explicite.

Taches :

- lire `.agents` et `CLAUDE.md` du repo BACKTRADER ;
- comparer ses sorties disponibles au contrat local
  `Implementation/EXTERNAL_ENGINE_PROCEDURE_MAPPING.md` ;
- lister les gaps de mapping ;
- proposer un plan d'adaptation avant toute modification.

### Phase C - Mise a jour continue du relais

Statut : permanent.

Regle : apres chaque validation importante, mettre a jour les deux fichiers
uniques :

- `.ai/current_plan.md` pour l'intention, les decisions, les prochaines etapes ;
- `.ai/checkpoint.json` pour l'etat machine, les commandes, les resultats, les
  fichiers touches et les risques.

### Phase D - Stabiliser le cockpit Implementation/Active

Statut : termine.

Decision :

- le hook actif est deplace vers `Implementation/Active/HOOK.md` ;
- le suivi JSON actif est deplace vers `Implementation/Active/tracking.json` ;
- `.ai/checkpoint.json` pointe vers ces deux chemins via `active_paths` ;
- `AGENTS.md` reste generique et ne fige pas un nom de hook particulier ;
- les documents de gouvernance runtime impactes sont corriges.

Validation :

- `python -m json.tool .ai\checkpoint.json` : PASS ;
- `python -m json.tool Implementation\Active\tracking.json` : PASS ;
- `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` : PASS, 52 tests ;
- `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` : PASS, package `PASS` ;
- `git diff --check -- Implementation Protocole .ai AGENTS.md .agents` : PASS ;
- aucune reference restante aux anciens chemins actifs du hook et du tracking.

## Risques actifs

| ID | Risque | Controle |
| --- | --- | --- |
| R1 | Creer une source de verite concurrente au protocole EBTA | Le plan `.ai` ne decrit que la reprise multi-IA et pointe vers `Protocole/` / `Implementation/` |
| R2 | Lancer BACKTRADER trop tot | Lecture gouvernance obligatoire avant integration |
| R3 | Se fier a un checkpoint stale | Relancer les validations avant modification runtime significative |
| R4 | Polluer le repo avec des plans multiples | Ecraser seulement `.ai/current_plan.md` et `.ai/checkpoint.json` |
| R5 | Schemas JSON non couverts en rejet laisseraient passer des données corrompues | 7 tests de rejet ajoutes (P1) — 59 tests PASS |

## Commandes de validation standard

```powershell
python -m json.tool .ai\checkpoint.json
python -m json.tool Implementation\Active\tracking.json
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
python Implementation\examples\minimal_pilot_pipeline\build_research_package.py
git diff --check -- Implementation Protocole .ai AGENTS.md
```

## Prochaine action recommandee

La Phase F est terminee. Prochaine action recommandee :
`STEP_3_BACKTRADER_INTEGRATION`.

Avant toute modification, lire la gouvernance BACKTRADER indiquee par
l'utilisateur :

- `D:\TRADING\ENTREPRISE\0 - Phase de lancement\Strategie de trading\0 - Backtest\BACKTRADER\.agents`
- `D:\TRADING\ENTREPRISE\0 - Phase de lancement\Strategie de trading\0 - Backtest\BACKTRADER\CLAUDE.md`

Ensuite seulement, comparer ses sorties disponibles au contrat local
`Implementation/EXTERNAL_ENGINE_PROCEDURE_MAPPING.md` et proposer un plan
d'adaptation.
