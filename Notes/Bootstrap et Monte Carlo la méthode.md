---
exported: 2026-06-12T08:57:57.351Z
source: NotebookLM
type: note
title: "Bootstrap et Monte Carlo : la méthode"
---

# Bootstrap et Monte Carlo : la méthode

导出时间: 12/06/2026 10:57:57

---

Voici l'analyse exhaustive des méthodes **Bootstrap** et **Monte Carlo**, piliers des tests d'inférence statistique en trading selon David Aronson.

### **Idées clés :**

**Solution au "Sample Unique" :** Ces méthodes permettent d'estimer la variabilité d'une stratégie alors qu'on ne dispose que d'un seul historique de marché\[1\]\[2\].

**Simuler l'infini :** Elles utilisent la puissance de calcul pour "recycler" les données et créer des milliers d'univers de backtests parallèles\[2\]\[3\].

**Différence de philosophie :** Le Bootstrap teste si le profit moyen est supérieur à zéro, tandis que Monte Carlo teste si le signal contient une information supérieure au hasard\[4\]\[5\].

**Signification statistique :** Elles fournissent le "benchmark" (étalon) nécessaire pour calculer la **p-value** et rejeter l'Hypothèse Nulle (H0​)\[6\]\[7\].

\--------------------------------------------------------------------------------

### **Référence :**

_Deriving the Sampling Distribution with the Computer-Intensive Approach_ (Pages 215, 234–243, 320–330).

### **Citation Directe :**

« Computer-intensive methods estimate the sampling distribution's shape by randomly resampling (reusing) the original sample of observation so as to produce new computer-generated samples. » (Page 236).

\--------------------------------------------------------------------------------

### **Vision Macro :**

L'enjeu est de sortir de l'anecdote historique pour entrer dans la preuve scientifique\[8\]\[9\]. Un backtest classique ne donne qu'un chiffre. Aronson explique que ce chiffre est "pollué" par la variabilité d'échantillonnage\[10\]. Sans simuler des milliers de variantes du passé, le trader ne peut pas savoir si sa stratégie a du "talent" ou si elle a simplement bénéficié d'une coïncidence chanceuse entre ses signaux et le bruit du marché\[11\].

\--------------------------------------------------------------------------------

### **Vision Micro : Cas d'usage et Limites**

**1\. La Méthode Bootstrap**

**Cas d'usage :** Idéal pour tester la rentabilité d'une règle unique et générer des **intervalles de confiance**\[12\]\[13\]. Il permet de voir comment la moyenne des profits fluctue si l'ordre des jours de bourse était différent\[14\].

**Limites :**

Dans sa forme basique, il ne convient pas aux règles issues du **data mining** (minage de données), car il ignore le biais de sélection\[3\]\[15\].

Il nécessite une modification (White's Reality Check) pour gérer des milliers de règles\[15\].

**2\. La Permutation de Monte Carlo (MCP)**

**Cas d'usage :** Spécifiquement conçu pour tester la **valeur informative** d'un signal\[16\]. Il permet de voir si une règle de "bruit" (totalement inutile) aurait fait aussi bien sur le même marché\[5\]\[17\].

**Limites :**

**Incapable de générer des intervalles de confiance**, car il ne teste pas un paramètre de population (comme la moyenne) mais brise le lien entre signal et prix\[12\].

Il teste une version différente de H0​ : l'absence totale de corrélation\[20\].

\--------------------------------------------------------------------------------

### **Processus détaillés pas à pas**

**Algorithme du Bootstrap (Rééchantillonnage avec remise)**\[21\] **:**

**Collecte :** Récupérer tous les rendements quotidiens du backtest original.

**Centrage sur zéro (Zero-Centering) :** Soustraire la moyenne des profits de chaque rendement quotidien. (Étape cruciale pour que le test simule une règle qui ne gagne rien, conformément à H0​)\[23\]\[25\].

**Tirage au sort :** Placer ces données "centrées" dans un seau virtuel.

**Resampling :** Tirer au hasard une donnée, noter sa valeur, et la **remettre** dans le seau.

**Construction d'un échantillon :** Répéter le tirage N fois (où N est le nombre exact de jours du backtest original)\[14\]\[24\].

**Calcul :** Calculer la moyenne de ce nouvel échantillon simulé.

**Répétition :** Recommencer les étapes 4 à 6 au moins **5 000 fois**.

**Verdict :** Créer l'histogramme de ces 5 000 moyennes. Si votre profit réel est dans les 5 % supérieurs (queue droite), la règle est statistiquement significative\[26\]\[27\].

**Algorithme de Monte Carlo (Permutation/Scrambling)**\[28\] **:**

**Isolation :** Prendre d'un côté la séquence des signaux de la règle (+1 pour achat, -1 pour vente) et de l'autre les rendements réels du marché (dé-tendancés).

**Mélange (Scrambling) :** Mélanger aléatoirement les rendements du marché comme un jeu de cartes\[5\]\[28\].

**Appariement :** Associer le signal du jour 1 avec un rendement de marché pris au hasard dans le paquet mélangé (sans remise cette fois)\[16\]\[29\].

**Calcul du profit :** Multiplier chaque signal par son rendement de marché associé et faire la moyenne pour obtenir le profit d'une "règle de bruit"\[33\].

**Répétition :** Recommencer le mélange et l'appariement **5 000 fois**.

**Verdict :** Comparer le profit du backtest réel à cette distribution de profits "accidentels". La p-value est la fraction de tests Monte Carlo qui ont fait mieux que votre règle\[32\]\[33\].

\--------------------------------------------------------------------------------

### **Résumé Simplifié :**

Le **Bootstrap**, c'est comme reprendre tous tes trades passés, les mettre dans un sac et en piocher au hasard pour voir si, en changeant l'ordre ou la fréquence de certains jours, tu serais toujours gagnant\[21\]. Le **Monte Carlo**, c'est comme si un singe tapait au hasard sur les touches "Achat" et "Vente" : on regarde si ton score est vraiment meilleur que celui du singe sur des milliers de tentatives\[5\].

\--------------------------------------------------------------------------------

### **Actions Concrètes :**

**Utilisez le Bootstrap** pour estimer la fourchette de gains futurs probables (intervalles de confiance)\[12\].

**Utilisez Monte Carlo** pour débusquer les règles qui semblent marcher mais qui ne font que profiter de quelques gros mouvements de marché par pur hasard\[5\].

**Exemple du livre (TT-4-91) :** Sur cette règle, le Bootstrap a montré une p-value de 0,069. Cela signifie qu'il y a 6,9 % de chances que le hasard fasse aussi bien, ce qui rend la règle "possiblement" mais pas "hautement" significative\[26\]\[27\].

\--------------------------------------------------------------------------------

### **À retenir absolument :**

Le Bootstrap simule la **variabilité** ; Monte Carlo simule l'**absence de talent**\[4\]\[5\].

Le **centrage sur zéro** est obligatoire pour le Bootstrap avant le test\[23\]\[25\].

Monte Carlo est **public** ; le Bootstrap pour test de règles est souvent **breveté** (ex: WRC)\[34\]\[35\].

Plus on fait de simulations (ex: 5 000), plus la **p-value** est précise\[17\]\[24\].

La p-value est la **seule mesure** qui sépare scientifiquement le trader de l'illusionniste\[36\].

J'ai terminé l'analyse des méthodes Bootstrap et Monte Carlo selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[7] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[9] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[15] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[17] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[20] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[21] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[23] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[24] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[25] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[26] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[27] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[28] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[29] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[32] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[33] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[34] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[35] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[36] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
