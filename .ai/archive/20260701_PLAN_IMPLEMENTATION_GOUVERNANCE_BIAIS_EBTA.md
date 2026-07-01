# PLAN D'IMPLÉMENTATION — Gouvernance des biais humains dans EBTA

## Audit IA avant routage

- [x] Brouillon humain lu depuis `0 - HUMAN START HERE/`.
- [x] Bootstrap EBTA lu : `AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json`, hook actif, tracking actif.
- [x] Gouvernance IA lue : `.ai/governance/AI_MODIFICATION_CHECKLIST.md`.
- [x] Point d'entrée protocolaire lu : `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md`.
- [x] Classification initiale : `NORMATIVE_CHANGE_REQUIRED`.
- [x] Décision de routage : annexe, car le chantier propose une évolution transversale du protocole et du runtime sans remplacer le mainline actif `STEP_3_BACKTRADER_INTEGRATION`.

| Champ | Valeur |
| --- | --- |
| Track | annexe |
| Lifecycle | TRIAGED |
| Scope | Audit, décision normative éventuelle, documentation protocolaire, schémas et contrôles runtime subordonnés au protocole. |
| Non-goals | Ne pas implémenter directement un nouveau gate EBTA sans décision normative explicite ; ne pas contourner le gel `EBTA-DOC-1.0` ; ne pas modifier BACKTRADER ; ne pas affaiblir WRC, préenregistrement, ouverture unique OOS ou non-réparation post-OOS. |
| Source | Brouillon humain `0 - HUMAN START HERE/PLAN_IMPLEMENTATION_GOUVERNANCE_BIAIS_EBTA.md`, audité par IA avant promotion. |
| Exit criteria | Le chantier est routé dans `.ai/backlog/annexes/`, visible dans `.ai/checkpoint.json`, et bloqué avant mutation protocolaire tant qu'une décision normative explicite n'ouvre pas la version documentaire requise. |

## Objectif

Mettre en place une couche transversale de gouvernance permettant d'identifier, verrouiller, tracer et corriger les biais humains susceptibles de fausser le protocole EBTA.

L'objectif n'est pas de modifier la logique statistique centrale du protocole, mais d'ajouter une couche de contrôle méthodologique explicite :

```text
Biais humain potentiel
→ risque nommé
→ détecteur technique
→ gate bloquant
→ incident versionné
→ procédure corrective
→ statut final auditable
```

Cette implémentation doit distinguer clairement :

- les modifications documentaires dans `/Protocole` ;
- les modifications exécutables dans `/Implementation` ;
- les templates et schémas nécessaires à la traçabilité ;
- les tests de non-régression garantissant que les nouveaux contrôles ne cassent pas l'existant.

---

# 1. Périmètre général

## 1.1. Ce qui doit être ajouté

Ajouter une gouvernance explicite des biais humains couvrant au minimum :

- p-hacking ;
- data snooping ;
- HARKing ;
- cherry-picking ;
- sélection opportuniste d'actifs ;
- metric shopping ;
- benchmark shopping ;
- robustness shopping ;
- contamination OOS ;
- OOS repair ;
- bug opportuniste ;
- suppression de candidates perdantes ;
- exclusion post-hoc de périodes, trades, actifs ou coûts ;
- narration post-échec non distinguée d'une hypothèse confirmatoire.

## 1.2. Ce qui ne doit pas être fait

Ne pas réécrire tout le protocole EBTA.

Ne pas modifier la philosophie générale Train/Test/OOS.

Ne pas affaiblir les exigences existantes de préenregistrement, de WRC/MCP, de registre des candidates ou d'ouverture unique de l'OOS.

Ne pas transformer les procédures correctives en moyen de sauver une stratégie échouée.

Ne pas permettre à un incident post-OOS de redevenir confirmatoire sur le même segment OOS.

---

# 2. Modifications dans `/Protocole`

## 2.1. Créer un nouveau SOP dédié

### Type de modification

`/Protocole`

### Fichier à créer

```text
/Protocole/SOP 13 - Gouvernance des biais humains et incidents méthodologiques.md
```

### Objectif du fichier

Créer une SOP transversale qui formalise :

- les biais humains comme risques méthodologiques ;
- leur niveau de gravité ;
- les artefacts à contrôler ;
- les gates impactés ;
- les procédures de correction ;
- les conditions de reprise ou d'invalidation.

### Contenu attendu

Le SOP doit contenir au minimum les sections suivantes :

```text
# SOP 13 - Gouvernance des biais humains et incidents méthodologiques

## 1. Principe général
## 2. Définition d'un biais humain EBTA
## 3. Taxonomie des biais
## 4. Niveaux de gravité
## 5. Incidents méthodologiques
## 6. Gates impactés
## 7. Procédures correctives
## 8. Contamination OOS
## 9. Règles pour les agents IA et assistants de recherche
## 10. Critères de PASS / FAIL / INCONCLUSIVE / BURNED
## 11. Artefacts obligatoires
## 12. Checklist de revue indépendante
```

### Règles conceptuelles à inclure

Inclure explicitement cette règle :

```text
Aucun résultat EBTA ne peut être interprété sans audit explicite des biais humains ayant pu influencer la génération, la sélection, la modification, l'exclusion, la visualisation ou la narration des candidates.
```

