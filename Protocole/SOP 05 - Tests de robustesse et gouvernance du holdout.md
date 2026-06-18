# SOP 05 — Tests de robustesse et gouvernance du holdout
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 05 |
| Rôle dans le paquet EBTA | Robustesse decisionnelle pre-OOS et diagnostics post-OOS non reparateurs. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## 1. Statut et objet

- **Type :** Standard Operating Procedure méthodologique.
- **Statut :** spécification normative des tests de robustesse du protocole EBTA.
- **Architecture applicable :** Walk-Forward à segments `OOS_k` successifs, sans holdout final supplémentaire.
- **Objet évalué :** processus préenregistré de recherche, de sélection, de recalibration et d’exécution, et non seul meilleur point paramétrique.
- **Moment des tests décisionnels :** avant l’ouverture de chaque `OOS_k`.
- **Effet bloquant :** un gate de robustesse non satisfait interdit l’ouverture de l’`OOS_k` concerné.

Cette SOP définit :

- les objectifs et le périmètre des tests de robustesse ;
- les entrées qui doivent être gelées ;
- le socle commun de stress-tests ;
- les tests conditionnels liés à l’hypothèse, aux données et à l’exécution ;
- les perturbations paramétriques, temporelles et cross-sectionnelles ;
- les diagnostics d’outliers ;
- les scénarios de frictions, d’exécution et de données ;
- l’agrégation mécanique des résultats ;
- les gates et statuts décisionnels ;
- les règles applicables après observation d’un OOS ;
- les livrables et preuves de reproductibilité.

Le mot **holdout** dans le titre désigne la fonction de données vierges remplie par chaque `OOS_k`. Il ne désigne pas un quatrième segment ni un holdout final ajouté après l’OOS Walk-Forward global.

---

## 2. Objectif méthodologique

La robustesse cherche à falsifier l’hypothèse selon laquelle la performance dépend de conditions trop précises ou irréalistes pour survivre au déploiement.

Elle doit notamment déterminer si le processus dépend :

- d’un optimum paramétrique isolé ;
- d’une sous-période ou d’un régime unique ;
- d’un actif ou d’un sous-univers choisi après observation ;
- de quelques périodes, trades ou événements extrêmes ;
- d’un modèle de coûts optimiste ;
- d’une exécution parfaite ;
- d’une qualité de données irréaliste ;
- d’une transformation, d’une métrique ou d’une convention sélectionnée après coup ;
- d’une dépendance dominante incompatible avec l’hypothèse économique.

La robustesse n’a pas pour objectif :

- de maximiser la performance d’une variante ;
- de créer une nouvelle candidate non prévue après observation ;
- d’obtenir un résultat rassurant sur tous les scénarios extrêmes ;
- de remplacer les tests multiples de la SOP 02 ;
- de remplacer l’estimation OOS de la SOP 01 ;
- de réparer un processus après observation de son OOS.

---

## 3. Principe fondamental

Un stress-test devient une comparaison appartenant à l’effort de recherche dès que son résultat peut influencer :

- la sélection d’une candidate ;
- le choix d’un paramètre ;
- la modification de la logique ;
- l’éligibilité d’un modèle ;
- l’ouverture d’un `OOS_k` ;
- le déploiement ;
- le sizing ou les contraintes ;
- le verdict final.

Dans ce cas :

- le stress-test est préenregistré ;
- ses variantes sont tracées selon la SOP 03 ;
- toute nouvelle candidate est comptabilisée dans la famille de recherche applicable ;
- les résultats sont observés avant l’ouverture de l’`OOS_k` concerné ;
- la décision est produite par un gate mécanique.

Un stress-test purement descriptif ne peut rester hors de la famille décisionnelle que si :

- son absence d’effet sur la sélection et le déploiement est fixée avant son exécution ;
- il est étiqueté comme diagnostic secondaire ;
- aucune modification du processus n’en découle ;
- son résultat ne sert pas à accorder une seconde chance.

---

## 4. Autorité normative et séparation des responsabilités

La SOP 05 orchestre la robustesse. Elle ne redéfinit pas les domaines déjà attribués aux SOP spécialisées.

- **SOP 01 :** estimation, intervalle de confiance et gate statistique sur l’OOS concaténé ;
- **SOP 02 :** inférence multiple et traitement statistique de la famille de candidates ;
- **SOP 03 :** identité des candidates, registre, familles de recherche, matrices, lignage et scellement ;
- **SOP 04 :** calendrier Walk-Forward, folds, fenêtres, purge, embargo et ouverture des `OOS_k` ;
- **SOP 07 :** detrending, benchmark statistique, zero-centering et ordre des transformations ;
- **SOP 08 :** série de rendement, métrique primaire, hurdle et métriques secondaires ;
- **SOP 09A :** données point-in-time, snapshots, qualité des données et anti-leakage ;
- **SOP 09B :** modèle d’exécution, coûts, slippage, capacité, sizing et contraintes ;
- **SOP 10 :** accès OOS, contamination, échecs, post-mortem et réexécutions techniques ;
- **SOP 12 :** paquet final, archivage et reproduction indépendante.

En cas de contradiction, la SOP spécialisée prévaut dans son domaine.

La SOP 05 reste l’autorité pour :

- le plan de robustesse ;
- la classification des scénarios ;
- la matérialité des stress-tests ;
- leur ordre d’exécution ;
- leur agrégation ;
- leur conséquence décisionnelle avant OOS.

