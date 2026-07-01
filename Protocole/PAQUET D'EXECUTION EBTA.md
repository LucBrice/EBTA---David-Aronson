# Paquet d'exécution EBTA
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SPECIFICATION_OPERATIONNELLE |
| Version documentaire | EBTA-DOC-1.1 |
| Date de gel documentaire | 2026-07-01 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | Gouvernance protocole EBTA |
| Rôle dans le paquet EBTA | Definition des formulaires, checklists, schemas, rapports, journaux, manifeste et invariants a implementer. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

Version documentaire : 2026-07-01

## Fonction du paquet

Ce document transforme les SOP EBTA en contrôles opérationnels utilisables avant
implémentation logicielle complète.

Il définit :

- les formulaires à remplir ;
- les checklists de gate ;
- les schémas minimaux de configuration et de registre ;
- les formats de rapports ;
- le journal d’accès OOS ;
- le manifeste de reproductibilité ;
- les invariants méthodologiques à automatiser.

Les scripts, formulaires machine-readable et tests automatisés effectifs restent
à produire dans une phase d’implémentation dédiée.

---

## 1. Formulaires obligatoires

| Formulaire | Moment | Source normative | Fichier / emplacement |
| --- | --- | --- | --- |
| Configuration préenregistrée | Avant recherche et avant `PRE_OOS_SEALED` | Registre normatif, SOP 04, SOP 12 | `Protocole/TEMPLATE - Configuration préenregistrée d'une recherche EBTA.md` |
| Hypothèse et portée | Avant accès aux données de recherche | SOP 03 | Section 1 du template |
| Déclaration de données point-in-time | Avant splits et features | SOP 09A | Section 2 du template |
| Déclaration Walk-Forward | Avant premier fold | SOP 04 | Section 3 du template |
| Espace de recherche et candidates | Avant première évaluation exploitable | SOP 03, SOP 06 | Section 4 du template |
| Modèle d’exécution | Avant Test/OOS | SOP 09B | Section 8 du template |
| Plan de robustesse | Avant ouverture `OOS_k` | SOP 05 | Section 10 du template |
| Incident de biais | Dès détection d'un biais ou d'une contamination potentielle | SOP 13 | `Protocole/TEMPLATE - Incident de biais EBTA.md` |
| Dérogation méthodologique | Avant la décision affectée et avant usage de l'exception | SOP 13 | `Protocole/TEMPLATE - Dérogation méthodologique EBTA.md` |
| Plan d’incubation/live | Avant `VALIDATION_READY` / `DEPLOYMENT_CERTIFIED` | SOP 11 | Section 13 du template |

---

## 2. Checklists de gate

### G0 - Préenregistrement

- [ ] `CONFIG_ID`, `PROJECT_ID`, `RESEARCH_FAMILY_ID`, `HYPOTHESIS_ID` et `PROCESS_VERSION_ID` définis.
- [ ] Hypothèse falsifiable écrite.
- [ ] Univers, période, calendrier et fréquence définis.
- [ ] Folds, purge, embargo et point d’arrêt informationnel définis.
- [ ] Espace de recherche, budget, seeds et règle d’arrêt définis.
- [ ] Métrique primaire, hurdle économique et MDE définis.
- [ ] Modèle d’exécution central défini.
- [ ] Plan de robustesse défini.
- [ ] Template hashé et référencé dans le registre.

### G1 - Données point-in-time

- [ ] Snapshots de données identifiés et hashés.
- [ ] Horodatages de publication, ingestion et disponibilité présents.
- [ ] Survivorship, delisting et corporate actions couverts.
- [ ] Données macro, fondamentales ou alternatives versionnées par vintage.
- [ ] Transformations apprises limitées à `Train_k`.
- [ ] Purge et embargo cohérents avec les dépendances.
- [ ] Contrôles anti-leakage exécutés et archivés.

### G2 - Registre et candidates

