# PROTOCOLE EBTA
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - PROTOCOLE_PRINCIPAL_GELE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | Gouvernance protocole EBTA |
| Rôle dans le paquet EBTA | Carte generale du processus, boucles de recherche, hooks de reprise, ordre des gates, livrables, gouvernance et index des SOP. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

Version documentaire : 2026-06-24

## 1. Fonction du protocole principal

Ce document est la carte générale du processus EBTA.

Il définit :

- l’ordre des gates ;
- les livrables obligatoires ;
- la gouvernance des décisions ;
- l’index des SOP applicables ;
- les interdictions qui protègent l’OOS, la reproductibilité et l’auditabilité.

Il ne recopie pas les détails techniques des SOP. En cas de divergence, la SOP
propriétaire indiquée dans ce protocole et dans le registre normatif prévaut.

Documents de référence internes :

- `Protocole/MATRICE DE COHERENCE DES SOP EBTA.md`
- `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md`
- `Protocole/TEMPLATE - Configuration préenregistrée d'une recherche EBTA.md`
- `Protocole/Archives/AUDIT METHODOLOGIQUE PROTOCOLE EBTA.md`
- `Protocole/Archives/HOOK - Finalisation du protocole EBTA après revue des SOP.md`

Pointeurs opérationnels subordonnés :

- `Implementation/Active/HOOK.md`
- `Implementation/GUIDE - Construire un pipeline de recherche EBTA.md`
- `Implementation/PROCEDURE_CALCULATION_MAP.md`
- `Implementation/TRACEABILITY_MATRIX.md`
- `Implementation/Active/tracking.json`

Ces pointeurs opérationnels expliquent comment le protocole gelé est traduit en
contrats exécutables. Ils ne créent aucune règle normative concurrente.

Référence méthodologique principale :

- David Aronson, *Evidence-Based Technical Analysis: Applying the Scientific Method and Statistical Inference to Trading Signals*.

---

## 2. Objectif EBTA

Le protocole EBTA transforme une recherche de stratégie de trading en processus :

- déterministe ;
- préenregistrable ;
- reproductible ;
- auditable ;
- protégé contre le data-mining bias, le surapprentissage, le leakage, la contamination OOS et la sélection opportuniste.

Le protocole valide un **processus de recherche et de sélection**, pas seulement
une règle isolée.

---

## 3. Architecture normative

### 3.1 Walk-Forward obligatoire

L’architecture principale EBTA est un Walk-Forward composé de folds successifs :

```text
Train_k -> Test_k + WRC_k -> gate pré-OOS -> OOS_k
```

Les segments `OOS_k` :

- sont successifs ;
- ne se chevauchent jamais ;
- sont ouverts une seule fois ;
- sont concaténés chronologiquement pour former l’unique OOS global.

Aucun holdout final supplémentaire n’est ajouté après l’OOS Walk-Forward global.

### 3.2 Rôle des segments

| Segment | Rôle | Propriétaire |
| --- | --- | --- |
| `Train_k` | Calibration, apprentissage, préparation des candidates et transformations apprises. | SOP 04, SOP 06, SOP 09A |
| `Test_k` | Sélection de complexité, matrice complète de candidates, inférence multiple locale. | SOP 02, SOP 06 |
| `OOS_k` | Exécution passive du processus gelé et contribution à l’OOS global. | SOP 01, SOP 04, SOP 10 |

L’OOS ne sélectionne, ne départage, ne répare et ne revalide jamais un modèle.

### 3.3 Carte processuelle complète

Le processus EBTA n’est pas une liste plate de contrôles. C’est une chaîne de
décisions, de preuves et de verrous. Le diagramme ci-dessous donne l’ordre. Le
tableau qui suit indique quelle SOP ouvrir pour comprendre chaque bloc.

