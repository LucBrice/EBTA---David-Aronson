# Registre des décisions normatives EBTA
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - REGISTRE_NORMATIF |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | Gouvernance protocole EBTA |
| Rôle dans le paquet EBTA | Index central des decisions figees, proprietaires documentaires, preuves et moments de preenregistrement. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

Date de création : 2026-06-24

## Objet

Ce registre centralise les décisions méthodologiques figées dans les SOP EBTA.
Il sert d’index normatif entre :

- les SOP 01 à 12 ;
- la matrice de cohérence transversale ;
- le futur template de configuration préenregistrée ;
- la mise à jour ultérieure du protocole principal.

Une règle ne doit pas être redéfinie indépendamment dans plusieurs documents.
Chaque SOP conserve son autorité dans son domaine, mais ce registre indique le
document propriétaire et les documents consommateurs.

---

## Règles de lecture

| Champ | Sens |
| --- | --- |
| `Fixe` | Décision méthodologique générale du protocole EBTA. Toute modification crée une nouvelle version du protocole. |
| `Configurable` | Valeur propre à une recherche, famille ou marché. Elle doit être préenregistrée avant l’étape indiquée. |
| `Procédural` | Règle déterministe dont la sortie dépend des données et artefacts gelés. |
| `Preuve attendue` | Artefact minimal permettant à un reviewer de reconstruire ou vérifier la décision. |

---

## Taxonomie globale des statuts

| Famille | Statuts | Propriétaire | Sens normatif |
| --- | --- | --- | --- |
| Verdicts de validation | `PASS`, `NOT_VALIDATED`, `REJECTED_ECONOMIC`, `FAIL`, `INCONCLUSIVE` | SOP 01, SOP 08, SOP 10 | Décision globale sur la validité statistique, économique et méthodologique du processus. |
| Gate Test local | `PASS`, `FAIL`, `INCONCLUSIVE` | SOP 02 | Autorise ou interdit l’exposition du fold suivant à `OOS_k`. |
| Registre et intégrité | `PASS`, `FAIL`, `INCONCLUSIVE` | SOP 03 | Contrôle l’opposabilité de l’effort de recherche et des matrices. |
| Politique locale de fold | `NO_MODEL`, `STOP_PROCESS` | SOP 04, SOP 06 | Sorties procédurales en absence de candidate admissible. |
| Gate économique | `PASS`, `REJECTED_ECONOMIC`, `INCONCLUSIVE` | SOP 08, SOP 09B | Évalue la performance économique réelle, séparée du gate statistique. |
| Incident technique OOS | `INVALID_TECHNICAL` | SOP 10 | Marque une estimation OOS techniquement invalide sans restaurer automatiquement la virginité OOS. |
| Monitoring | `WATCH`, `PASS`, `FAIL`, `INCONCLUSIVE` | SOP 11 | Surveille le processus validé en incubation/live ; ne remplace pas le verdict de validation. |
| Stades du paquet | `PRE_OOS_SEALED`, `VALIDATION_READY`, `DEPLOYMENT_CERTIFIED`, `LIFECYCLE_ARCHIVED` | SOP 12 | États immuables du paquet de preuve et de son cycle de vie. |

---

## Décisions normatives