---

## 5. Architecture normative

### 5.1 Architecture Walk-Forward

L’architecture obligatoire est :

```text
Pour chaque fold k :

Train_k
  → Test_k et robustesse décisionnelle sur les données autorisées avant OOS_k
  → enregistrement de toutes les variantes influentes
  → scellement du catalogue et de la matrice locale complète
  → inférence multiple et gates finaux pré-OOS
  → gel de la candidate locale et du processus
  → revue indépendante
  → ouverture unique de OOS_k
```

La robustesse et la sélection appartiennent à une même phase informationnelle pré-OOS. Leur ordre interne peut être itératif uniquement dans les limites du plan préenregistré et du registre append-only.

L’inférence multiple autorisant l’ouverture est calculée après :

- l’exécution de toutes les variantes décisionnelles prévues ;
- leur enregistrement dans la famille applicable ;
- la production de leurs séries ;
- le scellement de la matrice locale complète.

Un stress-test observé après le scellement qui conduit à créer ou sélectionner une variante :

- invalide le scellement antérieur pour cette décision ;
- exige une nouvelle version de matrice ;
- exige le recalcul des gates applicables ;
- reste strictement antérieur à l’ouverture de `OOS_k`.

Les `OOS_k` :

- sont successifs et non chevauchants ;
- restent passifs ;
- ne servent ni à sélectionner ni à réparer ;
- sont concaténés chronologiquement selon la SOP 04 ;
- forment l’unique OOS global.

Aucun holdout final supplémentaire n’est créé après cette concaténation.

### 5.2 Données autorisées pour la robustesse décisionnelle

Les stress-tests conditionnant l’ouverture de `OOS_k` utilisent uniquement :

- les données disponibles avant la frontière d’ouverture de `OOS_k` ;
- les segments `Train_k` et `Test_k` autorisés ;
- les snapshots point-in-time correspondants ;
- les données externes préenregistrées et disponibles à cette date ;
- les conventions de purge, embargo et disponibilité définies par les SOP 04 et 09A.

Il est interdit :

- d’exécuter plusieurs variantes sur `OOS_k` puis de choisir la plus stable ;
- d’utiliser des données postérieures à la frontière ;
- de calculer un stress décisionnel sur la concaténation OOS déjà observée ;
- de rouvrir un `OOS_k` après modification.

### 5.3 Objet robuste

Le verdict porte sur le **processus préenregistré**, comprenant :

- le générateur de candidates ;
- la procédure de calibration ;
- la sélection sur Test ;
- les gates statistiques et économiques ;
- la politique d’absence de candidat ;
- la fréquence de recalibration ;
- le modèle d’exécution ;
- les contraintes de portefeuille ;
- la politique de robustesse elle-même.

Une candidate locale peut recevoir un diagnostic de fragilité. Le verdict global doit toutefois rester attaché au processus qui produit successivement les candidates locales.

---

## 6. Préenregistrement

Avant le premier run sensible, le plan de robustesse doit figer :

- `PROJECT_ID`, `RESEARCH_FAMILY_ID` et `PROCESS_VERSION_ID` ;
- le ou les folds concernés ;
- la candidate ou le processus évalué ;
- le snapshot de données ;
- la segmentation autorisée ;
- la série de rendement primaire ;
- la métrique primaire ;
- le benchmark et le hurdle ;
- les métriques secondaires ;
- le modèle central de coûts et d’exécution ;
- le catalogue des stress-tests ;
- la justification de leur matérialité ;
- les paramètres perturbés ;
- les amplitudes et unités ;
- les interactions paramétriques testées ;
- les actifs et sous-univers ;
- les sous-périodes et régimes ;
- les scénarios de données ;
- les scénarios d’exécution ;
- les classes `CENTRAL`, `PLAUSIBLE_BASE` et `EXTREME` ;
- les seuils ;
- les conditions bloquantes ;
- les diagnostics non bloquants ;
- la méthode d’agrégation ;
- l’ordre des tests ;
- les règles d’arrêt ;
- le traitement des données insuffisantes ;
- le traitement des échecs techniques ;
- les seeds et tolérances éventuelles ;
- les livrables ;
- la revue indépendante requise.

Les valeurs telles que :

- `±5 %` ;
- `coûts ×2` ;
- retrait des cinq meilleurs trades ;
- trois actifs comparables ;
- cinq sous-périodes ;

ne constituent pas des standards universels. Leur utilisation exige une justification ex ante.

Toute modification du plan après observation :

- crée un événement dans le registre ;
- peut créer une nouvelle candidate ou version de processus ;
- interdit de présenter le nouveau plan comme préenregistré ;
- exige de nouvelles données vierges s’il utilise une information OOS.

---

## 7. Entrées obligatoires

Le pipeline de robustesse reçoit au minimum :

```text
[IDENTITY]
project_id:
research_family_id:
process_version_id:
fold_id:
candidate_id:
plan_id:

[DATA]
data_snapshot_id:
train_period:
test_period:
oos_boundary:
calendar:
timezone:
point_in_time_policy:

[PERFORMANCE]
primary_return_series:
primary_metric:
benchmark:
hurdle:
secondary_metrics:
risk_gates:

[EXECUTION]
execution_model_version:
central_cost_model:
capital_target:
sizing_rule:
portfolio_constraints:

[ROBUSTNESS]
stress_catalog_version:
scenario_classes:
parameter_grid:
interaction_plan:
subperiod_plan:
cross_section_plan:
outlier_plan:
friction_plan:
execution_perturbation_plan:
data_perturbation_plan:
aggregation_rule:
decision_thresholds:

[REPRODUCIBILITY]
code_commit:
config_hash:
environment_hash:
seed_policy:
numeric_tolerances:
```

