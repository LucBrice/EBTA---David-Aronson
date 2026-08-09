# Brouillon — Diagnostic actionnable des ancres de preuve workflow

> Sous-chantier 3/3 de
> `EPIC_AMELIORATIONS_POST_RETROSPECTIVE_CI_NODE20`. Intake autonome, non
> executable avant routage, audits et baseline.

## Objectif

Quand une reference de preuve vise une ancre Markdown absente, conserver le
rejet fail-closed mais rendre l'erreur actionnable en affichant le slug demande
et les slugs de titres valides du fichier, sans exposer le contenu des preuves.

## Constat live

- `Test-EvidenceReferenceSubstance` rejette deja une ancre absente.
- La boucle parcourt deja tous les titres Markdown mais ne conserve pas leurs
  slugs.
- Le message actuel ne montre ni le slug normalise demande ni les choix valides.
- Le test negatif existe, mais `Assert-Throws` ne controle pas le message.
- Les consommateurs sont `Add-WorkflowEvidence`, `plan.ps1` et le harnais
  `.ai/tools/tests/test_workflow_state_machine.ps1`.

## Changement propose

1. Collecter les slugs de titres pendant la validation existante.
2. En cas d'absence, afficher le slug demande et la liste triee/dedupliquee des
   slugs valides; afficher une sentinelle explicite si le fichier n'a aucun titre.
3. Ajouter un helper de test capturant le message, un cas negatif exact et
   conserver le cas positif existant.
4. Ne jamais accepter une ancre auparavant invalide et ne jamais afficher le
   corps du fichier ou le contenu d'une preuve.

## Perimetre

Autorise :

```text
.ai/tools/workflow_state.ps1
.ai/tools/tests/test_workflow_state_machine.ps1
```

## Non-objectifs

- Ne pas modifier `WORKFLOW.json`, `plan.ps1`, les schemas ou le checkpoint.
- Ne pas changer l'algorithme `ConvertTo-HeadingSlug` ni promettre une parite
  GitHub complete.
- Ne pas divulguer les lignes de contenu, chemins absolus ou preuves.
- Ne pas modifier `Protocole/`, `Implementation/` ou BACKTRADER.
- Ne pas effectuer de push.

## Exit criteria

1. Une ancre valide reste acceptee et enregistree.
2. Une ancre absente reste rejetee.
3. L'erreur negative contient le slug demande et les slugs valides, uniquement.
4. Les slugs sont deterministes, tries et dedupliques; le cas sans titre est
   explicite.
5. Le harnais workflow complet retourne `workflow_state_machine=PASS`.
6. Aucun contrat JSON, schema, backend ou fichier hors perimetre n'est modifie.

## Decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-09 | `/continue` persistant sur l'EPIC. | Autorise le cycle gouverne du Lot 3; aucun push. |

## Journal de convergence de l'intake

| Passe | Constat | Correction | Resultat |
| --- | --- | --- | --- |
| `/evaluate` 1 | Le besoin est confirme, mais il faut borner l'ordre, les doublons, le fichier sans titre et la non-divulgation. | Liste triee/dedupliquee, sentinelle sans titre et limites de sortie ajoutees. | Corrections appliquees; seconde passe requise. |
| `/evaluate` 2 | Le correctif reutilise la boucle et le slugger existants; positif, negatif, consommateurs et non-goals sont couverts sans changement de transition. | Aucune correction supplementaire. | `CONVERGE` en 2 passes; aucun angle mort majeur. |