| ID | Sujet | Valeur ou règle retenue | SOP propriétaire | SOP concernées | Justification | Nature | Moment du préenregistrement | Preuve attendue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DN-001 | Architecture de validation | EBTA utilise un Walk-Forward avec segments `OOS_k` successifs, non chevauchants, concaténés en un unique OOS global. | SOP 04 | SOP 01, 02, 05, 06, 08, 10, 12 | Évite le holdout final opportuniste et conserve une chronologie reconstructible. | Fixe | Avant création du paquet `PRE_OOS_SEALED`. | Calendrier des folds, manifeste SOP 04, paquet SOP 12. |
| DN-002 | Absence de holdout final supplémentaire | Aucun quatrième segment ni holdout final historique n’est ajouté après l’OOS Walk-Forward global. | SOP 01 | SOP 04, 05, 06, 10 | Empêche une seconde validation discrétionnaire après consommation de l’OOS. | Fixe | Avant la première recherche EBTA. | Protocole versionné, configuration des folds. |
| DN-003 | Fonctions Train/Test/OOS | `Train_k` calibre, `Test_k` sélectionne et infère, `OOS_k` estime passivement le processus gelé. | SOP 04 | SOP 02, 06, 07, 09A, 10 | Sépare apprentissage, sélection et estimation confirmatoire. | Fixe | Avant accès à `Train_k`. | Manifeste de fold, logs d’accès aux données. |
| DN-004 | Point d’arrêt informationnel | Le verdict OOS global est calculé au point d’arrêt préenregistré ; des folds futurs ne peuvent être ajoutés que selon une règle indépendante des résultats observés. | SOP 01 | SOP 04, 10 | Évite l’arrêt opportuniste sur significativité ou performance. | Configurable | Avant première ouverture OOS. | Plan d’analyse OOS, calendrier, justification de puissance. |
| DN-005 | Identité d’une candidate | Une candidate est une spécification exécutable unique ayant produit une information de performance exploitable ou sélectionnable. | SOP 03 | SOP 02, 05, 06, 09B, 12 | Rend opposable l’effort réel de recherche. | Fixe | Avant première évaluation exploitable. | Registre append-only, représentation canonique, `candidate_id`. |
| DN-006 | Déduplication des candidates | La déduplication n’est admise qu’ex ante par procédure automatique préenregistrée ; aucune fusion rétrospective ne réduit l’univers statistique. | SOP 03 | SOP 02, 06, 12 | Empêche la réduction opportuniste du nombre de tests. | Fixe | Avant exécution des candidates. | Algorithme de déduplication, logs et hashes. |
| DN-007 | Famille de recherche | La famille inclut toutes les candidates dont les résultats ont pu influencer une même décision sur des données de sélection partagées. | SOP 03 | SOP 02, 05, 06, 12 | Définit la population opposable pour l’inférence multiple. | Fixe | Avant WRC local. | `RESEARCH_FAMILY_ID`, catalogue, matrice scellée. |
| DN-008 | Population testée par WRC | Le WRC local porte sur l’univers complet et reconstructible des candidates applicables à `Test_k`. | SOP 02 | SOP 03, 06, 12 | Corrige le biais de data mining lié à la sélection de la meilleure règle. | Fixe | Avant exécution du WRC local. | Matrice `Test_k`, hash du catalogue, rapport WRC. |
| DN-009 | Test confirmatoire Test | Le test confirmatoire primaire sur `Test_k` est White’s Reality Check au niveau unilatéral `alpha = 0,05`. | SOP 02 | SOP 06, 10 | Fournit le gate corrigé de recherche multiple avant OOS. | Fixe | Avant accès à `Test_k`. | Plan statistique, rapport WRC, seed bootstrap. |
| DN-010 | Rôle SPA | Hansen SPA est une analyse secondaire de sensibilité ; il ne renverse pas un WRC primaire `FAIL` ou `INCONCLUSIVE`. | SOP 02 | SOP 06, 10 | Préserve l’autorité du gate confirmatoire primaire. | Fixe | Avant WRC local. | Rapport SPA lié au rapport WRC. |
| DN-011 | Rôle Romano-Wolf | Romano-Wolf identifie des candidates individuelles après rejet global, sans autoriser un choix post hoc non préenregistré. | SOP 02 | SOP 06 | Évite de transformer l’identification multiple en nouvelle sélection discrétionnaire. | Fixe | Avant WRC local. | Rapport Romano-Wolf, règle de transmission. |
| DN-012 | Candidate transmise à OOS | Après WRC local `PASS`, seule la candidate désignée par la règle de sélection préenregistrée est transmise à `OOS_k`. | SOP 06 | SOP 02, 04, 10 | L’OOS ne sélectionne, ne départage et ne répare jamais un modèle. | Procédural | Avant accès à `Test_k`. | `selected_candidate_id`, règle de sélection, logs de gel. |
| DN-013 | Absence de modèle | Si aucune candidate admissible n’existe, la politique `NO_MODEL` ou `STOP_PROCESS` préenregistrée s’applique mécaniquement. | SOP 04 | SOP 06, 08, 10, 11 | Empêche de forcer une candidate non admissible. | Configurable | Avant exécution du fold. | Configuration de fold, statut appliqué, série de cash/non-déploiement. |
| DN-014 | Série statistique primaire | L’unité primaire est la série quotidienne complète des log-rendements nets detrendés du portefeuille. | SOP 08 | SOP 01, 02, 07, 12 | Maintient une unité temporelle commune et évite les moyennes de ratios de folds. | Fixe | Avant première estimation statistique. | Série quotidienne, dictionnaire de colonnes, réconciliation NAV. |
| DN-015 | Jours sans exposition | Tous les jours, y compris `NO_MODEL`, WRC `FAIL`, WRC `INCONCLUSIVE` et périodes sans exposition, restent dans la chronologie. | SOP 08 | SOP 01, 02, 04, 06, 10 | Préserve l’objet OOS global et évite l’exclusion opportuniste de périodes défavorables. | Fixe | Avant premier fold OOS. | Série quotidienne complète, calendrier, justification des jours. |
| DN-016 | Detrending | Le detrending retire le drift excédentaire du marché pondéré par exposition, uniquement dans le flux d’évaluation. | SOP 07 | SOP 01, 02, 08 | Mesure l’alpha de timing/sélection sans contaminer les signaux. | Fixe | Avant calcul de la série primaire. | Série detrendée, formule, benchmark/cash, contrôles numériques. |
| DN-017 | Flux signal vs flux évaluation | Les signaux, positions, sizing et ordres sont produits à partir de données point-in-time non detrendées. | SOP 07 | SOP 09A, 09B | Empêche le look-ahead et l’usage du detrending comme feature. | Fixe | Avant génération des signaux. | Logs de pipeline, hash de features, contrôles anti-leakage. |
| DN-018 | Zero-centering | Le zero-centering sert uniquement à construire `H0` dans le bootstrap conjoint des candidates ; il n’est jamais appliqué à l’estimation OOS. | SOP 07 | SOP 02, 01 | Distingue la simulation de l’hypothèse nulle de l’estimation de performance. | Fixe | Avant WRC local. | Paramètres bootstrap, matrices centrées, rapport WRC. |
| DN-019 | Gate statistique OOS | Le gate statistique OOS porte sur l’espérance nette detrendée, avec borne inférieure unilatérale à 95 %. | SOP 01 | SOP 08, 10 | Transforme l’OOS en estimation confirmatoire préenregistrée, pas en nouvelle sélection. | Fixe | Avant première ouverture OOS. | Rapport OOS, intervalle, code d’estimation. |
| DN-020 | Bootstrap OOS | L’IC OOS utilise un bootstrap stationnaire par blocs sur la série OOS concaténée, distinct de la distribution WRC Test. | SOP 01 | SOP 02, 04, 08 | Corrige la réutilisation invalide de la distribution WRC pour l’OOS. | Fixe | Avant première ouverture OOS. | Paramètres bootstrap, seed, réplications, rapport d’IC. |
| DN-021 | Puissance cible OOS | L’analyse OOS exige une puissance cible minimale de 80 % selon le plan préenregistré. | SOP 01 | SOP 04, 10 | Évite de conclure avec une taille informationnelle insuffisante. | Fixe | Avant première ouverture OOS. | Calcul de puissance, MDE, point d’arrêt. |
| DN-022 | Nombre de réplications OOS | Le plan OOS utilise 5 000 réplications bootstrap, sauf si une version future du protocole modifie explicitement cette valeur. | SOP 01 | SOP 12 | Assure une précision numérique minimale reproductible. | Fixe | Avant estimation OOS. | Configuration statistique, seed, logs. |
| DN-023 | Gate économique séparé | Le gate économique est distinct du gate statistique et porte sur la NAV réelle nette, les coûts, le risque, la capacité et l’exécutabilité. | SOP 08 | SOP 01, 09B, 10, 11 | Un succès statistique ne compense pas un échec économique, et inversement. | Fixe + seuils configurables | Avant première ouverture OOS. | Rapport économique, seuils, réconciliation NAV. |
| DN-024 | Hurdle économique | Les seuils économiques bloquants sont préenregistrés par recherche et ne peuvent pas être remplacés après observation par des métriques favorables. | SOP 08 | SOP 01, 05, 09B, 10 | Évite le cherry-picking de métriques secondaires. | Configurable | Avant Test/OOS selon le gate concerné. | Template de configuration, rapport de performance. |
| DN-025 | Données point-in-time | Toute valeur utilisée par une décision doit avoir été disponible opérationnellement avant cette décision, après publication, latence, ingestion et validation. | SOP 09A | SOP 03, 04, 06, 07, 08, 10, 12 | Empêche leakage, survivorship bias et vintage bias. | Fixe | Avant consommation de données. | Snapshots, horodatages, latences, contrôles anti-leakage. |
| DN-026 | Transformations apprises | Toute transformation dépendante des données est fit exclusivement sur `Train_k` puis appliquée à `Test_k` et `OOS_k`. | SOP 09A | SOP 06, 07 | Empêche apprentissage implicite sur Test/OOS. | Fixe | Avant fitting des transformations. | Logs de fit, paramètres gelés, hash de pipeline. |
| DN-027 | Purge et embargo | La purge couvre les dépendances aux frontières ; l’embargo ne traite que les dépendances résiduelles justifiées et préspécifiées. | SOP 04 | SOP 09A | Évite les fuites temporelles entre segments. | Configurable | Avant calendrier Walk-Forward. | Configuration de splits, justification, audit anti-leakage. |
| DN-028 | Modèle central d’exécution | Le scénario central doit représenter une exécution réellement tradable avec prix exécutables, coûts, impact, financement, FX, borrow, sizing et contraintes. | SOP 09B | SOP 05, 08, 10, 11 | Évite que la performance statistique repose sur un P&L non négociable. | Configurable | Avant Test et OOS. | Journal signal-ordre-fill-position-P&L, modèle de coûts, capacité. |
| DN-029 | Capacité et sizing | Le capital cible ne peut dépasser le plus grand niveau où tous les gates restent satisfaits sur la grille de capacité préenregistrée. | SOP 09B | SOP 08, 11 | Empêche le passage live au-delà de la capacité démontrée. | Configurable | Avant gate économique et live. | Grille de capitaux, rapport de capacité, limites de live. |
| DN-030 | Robustesse décisionnelle | Les stress-tests décisionnels sont préenregistrés et exécutés avant l’ouverture de chaque `OOS_k`. | SOP 05 | SOP 03, 06, 09B, 10 | Évite que l’OOS devienne un ensemble de sélection par robustesse post hoc. | Configurable | Avant ouverture de l’`OOS_k` concerné. | Plan de robustesse, matrice, verdicts, preuves. |
| DN-031 | Analyses post-OOS | Après observation OOS, les analyses de robustesse sont descriptives et ne donnent droit à aucune réparation, reselection ou seconde tentative sur les mêmes données. | SOP 05 | SOP 10, 11 | Protège la virginité consommée de l’OOS. | Fixe | Avant ouverture OOS. | Journal d’observation, rapport descriptif, décision archivée. |
| DN-032 | Gate d’ouverture OOS | L’ouverture d’un `OOS_k` exige WRC local `PASS`, gates pré-OOS satisfaits, candidate/processus gelés, données validées, exécution/capacité vérifiée et paquet `PRE_OOS_SEALED`. | SOP 10 | SOP 02, 05, 06, 09A, 09B, 12 | Ordonne les dépendances avant consommation du holdout fonctionnel. | Fixe | Avant chaque ouverture `OOS_k`. | Checklist d’ouverture, journal d’accès, manifeste `PRE_OOS_SEALED`. |
| DN-033 | Réexécution même-OOS | Une réexécution sur le même OOS n’est admise que pour une erreur technique objective, minimale, indépendante de la performance et documentée. | SOP 10 | SOP 05, 09A, 09B, 12 | Empêche de transformer un échec en nouvelle tentative déguisée. | Fixe | Avant toute correction post-OOS. | Post-mortem, preuve d’erreur, diff minimal, nouvelle version. |
| DN-034 | Nouvelle candidate après modification | Toute modification de logique alpha, données décisionnelles, exécution ou sizing influente crée une nouvelle candidate ou version nécessitant des observations futures. | SOP 03 | SOP 05, 06, 09A, 09B, 10, 11 | Maintient la traçabilité et empêche la restauration fictive de l’OOS. | Fixe | Au moment de la modification. | Événement de registre, lineage, nouvelle version. |
| DN-035 | Incubation | Seul un processus `PASS` statistique, économique, robustesse, exécution/capacité et reproduction peut entrer en incubation confirmatoire. | SOP 11 | SOP 01, 05, 08, 09B, 10, 12 | L’incubation vérifie prospectivement l’opérationnel ; elle ne répare pas l’alpha. | Fixe + critères configurables | Avant démarrage paper trading. | Dossier `VALIDATION_READY`, plan d’incubation, approbations. |
| DN-036 | Passage live limité | Le live commence à capital limité et progresse par paliers fondés sur risque, capacité et conformité opérationnelle. | SOP 11 | SOP 09B, 12 | Réduit le risque de déploiement et respecte la capacité validée. | Configurable | Avant `DEPLOYMENT_CERTIFIED`. | Plan de live, limites, kill switch, monitoring. |
| DN-037 | Monitoring statistique | Le monitoring statistique suit un calendrier ou une procédure séquentielle préenregistrée contrôlant les consultations répétées. | SOP 11 | SOP 10, 12 | Évite les alarmes opportunistes ou les tests répétés non contrôlés. | Configurable | Avant live. | Plan de monitoring, règles d’alerte, logs. |
| DN-038 | Paquet `PRE_OOS_SEALED` | Le paquet `PRE_OOS_SEALED` est obligatoire avant tout accès OOS. | SOP 12 | SOP 10 | Assure que intention, code, données, configuration et candidates sont gelés avant consommation OOS. | Fixe | Avant ouverture `OOS_k`. | Manifeste, checksums, registre, configuration. |
| DN-039 | Paquet `VALIDATION_READY` | Le stade `VALIDATION_READY` est obligatoire avant incubation et exige séries OOS, verdicts, gates et reproduction indépendante `PASS`. | SOP 12 | SOP 11 | Empêche l’incubation sans paquet reproductible. | Fixe | Avant paper trading. | Manifeste `VALIDATION_READY`, rapport de reproduction. |
| DN-040 | Paquet `DEPLOYMENT_CERTIFIED` | Le stade `DEPLOYMENT_CERTIFIED` est obligatoire avant live limité et ajoute paper trading `PASS`, version live, limites, sizing, kill switch et monitoring. | SOP 12 | SOP 11 | Lie le passage live à une version opérationnelle exacte. | Fixe | Avant live limité. | Manifeste `DEPLOYMENT_CERTIFIED`, approbation live. |
| DN-041 | Conservation et archivage | Les versions, runs perdants, erreurs, accès OOS, décisions et journaux sont conservés au moins dix ans après retrait. | SOP 12 | SOP 03, 10, 11 | Permet audit indépendant et reconstruction historique. | Fixe | Dès création du paquet. | Archive, checksums, politique de rétention. |

