# SOP 01 — Estimation et intervalle de confiance OOS
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 01 |
| Rôle dans le paquet EBTA | Estimation OOS, intervalle de confiance, puissance et verdict statistique global. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## 1. Statut du document

- **Type :** Standard Operating Procedure méthodologique.
- **Statut :** spécification normative de l’estimation et du verdict OOS.
- **Périmètre :** Estimation de la performance du processus Walk-Forward gelé sur la série chronologique concaténée de ses folds OOS non chevauchants.
- **Architecture retenue :** aucun holdout final supplémentaire n’est réservé. Chaque fold du Walk-Forward possède son propre segment OOS. Le verdict global repose sur l’ensemble concaténé de ces segments, sous réserve qu’aucun résultat OOS intermédiaire n’ait influencé les folds suivants.
- **Hors périmètre :**
  - sélection de la règle gagnante ;
  - correction du data-mining bias ;
  - White’s Reality Check, SPA, Romano–Wolf et MCP ;
  - choix de la métrique primaire en amont ;
  - tests de robustesse postérieurs ;
  - règles complètes de Walk-Forward ;
  - sizing et allocation de capital.

Cette SOP complète le fichier `Protocole/PROTOCOLE EBTA.md`. En cas de contradiction sur la construction de l’intervalle de confiance OOS, la présente SOP constitue la spécification méthodologique proposée.

---

## 2. Objectif

L’objectif est de produire, sur l’OOS :

1. une **estimation ponctuelle** de la performance future attendue de la règle gelée ;
2. un **intervalle de confiance** quantifiant l’erreur d’échantillonnage entourant cette estimation ;
3. un verdict statistique reproductible :
   - `PASS` ;
   - `NOT_VALIDATED` ;
   - `FAIL` ;
   - `INCONCLUSIVE`.

Cette estimation doit être calculée sans :

- réutiliser l’OOS pour sélectionner une règle ;
- utiliser le résultat de `OOS_k` pour modifier le processus appliqué aux folds suivants ;
- modifier la règle après observation de l’OOS ;
- réutiliser la distribution du maximum WRC calculée sur le Test ;
- choisir après coup la méthode d’intervalle donnant le résultat le plus favorable.

---

## 3. Fondement statistique

### 3.1 Test de sélection et estimation OOS

Le protocole distingue deux objets :

- **Test corrigé du data mining sur le Test :** déterminer si la meilleure règle issue de la recherche possède une performance difficilement explicable par le hasard, compte tenu de l’univers complet des règles candidates.
- **Estimation sur l’OOS :** mesurer la performance et l’incertitude du processus Walk-Forward gelé, chaque règle produite dans un fold étant figée avant l’ouverture de son segment `OOS_k`.

Le White’s Reality Check porte sur le maximum d’un univers de règles. Son bootstrap produit une distribution adaptée au test global de sélection.

L’intervalle OOS porte sur la moyenne de la série globale produite par un seul processus Walk-Forward gelé. Sa distribution d’échantillonnage doit être construite à partir de la série OOS concaténée correspondante.

Ces deux distributions ne décrivent pas le même estimateur.

### 3.2 Règle impérative

> **La distribution bootstrap utilisée pour l’intervalle de confiance OOS doit être générée à partir des observations OOS concaténées du processus Walk-Forward gelé. La distribution du maximum WRC calculée sur le Test ne doit pas être recentrée ni réutilisée pour produire cet intervalle.**

### 3.3 Interprétation fréquentiste

Un intervalle de confiance à 90 % ne signifie pas qu’il existe, après calcul, une probabilité de 90 % que le paramètre fixe se trouve dans cet intervalle.

Il signifie que si la même procédure d’échantillonnage et de construction était répétée un grand nombre de fois, environ 90 % des intervalles obtenus couvriraient le paramètre réel, sous les hypothèses de validité de la méthode.

---

## 4. Objet estimé

### 4.1 Paramètre primaire

Le paramètre primaire est l’espérance de la série quotidienne des log-rendements nets detrendés du portefeuille selon la méthode d’Aronson :

$$
\mu = E[d_t]
$$

où :

- $d_t$ est le log-rendement quotidien net detrendé utilisé pour mesurer l’alpha de sélection de la règle ;
- les frais, le slippage et les autres frictions préenregistrées sont déduits ;
- le rendement attribuable au drift moyen du marché est ajusté par l’exposition nette quotidienne de la stratégie, comprise entre $-1$ et $+1$ ;
- le drift est estimé une seule fois sur la série OOS chronologique concaténée ;
- les jours sans exposition sont conservés dans la série.

La formule exacte de detrending et d’ajustement du benchmark doit être figée conformément à `SOP 07 - Detrending benchmark et zero-centering.md` avant l’exécution du premier fold OOS.

Le detrending est une transformation d’évaluation ex post : le drift estimé sur l’OOS concaténé ne peut jamais intervenir dans les signaux, les positions, le sizing ou l’exécution simulée.

