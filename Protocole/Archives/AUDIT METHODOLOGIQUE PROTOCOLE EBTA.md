# Audit méthodologique du protocole EBTA
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ARCHIVE - HISTORIQUE_CLOTURE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | Gouvernance protocole EBTA |
| Rôle dans le paquet EBTA | Audit historique, cloture des constats methodologiques et justification du gel documentaire. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## Objet du document

Ce document mémorise l’audit du fichier `Protocole/PROTOCOLE EBTA.md`.

Il ne remplace pas le protocole et ne cherche pas à le réécrire. Il sert de référence de travail pour examiner, une par une, les sections qui doivent encore être précisées avant de figer définitivement le processus de recherche EBTA.

## Verdict général

Le protocole possède une architecture EBTA cohérente à haut niveau, mais il n’est pas encore assez précis pour devenir une procédure entièrement exécutable, reproductible et auditable.

Le problème principal n’est pas l’absence de concepts. Plusieurs décisions statistiques essentielles reposent encore sur :

- des règles fixes dont la justification n’est pas définie ;
- des formulations qualitatives laissant une marge d’interprétation ;
- des méthodes statistiques citées sans spécification algorithmique ;
- des étapes qui risquent de réutiliser ou de contaminer les données de validation.

Trois points nécessitent une revue prioritaire :

1. La réutilisation de la distribution WRC calculée sur le Test pour construire l’intervalle de confiance OOS.
2. Les tests de robustesse réalisés après ouverture de l’OOS, notamment en modifiant les paramètres.
3. Le Walk-Forward présenté comme une succession de folds indépendants, alors que les folds et leurs résultats sont généralement dépendants.

## Statut de clôture après revue des SOP

Date de clôture documentaire : 2026-06-24

Ce statut ne supprime pas le diagnostic historique ci-dessous. Il indique comment
chaque constat est désormais traité par les SOP, la matrice de cohérence, le
registre normatif, le template de configuration et le protocole principal révisé.

| Constat de l’audit | Statut | Document propriétaire | Commentaire de clôture |
| --- | --- | --- | --- |
| 1. Construction de l’intervalle de confiance OOS | `CLOSED` | SOP 01 | La distribution WRC Test n’est plus réutilisée ; l’IC OOS est construit sur la série OOS concaténée par bootstrap stationnaire par blocs. |
| 2. WRC, SPA, Romano-Wolf et MCP | `CLOSED` | SOP 02 | Le WRC local est le gate confirmatoire primaire ; SPA, Romano-Wolf et MCPM ont des rôles secondaires bornés. |
| 3. Définition d’une règle candidate et registre du data mining | `CLOSED` | SOP 03 | La candidate, la famille de recherche, la déduplication ex ante et le registre append-only sont définis. |
| 4. Walk-Forward et segmentation temporelle | `CLOSED` | SOP 04 | Le Walk-Forward est obligatoire ; les `OOS_k` sont non chevauchants et concaténés ; les folds ne sont pas traités comme IID sans justification. |
| 5. Robustesse et contamination de l’OOS | `CLOSED` | SOP 05, SOP 10 | La robustesse décisionnelle est pré-OOS ; les analyses post-OOS sont descriptives et ne permettent aucune réparation. |
| 6. Sélection des candidates et optimisation de la complexité | `CLOSED` | SOP 06 | La sélection locale, le maximum Test, la famille complète WRC et l’interdiction de sélection OOS sont définis. |
| 7. Detrending, benchmark et zero-centering | `CLOSED` | SOP 07 | Les flux signal/évaluation sont séparés ; detrending et zero-centering ne sont plus confondus. |
| 8. Mesure de performance | `CLOSED` | SOP 08 | La série primaire est le log-rendement quotidien net detrendé ; le gate économique reste séparé. |
| 9. Qualité des données et modèle d’exécution | `CLOSED` | SOP 09A, SOP 09B | Données point-in-time, anti-leakage, exécution, coûts, sizing, capacité et NAV tradable sont couverts. |
| 10. Gestion des échecs OOS | `CLOSED` | SOP 10 | L’accès OOS, la contamination, les réexécutions techniques et les conséquences des échecs sont gouvernés. |
| 11. Incubation, passage live et monitoring | `CLOSED` | SOP 11 | L’incubation ne répare pas l’alpha ; le live limité et le monitoring séquentiel sont définis. |
| 12. Reproductibilité et paquet de validation | `CLOSED` | SOP 12 | Les stades `PRE_OOS_SEALED`, `VALIDATION_READY`, `DEPLOYMENT_CERTIFIED` et `LIFECYCLE_ARCHIVED` structurent le paquet. |
| Centralisation des décisions normatives | `CLOSED` | Registre normatif | Les décisions figées, propriétaires, preuves et moments de préenregistrement sont indexés. |
| Séparation principes / paramètres de recherche | `CLOSED` | Template de configuration | Les paramètres configurables sont sortis du protocole principal et placés dans un template remplissable. |
| Protocole principal | `CLOSED` | Protocole EBTA | Le protocole principal est révisé comme carte générale, ordre des gates, livrables, gouvernance et index des SOP. |
| Artefacts opérationnels exécutables | `DEFERRED_IMPLEMENTATION` | Futur paquet d’exécution | Les formulaires, schémas, tests automatisés d’invariants et journaux exécutables restent à produire après gel documentaire. |