Une entrée manquante ne peut être complétée après lecture des résultats sans déclencher le traitement prévu pour une modification postérieure.

---

## 8. Catalogue des stress-tests

### 8.1 Socle commun obligatoire

Sauf impossibilité matérielle documentée, tout processus doit couvrir :

1. stabilité paramétrique ;
2. stabilité temporelle ;
3. concentration et outliers ;
4. frictions et exécution ;
5. qualité et perturbation plausible des données ;
6. cohérence avec la portée économique de l’hypothèse ;
7. dépendances dominantes susceptibles d’expliquer l’edge.

### 8.2 Tests conditionnels

Des tests supplémentaires deviennent obligatoires lorsque leur risque est matériel pour la stratégie, notamment :

- stabilité cross-sectionnelle pour une hypothèse prétendant se généraliser à plusieurs actifs ;
- disponibilité short pour une stratégie vendeuse ;
- borrow et recall pour des actifs difficiles à emprunter ;
- impact et capacité pour une stratégie sensible à la liquidité ;
- latence et partial fills pour une stratégie à horizon court ;
- changements de fournisseur pour une donnée propriétaire ou fragile ;
- corporate actions pour les actions ;
- financement et marge pour les stratégies levier ;
- corrélation et concentration pour les portefeuilles multi-actifs ;
- dépendance à un régime lorsque le rationnel économique l’implique.

### 8.3 Test non applicable

Un test ne peut être classé `NOT_APPLICABLE` que si :

- l’absence de matérialité est justifiée ;
- la justification est préenregistrée ;
- une revue indépendante l’approuve ;
- le statut est conservé dans la matrice.

Un test matériel impossible faute de données n’est pas `NOT_APPLICABLE`. Il produit `INCONCLUSIVE` ou `NOT_VALIDATED` selon la règle de décision préenregistrée.

---

## 9. Stabilité paramétrique

### 9.1 Paramètres matériels

Un paramètre est matériel si sa variation plausible peut modifier :

- les signaux ;
- les positions ;
- le P&L ;
- l’exposition ;
- le turnover ;
- les coûts ;
- l’éligibilité ;
- le classement ;
- le verdict.

Tous les paramètres matériels doivent être identifiés.

### 9.2 Voisinage local

Pour un paramètre continu $p_j$ :

$$
p'_j \in
\left\{
p_j-\Delta_{j,m},
\ldots,
p_j,
\ldots,
p_j+\Delta_{j,m}
\right\}
$$

Les amplitudes sont déterminées à partir :

- de la résolution économique ;
- de l’incertitude d’estimation ;
- de la fréquence des données ;
- de la granularité d’exécution ;
- de la variation plausible en production ;
- des contraintes de domaine.

La grille doit couvrir le voisinage matériel sans prétendre qu’une distance relative identique convient à tous les paramètres.

### 9.3 Interactions

La procédure normative est fondée sur le risque :

- voisinage local pour tous les paramètres matériels ;
- interactions préspécifiées lorsque plusieurs paramètres peuvent modifier conjointement le comportement ;
- grille factorielle exhaustive uniquement si elle est justifiée et calculatoirement défendable ;
- variation univariée seule uniquement si l’absence d’interactions matérielles est démontrée.

Le choix rétrospectif des interactions les plus favorables est interdit.

### 9.4 Mesures

Rapporter au minimum :

- performance relative au centre ;
- pente locale ;
- dispersion ;
- proportion de voisins au-dessus du hurdle ;
- largeur du plateau acceptable ;
- continuité des signaux ;
- continuité de l’exposition ;
- continuité du turnover ;
- continuité des coûts ;
- distance entre centre et frontière d’échec ;
- interactions matérielles observées.

La robustesse exige une région préspécifiée acceptable. Un point central supérieur entouré de voisins en échec constitue un pic isolé.

---

## 10. Stabilité temporelle et régimes

Les découpages doivent être définis sans utiliser leur performance :

- blocs calendaires ;
- régimes économiques préspécifiés ;
- volatilité haute, médiane ou basse ;
- tendance haussière, baissière ou latérale ;
- liquidité haute ou basse ;
- périodes de stress ;
- périodes structurelles pertinentes pour l’hypothèse.

La définition d’un régime doit préciser :

- les variables utilisées ;
- les seuils ;
- la disponibilité point-in-time ;
- la règle de classification ;
- les dates ou la procédure de construction ;
- les tailles minimales ;
- la conséquence d’une couverture insuffisante.

Les statistiques par sous-période sont secondaires sauf si un gate par régime a été préenregistré.

Il est interdit :

- de découper jusqu’à trouver une période positive ;
- d’exclure une période défavorable après observation ;
- de remplacer le gate global par le pourcentage de sous-périodes gagnantes ;
- de traiter des segments trop courts comme preuve de stabilité.

---

## 11. Stabilité cross-sectionnelle

Le plan doit déclarer la portée attendue de l’hypothèse :

```text
ASSET_SPECIFIC
SECTOR
ASSET_CLASS
MULTI_ASSET
GLOBAL
```

Les actifs testés sont choisis ex ante selon :

