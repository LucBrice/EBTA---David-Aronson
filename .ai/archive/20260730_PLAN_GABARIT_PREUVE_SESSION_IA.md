# Plan — template JSON de preuve de session IA

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Chantier existant ? | Aucun ; enfant 2/2 de `EPIC_PHASE_1_POLICIES_ET_PREUVE_SESSION`. |
| Verrou actif ? | Aucun. |
| Decision humaine ? | Non, la boucle demande ce palier documentaire. |
| Remplacement ? | Non. |

Test `epic-orchestrator` : **SINGLE**. Le template et sa documentation forment
un seul contrat de compréhension.

## Audit IA de promotion

- [x] Source Phase 1 et veille #2 relues.
- [x] Deux passes intake convergentes.
- [x] Champs minimaux et liens claim/evidence définis.
- [x] Risque de fausse attestation traité.
- [x] Schéma, validateur, registre et gate exclus.
- [x] Périmètre limité au template et au README.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `annexe` |
| Lifecycle | `TRIAGED` |
| Type de chantier | `SINGLE` |
| Scope | Créer un template JSON copiable de preuve de session et documenter son usage non mécanique dans le README de gouvernance. |
| Non-goals | Ne créer ni schéma, validateur, registre de sessions, état projet, gate de clôture ou obligation générale ; ne pas modifier le contrat de commit, `Protocole/` ou `Implementation/`. |
| Source | Lot 2/2 du parent Phase 1, veille #2 et Fil A. |
| Exit criteria | Le JSON est valide, porte `template_only: true`, les champs minimaux et complémentaires, au moins un test exemple et une claim dont tous les `evidence_ids` existent ; les statuts de test sont dans `PASS|FAIL|SKIP|NOT_RUN` et les types de preuve dans `COMMAND_OUTPUT|FILE|DIFF|COMMIT|MANUAL_REVIEW`; tous les exemples restent des placeholders ; le README le référence comme optionnel et non mécaniquement validé ; `git diff --check` passe. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `IMPLEMENTE — GATES PASS, /close EN ATTENTE` |
| Date de creation | 2026-07-30 |
| Date d'activation | - |
| Autorite normative | Aucune ; `.ai/governance/README.md` décrit le rôle procédural. |
| Autorite executable | Aucune. |
| Changement normatif attendu | Aucun. |
| Dependances externes | Aucune. |

## Carte d'execution IA

| Champ | Contenu |
| --- | --- |
| Objectif executable | Fournir un exemple JSON honnête reliant claims, tests et evidence. |
| Lecture minimale | Parent, contrat de commit, README de gouvernance, ce plan. |
| Perimetre autorise | Template JSON, README, ce plan, checkpoint via `plan.ps1`. |
| Interdits absolus | Toute mécanique ou preuve réelle dans le template. |
| Phase de reprise | Phase 1. |
| Preuve attendue | JSON syntaxe, références internes, vocabulaire fermé, README, diff check. |
| Arret et escalade | Tout besoin de rendre le template obligatoire ou d'imposer un chemin de stockage réel. |

## 1. Role de ce document et non-objectifs

Le template est un exemple à copier. Il ne stocke aucune session et ne prouve
rien par sa seule existence.

Non-objectifs :

- ne pas remplacer les commits ;
- ne pas créer de source d'état ;
- ne pas annoncer de validation absente ;
- ne pas choisir où les preuves réelles seront persistées.

## 2. Contexte obligatoire

1. `.ai/workflows/common/WORKFLOW.md`, contrat de commit.
2. `.ai/governance/README.md`.
3. Parent Phase 1.
4. Brouillon enfant archivé.

## 3. Etat des lieux

Les commits exigent déjà le pourquoi, les fichiers, non-touchés et validations,
mais sous forme de prose. Aucun objet de session structuré n'existe. Le manque
est un modèle, pas encore un système de stockage ou d'enforcement.

## 4. Decision d'architecture

Un JSON valide contient :

```text
template_only, template_version, session_id, task_id, objective
files_modified[], files_not_touched[]
tests_executed[{command,status,result}]
claims[{claim_id,statement,evidence_ids[]}]
evidence[{evidence_id,type,reference,verification}]
risks_remaining[], decisions_required[]
```

Tous les exemples textuels utilisent `<...>`. Les références de claim sont
vérifiées ponctuellement contre les IDs d'evidence.

Autorises :

```text
.ai/governance/TEMPLATE_PREUVE_SESSION_IA.json                 [CREER]
.ai/governance/README.md                                      [MODIFIER]
.ai/backlog/annexes/PLAN_GABARIT_PREUVE_SESSION_IA.md         [MODIFIER]
.ai/checkpoint.json                                            [plan.ps1]
```

Interdits : tout autre fichier.

## 5. Decoupage en phases

### Phase 1 - Ecrire le template

Objectif : produire un JSON valide, non assimilable à une preuve réelle.

Classification : GOVERNANCE

Actions :

- écrire les champs et tableaux définis ;
- utiliser `template_only: true` et des placeholders ;
- relier une claim exemple à une evidence exemple ;
- utiliser un statut de test autorisé.