Verdict de clôture documentaire :

`CLOSED_WITH_DEFERRED_IMPLEMENTATION`

Les décisions méthodologiques sont documentées et propriétaires. L’implémentation
opérationnelle reste une étape séparée : elle doit transformer les SOP en
formulaires, schémas, registres machine-readable, checklists exécutables et tests
automatisés.

---

## Éléments déjà suffisamment clairs dans le protocole général

Les principes suivants sont correctement établis et peuvent rester dans le document principal :

- séparation entre découverte, sélection et validation ;
- formulation préalable d’une hypothèse falsifiable ;
- nécessité de comptabiliser l’intégralité de l’effort de recherche ;
- interdiction de réoptimiser après observation de l’OOS ;
- gel du code avant validation finale ;
- prise en compte générale du look-ahead bias, du survivorship bias et des coûts ;
- journalisation des essais et archivage des échecs ;
- distinction conceptuelle entre preuve statistique et estimation économique ;
- progression générale Train → Test → OOS → robustesse → incubation → live ;
- nécessité de corriger le biais de data mining ;
- recherche de stabilité des paramètres plutôt que de pics isolés ;
- obligation de définir un rationnel économique ou comportemental.

Ces sections définissent correctement la philosophie du processus. Elles doivent toutefois renvoyer vers des procédures spécialisées pour leurs modalités d’exécution.

---

# Sections à renforcer

## 1. Construction de l’intervalle de confiance OOS

### Passage concerné

Le protocole demande de conserver la distribution d’échantillonnage produite par le WRC sur le Test, de la recentrer sur la moyenne OOS et d’en déduire l’intervalle de confiance de la performance future.

### Problème

La distribution générée par le WRC et la distribution nécessaire à l’estimation OOS ne décrivent pas nécessairement le même objet statistique :

- le WRC étudie le maximum d’un univers de règles sous l’hypothèse nulle ;
- l’intervalle OOS étudie l’incertitude associée à une règle unique et déjà gelée ;
- les périodes Test et OOS peuvent avoir des tailles, régimes et structures de dépendance différents ;
- le maximum d’un ensemble de règles possède une distribution différente de la moyenne d’une règle fixe.

La distribution WRC du Test ne peut donc pas être automatiquement réutilisée comme distribution d’estimation OOS sans démonstration méthodologique.

### Point logique à clarifier

Exiger que la borne inférieure d’un intervalle de confiance OOS soit supérieure à zéro revient implicitement à prendre une décision équivalente à un test unilatéral de :

$$H_0 : \mu \leq 0$$

