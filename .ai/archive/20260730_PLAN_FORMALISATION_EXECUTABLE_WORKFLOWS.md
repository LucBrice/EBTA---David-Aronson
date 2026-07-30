# Plan d'implementation — formalisation executable des workflows

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Un chantier couvre-t-il deja ce perimetre ? | Non. La formalisation documentaire est `DONE`; sa suite machine-readable restait hors scope. |
| Un verrou bloque-t-il ce chantier ? | Non. La demande humaine exécute explicitement la suite structurante. |
| Une decision humaine est-elle necessaire ? | Non. Le panel a tranché enforcement strict avec migration honnête des historiques. |
| Ce plan remplace-t-il un chantier ? | Non ; il étend le résultat documentaire sans le réécrire. |

Test `epic-orchestrator` : **SINGLE**. Contrats, moteur de transitions, migration,
tests et documentation sont séquentiels : aucun n'a de sens ou de critère
complet sans les précédents.

## Audit IA de promotion

- [x] Cockpit, workflows, schema et backend relus.
- [x] Brouillon audité en deux passes convergentes.
- [x] Tension strict/legacy tranchée par `expert-panel`.
- [x] Perimetre fermé et sans `Protocole/Implementation`.
- [x] États, preuves et transitions explicités.
- [x] Tests négatifs et intégration temporaire exigés.
- [x] Limite sémantique des références de preuve déclarée.
- [x] Aucune dépendance nouvelle.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `annexe` |
| Lifecycle | `TRIAGED` |
| Type de chantier | `SINGLE` |
| Scope | Rendre les workflows machine-readable et exécutables par une machine à états dans `plan.ps1`, migrer tous les workstreams, générer Mermaid et couvrir les transitions interdites. |
| Non-goals | Ne pas modifier `Protocole/` ou `Implementation/`; ne pas démarrer le workflow interface; ne pas prétendre vérifier sémantiquement un audit ou une preuve; ne pas créer de service, dépendance, RAG, base vectorielle ou agent autonome; ne pas migrer `tracking.json`. |
| Source | Recommandation ajoutée aux suites du chantier de formalisation, puis instruction directe de boucle de clôture du 2026-07-30. |
| Exit criteria | (1) Les trois `WORKFLOW.json` valident contre `WORKFLOW.schema.json`. (2) Les trois `.mmd` sont reproductiblement générés depuis les JSON, sans diff après régénération. (3) Chaque workstream du checkpoint possède `workflow{id,contract_version,stage,evidence}` et le checkpoint valide contre le schema 1.3.0. (4) Tout nouveau `/start` exige audit intake, workflow actif et crée l'état `TRIAGED`; `baseline`, `continue`, `ready`, `close DONE` appliquent les transitions prévues. (5) Les tests négatifs prouvent les refus avant baseline, sans evidence, et avant READY; le chemin nominal passe dans un repo temporaire. (6) Les documents et `POLICIES.md` décrivent les nouvelles commandes sans garantie supérieure au code. (7) `git diff --check` passe. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `ACTIVE` |
| Date de creation | 2026-07-30 |
| Date d'activation | 2026-07-30 |
| Autorite normative | Aucune scientifique ; contrats workflow propriétaires du processus IA uniquement. |
| Autorite executable | `.ai/tools/plan.ps1` et `.ai/tools/workflow_state.ps1`. |
| Changement normatif attendu | Aucun changement EBTA. Changement structurel de gouvernance IA. |
| Dependances externes | PowerShell, Git, Python/jsonschema déjà présents. |

## Carte d'execution IA

| Champ | Contenu |
| --- | --- |
| Objectif executable | Impossible pour `plan.ps1` de franchir une étape workflow interdite ou sans IDs de preuve requis. |
| Autorite et lecture minimale | Bootstrap → `POLICIES.md` → workflows docs → ce plan → contrats JSON → module état → backend → schemas/tests. |
| Perimetre autorise | Liste fermée section 4. |
| Interdits absolus | `Protocole/`, `Implementation/`, interface active, dépendance, preuve sémantique prétendue, édition manuelle Mermaid/checkpoint hors backend. |
| Phase de reprise | Phase 1, contrats et schéma. |
| Preuve attendue | Schémas PASS, Mermaid idempotent, tests unitaires/intégration PASS, migration complète, checkpoint PASS. |
| Arret et escalade | Besoin de modifier runtime EBTA, d'inventer une gate scientifique ou d'altérer une règle humaine non tranchée. |

## 1. Role de ce document et non-objectifs

Ce plan transforme les règles procédurales déjà adoptées en transitions
machine-verifiables. Les JSON de workflow deviennent l'autorité du processus
pour les états/actions/evidence IDs ; les Markdown expliquent le sens humain et
restent nécessaires pour les gates sémantiques.

Non-objectifs :