```text
[P0] Intention de recherche
        |
        v
[P1] Configuration préenregistrée
     hypothèse, calendrier, seeds, gates
        |
        v
[P2] Données point-in-time
     purge, embargo, warm-up, anti-leakage
        |
        v
[P3] Folds Walk-Forward non chevauchants
     Train_k / Test_k / OOS_k
        |
        v
[P4] Boucle locale du fold k
     Train_k -> Test_k -> sélection locale -> WRC_k -> robustesse -> scellement
        |                                               |
        |                                               v
        |                              FAIL / INCONCLUSIVE / NO_MODEL
        |                                               |
        v                                               v
     gates pré-OOS satisfaits                    pas d'ouverture OOS_k
        |
        v
[P5] Ouverture unique et journalisée de OOS_k
        |
        v
[P6] Exécution passive du processus gelé sur OOS_k
        |
        v
[P7] Concaténation chronologique des OOS_k
        |
        v
[P8] Estimation OOS globale
     gate statistique + gate économique séparé
        |
        v
[P9] Paquet reproductible
     incubation -> déploiement limité -> cycle de vie
```

Chaque flèche implique une preuve opposable : configuration, registre, matrice
de candidates, rapport de gate, rapport WRC, manifeste, hash, journal d’accès ou
paquet de validation.

Lecture du diagramme :

| Bloc | Ce que le bloc veut dire | SOP propriétaires à ouvrir |
| --- | --- | --- |
| P0-P1 | Définir l’intention, préenregistrer l’hypothèse, le calendrier, les seeds, les gates et les règles d’arrêt. | SOP 03, SOP 04, SOP 12 |
| P2 | Prouver que les données et transformations étaient disponibles au moment de la décision. | SOP 09A, SOP 04 |
| P3 | Construire les fenêtres `Train_k`, `Test_k`, `OOS_k`, sans chevauchement OOS, avec purge, embargo et warm-up. | SOP 04 |
| P4 Train/Test | Calibrer sur `Train_k`, transférer mécaniquement vers `Test_k`, monter les niveaux de complexité et choisir la candidate locale. | SOP 06 |
| P4 Famille complète | Conserver l’univers complet des candidates influentes qui ont pu conduire à la sélection, y compris les couples `stratégie × actif` lorsque l’actif est sélectionnable. | SOP 03, SOP 06 |
| P4 WRC | Tester la famille complète applicable avec le WRC local primaire ; garder SPA, Romano-Wolf et MCPM comme analyses secondaires. | SOP 02 |
| P4 Robustesse | Exécuter les contrôles de robustesse pré-OOS sans utiliser l’OOS pour réparer. | SOP 05 |
| P4 Scellement | Geler le paquet pré-OOS avant toute ouverture de `OOS_k`. | SOP 10, SOP 12 |
| P5-P6 | Ouvrir `OOS_k` une seule fois et exécuter passivement le processus gelé, avec coûts, sizing, NAV et capacité. | SOP 08, SOP 09B, SOP 10 |
| P7-P8 | Concaténer les segments OOS et produire l’estimation statistique globale, séparée du gate économique. | SOP 01, SOP 04, SOP 08, SOP 09B |
| P9 | Produire le paquet reproductible, puis gouverner incubation, déploiement limité, monitoring et archivage. | SOP 11, SOP 12 |

### 3.4 Boucle locale Train/Test/OOS

Dans chaque fold, EBTA impose une boucle fermée :

```text
1. Construire Train_k, Test_k, OOS_k sans chevauchement.
   Autorité : SOP 04.
2. Apprendre uniquement sur Train_k.
   Autorité : SOP 06, SOP 09A.
3. Produire la famille complète des candidates applicables, incluant tout
   couple `stratégie × actif` évalué lorsque l’actif peut influencer la
   sélection.
   Autorité : SOP 03, SOP 06.
4. Sélectionner localement sur Test_k selon la règle préenregistrée.
   Autorité : SOP 06.
5. Tester la famille complète avec le WRC local primaire.
   Autorité : SOP 02.
6. Exécuter les contrôles de robustesse pré-OOS.
   Autorité : SOP 05.
7. Sceller le paquet PRE_OOS_SEALED.
   Autorité : SOP 10, SOP 12.
8. Ouvrir OOS_k une seule fois.
   Autorité : SOP 10.
9. Exécuter passivement la candidate gelée.
   Autorité : SOP 08, SOP 09B, SOP 10.
10. Conserver le segment dans la chronologie globale.
    Autorité : SOP 01, SOP 04.
```