Le protocole affirme parallèlement qu’aucun test d’hypothèse ne doit être effectué sur l’OOS. Cette formulation est trop absolue.

Ce qui doit être interdit est :

- de sélectionner plusieurs règles sur l’OOS ;
- de modifier la règle à partir du résultat OOS ;
- de multiplier les analyses OOS jusqu’à obtenir un résultat favorable.

Un critère confirmatoire préenregistré sur une règle gelée peut être statistiquement valide, à condition que son rôle et ses conséquences soient précisément définis.

### Processus séparé requis

`SOP 01 - Estimation et intervalle de confiance OOS.md`

Le document devra définir :

- la quantité estimée ;
- l’unité d’observation ;
- la méthode d’intervalle de confiance ;
- la gestion de l’autocorrélation ;
- la gestion des rendements ou trades qui se chevauchent ;
- le niveau de confiance ;
- la règle de décision ;
- la différence entre estimation, test confirmatoire et sélection ;
- les conséquences exactes d’un échec OOS.

### Pourquoi ce processus est critique

Une mauvaise distribution d’échantillonnage produit une borne basse incorrecte. Le protocole pourrait alors accepter une stratégie trop incertaine ou rejeter une stratégie pour une raison statistiquement invalide.

---

## 2. White’s Reality Check, SPA, Romano–Wolf et MCP

### Problème

Le protocole regroupe plusieurs méthodes sous des formulations trop générales et présente parfois Romano–Wolf comme une simple version améliorée du WRC.

Ces méthodes répondent pourtant à des objectifs différents :

- **White’s Reality Check :** test global de la meilleure règle contre un benchmark en tenant compte de la recherche multiple ;
- **Hansen SPA :** amélioration de puissance du Reality Check, notamment lorsqu’un univers contient beaucoup de mauvaises règles ;
- **Romano–Wolf :** procédure stepdown de tests multiples permettant notamment d’identifier plusieurs hypothèses significatives tout en contrôlant l’erreur familiale ;
- **MCP :** méthode de permutation destinée à casser la relation entre signaux et rendements, dont la validité dépend du schéma exact de permutation.

### Éléments non définis

- hypothèse nulle exacte ;
- statistique de performance testée ;
- benchmark ;
- performance différentielle ;
- zero-centering ;
- studentisation ;
- méthode de bootstrap ;
- longueur et choix des blocs ;
- nombre de réplications ;
- seed aléatoire ;
- traitement de l’autocorrélation ;
- traitement de l’hétéroscédasticité ;
- traitement des rendements qui se chevauchent ;
- règle de choix entre WRC, SPA, Romano–Wolf et MCP ;
- procédure en cas de valeurs manquantes ou d’historiques différents entre règles ;
- conditions minimales de puissance statistique.

### Processus séparé requis

`SOP 02 - Inférence multiple WRC SPA Romano-Wolf MCP.md`

### Pourquoi ce processus est critique

Sans spécification exacte, deux implémentations portant le même nom peuvent produire des p-values et des verdicts différents. Le risque porte directement sur le contrôle des faux positifs issus du data mining.

---

## 3. Définition d’une règle candidate et registre du data mining

### Problème

Le protocole repose fortement sur le compteur global $M$, mais ne définit pas complètement ce qui constitue une règle ou une hypothèse candidate.

Le WRC ne consomme pas uniquement un nombre $M$. Il nécessite normalement la série temporelle de performance différentielle de chaque candidate.

### Questions non résolues

Une candidate distincte est-elle créée par :

- chaque combinaison de paramètres ?
- chaque actif ?
- chaque univers d’actifs ?
- chaque règle de sortie ?
- chaque méthode de sizing ?
- chaque modèle de coûts ?
- chaque architecture ML ?
- chaque seed aléatoire ?
- chaque sélection de variables ?
- chaque transformation des données ?
- chaque benchmark ?
- chaque modification humaine issue de l’observation d’un résultat ?
- chaque relance partielle ou abandonnée ?

