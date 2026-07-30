# Plan — index declaratif `POLICIES.md`

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Chantier existant ? | Aucun ; enfant 1/2 de `EPIC_PHASE_1_POLICIES_ET_PREUVE_SESSION`. |
| Verrou actif ? | Aucun ; Phase 0 `DONE` et parent route. |
| Decision humaine ? | Non, la boucle demande l'execution du palier documentaire. |
| Remplacement ? | Non. |

Test `epic-orchestrator` : **SINGLE**. L'index et son unique pointeur de
découvrabilité partagent un seul critère de sortie.

## Audit IA de promotion

- [x] Sources réelles relues.
- [x] Deux passes intake convergentes.
- [x] Liste d'actions minimale définie.
- [x] Vocabulaire `OUI` / `CONDITIONNELLE` / `NON` fermé.
- [x] Priorité des sources propriétaires explicitée.
- [x] Périmètre limité à deux fichiers.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `annexe` |
| Lifecycle | `TRIAGED` |
| Type de chantier | `SINGLE` |
| Scope | Créer `POLICIES.md` comme index déclaratif sourcé et ajouter son pointeur court dans `AGENTS.md`. |
| Non-goals | Ne créer aucune règle, autorisation, mécanique, dépendance ou état ; ne pas modifier `.ai/governance/`, `Protocole/`, `Implementation/` ou les workflows. |
| Source | Lot 1/2 du parent Phase 1, issu de la veille #5 et du Fil A. |
| Exit criteria | `POLICIES.md` contient la table à cinq colonnes, les trois valeurs fermées, au moins les neuf catégories d'action du brouillon, une source existante par ligne et la clause de priorité ; `AGENTS.md` le route en une ligne et reste à 60 lignes maximum ; aucun contenu source n'est dupliqué en procédure longue ; `git diff --check` passe. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `IMPLEMENTE — GATES PASS, /close EN ATTENTE` |
| Date de creation | 2026-07-30 |
| Date d'activation | - |
| Autorite normative | Les sources citées, jamais `POLICIES.md`. |
| Autorite executable | Aucune. |
| Changement normatif attendu | Aucun. |
| Dependances externes | Aucune. |

## Carte d'execution IA

| Champ | Contenu |
| --- | --- |
| Objectif executable | Indexer les autorisations existantes sans les recopier ni les étendre. |
| Lecture minimale | `AGENTS.md`, workflows commun/core-engine, checklist et politiques `.ai/governance/`. |
| Perimetre autorise | `POLICIES.md`, `AGENTS.md`, ce plan, checkpoint via `plan.ps1`. |
| Interdits absolus | Toute règle nouvelle ou détail procédural copié. |
| Phase de reprise | Phase 1. |
| Preuve attendue | Table complète, chemins existants, AGENTS ≤60 lignes, diff check. |
| Arret et escalade | Une action dont l'autorisation n'est pas tranchée par les sources actuelles. |

## 1. Role de ce document et non-objectifs

Le plan produit un index de navigation. Il ne rend aucune action exécutable.

Non-objectifs :

- ne pas faire de `POLICIES.md` une autorité ;
- ne pas construire un Policy Engine ;
- ne pas inclure des actions absentes du corpus actuel ;
- ne pas dupliquer les workflows.

## 2. Contexte obligatoire

1. `AGENTS.md`.
2. `.ai/workflows/common/WORKFLOW.md`.
3. `.ai/workflows/core-engine/WORKFLOW.md`.
4. `.ai/governance/AI_MODIFICATION_CHECKLIST.md`.
5. `.ai/governance/NORMATIVE_CHANGE_POLICY.md`.
6. `.ai/governance/CONFLICT_RESOLUTION_POLICY.md`.
7. Parent Phase 1.

## 3. Etat des lieux

Les règles existent mais sont réparties selon leur propriétaire. Cette
distribution est légitime ; le manque est seulement un index transversal.

| Zone | Role à conserver |
| --- | --- |
| `AGENTS.md` | Bootstrap et invariants courts. |
| `common/WORKFLOW.md` | Cycle des plans et commits. |
| `core-engine/WORKFLOW.md` | Gates moteur et frontière BACKTRADER. |
| `.ai/governance/` | Transformation et conflits. |

## 4. Decision d'architecture

Une table unique à cinq colonnes, chaque ligne finissant par un lien de source.
Les conditions résument en une proposition ; le lecteur ouvre la source pour
la procédure.

```text
Action -> statut fermé -> conditions courtes -> preuve requise -> source
```

Autorises :

```text
POLICIES.md                                                    [CREER]
AGENTS.md                                                      [MODIFIER]
.ai/backlog/annexes/PLAN_POLICIES_DECLARATIF_IA.md             [MODIFIER]
.ai/checkpoint.json                                            [plan.ps1]
```

Interdits : tout autre fichier.

