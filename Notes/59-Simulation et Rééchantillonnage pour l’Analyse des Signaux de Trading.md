---
exported: 2026-06-12T08:57:58.431Z
source: NotebookLM
type: note
title: "59-Simulation et Rééchantillonnage pour l’Analyse des Signaux de Trading"
---

# 59-Simulation et Rééchantillonnage pour l’Analyse des Signaux de Trading

导出时间: 12/06/2026 10:57:58

---

### **CH 4 - 25 : DERIVING THE SAMPLING DISTRIBUTION WITH THE COMPUTER-INTENSIVE APPROACH**

Voici l'analyse des méthodes intensives par ordinateur (Bootstrap et Permutation de Monte Carlo), qui constituent le cœur technologique de l'approche EBTA pour évaluer les signaux de trading\[1\]\[2\].

**Idées clés :**

**Solution au problème de l'échantillon unique :** Ces méthodes permettent d'estimer la variabilité d'une statistique de performance alors qu'on ne dispose que d'un seul historique de marché\[2\]\[3\].

**Rééchantillonnage (Resampling) :** La forme de la distribution d'échantillonnage est approximée en réutilisant (« recyclant ») intelligemment les données de l'échantillon original des milliers de fois\[2\]\[4\].

**Indépendance vis-à-vis de la forme des données :** Contrairement à l'approche classique, ces méthodes ne supposent pas que les rendements suivent une courbe en cloche (normale), ce qui les rend plus robustes pour les marchés financiers\[5\]\[6\].

**Création d'un "Benchmark" du hasard :** Elles simulent ce qu'un "trader de bruit" (sans aucun talent) obtiendrait, fournissant ainsi un étalon pour juger la règle réelle\[7\]\[8\].

**Référence :**

_Deriving the Sampling Distribution with the Computer-Intensive Approach_ (Pages 215, 234 à 243)\[1\].

**Citation Directe :**

« Computer-intensive methods estimate the sampling distribution's shape by randomly resampling (reusing) the original sample of observation so as to produce new computer-generated samples. » (Page 236)\[2\].

**Vision Macro :**

L'enjeu est de s'affranchir des limites de l'histoire unique\[3\]\[10\]. David Aronson explique que, puisque nous ne pouvons pas observer 1 000 versions parallèles du passé boursier pour tester notre règle, nous devons utiliser la puissance de calcul pour les simuler\[11\]\[12\]. Cette approche transforme le backtest d'une simple observation historique en une preuve statistique rigoureuse, permettant de distinguer si un profit est dû au talent ou à une coïncidence chanceuse entre les signaux et le bruit du marché\[7\]\[13\].

**Vision Micro :**

Le mécanisme repose sur deux algorithmes distincts qui testent des versions légèrement différentes de l'Hypothèse Nulle (H0​)\[14\] :

**Le Bootstrap (Rééchantillonnage avec remise) :**

**Principe :** On considère l'échantillon original comme une représentation miniature de la population\[2\]\[15\].

**Ajustement :** On soustrait la moyenne des rendements du backtest de chaque rendement quotidien pour "centrer" les données sur zéro (conformité à H0​)\[16\]\[17\].

**Procédure :** On tire au sort N rendements (où N est la taille du backtest original) avec remise : chaque donnée peut être choisie plusieurs fois ou jamais\[18\]\[19\].

**Répétition :** On répète l'opération 5 000 fois pour obtenir 5 000 moyennes simulées formant la distribution\[19\]\[20\].

**La Permutation de Monte Carlo (MCP) :**

**Principe :** On brise le lien entre les signaux de la règle (+1/-1) et les rendements du marché\[8\]\[21\].

**Procédure :** On conserve la séquence temporelle des signaux, mais on mélange aléatoirement (scrambling) les rendements du marché\[8\]\[22\].

**Calcul :** On apparie chaque signal à un rendement mélangé, créant une "règle de bruit" totalement dénuée de pouvoir prédictif\[8\]\[23\].

**Répétition :** En faisant cela 5 000 fois, on définit la plage de profits qu'il est possible d'obtenir par pur accident\[23\]\[24\].

**Résumé Simplifié :**

Puisque tu n'as qu'un seul passé boursier, ces méthodes utilisent l'ordinateur pour "secouer" ton backtest dans un bocal. Le Bootstrap mélange tes propres résultats pour voir s'ils sont stables, tandis que le Monte Carlo apparie tes signaux avec des jours de bourse tirés au sort. Si ton vrai profit est bien meilleur que ces milliers de tests "mélangés", alors tu as probablement un avantage réel\[2\].

**Exemples du livre pour mieux comprendre :**

**La règle TT-4-91 :** Testée sur le S&P 500, elle affichait +4,84 % de profit\[17\]. Le Bootstrap a généré 5 000 mondes où cette règle n'avait aucun talent\[25\]. Le résultat a montré que dans 6,9 % des cas (p-value = 0,069), le hasard seul faisait aussi bien ou mieux, rendant la règle "possiblement significative" mais incertaine\[25\]\[26\].

**L'analogie de la roulette :** Le Monte Carlo est comparé à une roue de casino où chaque case contient un rendement du marché\[7\]\[13\]. Faire tourner la roue pour chaque signal simule une stratégie qui parie au hasard\[8\]\[21\].

**Actions Concrètes :**

**Utiliser le rééchantillonnage pour les p-values :** Ne vous fiez pas aux formules classiques si vos rendements ne sont pas normaux ; utilisez le Bootstrap\[5\]\[6\].

**Appliquer le "Zero-Centering" :** Avant de simuler, ajustez toujours vos données pour qu'elles aient une moyenne de zéro, afin de tester correctement l'absence de talent\[16\]\[17\].

**Maintenir la taille d'échantillon (**N**) :** Pour que le Théorème du Bootstrap soit valide, vos simulations doivent impérativement avoir le même nombre de trades que votre backtest réel\[18\]\[19\].

**Utiliser White's Reality Check (WRC) :** Si vous avez testé des milliers de règles (data mining), utilisez cette version spécifique du Bootstrap qui ajuste la distribution pour le biais de sélection\[27\].

**À retenir absolument :**

L'ordinateur remplace les formules mathématiques complexes par de la **puissance de calcul**\[1\]\[2\].

Le **Bootstrap** simule la variabilité du profit ; le **Monte Carlo** simule l'absence de lien prédictif\[8\]\[14\].

On crée **5 000 mondes parallèles** pour vérifier si le nôtre est exceptionnel\[20\]\[23\].

C'est la méthode de référence d'Aronson car elle est **plus fiable** que l'approche classique sur les marchés financiers\[2\]\[5\].

Sans simulation, un profit de backtest n'est qu'une **statistique sans contexte**\[3\]\[30\].

J'ai terminé l'analyse de la dérivation de la distribution d'échantillonnage par l'approche intensive selon le protocole EBTA.
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
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] undefined
[13] undefined
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[15] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[17] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[18] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[19] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[20] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[21] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[22] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[23] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[24] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[25] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[26] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[27] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[30] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
