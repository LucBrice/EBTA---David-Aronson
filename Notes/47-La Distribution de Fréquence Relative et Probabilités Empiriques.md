---
exported: 2026-06-12T08:58:10.536Z
source: NotebookLM
type: note
title: "47-La Distribution de Fréquence Relative et Probabilités Empiriques"
---

# 47-La Distribution de Fréquence Relative et Probabilités Empiriques

导出时间: 12/06/2026 10:58:10

---

### **CH 4 - 10 : RELATIVE FREQUENCY DISTRIBUTION OF** f−g

**(AJOUT) Idées clés :**

**Normalisation des données :** La fréquence relative consiste à diviser le nombre d'apparitions d'une valeur par le nombre total d'observations\[1\].

**Représentation visuelle :** Dans ce graphique, la hauteur de chaque barre représente une proportion (fraction de 1) et non plus un compte absolu\[1\]\[3\].

**Propriété d'unité :** La somme de toutes les fréquences relatives dans une distribution est impérativement égale à 1,0, soit 100 % des observations\[4\]\[5\].

**Fondement de la probabilité :** Ce type de distribution permet de transformer des fréquences observées en probabilités empiriques\[2\].

**Référence :**_Relative Frequency Distribution of f-g_, pages 181 à 183 et 193 à 200\[1\].

**Citation Directe :**« In the relative frequency distribution, the height of a bar represents the number of observed occurrences relative to (divided by) the total number of observations comprising the distribution. » (Page 181)\[1\]\[3\].

**Vision Macro :**L'enjeu est de passer de la simple description de données à la quantification de l'incertitude\[8\]\[9\]. Aronson explique que pour tester une règle de trading, nous avons besoin d'un langage commun : la probabilité\[10\]\[11\]. La distribution de fréquence relative est l'outil qui permet ce passage, car elle ne dit pas seulement combien de fois un profit est arrivé, mais quelle est sa part de "place" dans l'univers des possibles\[12\]. C'est ce qui permet de dire si un profit de backtest est "banal" ou "exceptionnel"\[10\]\[15\].

**Vision Micro :**La construction d'une distribution de fréquence relative pour la statistique f−g repose sur un mécanisme mathématique précis :

**Calcul de la fréquence relative (**Freqrel​**) :** On utilise la formule : Nombre total d’opportuniteˊsNombre d’occurrences d’un eˊveˊnement​\[2\]\[7\].

_Exemple du livre :_ Si la valeur f−g\=0,60 est apparue dans 10 échantillons sur un total de 50, sa fréquence relative est de 10/50\=0,20\[1\]\[3\].

**Géométrie de la distribution :** Sur l'axe vertical, l'échelle va désormais de 0 à 1 (ou 0% à 100%)\[4\].

**L’équivalence fréquence-aire :** Puisque le total des fréquences vaut 1,0, l'aire d'une barre spécifique représente la probabilité exacte d'obtenir cette valeur par hasard\[4\].

**Convergence (Loi des Grands Nombres) :** À mesure que le nombre d'observations augmente, la fréquence relative observée se rapproche de la probabilité théorique réelle de la population\[16\].

**(AJOUT) Résumé Simplifié :**Au lieu de dire "j'ai eu 10 fois ce résultat", on dit "ce résultat est arrivé dans 20 % des cas"\[1\]\[3\]. Cela permet de comparer des tests de tailles différentes sur une base commune de 100 %. C'est ce qui permet aux statisticiens de calculer tes chances de gagner en fonction de la "place" que prend ton profit sur le graphique\[12\]\[14\].

**Actions Concrètes :**

**Standardiser les backtests :** Convertissez toujours vos comptes de trades gagnants/perdants en pourcentages (fréquences relatives) pour évaluer la stabilité de votre avantage\[7\]\[8\].

**Calculer les probabilités de "queue" :** Pour savoir si votre stratégie a du talent, additionnez les aires (fréquences relatives) de toutes les barres situées à droite de votre profit moyen pour obtenir votre p-value\[5\].

**Vérifier la somme :** Assurez-vous que votre logiciel de statistiques affiche une distribution dont la somme totale est égale à 1,0, garantissant qu'aucun événement n'a été oublié\[4\]\[5\].

**(AJOUT) À retenir absolument :**

**Fréquence relative = Probabilité empirique**\[2\]\[7\].

La hauteur d'une barre indique la **probabilité** de ce résultat\[1\]\[3\].

L'aire totale sous l'histogramme est toujours **1,0 (100 %)**\[4\]\[5\].

C'est l'outil indispensable pour **rejeter l'Hypothèse Nulle**\[10\].

Plus l'échantillon est grand, plus cette distribution est **fiable**\[16\]\[19\].

J'ai terminé l'analyse de la distribution de fréquence relative de f−g selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[3] undefined
[4] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] undefined
[7] undefined
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[9] undefined
[10] undefined
[11] undefined
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] undefined
[15] undefined
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[19] undefined
