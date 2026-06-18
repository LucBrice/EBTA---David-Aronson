# SOP 04 — Segmentation temporelle et Walk-Forward
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 04 |
| Rôle dans le paquet EBTA | Segmentation temporelle, Walk-Forward, folds, purge, embargo et OOS global. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## 1. Statut du document

- **Type :** Standard Operating Procedure méthodologique.
- **Statut :** Spécification normative du protocole de segmentation temporelle.
- **Architecture principale :** Walk-Forward à segments OOS successifs non chevauchants.
- **Objet validé :** processus complet de sélection et de recalibration tel qu’il doit être exécuté en production.
- **Objet OOS global :** série chronologique concaténée des rendements des segments OOS.
- **Holdout final supplémentaire :** aucun.

Cette SOP définit :

- les fonctions respectives de `Train`, `Test` et `OOS` ;
- le calendrier des folds ;
- le dimensionnement des fenêtres ;
- le warm-up, la purge et l’embargo ;
- les règles de déplacement et de recalibration ;
- la gestion des positions aux frontières ;
- les cas d’insuffisance ou d’échec local ;
- les livrables et preuves de reproductibilité.

Elle ne définit pas :

- les algorithmes WRC, SPA, Romano–Wolf ou MCP, régis par la SOP 02 ;
- le registre opposable des candidates et expériences, régi par la SOP 03 ;
- la construction de l’intervalle de confiance OOS, régie par la SOP 01 ;
- le detrending et le zero-centering, régis par la SOP 07 ;
- le modèle d’exécution et de coûts, régi par la SOP 09B.

---

## 2. Objectif méthodologique

Le Walk-Forward valide une **stratégie apprenante**, c’est-à-dire le processus mécanique qui :

1. reçoit uniquement les données disponibles à la date du fold ;
2. calibre les paramètres sur `Train_k` ;
3. sélectionne la structure et la complexité sur `Test_k` ;
4. applique les gates statistiques prévus ;
5. gèle la candidate locale ;
6. l’exécute une seule fois sur `OOS_k` ;
7. recommence selon la fréquence de recalibration prévue en production.

Le verdict ne porte donc pas sur une règle fixe choisie une fois pour toutes, mais sur la capacité du processus préenregistré à produire successivement des règles exploitables sans utiliser d’information future.

---

## 3. Architecture normative

### 3.1 Walk-Forward obligatoire

L’architecture confirmatoire principale est :

```text
Fold 1 : [Warm-up][Train_1][Purge][Test_1][Purge/Embargo][OOS_1]
Fold 2 :       [Warm-up][Train_2][Purge][Test_2][Purge/Embargo][OOS_2]
...
Fold K :                         [Warm-up][Train_K][Purge][Test_K][Purge/Embargo][OOS_K]
```

Les segments `OOS_k` :

- sont strictement chronologiques ;
- ne se chevauchent pas ;
- ne sont ouverts qu’après les gates et le gel du fold correspondant ;
- forment collectivement l’unique OOS confirmatoire du processus.

Le fold unique peut être utilisé comme analyse exploratoire ou pédagogique, mais il ne constitue pas l’architecture confirmatoire normative de cette SOP.

### 3.2 Trois fonctions distinctes dans chaque fold

Chaque fold conserve obligatoirement trois fonctions :

- **Train :** calibration des paramètres et apprentissage autorisé ;
- **Test :** sélection de la structure ou de la complexité et inférence multiple ;
- **OOS :** estimation passive de la performance du processus localement gelé.

Il est interdit :

- de fusionner `Train` et `Test` pour augmenter artificiellement la taille d’apprentissage ;
- de sélectionner directement une candidate sur `OOS_k` ;
- d’utiliser `OOS_k` comme un second Test ;
- d’ouvrir `OOS_k` lorsqu’aucune politique ex ante ne l’autorise.

---

## 4. Préenregistrement

Avant l’exécution du premier fold, le protocole doit figer :