### 4.1.1 Formule normative de detrending

Pour un actif unique, l’estimand statistique quotidien est :

$$
d_t=r^{strat,net}_t-r^{cash}_t-e_t\left(\bar r^{market}-\bar r^{cash}\right)
$$

où :

- $r^{strat,net}_t$ est le log-rendement quotidien net de la stratégie ;
- $r^{cash}_t$ est le log-rendement quotidien du cash réellement disponible ;
- $e_t$ est l’exposition nette quotidienne, comprise entre $-1$ et $+1$ ;
- $\bar r^{market}$ est le drift moyen quotidien du marché ;
- $\bar r^{cash}$ est le rendement quotidien moyen du cash sur la même période.

Cette écriture applique le detrending Aronson tout en neutralisant le rendement du cash dans le gate statistique. Elle évite de soustraire deux fois le taux sans risque : le drift retiré est le drift excédentaire du marché, pondéré par l’exposition.

Le rendement du cash reste publié et pris en compte dans le gate économique.

Le rendement du cash correspond au taux monétaire réellement accessible dans la devise concernée, net des coûts, frais, spreads et éventuelles contraintes opérationnelles. Un taux sans risque théorique ne peut le remplacer que si cette convention est explicitement préenregistrée comme approximation conservatrice.

### 4.1.2 Portefeuille multi-actifs

Le drift est estimé séparément pour chaque actif sur ses log-rendements de marché correspondant exactement aux périodes de P&L. Les contributions detrendées sont ensuite agrégées selon les expositions effectives du portefeuille :

$$
d_t=r^{strat,net}_t-r^{cash}_t-
\sum_{i=1}^{M}e_{i,t}\left(\bar r_i^{market}-\bar r^{cash}\right)
$$

Il est interdit de remplacer ces drifts propres aux actifs par la moyenne non pondérée des drifts ou par un benchmark global choisi après observation.

### 4.1.3 Portefeuille multidevise

Pour un portefeuille multidevise :

- les soldes cash, P&L, coûts et expositions sont convertis quotidiennement dans la devise de base du portefeuille ;
- les conversions utilisent les taux FX point-in-time réellement disponibles à l’instant de valorisation ;
- les coûts de conversion et de financement sont inclus ;
- la convention de fixing, la source FX et l’heure de valorisation sont préenregistrées ;
- aucune conversion au taux final de la période n’est autorisée rétroactivement.

### 4.2 Sortie économique secondaire

Le rapport doit également présenter la performance nette non detrendée de la stratégie, afin de mesurer son comportement économique réellement simulé :

- rendement moyen net ;
- rendement annualisé selon la convention préenregistrée ;
- volatilité ;
- drawdown ;
- nombre de périodes actives ;
- nombre de trades ;
- exposition moyenne.

Ces métriques secondaires ne peuvent pas remplacer après coup la métrique primaire utilisée par le gate OOS.

### 4.3 Estimation ponctuelle

L’estimation ponctuelle primaire est la moyenne arithmétique :

$$
\hat{\mu}_{OOS} = \frac{1}{N}\sum_{t=1}^{N}d_t
$$

La moyenne est calculée sur la série OOS complète après frais, slippage et autres frictions figées.

---

## 5. Unité d’observation

### 5.1 Unité primaire

L’unité d’observation primaire est le **rendement quotidien du portefeuille**, y compris pour une stratégie intraday.

La mesure primaire est le **log-rendement quotidien**, calculé à partir de l’equity nette :

$$
r_t=\ln\left(\frac{V_t}{V_{t-1}}\right)
$$

où $V_t$ désigne l’equity nette marquée au marché à la clôture de la session de référence.

La journée est définie par la session et le fuseau horaire propres au marché négocié. Pour un portefeuille multi-marchés, la convention d’agrégation des sessions doit être préenregistrée.

Les positions conservées pendant la nuit sont valorisées quotidiennement en mark-to-market. Leur résultat n’est pas reporté intégralement au jour de clôture du trade.

Un jour sans exposition reste présent dans la série. Son rendement économique correspond à celui du cash réellement simulé, après les coûts éventuels. Dans l’estimand statistique, le rendement du cash est neutralisé ; en l’absence de coûts ou d’autres P&L, la contribution detrendée du jour est donc nulle.

Le rendement quotidien de portefeuille est préféré au rendement par trade, car il :

- conserve les périodes sans position ;
- intègre les positions simultanées ;
- respecte l’exposition réelle du capital ;
- évite de considérer comme indépendants des trades qui se chevauchent ;
- permet une comparaison cohérente au benchmark.

### 5.2 Analyse par trade

Une analyse par trade peut être fournie comme diagnostic secondaire.

Elle ne peut être utilisée comme base primaire de l’IC que si le protocole démontre que :

