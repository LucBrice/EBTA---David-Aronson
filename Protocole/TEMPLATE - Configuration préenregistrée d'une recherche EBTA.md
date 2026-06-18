# TEMPLATE - Configuration préenregistrée d'une recherche EBTA
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - TEMPLATE_CONFIG |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | Gouvernance protocole EBTA |
| Rôle dans le paquet EBTA | Template remplissable pour les parametres preregistres propres a une recherche EBTA. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

Version du template : 2026-06-24

## Fonction du document

Ce template fixe les paramètres propres à une recherche EBTA avant leur
utilisation. Il complète les SOP sans les redéfinir.

À remplir avant l’exécution d’une recherche, puis à sceller dans le paquet
`PRE_OOS_SEALED` selon la SOP 12.

---

## 0. Statut de la configuration

| Champ | Valeur |
| --- | --- |
| `CONFIG_ID` |  |
| `PROJECT_ID` |  |
| `RESEARCH_FAMILY_ID` |  |
| `HYPOTHESIS_ID` |  |
| `PROCESS_VERSION_ID` |  |
| Version du protocole EBTA |  |
| Date de création |  |
| Date de gel |  |
| Statut | ACTIF - TEMPLATE_CONFIG |
| Auteur |  |
| Reviewer indépendant |  |
| Emplacement du paquet `PRE_OOS_SEALED` |  |
| Hash du document gelé |  |

Conditions de gel :

- [ ] Toutes les sections applicables sont remplies.
- [ ] Les sections non applicables sont justifiées.
- [ ] Les valeurs configurables ont été fixées avant consultation des résultats concernés.
- [ ] Le document est référencé dans le registre SOP 03.
- [ ] Le hash est inclus dans le paquet SOP 12.

---

## 1. Hypothèse et portée

| Champ | Valeur |
| --- | --- |
| Hypothèse économique testée |  |
| Classe de stratégie |  |
| Marchés / instruments |  |
| Devise de base du portefeuille |  |
| Sens autorisés | Long / Short / Long-Short |
| Horizon de détention cible |  |
| Fréquence de décision |  |
| Fréquence de marquage à marché |  |
| Objectif de généralisation | `ASSET_SPECIFIC` / `CROSS_SECTIONAL` / autre |
| Contraintes réglementaires ou opérationnelles |  |

Non-objectifs et exclusions :

- [ ] Exclusions d’actifs documentées.
- [ ] Exclusions de périodes documentées.
- [ ] Exclusions de types d’ordres documentées.
- [ ] Limites de généralisation documentées.

---

## 2. Univers, données et disponibilité point-in-time

| Champ | Valeur |
| --- | --- |
| Fournisseurs de données |  |
| Types de données | Prix / Volume / Corporate actions / Fondamentaux / Macro / Alternatives / Autre |
| Début de période disponible |  |
| Fin de période disponible |  |
| Calendrier de marché utilisé |  |
| Fuseau horaire de référence |  |
| Politique de survivorship bias |  |
| Données de delisting |  |
| Corporate actions |  |
| Latence de publication |  |
| Latence d’ingestion |  |
| Règle de disponibilité opérationnelle |  |
| Identifiants de snapshots |  |
| Hashes des snapshots |  |

Contrôles SOP 09A :

- [ ] Chaque valeur décisionnelle possède un timestamp de disponibilité.
- [ ] Les données alternatives ou fondamentales ont une vintage reconstructible.
- [ ] Les corrections de données créent un nouveau snapshot.
- [ ] Les transformations apprises sont fit exclusivement sur `Train_k`.
- [ ] Les contrôles anti-leakage sont définis avant exécution.

---

## 3. Segmentation Walk-Forward

| Champ | Valeur |
| --- | --- |
| Architecture | Rolling / Expanding / autre |
| Nombre minimal de folds |  |
| Règle de création des folds |  |
| Taille de `Train_k` |  |
| Taille de `Test_k` |  |
| Taille de `OOS_k` |  |
| Pas de déplacement |  |
| Warm-up |  |
| Purge |  |
| Embargo |  |
| Justification purge / embargo |  |
| Politique absence de candidate | `NO_MODEL` / `STOP_PROCESS` |
| Point d’arrêt informationnel |  |
| Règle d’ajout de folds futurs |  |

Table des folds :

| Fold | `Train_k` | `Test_k` | `OOS_k` | Purge | Embargo | Statut prévu si aucune candidate |
| --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |

Contraintes :

- [ ] Les segments OOS ne se chevauchent pas.
- [ ] Aucun résultat `OOS_k` ne peut influencer les folds ultérieurs.
- [ ] Les folds ne seront pas traités comme observations IID sans justification.
- [ ] Le verdict global utilisera la série OOS concaténée.

---

## 4. Espace de recherche et candidates

| Champ | Valeur |
| --- | --- |
| Générateur de candidates |  |
| Familles de règles |  |
| Paramètres explorés |  |
| Grille ou méthode de recherche |  |
| Budget de recherche |  |
| Règle d’arrêt |  |
| Règle de déduplication ex ante |  |
| Règle de transfert `Train_k -> Test_k` |  |
| Règle de sélection sur `Test_k` |  |
| Gestion des égalités |  |
| Tolérances numériques |  |
| Seeds stochastiques |  |
| Politique ML / early stopping |  |