- la fréquence des données ;
- le calendrier et le fuseau horaire ;
- la fréquence de décision ;
- l’horizon de détention maximal ;
- le lookback maximal ;
- l’horizon futur maximal des labels ;
- la fréquence de recalibration prévue en production ;
- les longueurs `Train`, `Test` et `OOS` ;
- le nombre minimal de folds ;
- le pas de déplacement ;
- le warm-up ;
- la règle de purge ;
- la règle et la durée éventuelle d’embargo ;
- la gestion des positions aux frontières ;
- les règles de sélection et de tie-break ;
- la politique applicable si aucun candidat ne passe le Test ;
- les critères `PASS`, `NOT_VALIDATED`, `REJECTED_ECONOMIC`, `FAIL` et `INCONCLUSIVE` ;
- les versions du code, des données, des configurations et du modèle de coûts.

Les ratios usuels tels que `50/25/25` ou `70/15/15` ne constituent pas une justification méthodologique.

---

## 5. Unité temporelle et disponibilité de l’information

Les frontières sont définies à partir :

- de l’unité de décision ;
- du calendrier réel du marché ;
- de l’horizon maximal pendant lequel une information, un label, une position ou un P&L peut affecter un segment voisin.

Un nombre de barres ou de trades clôturés ne suffit pas à définir une frontière valide.

Pour toute observation utilisée dans un fold, le protocole doit pouvoir démontrer qu’elle était effectivement disponible au point de décision correspondant.

Les conventions temporelles doivent rester identiques entre :

- la recherche ;
- la validation Walk-Forward ;
- l’incubation ;
- la production.

---

## 6. Dimensionnement des fenêtres

### 6.1 Principe

Les longueurs de `Train`, `Test` et `OOS` sont déterminées avant les résultats par une combinaison documentée de :

- puissance statistique cible ;
- effet minimal économiquement pertinent ;
- variance de référence ;
- nombre de périodes ;
- nombre de décisions ;
- nombre de trades ;
- nombre effectif d’observations ;
- nombre approximatif de blocs distincts ;
- taille de l’univers candidat ;
- fréquence de recalibration ;
- horizon prévu de déploiement avant la recalibration suivante.

Il est interdit de choisir les longueurs selon la performance observée.

### 6.2 Taille du Train

`Train_k` doit contenir assez d’information pour :

- calculer toutes les features ;
- calibrer les paramètres ;
- couvrir les états ou régimes exigés par le préenregistrement ;
- limiter la variance de l’estimation locale ;
- rendre l’apprentissage techniquement et économiquement défendable.

### 6.3 Taille du Test

`Test_k` doit permettre :

- la comparaison de la famille locale complète ;
- la sélection de la structure et de la complexité ;
- l’exécution des procédures de la SOP 02 ;
- l’application du gate d’autorisation OOS.

### 6.4 Taille de l’OOS

`OOS_k` doit :

- correspondre à la période de déploiement prévue avant recalibration ;
- fournir une mesure économiquement interprétable ;
- contribuer à une série globale suffisamment précise ;
- rester strictement non chevauchant avec les autres OOS.

### 6.5 Nombre minimal de folds

Le nombre minimal de folds est préenregistré et justifié par :

- la précision globale visée ;
- la couverture temporelle ou de régimes ;
- le nombre effectif d’observations OOS ;
- les besoins de diagnostic de stabilité.

Aucune formule universelle de type :

```text
K = floor(N / N_min)
```

ni aucune plage arbitraire telle que `3 à 10 folds` ne constitue une justification suffisante.

---

## 7. Fenêtre d’entraînement

### 7.1 Règle par défaut

La fenêtre d’entraînement normative est **rolling**, de longueur fixe :

$$
Train_k=[t_k-W+1,t_k]
$$

où $W$ est préenregistré avant l’ouverture du premier OOS.

Cette convention représente un processus de recalibration dans lequel les données anciennes sortent progressivement de l’échantillon d’apprentissage.