- ne pas rendre un LLM déterministe ;
- ne pas prouver qu'une référence d'evidence est vraie ;
- ne pas remplacer `code-architecture-evaluator` ou les skills ;
- ne pas stocker l'état runtime EBTA ;
- ne pas activer `interface`.

## 2. Contexte obligatoire

1. `AGENTS.md` et `POLICIES.md`.
2. `.ai/README.md` et `.ai/checkpoint.json`.
3. `.ai/workflows/README.md`, `common/WORKFLOW.md`,
   `core-engine/WORKFLOW.md`, `interface/WORKFLOW.md`.
4. `.ai/checkpoint.schema.json`.
5. `.ai/tools/plan.ps1`.
6. `.agents/skills/epic-orchestrator/SKILL.md`.
7. `.ai/governance/AI_MODIFICATION_CHECKLIST.md`.

## 3. Etat des lieux

| Element | Etat actuel | Manque |
| --- | --- | --- |
| Workflows Markdown | Règles humaines explicites. | Aucun contrat d'états consommable. |
| `plan.ps1` | Structure `/start`, multi-lot, mutation lifecycle. | Ne sait pas prouver double audit, baseline ou gates. |
| Checkpoint 1.2.0 | États macro `status/lifecycle`. | Aucun workflow, stage ou evidence par workstream. |
| Tests | Aucun test dédié au backend. | Transitions négatives non prouvées. |
| Mermaid | Diagrammes manuels dans certains plans. | Pas de vue générée depuis une autorité. |

## 4. Decision d'architecture

### Contrat et état

```text
WORKFLOW.schema.json
  -> <workflow>/WORKFLOW.json (autorité)
       -> workflow_state.ps1
            -> plan.ps1
                 -> checkpoint.workstreams[].workflow
       -> generate_workflow_mermaid.ps1
            -> <workflow>/WORKFLOW.mmd (vue générée)
```

État obligatoire :

```json
{
  "id": "common",
  "contract_version": "1.0.0",
  "stage": "ACTIVE",
  "evidence": [
    {
      "id": "baseline_commit",
      "reference": "abc123",
      "recorded_at": "2026-07-30"
    }
  ]
}
```

Transitions actives :

```text
TRIAGED --baseline--> BASELINED --continue--> ACTIVE
ACTIVE --ready + evidence--> READY_TO_CLOSE --close DONE--> DONE
TRIAGED|BASELINED|ACTIVE|READY_TO_CLOSE --close--> BLOCKED|REJECTED|SUPERSEDED
```

Le backend vérifie la présence des IDs de preuve, pas la vérité sémantique de
leurs références. Les skills et audits humains restent propriétaires de ce
jugement.

### Migration

`migrate-workflows` ajoute l'état à tout workstream sans état :

- `GOVERNANCE` et documentation -> `common`;
- `IMPLEMENTATION_DETAIL`, `CONTRACT_ENCODING`, `TEST_FIXTURE`,
  `ADAPTER_MAPPING` -> `core-engine`;