Inclure aussi cette règle :

```text
Tout biais détecté devient un incident méthodologique versionné, rattaché au registre, et gouverné avant tout verdict statistique, économique ou OOS.
```

---

## 2.2. Créer un registre des risques de biais

### Type de modification

`/Protocole`

### Fichier à créer

```text
/Protocole/BIAS_RISK_REGISTER.md
```

### Objectif du fichier

Lister les biais humains connus sous forme de risques auditables.

### Structure obligatoire pour chaque risque

Chaque entrée doit suivre ce format :

```text
## BIAS-XXX — Nom du biais

- Description :
- Phase concernée :
- Comportement humain typique :
- Manipulation consciente ou inconsciente possible :
- Signal de détection :
- Artefact contrôlé :
- Gate impacté :
- Niveau de gravité par défaut :
- Procédure corrective :
- SOP propriétaire :
- Exemples :
```

### Biais minimum à documenter

Créer au minimum les entrées suivantes :

```text
BIAS-001 — P-hacking
BIAS-002 — Data snooping
BIAS-003 — HARKing
BIAS-004 — Cherry-picking de candidates
BIAS-005 — Cherry-picking d'actifs
BIAS-006 — Suppression de candidates perdantes
BIAS-007 — Metric shopping
BIAS-008 — Benchmark shopping
BIAS-009 — Hurdle shopping
BIAS-010 — Robustness shopping
BIAS-011 — Stress-test réparateur
BIAS-012 — Exclusion post-hoc d'outliers
BIAS-013 — Hypothèse de régime post-hoc
BIAS-014 — OOS peeking
BIAS-015 — OOS repair
BIAS-016 — Bug opportuniste
BIAS-017 — Retest déguisé
BIAS-018 — Narration post-échec
BIAS-019 — Sélection opportuniste de coûts
BIAS-020 — Contamination par agent IA
```

---

## 2.3. Créer un template d'incident méthodologique

### Type de modification

`/Protocole`

### Fichier à créer

```text
/Protocole/TEMPLATE - Incident de biais EBTA.md
```

### Objectif du fichier

Fournir un format standard pour documenter tout biais détecté.

### Structure attendue

```text
# Incident de biais EBTA

## 1. Identification
- Incident ID :
- Date :
- Projet :
- Research Family ID :
- Candidate ID :
- Fold ID :
- Phase :
- Détecté par :

## 2. Type de biais
- Bias ID :
- Nom du biais :
- Description courte :

## 3. Preuve
- Artefact concerné :
- Hash avant incident :
- Hash après incident :
- Logs concernés :
- Description factuelle :

## 4. Gravité
- Niveau : LEVEL_0 / LEVEL_1 / LEVEL_2 / LEVEL_3 / LEVEL_4 / LEVEL_5
- Justification :

## 5. Impact méthodologique
- Gate impacté :
- OOS impacté : oui/non
- Famille contaminée : oui/non
- Étendue de la contamination :

## 6. Décision
- Statut : OPEN / RESOLVED / FAIL / INCONCLUSIVE / BURNED
- Action corrective :
- Reviewer :
- Date de clôture :
```

---

## 2.4. Créer un template de dérogation méthodologique

### Type de modification

`/Protocole`

### Fichier à créer

```text
/Protocole/TEMPLATE - Dérogation méthodologique EBTA.md
```

### Objectif du fichier

Permettre de documenter une exception contrôlée sans casser silencieusement le protocole.

### Règle importante

Une dérogation ne doit jamais permettre de :

- réparer une stratégie après observation OOS ;
- retirer des candidates perdantes ;
- changer la métrique primaire après résultat ;
- réduire l'univers testé après observation ;
- requalifier un échec OOS en succès.

---

## 2.5. Modifier le protocole principal

### Type de modification

`/Protocole`

### Fichier à modifier

```text
/Protocole/PROTOCOLE EBTA.md
```

### Modifications attendues

Ajouter une section transversale :

```text
## Gouvernance des biais humains
```

Cette section doit :

- pointer vers `SOP 13 - Gouvernance des biais humains et incidents méthodologiques.md` ;
- rappeler que tout biais détecté est un incident méthodologique ;
- introduire un gate transversal `G-BIAS` ;
- préciser que `G-BIAS` doit être satisfait avant ouverture OOS et avant validation finale ;
- préciser que les agents IA sont inclus dans la notion d'exposition et de contamination.

### Gate à ajouter

Ajouter ce gate dans la chaîne de validation :

```text
G-BIAS — Contrôle anti-biais transversal

PASS si :
- le registre des expériences est complet ;
- aucune candidate influente n'est absente de la famille statistique ;
- aucune métrique, hurdle, coût ou benchmark n'a été modifié après observation des résultats ;
- aucun actif perdant n'a été retiré de l'univers évalué ;
- aucune sortie OOS non autorisée n'a été consultée ;
- aucun stress-test décisionnel n'a été ajouté après observation ;
- aucun incident ouvert de niveau 2 ou supérieur ne bloque la validation ;
- la revue indépendante confirme la cohérence des artefacts.

Sinon :
- FAIL, INCONCLUSIVE ou BURNED selon la gravité.
```

---

## 2.6. Modifier les SOP existantes par renvoi léger

### Type de modification

`/Protocole`