### 7.2 Dérogation

Une fenêtre expanding n’est admise que comme dérogation explicitement justifiée et préenregistrée avant toute exécution confirmatoire :

$$
Train_k=[t_0,t_k]
$$

La dérogation crée une variante de protocole distincte. Il est interdit de comparer rolling et expanding sur leurs résultats puis de retenir rétrospectivement la meilleure architecture.

---

## 8. Pas de déplacement

Le pas de déplacement doit correspondre :

- à la durée de `OOS_k` ;
- à la fréquence de recalibration prévue en production.

Exemple :

```text
recalibration prévue : trimestrielle
durée OOS : 3 mois
pas : 3 mois
```

Il est interdit de choisir le pas dans le seul but :

- d’augmenter le nombre de folds ;
- d’améliorer la performance ;
- d’éviter une période défavorable ;
- de modifier la pondération implicite des régimes.

---

## 9. Warm-up

Le warm-up utilise exclusivement des observations antérieures qui étaient disponibles à la date du segment.

Pour chaque fold :

- le warm-up couvre le lookback maximal des indicateurs et états internes ;
- aucune donnée postérieure à la frontière ne peut être utilisée ;
- les rendements produits pendant le warm-up ne sont pas évalués ;
- le warm-up ne permet pas d’accéder aux résultats d’un OOS antérieur comme variable de sélection ;
- les conventions restent identiques à celles de la production.

Les données de warm-up et la première observation évaluée doivent être identifiables dans le manifeste du fold.

---

## 10. Purge

La purge retire les observations dont les labels, positions ou P&L utilisent une information appartenant au segment voisin.

Sa durée minimale est égale à l’horizon futur maximal par lequel un élément du processus peut traverser une frontière.

La purge est obligatoire notamment lorsqu’ :

- un signal à $t$ est évalué sur $t+H$ ;
- une cible utilise une fenêtre future ;
- des trades se chevauchent ;
- une position peut rester ouverte après la frontière ;
- un calcul de P&L dépend d’un prix postérieur ;
- une feature n’était pas réellement disponible au point de décision.

La durée moyenne des trades ne constitue pas une borne conservatrice suffisante lorsque certains trades durent plus longtemps.

---

## 11. Embargo

L’embargo n’est pas systématique.

Il devient obligatoire lorsqu’une dépendance résiduelle justifiée subsiste après la purge, notamment en raison :

- de la microstructure ;
- d’événements communs ;
- d’une dépendance sérielle persistante ;
- d’une latence de disponibilité ;
- d’un état de stratégie ou de portefeuille non neutralisé par la purge.

Lorsqu’il est utilisé, l’embargo doit :

- être préenregistré ;
- être exprimé en unités temporelles explicites ;
- suivre une règle mécanique identique entre folds ;
- être justifié indépendamment des performances ;
- être inclus dans les contrôles de reproductibilité.

Il est interdit d’ajuster sa durée après observation des résultats.

---

## 12. Positions ouvertes aux frontières

Une position ouverte à une frontière est traitée selon une convention ex ante cohérente avec l’exploitation prévue.

La convention doit préciser :

- si la position peut traverser la frontière ;
- si une clôture mécanique est requise ;
- l’instant et le prix d’exécution applicables ;
- l’attribution quotidienne du P&L mark-to-market ;
- l’attribution des coûts ;
- l’effet sur la purge ;
- l’effet sur l’exposition du premier jour du segment suivant.

Une clôture artificielle systématique n’est autorisée que si elle reproduit réellement la politique de production préenregistrée.

Une position ne peut jamais traverser silencieusement une frontière.

---

## 13. Exécution d’un fold

Pour chaque fold `k`, l’ordre suivant est obligatoire :