Si la boucle échoue avant OOS, `OOS_k` n’est pas ouvert. Si elle échoue après
ouverture OOS, le segment reste dans la chronologie comme preuve d’échec,
d’inconclusivité ou de non-déploiement. Il ne doit pas être retiré pour
améliorer le résultat global.

### 3.5 Boucle globale de validation

Les segments locaux ne valident pas isolément le processus. La validation finale
porte sur la série OOS globale :

```text
OOS_1 + OOS_2 + ... + OOS_n
        |
        v
Série quotidienne primaire complète
        |
        v
Detrending et estimation statistique OOS
        |
        v
Gate statistique global
        |
        v
Gate économique séparé
        |
        v
Reproductibilité indépendante
        |
        v
Incubation puis déploiement limité si les gates requis passent
```

Lecture de la boucle globale :

| Étape globale | SOP propriétaires |
| --- | --- |
| Segments OOS non chevauchants et concaténation chronologique | SOP 01, SOP 04 |
| Série quotidienne primaire complète | SOP 01, SOP 08 |
| Detrending et estimation statistique OOS | SOP 01, SOP 07 |
| Gate statistique global | SOP 01 |
| Gate économique séparé | SOP 08, SOP 09B |
| Reproductibilité indépendante | SOP 12 |
| Incubation, déploiement limité et cycle de vie | SOP 11, SOP 12 |

Le gate économique ne remplace pas le gate statistique. La reproduction ne
répare pas une faiblesse méthodologique. L’incubation et le live ne sont
autorisés qu’après les paquets et statuts exigés par SOP 11 et SOP 12.

### 3.6 Hiérarchie d’autorité et anti-divergence

Les chemins de lecture et de reprise sont centralisés dans
`Protocole/0-README - Comprendre et maintenir le protocole EBTA.md`.

La hiérarchie d’autorité est :

```text
MANIFESTE -> PROTOCOLE -> REGISTRE -> SOP -> PAQUET D'EXECUTION
        -> Implementation/ebta_engine -> adaptateurs externes
```

Si `Implementation/` contredit `Protocole/`, `Implementation/` est fautif. Si
`Implementation/` révèle une ambiguïté normative, il faut ouvrir une correction
documentaire contrôlée ou une nouvelle version documentaire avant de coder la
règle comme norme.

---

## 4. Ordre des gates