Multiplier automatiquement le nombre de paramètres par le nombre d’actifs n’est correct que si chaque couple règle-actif constitue réellement une hypothèse sélectionnable séparément.

### Processus séparé requis

`SOP 03 - Registre des expériences et univers des règles candidates.md`

### Contenu attendu

- identifiant immuable de chaque expérience ;
- définition d’une candidate ;
- empreinte des données et du code ;
- paramètres complets ;
- métrique primaire ;
- série de rendements différentiels ;
- date et motif de l’essai ;
- statut retenu ou rejeté ;
- essais avortés ;
- recherches adaptatives ;
- expériences menées dans d’autres notebooks ou projets sur les mêmes données ;
- règle de constitution de la matrice complète requise par les tests multiples.

### Pourquoi ce processus est critique

Les essais invisibles ou mal définis réduisent artificiellement la correction statistique. Le chercheur peut alors croire que la meilleure règle est significative alors qu’elle n’est que la gagnante d’un univers de recherche sous-déclaré.

---

## 4. Walk-Forward et segmentation temporelle

### Problème

Plusieurs valeurs sont présentées comme règles générales sans justification statistique suffisante :

- découpage 50 % / 25 % / 25 % ;
- environ 1 000 barres par fold ;
- nombre de folds compris entre 3 et 10 ;
- validation si au moins 75 % des folds sont positifs ;
- moyenne pondérée des performances OOS.

La taille adéquate d’un segment dépend notamment :

- du nombre de trades ;
- de la fréquence de la stratégie ;
- de l’autocorrélation ;
- de l’horizon de détention ;
- de la présence de rendements qui se chevauchent ;
- du turnover ;
- de la variance de la métrique ;
- de la puissance statistique visée ;
- du nombre de règles candidates.

### Dépendance entre folds

Les folds ne sont généralement pas indépendants lorsque :

- les fenêtres Train se chevauchent ;
- les indicateurs possèdent de longs lookbacks ;
- les périodes de marché sont serially dependent ;
- les règles successives sont issues du même processus adaptatif ;
- les positions chevauchent les frontières temporelles.

Le seuil de 75 % de folds valides ne possède donc pas, en l’état, de justification statistique explicite.

### Éléments manquants

- rolling window ou expanding window ;
- durée de Train, Test et OOS ;
- pas de déplacement ;
- purge aux frontières ;
- embargo ;
- warm-up des indicateurs ;
- gestion des positions ouvertes aux frontières ;
- réentraînement autorisé ;
- hyperparamètres figés ou recalibrés ;
- agrégation chronologique des prédictions OOS ;
- pondération des folds ;
- estimation globale de l’incertitude ;
- règle de décision en présence de folds contradictoires.

### Processus séparé requis

`SOP 04 - Segmentation temporelle et Walk-Forward.md`

### Pourquoi ce processus est critique

Une mauvaise segmentation crée du leakage, surestime la stabilité et produit des observations OOS artificiellement redondantes. Le méta-verdict devient alors beaucoup plus confiant que les données ne le permettent.

---

## 5. Robustesse et contamination de l’OOS

### Passage concerné

La checklist de robustesse autorise notamment :

- une variation de ±5 % des paramètres sur l’OOS ;
- un découpage de l’OOS en sous-périodes ;
- la suppression des meilleurs trades ;
- des tests sur d’autres actifs ;
- des modifications de frais et de délais d’exécution.

### Problème

Si ces résultats déterminent le passage ou non en production, l’OOS n’est plus une évaluation unique et passive. Il devient un nouvel ensemble de sélection.

La variation des paramètres sur l’OOS est particulièrement problématique : elle ouvre plusieurs nouvelles règles après consultation du holdout final.

### Architecture à choisir

Le protocole doit retenir explicitement l’une des architectures suivantes :

1. Tous les tests de robustesse sont préenregistrés et réalisés avant le holdout final.
2. Un quatrième segment de données est réservé aux tests de robustesse.
3. Les analyses post-OOS restent purement diagnostiques et ne donnent droit à aucune modification ni seconde tentative.

