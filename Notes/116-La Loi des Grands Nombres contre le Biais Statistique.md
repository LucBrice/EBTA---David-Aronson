---
exported: 2026-06-12T08:56:53.291Z
source: NotebookLM
type: note
title: "116-La Loi des Grands Nombres contre le Biais Statistique"
---

# 116-La Loi des Grands Nombres contre le Biais Statistique

导出时间: 12/06/2026 10:56:53

---

### **CH 6 : DATA-MINING BIAS AS A FUNCTION OF NUMBER OF OBSERVATIONS: IN A UNIVERSE OF VARIABLE MERIT**

Cette section explore la relation mathématique entre le volume de données historiques utilisées (le nombre d’observations) et l’intensité du biais de minage de données dans un contexte où les règles testées ont des talents réels différents.

**Idées clés :**

**L’antidote suprême :** L’augmentation du nombre d’observations est le moyen le plus efficace pour réduire le biais de minage de données\[1\]\[2\].

**Heed the Law of Large Numbers :** La Loi des Grands Nombres est le principe fondamental qui permet à la performance observée de converger vers la performance réelle\[3\]\[4\].

**Déclin exponentiel du biais :** L’ampleur du mensonge statistique (le biais) chute de façon spectaculaire à mesure que l’on passe d’un échantillon très court à un échantillon de taille modérée (environ 200 mois)\[5\]\[6\].

**Compensation du risque :** Un échantillon très large (ex: 1 000 mois) permet de tester un grand nombre de règles (ex: 100) tout en maintenant un biais résiduel très faible\[6\]\[7\].

**Référence :**

_Data-Mining Bias as a Function of Number of Observations: In a Universe of Variable Merit_, Chapitre 6, pages 314 à 316.

**Citation Directe :**

« The message to the data miner is clear: Heed the Law of Large Numbers. » (Page 315)\[3\].

\--------------------------------------------------------------------------------

**Vision Macro :**

L'enjeu est la lutte contre la tyrannie du "bruit" temporel. David Aronson explique que le hasard est une force qui domine les échantillons restreints. En trading, un profit réalisé sur une courte période n'a quasiment aucune valeur prédictive car il est impossible de savoir s'il provient du talent ou d'une simple coïncidence avec le marché\[8\]\[9\]. La "vérité" d'une stratégie ne peut émerger que si elle est soumise à une multitude d'épreuves sur une longue durée. Le temps est donc le seul filtre capable de dissoudre la chance pour laisser apparaître le mérite réel\[4\]\[10\].

\--------------------------------------------------------------------------------

**Vision Micro :**

Le mécanisme de réduction du biais par l'augmentation des observations repose sur la dynamique de la distribution d'échantillonnage :

**Resserrement de la distribution (Figure 6.34) :** Un petit échantillon produit une distribution "large". Cela laisse beaucoup d'espace pour que le hasard génère des profits extrêmes en backtest. Un grand échantillon "écrase" cette distribution autour de la moyenne réelle, empêchant les anomalies chanceuses de survivre\[1\]\[11\].

**Analyse des courbes (Figures 6.49 à 6.51) :** Aronson présente trois graphiques montrant le biais en fonction du nombre de mois (de 1 à 1 024)\[3\] :

**Pour 2 règles :** Le biais est déjà faible et s'annule presque avec 200 observations\[5\].

**Pour 100 règles :** Le biais initial est colossal sur 1 mois, mais il subit une chute brutale et se stabilise à un niveau bas une fois passé le cap des 400 à 600 observations\[6\].

**L'effet de convergence (Figure 6.52) :** En superposant les courbes, on s'aperçoit que si l'échantillon est suffisamment grand (proche de 1 000 mois), la différence de biais entre tester 2 règles et en tester 100 devient négligeable\[6\]\[12\]. La masse de données "noie" littéralement le risque lié au nombre de tests effectués.

\--------------------------------------------------------------------------------

**Résumé Simplifié :**

Imagine que tu doives recruter un archer. Si tu ne le regardes tirer qu'une seule flèche (échantillon court), n'importe quel amateur peut toucher le centre par chance. Si tu testes 100 amateurs, l'un d'eux sera forcément "le champion" par pur hasard. Mais si tu les forces à tirer 1 000 flèches chacun (échantillon large), la chance finit par s'épuiser. Seul le vrai professionnel gardera un bon score. En trading, plus tu as d'histoire, moins tu as de chances de recruter un imposteur chanceux\[1\]\[13\].

\--------------------------------------------------------------------------------

**Actions Concrètes :**

**Bannir les backtests courts :** Ne considérez jamais une statistique de performance (Rendement, Sharpe) calculée sur moins de quelques centaines de jours ou mois de données\[12\].

**Priorité à l'historique :** Avant d'ajouter des règles complexes à votre recherche, cherchez à obtenir l'historique de prix le plus profond possible\[1\].

**Ajuster l'ambition au volume de données :** Si vous n'avez que 2 ans de données, limitez-vous à tester 1 ou 2 idées. Si vous avez 30 ans de données, vous pouvez vous permettre de miner des centaines de règles sans exploser votre biais\[7\]\[12\].

\--------------------------------------------------------------------------------

**À retenir absolument :**

Le nombre d'observations est le **facteur n°1** de contrôle du biais\[1\].

La Loi des Grands Nombres est le **seul juge de paix** du trader EBTA\[3\].

Le biais chute **massivement** après 200 observations\[5\].

Un historique long permet une **recherche plus intensive** sans perte de fiabilité\[7\].

La performance sur échantillon court est une **hallucination statistique**\[8\].

J'ai terminé l'analyse de la section sur le biais de minage en fonction du nombre d'observations selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] undefined
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[7] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[9] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[10] undefined
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