### Fichiers à inspecter et modifier si nécessaire

```text
/Protocole/SOP 03 - Registre des expériences et univers des règles candidates.md
/Protocole/SOP 05 - Tests de robustesse et gouvernance du holdout.md
/Protocole/SOP 10 - Gouvernance OOS et gestion des échecs.md
/Protocole/SOP 12 - Reproductibilité et paquet de validation EBTA.md
```

### Modification attendue

Ne pas les réécrire.

Ajouter uniquement des renvois vers SOP 13 lorsque pertinent.

Exemples de renvois :

```text
Tout écart lié à une candidate manquante, un run non tracé, un actif retiré ou une famille statistique incomplète doit être déclaré comme incident méthodologique selon SOP 13.
```

```text
Toute consultation non autorisée de sorties OOS doit être traitée comme contamination selon SOP 10 et comme incident de biais selon SOP 13.
```

---

# 3. Modifications dans `/Implementation`

## 3.1. Créer un module de gouvernance

### Type de modification

`/Implementation`

### Dossier à créer

```text
/Implementation/ebta_engine/governance/
```

Si l'arborescence exacte diffère, adapter au style actuel du repo sans casser les imports existants.

### Fichiers à créer

```text
/Implementation/ebta_engine/governance/__init__.py
/Implementation/ebta_engine/governance/bias_risk_schema.json
/Implementation/ebta_engine/governance/incident_schema.json
/Implementation/ebta_engine/governance/bias_registry.py
/Implementation/ebta_engine/governance/incident_logger.py
/Implementation/ebta_engine/governance/preregistration_checker.py
/Implementation/ebta_engine/governance/candidate_family_checker.py
/Implementation/ebta_engine/governance/registry_completeness_checker.py
/Implementation/ebta_engine/governance/metric_lock_checker.py
/Implementation/ebta_engine/governance/robustness_gate_checker.py
/Implementation/ebta_engine/governance/oos_access_guard.py
/Implementation/ebta_engine/governance/bias_gate.py
```

---

## 3.2. Créer `bias_risk_schema.json`

### Type de modification

`/Implementation`

### Objectif

Définir le schéma machine des biais connus.

### Champs minimum

```json
{
  "bias_id": "BIAS-001",
  "name": "P-hacking",
  "description": "...",
  "phase": ["TRAIN", "TEST", "PRE_OOS", "OOS", "POST_OOS"],
  "default_severity": "LEVEL_2",
  "detectors": [],
  "controlled_artifacts": [],
  "impacted_gates": [],
  "corrective_procedure": "...",
  "sop_reference": "SOP 13"
}
```

---

## 3.3. Créer `incident_schema.json`

### Type de modification

`/Implementation`

### Objectif

Définir le format standard d'un incident de biais.

### Champs obligatoires

```json
{
  "incident_id": "BIAS-2026-0001",
  "timestamp": "2026-07-01T12:00:00+02:00",
  "project_id": "...",
  "research_family_id": "...",
  "candidate_id": "...",
  "fold_id": "...",
  "phase": "TEST_PRE_OOS",
  "bias_id": "BIAS-005",
  "bias_type": "ASSET_CHERRY_PICKING",
  "detected_by": "candidate_family_checker",
  "evidence_path": "...",
  "severity": "LEVEL_2",
  "oos_state": "SEALED",
  "decision": "BLOCK_OOS_AND_RECALCULATE_WRC",
  "reviewer": null,
  "status": "OPEN"
}
```

---

## 3.4. Créer `incident_logger.py`

### Type de modification

`/Implementation`

### Objectif

Logger les incidents dans un fichier append-only.

### Sortie attendue

```text
/Implementation/logs/INCIDENT_BIAS.jsonl
```

Si le repo possède déjà un dossier de logs ou d'artefacts, utiliser la convention existante.

### Comportement attendu

- append-only ;
- une ligne JSON par incident ;
- horodatage automatique ;
- interdiction de modifier silencieusement une ligne existante ;
- possibilité de charger tous les incidents ouverts ;
- possibilité de filtrer par `research_family_id`, `candidate_id`, `fold_id`, `severity`, `status`.

---

## 3.5. Créer `registry_completeness_checker.py`

### Type de modification

`/Implementation`

### Objectif

Détecter les runs, candidates ou artefacts manquants.

### Contrôles minimum

Le checker doit vérifier :

- tout run exécuté possède un `RUN_ID` ;
- tout run possède un `CANDIDATE_ID` ;
- tout run possède un `config_hash` ;
- tout run possède un `code_hash` ;
- tout run possède un `data_hash` ;
- les runs échoués ou interrompus sont conservés ;
- les candidates perdantes ne sont pas absentes du registre ;
- le nombre de candidates dans le registre correspond au nombre de candidates dans la matrice de test statistique.

### Incident à créer en cas d'échec

```text
BIAS-006 — Suppression de candidates perdantes
BIAS-002 — Data snooping
BIAS-004 — Cherry-picking de candidates
```

Selon le cas détecté.

---

## 3.6. Créer `candidate_family_checker.py`

### Type de modification

`/Implementation`

### Objectif

Vérifier que la famille statistique utilisée pour WRC/MCP correspond à toutes les candidates influentes.

### Contrôles minimum