- les trades ne se chevauchent pas ;
- les résultats ne sont pas regroupés par événement commun ;
- aucune position simultanée ne partage le même risque de marché ;
- l’indépendance de l’unité « trade » est méthodologiquement défendable ;
- ce choix a été préenregistré.

---

## 6. Prérequis avant ouverture de l’OOS

L’OOS ne peut être ouvert que si tous les éléments suivants sont figés et archivés.

### 6.1 Modèle

- code source de la règle ;
- paramètres ;
- univers d’actifs ;
- règles d’entrée et de sortie ;
- sizing ;
- gestion du risque ;
- fréquence ;
- modèle de coûts ;
- modèle de slippage ;
- benchmark ;
- méthode de detrending éventuelle.

### 6.2 Protocole statistique OOS

- métrique primaire ;
- série de rendement de référence ;
- unité d’observation ;
- seuil statistique $h_s=0$ ;
- critères du gate économique séparé ;
- niveau de confiance ;
- méthode bootstrap ;
- méthode de sélection de la longueur des blocs ;
- nombre de réplications ;
- seed ;
- critères `PASS`, `NOT_VALIDATED`, `FAIL` et `INCONCLUSIVE` ;
- traitement des données manquantes ;
- règle d’annualisation ;
- diagnostics obligatoires ;
- conditions autorisant une réexécution purement technique.

### 6.3 Preuves de gel

- hash du code ;
- hash de la configuration ;
- hash ou identifiant du snapshot de données ;
- identifiant du run ;
- date et heure d’ouverture de l’OOS ;
- validation du passage du gate statistique sur le Test ;
- confirmation que chaque fold OOS n’a pas été consulté avant le gel de la procédure qui lui est appliquée ;
- preuve que les résultats des folds OOS antérieurs n’ont pas influencé les folds ultérieurs.

Si un de ces éléments manque, le calcul OOS ne doit pas commencer.

---

## 7. Choix de la méthode d’intervalle

### 7.1 Principe général

La méthode doit reproduire aussi fidèlement que possible la structure d’échantillonnage de la série $d_t$.

Un bootstrap IID tirant chaque période indépendamment avec remise détruit l’autocorrélation, les clusters de volatilité et les dépendances produites par des positions qui se chevauchent.

### 7.2 Méthode par défaut

La méthode primaire par défaut est :

> **Bootstrap stationnaire par blocs appliqué à la série chronologique OOS des rendements différentiels nets.**

Ce choix est conservateur pour des séries financières potentiellement dépendantes et permet de préserver localement la structure temporelle.

### 7.3 Bootstrap IID

Le bootstrap IID par tirage individuel avec remise n’est autorisé que si :

- la stratégie ne crée pas mécaniquement de rendements qui se chevauchent ;
- l’horizon de détention ne crée pas de dépendance sérielle structurelle ;
- le protocole IID du projet conclut que l’hypothèse est acceptable ;
- cette méthode a été choisie avant l’ouverture de l’OOS.

L’absence de significativité d’un seul test d’autocorrélation ne suffit pas, à elle seule, à prouver l’indépendance.

### 7.4 Rendements qui se chevauchent

Si une décision à $t$ produit un rendement mesuré sur plusieurs périodes futures, les observations adjacentes se chevauchent et ne sont pas IID.

Dans ce cas :

- le bootstrap IID est interdit ;
- le bootstrap par blocs est obligatoire ;
- la longueur minimale des blocs doit être compatible avec l’horizon maximal de chevauchement.

### 7.5 Sélection de la longueur des blocs

La méthode de sélection doit être automatique ou fixée avant l’OOS.

La longueur des blocs est déterminée par l’algorithme automatique de **Politis–White avec la correction de Patton–Politis–White**, appliqué mécaniquement sans intervention discrétionnaire.

La longueur retenue ne peut toutefois pas être inférieure au minimum structurel imposé par la dépendance mécanique de la stratégie, notamment le chevauchement des positions et l’horizon maximal de détention. Si l’estimateur automatique produit une valeur inférieure, le minimum structurel prévaut.

Il est interdit d’essayer plusieurs longueurs de blocs et de conserver celle qui produit la borne basse la plus favorable.

La valeur retenue et sa justification doivent apparaître dans le rapport.

---

## 8. Construction de l’intervalle de confiance

### 8.1 Méthode primaire

La méthode primaire est l’**intervalle bootstrap par centiles**, conforme à la procédure décrite par Aronson pour l’estimation d’une règle fixe.

Contrairement au bootstrap destiné à construire une distribution sous $H_0$, les rendements OOS ne sont pas zero-centered pour construire l’IC.

### 8.2 Borne confirmatoire

Le gate statistique utilise une **borne inférieure unilatérale à 95 %** :

$$
L_{95}=Q_{0.05}(\hat{\mu}^*)
$$

Pour la présentation de l’incertitude, le rapport publie également l’intervalle bilatéral à 90 % :

