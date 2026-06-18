# SOP 06 — Sélection des règles candidates et optimisation de la complexité
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 06 |
| Rôle dans le paquet EBTA | Selection locale, optimisation de complexite, candidate transmise et absence de modele. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## 1. Statut et objet

- **Statut :** spécification normative de la sélection locale des candidates et de l’optimisation de la complexité.
- **Architecture :** application séparée dans chaque fold du Walk-Forward défini par la SOP 04.
- **Entrée :** univers de recherche immuable, métrique primaire, modèle de coûts, budget et règles de sélection préenregistrés.
- **Sortie :** une candidate locale unique gelée et autorisée, ou un statut bloquant explicite.

Cette SOP définit la procédure qui :

1. calibre les paramètres sur `Train_k` ;
2. construit les candidates représentatives de chaque famille et niveau de complexité ;
3. évalue ces candidates sur `Test_k` ;
4. sélectionne mécaniquement la structure et la complexité ;
5. soumet la famille complète applicable au White’s Reality Check local ;
6. gèle la candidate transmise à `OOS_k`.

Elle interdit la sélection visuelle, le changement opportuniste de l’espace de recherche, la réduction ex post de la famille statistique et toute sélection sur l’OOS.

---

## 2. Autorités normatives

La présente SOP consomme sans les redéfinir :

- la série primaire, les métriques et les hurdles de la SOP 08 ;
- le catalogue, le registre append-only, les identifiants et les lignages de la SOP 03 ;
- les fenêtres `Train_k`, `Test_k` et `OOS_k` de la SOP 04 ;
- les tests de robustesse pré-OOS de la SOP 05 ;
- le WRC local et les tests secondaires de la SOP 02 ;
- le detrending et le zero-centering de la SOP 07 ;
- les contrôles point-in-time de la SOP 09A ;
- les conventions d’exécution et de coûts de la SOP 09B.

En cas de contradiction, la SOP propriétaire de l’objet concerné prévaut.

---

## 3. Principe fondamental

Le processus sélectionné n’est pas « la meilleure equity curve ». Il s’agit d’un algorithme préenregistré qui transforme un snapshot de recherche et des données disponibles en :

- une candidate unique ;
- un verdict de gate ;
- une preuve complète et reproductible.

Dans chaque fold :

```text
snapshot de l’univers
  → calibration sur Train_k
  → une candidate représentative par famille/niveau prévu
  → évaluation de la complexité sur Test_k
  → WRC_k sur la famille complète applicable
  → gel
  → déploiement éventuel sur OOS_k
```

`Test_k` est une donnée de sélection. Sa performance est donc biaisée par l’optimisation de complexité et ne constitue pas une estimation finale.

---

## 4. Types de recherche

Chaque projet déclare avant le premier run l’un des types suivants, ou une combinaison explicitement ordonnée.

### 4.1 Optimisation paramétrique

La forme logique est fixe et seules des valeurs numériques varient.

### 4.2 Rule searching

Plusieurs formes logiques appartenant à un catalogue fini sont comparées.

### 4.3 Rule induction

La structure elle-même évolue, notamment par :

- ajout ou sélection de features ;
- opérateurs logiques ;
- arbres ;
- réseaux ;
- programmation génétique ;
- ensembles ou agrégations.

Le type de recherche, l’espace, la procédure, le budget et la règle d’arrêt sont des propriétés du run. Ils ne peuvent être requalifiés après observation des résultats.

---

## 5. Snapshot de l’espace de recherche

Avant l’accès à `Train_k`, le run référence un snapshot immuable contenant au minimum :

- `research_family_id` ;
- `universe_snapshot_id` et hash ;
- identifiant canonique de chaque spécification ;
- familles et sous-familles ;
- formes logiques ;
- paramètres, bornes, pas et contraintes ;
- features et transformations ;
- opérateurs autorisés ;
- niveaux de complexité ;
- seeds et réplications ;
- méthode de recherche ;
- budget maximal ;
- règle d’arrêt ;
- règle de transfert `Train_k → Test_k` ;
- règle de sélection inter-familles ;
- métrique primaire et sens d’optimisation ;
- modèle de coûts et d’exécution ;
- critères de validité et de stabilité ;
- politique `NO_MODEL` ou `STOP_PROCESS`.

Une description narrative non hashée ne constitue pas un snapshot.

---

## 6. Population appartenant à l’effort de recherche

Appartient à la famille statistique toute spécification dont le résultat a pu influencer :

- la sélection d’une famille ;
- le choix d’un niveau de complexité ;
- le choix d’un paramètre ;
- l’arrêt de la recherche ;
- la modification d’un filtre ;
- le sizing ou une contrainte ;
- la décision de transférer une candidate ;
- l’ouverture de l’OOS.

