# Registre des workflows IA

Un workflow decrit les regles procedurales propres a une famille de travail.
Ce registre est une reference lue par l'IA ; il n'ajoute aucun champ a
`.ai/checkpoint.json`, aucun parametre a `.ai/tools/plan.ps1` et aucun
routage comportemental automatique.

`AGENTS.md` reste le bootstrap universel. Chaque `WORKFLOW.md` complete ce
bootstrap sans devenir une autorite scientifique EBTA ni un cockpit d'etat.

## Registre

| ID | Etat documentaire | Fichier | Perimetre |
| --- | --- | --- | --- |
| `common` | ACTIF — lecture obligatoire | `.ai/workflows/common/WORKFLOW.md` | Regles universelles : commits, cycle `/start` → `/close`, doubles boucles `/evaluate`, multi-lot et clarification. |
| `core-engine` | ACTIF | `.ai/workflows/core-engine/WORKFLOW.md` | Plans, runtime, adaptateurs et code du moteur EBTA. |
| `interface` | PLANNED — non demarre | `.ai/workflows/interface/WORKFLOW.md` | Futur workflow de conception/validation UX ; aucune regle active. |

## Convention obligatoire

Tout fichier Markdown ajoute sous `.ai/workflows/` doit etre inscrit dans le
tableau ci-dessus ou explicitement reference par une de ses lignes. Un fichier
orphelin n'est jamais executable par defaut.

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
