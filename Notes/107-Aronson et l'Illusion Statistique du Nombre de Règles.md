---
exported: 2026-06-12T08:57:02.461Z
source: NotebookLM
type: note
title: "107-Aronson et l'Illusion Statistique du Nombre de Règles"
---

# 107-Aronson et l'Illusion Statistique du Nombre de Règles

导出时间: 12/06/2026 10:57:02

---

### **CH 6 : EXPERIMENT SET 1 - FACTOR 1: NUMBER OF RULES TESTED**

Cette section présente la première série d'expériences de David Aronson visant à isoler l'impact du nombre de règles testées sur l'ampleur du biais de minage de données, en utilisant des règles à mérite nul.

\--------------------------------------------------------------------------------

**Idées clés :**

**Mérite nul contrôlé :** Toutes les règles artificielles (ATR) sont paramétrées avec une probabilité de gain de 0,50, soit une espérance de rendement de zéro\[1\].

**Corrélation Biais/Nombre :** Plus le nombre de règles testées (N) augmente, plus le biais de minage de données (la surestimation du profit) est important\[1\]\[2\].

**Croissance log-linéaire :** L'ampleur du biais croît de manière quasi linéaire par rapport au logarithme du nombre de règles testées\[3\].

**Illusion de performance :** Dans un univers de 400 règles totalement inutiles, la meilleure peut afficher un profit annuel de +48 % par pur hasard sur une période de 24 mois\[3\]\[4\].

\--------------------------------------------------------------------------------

**Référence :**

_Experiment Set 1: Data Mining ATRs of Equal Merit - Factor 1: Number of Rules Tested_ (Pages 294–299).

\--------------------------------------------------------------------------------

**Citation Directe :**

« More monkeys dancing on keyboards increases the probability that one will get lucky enough to type something that appears literate. Similarly, back testing a larger number of rules increases the chance that one will enjoy extraordinary luck. » (Page 294)\[1\].

\--------------------------------------------------------------------------------

**Vision Macro :**

L'enjeu est de démontrer que la performance exceptionnelle n'est pas une preuve de validité, mais une conséquence mécanique de l'intensité de la recherche. David Aronson utilise ici des règles "inutiles" (mérite = 0) comme groupe témoin. Si l'on trouve du profit là où l'on sait qu'il n'y a pas de talent, on prouve que ce profit est un artefact statistique généré par l'acte même de sélectionner le meilleur résultat parmi plusieurs tentatives\[1\]\[5\].

\--------------------------------------------------------------------------------

**Vision Micro :**

Le mécanisme de l'expérience se décompose en étapes statistiques rigoureuses :

**Configuration des ATR :** L'ordinateur simule 1 000 historiques de 24 mois. Sans minage (test d'une seule règle), la distribution est centrée sur zéro (Figure 6.27)\[5\]\[6\].

**Procédure de sélection :** Aronson fait varier la taille de l'univers (N) de 2 à 400 règles et sélectionne systématiquement celle qui a le rendement le plus élevé\[5\].

**Quantification du biais (pour 24 mois de données) :**

**N = 2 :** La meilleure règle affiche +8,5 % de profit (Biais = 8,5 points)\[5\]\[7\].

**N = 10 :** Le profit "chanceux" monte à +22 %\[7\]\[8\].

**N = 50 :** Le profit atteint +33 %\[4\]\[8\].

**N = 400 :** Le profit atteint **+48 %**\[3\]\[4\].

**Loi Mathématique :** La relation entre le nombre de règles (N) et le biais est résumée à la Figure 6.32. Le biais augmente proportionnellement à log10​(N), ce qui signifie que chaque nouvelle règle ajoutée à l'optimisation augmente la probabilité de sélectionner un "coup de chance" encore plus extrême\[2\]\[3\].

\--------------------------------------------------------------------------------

**Résumé Simplifié :**

Imaginez que vous lanciez une pièce de monnaie. Si vous demandez à une personne de lancer 24 fois la pièce, elle obtiendra environ 12 "piles" (zéro profit). Mais si vous demandez à 400 personnes de le faire et que vous ne gardez que celle qui a fait le plus de "piles", cette personne affichera un score incroyable (par exemple 20 piles sur 24). Aronson prouve qu'en trading, si vous testez 400 stratégies avec votre ordinateur, la "meilleure" affichera +48 % de gain même si elle ne vaut rien en réalité\[1\].

\--------------------------------------------------------------------------------

**Actions Concrètes :**

**Tenir un registre des échecs :** Notez scrupuleusement le nombre total de variantes testées (N), car c'est ce chiffre qui détermine la taille de votre "mensonge" statistique\[1\]\[3\].

**Ajuster le seuil de rejet :** Si vous testez des centaines de règles, vous devez exiger un profit beaucoup plus élevé que la normale pour rejeter l'hypothèse nulle (le hasard)\[9\]\[10\].

**Se méfier des optimisations sur 2 ans :** L'expérience montre que sur une période courte (24 mois), le biais est massif et peut transformer n'importe quel signal aléatoire en "stratégie miracle"\[3\]\[6\].

\--------------------------------------------------------------------------------

**À retenir absolument :**

Le biais augmente avec le **nombre de règles testées** (N)\[1\].

Sur 24 mois, 400 tests génèrent **+48 % de profit imaginaire**\[3\]\[4\].

La croissance du biais suit une loi **log-linéaire**\[3\].

Le "meilleur" d'un backtest est statistiquement **le plus chanceux**, pas le plus talentueux\[5\].

Ne jamais croire un profit record sans connaître le nombre de tentatives nécessaires pour le trouver\[2\].

J'ai terminé l'analyse de l'expérience sur le nombre de règles testées selon le protocole EBTA.
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
[10] undefined
