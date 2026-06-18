---
exported: 2026-06-12T08:58:48.947Z
source: NotebookLM
type: note
title: "BLP2 - Calcul de la p-value en trading algorithmique selon l'EBTA"
---

# BLP2 - Calcul de la p-value en trading algorithmique selon l'EBTA

导出时间: 12/06/2026 10:58:48

---

Pour calculer une **p-value** selon la méthode EBTA, vous devez transformer vos résultats de backtest en une distribution de probabilité afin de mesurer si votre performance est due au talent ou à la chance\[1\]\[2\].

Voici la procédure exacte tirée du livre pour réaliser ce calcul.

### **Idées clés**

**Les données de base :** Le calcul se fait exclusivement sur les **rendements quotidiens détrendés** de la règle\[3\]\[4\].

**La méthode :** On utilise le **Bootstrap** ou la **Permutation Monte Carlo** pour créer une "distribution d'échantillonnage"\[5\]\[6\].

**Le principe :** La p-value est la proportion de résultats aléatoires qui font "aussi bien ou mieux" que votre stratégie réelle\[7\]\[8\].

**Le seuil :** Un résultat est jugé statistiquement significatif si la p-value est inférieure ou égale à **0,05**\[9\]\[10\].

### **Référence**

_STATISTICAL ANALYSIS: THE SAMPLING DISTRIBUTION_ (Pages 189–215) ; _HYPOTHESIS TESTING: THE MECHANICS_ (Pages 228–248)\[1\].

### **Citation Directe**

« P-value is the probability that the observed value of the test statistic could have occurred conditioned upon the hypothesis being tested (Ho) is true. » (Page 232)\[13\]._(Traduction : La p-value est la probabilité que la valeur observée de la statistique de test ait pu se produire à la condition que l'hypothèse testée (Ho) soit vraie.)_

### **Vision Macro**

L'enjeu est de répondre à la question : « Ai-je eu de la chance ? »\[14\]\[15\]. Un backtest positif n'est qu'un fait historique sans valeur si l'on ne prouve pas qu'il est improbable qu'un tel résultat provienne du hasard\[1\]\[2\]. La p-value est le "détecteur de bruit" qui permet de rejeter l'Hypothèse Nulle (H0​), laquelle affirme que votre règle n'a aucun pouvoir prédictif\[16\]\[17\].

### **Vision Micro : Comment calculer la p-value**

**1\. Sur quelles données travailler ?**

Le calcul doit être effectué sur les **rendements (P&L) quotidiens** de votre règle\[18\]\[19\]. Ces rendements doivent impérativement être calculés sur des **données de marché détrendées** (où la tendance moyenne a été soustraite) pour isoler le talent du biais de position\[3\].

**2\. La procédure par Bootstrap (Pas à pas)**

C’est la méthode privilégiée par Aronson pour tester une règle unique\[22\]\[23\] :

**Étape A (Centrage sur zéro) :** Prenez votre série de rendements quotidiens détrendés et soustrayez-en la moyenne. Cela crée une règle "fictive" dont le rendement moyen est exactement 0 (conforme à l'hypothèse nulle)\[24\]\[25\].

**Étape B (Rééchantillonnage) :** Utilisez un ordinateur pour tirer au sort (avec remise) des jours dans cette série jusqu'à reconstruire un historique de la même durée que votre test\[26\]\[27\].

**Étape C (Répétition) :** Répétez l'opération 5 000 fois pour obtenir 5 000 rendements moyens différents\[27\].

**Étape D (Comparaison) :** Placez votre rendement réel (non centré sur zéro) sur cette distribution de 5 000 résultats\[29\]\[30\].

**3\. Le calcul final**

La p-value est égale à la fraction de la distribution (les 5 000 simulations) dont les valeurs sont égales ou supérieures à votre rendement observé\[7\]\[29\].

_Exemple :_ Si sur 5 000 simulations de hasard, seulement 100 font mieux que vous, votre p-value est de 100/5000\=0,02\[8\].

### **Résumé Simplifié**

La p-value, c'est le pourcentage de chances que le hasard fasse mieux que toi\[13\]\[30\]. On crée 5 000 stratégies "idiotes" (basées sur tes propres données mais mélangées pour supprimer le talent) et on regarde combien d'entre elles battent ta stratégie réelle. Si c'est moins de 5 %, tu as probablement un vrai avantage\[9\]\[10\].

### **Actions Concrètes**

**Collectez vos Daily Returns :** Exportez chaque rendement quotidien de votre backtest sur données détrendées\[18\]\[31\].

**Vérifiez le centrage :** Avant de simuler, assurez-vous que la moyenne de vos données pour le test de hasard est de 0\[24\]\[25\].

**Exécutez 5 000 itérations :** Un nombre trop faible de simulations (ex: 50) rendra la p-value imprécise\[32\]\[33\].

**Appliquez la correction de minage :** Si vous avez testé 1 000 règles pour n'en garder qu'une, vous ne pouvez pas utiliser une p-value standard ; vous devez utiliser le "Reality Check" de White qui compare votre règle au _maximum_ des rendements du hasard\[23\].

### **À retenir absolument**

Le calcul se fait sur les **rendements détrendés**\[4\]\[36\].

La p-value mesure la **conformité au hasard**\[37\]\[38\].

P-value **\> 0,05** = Résultat non significatif (poubelle)\[9\].

P-value **< 0,01** = Résultat très significatif\[9\].

Plus vous testez de règles (data mining), plus la p-value réelle augmente (elle devient plus difficile à battre)\[41\]\[42\].
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] undefined
[7] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[9] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[10] undefined
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[15] undefined
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[17] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[18] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[19] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[22] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[23] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[24] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[25] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[26] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[27] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[29] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[30] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[31] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[32] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[33] undefined
[36] undefined
[37] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[38] undefined
[41] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[42] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