$$
IC_{90\%}=[Q_{0.05}(\hat{\mu}^*);Q_{0.95}(\hat{\mu}^*)]
$$

La borne basse est identique dans les deux représentations. Le niveau ne peut pas être changé après observation des résultats OOS.

### 8.3 Nombre de réplications

- **Valeur normative :** 5 000 réplications bootstrap.

Une augmentation du nombre de réplications améliore la précision numérique du bootstrap, mais ne compense pas un échantillon OOS trop petit ou non représentatif.

Aucun contrôle supplémentaire fondé sur plusieurs seeds ou plusieurs sous-échantillons de réplications n’est exigé. Le verdict repose sur les 5 000 réplications générées avec la seed déterministe préenregistrée.

### 8.4 Seed

La seed est déterministe et dérivée du hash immuable des entrées du run avant OOS, selon une transformation préenregistrée. Elle doit être enregistrée et identique lors de toute reproduction du même run.

Un résultat ne peut pas être déclaré `PASS` seulement pour certaines seeds.

### 8.5 Algorithme

Pour $b = 1,\dots,B$ :

1. Générer un échantillon bootstrap $d^{*(b)}$ de taille $N$ :
   - par tirage individuel avec remise si le mode IID est autorisé ;
   - par bootstrap stationnaire par blocs dans le cas général.
2. Calculer :

$$
\hat{\mu}^{*(b)} = \frac{1}{N}\sum_{t=1}^{N}d_t^{*(b)}
$$

3. Conserver les $B$ moyennes bootstrap.
4. Trier les valeurs $\hat{\mu}^{*(b)}$.
5. Calculer la borne inférieure unilatérale à 95 % :

$$
L_{95}=Q_{0.05}(\hat{\mu}^*)
$$

6. Pour l’IC bilatéral descriptif à 90 %, calculer :

$$
U_{90}=Q_{0.95}(\hat{\mu}^*)
$$

7. Produire :

$$
IC_{90\%}=[L_{95};U_{90}]
$$

### 8.6 Annualisation

L’IC doit d’abord être calculé dans l’unité native de la série.

Comme la métrique primaire est une moyenne de log-rendements quotidiens et si $A$ est le nombre de sessions annuelles préenregistré :

$$
\hat{\mu}_{annuelle} = A\hat{\mu}_{périodique}
$$

$$
IC_{annuel} = [A L;A U]
$$

Ces valeurs sont exprimées en log-rendement annuel. Leur présentation en rendement simple composé utilise :

$$
R_{annuel}=\exp(\mu_{annuelle})-1
$$

Cette transformation monotone peut être appliquée aux bornes après leur calcul. Toute autre transformation non linéaire doit être appliquée à chaque réplication bootstrap avant de calculer les quantiles.

---

## 9. Diagnostics obligatoires

Le rapport doit contenir au minimum :

- taille brute $N$ ;
- nombre et proportion de journées invalides ;
- nombre de périodes avec exposition ;
- nombre de trades ;
- horizon de détention médian et maximal ;
- présence de positions ou rendements qui se chevauchent ;
- taux de données manquantes ;
- moyenne ;
- médiane ;
- écart-type ;
- asymétrie ;
- concentration de la performance dans les meilleures observations ;
- autocorrélations pertinentes ;
- méthode bootstrap ;
- longueur moyenne ou fixe des blocs ;
- nombre de réplications ;
- seed ;
- distribution des moyennes bootstrap.

### 9.1 Données quotidiennes invalides

Aucune imputation de rendement n’est autorisée lorsque l’equity, le prix nécessaire au mark-to-market ou le benchmark requis est manquant.

Le seuil de tolérance est fixé à **0 % de journées invalides**. Toute journée invalide rend le run `INCONCLUSIVE` jusqu’à correction technique documentée selon la gouvernance OOS.

Sont notamment interdites :

- l’imputation d’un rendement nul ;
- l’utilisation discrétionnaire du dernier prix connu ;
- la suppression silencieuse de la journée ;
- la reconstruction après observation de l’effet sur le verdict.

Ces diagnostics ne donnent pas le droit de changer de méthode après observation de l’OOS.

Une méthode de repli ne peut être utilisée que si elle a été préenregistrée avec sa condition de déclenchement objective.

---

## 10. Règles de décision

### 10.1 Séparation des deux gates

Deux décisions distinctes sont produites :

1. **Gate statistique :** vérifier que l’espérance detrendée est strictement positive, avec un seuil $h_s=0$.
2. **Gate économique :** vérifier séparément que la stratégie satisfait les critères préenregistrés de rentabilité, de risque, de capacité et d’exécutabilité.

Une stratégie ne peut être admise au déploiement que si les deux gates sont `PASS`. Un succès statistique ne compense pas un échec économique, et inversement.

### 10.2 Gate statistique : `PASS`