- `DOCUMENTATION_CLARIFICATION_NEEDED` et `NORMATIVE_CHANGE_REQUIRED` ->
  `common` (l'état historique est importé sans exécuter la décision);
- stage dérivé du lifecycle/status réel ;
- evidence `legacy_import` explicitant qu'aucune gate historique n'est
  ré-attestée.

Après migration, le schema 1.3.0 rend la propriété obligatoire.

### Perimetre de fichiers explicite

Créer :

```text
.ai/workflows/WORKFLOW.schema.json
.ai/workflows/common/WORKFLOW.json
.ai/workflows/common/WORKFLOW.mmd
.ai/workflows/core-engine/WORKFLOW.json
.ai/workflows/core-engine/WORKFLOW.mmd
.ai/workflows/interface/WORKFLOW.json
.ai/workflows/interface/WORKFLOW.mmd
.ai/tools/workflow_state.ps1
.ai/tools/generate_workflow_mermaid.ps1
.ai/tools/tests/test_workflow_state_machine.ps1
```

Modifier :

```text
.ai/tools/plan.ps1
.ai/checkpoint.schema.json
.ai/checkpoint.json                         [plan.ps1 migrate/ready/close]
.ai/workflows/README.md
.ai/workflows/common/WORKFLOW.md
.ai/workflows/core-engine/WORKFLOW.md
.ai/workflows/interface/WORKFLOW.md
.ai/README.md
.ai/governance/AI_MODIFICATION_CHECKLIST.md
POLICIES.md
.ai/backlog/annexes/PLAN_FORMALISATION_EXECUTABLE_WORKFLOWS.md
```

Interdits :

```text
AGENTS.md
Protocole/
Implementation/
Implementation/Active/tracking.json
.agents/
.codex/
0 - HUMAN START HERE/archive/
```

## 5. Decoupage en phases

### Phase 1 - Contrats workflow et vues générées

Objectif : définir une autorité JSON validable pour les trois workflows.

Classification : CONTRACT_ENCODING

Actions :

- créer `WORKFLOW.schema.json`;
- créer les contrats `common`, `core-engine`, `interface`;
- encoder stages, transitions, actions et evidence IDs requis ;
- créer le générateur Mermaid et produire les trois `.mmd`;
- valider schémas et idempotence.

Livrables :

- huit fichiers : schéma, trois contrats, trois vues et générateur.

Critere de sortie :

- trois contrats valides et régénération Mermaid sans diff.

### Phase 2 - Moteur de transitions et backend

Objectif : appliquer le contrat dans `plan.ps1`.

Classification : IMPLEMENTATION_DETAIL

Actions :

- créer `workflow_state.ps1` avec chargement, validation, evidence et
  transition ;
- étendre les actions backend à `baseline`, `ready`, `migrate-workflows`;
- renforcer `start`, `continue`, `close`;
- exiger une référence d'audit post-`/start`, vérifier le commit de baseline
  par Git et prouver que ce commit contient le `source_path` du plan ;
- refuser un workflow `PLANNED`.

Livrables :

- module et backend.

Critere de sortie :

- les actions nominales mutent le stage attendu et les transitions interdites
  lèvent une erreur avant écriture.

### Phase 3 - Schema checkpoint et migration

Objectif : rendre l'état workflow obligatoire sans falsifier l'historique.

Classification : CONTRACT_ENCODING

Actions :

- ajouter la définition `workflow_state` au schema et la rendre requise ;
- passer le checkpoint en 1.3.0 via `migrate-workflows`;
- vérifier chaque workstream, y compris le chantier actif ;
- valider syntaxe et schema.

Livrables :

- checkpoint 1.3.0 intégralement migré.

Critere de sortie :

- zéro workstream sans état workflow et schema PASS.

### Phase 4 - Tests négatifs et documentation

Objectif : prouver l'enforcement et synchroniser les instructions humaines.

Classification : TEST_FIXTURE

Actions :

- créer tests unitaires du module ;
- créer un repo Git temporaire et exécuter les refus et le chemin nominal ;
- tester migration legacy, workflow PLANNED et Mermaid idempotent ;
- mettre à jour registre, workflows Markdown, cockpit, checklist et policies ;
- appliquer plan-conformance.

Livrables :

- test exécutable et documentation synchronisée.

Critere de sortie :

- test PowerShell exit 0, schemas PASS, aucune documentation ne sur-promet.

## 6. Artefacts produits

| Phase | Artefact | Autorité |
| --- | --- | --- |
| 1 | `WORKFLOW.json` | États/transitions/evidence IDs |
| 1 | `WORKFLOW.mmd` | Vue générée non autoritative |
| 2 | module/backend | Enforcement |
| 3 | checkpoint 1.3.0 | État courant |
| 4 | test | Preuve positive/négative |

## 7. Invariants absolus et NO GO

1. Aucun workstream ne manque de workflow après migration.
2. Aucun `DONE` nominal sans `READY_TO_CLOSE`.
3. Aucun `continue` sans `BASELINED`.
4. Une evidence ID prouve seulement qu'une référence a été enregistrée.
5. Mermaid n'est jamais source de transition.
6. L'historique migré ne reçoit aucune fausse gate rétrospective.

NO GO :

- rendre `workflow` optionnel dans le schema final ;
- permettre à `start` de sélectionner `interface`;
- accepter une transition absente du contrat ;
- coder les transitions en double hors des JSON ;
- écrire checkpoint manuellement au lieu de la migration backend ;
- prétendre que `legacy_import` valide un ancien audit ;
- toucher runtime ou protocole EBTA.

## 8. Verification a chaque etape

```powershell
python -c "import json,jsonschema,pathlib; s=json.load(open('.ai/workflows/WORKFLOW.schema.json',encoding='utf-8')); [jsonschema.validate(json.load(open(p,encoding='utf-8')),s) for p in pathlib.Path('.ai/workflows').glob('*/WORKFLOW.json')]; print('workflow_contracts=PASS')"

.\.ai\tools\generate_workflow_mermaid.ps1
$before = Get-ChildItem .ai\workflows -Recurse -Filter WORKFLOW.mmd |
  Sort-Object FullName | Get-FileHash
.\.ai\tools\generate_workflow_mermaid.ps1
$after = Get-ChildItem .ai\workflows -Recurse -Filter WORKFLOW.mmd |
  Sort-Object FullName | Get-FileHash
if (Compare-Object $before.Hash $after.Hash) { throw 'Mermaid generation is not idempotent' }

.\.ai\tools\tests\test_workflow_state_machine.ps1

python -c "import json,jsonschema; jsonschema.validate(json.load(open('.ai/checkpoint.json',encoding='utf-8')),json.load(open('.ai/checkpoint.schema.json',encoding='utf-8'))); print('checkpoint_schema=PASS')"

$cp = Get-Content .ai\checkpoint.json -Raw | ConvertFrom-Json
@($cp.workstreams | Where-Object { -not $_.workflow }).Count

git diff --check
```

Attendus : PASS, Mermaid sans diff, tests exit 0, compteur `0`.

### Execution sans interruption

Exécuter les quatre phases. Une erreur de test impose une correction de cause,
jamais la suppression du test ou l'assouplissement silencieux du contrat.

### Autorite decisionnelle accordee

L'IA peut choisir la structure interne PowerShell et les messages d'erreur,
tant que les états, transitions, preuves, migration et périmètre restent ceux
du plan.

### Interdiction des raccourcis

- pas de transition hardcodée uniquement dans les tests ;
- pas de `.mmd` écrit à la main sans générateur ;
- pas de workstream historique exclu du schema ;
- pas de test qui modifie le vrai checkpoint ;
- pas de succès fondé uniquement sur une recherche sans exécuter les refus.

## 9. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-30 | Ajouter la recommandation machine-readable/Mermaid aux suites. | Ouvre le sujet sans l'implémenter dans le chantier précédent. |
| 2026-07-30 | Exécuter la boucle de clôture des suites. | Autorise ce chantier structurant et son cycle complet. |

## 10. Risques et blocages connus

| Risque | Impact | Mitigation |
| --- | --- | --- |
| Migration historique fabrique des preuves | Audit falsifié | `legacy_import` dit explicitement l'absence de ré-attestation. |
| Références de preuve mensongères | Faux sentiment de sécurité | Limite documentée ; skills et humains jugent le fond. |
| Transitions dupliquées | Drift JSON/code | Module lit les transitions du contrat ; tests changent le JSON. |
| Test altère le vrai repo | État corrompu | Repo temporaire vérifié puis supprimé. |
| Interface activée par accident | Règles D1-D15 contournées | Contrat `PLANNED` refusé par `start`. |
| Baseline circulaire | Commit impossible à référencer | Commit plan d'abord, puis action `baseline`, puis commit d'état séparé. |

## 11. Definition of Done

- [x] Quatre phases validées.
- [x] Sept Exit criteria prouvés.
- [x] Trois contrats schema PASS.
- [x] Trois Mermaid générés et idempotents.
- [x] Checkpoint 1.3.0, zéro workflow manquant.
- [x] Tests positifs/négatifs et intégration temporaire PASS.
- [x] Documentation synchronisée sans sur-promesse.
- [x] Aucun fichier hors scope.
- [x] Plan-conformance sans critère manquant.
- [x] `git diff --check` PASS.

## 12. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat final | Trois contrats JSON, trois Mermaid générés, moteur d'état, backend renforcé, checkpoint 1.3.0 migré, tests adversariaux et documentation synchronisée. |
| Ecarts | Aucun écart fonctionnel ; les références d'evidence restent volontairement une preuve de présence et non une vérification sémantique. |
| Suites a prevoir | Aucune suite nouvellement actionnable. Le workflow `interface` reste `PLANNED` et relève de l'escalade D4 déjà ouverte, après arbitrage humain D1-D15. |

## 13. Journal d'audits post-hoc

| Date | Passe | Correction |
| --- | --- | --- |
| 2026-07-30 | Intake 1 | Forme d'état/evidence et test d'intégration backend temporaire ajoutés. |
| 2026-07-30 | Intake 2 | Baseline non circulaire, migration backend stricte et Mermaid dérivé ; convergence. |
| 2026-07-30 | Plan normalise 1 | Compte Phase 1 corrigé (8), mapping historique complété, preuve Mermaid remplacée par comparaison de hashes couvrant aussi les fichiers non suivis. |
| 2026-07-30 | Plan normalise 2 | Baseline renforcée par une référence d'audit dédiée et la présence du plan dans le commit ; transitions répétées et IDs d'evidence dupliqués ajoutés aux refus à tester ; convergence. |
| 2026-07-30 | Bug-hunter fermeture | Aucun bug confirmé sur les quatre scripts PowerShell : parse PASS, tests hostiles et intégration PASS. Aucun fichier `Implementation/` touché. |
| 2026-07-30 | Adversarial-tester fermeture | PASS : refus du faux SHA, du workflow PLANNED ou incompatible, des preuves dupliquées/manquantes, des transitions sautées/répétées et de `DONE` avant `READY_TO_CLOSE`; migration et génération idempotentes. |
| 2026-07-30 | Plan-conformance fermeture | `IMPLEMENTE` 7/7 depuis `311f265`; zéro critère manquant, zéro fichier interdit, aucun résultat seulement préexistant revendiqué comme livraison. |
