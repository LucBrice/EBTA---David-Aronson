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
| Derniere mise a jour | 2026-06-29T09:34:00+02:00 |
| Statut global | ACTIF - AMELIORATIONS_POST_AUDIT_COMPLETES |
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

## Plan operationnel propose

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

Les 4 ameliorations post-audit (P1-P4) sont completes et validees :

- P1 : 7 tests de rejet — 59 tests PASS ;
- P2 : hook pre-commit anti-stale + INSTALL_GIT_HOOK.md ;
- P3 : .codex/README.md ;
- P4 : politique de migration de schema dans le GUIDE.

Prochaine etape : reprendre `STEP_3_BACKTRADER_INTEGRATION` uniquement par
un audit de gouvernance BACKTRADER et un mapping, sans modification de
BACKTRADER ni du protocole EBTA.