Le gate statistique est `PASS` si toutes les conditions suivantes sont satisfaites :

1. tous les prérequis de gel sont valides ;
2. le run OOS est techniquement valide ;
3. la méthode statistique préenregistrée a été appliquée sans modification ;
4. la puissance préenregistrée est d’au moins 80 % ;
5. l’estimation ponctuelle satisfait :

$$
\hat{\mu}_{OOS}>0
$$

6. la borne inférieure unilatérale à 95 % satisfait :

$$
L_{95}>0
$$

### 10.3 Gate statistique : `NOT_VALIDATED`

Le gate statistique est `NOT_VALIDATED` si le run est valide et suffisamment informatif, que l’estimation ponctuelle est positive, mais que l’incertitude ne permet pas de conclure :

$$
\hat{\mu}_{OOS}>0
$$

$$
L_{95}\leq0
$$

`NOT_VALIDATED` n’est ni un `PASS`, ni une autorisation de modifier la règle ou de réutiliser les mêmes observations OOS.

### 10.4 Gate statistique : `FAIL`

Le gate statistique est `FAIL` si le run est valide et suffisamment informatif, mais que :

$$
\hat{\mu}_{OOS}\leq0
$$

Le modèle est rejeté pour ce cycle de recherche. Aucun paramètre ne peut être retouché à partir du détail des résultats OOS.

### 10.5 Verdict `INCONCLUSIVE`

Le verdict est `INCONCLUSIVE` si une estimation défendable ne peut pas être produite, notamment lorsque :

- la puissance préenregistrée est inférieure à 80 % pour l’effet minimal économiquement détectable ;
- le nombre de trades est inférieur au minimum préenregistré ;
- le nombre de blocs effectivement distincts est inférieur à 30 ;
- une seule journée de l’OOS global est invalide ;
- une anomalie technique empêche de déterminer la performance correcte ;
- la série OOS ne couvre pas les conditions minimales prévues par le protocole.

`INCONCLUSIVE` n’est pas un `PASS`.

Après ouverture de l’OOS, ce statut ne donne pas le droit :

- d’optimiser la règle ;
- de modifier la métrique ;
- de changer discrétionnairement le niveau de confiance ;
- de choisir une autre méthode bootstrap plus favorable ;
- de recommencer sur la même période.

Si la quantité d’information est insuffisante, de nouveaux folds strictement futurs peuvent être ajoutés sans modifier le processus, jusqu’à l’atteinte du volume d’information préenregistré correspondant à une puissance d’au moins 80 %. Les observations déjà ouvertes restent consommées et archivées.

Cette prolongation ne peut pas dépendre du signe, du niveau ou de la significativité de la performance observée. Le calendrier, la taille des folds et la règle d’arrêt informationnelle doivent être fixés avant la première consultation OOS. Le verdict n’est calculé qu’au point d’arrêt prévu, sauf procédure séquentielle distincte préenregistrée.

### 10.6 Gate économique séparé

Le gate économique est défini dans la SOP de mesure de performance et la SOP d’exécution. Il peut notamment inclure un rendement net minimal, un drawdown maximal, une capacité minimale et des contraintes de coûts ou de liquidité.

Ses seuils doivent être préenregistrés. Les métriques économiques ne peuvent pas remplacer après coup l’estimand detrendé du gate statistique.

L’effet minimal économiquement détectable utilisé dans l’analyse de puissance est dérivé du rendement annuel minimal exigé par ce gate économique. Comme la mesure primaire est un log-rendement, sa conversion quotidienne utilise la convention annuelle préenregistrée :

$$
\delta_{jour}=\frac{\ln(1+R_{annuel,min})}{A}
$$

où $A$ est le nombre préenregistré de sessions annuelles.

L’analyse de puissance utilise une estimation prudente de la **variance long terme**, tenant compte de l’autocorrélation, calculée exclusivement sur les données de développement disponibles avant l’OOS.

Il n’existe pas de minimum universel fixe de trades. Le minimum requis est dérivé de l’analyse de puissance, du nombre effectif d’observations et de la structure de dépendance. Il s’applique à la série OOS globale concaténée, et non séparément à chaque fold.

Indépendamment du nombre de trades, l’estimation exige au moins **30 blocs effectivement distincts** selon la longueur de bloc retenue. En dessous de ce seuil, le résultat est `INCONCLUSIVE`.

### 10.7 Décision globale

La décision globale combine les gates sans les fusionner :

| Gate statistique | Gate économique | Décision globale |
|---|---|---|
| `PASS` | `PASS` | `PASS` |
| `PASS` | `FAIL` | `REJECTED_ECONOMIC` |
| `NOT_VALIDATED` | `PASS` ou `FAIL` | `NOT_VALIDATED` |
| `FAIL` | toute valeur | `FAIL` |
| `INCONCLUSIVE` | toute valeur | `INCONCLUSIVE` |

