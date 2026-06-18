---
exported: 2026-06-12T08:57:30.663Z
source: NotebookLM
type: note
title: "81-Le Paradoxe de l'Asymétrie en Inférence Statistique"
---

# 81-Le Paradoxe de l'Asymétrie en Inférence Statistique

导出时间: 12/06/2026 10:57:30

---

### **CH 5 - 6 : HYPOTHESIS TESTS VERSUS CONFIDENCE INTERVALS - POTENTIAL CONFLICT**

Cette section explore une situation paradoxale où les deux outils de l'inférence statistique (le test d'hypothèse et l'intervalle de confiance) peuvent aboutir à des conclusions opposées concernant la validité d'une règle de trading\[1\].

**Idées clés :**

**Divergence possible :** Un test d'hypothèse peut rejeter la chance (p-value < 0,05) alors que l'intervalle de confiance suggère une possible espérance de gain négative\[1\]\[2\].

**Focalisation des queues :** Le conflit provient du fait que le test d'hypothèse se concentre sur la queue droite de la distribution, tandis que l'intervalle de confiance (IC) se concentre sur la queue gauche\[1\].

**L'asymétrie comme cause :** Ce problème survient uniquement lorsque la distribution d'échantillonnage n'est pas symétrique (distribution asymétrique ou _skewed_)\[3\]\[4\].

**Le rôle régulateur du CLT :** Grâce au Théorème Central Limite (Central Limit Theorem), ce conflit est rare pour les moyennes de grands échantillons, car la distribution tend naturellement vers la symétrie\[4\]\[5\].

**Référence :**

_Hypothesis Tests versus Confidence Intervals: Potential Conflict_, pages 250 à 252\[1\]\[5\].

**Citation Directe :**

« It is possible for a hypothesis test and a confidence interval to lead to different conclusions about a rule’s expected return. » (Page 250)\[1\].

\--------------------------------------------------------------------------------

**Vision Macro :**

L'enjeu est la fiabilité du verdict scientifique. David Aronson explique qu'en théorie, ces deux outils devraient être en parfait accord : si la borne inférieure d'un intervalle de confiance à 90 % est au-dessus de zéro, alors le hasard devrait être rejeté avec une p-value de 0,05\[6\]. Cependant, le trading réel traite souvent avec des données imparfaites. Ce chapitre avertit le trader EBTA : la "signification statistique" (rejet du hasard) ne garantit pas toujours une sécurité totale contre les pertes si la structure de la distribution des rendements est irrégulière\[2\].

\--------------------------------------------------------------------------------

**Vision Micro :**

Le mécanisme de ce conflit repose sur la géométrie de la distribution d'échantillonnage :

**L'asymétrie (Skewness) :** Si la distribution est "étirée" vers la gauche (asymétrie négative), la queue droite (utilisée par le test) peut être très courte et la queue gauche (utilisée par l'IC) très longue\[3\].

**Le paradoxe du test :** Parce que la queue droite est courte, le rendement observé peut tomber dans la zone des 5 % supérieurs de la distribution de la chance, entraînant le rejet de H0​ (la règle est jugée "bonne")\[3\]\[4\].

**Le paradoxe de l'IC :** En déplaçant cette même distribution asymétrique sur le profit réel pour calculer l'intervalle de confiance, la queue gauche (qui est très longue) peut s'étendre bien en dessous de zéro\[2\]\[4\].

**Conséquence :** On se retrouve avec une règle "statistiquement significative" mais dont l'intervalle de confiance indique qu'il y a plus de 5 % de probabilité que le rendement réel futur soit négatif\[2\].

\--------------------------------------------------------------------------------

**Résumé Simplifié :**

Parfois, vos statistiques vous envoient des messages contradictoires. Le test d'hypothèse vous dit : "Ton profit est trop bizarre pour être dû au hasard". Mais l'intervalle de confiance vous dit : "Attention, avec mes calculs, tu as encore de fortes chances de perdre de l'argent à l'avenir". Ce "bug" statistique arrive quand vos résultats de trading ne sont pas équilibrés (quand ils ne forment pas une belle courbe en cloche symétrique)\[3\]\[4\].

\--------------------------------------------------------------------------------

**Exemple du livre pour mieux comprendre :**

**La distribution asymétrique (Figure 5.22) :** Aronson présente une courbe fortement asymétrique vers la gauche. En bas de l'image, le test de H0​ montre que le profit est dans la zone rare (< 0,05). En haut de l'image, l'IC à 90 % centré sur ce même profit montre une borne inférieure qui "plonge" sous le zéro. La règle est validée par le test mais reste suspecte selon l'IC\[4\].

\--------------------------------------------------------------------------------

**Actions Concrètes :**

**Vérifier la symétrie :** Ne vous contentez pas de la p-value ; regardez si la distribution Bootstrap générée est symétrique\[3\]\[4\].

**Priorité à la prudence :** En cas de conflit, Aronson suggère qu'une position conservatrice consiste à douter de la règle si l'IC inclut des valeurs négatives\[2\].

**Augmenter la taille N :** Plus vous testez votre règle sur un grand nombre de jours/trades, plus le Théorème Central Limite rendra votre distribution symétrique, éliminant ainsi ce risque de conflit\[4\]\[5\].

\--------------------------------------------------------------------------------

**À retenir absolument :**

Le conflit naît de l'**asymétrie** de la distribution\[3\].

Test d'hypothèse = focus sur la **queue droite** (rejet de H0​)\[1\].

Intervalle de confiance = focus sur la **queue gauche** (mesure du risque de perte)\[1\].

Le **Théorème Central Limite** résout généralement ce problème pour les échantillons larges (N élevé)\[4\].

Un résultat peut être statistiquement "significatif" tout en ayant une borne d'IC **négative**\[2\].

J'ai terminé l'analyse du conflit potentiel entre les tests d'hypothèse et les intervalles de confiance selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