1. charger le snapshot de données autorisé ;
2. appliquer le calendrier, le warm-up, la purge et l’embargo ;
3. calibrer les paramètres sur `Train_k` ;
4. produire la famille locale complète ;
5. évaluer la structure et la complexité sur `Test_k` ;
6. construire et sceller la matrice locale selon la SOP 03 ;
7. appliquer l’inférence multiple et les gates de la SOP 02 ;
8. appliquer la politique préenregistrée en cas d’absence de candidat admissible ;
9. geler la candidate, la configuration et la version du processus ;
10. obtenir la revue indépendante et l’autorisation d’ouverture ;
11. exécuter une seule fois sur `OOS_k` ;
12. enregistrer la série quotidienne OOS et les diagnostics ;
13. déplacer les fenêtres selon le pas préenregistré.

---

## 14. Absence de candidat admissible

Si aucun candidat ne passe le gate Test d’un fold, il est interdit :

- de choisir le candidat le moins mauvais ;
- de retenir le meilleur Sharpe Train ;
- de réduire l’univers après observation ;
- de modifier les seuils ;
- d’ouvrir l’OOS pour « apprendre ».

Le protocole doit choisir avant le premier fold l’une des politiques suivantes :

### `NO_MODEL`

- aucun modèle n’est déployé pendant `OOS_k` ;
- la série quotidienne conserve les jours correspondants selon la convention de portefeuille préenregistrée ;
- l’absence de modèle est une sortie légitime du processus ;
- le fold et sa cause restent intégralement documentés.

### `STOP_PROCESS`

- le processus s’arrête ;
- aucun OOS ultérieur n’est ouvert ;
- le verdict global devient `NOT_VALIDATED` ou `INCONCLUSIVE` selon la cause ;
- toute relance avec une procédure modifiée constitue une nouvelle version.

La politique ne peut pas varier discrétionnairement entre folds.

---

## 15. Insuffisance locale

Un fold est insuffisant lorsqu’il ne respecte pas un minimum préenregistré portant notamment sur :

- les périodes ;
- les décisions ;
- les trades ;
- les observations effectives ;
- les blocs distincts ;
- la couverture de données ;
- la puissance requise.

Dans ce cas :

- les seuils ne sont pas abaissés ;
- le fold n’est pas fusionné rétrospectivement avec un voisin ;
- aucune donnée manquante n’est remplacée arbitrairement par zéro ;
- son OOS n’est pas utilisé comme confirmation ;
- le statut est `INCONCLUSIVE`.

Si l’insuffisance remet en cause l’architecture globale préenregistrée, le processus global est également `INCONCLUSIVE`.

---

## 16. Adaptation entre folds

Sont autorisés :

- la recalibration mécanique prévue ;
- la sélection dans l’espace candidat préenregistré ;
- l’application de la même règle de complexité ;
- l’actualisation des données disponibles à la date du fold ;
- les adaptations explicitement codées et préenregistrées qui ne dépendent pas du signe ou du niveau de `OOS_k`.

Sont interdits :

- l’ajout d’un filtre après un échec OOS ;
- la modification de l’univers ;
- le changement de métrique ;
- le changement de fenêtre ;
- le changement de modèle de coûts ;
- l’ajustement des seuils ;
- toute décision influencée par la performance observée de `OOS_k`.

Un changement imprévu de logique, d’univers, de métrique, de coûts ou de calendrier :

- crée un nouveau `PROCESS_VERSION_ID` ;
- clôt la version antérieure ;
- interdit d’agréger naïvement les OOS antérieurs et postérieurs comme un test homogène ;
- exige une nouvelle justification et un nouveau préenregistrement.

---

## 17. OOS global

La sortie primaire est la série chronologique concaténée :

$$
D_{OOS}=
\left[
d^{OOS_1},
d^{OOS_2},
\ldots,
d^{OOS_K}
\right]
$$

Cette série :

- respecte l’ordre chronologique ;
- conserve les jours valides sans position ;
- utilise les rendements quotidiens nets mark-to-market ;
- inclut les coûts et expositions réellement simulés ;
- respecte les transformations définies dans les SOP 01, 07, 08 et 09B.

Le verdict global est produit selon la SOP 01 à partir de cette série.