## 5. Decoupage en phases

### Phase 1 - Construire l'inventaire sourcé

Objectif : écrire l'index minimal sans règle nouvelle.

Classification : GOVERNANCE

Actions :

- créer la clause de statut non autoritatif et de priorité ;
- remplir les actions du brouillon avec `OUI`, `CONDITIONNELLE` ou `NON`;
- citer un chemin propriétaire existant pour chaque ligne ;
- limiter les conditions à un résumé court.

Livrables :

- `POLICIES.md`.

Critere de sortie :

- toutes les catégories d'action ont une source existante et aucune condition
  ne crée une autorisation absente.

### Phase 2 - Router et verifier

Objectif : rendre l'index découvrable sans regonfler le bootstrap.

Classification : GOVERNANCE

Actions :

- ajouter une ligne courte dans `AGENTS.md`;
- vérifier le compte de lignes et les chemins ;
- appliquer plan-conformance.

Livrables :

- pointeur et preuves.

Critere de sortie :

- `AGENTS.md` compte au maximum 60 lignes et `git diff --check` passe.

## 6. Artefacts produits

| Artefact | Role |
| --- | --- |
| `POLICIES.md` | Index déclaratif non autoritatif |
| `AGENTS.md` | Routeur d'une ligne |

## 7. Invariants absolus et NO GO

1. La source propriétaire prime toujours.
2. Une absence de règle ne devient pas `OUI`.
3. L'index ne promet aucun enforcement.

NO GO :

- copier des procédures longues ;
- ajouter des seuils ou gates ;
- inventer une action interface future ;
- modifier une source pour l'adapter à l'index.

## 8. Verification a chaque etape

```powershell
$content = Get-Content POLICIES.md -Raw
@('Action','Autorisée ?','Conditions','Validation requise','Source propriétaire') |
  Where-Object { $content -notmatch [regex]::Escape($_) }

Select-String POLICIES.md -Pattern '\|\s*(OUI|CONDITIONNELLE|NON)\s*\|'
(Get-Content AGENTS.md).Count -le 60

git diff --check
```

Vérification manuelle obligatoire : chaque ligne est comparée à sa source.

### Execution sans interruption

Exécuter les deux phases tant qu'aucune source ne laisse une autorisation
matériellement ambiguë.

### Autorite decisionnelle accordee

L'IA choisit le libellé court et l'ordre des lignes, sans modifier leur sens.

### Interdiction des raccourcis

Un chemin existant ne prouve pas que le résumé est fidèle : la comparaison
ligne par ligne reste obligatoire.

## 9. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-30 | Exécuter la Phase 1 via la boucle de clôture. | Autorise ce lot documentaire. |

## 10. Risques et blocages connus

| Risque | Mitigation |
| --- | --- |
| Index concurrent | Clause de priorité et sources par ligne. |
| AGENTS regonfle | Une seule ligne, plafond 60. |
| Policy future incluse trop tôt | Actions actuelles uniquement. |

## 11. Definition of Done

- [x] Table et clause de priorité présentes.
- [x] Neuf catégories minimales couvertes (14 lignes d'action).
- [x] Chaque source existe et a été vérifiée ligne par ligne.
- [x] `AGENTS.md` route l'index et reste à 49 lignes.
- [x] Aucun fichier hors scope.
- [x] Plan-conformance sans critère manquant.
- [x] `git diff --check` PASS.

## 12. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat final | `DONE` propose : index de 14 actions sourcées, clause de priorité et routeur mince. |
| Ecarts | Commande de vérification corrigée pour conserver les accents réels du header ; aucun écart fonctionnel. |
| Suites a prevoir | Aucune attendue dans ce lot. |

### Resultat d'execution

| Champ | Valeur |
| --- | --- |
| Date | 2026-07-30 |
| Artefacts | `POLICIES.md`; une ligne ajoutée à `AGENTS.md`. |
| Validation | 14 lignes de statut ; 0 source manquante ; `AGENTS.md` 49 lignes ; comparaison manuelle fidèle ; `git diff --check` PASS. |
| Conformance | Tous les critères IMPLEMENTES ; aucun non-goal violé. |

## 13. Journal d'audits post-hoc

| Date | Passe | Correction |
| --- | --- | --- |
| 2026-07-30 | Intake 1 | Vocabulaire fermé et priorité des sources. |
| 2026-07-30 | Intake 2 | Conditions courtes et non-duplication ; convergence. |
| 2026-07-30 | Plan normalise 1 | Inventaire confronté aux propriétaires actuels ; `/start`, `/continue`, `/close`, commit et push seront des lignes distinctes pour éviter une autorisation composite ambiguë. |
| 2026-07-30 | Plan normalise 2 | Contrôle du plafond d'`AGENTS.md`, des neuf catégories et de la clause anti-enforcement ; aucun nouvel angle mort majeur, convergence. |