- comparer `candidate_registry` avec `statistical_family_matrix` ;
- vérifier que chaque couple `strategy × asset` sélectionnable est représenté ;
- vérifier que les actifs perdants n'ont pas été retirés après observation ;
- vérifier que les variantes de paramètres testées sont incluses ;
- vérifier que la matrice WRC/MCP ne contient pas seulement la gagnante.

### Incident à créer en cas d'échec

```text
BIAS-004 — Cherry-picking de candidates
BIAS-005 — Cherry-picking d'actifs
BIAS-006 — Suppression de candidates perdantes
```

---

## 3.7. Créer `metric_lock_checker.py`

### Type de modification

`/Implementation`

### Objectif

Empêcher les changements opportunistes de métrique, hurdle, coût ou benchmark.

### Contrôles minimum

Comparer la configuration préenregistrée avec la configuration exécutée :

- `primary_metric` ;
- `secondary_metrics` ;
- `economic_hurdle` ;
- `benchmark` ;
- `cost_model` ;
- `slippage_model` ;
- `execution_assumptions`.

### Règle

Si une variable décisionnelle a changé après observation des résultats, le gate doit échouer.

### Incident à créer en cas d'échec

```text
BIAS-007 — Metric shopping
BIAS-008 — Benchmark shopping
BIAS-009 — Hurdle shopping
BIAS-019 — Sélection opportuniste de coûts
```

---

## 3.8. Créer `robustness_gate_checker.py`

### Type de modification

`/Implementation`

### Objectif

Empêcher l'utilisation opportuniste des stress-tests.

### Contrôles minimum

- vérifier que les stress-tests décisionnels étaient prévus avant leur usage ;
- vérifier que tous les stress-tests obligatoires ont été exécutés ;
- vérifier qu'aucun stress-test défavorable n'a été supprimé ;
- vérifier qu'un stress-test ajouté après observation est taggé `diagnostic_only` ;
- vérifier que la robustesse ne sert pas à sélectionner une nouvelle variante non déclarée.

### Incident à créer en cas d'échec

```text
BIAS-010 — Robustness shopping
BIAS-011 — Stress-test réparateur
BIAS-012 — Exclusion post-hoc d'outliers
```

---

## 3.9. Créer `oos_access_guard.py`

### Type de modification

`/Implementation`

### Objectif

Contrôler l'ouverture de l'OOS.

### Règle centrale

L'OOS ne doit être ouvert que si tous les gates pré-OOS sont satisfaits, y compris `G-BIAS`.

### Contrôles minimum avant ouverture OOS

- paquet pré-OOS scellé ;
- hash du code gelé ;
- hash des données gelé ;
- config gelée ;
- WRC/MCP passé ;
- robustesse passée ;
- registre complet ;
- aucun incident ouvert de niveau 2 ou supérieur ;
- reviewer indépendant enregistré ;
- statut OOS différent de `BURNED`.

### Incident à créer en cas d'accès non autorisé

```text
BIAS-014 — OOS peeking
BIAS-015 — OOS repair
BIAS-017 — Retest déguisé
BIAS-020 — Contamination par agent IA
```

---

## 3.10. Créer `bias_gate.py`

### Type de modification

`/Implementation`

### Objectif

Centraliser le verdict `G-BIAS`.

### Entrées attendues

```text
candidate_registry
statistical_family_matrix
preregistration_manifest
robustness_matrix
oos_access_log
incident_log
reviewer_report
```

### Sortie attendue

```json
{
  "gate": "G-BIAS",
  "status": "PASS",
  "blocking_incidents": [],
  "warnings": [],
  "checked_artifacts": [],
  "timestamp": "..."
}
```

### Statuts possibles

```text
PASS
FAIL
INCONCLUSIVE
BURNED
```

### Règles de décision

```text
PASS : aucun incident bloquant, artefacts complets, revue indépendante OK.
INCONCLUSIVE : artefact manquant ou preuve insuffisante sans contamination OOS prouvée.
FAIL : biais pré-OOS matériel ou famille statistique invalide.
BURNED : OOS consulté, influencé ou contaminé avant autorisation.
```

---

# 4. Tests à ajouter

## 4.1. Type de modification

`/Implementation`

## 4.2. Dossier recommandé

```text
/Implementation/tests/governance/
```

Adapter au style existant si un dossier de tests existe déjà.

## 4.3. Tests minimum

Créer des tests unitaires ou d'intégration couvrant :

```text
test_bias_gate_pass_when_all_artifacts_valid.py
test_bias_gate_fails_when_candidate_missing.py
test_bias_gate_fails_when_asset_removed.py
test_bias_gate_fails_when_primary_metric_changed.py
test_bias_gate_inconclusive_when_artifact_missing.py
test_oos_guard_blocks_if_incident_open.py
test_oos_guard_marks_burned_on_unauthorized_access.py
test_incident_logger_is_append_only.py
test_robustness_checker_detects_removed_stress_test.py
test_registry_checker_detects_unlogged_run.py
```

---

# 5. Procédures correctives à implémenter

## 5.1. Type de modification

`/Protocole` et `/Implementation`

## 5.2. Niveaux de gravité

Implémenter cette classification dans la documentation et dans les statuts machine :