Ne constituent pas des gates confirmatoires primaires :

- la moyenne simple des Sharpes de folds ;
- la médiane des performances ;
- le nombre de folds gagnants ;
- un seuil de 50 % ou 75 % de folds positifs.

Ces statistiques peuvent être publiées comme diagnostics secondaires.

---

## 18. Dépendance entre folds

Le non-chevauchement des OOS ne suffit pas à démontrer l’indépendance complète des folds.

Une dépendance peut subsister en raison :

- du chevauchement des fenêtres Train ;
- du même générateur de candidates ;
- de régimes persistants ;
- d’expositions communes ;
- d’un état de portefeuille partagé ;
- d’une même procédure adaptative.

Toute méthode d’inférence doit utiliser une structure de dépendance cohérente avec la série temporelle réelle. Il est interdit de traiter les folds comme des observations IID sans justification.

---

## 19. Diagnostics par fold

Chaque fold doit rapporter au minimum :

- ses dates exactes ;
- le snapshot de données disponible ;
- la version du processus ;
- les longueurs des fenêtres ;
- le warm-up, la purge et l’embargo ;
- l’univers local ;
- le nombre de candidates ;
- la candidate et les paramètres sélectionnés ;
- la complexité ;
- les résultats et gates du Test ;
- la p-value corrigée applicable ;
- la politique appliquée en l’absence de modèle ;
- la série quotidienne OOS ;
- la performance OOS ;
- le nombre de trades ;
- l’exposition ;
- les coûts ;
- les diagnostics de régime ;
- la distance entre paramètres successifs.

Une forte instabilité des paramètres est un diagnostic de fragilité.

Elle ne produit automatiquement `FAIL` que si :

- la métrique d’instabilité ;
- son seuil ;
- et la conséquence décisionnelle

ont été préenregistrés.

---

## 20. Statuts décisionnels

### `PASS`

Le processus est `PASS` si :

- l’architecture est préenregistrée et respectée ;
- les tailles minimales sont satisfaites ;
- les OOS ne se chevauchent pas ;
- le warm-up, la purge et l’embargo sont conformes ;
- aucun OOS n’a influencé un fold ultérieur ;
- le processus est reproductible ;
- le gate statistique global défini par la SOP 01 est satisfait ;
- le gate économique est satisfait.

### `NOT_VALIDATED`

Le processus est `NOT_VALIDATED` lorsque les preuves disponibles ne permettent pas de franchir le gate statistique confirmatoire sans qu’une violation méthodologique irréparable soit démontrée.

### `REJECTED_ECONOMIC`

Le processus est `REJECTED_ECONOMIC` lorsque le gate statistique applicable est satisfait, mais que la performance nette ne franchit pas le hurdle économique préenregistré.

### `FAIL`

Le processus est `FAIL` notamment en présence de :

- leakage ;
- influence d’un OOS sur un fold futur ;
- modification rétrospective des fenêtres ou seuils ;
- ouverture OOS non autorisée ;
- changement non déclaré de processus ;
- falsification ou omission d’un fold ;
- violation volontaire de la politique d’absence de candidat ;
- performance globale sous un critère classé explicitement comme gate d’échec.

### `INCONCLUSIVE`

Le processus est `INCONCLUSIVE` notamment en présence de :

- trop peu de folds ;
- trop peu d’observations effectives ;
- puissance insuffisante ;
- données locales invalides ou manquantes ;
- dépendance empêchant l’inférence prévue ;
- fold requis non reconstructible ;
- couverture de régime obligatoire non atteinte ;
- résultat global trop imprécis pour statuer.

Les statuts statistiques, économiques, méthodologiques et techniques doivent rester distinguables dans les livrables.

---

## 21. Relations normatives avec les autres SOP

### SOP 01 — Estimation et intervalle de confiance OOS

La SOP 04 produit les segments `OOS_k` et leur concaténation chronologique. La SOP 01 définit l’estimation, l’intervalle de confiance et le gate global appliqués à cette série.

