# Checkpoint runtime EBTA - 2026-06-26

## Statut

| Champ | Valeur |
| --- | --- |
| Etape | STEP_1_CHECKPOINT |
| Statut | GO |
| Type | GOVERNANCE |
| Runtime | EBTA-ENGINE-0.1.0 |
| Impact protocole | NONE |
| Hook | `Implementation/HOOK - Plan actif stabilisation archive et pipeline pilote.md` |
| Suivi JSON | `Implementation/task_tracking.json` |

## Synthese

Le lot runtime courant est coherent avec le plan actif apres execution de
l'etape 0 et de l'etape 1.

Decision : `GO` pour passer ensuite a `STEP_2_LOCAL_PILOT_PIPELINE`.

## Etape 0 - Archivage controle

Resultat :

- `Applications/` a ete archive vers `Archives/Applications_2026-06-26/`.
- `Notes/` reste actif car cite par plusieurs SOP.
- `Protocole/Archives/` reste l'archive documentaire officielle du protocole.
- les hooks/plans/contextes termines ont ete archives sous
  `Implementation/Archives/completed_2026-06-26/` apres correction des
  pointeurs actifs.
- Les caches Python `__pycache__` ne sont pas archives car ils sont generes et
  recreables.

Preuve :

- `Applications/` absent de la racine apres deplacement.
- `Archives/Applications_2026-06-26/` present avec 69 fichiers.
- References actives restantes a `Applications` limitees a `.gitignore`,
  `Archives/README.md` et `Implementation/ARCHIVE_INVENTORY_2026-06-26.md`.
- `Implementation/HOOK - Reprise EBTA Engine Core autonome.md`,
  `Implementation/PLAN - Procedures de calcul EBTA et optimisation ML.md` et
  `Implementation/implementation_context.json` ont ete deplaces dans
  `Implementation/Archives/completed_2026-06-26/`.

## Etape 1 - Checkpoint du lot actuel

### Audit du diff

Le working tree contient le socle runtime EBTA deja ajoute dans `Implementation/`,
des clarifications documentaires deja presentes dans `Protocole/`, et les
artefacts ajoutes pour ce lot :

- `Archives/README.md` ;
- `Implementation/ARCHIVE_INVENTORY_2026-06-26.md` ;
- `Implementation/CHECKPOINT_2026-06-26.md` ;
- `Implementation/HOOK - Plan actif stabilisation archive et pipeline pilote.md` ;
- `Implementation/task_tracking.json` ;
- mise a jour de `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`.

### Anti-divergence Protocole -> Implementation

Controle effectue :

- recherche des marqueurs de changement normatif (`NORMATIVE_CHANGE_REQUIRED`,
  nouveau gate, nouveau statut, nouveau seuil, nouvelle definition) ;
- lecture du hook actif et de l'historique runtime ;
- verification que les nouvelles decisions sont classees `GOVERNANCE` avec
  `Impact protocole: NONE`.

Conclusion :

- aucune nouvelle regle EBTA n'est creee ;
- aucun gate, statut, seuil ou ordre de gate n'est modifie ;
- l'archivage concerne une source historique non normative et ignoree par Git ;
- `Implementation/` reste subordonne a `Protocole/`.

## Validations

| Commande | Resultat |
| --- | --- |
| `python -m json.tool Implementation\task_tracking.json` | PASS |
| `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` | PASS - 50 tests |
| `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` | PASS - package status PASS |
| `git diff --check -- Implementation Protocole Archives .gitignore` | PASS |

## Risques residuels

| Risque | Statut | Traitement |
| --- | --- | --- |
| Archiver une source active | CLOSED | `Notes/` conserve, `Applications/` non reference hors traces d'archive. |
| Archiver un hook/plan/json termine | CLOSED | Hook de reprise, plan procedures et contexte JSON deplaces apres correction des pointeurs actifs. |
| Ajouter une norme EBTA par le runtime | OPEN pour les lots futurs | Bloquer comme `NORMATIVE_CLARIFICATION_REQUIRED` si cela apparait. |
| Importer la dette BACKTRADER | OPEN pour etape 3 | Lire la gouvernance BACKTRADER avant toute integration. |

## Decision

`STEP_0_ARCHIVE_OBSOLETE` et `STEP_1_CHECKPOINT` sont terminees.

Le prochain lot peut demarrer sur `STEP_2_LOCAL_PILOT_PIPELINE`.