Obligations SOP 03 / SOP 06 :

- [ ] Toute candidate influente est enregistrée.
- [ ] Les candidates perdantes sont conservées.
- [ ] Les seeds sélectionnables sont traitées comme candidates distinctes.
- [ ] Les agrégations de seeds sont préspécifiées si elles existent.
- [ ] La famille complète applicable est transmise au WRC local.

---

## 5. Série de rendement, benchmark et cash

| Champ | Valeur |
| --- | --- |
| Unité statistique primaire | Log-rendement quotidien net detrendé du portefeuille |
| Source de NAV |  |
| Devise de base |  |
| Convention de cash |  |
| Taux cash accessible |  |
| Benchmark de marché |  |
| Benchmark institutionnel secondaire |  |
| Méthode de detrending | SOP 07 |
| Traitement des jours sans exposition | Conservés dans la série quotidienne |
| Traitement des périodes `NO_MODEL` |  |
| Tolérance de réconciliation NAV |  |

Rappels normatifs :

- [ ] Le cash est neutralisé dans le gate statistique.
- [ ] Le cash réel reste inclus dans le gate économique.
- [ ] Les signaux ne consomment jamais de données detrendées.
- [ ] Le zero-centering est réservé au bootstrap WRC, pas à l’OOS.
- [ ] Les métriques secondaires ne remplacent pas la métrique primaire.

---

## 6. Inférence multiple sur Test

| Champ | Valeur |
| --- | --- |
| Test confirmatoire primaire | White’s Reality Check |
| Seuil WRC primaire | `alpha = 0,05` unilatéral |
| Méthode bootstrap WRC |  |
| Longueur de blocs WRC |  |
| Nombre de réplications WRC |  |
| Seed WRC |  |
| SPA | Oui / Non |
| Romano-Wolf | Oui / Non |
| MCPM | Oui / Non |
| Critères `PASS` / `FAIL` / `INCONCLUSIVE` |  |

Preuves :

- [ ] Catalogue complet des candidates.
- [ ] Matrice locale `Test_k`.
- [ ] Hash de matrice.
- [ ] Rapport WRC.
- [ ] Rapport SPA / Romano-Wolf / MCPM si applicables.

---

## 7. Estimation OOS et puissance

| Champ | Valeur |
| --- | --- |
| Objet OOS global | Série quotidienne concaténée des `OOS_k` |
| Méthode d’IC OOS | Bootstrap stationnaire par blocs |
| Nombre de réplications OOS | 5 000 |
| Longueur de blocs OOS |  |
| Seed OOS |  |
| Borne confirmatoire | Borne inférieure unilatérale à 95 % |
| Effet minimal détectable |  |
| Puissance cible minimale | 80 % |
| Nombre minimal de blocs distincts |  |
| Règle `NOT_VALIDATED` |  |
| Règle `INCONCLUSIVE` |  |

Contraintes :

- [ ] La distribution WRC Test n’est pas réutilisée pour l’IC OOS.
- [ ] Le verdict OOS n’est calculé qu’au point d’arrêt prévu.
- [ ] Aucun résultat OOS ne modifie rétroactivement le processus.
- [ ] Les observations OOS déjà ouvertes restent consommées et archivées.

---

## 8. Modèle d’exécution, coûts, capacité et sizing

| Champ | Valeur |
| --- | --- |
| Types d’ordres autorisés |  |
| Règle signal -> ordre |  |
| Règle ordre -> fill |  |
| Prix exécutables utilisés |  |
| Commissions |  |
| Spreads |  |
| Slippage |  |
| Impact de marché |  |
| Borrow / short fees |  |
| Financement |  |
| FX |  |
| Marge et levier |  |
| Règle de sizing |  |
| Contraintes de turnover |  |
| Grille de capital testée |  |
| Capital cible demandé |  |
| Limites de capacité |  |

Preuves SOP 09B :

- [ ] Journal signal-ordre-fill-position-P&L.
- [ ] Réconciliation NAV.
- [ ] Rapport de coûts.
- [ ] Rapport de capacité.
- [ ] Justification du capital cible.

---

## 9. Gate économique

| Champ | Valeur |
| --- | --- |
| Hurdle de rendement net |  |
| Hurdle de drawdown |  |
| Hurdle de volatilité |  |
| Hurdle de liquidité / capacité |  |
| Hurdle de turnover |  |
| Hurdle de coûts |  |
| Statut si preuve économique insuffisante |  |
| Critère `REJECTED_ECONOMIC` |  |

Rappels :

- [ ] Le gate économique ne compense jamais un gate statistique non `PASS`.
- [ ] Le gate statistique ne compense jamais un échec économique.
- [ ] Les seuils sont définis avant observation du résultat concerné.

---

## 10. Robustesse pré-OOS

