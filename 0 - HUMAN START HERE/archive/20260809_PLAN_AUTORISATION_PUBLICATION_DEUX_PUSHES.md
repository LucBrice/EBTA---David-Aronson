# Brouillon — Autorisation explicite des deux pushes potentiels

> Sous-chantier 2/3 de
> `EPIC_AMELIORATIONS_POST_RETROSPECTIVE_CI_NODE20`. Intake autonome et non
> executable avant son cycle `/start`, audits et baseline.

## Objectif

Clarifier `.ai/workflows/common/WORKFLOW.md` pour le cas ou un gate distant
exige un push du commit d'implementation avant `/close`, alors que `/close`
cree ensuite un commit local de fermeture qui ne peut etre publie que par un
second push distinct et conditionnel.

## Constat live

- Le contrat d'autorisation separe deja persistance, commit et push.
- `/close` cree un commit de fermeture limite a ses fichiers et interdit tout
  push automatique.
- Le workflow ne demande pas encore de distinguer explicitement, dans la
  question d'autorisation, le push d'implementation necessaire au gate distant
  et l'eventuel push du commit de fermeture.
- L'incident CI Node.js 20 a produit `54e00f4` pour l'implementation publiee,
  puis `0d70f77` pour la fermeture locale; l'autorisation du premier push ne
  couvrait pas automatiquement le second.
- `PLAN_INTEGRATION_LEARN_SESSION_POST_CLOSE` est `DONE`; son texte est deja
  integre au workflow courant et ne constitue plus un conflit actif.

## Changement propose

Ajouter au contrat conversationnel une regle concise :

1. Quand un gate distant impose un push avant `/close`, enumerer separement
   dans la demande d'autorisation :
   - push A, publication du commit d'implementation pour executer le gate;
   - push B, publication conditionnelle du commit de fermeture cree apres
     validations et `/close`.
2. L'autorisation de A n'autorise jamais B.
3. Une autorisation couvrant A et B doit les nommer explicitement; B reste
   conditionne a l'existence et au succes du commit de fermeture et ne peut
   embarquer aucun autre commit hors scope.
4. Si seul A est autorise, terminer `/close` avec le commit local et signaler
   que B attend une autorisation separee; ne jamais le deduire de A.
5. Si la validation ou le commit de fermeture echoue, B est interdit meme
   lorsqu'il avait ete autorise conditionnellement.
6. Ne modifier ni `WORKFLOW.json`, ni les transitions, ni les permissions ou
   gates executables.

## Perimetre

Autorise :

```text
.ai/workflows/common/WORKFLOW.md
```

Lecture seule :

```text
.ai/workflows/common/WORKFLOW.json
.ai/tools/plan.ps1
.ai/checkpoint.json
.ai/archive/20260809_PLAN_CORRECTION_CI_NODE20_DEPRECATION_CORE_ENGINE.md
.ai/archive/20260809_PLAN_INTEGRATION_LEARN_SESSION_POST_CLOSE.md
```

## Non-objectifs

- Ne pas autoriser un push implicite ou automatique.
- Ne pas modifier `WORKFLOW.json`, Mermaid, `plan.ps1` ou un hook Git.
- Ne pas changer le contrat de commit automatique de `/close`.
- Ne pas ajouter de transition, preuve machine ou champ checkpoint.
- Ne pas modifier `Protocole/`, `Implementation/`, BACKTRADER ou les autres
  fichiers humains.
- Ne pas effectuer de push dans ce chantier.

## Exit criteria

1. Le workflow nomme les deux pushes potentiels et leur ordre.
2. Il dit explicitement que l'autorisation du push A n'autorise pas le push B.
3. Il permet une autorisation anticipee des deux seulement si les deux sont
   nommes et si B reste conditionnel au commit de fermeture valide, sans
   commit hors scope.
4. Le workflow exige l'arret apres commit local si seul A est autorise et
   interdit B si validation/commit de fermeture echoue.
5. `/close` reste sans push automatique, `WORKFLOW.json` reste identique et
   `.ai/tools/tests/test_workflow_state_machine.ps1` retourne `PASS`.
6. Les recherches textuelles ciblent le nouveau contrat et une contre-preuve
   confirme qu'aucune phrase ne transforme A en autorisation implicite de B.
7. Aucun fichier hors perimetre n'est modifie.

## Decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-09 | `Je valide tes propositions`, puis `/continue`. | Autorise le cycle gouverne du Lot 2 apres cloture du Lot 1. N'autorise aucun push. |

## Journal de convergence de l'intake

| Passe | Constat | Correction | Resultat |
| --- | --- | --- | --- |
| `/evaluate` 1 | Le principe A/B est coherent avec le workflow live, mais le brouillon ne bornait pas le cas d'echec de validation/commit et ne disait pas quoi faire si seul A est autorise. Il ne declarait pas non plus la suite de tests executable du workflow. Migration, API, deploiement, monitoring et donnees sont non applicables; contrat, tests, phase transitoire et documentation sont les angles pertinents. | Ajout du stop local si seul A est autorise, de l'interdiction de B apres echec, et du test `test_workflow_state_machine.ps1` dans l'Exit criteria. | Corrections appliquees; seconde passe requise. |
| `/evaluate` 2 | Contre-audit du brouillon corrige contre `WORKFLOW.md`, `WORKFLOW.json`, `plan.ps1` et l'historique CI. Le chantier est `SINGLE` : une clarification documentaire et sa preuve de non-regression forment une sequence unique. Les deux autorisations restent separees, B est conditionnel et fail-closed, aucune transition machine n'est modifiee. | Aucune correction supplementaire. | `CONVERGE` en 2 passes; aucun angle mort majeur restant. |
