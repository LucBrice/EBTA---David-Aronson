# Brouillon — Lot 1 : substantifier les preuves du gate `ready` de `workflow_state.ps1`

Track : fix
Lifecycle : INTAKE
Scope : Rendre `Add-WorkflowEvidence` (`.ai/tools/workflow_state.ps1`) exigeant
sur la substance des preuves `bug_hunter`, `adversarial_tester`,
`plan_conformance` : la reference doit pointer vers un artefact reel
(fichier existant, avec verification best-effort de l'ancre Markdown si une
ancre est fournie), au lieu d'accepter n'importe quelle chaine non vide.
Non-goals : Ne modifie ni `Assert-WorkflowState` (relit l'historique deja
enregistre — validation retroactive interdite), ni les IDs `intake_audit`,
`plan_audit`, `baseline_commit`, `legacy_import` (formats heterogenes : SHA,
phrase libre — hors perimetre de cette recommandation). Ne verifie pas le
contenu semantique de l'artefact, seulement son existence (et son ancre si
fournie). Ne rend pas la fraude impossible — seulement plus couteuse.
Source : Sous-chantier 1/6 de `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE`,
Phase 1. Recommandation 1 de l'audit source
`0 - HUMAN START HERE/archive/20260807_AUDIT_ROBUSTESSE_ARCHITECTURE_FACE_ERREURS_IA_2026-08-07.md`.
Exit criteria : (1) `Add-WorkflowEvidence` rejette une reference `bug_hunter`,
`adversarial_tester` ou `plan_conformance` qui ne pointe pas vers un fichier
existant du depot ; (2) elle continue d'accepter une reference valide
(fichier existant, avec ou sans ancre valide) ; (3)
`.ai/tools/tests/test_workflow_state_machine.ps1` retourne PASS, y compris un
nouveau cas negatif qui appelle `Add-WorkflowEvidence` avec
`bug_hunter=chaine_arbitraire_sans_artefact` et exige qu'il leve une erreur.

## Contraintes techniques deja etablies par l'audit source (a respecter)

1. Les references reelles deja enregistrees ne sont pas des chemins nus mais
   des chemins avec ancre Markdown
   (`.ai/archive/20260731_PLAN_CORRECTION_MANIFESTE_FREEZE_SOP06.md#resultat-dexecution-...`).
   Il faut decouper sur `#` avant de tester l'existence, et verifier que
   l'ancre existe reellement dans le fichier si elle est fournie.
2. `baseline_commit` porte un SHA et `legacy_import` une phrase libre : la
   validation doit etre **ciblee par ID** (seulement `bug_hunter`,
   `adversarial_tester`, `plan_conformance`), jamais globale.
3. La validation doit rester **a l'ecriture** (`Add-WorkflowEvidence`), pas
   dans `Assert-WorkflowState` qui relit l'historique deja enregistre, sous
   peine de rendre invalides retroactivement des workstreams archives.
4. `.ai/tools/tests/test_workflow_state_machine.ps1` doit rester PASS.

## Honnetete du gain (a respecter dans toute documentation de cloture)

L'existence d'un fichier ne prouve pas son contenu. Ce durcissement eleve le
cout de la fraude (il faut produire un artefact reel) sans la rendre
impossible. Ne jamais presenter ce lot comme rendant la fraude impossible.

## Boucle `/evaluate` d'intake

A executer via `code-architecture-evaluator`, minimum 2 passes, convergence
avant `/start`. Points d'attention deja identifies a verifier pendant la
boucle : comment `Add-WorkflowEvidence` obtient la racine du depot pour
resoudre un chemin relatif (aucun parametre `RepoRoot` n'existe aujourd'hui
dans sa signature) ; tous les appelants (`plan.ps1` lignes ~287, ~389-390,
~437, ~514, et le test unitaire) doivent continuer de fonctionner ou etre
mis a jour explicitement.