- le rationnel économique ;
- les mécanismes de marché ;
- la comparabilité des données ;
- la négociabilité ;
- les contraintes d’exécution ;
- l’univers point-in-time.

Les résultats doivent distinguer :

- stratégie de portefeuille fixe ;
- actifs diagnostiqués séparément ;
- couples règle-actif sélectionnables ;
- univers ou pondérations sélectionnables.

Selon la SOP 03 :

- un portefeuille fixe peut rester une candidate unique ;
- chaque couple règle-actif devient une candidate s’il est sélectionnable ;
- toute restriction d’univers après observation crée une nouvelle candidate ou version ;
- les actifs perdants ne peuvent être omis.

L’échec cross-sectionnel n’entraîne `FAIL` que si la portée déclarée de l’hypothèse exige cette généralisation. Pour une hypothèse explicitement `ASSET_SPECIFIC`, les autres actifs peuvent rester diagnostiques.

---

## 12. Outliers et concentration

### 12.1 Résultat principal

Toute observation valide reste dans la série principale.

Il est interdit :

- de retirer une perte parce qu’elle paraît exceptionnelle ;
- de retirer un événement valide pour améliorer la métrique ;
- de remplacer la série principale par une série winsorisée après observation ;
- de présenter le résultat sans outliers comme vérité historique.

### 12.2 Diagnostics obligatoires

Rapporter au minimum :

- contribution des 1 %, 5 % et 10 % meilleures périodes ;
- contribution des 1 %, 5 % et 10 % pires périodes ;
- contribution des meilleurs et pires trades ;
- concentration par actif ;
- concentration par régime ;
- concentration par événement ;
- asymétrie ;
- kurtosis ou autre diagnostic de queues ;
- part du P&L expliquée par les principales observations ;
- performance sans les $k$ meilleures observations définies ex ante.

### 12.3 Scénarios de retrait ou de plafonnement

Un scénario sans certaines observations valides :

- est un stress-test ;
- conserve un lien vers la série originale ;
- ne modifie pas le résultat central ;
- utilise une règle de retrait préenregistrée ;
- ne peut servir à supprimer définitivement les observations ;
- produit une candidate distincte s’il influence la sélection ou le déploiement.

---

## 13. Frictions et capacité

### 13.1 Modèle central

Le scénario `CENTRAL` utilise le modèle réaliste défini par la SOP 09B.

Il doit déjà inclure, selon la stratégie :

- spread ;
- commissions et taxes ;
- slippage ;
- impact ;
- borrow ;
- financement ;
- latence ;
- partial fills ;
- contraintes de liquidité ;
- contraintes de portefeuille ;
- capital cible.

Un scénario central à coûts nuls ou volontairement optimiste est interdit.

### 13.2 Scénarios plausibles défavorables

Les scénarios `PLAUSIBLE_BASE` modélisent les dégradations crédibles :

- quantiles défavorables de spread ;
- slippage supérieur ;
- impact supérieur ;
- volume disponible réduit ;
- latence plausible supplémentaire ;
- financement défavorable ;
- borrow plus coûteux ou partiellement indisponible ;
- capacité proche du capital cible ;
- dégradation des fills.

Ils sont calibrés à partir :

- de quantiles historiques ;
- de l’incertitude du modèle ;
- de la variation entre fournisseurs ou périodes ;
- du capital et du participation rate ;
- de contraintes observables en production.

### 13.3 Scénarios extrêmes

Les scénarios `EXTREME` représentent des conditions sévères mais documentées.

Ils peuvent inclure :

- coûts multipliés ;
- absence temporaire de liquidité ;
- gaps extrêmes ;
- indisponibilité short ;
- impact exceptionnel ;
- suspension ou contraintes de marché.

`Coûts ×2` peut être utilisé comme scénario extrême, mais jamais comme seule justification de la robustesse des frictions.

---

## 14. Retards et perturbations d’exécution

Tester selon la matérialité :

- délai d’une unité de décision ;
- délai compatible avec la latence réelle ;
- prix moins favorable ;
- absence de fill ;
- fill partiel ;
- expiration ou annulation ;
- réduction de participation ;
- indisponibilité short ;
- rappel de titres ;
- ordre reporté ;
- exécution au prochain prix réellement disponible.

Les perturbations doivent conserver :

- la chronologie signal → ordre → fill → position → P&L ;
- les contraintes de portefeuille ;
- la comptabilité des coûts ;
- le no-lookahead.

Il est interdit d’utiliser un retard ou une règle de fill pour découvrir après coup une variante plus performante sans la traiter comme nouvelle candidate.

---

## 15. Perturbation des données

Les scénarios doivent refléter une incertitude plausible et respecter la SOP 09A.

Ils peuvent inclure :

- timestamps décalés dans les bornes plausibles ;
- délai de publication ;
- valeurs manquantes ;
- barres incomplètes ;
- arrondis ;
- changement de fournisseur ;
- révision de données ;
- correction de corporate actions ;
- changement de calendrier ;
- univers point-in-time alternatif préspécifié ;
- indisponibilité temporaire d’une source.

Chaque scénario précise :

- le défaut simulé ;
- sa justification ;
- son amplitude ;
- les variables touchées ;
- la règle de traitement ;
- l’effet attendu sur la disponibilité ;
- les contrôles no-lookahead.

Il est interdit :