### SOP 02 — Inférence multiple

La SOP 04 définit les fenêtres et les points d’application. La SOP 02 définit les calculs WRC, SPA, Romano–Wolf et MCP ainsi que leurs gates.

La SOP 04 ne doit pas dupliquer ces algorithmes.

### SOP 03 — Registre des expériences

La SOP 03 trace :

- chaque fold ;
- chaque candidate ;
- chaque matrice locale ;
- chaque adaptation ;
- chaque changement de version ;
- chaque autorisation et ouverture OOS ;
- chaque sortie et événement de décision.

### SOP 07 — Detrending et zero-centering

La SOP 07 définit les transformations statistiques appliquées aux séries produites par les fenêtres de la SOP 04.

### SOP 09A — Données point-in-time et anti-leakage

La SOP 09A établit la disponibilité point-in-time des observations et les contrôles anti-lookahead utilisés pour valider les frontières.

### SOP 09B — Exécution, frictions, capacité et sizing

La SOP 09B définit les conventions de prix, coûts, slippage, financement, expositions et P&L utilisées dans chaque segment.

### SOP 12 — Reproductibilité

La SOP 12 assemble le paquet final de validation et contrôle la reproduction des calendriers, folds, artefacts et verdicts.

---

## 22. Livrables obligatoires

### 22.1 Configuration versionnée

```text
[WINDOW_DESIGN]
process_version_id:
mode: walk_forward
train_window_type: rolling
train_length:
test_length:
oos_length:
step:
minimum_fold_count:
calendar:
timezone:
decision_frequency:
recalibration_frequency:

[BOUNDARIES]
maximum_lookback:
maximum_label_horizon:
maximum_holding_period:
warmup:
purge:
embargo:
boundary_position_policy:

[POWER]
minimum_effect:
variance_assumption:
target_power:
minimum_periods:
minimum_trades:
minimum_effective_observations:
minimum_distinct_blocks:

[FAILURE_POLICY]
no_candidate_policy: NO_MODEL | STOP_PROCESS
insufficient_fold_policy: INCONCLUSIVE
```

### 22.2 Manifeste par fold

```text
[IDENTIFICATION]
fold_id:
process_version_id:
data_snapshot_id:
code_commit:
config_hash:
environment_hash:
seed:

[DATES]
warmup_start:
train_start:
train_end:
test_start:
test_end:
oos_start:
oos_end:

[SELECTION]
candidate_catalog_id:
matrix_id:
candidate_count:
selected_candidate_id:
selected_parameters:
complexity:
corrected_pvalue:
test_gate:
no_candidate_policy_applied:

[OOS]
opening_authorization_id:
opened_at:
daily_return_series_path:
return_series_hash:
trade_count:
exposure:
costs:
fold_status:
```

### 22.3 Livrable global

```text
[GLOBAL]
process_version_id:
fold_count:
concatenated_oos_path:
concatenated_oos_hash:
point_estimate:
confidence_interval:
statistical_gate:
economic_gate:
methodological_status:
final_verdict:
review_id:
```

---

## 23. Reproductibilité

Une reproduction valide doit retrouver exactement :

- le calendrier des folds ;
- les snapshots de données ;
- les frontières ;
- le warm-up, la purge et l’embargo ;
- les configurations ;
- les seeds ;
- les catalogues de candidates ;
- les matrices locales ;
- les résultats de sélection ;
- les candidates gelées ;
- les séries quotidiennes OOS ;
- la série OOS concaténée ;
- les hashes des artefacts déterministes ;
- les statuts et décisions.

Une reproduction approximative du verdict final ne suffit pas.

Toute tolérance numérique applicable à un composant non déterministe doit être préenregistrée avec :

- la métrique comparée ;
- la tolérance ;
- les invariants obligatoires ;
- la conséquence d’un dépassement.

---

## 24. Revue indépendante

Une revue indépendante est requise avant :