```text
LEVEL_0 — Écart documentaire mineur
LEVEL_1 — Écart technique pré-OOS sans effet décisionnel
LEVEL_2 — Écart pré-OOS influençant la recherche
LEVEL_3 — Échec post-OOS non réparateur
LEVEL_4 — Contamination OOS grave
LEVEL_5 — Invalidité méthodologique irréparable
```

## 5.3. Actions par niveau

### LEVEL_0

```text
Action : correction documentaire.
OOS : non impacté.
Statut possible : DOCUMENTARY_FIX.
```

### LEVEL_1

```text
Action : correction technique avec preuve que signaux, positions, métriques et gates ne changent pas.
OOS : non impacté si preuve suffisante.
Statut possible : TECHNICAL_FIX_PRE_OOS.
```

### LEVEL_2

```text
Action : blocage de l'OOS, recalcul de la famille statistique, WRC/MCP à rejouer.
OOS : reste scellé.
Statut possible : PRE_OOS_REPAIR_ALLOWED ou INCONCLUSIVE.
```

### LEVEL_3

```text
Action : archivage du verdict, post-mortem uniquement exploratoire.
OOS : utilisé, non réparable.
Statut possible : NOT_VALIDATED, FAIL, REJECTED_ECONOMIC ou INCONCLUSIVE.
```

### LEVEL_4

```text
Action : OOS marqué BURNED, famille contaminée, confirmation future obligatoire.
OOS : brûlé pour toute version influencée.
Statut possible : BURNED.
```

### LEVEL_5

```text
Action : invalidation méthodologique, retrait de la validation, audit indépendant requis.
OOS : inutilisable pour les descendants influencés.
Statut possible : FAIL.
```

---

# 6. Ordre d'implémentation recommandé

## Phase 1 — Audit de l'existant

### Type de modification

Aucune modification directe au départ.

### Action

Inspecter :

```text
/Protocole/PROTOCOLE EBTA.md
/Protocole/SOP 03*
/Protocole/SOP 05*
/Protocole/SOP 10*
/Protocole/SOP 12*
/Implementation/
```

### Objectif

Identifier :

- les conventions de nommage ;
- les structures de registre déjà existantes ;
- les éventuels schémas JSON existants ;
- les dossiers de tests ;
- les conventions d'artefacts ;
- les modules déjà responsables des gates.

### Résultat audit IA — 2026-07-01

Statut : `DONE_READ_ONLY`.

Constats principaux :

- Le protocole EBTA couvre déjà plusieurs risques anti-biais de façon distribuée : WRC sur famille complète, registre append-only, non-réduction ex post des candidates ou actifs, métrique/hurdle/coût préenregistrés, robustesse pré-OOS, contamination OOS et statut `BURNED`.
- Aucun fichier actif `Protocole/SOP 13 - Gouvernance des biais humains et incidents méthodologiques.md` n'existe.
- Aucun `Protocole/BIAS_RISK_REGISTER.md` actif n'existe.
- Aucun gate transversal `G-BIAS` n'existe dans la table G0-G14 du protocole principal.
- Aucun module `Implementation/ebta_engine/governance/` n'existe.
- Aucun fichier `Implementation/logs/INCIDENT_BIAS.jsonl` n'existe.
- Le runtime possède déjà des briques proches : `validators/gate_validator.py`, `validators/registry_append_only_validator.py`, `validators/invariant_validator.py`, `procedures/candidate_matrix.py`, `procedures/robustness.py`, `procedures/oos_access.py`, `schemas/oos_access_event.schema.json`, fixtures et tests sous `Implementation/ebta_engine/tests/`.
- Les tests runtime existants sont centralisés sous `Implementation/ebta_engine/tests/`, pas sous `Implementation/tests/governance/`. Toute future implémentation doit suivre cette convention sauf décision contraire.

Conclusion de contrôle :

- Les phases 2 à 7 du présent plan introduisent une nouvelle autorité transversale, un nouveau gate et une taxonomie d'incidents. Elles sont donc `NORMATIVE_CHANGE_REQUIRED`.
- Aucune modification `Protocole/` ni `Implementation/` ne doit être faite avant décision explicite ouvrant une nouvelle version documentaire ou autorisant le périmètre exact du changement.
- La prochaine action sûre est de préparer un paquet de décision normative : impacts SOP, positionnement de `G-BIAS` dans G0-G14, statut de `SOP 13`, et règles de compatibilité runtime.

### Paquet de décision normative — 2026-07-01

Statut : `READY_FOR_HUMAN_DECISION`.

#### Décision à prendre

Faut-il ouvrir une nouvelle version documentaire `EBTA-DOC-1.1` pour intégrer une gouvernance explicite des biais humains sous forme de `SOP 13`, registre `BIAS_RISK_REGISTER`, templates d'incidents/dérogations, gate transversal `G-BIAS`, puis implémentation runtime subordonnée ?

#### Options

| Option | Décision | Conséquence |
| --- | --- | --- |
| A | Ouvrir `EBTA-DOC-1.1` et intégrer `SOP 13` + `G-BIAS`. | Changement normatif complet, cohérent avec le gel documentaire. Nécessite mise à jour du protocole principal, registre normatif, matrice de cohérence, historique, manifeste, puis runtime. |
| B | Ne pas créer `SOP 13`; seulement renforcer `Implementation/` avec des checkers dérivés des SOP 02/03/05/08/10/12. | Implémentation possible uniquement si aucun nouveau gate, statut, seuil, taxonomie ou verdict n'est créé. `G-BIAS`, `BIAS-*` et `LEVEL_*` doivent alors être retirés ou traités comme diagnostics non normatifs. |
| C | Rejeter ou différer le chantier. | Aucun changement ; les contrôles anti-biais restent distribués dans EBTA-DOC-1.0. |

