---
exported: 2026-06-12T08:58:11.752Z
source: NotebookLM
type: note
title: "46-L'Équivalence Géométrique : De l'Histogramme à la Probabilité"
---

# 46-L'Équivalence Géométrique : De l'Histogramme à la Probabilité

导出时间: 12/06/2026 10:58:11

---

### **CH 4 - 9 : THE EQUIVALENCE OF FREQUENCY AND AREA**

Voici l'analyse de la section consacrée à l'équivalence entre la fréquence et l'aire, un concept fondamental qui permet de transformer un graphique (histogramme) en un outil de calcul de probabilités.

**(AJOUT) Idées clés :**

**Représentation géométrique :** La surface (aire) occupée par les barres d'une distribution de fréquence correspond au nombre total d'observations\[1\]\[2\].

**Proportionnalité :** L'aire d'une barre spécifique représente la fraction du total des observations pour cette valeur précise\[3\]\[4\].

**Fondement de l'inférence :** Cette équivalence est ce qui permet d'utiliser les distributions pour mesurer la probabilité qu'un profit de backtest soit dû au hasard\[4\]\[5\].

**Cumulativité :** L'aire combinée de plusieurs barres adjacentes permet de calculer la probabilité d'une plage de résultats\[6\]\[7\].

**Référence :**

_The Equivalence of Frequency and Area_, pages 180 à 183\[1\].

**Citation Directe :**

« the bar's fractional area is equal to the fraction of the total observations represented by that bar. » (Page 180)\[3\]\[4\].

**Vision Macro :**

L'enjeu pour le trader EBTA est de passer d'une simple observation visuelle ("ce résultat a l'air rare") à une mesure mathématique précise ("ce résultat a X% de chances de se produire"). Aronson explique que sans cette conversion de l'aire en probabilité, le trader reste dans l'estimation subjective\[4\]\[5\]. Ce concept est le pont qui permet d'appliquer la rigueur statistique aux graphiques de performance, transformant un histogramme de backtest en un véritable "instrument de mesure" du hasard\[4\]\[5\].

**Vision Micro :**

Le mécanisme repose sur la géométrie de l'histogramme :

**L'Unité Totale :** Dans une distribution de fréquence relative, la somme de toutes les aires de barres est égale à 1,0 (soit 100% des données)\[8\]\[9\].

**Calcul d'une barre unique :** Si une barre associée à un rendement de +0,60 a une fréquence de 10 sur un total de 50 échantillons, elle représente 20% des observations (10/50 = 0,20). Géométriquement, l'aire de cette barre occupe exactement 0,20 de la surface totale du graphique\[3\].

**Calcul d'une zone (La Queue) :** Pour connaître la probabilité d'obtenir un résultat "égal ou supérieur" à une valeur donnée, on additionne les aires de toutes les barres situées à droite de cette valeur\[6\]\[7\].

_Exemple du livre :_ Pour obtenir la fréquence relative des valeurs de f−g≥0,65, on additionne les fréquences relatives des barres 0,65 (0,10), 0,70 (0,06), 0,75 (0,02) et plus. Le total de 0,20 signifie que cette zone représente 20% de l'aire totale\[6\]\[7\].

**Transition vers la densité :** Ce principe s'applique ensuite aux courbes lisses (fonctions de densité de probabilité) où l'aire sous la courbe entre deux points définit la probabilité\[10\]\[11\].

**(AJOUT) Résumé Simplifié :**

Imagine que ton graphique de résultats est un gâteau. La taille de chaque part (aire) te dit combien de fois ce résultat est arrivé. Si la part des "gros profits" représente 5% de la surface totale du gâteau, alors tu as 5% de chances d'obtenir ce résultat par pur hasard. Les statistiques utilisent la surface des graphiques pour calculer précisément tes chances de gagner ou de perdre.

**Actions Concrètes :**

**Analyser les "Queues" de distribution :** Ne regardez pas seulement la moyenne de vos trades, mais mesurez la surface occupée par vos meilleurs résultats sur l'histogramme pour voir s'ils sont statistiquement "normaux" ou exceptionnels\[4\]\[5\].

**Utiliser la Fréquence Relative :** Dans vos logiciels de backtest, paramétrez l'affichage pour que la hauteur des barres soit divisée par le nombre total de trades. Cela transforme immédiatement votre graphique en outil de probabilité\[9\]\[12\].

**Vérifier le cumul :** Si vous fixez un objectif de profit, additionnez l'aire de toutes les barres de l'histogramme situées au-dessus de cet objectif pour connaître votre probabilité réelle de succès basée sur l'échantillon\[6\].

**(AJOUT) À retenir absolument :**

**Aire = Probabilité** (dans une distribution de fréquence relative)\[6\]\[7\].

La surface totale du graphique vaut toujours **1,0 (100%)**\[8\]\[9\].

C'est la base du calcul de la **P-value** en trading\[14\].

Plus une barre est large ou haute, plus le résultat qu'elle représente est **probable**\[3\]\[4\].

Ce principe permet de quantifier **l'incertitude** de manière objective\[4\]\[5\].

J'ai terminé l'analyse de l'équivalence entre fréquence et aire selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] undefined
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] undefined
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[7] undefined
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[9] undefined
[10] undefined
[11] undefined
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] undefined