Lorsque le gate statistique est `NOT_VALIDATED`, l’attente de folds futurs n’est autorisée que si elle respecte le calendrier et le point d’arrêt informationnel préenregistrés. Le succès du gate économique ne permet ni une incubation confirmatoire, ni un passage live anticipé.

---

## 11. Relation entre intervalle de confiance et test confirmatoire

Exiger que la borne inférieure unilatérale à 95 % soit supérieure à zéro est mathématiquement lié à un test unilatéral au niveau de 5 %, sous la procédure d’inversion correspondante. Cette borne est identique à la borne basse de l’IC bilatéral descriptif à 90 %.

Par conséquent, la formulation correcte est :

> L’OOS n’est pas utilisé pour conduire une nouvelle sélection multiple ni pour recalibrer rétroactivement le processus. Il applique au processus Walk-Forward gelé un gate confirmatoire préenregistré fondé sur son estimation et son incertitude.

La formulation suivante doit être évitée :

> Tout test d’hypothèse sur l’OOS est mathématiquement invalide.

Ce qui est invalide ou contaminant est :

- de comparer plusieurs règles sur l’OOS ;
- de tester plusieurs métriques et de choisir la meilleure ;
- de modifier le seuil après observation ;
- de retoucher le modèle ;
- d’accumuler des consultations OOS non comptabilisées.

---

## 12. Procédure opérationnelle complète

### Phase A — Avant ouverture

- [ ] Vérifier que le gate Test corrigé du data mining est `PASS`.
- [ ] Vérifier que le processus Walk-Forward est gelé et que la règle de chaque fold sera figée avant son `OOS_k`.
- [ ] Vérifier les hashes du code, de la configuration et des données.
- [ ] Vérifier que l’estimand detrendé et le seuil statistique $h_s=0$ sont figés.
- [ ] Vérifier que le gate économique séparé et ses seuils sont figés.
- [ ] Vérifier que l’unité d’observation est figée.
- [ ] Vérifier la session, le fuseau horaire et la convention multi-marchés.
- [ ] Vérifier que l’effet minimal détectable et la puissance cible de 80 % sont figés.
- [ ] Vérifier que la règle d’ajout de folds futurs et son point d’arrêt sont figés.
- [ ] Vérifier que la méthode bootstrap est figée.
- [ ] Vérifier que le niveau de confiance est figé.
- [ ] Vérifier que la longueur de bloc ou son algorithme est figé.
- [ ] Vérifier que $B$ et la seed sont figés.
- [ ] Vérifier que les critères `PASS`, `NOT_VALIDATED`, `FAIL` et `INCONCLUSIVE` sont figés.
- [ ] Confirmer par écrit que chaque OOS n’a pas été consulté avant le gel de son exécution.
- [ ] Confirmer que les résultats OOS antérieurs n’ont pas influencé les folds suivants.

### Phase B — Exécution OOS

- [ ] Déverrouiller chaque segment `OOS_k` une seule fois, à l’étape prévue du Walk-Forward.
- [ ] Exécuter le code gelé sans modification.
- [ ] Exporter la série chronologique complète des rendements OOS.
- [ ] Exporter les positions, expositions, trades, coûts et benchmarks.
- [ ] Sceller les sorties brutes avant calcul statistique.
- [ ] Vérifier uniquement la validité technique du run.

### Phase C — Estimation

- [ ] Construire la série différentielle nette $d_t$.
- [ ] Calculer $\hat{\mu}_{OOS}$.
- [ ] Générer les réplications bootstrap selon la méthode figée.
- [ ] Calculer les quantiles de l’IC.
- [ ] Produire les diagnostics obligatoires.
- [ ] Appliquer mécaniquement la règle de décision.

### Phase D — Archivage

- [ ] Enregistrer le verdict.
- [ ] Enregistrer la série OOS et les réplications ou leur preuve reproductible.
- [ ] Enregistrer la seed et tous les paramètres.
- [ ] Enregistrer les graphiques et diagnostics.
- [ ] Interdire toute modification rétroactive du modèle.
- [ ] Transmettre le résultat à la gouvernance OOS.

---

## 13. Walk-Forward

Cette section fixe uniquement la règle d’estimation ; l’architecture complète relève de la SOP Walk-Forward.

### 13.1 Réutilisation chronologique des données

Les observations d’un ancien segment `OOS_k` peuvent intégrer mécaniquement la fenêtre Train d’un fold ultérieur lorsque l’architecture rolling ou expanding préenregistrée le prévoit.

Cette réutilisation ne remet pas en cause leur caractère OOS au moment où elles ont été produites, à condition que :

- le calendrier et la règle de déplacement des fenêtres aient été gelés avant le premier fold ;
- aucune inspection humaine de `OOS_k` ne modifie les features, paramètres, hyperparamètres, critères de sélection ou règles d’arrêt ;
- l’intégration dans le Train ultérieur soit automatique et identique quel que soit le résultat observé.