#### Recommandation IA

Option A, mais en deux lots stricts :

1. Lot documentaire `EBTA-DOC-1.1` : créer la norme et ses propriétaires.
2. Lot runtime : encoder uniquement ce qui a été validé dans `Protocole/`.

Raison : le brouillon introduit un nouveau gate transversal, de nouveaux statuts de gravité, un registre de risques et une procédure d'incident. Les coder directement dans `Implementation/` créerait une source de vérité concurrente.

#### Positionnement proposé de `G-BIAS`

`G-BIAS` ne doit pas remplacer G0-G14. Il doit être défini comme gate transversal avec deux points de contrôle obligatoires :

- avant `G8 - Ouverture OOS`, pour bloquer toute ouverture si un incident pré-OOS matériel reste ouvert ;
- avant `G11 - Validation reproductible`, pour empêcher qu'une recherche contaminée, réparée ou cherry-pickée devienne confirmatoire.

Conséquence documentaire : `PROTOCOLE EBTA.md` doit expliquer que `G-BIAS` traverse G0-G14 sans devenir une nouvelle chaîne concurrente.

#### SOP impactées

| Fichier | Impact si Option A |
| --- | --- |
| `PROTOCOLE EBTA.md` | Ajouter la section transversale, référencer `SOP 13`, insérer `G-BIAS` dans la logique des gates sans casser l'ordre G0-G14. |
| `REGISTRE DES DECISIONS NORMATIVES EBTA.md` | Ajouter les décisions normatives propriétaires : définition d'un incident de biais, obligation de revue, positionnement de `G-BIAS`, gravités et conséquences. |
| `MATRICE DE COHERENCE DES SOP EBTA.md` | Ajouter le thème transversal "gouvernance des biais humains" et vérifier les dépendances SOP 02/03/05/08/10/12/13. |
| `MANIFESTE DE GEL EBTA.md` | Recalculer les hashes et figer `EBTA-DOC-1.1` après modification. |
| `HISTORIQUE DES VERSIONS EBTA.md` | Journaliser l'ouverture et la clôture de `EBTA-DOC-1.1`. |
| `SOP 03` | Renvoi léger pour candidates/runs/familles manquants. |
| `SOP 05` | Renvoi léger pour robustness shopping et stress-tests réparateurs. |
| `SOP 08` | Renvoi léger pour metric, hurdle, benchmark et cost shopping. |
| `SOP 10` | Renvoi léger pour OOS peeking, OOS repair, retest déguisé et contamination IA. |
| `SOP 12` | Renvoi léger pour paquet reproductible, incidents, audit et conservation. |

#### Impact runtime après décision

Si Option A est validée, l'ordre runtime recommandé est :

1. Créer les schémas `bias_risk_schema.json` et `incident_schema.json`.
2. Créer un logger append-only d'incidents.
3. Encoder les checkers en s'appuyant sur les modules existants : registre, famille candidate, robustesse, accès OOS, gates.
4. Ajouter `bias_gate.py` seulement après stabilisation des schémas.
5. Ajouter les tests sous `Implementation/ebta_engine/tests/`, conformément à la convention actuelle.
6. Rerun non-divergence après chaque lot : `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`.

#### Décision humaine minimale attendue

Pour autoriser la Phase 2, répondre explicitement avec l'une des formes suivantes :

```text
GO Option A — ouvrir EBTA-DOC-1.1 pour SOP 13 + G-BIAS
GO Option B — runtime diagnostic seulement, sans nouvelle norme
NO GO — différer ou rejeter le chantier
```

---

## Phase 2 — Documentation protocolaire

### Type de modification

`/Protocole`

### Actions

1. Créer SOP 13.
2. Créer `BIAS_RISK_REGISTER.md`.
3. Créer les deux templates.
4. Modifier légèrement le protocole principal.
5. Ajouter des renvois légers dans SOP 03, SOP 05, SOP 10, SOP 12.

### Critère d'acceptation

La documentation doit permettre à un humain de comprendre :

- quel biais est détecté ;
- pourquoi il est grave ;
- quel gate il bloque ;
- quelle procédure corrective appliquer ;
- si l'OOS reste utilisable ou non.

---

## Phase 3 — Schémas machine

### Type de modification

`/Implementation`

### Actions

1. Créer `bias_risk_schema.json`.
2. Créer `incident_schema.json`.
3. Créer ou adapter les fixtures de test.

### Critère d'acceptation

Un incident doit pouvoir être validé automatiquement contre le schéma.

---

## Phase 4 — Logger d'incidents

### Type de modification

`/Implementation`

### Actions

1. Créer `incident_logger.py`.
2. Gérer l'append-only JSONL.
3. Ajouter lecture, filtrage et validation.
4. Ajouter tests unitaires.

### Critère d'acceptation

Un incident ne peut pas être perdu silencieusement.

---

