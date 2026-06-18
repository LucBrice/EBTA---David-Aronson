---
exported: 2026-06-12T08:58:56.683Z
source: NotebookLM
type: note
title: "13-L'Illusion du Profit : Démasquer le Biais de Tendance en Backtesting"
---

# 13-L'Illusion du Profit : Démasquer le Biais de Tendance en Backtesting

导出时间: 12/06/2026 10:58:56

---

**Référence :** THE CONJOINT EFFECT OF POSITION BIAS AND MARKET TREND ON BACK-TEST PERFORMANCE (Pages 23–27).

**Citation Directe :** « The performance of a rule can be profoundly affected by factors that have nothing to do with its predictive power. » (Page 23)\[1\]\[2\].

**Vision Macro :**L'enjeu fondamental pour le trader EBTA est d'éliminer l'**illusion de la performance**\[3\]. Un backtest peut afficher un profit impressionnant sans que la règle ne possède la moindre "intelligence" ou pouvoir prédictif\[3\]\[4\]. Ce profit trompeur est souvent le résultat mécanique d'une exposition fortuite à la tendance dominante du marché pendant la période de test\[3\]. L'objectif est donc de distinguer ce qui relève du talent du trader (couplage intelligent entre position et mouvement) de ce qui relève de la simple "chance de position"\[3\]\[5\].

**Vision Micro :**La performance observée d'une règle est la somme de deux composantes : le pouvoir prédictif réel et l'interaction entre deux facteurs externes\[1\]\[5\] :

**Le biais de position (****Position Bias****) :** C'est le pourcentage de temps passé en position longue (+1) par rapport au temps passé en position courte (-1)\[4\]\[5\]. Si une règle a des conditions d'achat plus faciles à satisfaire (laxistes) que ses conditions de vente (restrictives), elle passera naturellement plus de temps à l'achat\[5\].

**La tendance nette du marché (****Market's Net Trend****) :** C'est la variation quotidienne moyenne (ADC) du prix durant le test\[4\]\[5\].

**L'effet conjoint :** Si vous testez une règle avec un biais acheteur (ex: long 75% du temps) sur une période où le marché est haussier (ADC > 0), la règle gagnera de l'argent par simple exposition, même si ses signaux sont générés de manière aléatoire\[5\]\[8\].

**L'exemple du livre (La Roulette) :** Aronson imagine une règle sans talent simulée par une roulette de 100 cases dont 75 sont marquées "+1" (long) et 25 sont marquées "-1" (short)\[5\]\[8\]. Chaque jour, on lance la roulette pour décider de la position. Si le marché monte en moyenne de 0,035% par jour sur 7 000 jours, cette règle affichera un profit positif significatif alors qu'elle est basée sur le pur hasard\[5\].

**Réponse sur le "filtrage" et la création de stratégie :**Dans la méthode EBTA, l'enjeu n'est pas de filtrer le signal _en fonction_ de la tendance lors de l'exécution, mais de **détrendrer les données lors de l'évaluation**\[10\].

**Pourquoi ?** Si vous ne "filtrez" pas (n'enlevez pas) la tendance des données de test, vous ne saurez jamais si votre règle est bonne ou si elle a juste bénéficié du marché haussier\[3\]\[14\].

**Conséquence :** Si une règle ne produit plus de profit sur des **données détrendées** (où la tendance moyenne est ramenée à zéro), cela signifie qu'elle n'a aucun pouvoir prédictif et qu'elle échouera dès que la tendance du marché changera ou s'inversera\[12\].

**Actions Concrètes :**

**Calculer le rendement attendu du hasard (ER) :** Utiliser la formule ER\=\[p(L)×ADC\]−\[p(S)×ADC\] pour quantifier ce qu'une règle nulle gagnerait par simple exposition\[17\]\[18\].

**Détrendrer les données :** Soustraire le changement quotidien moyen de chaque jour de la série de prix avant de calculer les profits du backtest\[13\]\[19\].

**Utiliser les données réelles pour les signaux :** Générer les signaux d'achat/vente sur les prix réels, mais calculer les gains/pertes (P&L) uniquement sur les données détrendées\[11\]\[13\].

**Vérifier la symétrie :** S'assurer que les conditions d'entrée en position longue ne sont pas plus "faciles" que les conditions de vente, pour éviter un biais de position involontaire qui fausserait les résultats\[7\]\[18\].
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] undefined
[3] undefined
[4] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] undefined
[7] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] undefined
[13] undefined
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[17] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[18] undefined
[19] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