| Ordre | Gate | Condition de passage | Sortie si échec | SOP propriétaires |
| --- | --- | --- | --- | --- |
| G0 | Préenregistrement | Hypothèse, configuration, données, `asset_universe`, folds, espace de recherche, seeds et gates scellés. | Pas de recherche EBTA valide. | SOP 03, SOP 04, SOP 09A, SOP 12 |
| G1 | Données point-in-time | Données disponibles, snapshots, latences, purge et embargo validés. | `FAIL` ou `INCONCLUSIVE`. | SOP 09A |
| G2 | Registre et candidates | Registre complet, candidates et familles opposables, couples `stratégie × actif` comptés si sélectionnables, matrices reconstructibles. | `FAIL` ou `INCONCLUSIVE`. | SOP 03 |
| G3 | Sélection locale | Candidate locale désignée mécaniquement selon la règle préenregistrée. | `NO_MODEL`, `STOP_PROCESS`, `NOT_VALIDATED` ou `INCONCLUSIVE`. | SOP 06 |
| G4 | Inférence multiple Test | WRC local primaire `PASS` sur la famille complète applicable, sans retirer les actifs ou couples perdants après observation. | Pas d’exposition sur `OOS_k`. | SOP 02 |
| G5 | Robustesse pré-OOS | Stress-tests décisionnels préenregistrés satisfaits. | OOS non ouvert ou statut bloquant préspécifié. | SOP 05 |
| G6 | Exécution et capacité | Modèle d’exécution central, coûts, sizing, capacité et NAV tradable validés. | `REJECTED_ECONOMIC`, `FAIL` ou `INCONCLUSIVE`. | SOP 09B |
| G7 | Paquet pré-OOS | Paquet `PRE_OOS_SEALED` complet et hashé. | OOS non ouvert. | SOP 12 |
| G8 | Ouverture OOS | Journal d’accès OOS prêt ; toutes les conditions précédentes sont satisfaites. | OOS non ouvert. | SOP 10 |
| G9 | Estimation OOS globale | IC OOS, puissance, série concaténée et gate statistique calculés au point d’arrêt prévu. | `NOT_VALIDATED`, `FAIL` ou `INCONCLUSIVE`. | SOP 01 |
| G10 | Gate économique | Hurdle économique, coûts, risque, capacité et exécutabilité satisfaits. | `REJECTED_ECONOMIC` ou `INCONCLUSIVE`. | SOP 08, SOP 09B |
| G11 | Validation reproductible | Paquet `VALIDATION_READY` et reproduction indépendante `PASS`. | Pas d’incubation. | SOP 12 |
| G12 | Incubation | Paper trading prospectif du processus gelé. | `FAIL`, `INCONCLUSIVE`, `WATCH` ou archivage. | SOP 11 |
| G13 | Déploiement limité | Paquet `DEPLOYMENT_CERTIFIED`, limites, sizing, kill switch et monitoring validés. | Pas de live. | SOP 11, SOP 12 |
| G14 | Cycle de vie | Monitoring, incidents, modifications, retrait et archive finale. | Nouvelle version ou retrait. | SOP 10, SOP 11, SOP 12 |

---

## 5. Verdicts globaux

Les verdicts globaux de validation sont :

- `PASS` ;
- `NOT_VALIDATED` ;
- `REJECTED_ECONOMIC` ;
- `FAIL` ;
- `INCONCLUSIVE`.

Règles :

- `PASS` exige un gate statistique `PASS`, un gate économique `PASS`, une robustesse pré-OOS suffisante, une exécution/capacité validée et un paquet reproductible.
- `NOT_VALIDATED` signifie que la preuve disponible ne suffit pas à valider le processus sans démontrer une violation irréparable.
- `REJECTED_ECONOMIC` signifie que le gate statistique applicable est satisfait, mais que le processus n’est pas exploitable économiquement.
- `FAIL` signifie qu’une condition statistique, méthodologique ou technique bloquante échoue selon une règle valide.
- `INCONCLUSIVE` signifie qu’aucune conclusion défendable ne peut être produite.

Les statuts locaux `NO_MODEL`, `STOP_PROCESS`, `INVALID_TECHNICAL`, `WATCH`,
`PRE_OOS_SEALED`, `VALIDATION_READY`, `DEPLOYMENT_CERTIFIED` et
`LIFECYCLE_ARCHIVED` conservent leur sens défini dans les SOP propriétaires et
dans le registre normatif.

---

## 6. Règles statistiques principales

### 6.1 Test side

Le Test est le lieu de l’inférence multiple.

Le gate confirmatoire primaire est le White’s Reality Check local, exécuté dans
chaque fold sur la famille complète et reconstructible des candidates
applicables.

Un SPA favorable, une analyse Romano-Wolf ou une MCPM ne peuvent pas renverser
un WRC primaire `FAIL` ou `INCONCLUSIVE`.

### 6.2 OOS side

L’OOS est le lieu de l’estimation passive du processus gelé.

Le verdict OOS global repose sur :

- la série quotidienne concaténée des segments `OOS_k` ;
- l’espérance nette detrendée ;
- une borne inférieure unilatérale à 95 % ;
- un bootstrap stationnaire par blocs propre à l’OOS ;
- la puissance et le point d’arrêt informationnel préenregistrés.