### Processus séparé requis

`SOP 05 - Tests de robustesse et gouvernance du holdout.md`

### Pourquoi ce processus est critique

Tester plusieurs perturbations sur l’OOS et ne conserver que les résultats rassurants recrée un data-mining bias après la validation supposée finale.

---

## 6. Sélection des candidates et optimisation de la complexité

### Problème

Les expressions suivantes restent qualitatives :

- sommet de la courbe ;
- plateau de performance ;
- zone stable ;
- baisse modérée ;
- effondrement ;
- niveau optimal de complexité.

Elles ne garantissent pas qu’un chercheur tiers prendra la même décision.

### Éléments à définir

- mesure exacte de la complexité ;
- liste ordonnée des complexités autorisées ;
- métrique primaire ;
- tolérance autour du maximum ;
- largeur minimale d’un plateau ;
- règle du modèle le plus simple ;
- règle en cas d’égalité ;
- nombre de candidates transférées du Train au Test ;
- méthode top-k ou sélection de plateau ;
- critère d’arrêt ;
- traitement des modifications adaptatives ;
- pénalisation du nombre de paramètres ;
- distinction entre complexité structurelle et complexité paramétrique.

### Processus séparé requis

`SOP 06 - Sélection des règles candidates et optimisation de la complexité.md`

### Pourquoi ce processus est critique

Une sélection subjective permet au jugement humain de devenir un hyperparamètre invisible. Les décisions prises après observation du Test augmentent alors le biais de sélection sans être correctement enregistrées.

---

## 7. Detrending, benchmark et zero-centering

### État actuel

Le protocole mentionne le detrending « si requis », sans définir précisément les conditions de son utilisation.

Une note détaillée existe déjà :

`Notes/Detrending - La méthode - benchmark selon Aronson.md`

Elle constitue une bonne base conceptuelle, mais doit être transformée ou référencée comme procédure reproductible.

### Éléments à préciser

- cas où le detrending est obligatoire ;
- tendance retirée ;
- méthode d’estimation de la tendance ;
- fenêtre d’estimation ;
- estimation globale ou uniquement passée ;
- traitement par actif ;
- traitement par fold ;
- traitement des gaps ;
- traitement des dividendes ;
- utilisation des prix réels pour les signaux ;
- utilisation des rendements detrendés pour le P&L ;
- différence entre detrending et rendement excédentaire au benchmark ;
- différence entre detrending et zero-centering des rendements de règles ;
- prévention du leakage lors de l’estimation de la tendance.

### Processus séparé requis

`SOP 07 - Detrending benchmark et zero-centering.md`

### Pourquoi ce processus est critique

Un detrending calculé avec des informations futures ou appliqué au mauvais flux de données peut créer du look-ahead bias ou modifier artificiellement les signaux.

---

## 8. Mesure de performance

### Problème

Le protocole propose plusieurs métriques possibles sans fixer clairement une métrique primaire unique ni leurs conventions de calcul.

### Éléments à définir

- métrique primaire de sélection ;
- métriques secondaires ;
- moyenne arithmétique, géométrique ou logarithmique ;
- rendement quotidien, par trade ou de portefeuille ;
- performance brute ou différentielle au benchmark ;
- taux sans risque ;
- annualisation ;
- nombre de périodes annuel ;
- exposition ;
- levier ;
- positions simultanées ;
- pondération des actifs ;
- rendements qui se chevauchent ;
- autocorrélation ;
- définition du Sharpe ;
- définition du drawdown ;
- traitement des périodes sans position ;
- règle de décision lorsque les métriques se contredisent.

### Processus séparé requis

`SOP 08 - Mesures de performance et série de rendement de référence.md`

### Pourquoi ce processus est critique

Choisir après coup la métrique donnant le meilleur résultat constitue du metric shopping. Des conventions différentes peuvent également transformer une même stratégie en succès ou en échec.

---

## 9. Qualité des données et modèle d’exécution

### État actuel

