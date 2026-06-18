---
exported: 2026-06-12T08:57:42.461Z
source: NotebookLM
type: note
title: "70-L'Arbitrage Statistique entre Chance et Performance de Trading"
---

# 70-L'Arbitrage Statistique entre Chance et Performance de Trading

导出时间: 12/06/2026 10:57:42

---

### **CH 5 - 5 : p-value, Statistical Significance, and Rejecting the Null Hypothesis**

Cette section définit les critères de décision mathématiques qui permettent à un trader EBTA de conclure si une stratégie de trading mérite d'être exploitée ou si elle doit être jetée aux oubliettes de la chance statistique.\[1\],\[2\]

**(AJOUT) Idées clés :**

**Mesure de la rareté :** La p-value est la probabilité qu'un rendement de backtest soit dû à la simple variabilité d'échantillonnage (chance) sous l'Hypothèse Nulle (H0​).\[3\],\[4\],\[5\]

**Critère de signification :** Un résultat est dit "statistiquement significatif" si sa p-value est inférieure à un seuil prédéfini, généralement 0,05.\[6\],\[4\],\[7\],\[8\]

**Conformité inversée :** Une p-value élevée indique que le résultat est conforme à H0​ (le hasard), tandis qu'une p-value faible indique une non-conformité.\[9\]

**Biais du data mining :** Pour le minage de données, le seuil de 0,05 est insuffisant et doit être ajusté pour éviter les "faux positifs" massifs.\[6\],\[10\],\[11\],\[12\]

**Référence :**

_p-value, Statistical Significance, and Rejecting the Null Hypothesis_, pages 232 à 234. (Voir aussi _Statistical Analysis_, page 171).\[13\],\[7\],\[6\]

**Citation Directe :**

« The smaller the p-value, the more statistically significant the test result. A statistically significant result is one for which the p-value is low enough to warrant a rejection of H0​. » (Page 232).\[9\]

**Vision Macro :**

L'enjeu est de ne pas "parier sur le bruit"\[14\]. David Aronson explique que le trader est constamment confronté à des profits passés qui semblent séduisants, mais qui n'ont aucune valeur prédictive\[15\],\[16\]. La p-value agit comme un juge de paix : elle quantifie le degré de "surprise"\[9\]. Si le résultat est trop surprenant pour être le fruit du hasard, le trader a une base rationnelle pour engager son capital\[17\],\[18\]. Sans cette rigueur, le trading n'est qu'une forme de crédulité face aux coïncidences\[19\],\[20\].

**Vision Micro :**

Le mécanisme de la p-value fonctionne selon une probabilité conditionnelle stricte :

**Le calcul de l'aire :** Graphiquement, la p-value est la fraction de l'aire sous la courbe de la distribution d'échantillonnage (centrée sur zéro) située à droite du rendement observé.\[21\],\[22\],\[23\]

**L'échelle de signification :** Aronson utilise des standards conventionnels :\[7\]

p≤0,10 : Résultat "possiblement significatif".\[7\]

p≤0,05 : Résultat "statistiquement significatif" (standard scientifique).\[7\]

p≤0,01 : Résultat "très significatif".\[7\]

p≤0,001 : Résultat "hautement significatif".\[7\]

**La décision de rejet :** Si la p-value est inférieure au seuil (alpha), on rejette H0​ et on adopte l'Hypothèse Alternative (HA​).\[4\]

**Lien avec l'Erreur de Type I :** La p-value représente précisément le risque que vous prenez de rejeter H0​ alors qu'elle est en réalité vraie (croire au talent alors que c'est de la chance).\[4\],\[7\]

**(AJOUT) Résumé Simplifié :**

La p-value est le "pourcentage de chance que tu sois en train de te faire avoir par un coup de bol"\[3\],\[24\]. Si ce pourcentage est très bas (moins de 5 %), la science t'autorise à dire que ta stratégie a probablement un vrai pouvoir de prédiction\[8\]. Si c'est au-dessus, tu dois admettre que n'importe quel imbécile aurait pu obtenir le même résultat par pur hasard\[25\],\[26\].

**Exemples du livre pour mieux comprendre :**

**Le test à +3,5 % :** Une règle affiche +3,5 % de profit. Le test montre que 10 % des simulations de hasard atteignent ou dépassent ce score (p\=0,10). Ce n'est pas suffisant pour rejeter la chance avec certitude (Figure 5.9).\[22\],\[13\],\[23\]

**Le cas du Data Mining :** Si vous testez 1 000 règles, environ 50 d'entre elles auront une p-value de 0,05 par pur hasard (faux positifs). Aronson montre qu'un profit de +37 % peut paraître génial (p<0,05 seul), mais devenir médiocre (p\=0,45) une fois ajusté pour le nombre de tests effectués (Figure 6.9 & 6.10).\[11\],\[27\],\[28\],\[29\]

**Actions Concrètes :**

**Fixer le seuil alpha :** Déterminez votre tolérance au risque de "faux positif" (ex: 0,05) avant même de commencer le backtest.\[4\],\[30\]

**Calculer systématiquement la p-value :** Ne regardez jamais un profit de backtest sans sa p-value associée.\[31\]

**Se méfier des p-values "limites" :** Un score de 0,04 est fragile ; visez des p-values beaucoup plus basses si vous avez exploré beaucoup de règles.\[12\],\[32\]

**Distinguer Signification Statistique et Pratique :** Une p-value de 0,001 sur un profit de 0,1 % signifie que le talent est réel, mais que le gain est trop faible pour couvrir les frais.\[30\]

**(AJOUT) À retenir absolument :**

**La p-value n'est pas** la probabilité que votre règle soit "bonne" ; c'est la probabilité que le **hasard ait fait aussi bien**.\[33\],\[5\]

p<0,05 est la porte d'entrée de la crédibilité scientifique.\[6\]

Une p-value élevée est une **absence de preuve**, pas une preuve que la règle est nulle.\[34\]

Plus la p-value est **petite**, plus vous pouvez être **confiant** dans votre rejet de la chance.\[9\]

Le **Data Mining** rend les p-values classiques totalement mensongères.\[35\],\[29\]

J'ai terminé l'analyse de la p-value et de la signification statistique selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] undefined
[6] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[7] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[8] undefined
[9] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] undefined
[15] undefined
[16] undefined
[17] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[18] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[19] undefined
[20] undefined
[21] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[22] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[23] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[24] undefined
[25] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[26] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[27] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[28] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[29] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[30] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[31] undefined
[32] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[33] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[34] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[35] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