Livrables :

- `.ai/governance/TEMPLATE_PREUVE_SESSION_IA.json`.

Critere de sortie :

- syntaxe JSON, références internes et vocabulaire passent.

### Phase 2 - Documenter les limites

Objectif : rendre le template découvrable sans inventer de mécanique.

Classification : GOVERNANCE

Actions :

- ajouter son rôle dans le README ;
- indiquer qu'il est optionnel, copiable, non persistant et non validé
  automatiquement ;
- vérifier le diff.

Livrables :

- README mis à jour.

Critere de sortie :

- aucune garantie mécanique absente n'est annoncée.

## 6. Artefacts produits

| Artefact | Role |
| --- | --- |
| Template JSON | Exemple structuré |
| README | Mode d'emploi et limites |

## 7. Invariants absolus et NO GO

1. Le modèle n'est jamais une preuve.
2. Toute claim exemple référence une evidence existante.
3. Aucun emplacement de preuve réelle n'est imposé.

NO GO :

- `template_only: false`;
- résultat réel ou chemin de session réelle ;
- nouveau statut de workstream ;
- prétendre que `/close` valide ce JSON ;
- créer un schéma ou script permanent.

## 8. Verification a chaque etape

```powershell
python -m json.tool .ai/governance/TEMPLATE_PREUVE_SESSION_IA.json

$t = Get-Content .ai/governance/TEMPLATE_PREUVE_SESSION_IA.json -Raw | ConvertFrom-Json
$ids = @($t.evidence.evidence_id)
$missing = @($t.claims.evidence_ids | Where-Object { $_ -notin $ids })
$badStatus = @($t.tests_executed.status | Where-Object { $_ -notin @('PASS','FAIL','SKIP','NOT_RUN') })
$badType = @($t.evidence.type | Where-Object { $_ -notin @('COMMAND_OUTPUT','FILE','DIFF','COMMIT','MANUAL_REVIEW') })
if (-not $t.template_only -or $missing.Count -or $badStatus.Count -or $badType.Count) { throw 'template contract invalid' }

Select-String .ai/governance/README.md -Pattern 'TEMPLATE_PREUVE_SESSION_IA.json'
git diff --check
```

Vérification manuelle : chaque valeur exemple non booléenne/versionnée est un
placeholder, et le README ne promet aucun gate.

### Execution sans interruption

Exécuter les deux phases sauf si un emplacement réel ou une obligation
mécanique devient nécessaire.

### Autorite decisionnelle accordee

L'IA choisit les noms secondaires et l'exemple, en conservant les champs
minimaux et les limites.

### Interdiction des raccourcis

Un JSON valide ne prouve ni la cohérence des IDs ni la véracité des claims ;
les deux contrôles supplémentaires sont obligatoires.

## 9. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-30 | Exécuter la Phase 1 via la boucle de clôture. | Autorise ce template documentaire. |

## 10. Risques et blocages connus

| Risque | Mitigation |
| --- | --- |
| Template pris pour preuve | `template_only`, placeholders, README. |
| Fausse validation | Commande ponctuelle explicitement distincte d'un gate. |
| État concurrent | Aucun stockage réel ni registre. |

## 11. Definition of Done

- [x] JSON valide et contrat interne PASS.
- [x] Champs minimaux et complémentaires présents.
- [x] Toutes les valeurs propres à une session restent des placeholders ; les
      IDs internes `claim-1`/`evidence-1` sont des identifiants d'exemple
      explicitement reliés.
- [x] README documente usage et limites.
- [x] Aucun fichier hors scope.
- [x] Plan-conformance sans critère manquant.
- [x] `git diff --check` PASS.

## 12. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat final | `DONE` propose : template JSON valide, cohérent et non assimilable à une preuve réelle. |
| Ecarts | Aucun. |
| Suites a prevoir | Aucune attendue ; mécanisation reste Phase 2 conditionnelle, hors scope. |

### Resultat d'execution

| Champ | Valeur |
| --- | --- |
| Date | 2026-07-30 |
| Artefacts | Template JSON et documentation dans le README de gouvernance. |
| Validation | JSON PASS ; `template_only=True`; 0 ID manquant ; 0 statut/type invalide ; limites README présentes ; `git diff --check` PASS. |
| Conformance | Tous critères IMPLEMENTES ; aucun non-goal violé. |

## 13. Journal d'audits post-hoc

| Date | Passe | Correction |
| --- | --- | --- |
| 2026-07-30 | Intake 1 | Marqueur template et placeholders anti-fausse-attestation. |
| 2026-07-30 | Intake 2 | Cohérence IDs/statuts vérifiable ponctuellement ; convergence. |
| 2026-07-30 | Plan normalise 1 | Vocabulaire des types de preuve fermé et ajouté au contrôle ponctuel pour éviter des catégories libres incompatibles. |
| 2026-07-30 | Plan normalise 2 | Relecture du contrat de commit, des placeholders et des non-goals ; aucun nouvel angle mort majeur, convergence. |