Sont notamment inclus :

- runs réussis, échoués ou interrompus ;
- variantes manuelles ;
- seeds ou réplications influentes ;
- agrégations ;
- inversions ;
- variantes de robustesse décisionnelles ;
- modèles ou métriques alternatifs consultés.

Il est interdit de limiter après coup le dénominateur aux seules candidates rentables, complètes ou finalement transmises.

---

## 7. Extension et adaptation de l’espace

Une extension pendant le cycle est autorisée uniquement si :

1. sa règle de déclenchement était entièrement préenregistrée ;
2. elle ne dépend pas du niveau ou du signe de la performance observée ;
3. son budget était borné ;
4. toutes les nouvelles candidates sont ajoutées au registre et à la famille statistique ;
5. le WRC rejoue le processus de recherche applicable.

Toute autre extension crée :

- une nouvelle version de recherche ;
- de nouvelles candidates ;
- un nouveau snapshot ;
- un nouveau run complet.

L’accès à un `OOS_k` déjà observé ne redevient jamais vierge pour cette nouvelle version.

---

## 8. Mesure de la complexité

La complexité est mesurée par une fonction ou un ordre préenregistré.

Exemples :

- nombre de paramètres libres ;
- nombre de features ;
- profondeur ou nombre de nœuds ;
- nombre de règles agrégées ;
- degrés de liberté effectifs ;
- longueur de description ;
- combinaison pondérée de dimensions.

### 8.1 Comparaison au sein d’une famille

Chaque famille définit une mesure cohérente `C_f(m)` et un ordre fini des niveaux explorés.

### 8.2 Comparaison inter-familles

Lorsque les dimensions ne sont pas comparables naturellement, le projet définit avant les résultats :

- une normalisation ;
- un ordre partiel ;
- une règle lexicographique ;
- ou une règle inter-familles distincte.

La performance Test ne peut pas servir de définition de la complexité.

---

## 9. Calibration sur `Train_k`

Pour chaque famille et niveau de complexité prévu :

1. appliquer exclusivement les données et transformations autorisées sur `Train_k` ;
2. évaluer toutes les spécifications prévues par l’algorithme ;
3. enregistrer les paramètres, séries quotidiennes, coûts et diagnostics ;
4. appliquer les critères de validité ;
5. produire une candidate représentative selon une règle mécanique.

Une candidate dont les données, rendements ou diagnostics requis sont incomplets :

- est exclue de manière traçable si la règle ex ante le permet ;
- ou rend la famille/le gate `INCONCLUSIVE` ou `NOT_VALIDATED` si l’absence compromet l’inférence.

Une valeur manquante ne peut être remplacée silencieusement par une simulation favorable.

---

## 10. Stabilité et plateau paramétrique

Lorsqu’un plateau est utilisé, sa définition est numérique et préenregistrée.

Le contrat de configuration précise :

- la proximité au maximum Train ;
- le nombre minimal de voisins valides ;
- la topologie du voisinage ;
- la dispersion ou sensibilité maximale ;
- la largeur minimale dans chaque dimension matérielle ;
- les tolérances sur exposition, turnover, coûts et fréquence de trading ;
- la politique aux frontières de grille.

Les valeurs sont propres au projet ou à la famille. La SOP impose les champs et la méthode, non des seuils universels.

### 10.1 Représentant du plateau

Le représentant est choisi selon une règle fixe, par exemple :

- centre géométrique ;
- médiane des paramètres ;
- point de moindre complexité ;
- point de moindre sensibilité.

### 10.2 Bordure ou voisinage insuffisant

Si le maximum est en bordure ou si le voisinage requis manque :

- la stabilité échoue ;
- ou la grille est étendue selon une règle préenregistrée ;
- ou le résultat devient `INCONCLUSIVE`.

Une conclusion visuelle est interdite.

---

## 11. Transfert `Train_k → Test_k`

Le nombre et l’identité des candidates transférées sont déterminés mécaniquement.

La règle primaire est :

> transférer la candidate représentative de chaque famille et de chaque niveau de complexité prévu par le plan.

Une autre règle bornée, telle qu’un `top-k` fixe, est admissible si elle est préenregistrée et compatible avec la puissance du test multiple.

Toutes les candidates transférées, et toutes celles ayant influencé leur sélection, restent comptabilisées dans l’effort de recherche.

Il est interdit :

- de choisir `k` après lecture de `Test_k` ;
- de réduire la famille après observation des p-values ;
- de ne conserver que la future gagnante.

---

## 12. Optimisation de la complexité sur `Test_k`

Pour chaque niveau `c`, mesurer la performance primaire :

$$
P_{Test_k}(c).
$$

Conformément à la procédure de complexité décrite par Aronson, la règle primaire est :