Le protocole mentionne les principales familles de biais, mais ne définit pas encore leurs contrôles opérationnels.

### Éléments à préciser

- univers point-in-time ;
- actifs radiés et rendements de delisting ;
- dates d’entrée et de sortie de l’univers ;
- données fondamentales point-in-time ;
- révisions macroéconomiques ;
- date réelle de publication ;
- fuseaux horaires ;
- calendriers de marché ;
- corporate actions ;
- prix ajustés pour les indicateurs ;
- prix réellement exécutables ;
- spread bid-ask ;
- commissions ;
- slippage ;
- impact de marché ;
- disponibilité et coût de l’emprunt short ;
- contraintes de liquidité ;
- capacité ;
- séquence signal → ordre → fill ;
- ordres non exécutés ou partiellement exécutés.

### Processus séparés requis

`SOP 09A - Données point-in-time et contrôles anti-leakage.md`

`SOP 09B - Modèle d’exécution frictions capacité et sizing.md`

### Pourquoi ces processus sont critiques

Une stratégie peut être statistiquement significative sur des données impossibles à connaître ou à négocier au moment réel de la décision.

---

## 10. Gestion des échecs OOS

### État actuel

Le principe de non-retour après échec OOS est clairement affirmé. Une note spécialisée existe déjà :

`Notes/168-GESTION RIGOUREUSE DE L’ÉCHEC EN VALIDATION OUT-OF-SAMPLE (OOS).md`

### Points restant à définir

- différence entre erreur logicielle, erreur de données et échec économique ;
- conditions autorisant une réexécution technique ;
- preuve exigée qu’un bug existait avant l’ouverture OOS ;
- politique applicable au même rationnel économique reformulé ;
- période de quarantaine avant nouveau projet ;
- réutilisation éventuelle de l’ancien Train/Test ;
- contamination collective par plusieurs chercheurs ;
- archivage des décisions ;
- distinction entre nouveau modèle et modification du modèle rejeté.

### Processus séparé requis

`SOP 10 - Gouvernance OOS et gestion des échecs.md`

### Pourquoi ce processus est critique

Sans définition stricte d’un « nouveau projet », un modèle rejeté peut être légèrement renommé ou reformulé puis retesté sur le même OOS, ce qui transforme progressivement ce dernier en ensemble d’entraînement.

---

## 11. Incubation, passage en live et monitoring

### Problème

Le seuil de 90 jours est un critère calendaire, pas un critère d’information statistique.

Une stratégie mensuelle peut produire très peu de décisions en 90 jours, tandis qu’une stratégie intraday peut en produire plusieurs milliers.

### Éléments à définir

- nombre minimal de signaux ;
- nombre minimal de fills ;
- exposition cumulée minimale ;
- régimes de marché observés ;
- tolérance de tracking error ;
- slippage attendu et réalisé ;
- divergence de données ;
- seuils de suspension ;
- coupe-circuit ;
- règle de reprise ;
- procédure de recalibration ;
- responsabilité de validation ;
- monitoring séquentiel ;
- contrôle des faux signaux liés aux tests répétés ;
- différence entre bug d’infrastructure et perte d’edge.

### Processus séparé requis

`SOP 11 - Incubation passage live et monitoring séquentiel.md`

### Pourquoi ce processus est critique

Une durée fixe peut donner une fausse impression de validation malgré un échantillon trop faible. À l’inverse, des contrôles répétés non corrigés peuvent suspendre une stratégie valide uniquement à cause du hasard.

---

## 12. Reproductibilité et paquet de validation

### Éléments manquants

- version du code ;
- version des dépendances ;
- hash des données ;
- configuration complète ;
- seeds ;
- version du benchmark ;
- matrice des candidates ;
- résultats intermédiaires ;
- logs d’exécution ;
- rapport final généré automatiquement ;
- procédure permettant à un tiers de reproduire le verdict.

### Processus séparé requis

`SOP 12 - Reproductibilité et paquet de validation EBTA.md`

### Pourquoi ce processus est critique