La distribution WRC calculée sur Test ne doit pas être recentrée ni réutilisée
pour construire l’intervalle de confiance OOS.

---

## 7. Série de rendement et performance

La représentation canonique EBTA est une série quotidienne complète du
portefeuille. Si la recherche sélectionne un couple `stratégie × actif`, ce
couple est évalué comme candidate tradable ; si la recherche définit un
portefeuille multi-actifs fixe, c’est le portefeuille qui constitue la
candidate évaluée.

| Objet | Règle | SOP propriétaire |
| --- | --- | --- |
| Série statistique primaire | Log-rendement quotidien net detrendé. | SOP 08 |
| Detrending | Retrait du drift excédentaire du marché pondéré par exposition. | SOP 07 |
| Cash | Neutralisé dans le gate statistique, conservé dans le gate économique. | SOP 07, SOP 08 |
| Performance économique | NAV réelle nette, coûts, risque, capacité et exécutabilité. | SOP 08, SOP 09B |
| Jours sans exposition | Conservés dans la chronologie. | SOP 08 |

Les métriques secondaires ne remplacent jamais rétroactivement la métrique
primaire.

---

## 8. Préenregistrement et configuration

Chaque recherche EBTA doit produire une configuration préenregistrée à partir du
template :

`Protocole/TEMPLATE - Configuration préenregistrée d'une recherche EBTA.md`

Cette configuration fixe notamment :

- univers, actifs, règles d’éligibilité et période ;
- fréquence, calendrier et fuseau horaire ;
- fournisseurs et snapshots de données ;
- fenêtres `Train_k`, `Test_k`, `OOS_k` ;
- purge, embargo et warm-up ;
- benchmark, cash et devise de base ;
- coût, slippage, impact, financement, FX, borrow, sizing et capacité ;
- métrique primaire et hurdle économique ;
- effet minimal détectable, puissance cible et point d’arrêt ;
- méthodes bootstrap, réplications, longueurs de blocs et seeds ;
- stress-tests de robustesse ;
- critères d’incubation, live, suspension et retrait.

Une valeur configurable non préenregistrée ne peut pas devenir un critère de
passage après observation.

---

## 9. Livrables obligatoires

| Étape | Livrable minimal | SOP |
| --- | --- | --- |
| Préenregistrement | Configuration scellée, hypothèse, calendrier, plan d’analyse. | SOP 03, SOP 04, SOP 12 |
| Données | Snapshots, disponibilité point-in-time, purge, embargo, contrôles anti-leakage. | SOP 09A |
| Recherche | Registre append-only, candidates, runs, événements, matrices. | SOP 03 |
| Test | Rapport WRC, SPA/Romano-Wolf/MCPM si applicables, matrice et hashes. | SOP 02 |
| Sélection | Manifeste de recherche et candidate transmise. | SOP 06 |
| Robustesse | Plan, catalogue, matrice et verdict de robustesse. | SOP 05 |
| Exécution | Journal signal-ordre-fill-position-P&L, coûts, capacité, NAV. | SOP 09B |
| OOS | Journal d’accès, série OOS, IC, puissance, verdicts. | SOP 01, SOP 10 |
| Validation | Paquet `VALIDATION_READY`, reproduction indépendante. | SOP 12 |
| Incubation/live | Paper trading, limites, kill switch, monitoring, incidents. | SOP 11 |
| Archivage | Paquet `LIFECYCLE_ARCHIVED`, checksums et conservation. | SOP 12 |

---

## 10. Interdictions générales

Il est interdit de :