$$
c_k^*=\arg\max_c P_{Test_k}(c).
$$

Le niveau optimal est le niveau au sommet exact de la courbe Test avant sa dégradation.

### 12.1 Égalités exactes

En cas d’égalité dans la précision numérique préenregistrée, appliquer dans l’ordre :

1. complexité la plus faible ;
2. stabilité locale la plus forte ;
3. turnover le plus faible ;
4. coûts les plus faibles ;
5. exposition la plus simple ;
6. identifiant canonique.

Il est interdit de départager par l’OOS.

### 12.2 Règles de tolérance

Une règle de type one-standard-error peut être étudiée dans une expérience distincte. Elle n’est pas la règle primaire de cette SOP et doit être préenregistrée comme nouvelle procédure de sélection.

---

## 13. Règle d’arrêt et budget

La règle par défaut consiste à évaluer tous les niveaux prévus.

Un arrêt anticipé est admissible uniquement si :

- l’algorithme est préenregistré ;
- la patience, le seuil et le budget sont fixés ;
- les décisions intermédiaires sont enregistrées ;
- le processus est rejoué dans l’inférence lorsque nécessaire.

Un budget interrompu avant le point prévu produit `INCONCLUSIVE` ou `NOT_VALIDATED`, sauf si une condition d’arrêt préenregistrée a été satisfaite.

Il est interdit de revendiquer l’optimalité d’un espace non exploré selon son propre contrat.

---

## 14. Recherche stochastique

Pour tout composant stochastique, enregistrer :

- générateur et algorithme ;
- seeds ;
- nombre de réplications ;
- ordre d’exécution ;
- parallélisme ;
- règle d’agrégation ;
- tolérance de non-déterminisme.

Chaque seed influente est soit :

- une candidate distincte ;
- soit une réplication intégrée selon une règle d’agrégation préenregistrée.

Garder uniquement la meilleure seed est interdit.

---

## 15. Agrégations et règles inverses

Une agrégation est une candidate à part entière.

Son contrat fige :

- thème ;
- composants ;
- traitement des inverses ;
- pondérations ;
- seuils de vote ;
- normalisation ;
- gestion des signaux manquants ;
- exposition et contraintes.

Les inverses exacts ne peuvent être éliminés que par une règle automatique ex ante définie par la SOP 03.

Une déduplication fondée sur une corrélation observée après les résultats est interdite.

---

## 16. Machine learning

Le manifeste ML inclut :

- features ;
- transformations et leur fit ;
- architecture ;
- hyperparamètres ;
- fonction de perte ;
- seeds ;
- early stopping ;
- niveaux de complexité ;
- modèles évalués ;
- règle de sélection ;
- contraintes de dimensionnalité.

Dans chaque fold :

- `Train_k` apprend et calibre ;
- `Test_k` sélectionne la structure et la complexité ;
- `OOS_k` exécute passivement la candidate gelée.

Il n’existe aucune « exécution finale » supplémentaire après l’OOS Walk-Forward global.

---

## 17. Inférence locale

Après désignation de la candidate :

1. construire sur `Test_k` la matrice complète de la famille applicable ;
2. appliquer le detrending et le zero-centering selon la SOP 07 ;
3. exécuter le WRC local selon la SOP 02 ;
4. conserver SPA, Romano–Wolf et MCPM comme analyses secondaires ;
5. transmettre la candidate uniquement si le WRC primaire est `PASS`.

Tester seulement la candidate gagnante est interdit.

Un SPA favorable ne renverse pas un WRC primaire `FAIL` ou `INCONCLUSIVE`.

---

## 18. Robustesse et gate pré-OOS

La transmission vers `OOS_k` exige simultanément :

- snapshot conforme ;
- budget conforme ;
- calibration et sélection mécaniques ;
- stabilité requise ;
- matrice statistique complète ;
- WRC local `PASS` ;
- robustesse pré-OOS `PASS` ;
- exécution/capacité conformes ;
- candidate et processus gelés ;
- revue et traçabilité complètes.

---

## 19. Absence de modèle

La politique est fixée avant le premier fold.

### `NO_MODEL`

- aucune candidate n’est déployée sur `OOS_k` ;
- le segment reste dans l’OOS global avec la convention de cash/non-déploiement ;
- le calendrier peut continuer mécaniquement.

### `STOP_PROCESS`

- aucun OOS ultérieur n’est ouvert ;
- le processus global devient `NOT_VALIDATED` ou `INCONCLUSIVE` selon la cause.

Il est interdit de forcer la meilleure candidate Train ou Test lorsque les gates ne sont pas satisfaits.

---

## 20. Corrections techniques avant OOS

