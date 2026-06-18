---
exported: 2026-06-12T08:59:07.366Z
source: NotebookLM
type: note
title: "3- L'Art du Détrendage et de l'Évaluation des Règles de Trading"
---

# 3- L'Art du Détrendage et de l'Évaluation des Règles de Trading

导出时间: 12/06/2026 10:59:07

---

### **THE USE OF BENCHMARKS IN RULE EVALUATION**

**The Conjoint Effect of Position Bias and Market Trend on Back-Test Performance**

**Référence :** THE CONJOINT EFFECT OF POSITION BIAS AND MARKET TREND ON BACK-TEST PERFORMANCE (Pages 23–27).\[1\]\[2\]

**Citation Directe :** « The performance of a rule can be profoundly affected by factors that have nothing to do with its predictive power. » (Page 23).\[1\]

**Vision Macro :**L'enjeu fondamental est d'éviter l'illusion de la performance. Un trader peut croire qu'une règle de trading est efficace alors que son profit n'est que le résultat mécanique d'une exposition fortuite à la tendance dominante du marché. Pour que l'Analyse Technique soit fondée sur des preuves (EBTA), il est impératif de distinguer la puissance prédictive réelle de la simple "chance de position".\[1\]

**Vision Micro :**La performance d'un backtest est la combinaison de deux facteurs indépendants :

**Le biais de position (****Position Bias****) :** C'est le temps relatif qu'une règle passe en position longue (+1) par rapport au temps en position courte (-1). Si les conditions d'entrée à l'achat sont plus laxistes que celles à la vente, la règle aura un biais acheteur.\[2\]

**La tendance nette du marché (****Market's Net Trend****) :** C'est le changement quotidien moyen du prix pendant la période de test.\[2\]Si un marché est haussier, toute règle ayant un biais acheteur (même une règle de pur hasard comme un lancer de pièce biaisé) affichera un profit positif. Ce profit est trompeur car il ne reflète aucune intelligence du marché.\[6\]

**Actions Concrètes :**

**Calculer le rendement attendu du hasard :** Utiliser la formule ER\=\[p(L)×ADC\]−\[p(S)×ADC\] (où p(L) est la probabilité d'être long et ADC le changement quotidien moyen) pour connaître ce qu'une règle sans talent gagnerait par simple exposition.\[7\]\[9\]

**Ajuster la performance observée :** Soustraire ce rendement théorique du profit réel du backtest pour isoler la composante prédictive.\[10\]

**Analyser la structure de la règle :** Vérifier si les conditions d'achat et de vente sont d'une sévérité équivalente pour éviter les biais de position involontaires.\[5\]\[11\]

\--------------------------------------------------------------------------------

**A Simpler Solution to Benchmarking: Detrending the Market Data**

**Référence :** A SIMPLER SOLUTION TO BENCHMARKING: DETRENDING THE MARKET DATA (Pages 27–28).\[12\]

**Citation Directe :** « Detrending is a simple transformation, which results in a new market data series whose average daily price change is equal to zero. » (Page 28).\[13\]

**Vision Macro :**L'enjeu est la simplification et la standardisation de la rigueur statistique. Calculer un benchmark spécifique pour chaque règle testée (surtout lors de minage de données sur des milliers de règles) est fastidieux. En "détrendant" les données de prix, le trader ramène l'espérance de profit du hasard à zéro pour toutes les règles, rendant la comparaison immédiate et objective.\[12\]

**Vision Micro :**Le détrendage neutralise l'effet du biais de position. Si le changement quotidien moyen du marché est de zéro, alors \[p(long)×0\]−\[p(short)×0\] sera toujours égal à zéro, peu importe si la règle est long 90% ou 10% du temps. Ainsi, tout profit persistant sur des données détrendées est la preuve directe d'un couplage "intelligent" entre la position et les mouvements de prix, et non d'une simple exposition.\[13\]

**Actions Concrètes :**

**Transformer les séries de données :** Soustraire le changement quotidien moyen (ADC) de chaque changement de prix quotidien de la période de test.\[14\]

**Séparer signaux et rendements :** Utiliser les données réelles (avec tendance) pour générer les signaux de trading, mais utiliser exclusivement les données détrendées pour calculer les profits et pertes (P&L) du backtest.\[12\]

**Établir le zéro comme référence :** Considérer que toute règle dont le profit sur données détrendées n'est pas significativement supérieur à zéro n'a aucun pouvoir prédictif.\[13\]

\--------------------------------------------------------------------------------

**Using Logs of Daily Price Ratio Instead of Percentages**

**Référence :** USING LOGS OF DAILY PRICE RATIO INSTEAD OF PERCENTAGES (Page 29).\[16\]

**Citation Directe :** « These problems can be eliminated by computing daily returns as the logs of daily price ratios. » (Page 29).\[16\]

**Vision Macro :**L'enjeu est la précision mathématique et la validité des inférences statistiques. Les rendements en pourcentage sont asymétriques et difficiles à manipuler pour des opérations comme le détrendage ou le cumul de performance sur de longues périodes. L'utilisation des logarithmes est le standard scientifique pour traiter les séries temporelles financières.\[16\]

**Vision Micro :**Le rendement logarithmique est défini par : Log(prix du jour/prix de la veille).\[16\]Contrairement aux pourcentages, les rendements log sont additifs. Pour détrendre une série log, il suffit de calculer la moyenne des rendements log de la période et de la soustraire de chaque rendement quotidien. Cette méthode élimine proprement toute croissance géométrique ou tendance de fond dans les données, permettant une analyse statistique robuste.\[16\]

**Actions Concrètes :**

**Convertir les bases de données :** Travailler sur les ratios logarithmiques plutôt que sur les variations de prix brutes ou les pourcentages simples pour tous les calculs de performance.\[16\]

**Appliquer le détrendage log :** Calculer le rendement log moyen sur toute la période du backtest et le déduire de chaque observation pour obtenir une tendance nulle.\[16\]

**Standardiser les P&L :** Utiliser les rendements log pour calculer les ratios de Sharpe ou d'autres statistiques de performance afin de garantir la symétrie des gains et des pertes.\[17\]
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[7] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[9] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[17] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