- d’utiliser des données futures pour réparer un trou ;
- d’imputer arbitrairement une valeur favorable ;
- de choisir le fournisseur selon la performance ;
- de modifier silencieusement le snapshot central.

---

## 16. Classes de scénarios

Chaque ligne du plan reçoit obligatoirement une classe.

### `CENTRAL`

Le scénario de référence :

- applique les conventions normatives ;
- doit être réaliste ;
- doit franchir les gates statistiques et économiques applicables ;
- ne peut être choisi après comparaison avec les stress.

### `PLAUSIBLE_BASE`

Scénario défavorable mais raisonnablement susceptible d’être rencontré :

- voisinage paramétrique plausible ;
- coûts défavorables plausibles ;
- retard réaliste ;
- sous-période ou régime requis ;
- perturbation de données crédible ;
- actif appartenant à la portée déclarée.

Ces scénarios peuvent contenir des conditions bloquantes préenregistrées.

### `EXTREME`

Scénario sévère :

- utilisé pour mesurer la vulnérabilité et préparer les limites opérationnelles ;
- n’a pas à être `PASS` sauf décision contraire préenregistrée ;
- ne peut remplacer les scénarios centraux ou plausibles ;
- doit produire une conséquence opérationnelle explicite s’il révèle un risque de ruine, d’illiquidité ou d’exécution impossible.

La classification ne peut être modifiée après observation pour éviter un échec.

---

## 17. Agrégation

### 17.1 Matrice obligatoire

Produire une ligne par scénario :

| Champ | Description |
|---|---|
| `stress_id` | Identifiant immuable |
| `stress_family` | Paramètre, temps, actif, outlier, friction, exécution ou données |
| `scenario_class` | `CENTRAL`, `PLAUSIBLE_BASE` ou `EXTREME` |
| `candidate_id` | Candidate concernée |
| `input_value` | Valeur ou perturbation |
| `primary_metric` | Valeur de la métrique primaire |
| `confidence_interval` | IC applicable |
| `hurdle_margin` | Écart au hurdle |
| `drawdown` | Drawdown selon SOP 08 |
| `turnover` | Turnover |
| `exposure` | Exposition |
| `costs` | Coûts |
| `data_sufficiency` | Suffisance de l’information |
| `gate_id` | Gate applicable |
| `scenario_verdict` | Statut |
| `evidence_path` | Preuve |

### 17.2 Interdiction du score discrétionnaire

Le verdict global ne peut reposer sur :

- une appréciation visuelle ;
- une moyenne simple de performances hétérogènes ;
- le meilleur scénario ;
- un nombre arbitraire de graphiques rassurants ;
- une pondération choisie après observation.

### 17.3 Règle d’agrégation

L’agrégation est une fonction préenregistrée :

$$
V_{\text{robustesse}}
=
g\left(
V_{\text{central}},
V_{\text{plausible}},
V_{\text{extreme}},
S_{\text{données}},
G_{\text{bloquants}}
\right)
$$

Elle distingue :

- conditions nécessaires ;
- conditions bloquantes ;
- seuils quantitatifs ;
- diagnostics secondaires ;
- insuffisance de données ;
- violations méthodologiques ;
- risques extrêmes non bloquants mais opérationnellement matériels.

Un exemple admissible est :

- scénario central au-dessus du hurdle ;
- aucun scénario plausible classé bloquant sous sa limite de perte ;
- au moins $q$ % des voisins paramétriques acceptables ;
- largeur minimale de plateau satisfaite ;
- aucun test matériel manquant ;
- scénarios extrêmes documentés, sans obligation générale de `PASS`.

Les valeurs de $q$, de largeur, de marge et de perte sont propres au projet et fixées ex ante.

---

## 18. Définition des seuils

Les seuils de robustesse sont dérivés avant les résultats à partir :

- du hurdle économique ;
- de l’effet minimal économiquement pertinent ;
- de l’incertitude statistique ;
- de la précision disponible ;
- de la tolérance de production ;
- de la variation attendue des coûts ;
- du capital cible ;
- des limites de risque ;
- de la quantité d’information effective ;
- de la matérialité du scénario.

Une constante universelle ne constitue pas une justification suffisante.

Il est interdit :

- d’exiger seulement une performance positive ;
- de déplacer le seuil après lecture de la matrice ;
- de transformer une métrique secondaire favorable en critère principal ;
- d’abaisser les exigences parce que les données sont insuffisantes.

Lorsque la quantité d’information ne permet pas d’évaluer un seuil matériel, le résultat n’est pas `PASS`.

---

## 19. Statuts décisionnels

Les dimensions statistique, économique, méthodologique et technique restent séparables dans les livrables.

### `PASS`

Le processus est `PASS` si :

- l’architecture Walk-Forward est conforme ;
- le plan est préenregistré ;
- le socle commun est exécuté ;
- les tests conditionnels matériels sont exécutés ou valablement `NOT_APPLICABLE` ;
- le scénario central satisfait les gates applicables ;
- les scénarios plausibles satisfont leurs conditions bloquantes ;
- la stabilité paramétrique satisfait les seuils ;
- aucune dépendance dominante incompatible avec l’hypothèse n’est détectée ;
- aucune contamination n’est constatée ;
- le registre est complet ;
- la revue indépendante est favorable ;
- les artefacts sont reproductibles.

### `NOT_VALIDATED`

Le processus est `NOT_VALIDATED` lorsque la robustesse disponible ne permet pas de franchir un gate confirmatoire sans qu’une violation méthodologique irréparable soit démontrée, notamment lorsque :