- [ ] Registre append-only initialisé.
- [ ] Famille de recherche créée.
- [ ] Candidates et spécifications planifiées distinguées.
- [ ] Déduplication ex ante documentée.
- [ ] Runs interrompus ou échoués enregistrés.
- [ ] Matrice locale complète produite.
- [ ] Revue indépendante du registre effectuée.

### G3 - Sélection locale

- [ ] Paramètres calibrés uniquement sur `Train_k`.
- [ ] Candidates représentatives construites selon la règle prévue.
- [ ] Transfert `Train_k -> Test_k` mécanique.
- [ ] Maximum Test ou règle de sélection appliqué sans intervention discrétionnaire.
- [ ] Candidate transmise identifiée.
- [ ] Aucune candidate influente omise.

### G4 - Inférence multiple Test

- [ ] Famille complète applicable incluse dans la matrice.
- [ ] WRC local exécuté au seuil préenregistré.
- [ ] Bootstrap conjoint et zero-centered.
- [ ] SPA / Romano-Wolf / MCPM exécutés si prévus.
- [ ] `PASS`, `FAIL` ou `INCONCLUSIVE` attribué.
- [ ] OOS non ouvert si WRC local non `PASS`.

### G5 - Robustesse pré-OOS

- [ ] Socle commun de stress-tests exécuté.
- [ ] Tests conditionnels exécutés ou justifiés non applicables.
- [ ] Scénarios `CENTRAL`, `PLAUSIBLE_BASE` et `EXTREME` classés.
- [ ] Variantes influentes enregistrées.
- [ ] Matrice de robustesse scellée.
- [ ] Verdict pré-OOS produit avant ouverture `OOS_k`.

### G6 - Exécution, coûts, capacité et sizing

- [ ] Chaîne signal -> ordre -> fill -> position -> P&L reconstructible.
- [ ] Coûts, spreads, impact, borrow, financement et FX appliqués.
- [ ] NAV réconciliée.
- [ ] Grille de capacité calculée.
- [ ] Capital cible inférieur ou égal au capital validé.
- [ ] Rejets, partial fills et opportunités manquées journalisés.

### G7 - Paquet `PRE_OOS_SEALED`

- [ ] Hypothèse, configuration, registre, données, code et environnement présents.
- [ ] Candidate, matrice et rapports Test présents.
- [ ] Modèle d’exécution et robustesse présents.
- [ ] Seeds, versions et hashes présents.
- [ ] Aucun accès OOS antérieur non déclaré.
- [ ] Reviewer indépendant approuve le paquet.
- [ ] Checklist `G-BIAS` initiale jointe.

### G8 - Ouverture OOS

- [ ] `G-BIAS` évalué `PASS` par reviewer indépendant.
- [ ] Aucun incident `LEVEL_2` ou supérieur non résolu.
- [ ] Registre des risques de biais revu.
- [ ] Journal d’accès OOS initialisé.
- [ ] Autorisation d’ouverture signée.
- [ ] Accès horodaté.
- [ ] Exécution OOS lancée une seule fois.
- [ ] Aucun paramètre, code, sizing ou règle de décision modifié après ouverture.

### G9 - Estimation OOS globale

- [ ] Tous les `OOS_k` autorisés sont inclus dans la série concaténée.
- [ ] Jours sans exposition et `NO_MODEL` conservés.
- [ ] Série primaire detrendée reconstructible.
- [ ] Bootstrap OOS distinct du WRC Test.
- [ ] Puissance et point d’arrêt vérifiés.
- [ ] Gate statistique global attribué.

### G10 - Gate économique

- [ ] NAV réelle nette réconciliée.
- [ ] Hurdles économiques appliqués.
- [ ] Coûts, capacité et exécutabilité vérifiés.
- [ ] `REJECTED_ECONOMIC` utilisé si le statistique est `PASS` mais l’économie échoue.
- [ ] Gate statistique et gate économique publiés séparément.

### G11 - `VALIDATION_READY`

