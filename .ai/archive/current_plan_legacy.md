# Plan courant multi-IA EBTA

## Role

Ce fichier porte la reprise humaine courte.
L'etat machine verifiable est dans `.ai/checkpoint.json`, valide par
`.ai/checkpoint.schema.json`.

Ne pas creer de variantes datees, checkpoints dates ou copies concurrentes.

## Etat courant

| Champ | Valeur |
| --- | --- |
| Derniere mise a jour | 2026-06-30 |
| Statut global | ACTIF |
| Bootstrap IA officiel | `AGENTS.md` |
| Cockpit IA unique | `.ai/` |
| SAS humain | `.ai/sas_humain/` |
| Backlog mainline | `.ai/backlog/mainline/` |
| Backlog annexes | `.ai/backlog/annexes/` |
| Backlog fixes | `.ai/backlog/fixes/` |
| Schema checkpoint | `.ai/checkpoint.schema.json` |
| Cockpit micro actif | `Implementation/Active/HOOK.md` + `Implementation/Active/tracking.json` |
| Schema cockpit micro | `Implementation/Active/tracking.schema.json` |
| Autorite normative | `Protocole/` gele en `EBTA-DOC-1.0` |
| Runtime actif | `Implementation/` / `EBTA-ENGINE-0.1.0` |
| Etape runtime courante | `STEP_3_BACKTRADER_INTEGRATION` |

## Modele de gouvernance IA

`.ai/` est le seul cockpit d'etat IA du projet.

- `sas_humain/` recoit les idees brutes et n'est jamais executable par defaut.
- `checkpoint.json` suit les chantiers macro et leurs cycles de vie.
- `Implementation/Active/` suit seulement le detail micro du runtime actif.
- `.agents/` peut rester comme outillage ou historique, mais n'est pas une
  source d'etat projet.

Cycle de vie des chantiers :

```text
INTAKE -> TRIAGED -> PLANNED -> ACTIVE -> BLOCKED/DONE/REJECTED/SUPERSEDED -> ARCHIVED
```

## Ordre de reprise

1. Lire `AGENTS.md`.
2. Lire `.ai/current_plan.md`.
3. Lire `.ai/checkpoint.json`.
4. Lire les chemins actifs declares dans `.ai/checkpoint.json`.
5. Lire `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md`
   si la tache touche au protocole, a la methode EBTA ou aux decisions
   normatives.
6. Lire la gouvernance BACKTRADER avant toute integration ou modification
   BACKTRADER.

## Chantiers suivis

| ID | Track | Lifecycle | Statut | Chemin |
| --- | --- | --- | --- | --- |
| `STEP_3_BACKTRADER_INTEGRATION` | mainline | TRIAGED | PENDING | `.ai/backlog/mainline/EPIC_reprise_et_integration_backtrader.md` |
| `EPIC_ARCHITECTURE_IA_RAG` | annexe | TRIAGED | PENDING | `.ai/backlog/annexes/EPIC_Proposition_Architecture_IA_RAG.md` |

## Prochaine action active

`STEP_3_BACKTRADER_INTEGRATION` reste pending.

Avant toute modification, lire la gouvernance BACKTRADER indiquee par
l'utilisateur :

- `D:\TRADING\ENTREPRISE\0 - Phase de lancement\Strategie de trading\0 - Backtest\BACKTRADER\.agents`
- `D:\TRADING\ENTREPRISE\0 - Phase de lancement\Strategie de trading\0 - Backtest\BACKTRADER\CLAUDE.md`

Ensuite seulement, comparer les sorties BACKTRADER disponibles au contrat local
`Implementation/EXTERNAL_ENGINE_PROCEDURE_MAPPING.md` et proposer un plan
d'adaptation.

## Risques actifs

| ID | Risque | Controle |
| --- | --- | --- |
| R1 | `.ai/` devient une source normative concurrente | `.ai/` ne porte que le relais et les chantiers macro ; `Protocole/` reste normatif |
| R2 | Le checkpoint redevient narratif ou stale | Validation contre `.ai/checkpoint.schema.json` |
| R3 | Le tracking runtime diverge de sa forme attendue | Validation contre `Implementation/Active/tracking.schema.json` |
| R4 | BACKTRADER est modifie trop tot | Gouvernance BACKTRADER obligatoire avant integration |
| R5 | `Implementation/` redefine le Protocole | Toute regle methodologique nouvelle bloque en `NORMATIVE_CHANGE_REQUIRED` |
| R6 | Le SAS humain devient executable | `.ai/sas_humain/` est intake-only ; activation uniquement via checkpoint |

## Validations standard

```powershell
python -m json.tool .ai\checkpoint.json
python -c "import json, jsonschema; jsonschema.validate(json.load(open('.ai/checkpoint.json', encoding='utf-8')), json.load(open('.ai/checkpoint.schema.json', encoding='utf-8')))"
python -m json.tool Implementation\Active\tracking.json
python -c "import json, jsonschema; jsonschema.validate(json.load(open('Implementation/Active/tracking.json', encoding='utf-8')), json.load(open('Implementation/Active/tracking.schema.json', encoding='utf-8')))"
git diff --check -- AGENTS.md .ai .codex\README.md Implementation\Active\INSTALL_GIT_HOOK.md Implementation\Active\tracking.schema.json
```

Pour un changement runtime significatif, ajouter :

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
python Implementation\examples\minimal_pilot_pipeline\build_research_package.py
```

## Historique

L'historique detaille ne doit pas etre recopie ici. Utiliser :

- `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` pour le runtime ;
- `Protocole/HISTORIQUE DES VERSIONS EBTA.md` pour le protocole ;
- `.ai/archive/` pour les anciens plans de relais.
