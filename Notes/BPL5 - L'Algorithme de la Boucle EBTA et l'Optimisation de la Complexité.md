---
exported: 2026-06-12T08:58:46.180Z
source: NotebookLM
type: note
title: "BPL5 - L'Algorithme de la Boucle EBTA et l'Optimisation de la Complexité"
---

# BPL5 - L'Algorithme de la Boucle EBTA et l'Optimisation de la Complexité

导出时间: 12/06/2026 10:58:46

---

Voici le blueprint complet de la « boucle EBTA », structuré pour intégrer votre approche de décomposition par composants, telle que David Aronson la décrit pour la recherche de règles à complexité variable.

### **(AJOUT) Idées clés :**

**Filtrage initial :** Élimination des composants « inutiles » (espérance de gain ≤ 0 sur données détrendées)\[1\]\[2\].

**Optimisation de la complexité :** Passage de la règle simple (composant) à la règle complexe (stratégie finale)\[3\]\[4\].

**Double loop (Boucle double) :** Une boucle pour les paramètres, une boucle pour l'ajout de composants\[5\]\[6\].

**Sanctuarisation de l'OOS :** Le verdict final n'a lieu qu'une seule fois sur des données jamais "visitées"\[5\]\[7\].

\--------------------------------------------------------------------------------

### **Référence :**

_Objective Rules and Their Evaluation_ (Pages 23–28) ; _Data-Mining Bias_ (Pages 255–256) ; _Case Study: Complex Rules and Complexity Optimization_ (Pages 456–461).

\--------------------------------------------------------------------------------

### **Citation Directe :**

« In its search for the nonlinear rule of optimal complexity, machine learning algorithms cycle through the training and testing sets in two distinct loops. The inner loop searches for the optimal parameters... The outer loop searches for the optimal level of complexity. » (Page 457)\[5\].

\--------------------------------------------------------------------------------

### **Vision Macro :**

L'enjeu est de construire une stratégie par **induction rigoureuse**. On ne "devine" pas la combinaison gagnante. On commence par les briques les plus simples (les composants) et on n'ajoute de la complexité (de nouveaux composants) que si et seulement si cela améliore la performance sur un segment de données "test" que la règle n'a pas utilisé pour ajuster ses paramètres\[6\]\[8\]. Cette boucle protège contre le **surajustement** ( _overfitting_ )\[4\]\[9\].

\--------------------------------------------------------------------------------

### **Vision Micro : La Boucle EBTA de A à Z**

**PHASE 1 : ÉVALUATION DES COMPOSANTS (La sélection naturelle)**

**Détrendage initial :** Soustrayez la tendance moyenne (ADC) du marché de vos données historiques\[10\].

**Backtest individuel :** Testez chaque composant (ex: un RSI seul, une MM seule) sur ces données détrendées\[10\]\[12\].

**Calcul de la P-Value :** Utilisez le Bootstrap ou Monte Carlo pour chaque composant\[13\].

**Élimination (Useless TA) :** Jetez impitoyablement tout composant dont le profit est ≤ 0 ou dont la p-value est > 0,05\[1\]. Il ne reste que le "pool" de composants avec un pouvoir prédictif probable.

**PHASE 2 : CONSTRUCTION DE LA STRATÉGIE (La boucle de complexité)**

_Divisez vos données restantes en deux :_ **Training Set** _(Entraînement) et_ **Test Set** _(Test)_\[5\]\[8\]_._

**Boucle Interne (Paramètres) :** Sur le _Training Set_, trouvez les meilleurs réglages (ex: période du RSI) pour vos composants sélectionnés\[5\]\[6\].

**Boucle Externe (Complexité) :**

Prenez votre meilleur composant (Règle 1)\[6\].

Ajoutez un second composant pour former une règle complexe (Règle 1 + Règle 2)\[3\]\[18\].

**Le test de vérité :** Mesurez la performance de cette règle complexe sur le **Test Set**\[5\]\[18\].

**Condition d'arrêt :** Continuez d'ajouter des composants tant que la performance sur le _Test Set_ augmente. Dès que la performance sur le _Test Set_ commence à baisser, vous avez atteint l' **Optimal Complexity**. Tout ajout supplémentaire ne fait que "mémoriser le bruit" ( _overfitting_ )\[6\]\[19\].

**PHASE 3 : LE VERDICT FINAL (L'inférence corrigée)**

**Correction du Minage :** Comme vous avez fait plusieurs "visites" au _Test Set_ pour choisir vos composants, la performance observée est biaisée\[7\]\[20\]. Utilisez le **White's Reality Check** sur la stratégie finale pour obtenir une p-value honnête\[21\].

**Validation Hors-Échantillon (OOS) :** Testez la stratégie finale sur le **Validation Set** (les données que vous n'avez jamais touchées, pas même pour tester les composants)\[5\]\[7\]. C'est le seul chiffre que vous pouvez "mettre à la banque"\[25\].

\--------------------------------------------------------------------------------

### **(AJOUT) Résumé Simplifié :**

C'est comme un casting :

Tu élimines les acteurs qui ne savent pas jouer (Détrendage + P-Value par composant).

Tu formes des duos ou trios et tu les fais jouer sur une scène de répétition (Boucle de complexité).

Tu ne gardes que la troupe qui performe le mieux en répétition sans en faire trop (Optimal complexity).

Tu ne juges leur vrai talent qu'au soir de la première, devant un public qu'ils n'ont jamais vu (Test OOS).

\--------------------------------------------------------------------------------

### **Actions Concrètes :**

**Ne mélangez pas tout :** Ne testez jamais vos composants sur les données qui serviront à la validation finale (OOS)\[5\]\[7\].

**Détectez le pic :** Surveillez le moment où votre stratégie devient "trop belle" sur les données d'entraînement mais s'effondre sur les données de test\[6\]\[18\].

**Utilisez le P&L détrendé partout :** Pour la sélection des composants ET pour l'évaluation de la stratégie finale\[10\]\[12\].

\--------------------------------------------------------------------------------

### **(AJOUT) À retenir absolument :**

Le détrendage est l'étape 0 de chaque phase de test\[10\]\[11\].

Ajouter un composant à une stratégie sans que cela améliore le _Test Set_ est une erreur scientifique\[6\]\[19\].

L'inférence statistique sur la stratégie finale doit corriger le fait que vous avez "cherché" les meilleurs composants\[24\].

La performance OOS est toujours inférieure à la performance de backtest\[28\]\[29\].

Une stratégie complexe validée est une "Règle Objective Significative" (Subset 4 de l'AT)\[30\].
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] undefined
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[7] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[9] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] undefined
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[18] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[19] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[20] undefined
[21] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[24] undefined
[25] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[28] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[29] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[30] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