- une condition nécessaire n’est pas satisfaite ;
- un test matériel n’apporte pas la preuve exigée ;
- la stabilité attendue n’est pas démontrée ;
- un gate préenregistré reste non franchi.

### `REJECTED_ECONOMIC`

Le processus est `REJECTED_ECONOMIC` lorsque :

- la validité statistique applicable est acquise ;
- mais le scénario central ou un scénario plausible classé économiquement bloquant ne franchit pas le hurdle net ;
- ou les frictions, la capacité ou les contraintes rendent l’edge inexploitable.

### `FAIL`

Le processus est `FAIL` notamment en présence de :

- pic paramétrique isolé classé bloquant ;
- dépendance dominante à quelques observations contraire au plan ;
- portée cross-sectionnelle incompatible avec l’hypothèse déclarée ;
- coûts réalistes détruisant l’edge selon un gate d’échec ;
- exécution impossible ;
- scénario de données révélant un leakage ;
- choix rétrospectif d’un actif, régime, paramètre ou métrique ;
- contamination d’un `OOS_k` ;
- modification post-OOS nécessaire pour rendre le processus acceptable ;
- omission ou falsification d’un stress-test influent.

### `INCONCLUSIVE`

Le processus est `INCONCLUSIVE` notamment lorsque :

- les segments sont trop courts ;
- le nombre d’observations effectives est insuffisant ;
- un stress-test matériel manque de données ;
- l’impact, le borrow ou les frictions ne peuvent être calibrés ;
- un actif externe requis ne dispose pas de données comparables ;
- les résultats dépassent les tolérances de non-déterminisme ;
- une dépendance empêche l’évaluation prévue ;
- les seuils requis n’ont pas été préenregistrés.

`INCONCLUSIVE` n’autorise ni baisse de seuil ni seconde tentative sur les mêmes données.

---

## 20. Relation avec le registre et les tests multiples

Selon la SOP 03, appartient à la famille de recherche toute variante dont le résultat peut influencer :

- la sélection ;
- une modification ;
- l’ouverture OOS ;
- le déploiement.

Cela inclut notamment :

- paramètres voisins ;
- interactions paramétriques ;
- sous-périodes sélectionnables ;
- couples règle-actif sélectionnables ;
- transformations alternatives ;
- métriques alternatives utilisées pour décider ;
- modèles de coûts sélectionnables ;
- règles d’exécution sélectionnables ;
- versions créées après inspection.

Les sorties purement descriptives :

- restent enregistrées ;
- sont séparées des candidates décisionnelles ;
- ne peuvent rétroactivement influencer la sélection ;
- basculent dans la famille décisionnelle si elles sont utilisées pour modifier le processus.

La SOP 05 ne calcule pas elle-même la correction d’inférence multiple. Elle fournit à la SOP 03 et à la SOP 02 :

- les candidates concernées ;
- leurs séries ;
- leur lignage ;
- leur rôle décisionnel ;
- la matrice scellée ;
- le gate de complétude.

La matrice ne peut être scellée avant l’enregistrement de toutes les variantes de robustesse susceptibles d’influencer l’ouverture OOS. Les gates statistiques finaux sont exécutés sur la famille complète applicable.

---

## 21. Analyses après observation de l’OOS

Après observation d’un `OOS_k` ou de l’OOS global, les analyses de robustesse sont exclusivement descriptives.

Elles peuvent :

- documenter une fragilité ;
- alimenter un post-mortem ;
- identifier une nouvelle question de recherche ;
- définir des contrôles futurs ;
- justifier un arrêt ou un archivage ;
- préparer une hypothèse sur de nouvelles données.

Elles ne peuvent pas :

- modifier la candidate ;
- modifier le processus ;
- choisir un voisin paramétrique ;
- restreindre l’univers ;
- changer la métrique ;
- changer le modèle de coûts ;
- reclasser un scénario ;
- autoriser un nouveau test sur le même OOS ;
- produire une variante déployable sur la base des mêmes données.

Si un diagnostic préenregistré échoue après observation de l’OOS :

- le statut et la conséquence ex ante sont appliqués ;
- le modèle est rejeté, archivé ou déclaré inconclusif selon le plan ;
- aucune réparation n’est testée sur le même OOS ;
- toute nouvelle idée exige un nouveau cycle et de nouvelles données vierges.

La gouvernance détaillée de l’accès, de la contamination, du post-mortem et des échecs relève de la SOP 10.

---

## 22. Incidents techniques et réexécutions

La SOP 05 ne peut autoriser seule une réexécution sur un OOS.

Toute réexécution technique relève de la SOP 10 et exige notamment :

- une erreur objective démontrée indépendamment du niveau de performance ;
- une cause identifiée dans le code, les données ou l’infrastructure ;
- la preuve que la logique économique et les paramètres ne changent pas ;
- un correctif minimal ;
- une revue indépendante ;
- la conservation du run initial ;
- une décision écrite antérieure au rerun ;
- l’absence d’utilisation de la performance pour concevoir le correctif.

Si le correctif modifie les signaux, les positions, le P&L potentiel ou la logique économique :

- il crée une nouvelle candidate ;
- le même OOS reste brûlé ;
- aucune réexécution confirmatoire sur ce même OOS n’est autorisée.

---

## 23. Livrables obligatoires

### 23.1 Plan de robustesse

