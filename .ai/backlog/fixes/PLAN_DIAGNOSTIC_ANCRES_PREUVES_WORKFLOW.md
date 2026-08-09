# Plan — Diagnostic actionnable des ancres de preuve workflow

## 0. Bandeau de statut

| Champ | Valeur |
| --- | --- |
| ID | `PLAN_DIAGNOSTIC_ANCRES_PREUVES_WORKFLOW` |
| Track | `fix` |
| Lifecycle | `TRIAGED` |
| Portee | `meta` — outillage du workflow, sans changement scientifique EBTA |
| Classification | `IMPLEMENTATION_DETAIL` |
| Type de chantier | `SINGLE` |
| Workflow | `common` |
| Source | `0 - HUMAN START HERE/PLAN_DIAGNOSTIC_ANCRES_PREUVES_WORKFLOW.md` |
| Autorisation | `/continue` du chantier mere; commit local autorise, aucun push |

## Audit IA de promotion

- [x] Bootstrap, checkpoint, workflow et gouvernance lus.
- [x] Parent revalide : Lots 1 et 2 `DONE`, Lot 3 suivant.
- [x] Proprietaire, appels et tests recherches dans le repo live.
- [x] Intake converge en deux passes.
- [x] Test multi-lot : `SINGLE`, car code et test portent un seul comportement.
- [x] Fichiers humains hors perimetre identifies et preserves.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `fix` |
| Lifecycle | `TRIAGED` |
| Type de chantier | `SINGLE` |
| Scope | Enrichir uniquement le diagnostic d'une ancre Markdown invalide et tester le rejet ainsi que le message. |
| Non-goals | Aucun changement de transition, JSON, schema, slugger, contenu de preuve, Protocole, Implementation ou push. |
| Source | Lot 3 de `EPIC_AMELIORATIONS_POST_RETROSPECTIVE_CI_NODE20` et code live de `Test-EvidenceReferenceSubstance`. |
| Exit criteria | Ancre valide acceptee; invalide rejetee avec slug demande et slugs valides tries/dedupliques; sentinelle sans titre; harnais PASS; diff strictement borne. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `TRIAGED`, non executable avant baseline |
| Date | 2026-08-09 |
| Parent | `EPIC_AMELIORATIONS_POST_RETROSPECTIVE_CI_NODE20` |

## Carte d'execution IA

```text
Relire workflow_state.ps1 et le harnais -> verifier les consommateurs ->
baseliner -> modifier code et tests ensemble -> rejouer tout le harnais ->
audits adversarial et conformite -> close local -> reporter au parent.
```

## 1. Role et non-objectifs

Ce plan porte seulement le diagnostic d'une validation existante. Il ne change
ni ce qui constitue une preuve, ni les transitions, ni l'autorite des fichiers.

## 2. Contexte obligatoire a lire

1. `AGENTS.md`, `.ai/checkpoint.json` et le workflow `common`.
2. Le parent EPIC et le gate de consommateurs du skill `/evaluate`.
3. `.ai/tools/workflow_state.ps1`.
4. `.ai/tools/tests/test_workflow_state_machine.ps1`.
5. `.ai/governance/AI_MODIFICATION_CHECKLIST.md`.

## 3. Gates sequentiels

| Gate | Condition | Echec |
| --- | --- | --- |
| G0 | Intake et plan converges, baseline attestee | Ne pas coder |
| G1 | Consommateurs identifies | Corriger le plan |
| G2 | Rejet conserve et sortie limitee aux slugs | Ne pas clore |
| G3 | Harnais complet PASS | Ne pas clore |
| G4 | Adversarial et conformite sans finding | Ne pas clore |

## 4. Etat des lieux

### Existe deja

- `ConvertTo-HeadingSlug` normalise demande et titres.
- `Test-EvidenceReferenceSubstance` exige fichier et ancre reels.
- `Add-WorkflowEvidence` appelle ce validateur pour trois preuves substantielles.
- Le harnais possede un negatif ancre absente et un positif fichier reel.

### Manque reel

- Conservation des slugs parcourus pour le diagnostic.
- Assertion du message d'erreur.
- Cas explicite du fichier sans titre.

### Consommateurs contractuels recherches

| Type | Chemin | Impact |
| --- | --- | --- |
| Producteur | `.ai/tools/workflow_state.ps1::Test-EvidenceReferenceSubstance` | Produit l'erreur |
| Appelant | `.ai/tools/workflow_state.ps1::Add-WorkflowEvidence` | Propage le rejet |
| Backend | `.ai/tools/plan.ps1` | Enregistre les preuves via le validateur |
| Test | `.ai/tools/tests/test_workflow_state_machine.ps1` | Fige rejet, transitions et integration |
| Contrat | `.ai/workflows/common/WORKFLOW.json`, `.ai/workflows/core-engine/WORKFLOW.json` | Lecture seule; aucune valeur changee |