- [ ] Rapport OOS complet.
- [ ] Rapport économique complet.
- [ ] Rapport de robustesse complet.
- [ ] Paquet `G-BIAS` complet, incidents et dérogations inclus.
- [ ] Reproduction indépendante niveau requis `PASS`.
- [ ] Paquet `VALIDATION_READY` hashé.
- [ ] Approbation d’incubation présente.

### G12 - Incubation

- [ ] Processus gelé déployé en paper trading.
- [ ] Données, signaux, ordres, fills, coûts et risques vérifiés prospectivement.
- [ ] Aucune réparation alpha effectuée.
- [ ] Monitoring opérationnel actif.
- [ ] Monitoring statistique préenregistré respecté.

### G13 - `DEPLOYMENT_CERTIFIED`

- [ ] Paper trading `PASS`.
- [ ] Version live exacte identifiée.
- [ ] Limites, sizing, capital initial et kill switch définis.
- [ ] Monitoring live versionné.
- [ ] Approbation de déploiement signée.

### G14 - Cycle de vie et archive

- [ ] Incidents et changements d’état journalisés.
- [ ] Incidents de biais et dérogations réconciliés.
- [ ] Suspensions, reprises et retraits documentés.
- [ ] Paquet `LIFECYCLE_ARCHIVED` produit si applicable.
- [ ] Conservation minimale respectée.

---

## 3. Schémas minimaux

### 3.1 Configuration

Champs minimaux :

- `config_id`
- `project_id`
- `research_family_id`
- `hypothesis_id`
- `process_version_id`
- `protocol_version`
- `data_snapshots`
- `walk_forward_schedule`
- `candidate_space`
- `selection_rule`
- `statistical_plan`
- `execution_model`
- `robustness_plan`
- `oos_opening_gate`
- `incubation_plan`
- `reproducibility_manifest`
- `document_hash`

### 3.2 Registre des expériences

Champs minimaux :

- `event_id`
- `timestamp`
- `actor`
- `event_type`
- `project_id`
- `research_family_id`
- `candidate_id`
- `run_id`
- `fold_id`
- `data_snapshot_id`
- `input_hashes`
- `output_hashes`
- `decision_status`
- `evidence_path`
- `parent_event_id`
- `chain_hash`

### 3.3 Journal d’accès OOS

Champs minimaux :

- `access_event_id`
- `timestamp`
- `actor`
- `fold_id`
- `oos_segment_id`
- `pre_oos_package_hash`
- `opening_authorization_id`
- `access_reason`
- `command_or_process_id`
- `read_paths`
- `write_paths`
- `result_artifact_hash`
- `incident_flag`
- `reviewer`

### 3.4 Incident de biais

Champs minimaux :

- `incident_id`
- `timestamp`
- `actor_or_tool`
- `bias_category`
- `severity_level`
- `affected_gate`
- `affected_artifacts`
- `information_exposure`
- `impact_assessment`
- `immediate_action`
- `reviewer`
- `gbias_status`
- `evidence_path`
- `evidence_hash`

### 3.5 Dérogation méthodologique

Champs minimaux :

- `derogation_id`
- `timestamp`
- `requested_exception`
- `objective_constraint`
- `affected_gate`
- `documented_before_decision`
- `independent_of_observed_result`
- `no_oos_repair_effect`
- `reviewer`
- `decision`
- `conditions`
- `expiration`
- `registry_event_id`

---

## 4. Formats de rapports

| Rapport | Sections minimales |
| --- | --- |
| Rapport WRC local | Famille testée, matrice, méthode bootstrap, seuil, p-value, verdict, candidate transmise, hashes. |
| Rapport de robustesse | Plan, scénarios, données utilisées, seuils, résultats, verdict, variantes influentes, preuves. |
| Rapport OOS | Série OOS concaténée, méthode d’IC, puissance, point d’arrêt, verdict statistique, limitations. |
| Rapport économique | NAV, coûts, risques, capacité, sizing, hurdles, verdict économique. |
| Rapport d’exécution | Ordres, fills, positions, frictions, rejets, partial fills, réconciliation. |
| Rapport d’incubation | Données live/paper, signaux, exécution, coûts, risques, incidents, verdict. |
| Rapport de reproduction | Environnement, données, code, commandes, résultats attendus, tolérances, verdict. |
| Rapport `G-BIAS` | Registre de risques revu, incidents, dérogations, exposition d'information, impact, reviewer, verdict. |