---

## Paramètres à reporter dans le template de configuration

Ces éléments ne doivent pas être figés dans le protocole principal comme valeurs
universelles. Ils doivent être fournis par recherche ou famille de recherche.

| Paramètre | SOP propriétaire | Moment minimal de préenregistrement |
| --- | --- | --- |
| Univers, actifs, période et calendrier | SOP 04, SOP 09A | Avant création des splits. |
| Fréquence de données et calendrier de sessions | SOP 04, SOP 08 | Avant calcul des séries. |
| Fenêtres `Train_k`, `Test_k`, `OOS_k` | SOP 04 | Avant premier fold. |
| Nombre minimal de folds et point d’arrêt informationnel | SOP 01, SOP 04 | Avant première ouverture OOS. |
| Purge et embargo | SOP 04, SOP 09A | Avant création des splits. |
| Benchmark, cash et conventions multidevises | SOP 07, SOP 08 | Avant calcul des rendements. |
| Hurdle économique et effet minimal détectable | SOP 01, SOP 08 | Avant gate OOS. |
| Coûts, slippage, impact, borrow, financement et FX | SOP 09B | Avant Test/OOS. |
| Grille de capacité et sizing | SOP 09B | Avant gate économique et live. |
| Scénarios de robustesse et seuils bloquants | SOP 05 | Avant ouverture `OOS_k`. |
| Seeds, réplications et longueurs de blocs si non fixées par SOP | SOP 01, SOP 02, SOP 12 | Avant calcul statistique. |
| Critères d’incubation, suspension, kill switch et monitoring | SOP 11 | Avant incubation/live. |