Un résultat non reproductible ne permet pas de distinguer un edge réel d’une erreur de données, d’un état logiciel transitoire ou d’une exécution non déterministe.

---

# Documents complémentaires à produire

## Statut de réalisation des SOP

Les SOP identifiées par cet audit ont toutes été générées dans le dossier `Protocole/`.

| SOP | Statut |
|---|---|
| `SOP 01 - Estimation et intervalle de confiance OOS.md` | Générée |
| `SOP 02 - Inférence multiple WRC SPA Romano-Wolf MCP.md` | Générée |
| `SOP 03 - Registre des expériences et univers des règles candidates.md` | Générée |
| `SOP 04 - Segmentation temporelle et Walk-Forward.md` | Générée |
| `SOP 05 - Tests de robustesse et gouvernance du holdout.md` | Générée |
| `SOP 06 - Sélection des règles candidates et optimisation de la complexité.md` | Générée |
| `SOP 07 - Detrending benchmark et zero-centering.md` | Générée |
| `SOP 08 - Mesures de performance et série de rendement de référence.md` | Générée |
| `SOP 09A - Données point-in-time et contrôles anti-leakage.md` | Générée |
| `SOP 09B - Modèle d’exécution frictions capacité et sizing.md` | Générée |
| `SOP 10 - Gouvernance OOS et gestion des échecs.md` | Générée |
| `SOP 11 - Incubation passage live et monitoring séquentiel.md` | Générée |
| `SOP 12 - Reproductibilité et paquet de validation EBTA.md` | Générée |

Ce statut signifie que chaque sujet possède désormais une première spécification opérationnelle auditable. Il ne signifie pas encore que toutes les décisions normatives propres au projet — seuils, niveaux de confiance, tailles minimales ou tolérances — ont été validées humainement puis reportées dans le protocole principal.

## Priorité P0 — Nécessaires avant de figer le protocole

### P0.1 — Spécification d’inférence multiple

**Nom proposé :**

`SOP 02 - Inférence multiple WRC SPA Romano-Wolf MCP.md`

**Finalité :** définir exactement le test, le bootstrap, le benchmark, la statistique et l’univers d’hypothèses.

### P0.2 — Estimation et intervalle de confiance OOS

**Nom proposé :**

`SOP 01 - Estimation et intervalle de confiance OOS.md`

**Finalité :** corriger la réutilisation problématique de la distribution WRC et définir le rôle exact du verdict OOS.

### P0.3 — Segmentation temporelle et Walk-Forward

**Nom proposé :**

`SOP 04 - Segmentation temporelle et Walk-Forward.md`

**Finalité :** définir les fenêtres, la purge, l’embargo, le warm-up, l’agrégation OOS et la puissance minimale.

### P0.4 — Registre des expériences et règles candidates

**Nom proposé :**

`SOP 03 - Registre des expériences et univers des règles candidates.md`

**Finalité :** rendre l’intégralité de l’effort de recherche reconstructible et empêcher les essais invisibles.

### P0.5 — Mesures de performance

**Nom proposé :**

`SOP 08 - Mesures de performance et série de rendement de référence.md`

**Finalité :** empêcher le metric shopping et garantir la comparabilité de toutes les candidates.

### P0.6 — Gouvernance OOS, robustesse et échecs

**Noms proposés :**

`SOP 05 - Tests de robustesse et gouvernance du holdout.md`

`SOP 10 - Gouvernance OOS et gestion des échecs.md`

**Finalité :** définir ce qui reste autorisé après ouverture de l’OOS et supprimer les secondes chances implicites.

---

## Priorité P1 — Nécessaires avant l’implémentation industrielle

### P1.1 — Données point-in-time et contrôles anti-leakage

`SOP 09A - Données point-in-time et contrôles anti-leakage.md`

### P1.2 — Detrending, benchmark et zero-centering

`SOP 07 - Detrending benchmark et zero-centering.md`

### P1.3 — Sélection des candidates et complexité

`SOP 06 - Sélection des règles candidates et optimisation de la complexité.md`