Recherche complete sur `.ai/tools` et `.ai/workflows`; aucun autre producteur,
validateur, fixture, snapshot ou CI ne fige le texte exact de cette erreur.

## 5. Decision d'architecture

Collecter les slugs dans la boucle existante minimise le diff et garantit que
les suggestions suivent exactement le normaliseur deja utilise pour accepter
l'ancre. Trier et dedupliquer rend le message stable. Le helper de test doit
retourner le message capture plutot que rendre `Assert-Throws` plus permissif.

### Frontieres

| Couche | Fait | Ne fait pas |
| --- | --- | --- |
| Validateur | Rejette et suggere des slugs | N'expose pas le contenu |
| Helper test | Capture une erreur exigible | N'avale pas une absence d'erreur |
| Backend/JSON | Restent consommateurs inchanges | Aucun nouveau contrat |

## 6. Decoupage en phases

### Phase 1 — Baseline

Router, auditer deux passes post-route, committer le plan puis attester la
baseline dans le checkpoint.

### Phase 2 — Implementation et tests

- Ajouter une collection de slugs valides.
- Comparer comme aujourd'hui et conserver le rejet.
- Sur echec, formatter `requested slug` et `valid heading slugs`.
- Ajouter `Assert-ThrowsMessage`, negatif exact, positif existant et cas sans titre.
- Rejouer tout le harnais.

### Phase 3 — Audits et fermeture

Executer adversarial-tester, plan-conformance-audit, valider le checkpoint,
clore, committer localement et reporter au parent.

## 7. Artefacts produits

| Artefact | Format | Autorite |
| --- | --- | --- |
| Diagnostic | PowerShell | `workflow_state.ps1` |
| Regressions | PowerShell | harnais workflow |
| Preuves | Markdown | ce plan puis archive |

## 8. Invariants absolus et NO GO

### Invariants

1. Une ancre absente reste une erreur terminante.
2. Le message ne contient que metadonnees, chemin relatif et slugs.
3. Les suggestions sont stables, triees et dedupliquees.
4. Le comportement des transitions et preuves valides reste identique.

### NO GO

- Accepter une ancre par proximite ou fallback.
- Afficher le corps du Markdown ou le contenu d'une preuve.
- Modifier `ConvertTo-HeadingSlug`, JSON, schema ou `plan.ps1`.
- Affaiblir un test ou ne lancer qu'un fragment du harnais.
- Toucher `Protocole/`, `Implementation/` ou les brouillons humains paralleles.

## 9. Verification a chaque etape

```powershell
& .\.ai\tools\tests\test_workflow_state_machine.ps1
git diff --name-only -- .ai/workflows/*.json .ai/tools/plan.ps1 .ai/checkpoint.schema.json
python -c "import json,jsonschema; jsonschema.validate(json.load(open('.ai/checkpoint.json',encoding='utf-8')),json.load(open('.ai/checkpoint.schema.json',encoding='utf-8')))"
git diff --check -- .ai
```

## 10. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-09 | `/continue`. | Executer les lots bornes de l'EPIC et committer localement; aucun push. |

## 11. Risques

| Risque | Controle |
| --- | --- |
| Faux succes | Negatif prouve qu'une exception est toujours levee |
| Fuite de contenu | Assertion du message et revue adversariale |
| Message instable | Tri et deduplication |
| Regression backend | Harnais integration complet |

## 12. Definition of Done

- [ ] Scope, track, type et classification coherents.
- [ ] Exit criteria 1-6 prouves.
- [ ] Harnais workflow complet PASS.
- [ ] Fichiers interdits sans diff.
- [ ] Bug-hunter classe; adversarial et conformite sans finding.
- [ ] Checkpoint valide et aucun push.

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat final | A remplir lors de `/close` |
| Ecarts | A remplir lors de `/close` |
| Suites | Retour au parent pour audit global et cloture |

## 14. Journal d'audits post-hoc

### Journal de convergence de l'intake

| Passe | Constat | Correction | Resultat |
| --- | --- | --- | --- |
| 1 | Ordre, doublons, sans-titre et non-divulgation initialement sous-specifies. | Critere deterministe et sortie bornee ajoutes. | Correction; seconde passe. |
| 2 | Propriete, consommateurs, positif/negatif et non-goals couverts. | Aucune. | `CONVERGE`. |

### Journal d'audits post-route

| Passe | Constat | Correction | Resultat |
| --- | --- | --- | --- |
| `/evaluate` 1 | Le plan doit figer une sentinelle sans titre et eviter de changer le helper existant. | `Assert-ThrowsMessage` separe et sentinelle explicite ajoutes. | Correction appliquee. |
| `/evaluate` 2 | Contre-audit du plan corrige contre producteurs, appelants, JSON et harnais. Aucun changement de contrat machine ni angle mort majeur. | Aucune. | `CONVERGE` en 2 passes. |