## Phase 5 — Checkers pré-OOS

### Type de modification

`/Implementation`

### Actions

Implémenter :

```text
registry_completeness_checker.py
candidate_family_checker.py
metric_lock_checker.py
robustness_gate_checker.py
```

### Critère d'acceptation

Les checkers doivent détecter au minimum :

- candidate manquante ;
- actif retiré ;
- métrique changée ;
- stress-test retiré ;
- run non loggé.

---

## Phase 6 — Guard OOS

### Type de modification

`/Implementation`

### Actions

1. Créer `oos_access_guard.py`.
2. Brancher le guard avant tout accès aux données OOS.
3. Bloquer l'accès si un gate pré-OOS est incomplet.
4. Marquer `BURNED` en cas d'accès non autorisé.

### Critère d'acceptation

Aucun script ou notebook ne doit pouvoir ouvrir l'OOS sans passer par le guard.

---

## Phase 7 — Gate transversal G-BIAS

### Type de modification

`/Implementation`

### Actions

1. Créer `bias_gate.py`.
2. Agréger les résultats des checkers.
3. Produire un verdict `PASS / FAIL / INCONCLUSIVE / BURNED`.
4. Exporter un rapport machine lisible.

### Critère d'acceptation

Le protocole doit pouvoir bloquer l'ouverture OOS ou la validation finale si `G-BIAS` n'est pas `PASS`.

---

## Phase 8 — Tests et non-régression

### Type de modification

`/Implementation`

### Actions

1. Ajouter les tests de gouvernance.
2. Vérifier que les imports existants ne cassent pas.
3. Vérifier que les anciens workflows restent exécutables tant que `G-BIAS` n'est pas explicitement activé.
4. Ajouter une option de compatibilité si nécessaire :

```text
EBTA_ENABLE_BIAS_GOVERNANCE=true/false
```

### Critère d'acceptation

Les tests existants et nouveaux passent.

---

# 7. Critères d'acceptation globaux

Le travail est terminé uniquement si :

```text
[x] SOP 13 existe.
[x] BIAS_RISK_REGISTER.md existe.
[x] Les templates d'incident et de dérogation existent.
[x] PROTOCOLE EBTA.md référence G-BIAS.
[x] SOP 03, 05, 10, 12 référencent SOP 13 si pertinent.
[x] Le module /Implementation/ebta_engine/governance/ existe.
[x] Les schémas JSON existent.
[x] Le logger d'incidents fonctionne en append-only.
[x] Les checkers pré-OOS existent.
[x] Le guard OOS existe.
[x] Le gate G-BIAS existe.
[x] Les tests de gouvernance existent.
[x] Un incident de biais peut bloquer l'OOS.
[x] Un accès OOS non autorisé peut produire un statut BURNED.
[x] Une candidate manquante peut produire FAIL ou INCONCLUSIVE.
[x] Une métrique changée après résultat peut produire FAIL.
[x] La documentation distingue clairement correction pré-OOS et contamination post-OOS.
```

---

# 8. Règles importantes pour Codex

Ne pas inventer de chemins si le repo possède déjà une convention claire.

Inspecter l'arborescence avant d'ajouter les fichiers.

Respecter le style Markdown existant dans `/Protocole`.

Respecter le style Python existant dans `/Implementation`.

Ne pas supprimer de contenu existant sans justification explicite.

Préférer des ajouts minimaux, traçables et compatibles avec l'existant.

Tout changement de protocole doit rester aligné avec :

- préenregistrement ;
- registre exhaustif ;
- correction data-mining bias ;
- ouverture unique OOS ;
- non-réparation post-OOS ;
- reproductibilité indépendante ;
- distinction exploration / confirmation.

---

# 9. Résultat attendu final

À la fin, fournir dans la réponse Codex :

```text
1. Liste des fichiers créés.
2. Liste des fichiers modifiés.
3. Résumé des changements /Protocole.
4. Résumé des changements /Implementation.
5. Tests ajoutés.
6. Tests exécutés.
7. Points non résolus ou hypothèses prises.
8. Risques restants.
```

---

# 10. Principe directeur

La gouvernance des biais humains ne doit pas être décorative.

Elle doit empêcher techniquement le chercheur, même de bonne foi, de transformer une recherche exploratoire, contaminée, réparée ou cherry-pickée en preuve confirmatoire.

---

## Résultat Option A — 2026-07-01

Statut : `DOCUMENTATION_DONE_RUNTIME_PENDING`

Lot documentaire `EBTA-DOC-1.1` ouvert et gelé.

### Fait dans `/Protocole`

- [x] `SOP 13 - Gouvernance des biais humains et incidents méthodologiques.md` créé.
- [x] `BIAS_RISK_REGISTER.md` créé.
- [x] `TEMPLATE - Incident de biais EBTA.md` créé.
- [x] `TEMPLATE - Dérogation méthodologique EBTA.md` créé.
- [x] `PROTOCOLE EBTA.md` référence `G-BIAS` comme gate transversal sans renuméroter `G0` à `G14`.
- [x] `REGISTRE DES DECISIONS NORMATIVES EBTA.md` ajoute DN-042 à DN-047.
- [x] `MATRICE DE COHERENCE DES SOP EBTA.md` intègre SOP 13 comme propriétaire de la gouvernance biais.
- [x] `PAQUET D'EXECUTION EBTA.md` ajoute les artefacts et invariants `G-BIAS`.
- [x] SOP 03, SOP 05, SOP 08, SOP 10 et SOP 12 référencent SOP 13 là où elles consomment la gouvernance biais.
- [x] `HISTORIQUE DES VERSIONS EBTA.md` documente `EBTA-DOC-1.1`.
- [x] `MANIFESTE DE GEL EBTA.md` est recalculé avec les nouveaux hashes.

