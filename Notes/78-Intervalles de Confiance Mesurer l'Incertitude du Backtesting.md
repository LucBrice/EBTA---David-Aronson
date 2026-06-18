---
exported: 2026-06-12T08:57:34.482Z
source: NotebookLM
type: note
title: "78-Intervalles de Confiance : Mesurer l'Incertitude du Backtesting"
---

# 78-Intervalles de Confiance : Mesurer l'Incertitude du Backtesting

导出时间: 12/06/2026 10:57:34

---

### **CH 5 - 6 : WHAT DO CONFIDENCE INTERVALS TELL US?**

Voici l’analyse technique de l’utilité et de la signification des intervalles de confiance, l’outil qui permet de quantifier l’incertitude entourant la performance future d'une règle de trading\[1\]\[2\].

**Idées clés :**

**Correction de l'estimation ponctuelle :** Une estimation ponctuelle est incomplète car elle ne véhicule aucune notion d'incertitude ; l'intervalle de confiance (IC) résout ce problème en intégrant l'erreur d'échantillonnage\[3\].

**Définition de la fourchette :** L'IC est une gamme de valeurs entourant l'estimation, définie par des bornes supérieure et inférieure\[4\].

**Probabilité de couverture :** Un IC à 90 % signifie que si l'on construisait un grand nombre d'intervalles basés sur des échantillons indépendants, environ 90 % d'entre eux contiendraient la valeur réelle du paramètre\[5\]\[6\].

**Compromis Confiance/Précision :** Augmenter le niveau de confiance (ex: passer de 90 % à 99 %) rend l'intervalle plus large, ce qui diminue la précision de l'estimation\[7\].

**Lien avec la p-value :** Les intervalles de confiance sont dérivés de la même distribution d'échantillonnage que celle utilisée pour les tests d'hypothèse\[8\].

**Référence :**

_What Do Confidence Intervals Tell Us?_ (Pages 245–247 ; Audiobook Transcription 153).

**Citation Directe :**

« A point estimate has limited value because it conveys no sense of the uncertainty in the estimate due to sampling error. The confidence interval solves this problem by combining the information of the point estimate with the information about the estimator’s sampling distribution. » (Page 245)\[3\].

**Vision Macro :**

L'enjeu est l'honnêteté statistique. David Aronson explique que prétendre qu'une règle rapportera "exactement 10 %" est une erreur méthodologique. L'intervalle de confiance force le trader à accepter que son résultat de backtest n'est qu'une photographie imparfaite d'un futur incertain\[3\]\[9\]. Il permet de définir un "cadre de réalisme" : si la borne basse de l'intervalle est proche de zéro ou négative, le trader sait que sa stratégie est fragile, même si son profit moyen paraît séduisant\[6\]\[10\].

**Vision Micro :**

Le mécanisme de l'intervalle de confiance repose sur la manipulation de la distribution d'échantillonnage :

**La Structure :** La valeur réelle du paramètre de population (μ) est égale à la moyenne d'échantillon (Xˉ) plus ou moins l'erreur d'échantillonnage\[8\]\[11\].

**Le Positionnement :** Contrairement au test d'hypothèse où la distribution est centrée sur zéro (l'hypothèse nulle), pour l'IC, la distribution est centrée sur la performance observée dans le backtest (ex: +7 %)\[12\]\[13\].

**Le calcul des bornes :** Pour un IC à 90 %, on identifie les valeurs de la distribution d'échantillonnage qui laissent 5 % de probabilité dans la queue gauche et 5 % dans la queue droite. Les valeurs restantes entre ces deux points constituent l'intervalle\[14\].

**Dépendance à la dispersion :** La largeur de l'intervalle dépend de la largeur de la distribution d'échantillonnage. Plus les rendements sont volatils ou plus l'échantillon est petit (N), plus l'IC sera large et donc incertain\[15\]\[16\].

**Résumé Simplifié :**

L'estimation ponctuelle vous donne un chiffre unique (ex: "15 % de gain"). L'intervalle de confiance est plus prudent : il vous dit "Je suis sûr à 95 % que ton gain sera compris entre 5 % et 25 %". Il vous montre la marge d'erreur de votre backtest\[1\]\[4\].

**Exemples du livre pour mieux comprendre :**

**La règle à 7 % :** Aronson donne l'exemple d'une règle ayant gagné 7 % en backtest. Un IC à 90 % pourrait indiquer que le rendement réel futur se situe entre 2 % et 12 %. Le trader est ainsi averti que le rendement pourrait être bien plus bas que les 7 % observés\[6\].

**L'erreur de l'IC :** La Figure 5.16 montre 10 intervalles de confiance à 90 %. Statistiquement, l'un de ces dix intervalles échoue à inclure la moyenne réelle (μ), illustrant que l'IC n'est pas une garantie absolue mais une probabilité de succès\[11\]\[17\].

**Actions Concrètes :**

**Ne jamais trader un chiffre seul :** Exigez systématiquement les bornes haute et basse de l'IC avant d'allouer du capital à une stratégie\[3\].

**Choisir son niveau de risque :** Utilisez un IC à 95 % ou 99 % si vous voulez minimiser le risque de mauvaise surprise, tout en acceptant que votre estimation sera très large\[7\].

**Surveiller la borne basse :** Si la borne inférieure de votre IC est négative, cela signifie qu'il y a une probabilité non négligeable que votre règle soit structurellement perdante malgré un backtest positif\[18\].

**Augmenter le nombre de trades :** Pour rétrécir l'IC (et donc gagner en précision), testez votre règle sur un historique de données plus long\[16\]\[19\].

**À retenir absolument :**

L'IC mesure l'**incertitude** liée à l'erreur d'échantillonnage\[3\].

**Confiance** \= **Précision** : un intervalle très "sûr" est souvent très large\[7\].

Un IC à 90 % laisse un **risque de 10 %** d'être totalement en dehors de la plaque\[5\].

Il centre la "cloche du hasard" sur votre **résultat réel**, pas sur zéro\[12\].

C'est l'outil indispensable pour la **gestion réaliste des attentes** de profit\[6\]\[9\].

J'ai terminé l'analyse de ce que nous disent les intervalles de confiance selon le protocole EBTA.
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
[16] undefined
[17] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[18] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[19] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