### 13.2 Série OOS globale

Lorsque plusieurs segments OOS non chevauchants sont produits par un processus Walk-Forward, l’estimation globale doit être calculée sur la série chronologique concaténée des rendements OOS :

$$
D_{OOS} =
\left[
d^{OOS_1},
d^{OOS_2},
\dots,
d^{OOS_K}
\right]
$$

La moyenne, la borne inférieure unilatérale à 95 % et l’IC descriptif bilatéral à 90 % sont calculés sur cette série concaténée en respectant son ordre temporel.

Cette série constitue l’unique OOS global du protocole. Aucun holdout final supplémentaire n’est prévu.

L’agrégation n’est valide que si la procédure complète du Walk-Forward a été gelée avant l’exécution des folds et si `OOS_k` n’a jamais servi à modifier le traitement des folds ultérieurs. Dans le cas contraire, les segments concernés ne peuvent pas être présentés comme l’exécution d’un même protocole confirmatoire.

### 13.3 Intervalles par fold

Les estimations par fold sont des diagnostics de stabilité temporelle.

Un fold ne comportant aucun trade est conservé intégralement dans la série globale avec tous ses jours et le rendement du cash réellement simulé. Il n’est ni supprimé, ni déclaré automatiquement en échec.

Les résultats par fold ne constituent aucun gate de stabilité. Aucun nombre minimal de folds positifs, vote majoritaire ou critère d’hétérogénéité ne peut remplacer ou compléter le verdict statistique global dans cette SOP.

Elles ne doivent pas être transformées automatiquement en votes indépendants, car :

- les fenêtres Train peuvent se chevaucher ;
- le processus de sélection est commun ;
- les régimes de marché peuvent être dépendants ;
- les estimations par fold peuvent avoir des précisions différentes.

### 13.4 Bootstrap global

Le bootstrap global doit :

- respecter les frontières et la chronologie des segments ;
- interdire à un bloc de traverser la frontière entre deux folds, même lorsque leurs dates sont contiguës ;
- ne jamais créer artificiellement de rendement sur une période absente ;
- préserver la dépendance temporelle pertinente ;
- suivre une convention préenregistrée concernant les frontières entre folds.

Le verdict final repose prioritairement sur l’IC de la série OOS agrégée, sauf règle différente justifiée dans la SOP Walk-Forward.

Chaque journée valide possède le même poids dans l’estimation globale. Aucun poids égal par fold, ajustement inverse à la variance ou surpondération des observations récentes n’est autorisé.

---

## 14. Réexécution technique

Une réexécution sur le même OOS n’est autorisée que si :

- une anomalie technique objective est démontrée ;
- l’anomalie ne dépend pas du niveau ou du signe de la performance observée ;
- le correctif ne modifie pas la logique économique, les paramètres ou le modèle de risque ;
- l’erreur et le correctif sont documentés ;
- l’autorisation est accordée par une revue indépendante ;
- les deux résultats, erroné et corrigé, restent archivés.

Une mauvaise performance n’est jamais une anomalie technique.

Une donnée invalide peut être corrigée depuis une source officielle si la correction est purement technique, documentée et indépendante du résultat observé. Le snapshot initial, la preuve de l’erreur, la source corrective, le run invalide et le run corrigé doivent tous être conservés.

Les cas détaillés doivent être définis dans `SOP 10 - Gouvernance OOS et gestion des échecs.md`.

---

## 15. Livrable obligatoire

Le rapport OOS doit contenir :

```text
[IDENTIFICATION]
Projet :
Règle :
Version du code :
Hash du code :
Hash de la configuration :
Snapshot des données :
Date d’ouverture OOS :

[ESTIMAND]
Série primaire :
Benchmark / référence :
Référence cash :
Devise de base :
Source et fixing FX :
Seuil statistique hs : 0
Gate économique :
Fréquence :
Unité d’observation :
Convention de rendement : log-rendement quotidien
Session et fuseau horaire :
Convention multi-marchés :
Méthode de detrending :
Drift estimé sur :
Exposition utilisée : exposition nette [-1 ; +1]
Traitement du cash dans le gate statistique : neutralisé
Traitement du cash dans le gate économique : inclus
Frais et slippage :

[ÉCHANTILLON]
N brut :
N effectif estimé :
Nombre de trades :
Minimum de trades dérivé de la puissance :
Nombre de blocs effectivement distincts :
Nombre de périodes exposées :
Chevauchement :
Données manquantes :
Journées invalides : 0

[BOOTSTRAP]
Méthode :
Justification :
Longueur de bloc :
Méthode de sélection du bloc :
Réplications B :
Seed :
Niveau de la borne unilatérale : 95 %
Niveau de l’IC bilatéral descriptif : 90 %
Méthode d’intervalle :

[RÉSULTATS PRIMAIRES]
Estimation ponctuelle :
Borne inférieure unilatérale L95 :
Borne supérieure descriptive U90 :
Résultat annualisé :
Puissance préenregistrée :
Effet minimal détectable :
Variance long terme pré-OOS :
Point d’arrêt informationnel :

[VERDICT]
Gate statistique — PASS / NOT_VALIDATED / FAIL / INCONCLUSIVE :
Gate économique — PASS / FAIL / INCONCLUSIVE :
Décision globale — PASS / REJECTED_ECONOMIC / NOT_VALIDATED / FAIL / INCONCLUSIVE :
Justification mécanique :

[GOUVERNANCE]
Modification post-OOS autorisée : NON
Étape suivante :
```

