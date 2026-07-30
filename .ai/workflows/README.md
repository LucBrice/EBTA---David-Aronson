# Registre des workflows IA

Un workflow decrit les regles procedurales propres a une famille de travail.
Chaque dossier contient trois representations aux responsabilites distinctes :

- `WORKFLOW.json` est l'autorite machine-readable sur les etats, transitions
  et IDs de preuve requis ;
- `WORKFLOW.mmd` est une vue Mermaid generee depuis ce JSON, jamais une
  autorite ni un fichier a editer manuellement ;
- `WORKFLOW.md` explique les jugements humains et les commandes.

`.ai/tools/workflow_state.ps1` applique le contrat et
`.ai/tools/plan.ps1` persiste l'etat sous
`checkpoint.workstreams[].workflow`. Le backend verifie qu'un ID et une
reference de preuve existent ; il ne prouve jamais que leur contenu est vrai.
`AGENTS.md` reste le bootstrap universel et aucun de ces fichiers ne devient
une autorite scientifique EBTA.

## Registre

| ID | Etat executable | Contrat | Perimetre |
| --- | --- | --- | --- |
| `common` | `ACTIVE` — lecture obligatoire | `.ai/workflows/common/WORKFLOW.json` | Regles universelles : commits, cycle `/start` → `/close`, doubles boucles `/evaluate`, multi-lot et clarification. |
| `core-engine` | `ACTIVE` | `.ai/workflows/core-engine/WORKFLOW.json` | Plans, runtime, adaptateurs et code du moteur EBTA. |
| `interface` | `PLANNED` — non executable | `.ai/workflows/interface/WORKFLOW.json` | Futur workflow de conception/validation UX ; aucune transition autorisee. |

## Convention obligatoire

Tout workflow ajoute sous `.ai/workflows/` doit valider contre
`WORKFLOW.schema.json`, etre inscrit ci-dessus et fournir JSON, Markdown et
Mermaid genere. Un fichier orphelin n'est jamais executable par defaut.

Precedent : `WORKFLOW_VALIDATION_UX_EBTA.updated.md` a existe ici sans
registre ni point d'entree. Il a ete reclasse le 2026-07-29 comme brouillon
`INTAKE` sous
`0 - HUMAN START HERE/PROPOSITION_WORKFLOW_VALIDATION_UX_EBTA.md`, puis le
dossier a ete recree proprement par le plan de formalisation.

## Selection

- Pour toute action substantielle, lire d'abord `common`.
- Pour toute tache touchant `Implementation/`, un adaptateur de backtest, un
  gate executable ou une fermeture de chantier moteur, lire ensuite
  `core-engine`.
- Pour `interface`, ne rien executer depuis ce registre : les propositions
  doivent d'abord suivre `/start` et leurs contradictions doivent etre
  arbitrees.
- Si aucun workflow specialise ne correspond, appliquer `AGENTS.md` puis
  `common`, et escalader avant d'inventer une procedure specialisee.

## Generation et validation

```powershell
.\.ai\tools\generate_workflow_mermaid.ps1
.\.ai\tools\tests\test_workflow_state_machine.ps1
```

Une regeneration qui modifie un `.mmd` signale soit un changement du contrat
JSON, soit un drift a examiner. Ne jamais corriger la vue pour contourner le
contrat.
