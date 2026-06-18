# Le moment du test d'hypothèse dans le processus EBTA

## Référence

- **Titre :** Méthodologie et processus de recherche — synthèse basée sur l'ensemble de l'ouvrage *Evidence-Based Technical Analysis* de David Aronson, notamment les chapitres 3, 4 et 6.
- **Thème principal :** Le rôle de l'inférence statistique et le moment opportun pour réaliser les tests d'hypothèse afin d'éviter le biais de **data mining**.

---

## Idées clés

1. **Le test d'hypothèse ne doit pas être une sélection de stratégie.**

   Le but est de déterminer si la performance observée est due à une réelle capacité prédictive ou au hasard.

2. **L'ensemble d'entraînement — Train — est dédié à la recherche.**

   C'est ici que l'on génère et calibre des règles, mais ces résultats sont fortement biaisés.

3. **Le test d'hypothèse est appliqué après la phase d'exploration.**

   Il intervient sur l'ensemble **Test**, et non sur le **Train**, pour évaluer si la meilleure règle issue de la phase de recherche survit au « châtiment statistique ».

4. **La validation OOS — Out-of-Sample — est le juge final.**

   Elle ne doit jamais être utilisée pour des tests d'hypothèse ou des décisions de sélection, sous peine de contamination des données.

---

## Citation directe

> “Since the historical performance of the rules/signals discovered by data mining are upwardly biased, new statistical tests are required to make reasonable inferences about future profitability.”  
> *(Page 530)*

**Explication :** Cette citation signifie que les performances obtenues lors du développement d'une stratégie, par exemple lors d'un **backtest** classique, sont presque toujours surestimées.

L'utilisation de tests statistiques rigoureux est indispensable pour distinguer une stratégie réellement efficace du simple fruit du hasard ou du **data mining**.

---

## Vision macro

L'enjeu philosophique de l'EBTA est de transformer le trading d'une pratique basée sur l'intuition en une science observationnelle.

Le test d'hypothèse est le garde-fou qui empêche de prendre des décisions basées sur des corrélations fortuites.

Si on effectue les tests trop tôt ou sur les mauvaises données, notamment le **Train**, on tombe dans le piège de l'**overfitting**.

Si on les effectue trop tard, on manque une étape critique pour filtrer les règles non robustes.

---

## Vision micro

Le processus suit une logique stricte.

### 1. Phase de recherche — Train

On génère et sélectionne des règles candidates.

À ce stade, la performance est biaisée à la hausse, car les règles sont construites, ajustées ou choisies à partir de ces données.

### 2. Phase de correction statistique — Test

On applique ici le test d'hypothèse, par exemple le **White's Reality Check**.

On ne teste pas seulement la règle choisie, mais l'ensemble du processus de recherche, afin de voir si la meilleure règle bat le hasard de manière significative.

### 3. Phase de validation — OOS

Après avoir « gelé » le modèle suite au test d'hypothèse, on l'applique sur des données vierges.

Le but est d'obtenir une estimation non biaisée de la performance future, pas de refaire un test d'hypothèse ni de sélectionner une nouvelle stratégie.

---

## Exemples du livre

David Aronson illustre ses propos par l'optimisation d'une règle de croisement de deux moyennes mobiles : une moyenne mobile courte et une moyenne mobile longue.

- **Contexte :** toutes les combinaisons de fenêtres sont testées sur les données d'entraînement, c'est-à-dire le **Train**.
- **Ce qu'il montre :** plus on teste de variantes sur le **Train**, plus la performance augmente artificiellement par **data mining**.
- **Conséquence :** il est impératif de soumettre ces résultats à des tests statistiques sur un jeu de données indépendant, le **Test**, avant de conclure à une quelconque validité.

---

## Résumé simplifié

Le test d'hypothèse ne doit **jamais** être utilisé sur les données qui ont servi à construire ou entraîner votre stratégie.

Il sert à valider si les résultats sont réels.

1. Vous cherchez sur le **Train**.
2. Vous testez la solidité statistique sur le **Test**.
3. Vous validez la performance finale sur l'**OOS**, sans plus rien modifier.

> Si vous testez votre hypothèse sur le **Train**, vous trichez avec les statistiques et vous ne saurez jamais si votre stratégie fonctionnera demain.

---

## Actions concrètes

- **Ce qu'il faut faire :** appliquer des tests de significativité statistique, comme le **White's Reality Check**, uniquement sur l'ensemble **Test**.
- **Ce qu'il faut éviter :** utiliser les données de validation **OOS** pour sélectionner ou modifier des paramètres, car cela invalide l'OOS.
- **Ce qu'il faut mesurer :** la significativité statistique de la règle gagnante, en prenant en compte le nombre total de règles testées initialement.
- **Ce qu'il faut tester :** la capacité du modèle à battre l'hypothèse nulle $H_0$.

---

## Limites et erreurs fréquentes

### Limites

Le test d'hypothèse ne prouve pas la rentabilité future.

Il mesure la probabilité que les résultats passés soient le fruit du hasard.

### Erreurs fréquentes

- **Confondre le Train et le Test :** appliquer les tests statistiques sur le **Train** conduit inévitablement au surapprentissage.
- **Réutiliser l'OOS :** une fois que vous avez regardé les résultats sur l'**OOS**, ces données ne sont plus vierges. Les réutiliser pour ajuster le modèle est une erreur fatale de **data snooping**.
- **Ignorer le data mining bias :** tester des centaines de règles et ne garder que la meilleure sans ajuster la significativité statistique, par exemple via des tests comme celui de White, est la source principale d'échec en trading quantitatif.

---

## À retenir absolument

1. Le **Train** sert à la découverte, le **Test** au filtrage statistique, et l'**OOS** à la validation finale.
2. Tout test d'hypothèse effectué sur des données ayant servi à la recherche est invalide.
3. Le **data mining** crée des illusions de performance qu'il faut corriger mathématiquement.
4. L'**OOS** est une zone sacrée qui ne doit être consultée qu'une seule fois.
5. Une règle qui ne bat pas le hasard au test statistique doit être rejetée, quelle que soit sa performance sur le **Train**.
