---
exported: 2026-06-12T08:57:33.580Z
source: NotebookLM
type: note
title: "79-L'Architecture Statistique de l'Incertitude : De la Distribution à l'Intervalle"
---

# 79-L'Architecture Statistique de l'Incertitude : De la Distribution à l'Intervalle

导出时间: 12/06/2026 10:57:33

---

### **CH 5 - 6 : THE CONFIDENCE INTERVAL AND ITS CONNECTION TO THE SAMPLING DISTRIBUTION**

Voici l’analyse technique de la relation structurelle entre les intervalles de confiance et la distribution d’échantillonnage, le moteur mathématique qui permet de quantifier l’incertitude de la performance.\[1\]

**Idées clés :**

**Source commune :** Les intervalles de confiance sont dérivés de la même distribution d'échantillonnage que celle utilisée pour calculer les p-values.\[1\]

**Moyenne vs Erreur :** La moyenne d'échantillon (Xˉ) est égale au paramètre de population (μ) plus ou moins l'erreur d'échantillonnage.\[2\]

**Logique inverse :** Par inversion algébrique, le paramètre de population est égal à la moyenne observée plus ou moins l'erreur d'échantillonnage.\[2\]

**Déplacement de la distribution :** Pour un intervalle de confiance, la distribution d'échantillonnage est simplement décalée pour être centrée sur la moyenne observée au lieu de zéro.\[3\]

**Référence :**

_The Confidence Interval and Its Connection to the Sampling Distribution_, pages 247 à 248.\[1\]

**Citation Directe :**

« Confidence intervals are derived from the same sampling distribution that is used to compute the p-values for a hypothesis test. » (Page 247).\[1\]

**Vision Macro :**

L'enjeu est la cohérence interne de l'inférence statistique. David Aronson explique que le rejet de la chance (test d'hypothèse) et la mesure de la performance probable (estimation par intervalle) ne sont que les deux faces d'une même pièce.\[4\]\[5\] Le trader utilise l'erreur d'échantillonnage non plus seulement comme un obstacle pour prouver son talent, mais comme un ruban à mesurer pour définir les limites de ce qu'il peut espérer gagner dans le futur réel.\[1\]\[6\]

**Vision Micro :**

Le lien technique repose sur la manipulation de la distribution d'échantillonnage selon deux configurations :\[3\]

**Configuration Test d'Hypothèse (Figure 5.21) :** La distribution (la cloche) est centrée sur la valeur de l'Hypothèse Nulle (généralement 0 %). On regarde si le résultat observé tombe dans les zones rares de la queue droite.\[3\]\[7\]

**Configuration Intervalle de Confiance (Figure 5.21) :** On prend la même distribution, mais on la "glisse" le long de l'axe horizontal pour que son sommet (la moyenne la plus probable) se trouve exactement au-dessus du rendement obtenu en backtest (ex : +7 %).\[3\]

**Calcul des limites :** À partir de cette position centrée sur le profit réel, les bornes de l'intervalle (ex : 90 %) sont fixées par la largeur de cette même distribution. Plus l'erreur d'échantillonnage est grande (due à une forte volatilité ou un petit échantillon N), plus la cloche est large et plus les bornes de l'intervalle s'écartent.\[2\]

**Résumé Simplifié :**

Le test de p-value et l'intervalle de confiance utilisent le même outil : la "cloche de la chance". Pour savoir si vous avez du talent, on met la cloche sur zéro.\[3\] Pour savoir combien vous allez gagner, on déplace la cloche pour la mettre sur votre profit, et les bords de la cloche vous indiquent vos marges d'erreur haute et basse.\[8\]

**Exemples du livre pour mieux comprendre :**

**La règle à 7 % :** Si une règle gagne 7 % en backtest, on centre la distribution d'échantillonnage sur 7 %.\[3\]\[11\] Si la largeur de la distribution (l'erreur) est de 5 %, alors l'intervalle de confiance sera de 2 % à 12 % (7 - 5 et 7 + 5).\[11\]

**La transposition (Figure 5.19) :** Aronson montre par une formule simple que si la mesure connue (le backtest) est la vérité plus une erreur, alors la vérité est la mesure connue moins cette même erreur.\[2\]

**Actions Concrètes :**

**Réutiliser la distribution Bootstrap :** Ne générez pas deux distributions différentes ; utilisez celle créée pour votre test de p-value en la recentrant sur votre profit moyen pour obtenir votre IC.\[12\]

**Analyser le chevauchement avec zéro :** Si vous déplacez la cloche sur votre profit et qu'une grande partie de la cloche couvre encore des valeurs négatives, votre stratégie est statistiquement instable.\[13\]\[14\]

**À retenir absolument :**

L'intervalle de confiance est une **transposition géographique** du test d'hypothèse.\[3\]

Il repose entièrement sur la **largeur de la distribution d'échantillonnage**.\[2\]

Il transforme l'incertitude du hasard en une **fourchette de profit exploitable**.\[15\]\[16\]

Centrer sur le profit permet de voir la **distance par rapport à l'échec (zéro)**.\[7\]

La précision de l'intervalle dépend mécaniquement de la **taille de l'échantillon (**N**)**.\[10\]\[17\]

J'ai terminé l'analyse de la connexion entre l'intervalle de confiance et la distribution d'échantillonnage selon le protocole EBTA.
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
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[15] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[16] undefined
[17] undefined