---

## Points à corriger ou surveiller

| Point | Statut | Action |
| --- | --- | --- |
| Statut SOP 01 | `CLOSED` | Harmonisé en spécification normative. |
| Statut SOP 02 | `CLOSED` | Ligne de statut normative ajoutée. |
| Statut SOP 03 | `CLOSED` | Ligne de statut normative ajoutée. |
| Doublons série primaire / detrending | `CLOSED_FOR_DOCUMENTATION` | Le propriétaire est fixé ici ; le protocole principal référence les propriétaires sans recopier les formules. |
| Taxonomie globale des statuts | `CLOSED_FOR_PROTOCOL_DRAFT` | La table de taxonomie de ce registre doit être reprise comme index du protocole principal ou artefact opérationnel. |
| Template de configuration | `CLOSED` | `Protocole/TEMPLATE - Configuration préenregistrée d'une recherche EBTA.md` créé. |
| Mise à jour du protocole principal | `CLOSED` | `Protocole/PROTOCOLE EBTA.md` révisé comme carte du processus et index des SOP. |
| Clôture de l’audit méthodologique | `CLOSED_WITH_DEFERRED_IMPLEMENTATION` | Audit mis à jour avec statuts par constat ; les artefacts exécutables restent à produire. |
| Paquet d’exécution documentaire | `CLOSED_WITH_DEFERRED_IMPLEMENTATION` | `Protocole/PAQUET D'EXECUTION EBTA.md` créé ; scripts et schémas machine-readable restent à implémenter. |
| Revue finale et gel documentaire | `CLOSED` | Version documentaire `EBTA-DOC-1.0` gelée dans `Protocole/MANIFESTE DE GEL EBTA.md`. |

---

## Prochaine étape

Ouvrir une nouvelle version documentaire pour toute évolution méthodologique
future. La prochaine phase non documentaire est l’implémentation machine-readable
du paquet d’exécution.