### Validations exécutées

```text
PASS python -m unittest Implementation.ebta_engine.tests.test_protocol_manifest_hashes
PASS python -m json.tool .ai\checkpoint.json
PASS python -c "import json, jsonschema; jsonschema.validate(...)"
PASS git diff --check -- Protocole .ai
PASS python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
```

### Reste à faire

- [x] Phase 2 runtime : créer `Implementation/ebta_engine/governance/`.
- [x] Créer les schémas machine-readable incidents/risques.
- [x] Créer le logger append-only d'incidents.
- [x] Créer les checkers pré-OOS et le guard OOS.
- [x] Créer le gate runtime `G-BIAS`.
- [x] Ajouter les tests de gouvernance runtime.

## Résultat runtime Phase 3/4 — 2026-07-01

Statut : `SCHEMAS_AND_INCIDENT_LOGGER_DONE_CHECKERS_PENDING`

### Fait dans `/Implementation`

- [x] `Implementation/ebta_engine/governance/__init__.py` créé.
- [x] `Implementation/ebta_engine/governance/bias_risk_schema.json` créé.
- [x] `Implementation/ebta_engine/governance/incident_schema.json` créé.
- [x] `Implementation/ebta_engine/governance/bias_registry.py` créé avec les 20 biais `BIAS-001` à `BIAS-020`.
- [x] `Implementation/ebta_engine/governance/incident_logger.py` créé avec append-only JSONL, validation, chargement, filtrage et incidents ouverts.
- [x] `Implementation/ebta_engine/__init__.py` aligne le runtime avec `EBTA-DOC-1.1`.
- [x] `Implementation/TRACEABILITY_MATRIX.md` trace le socle `G-BIAS`.
- [x] `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` journalise le lot.

### Tests ajoutés

- [x] `Implementation/ebta_engine/tests/test_governance_bias.py`

### Validations exécutées

```text
PASS python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_governance_bias.py
```

### Reste à faire côté runtime

- [x] Créer `registry_completeness_checker.py`.
- [x] Créer `candidate_family_checker.py`.
- [x] Créer `metric_lock_checker.py`.
- [x] Créer `robustness_gate_checker.py`.
- [x] Créer `oos_access_guard.py`.
- [x] Créer `bias_gate.py`.
- [x] Brancher `G-BIAS` dans les validations de paquet avec compatibilité descendante.

## Résultat runtime Phase 5/6/7/8 — 2026-07-01

Statut : `G_BIAS_RUNTIME_DONE`

### Fait dans `/Implementation`

- [x] `preregistration_checker.py` compare les champs décisionnels préenregistrés et exécutés.
- [x] `registry_completeness_checker.py` détecte runs, candidates et hashes manquants.
- [x] `candidate_family_checker.py` vérifie la famille statistique complète et l'axe stratégie x actif.
- [x] `metric_lock_checker.py` bloque les changements de métrique, hurdle, benchmark, coûts et hypothèses d'exécution.
- [x] `robustness_gate_checker.py` détecte stress-tests retirés, ajoutés décisionnellement ou utilisés pour resélection.
- [x] `oos_access_guard.py` refuse l'ouverture OOS sans `G-BIAS` PASS et marque `BURNED` en cas d'accès non autorisé.
- [x] `bias_gate.py` agrège les preuves en `PASS / FAIL / INCONCLUSIVE / BURNED`.
- [x] `validators/package_validator.py` lit `reports/g_bias.json` et échoue si le rapport présent ou enforcé n'est pas `PASS`.
- [x] Le pilote minimal génère `reports/g_bias.json` et exige `bias_gate_pass` avant autorisation OOS.

### Tests ajoutés ou étendus

- [x] `test_governance_bias.py` couvre PASS, FAIL candidate manquante, FAIL actif retiré, FAIL métrique changée, INCONCLUSIVE artefact manquant, OOS guard bloquant, BURNED, append-only, robustesse retirée et run non loggé.
- [x] `test_package_validator.py` couvre `reports/g_bias.json` présent en FAIL et enforcement sans rapport.
- [x] `test_procedure_governance.py` couvre l'autorisation OOS uniquement après `bias_gate_pass`.

### Validations exécutées

```text
PASS python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_governance_bias.py — 20 tests
PASS python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_package_validator.py — 6 tests
PASS python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_procedure_governance.py — 8 tests
PASS python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation — 87 tests
PASS python Implementation\examples\minimal_pilot_pipeline\build_research_package.py — package status PASS
```

### Conclusion

L'annexe `PLAN_IMPLEMENTATION_GOUVERNANCE_BIAIS_EBTA` est complète côté documentation et runtime. Le mainline reste `STEP_3_BACKTRADER_INTEGRATION`, à reprendre uniquement après lecture de la gouvernance BACKTRADER.