---

## 16. Erreurs interdites

- Réutiliser la distribution du maximum WRC du Test pour l’IC OOS.
- Zero-center les rendements lors de la construction de l’IC d’estimation.
- Utiliser une permutation MCP comme méthode d’IC de l’espérance.
- Mélanger rendements bruts, detrendés et benchmark-relative dans le même estimand.
- Bootstrapper des trades supposés indépendants alors qu’ils se chevauchent.
- Utiliser un bootstrap IID sur une série structurellement dépendante.
- Choisir la longueur des blocs en fonction du verdict obtenu.
- Essayer plusieurs seeds et retenir la plus favorable.
- Changer le niveau de confiance après observation.
- Remplacer la métrique primaire par une métrique secondaire favorable.
- Confondre précision numérique du bootstrap et puissance informationnelle de l’OOS.
- Interpréter un IC à 90 % comme une probabilité postérieure de 90 %.
- Déclarer `PASS` lorsque le résultat est `INCONCLUSIVE`.
- Assimiler `NOT_VALIDATED` à un `PASS`.
- Utiliser un fold OOS pour modifier un fold ultérieur puis concaténer les deux comme une validation homogène.
- Modifier la règle après un `FAIL`.

---

## 17. Modifications requises dans le protocole principal

Après validation de cette SOP, les formulations suivantes du protocole principal devront être corrigées :

1. Supprimer l’instruction demandant de conserver la distribution WRC du Test pour la recentrer sur la moyenne OOS.
2. Remplacer cette instruction par la génération d’une distribution bootstrap propre au processus Walk-Forward gelé sur sa série OOS concaténée.
3. Remplacer « aucun test d’hypothèse sur l’OOS n’est valide » par l’interdiction précise de toute nouvelle sélection ou modification fondée sur l’OOS.
4. Présenter la borne inférieure unilatérale à 95 % comme un gate confirmatoire préenregistré sur le processus Walk-Forward gelé.
5. Ajouter les verdicts `NOT_VALIDATED` et `INCONCLUSIVE`.
6. Remplacer la simple mention « moyenne OOS » par la définition complète de l’estimand et de l’unité d’observation.
7. Ajouter la gestion de la dépendance temporelle et des rendements qui se chevauchent.
8. En Walk-Forward, privilégier l’IC de la série OOS chronologique agrégée plutôt qu’un vote supposant l’indépendance des folds.

---

## 18. Sources internes utilisées

- `Notes/76-L'Estimation Statistique de la Performance en Trading.md`
- `Notes/77-L'Art de l'Estimation Ponctuelle en Trading Objectif.md`
- `Notes/78-Intervalles de Confiance Mesurer l'Incertitude du Backtesting.md`
- `Notes/79-L'Architecture Statistique de l'Incertitude De la Distribution à l'Intervalle.md`
- `Notes/80-Le Bootstrap et l'Incertitude Statistique en Trading.md`
- `Protocole/Archives/AUDIT METHODOLOGIQUE PROTOCOLE EBTA.md`
- `Protocole/PROTOCOLE EBTA.md`

---

## 19. Références méthodologiques complémentaires

- Aronson, D. — *Evidence-Based Technical Analysis*, chapitre 5, sections consacrées à l’estimation et aux intervalles de confiance.
- Efron, B. et Tibshirani, R. J. — *An Introduction to the Bootstrap*.
- Politis, D. N. et Romano, J. P. — *The Stationary Bootstrap*.
- Künsch, H. R. — travaux fondateurs sur le bootstrap par blocs pour séries dépendantes.

---

## 20. Décision méthodologique synthétique

> **Le Test démontre, avec correction de la recherche multiple, que le processus mérite d’être évalué. Aucun holdout final supplémentaire n’est réservé : l’OOS global est la série quotidienne concaténée des folds OOS non chevauchants du Walk-Forward gelé. Le gate statistique porte sur l’espérance nette detrendée, utilise une borne inférieure unilatérale à 95 % obtenue par 5 000 réplications d’un bootstrap stationnaire par blocs et exige une puissance préenregistrée d’au moins 80 %. Un gate économique distinct reste obligatoire. Aucun résultat OOS ne donne le droit de modifier rétroactivement le processus.**