### P1.4 — Robustesse préenregistrée

À intégrer dans :

`SOP 05 - Tests de robustesse et gouvernance du holdout.md`

### P1.5 — Exécution, frictions, capacité et sizing

`SOP 09B - Modèle d’exécution frictions capacité et sizing.md`

---

## Priorité P2 — Nécessaires avant le déploiement live

### P2.1 — Incubation et monitoring

`SOP 11 - Incubation passage live et monitoring séquentiel.md`

### P2.2 — Reproductibilité

`SOP 12 - Reproductibilité et paquet de validation EBTA.md`

---

# Ordre proposé pour la revue section par section

L’ordre suivant limite les dépendances entre décisions :

1. Définition de la performance et de la série de rendements.
2. Définition d’une règle candidate et du registre de recherche.
3. Detrending, benchmark et zero-centering.
4. WRC, SPA, Romano–Wolf et MCP.
5. Segmentation Train/Test/OOS.
6. Walk-Forward.
7. Sélection des candidates et optimisation de la complexité.
8. Estimation et intervalle de confiance OOS.
9. Gouvernance des échecs OOS.
10. Robustesse.
11. Données point-in-time et modèle d’exécution.
12. Incubation, live et monitoring.
13. Reproductibilité et archivage final.

---

# Notes existantes à consolider

Le dossier contient déjà des documents conceptuels utiles, notamment :

- `Notes/125-Le White's Reality Check Valider le Minage de Données.md`
- `Notes/126-Validation Statistique par Permutation de Monte Carlo.md`
- `Notes/Detrending - La méthode - benchmark selon Aronson.md`
- `Notes/Le Zero-Centering la méthode.md`
- `Notes/Éliminer les Biais Detrending et Zero-Centering - comparaisons.md`
- `Notes/122-Dynamique et Robustesse du Walk-Forward Testing.md`
- `Notes/166-Adaptation et Sélection Dynamique en Processus Walk-Forward.md`
- `Notes/168-GESTION RIGOUREUSE DE L’ÉCHEC EN VALIDATION OUT-OF-SAMPLE (OOS).md`
- `Notes/169-Optimisation de la Complexité et Détection du Surapprentissage en Walk-Forward.md`
- `Notes/173-Le rôle de l'OOS, estimation et stabilité dans l'EBTA.md`
- `Notes/174-Faut-il réaliser un test d'hypothèse sur l'OOS.md`
- `Notes/177 - L'Optimisation de la Complexité par l'Apprentissage Automatique.md`

Ces notes peuvent servir de matière première. Elles restent cependant principalement explicatives. Les futurs documents SOP devront définir des entrées, des sorties, des algorithmes, des seuils, des interdictions, des preuves attendues et des critères PASS/FAIL.

---

# Références méthodologiques principales

- White, H. — *A Reality Check for Data Snooping*.
- Hansen, P. R. — *A Test for Superior Predictive Ability*.
- Romano, J. P. et Wolf, M. — *Stepwise Multiple Testing as Formalized Data Snooping*.
- Politis, D. N. et Romano, J. P. — *The Stationary Bootstrap*.
- Bailey et López de Prado — travaux sur la probabilité de surapprentissage des backtests.

---

# Conclusion de l’audit

Le protocole actuel constitue une bonne charte méthodologique générale. Il ne constitue pas encore une spécification opératoire complète.

Avant de le figer, les documents P0 doivent être produits. Sans eux, deux chercheurs appliquant honnêtement le même protocole peuvent encore :

- construire des univers de candidates différents ;
- compter différemment l’effort de recherche ;
- choisir des bootstraps différents ;
- obtenir des p-values différentes ;
- construire des intervalles OOS différents ;
- prendre des décisions différentes sur les mêmes résultats ;
- contaminer involontairement l’OOS pendant les tests de robustesse.

L’objectif de la prochaine phase est donc de transformer chaque principe critique en procédure déterministe, préenregistrée, reproductible et auditable.