```text
[ROBUSTNESS PLAN]
plan_id:
project_id:
research_family_id:
process_version_id:
fold_id:
candidate_id:
status:
created_at:
approved_by:

[AUTHORITIES]
registry_sop:
walk_forward_sop:
performance_sop:
data_sop:
execution_sop:
oos_governance_sop:
reproducibility_sop:

[SCOPE]
economic_hypothesis:
declared_scope:
material_risks:
common_tests:
conditional_tests:
not_applicable_tests:

[DECISION]
primary_metric:
hurdle:
blocking_gates:
diagnostic_metrics:
aggregation_rule:
status_mapping:
```

### 23.2 Catalogue des stress-tests

```text
[STRESS]
stress_id:
stress_family:
scenario_class:
materiality:
input_object:
central_value:
perturbed_values:
units:
justification:
candidate_effect:
registry_treatment:
gate_id:
failure_consequence:
seed:
```

### 23.3 Manifeste d’exécution

```text
[RUN]
robustness_run_id:
plan_id:
fold_id:
data_snapshot_id:
code_commit:
config_hash:
environment_hash:
started_at:
completed_at:

[INPUTS]
candidate_id:
primary_return_series_hash:
execution_model_version:
stress_catalog_version:

[OUTPUTS]
scenario_matrix_path:
scenario_matrix_hash:
report_path:
report_hash:
log_path:
log_hash:
```

### 23.4 Matrice et rapport

Le rapport doit contenir :

- la matrice complète ;
- les valeurs centrales et perturbées ;
- les IC applicables ;
- les marges au hurdle ;
- les conditions bloquantes ;
- les diagnostics ;
- les tests `NOT_APPLICABLE` ;
- les données insuffisantes ;
- les exceptions ;
- les violations ;
- les décisions ;
- les preuves ;
- les liens vers le registre ;
- les hashes ;
- la revue indépendante.

### 23.5 Verdict

```text
[ROBUSTNESS VERDICT]
plan_id:
process_version_id:
fold_id:
central_status:
plausible_base_status:
extreme_diagnostics:
statistical_status:
economic_status:
methodological_status:
technical_status:
final_status:
oos_opening_authorized:
review_id:
decision_timestamp:
```

---

## 24. Reproductibilité

Une reproduction valide doit retrouver :

- le plan préenregistré ;
- le catalogue des stress-tests ;
- les snapshots de données ;
- la frontière temporelle ;
- la candidate et le processus gelés ;
- le modèle central ;
- les valeurs perturbées ;
- les classes de scénarios ;
- l’ordre des tests ;
- les seeds ;
- les séries de rendement ;
- les métriques ;
- les IC ;
- les matrices ;
- les gates ;
- les statuts ;
- les hashes ;
- le verdict ;
- la décision d’autorisation OOS.

Les artefacts déterministes doivent être reproduits exactement.

Pour un composant non déterministe, le plan doit fixer avant exécution :

- le générateur ;
- l’algorithme ;
- les seeds ;
- le parallélisme ;
- la tolérance numérique ;
- les invariants obligatoires ;
- la distribution attendue ;
- le nombre de répétitions ;
- la conséquence d’un dépassement.

Le gate final exige au minimum le niveau 3 de la SOP 12 :

> un tiers exécute le paquet sans intervention du chercheur et retrouve le verdict dans les tolérances préenregistrées.

Une reproduction approximative du seul verdict ne suffit pas.

---

## 25. Revue indépendante

Une revue indépendante est requise avant :

- le scellement du plan ;
- l’exécution des stress-tests décisionnels ;
- le scellement de la matrice ;
- l’émission du verdict ;
- l’autorisation d’ouverture de chaque `OOS_k` ;
- toute demande de réexécution technique.

Elle contrôle au minimum :

- la séparation des responsabilités entre SOP ;
- la complétude du registre ;
- la frontière temporelle ;
- la disponibilité point-in-time ;
- la matérialité des tests ;
- la justification des amplitudes ;
- les interactions paramétriques ;
- la portée cross-sectionnelle ;
- la classification des scénarios ;
- le modèle central de coûts ;
- les seuils ;
- la fonction d’agrégation ;
- les statuts ;
- l’absence de sélection post-OOS ;
- les hashes ;
- la reproductibilité.

La personne ayant conçu ou optimisé la candidate ne peut être l’unique reviewer.

---

## 26. Erreurs interdites

- Ajouter un holdout final après l’OOS Walk-Forward global.
- Exécuter plusieurs variantes sur `OOS_k` puis choisir la meilleure.
- Utiliser un résultat OOS pour modifier un fold futur.
- Appliquer arbitrairement `±5 %` à tous les paramètres.
- Tester uniquement les paramètres faciles ou favorables.
- Ignorer des interactions matérielles sans justification.
- Choisir les interactions après observation.
- Découper les périodes jusqu’à trouver un résultat positif.
- Restreindre l’univers aux actifs gagnants.
- Omettre les actifs ou variantes perdants du registre.
- Retirer des observations valides du résultat principal.
- Winsoriser après observation pour améliorer la métrique.
- Utiliser zéro coût comme scénario central.
- Utiliser `coûts ×2` comme unique preuve.
- Déclarer robuste une stratégie dépendant d’une exécution parfaite.
- Choisir un fournisseur selon la performance.
- Utiliser des données futures pour réparer une perturbation.
- Classer après coup un scénario échoué comme extrême.
- Construire le verdict par inspection visuelle.
- Moyenner des scénarios hétérogènes sans règle préenregistrée.
- Sélectionner le meilleur scénario.
- Abaisser un seuil faute de données.
- Transformer `INCONCLUSIVE` en `PASS`.
- Confondre `REJECTED_ECONOMIC` et absence de preuve statistique.
- Utiliser un diagnostic post-OOS pour accorder une seconde chance.
- Appeler un mauvais résultat « bug » sans preuve indépendante.
- Réexécuter une correction logique sur le même OOS.
- Conserver uniquement une equity curve ou un rapport agrégé.