| Champ | Valeur |
| --- | --- |
| Socle commun de stress-tests |  |
| Tests conditionnels |  |
| Tests non applicables et justification |  |
| Seuils bloquants |  |
| Scénarios `CENTRAL` |  |
| Scénarios `PLAUSIBLE_BASE` |  |
| Scénarios `EXTREME` |  |
| Règle d’agrégation |  |
| Statut si données insuffisantes |  |

Stress-tests prévus :

| ID | Risque testé | Scénario | Données utilisées | Seuil | Bloquant ? | Preuve attendue |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

Contraintes :

- [ ] Les stress-tests décisionnels sont exécutés avant ouverture `OOS_k`.
- [ ] Aucune variante n’est choisie sur `OOS_k`.
- [ ] Les analyses post-OOS sont descriptives seulement.
- [ ] Toute variante influente est enregistrée dans la famille.

---

## 11. Gate d’ouverture OOS

Pour chaque `OOS_k`, cocher avant ouverture :

| Condition | SOP | Statut / preuve |
| --- | --- | --- |
| WRC local primaire `PASS` | SOP 02 |  |
| Candidate locale gelée | SOP 06 |  |
| Registre complet et scellé | SOP 03 |  |
| Données point-in-time validées | SOP 09A |  |
| Calendrier, purge, embargo conformes | SOP 04 |  |
| Série primaire reconstructible | SOP 07 / SOP 08 |  |
| Modèle d’exécution et capacité validés | SOP 09B |  |
| Robustesse pré-OOS `PASS` ou statut autorisé | SOP 05 |  |
| Paquet `PRE_OOS_SEALED` créé | SOP 12 |  |
| Journal d’accès OOS prêt | SOP 10 |  |

Décision d’ouverture :

| Fold | Ouverture autorisée ? | Date / heure | Reviewer | Hash du paquet |
| --- | --- | --- | --- | --- |
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |

---

## 12. Gestion des incidents et réexécutions

| Champ | Valeur |
| --- | --- |
| Politique de correction technique pré-OOS |  |
| Politique de correction technique post-OOS | SOP 10 |
| Critère d’erreur objective |  |
| Reviewer indépendant requis |  |
| Diff maximal autorisé |  |
| Preuves minimales |  |

Rappels :

- [ ] Une réexécution même-OOS n’est jamais automatique.
- [ ] L’erreur doit être indépendante de la performance observée.
- [ ] Tout changement de logique crée une nouvelle candidate ou version.
- [ ] L’OOS déjà ouvert ne redevient jamais vierge.

---

## 13. Incubation, live et monitoring

| Champ | Valeur |
| --- | --- |
| Critère d’entrée en incubation |  |
| Durée minimale de paper trading |  |
| Couverture minimale des régimes |  |
| Critères paper trading `PASS` |  |
| Critères paper trading `FAIL` |  |
| Critères paper trading `INCONCLUSIVE` |  |
| Capital initial live limité |  |
| Paliers de montée en capital |  |
| Kill switch opérationnel |  |
| Monitoring statistique |  |
| Calendrier des revues |  |
| Statut `WATCH` |  |
| Critères de suspension |  |
| Critères de retrait |  |

Contraintes :

- [ ] `NOT_VALIDATED`, `FAIL`, `REJECTED_ECONOMIC` et `INCONCLUSIVE` n’autorisent pas l’incubation confirmatoire.
- [ ] Le paper trading ne sert pas à réparer le modèle.
- [ ] Toute modification alpha repart en recherche.
- [ ] Le live exige le stade `DEPLOYMENT_CERTIFIED`.

---

## 14. Reproductibilité et paquet de preuve

| Stade SOP 12 | Condition d’obtention | Emplacement | Hash |
| --- | --- | --- | --- |
| `PRE_OOS_SEALED` | Avant tout accès OOS |  |  |
| `VALIDATION_READY` | Avant incubation |  |  |
| `DEPLOYMENT_CERTIFIED` | Avant live limité |  |  |
| `LIFECYCLE_ARCHIVED` | Conservation finale |  |  |

Artefacts minimaux :

- [ ] Configuration préenregistrée gelée.
- [ ] Registre SOP 03.
- [ ] Snapshots de données.
- [ ] Code et environnement.
- [ ] Seeds et paramètres d’aléatoire.
- [ ] Matrices Test et OOS.
- [ ] Rapports WRC / OOS / robustesse / économique.
- [ ] Journaux d’exécution et de capacité.
- [ ] Journaux d’accès OOS.
- [ ] Revues indépendantes.
- [ ] Checksums.

---

## 15. Signatures

| Rôle | Nom | Date | Signature / preuve |
| --- | --- | --- | --- |
| Chercheur responsable |  |  |  |
| Reviewer méthodologique |  |  |  |
| Reviewer données |  |  |  |
| Reviewer exécution / risque |  |  |  |
| Reviewer reproductibilité |  |  |  |

Décision de gel :

- [ ] La configuration est acceptée.
- [ ] La configuration est refusée.
- [ ] La configuration est acceptée sous conditions listées ci-dessous.

Conditions ou réserves :

| ID | Réserve | Responsable | Date limite | Statut |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