- ouvrir un `OOS_k` après WRC local `FAIL` ou `INCONCLUSIVE` ;
- sélectionner, départager ou réparer une candidate sur l’OOS ;
- ajouter un holdout final historique après l’OOS Walk-Forward global ;
- retirer des candidates médiocres après observation ;
- réduire l’univers statistique par déduplication rétrospective ;
- remplacer le WRC par un SPA favorable ;
- traiter les folds comme IID sans justification ;
- utiliser le pourcentage de folds positifs comme gate confirmatoire ;
- calculer l’IC OOS depuis la distribution WRC Test ;
- confondre rendement brut, rendement net, alpha detrendé et performance économique ;
- choisir un benchmark, un hurdle, un coût ou une métrique après résultat ;
- apprendre une transformation hors `Train_k` ;
- modifier les paramètres, le code, l’exécution ou le sizing après observation OOS sans nouvelle candidate/version ;
- transformer `NOT_VALIDATED`, `REJECTED_ECONOMIC` ou `INCONCLUSIVE` en `PASS` ;
- incuber ou passer live sans paquet reproductible au stade requis.

---

## 11. Gouvernance des modifications

Toute modification doit être classée avant exécution :

| Type de modification | Conséquence |
| --- | --- |
| Correction documentaire sans effet méthodologique | Nouvelle version documentaire. |
| Correction technique pré-OOS sans effet sur signaux/P&L/statuts | Nouveau run ou nouvelle version technique selon SOP 03/SOP 12. |
| Correction technique post-OOS | Gouvernée par SOP 10 ; nécessite preuve indépendante et diff minimal. |
| Changement de logique alpha, données décisionnelles, exécution, sizing ou seuil influent | Nouvelle candidate ou nouvelle version de processus. |
| Changement de décision normative du protocole | Nouvelle version du protocole EBTA. |

Un segment OOS déjà ouvert ne redevient jamais vierge pour une version modifiée.

---

## 12. Index des SOP

| SOP | Propriété principale |
| --- | --- |
| SOP 01 - Estimation et intervalle de confiance OOS | Estimation OOS, IC, puissance, verdict statistique global. |
| SOP 02 - Inférence multiple WRC SPA Romano-Wolf MCP | WRC local, SPA, Romano-Wolf, MCPM, correction du data-mining bias. |
| SOP 03 - Registre des expériences et univers des règles candidates | Source de vérité des candidates, couples `stratégie × actif`, runs, familles, événements et matrices. |
| SOP 04 - Segmentation temporelle et Walk-Forward | Calendrier, folds, purge, embargo, OOS global. |
| SOP 05 - Tests de robustesse et gouvernance du holdout | Robustesse décisionnelle pré-OOS et diagnostics post-OOS non réparateurs. |
| SOP 06 - Sélection des règles candidates et optimisation de la complexité | Sélection locale, complexité, candidate transmise, `NO_MODEL`. |
| SOP 07 - Detrending benchmark et zero-centering | Flux signal/évaluation, detrending, benchmark, cash, zero-centering. |
| SOP 08 - Mesures de performance et série de rendement de référence | Série primaire, NAV, gate économique, portefeuille multi-actifs et métriques. |
| SOP 09A - Données point-in-time et contrôles anti-leakage | Disponibilité temporelle, `asset_universe` point-in-time, snapshots, anti-leakage, purge/embargo côté données. |
| SOP 09B - Modèle d’exécution frictions capacité et sizing | Ordres, fills, coûts, capacité, sizing, NAV tradable. |
| SOP 10 - Gouvernance OOS et gestion des échecs | Accès OOS, contamination, échecs, réexécutions techniques. |
| SOP 11 - Incubation passage live et monitoring séquentiel | Paper trading, live limité, monitoring, suspension, retrait. |
| SOP 12 - Reproductibilité et paquet de validation EBTA | Paquets, stades, checksums, reproduction et archivage. |

---

## 13. Critère de gel du protocole

Le protocole EBTA est gelable lorsque :

- la matrice de cohérence ne contient plus de contradiction bloquante ;
- le registre normatif est à jour ;
- le template de configuration est disponible ;
- le protocole principal référence les SOP sans les dupliquer ;
- l’audit méthodologique initial est clôturé point par point ;
- les artefacts exécutables nécessaires sont définis ;
- les hashes des documents gelés sont produits et archivés.

Toute évolution ultérieure ouvre une nouvelle version identifiable du protocole.