- le scellement de chaque matrice locale ;
- l’ouverture de chaque `OOS_k` ;
- le scellement de la série OOS globale ;
- l’émission du verdict final.

Elle contrôle notamment :

- le respect du calendrier ;
- la disponibilité point-in-time ;
- le dimensionnement ;
- la purge et l’embargo ;
- la gestion des positions aux frontières ;
- la complétude du registre ;
- la conformité des matrices ;
- la version du processus ;
- l’absence d’influence OOS ;
- la reproductibilité.

---

## 25. Erreurs interdites

- Imposer un ratio `50/25/25` sans justification.
- Choisir le nombre de folds par une formule arbitraire.
- Choisir rétrospectivement rolling ou expanding.
- Faire chevaucher les segments OOS.
- Oublier les jours sans position.
- Utiliser une donnée future pour le warm-up.
- Sous-dimensionner la purge selon la durée moyenne des trades.
- Laisser une position traverser une frontière sans convention.
- Modifier l’embargo selon les performances.
- Utiliser `OOS_k` pour améliorer le fold suivant.
- Ouvrir l’OOS lorsque le gate Test a échoué.
- Choisir le candidat le moins mauvais.
- Réduire les seuils d’un fold insuffisant.
- Fusionner rétrospectivement des fenêtres.
- Imputer arbitrairement une observation manquante par zéro.
- Modifier l’univers, la métrique ou les coûts sans changer de version.
- Agréger comme homogènes des OOS issus de versions différentes.
- Moyenniser les Sharpes comme verdict primaire.
- Utiliser le pourcentage de folds positifs comme gate confirmatoire.
- Traiter les folds comme IID sans justification.
- Déclarer `FAIL` pour instabilité sans seuil préenregistré.
- Conserver uniquement une equity curve ou des métriques agrégées.

---

## 26. Sources internes

- `Protocole/PROTOCOLE EBTA.md`
- `Protocole/SOP 01 - Estimation et intervalle de confiance OOS.md`
- `Protocole/SOP 02 - Inférence multiple WRC SPA Romano-Wolf MCP.md`
- `Protocole/SOP 03 - Registre des expériences et univers des règles candidates.md`
- `Protocole/SOP 07 - Detrending benchmark et zero-centering.md`
- `Protocole/SOP 09A - Données point-in-time et contrôles anti-leakage.md`
- `Protocole/SOP 09B - Modèle d’exécution frictions capacité et sizing.md`
- `Protocole/SOP 12 - Reproductibilité et paquet de validation EBTA.md`
- `Notes/121-La Validation Hors-Échantillon L'Épreuve de Réalité Statistique.md`
- `Notes/122-Dynamique et Robustesse du Walk-Forward Testing.md`
- `Notes/123-L'Éphémère Rigueur Limites des Tests Hors-Échantillon.md`
- `Notes/166-Adaptation et Sélection Dynamique en Processus Walk-Forward.md`
- `Notes/168-GESTION RIGOUREUSE DE L’ÉCHEC EN VALIDATION OUT-OF-SAMPLE (OOS).md`
- `Notes/169-Optimisation de la Complexité et Détection du Surapprentissage en Walk-Forward.md`

---

## 27. Décision méthodologique synthétique

> **Le protocole EBTA utilise un Walk-Forward rolling à trois fonctions distinctes dans chaque fold : Train pour la calibration, Test pour la sélection et l’inférence multiple, OOS pour l’estimation passive. Les segments OOS sont successifs, non chevauchants et concaténés chronologiquement pour former l’unique objet OOS global. Les longueurs, frontières, purges, embargos, politiques d’absence de modèle et critères de décision sont préenregistrés. Aucun résultat OOS ne peut influencer un fold ultérieur. Toute modification imprévue crée une nouvelle version de processus. Le verdict final repose sur la série quotidienne OOS globale, son incertitude et son hurdle économique, et non sur une moyenne de ratios ou un pourcentage de folds gagnants.**