Une erreur détectée après gel mais avant ouverture d’OOS suit la procédure suivante :

1. classifier l’erreur indépendamment de la performance ;
2. conserver la version initiale ;
3. créer une nouvelle version technique ;
4. appliquer un correctif minimal ;
5. réexécuter mécaniquement toutes les étapes affectées ;
6. réappliquer tous les gates ;
7. obtenir une revue indépendante.

Le correctif ne peut pas être choisi parmi plusieurs versions en fonction de la performance.

---

## 21. Statuts

### `PASS`

Toutes les conditions de la section 18 sont satisfaites et la candidate peut être gelée pour `OOS_k`.

### `NOT_VALIDATED`

La procédure est valide, mais la preuve requise par un gate confirmatoire n’est pas obtenue.

### `REJECTED_ECONOMIC`

Le gate statistique applicable est satisfait, mais les coûts, le hurdle, le risque ou la capacité rendent la candidate inexploitable.

### `FAIL`

Violation méthodologique irréparable, contamination, sélection subjective, famille incomplète ou test valide défavorable selon sa SOP propriétaire.

### `INCONCLUSIVE`

Information, données, budget ou calcul insuffisants pour produire le verdict prévu.

### `NO_MODEL`

Aucune candidate admissible n’est déployée dans le fold selon la politique préenregistrée.

---

## 22. Livrables obligatoires

### 22.1 Manifeste de recherche

```text
[IDENTITY]
project_id:
research_family_id:
fold_id:
run_id:
universe_snapshot_id:
universe_snapshot_hash:

[SEARCH]
search_type:
families:
complexity_definition:
complexity_levels:
budget:
stop_rule:
seeds:

[TRAIN]
train_period:
calibration_rule:
plateau_rule:
representatives:

[TEST]
test_period:
primary_metric:
candidate_matrix_path:
candidate_matrix_hash:
selected_complexity:
selected_candidate_id:

[GATES]
stability_status:
wrc_status:
robustness_status:
execution_status:
deployment_authorized:

[FREEZE]
code_hash:
config_hash:
data_hash:
reviewer:
timestamp:
```

### 22.2 Trajectoire de recherche

Conserver :

- toutes les évaluations ;
- les candidates invalides ;
- les décisions d’arrêt ;
- les extensions ;
- les seeds ;
- les erreurs ;
- les règles de départage ;
- les séries quotidiennes ;
- les preuves de gate.

---

## 23. Contrôles de reproductibilité

Vérifier au minimum :

- même snapshot → même catalogue ;
- même seed → même trajectoire dans la tolérance ;
- même `Train_k` → mêmes représentantes ;
- même `Test_k` → même complexité sélectionnée ;
- même matrice → même WRC ;
- aucune lecture OOS dans le processus ;
- aucune candidate influente omise ;
- hashes et identifiants réconciliés avec la SOP 03.

---

## 24. Erreurs interdites

- Choisir visuellement un plateau.
- Garder la meilleure seed.
- Réduire la famille après observation du Test.
- Tester seulement la gagnante.
- Arrêter dès qu’un résultat favorable apparaît.
- Modifier l’espace après lecture du Test sans nouvelle version.
- Utiliser l’OOS pour départager.
- Déployer après WRC `FAIL` ou `INCONCLUSIVE`.
- Exclure les périodes `NO_MODEL` de l’OOS global.
- Présenter le Test comme estimation finale.

---

## 25. Sources internes

- `Notes/88-L'Induction de Règles à Complexité Variable en Trading Objectif.md`
- `Notes/90-Analyse Comparative de la Recherche et de l'Induction de Règles.md`
- `Notes/169-Optimisation de la Complexité et Détection du Surapprentissage en Walk-Forward.md`
- `Notes/175-La Loi d'Ashby et la Synergie des Règles Complexes.md`
- `Notes/176-L'Agrégation Thématique, Stratégies de Vote et Consensus Linéaire.md`
- `Notes/177 - L'Optimisation de la Complexité par l'Apprentissage Automatique.md`
- `Notes/BPL5 - L'Algorithme de la Boucle EBTA et l'Optimisation de la Complexité.md`

---

## 26. Décision méthodologique synthétique

> **Dans chaque fold, SOP 06 calibre les paramètres sur `Train_k`, évalue sur `Test_k` la candidate représentative de chaque famille et niveau de complexité, sélectionne le maximum exact de performance Test selon la procédure d’Aronson, puis soumet la famille complète au WRC local. Seul un WRC `PASS`, accompagné des gates de stabilité, robustesse et exécution, autorise le gel et le déploiement d’une candidate unique sur `OOS_k`. Toute variante influente reste dans le registre et dans l’effort de recherche. L’OOS ne sélectionne, ne départage et ne répare jamais un modèle.**