---

## 27. Relations normatives avec les autres SOP

### SOP 01 — Estimation et intervalle de confiance OOS

La SOP 05 autorise ou interdit l’ouverture de chaque `OOS_k`. La SOP 01 estime ensuite la performance du processus à partir de la série OOS concaténée.

### SOP 02 — Inférence multiple

La SOP 05 identifie les variantes influentes. La SOP 02 définit leur traitement statistique lorsqu’elles appartiennent à une comparaison multiple.

### SOP 03 — Registre des expériences

La SOP 03 enregistre les stress-tests, candidates, runs, observations, décisions, matrices, hashes et lignages. Elle détermine la famille statistique opposable.

### SOP 04 — Segmentation temporelle et Walk-Forward

La SOP 04 fournit le calendrier, les données autorisées avant chaque frontière et l’architecture sans holdout final supplémentaire.

### SOP 07 — Detrending et zero-centering

Les transformations utilisées dans les scénarios restent conformes à la SOP 07. Une transformation alternative décisionnelle crée une variante enregistrée.

### SOP 08 — Mesures de performance

La SOP 08 fournit la série primaire, la métrique, le hurdle et les métriques secondaires. La SOP 05 ne peut changer de métrique après observation.

### SOP 09A — Données point-in-time

La SOP 09A définit les snapshots, la disponibilité et les contrôles no-lookahead applicables aux perturbations de données.

### SOP 09B — Exécution, frictions, capacité et sizing

La SOP 09B définit le modèle central et les paramètres d’exécution. La SOP 05 organise leurs scénarios de stress et leurs conséquences.

### SOP 10 — Gouvernance OOS et gestion des échecs

La SOP 05 gouverne les tests de robustesse avant OOS. La SOP 10 gouverne l’accès, la contamination, les résultats OOS, les post-mortems et les réexécutions techniques.

### SOP 12 — Reproductibilité

La SOP 12 assemble les artefacts de la SOP 05 dans le paquet final et contrôle la reproduction indépendante.

---

## 28. Sources internes

- `Protocole/PROTOCOLE EBTA.md`
- `Protocole/SOP 01 - Estimation et intervalle de confiance OOS.md`
- `Protocole/SOP 02 - Inférence multiple WRC SPA Romano-Wolf MCP.md`
- `Protocole/SOP 03 - Registre des expériences et univers des règles candidates.md`
- `Protocole/SOP 04 - Segmentation temporelle et Walk-Forward.md`
- `Protocole/SOP 07 - Detrending benchmark et zero-centering.md`
- `Protocole/SOP 08 - Mesures de performance et série de rendement de référence.md`
- `Protocole/SOP 09A - Données point-in-time et contrôles anti-leakage.md`
- `Protocole/SOP 09B - Modèle d’exécution frictions capacité et sizing.md`
- `Protocole/SOP 10 - Gouvernance OOS et gestion des échecs.md`
- `Protocole/SOP 12 - Reproductibilité et paquet de validation EBTA.md`
- `Notes/104-Les Cinq Facteurs du Biais de Minage de Données.md`
- `Notes/110-L'Illusion du Profit L'Impact des Valeurs Extrêmes en Trading.md`
- `Notes/121-La Validation Hors-Échantillon L'Épreuve de Réalité Statistique.md`
- `Notes/123-L'Éphémère Rigueur Limites des Tests Hors-Échantillon.md`
- `Notes/168-GESTION RIGOUREUSE DE L’ÉCHEC EN VALIDATION OUT-OF-SAMPLE (OOS).md`
- `Notes/173-Le rôle de l'OOS, estimation et stabilité dans l'EBTA.md`

---

## 29. Décision méthodologique synthétique

> **Le protocole EBTA évalue la robustesse du processus Walk-Forward avant l’ouverture de chaque segment `OOS_k`, à partir des seules données alors disponibles. Les stress-tests décisionnels sont préenregistrés, enregistrés dans la famille de recherche et agrégés par des gates mécaniques. Le plan combine un socle commun et des tests conditionnels fondés sur les risques matériels de l’hypothèse, des données et de l’exécution. La stabilité paramétrique porte sur un voisinage local de tous les paramètres matériels et sur les interactions préspécifiées pertinentes. Les observations valides restent dans le résultat principal ; leur retrait n’est qu’un scénario de stress. Le scénario central de coûts est déjà réaliste, les scénarios plausibles peuvent être bloquants et les scénarios extrêmes sont principalement diagnostiques. Les verdicts distinguent `PASS`, `NOT_VALIDATED`, `REJECTED_ECONOMIC`, `FAIL` et `INCONCLUSIVE`. Après observation d’un OOS, aucune analyse ne peut servir à réparer, sélectionner ou revalider sur les mêmes données. Les segments OOS concaténés constituent l’unique OOS global ; aucun holdout final supplémentaire n’est ajouté.**