---

## 5. Manifeste de reproductibilité

Champs obligatoires :

- identité projet / hypothèse / famille / version ;
- version du protocole et des SOP ;
- configuration gelée et hash ;
- données et snapshots ;
- code, dépendances et environnement ;
- seeds et paramètres d’aléatoire ;
- calendrier Walk-Forward ;
- registre des candidates ;
- matrices Test et OOS ;
- rapports de gates ;
- logs d’exécution ;
- logs d’accès OOS ;
- incidents de biais, dérogations et décisions `G-BIAS` ;
- reviewers et approbations ;
- hashes de tous les artefacts.

---

## 6. Invariants méthodologiques à automatiser

| ID | Invariant | Statut si violation |
| --- | --- | --- |
| INV-001 | Aucun `OOS_k` ne chevauche un autre `OOS_k`. | `FAIL` |
| INV-002 | Aucun accès OOS avant paquet `PRE_OOS_SEALED`. | `FAIL` |
| INV-003 | Aucun `OOS_k` ouvert après WRC local non `PASS`. | `FAIL` |
| INV-004 | Toute candidate influente apparaît dans le registre. | `FAIL` ou `INCONCLUSIVE` |
| INV-005 | La matrice WRC contient la famille complète applicable. | `FAIL` |
| INV-006 | Les transformations apprises sont fit uniquement sur `Train_k`. | `FAIL` |
| INV-007 | Les timestamps de disponibilité précèdent les décisions qui les utilisent. | `FAIL` |
| INV-008 | Les jours `NO_MODEL` et sans exposition restent dans la série OOS. | `FAIL` |
| INV-009 | Le bootstrap OOS ne réutilise pas la distribution WRC Test. | `FAIL` |
| INV-010 | Le gate économique ne remplace pas le gate statistique. | `FAIL` |
| INV-011 | Aucune robustesse décisionnelle n’utilise un OOS déjà observé. | `FAIL` |
| INV-012 | Toute réexécution même-OOS possède un post-mortem SOP 10. | `FAIL` |
| INV-013 | Toute modification influente crée une nouvelle candidate ou version. | `FAIL` |
| INV-014 | Le paquet `VALIDATION_READY` précède l’incubation. | `FAIL` |
| INV-015 | Le paquet `DEPLOYMENT_CERTIFIED` précède le live limité. | `FAIL` |
| INV-016 | Les hashes référencés dans le manifeste correspondent aux artefacts présents. | `FAIL` |
| INV-017 | Aucun `G8` n'est ouvert sans `G-BIAS PASS`. | `FAIL` |
| INV-018 | Aucun `G11` n'est validé avec incident `LEVEL_2` ou supérieur non résolu. | `FAIL` |
| INV-019 | Toute dérogation est antérieure à la décision affectée et non réparatrice. | `FAIL` |

---

## 7. Prochaine phase d’implémentation

Pour rendre ce paquet machine-readable, créer ensuite :

- un schéma JSON de configuration ;
- un schéma JSONL du registre append-only ;
- un schéma JSONL du journal d’accès OOS ;
- un schéma JSONL des incidents de biais ;
- un schéma JSON des dérogations méthodologiques ;
- un générateur de manifeste ;
- un validateur d’invariants ;
- des tests automatisés intégrés au pipeline de recherche.

Ces artefacts doivent être développés contre une implémentation concrète du
pipeline EBTA afin d’éviter des contrôles abstraits non exécutables.
