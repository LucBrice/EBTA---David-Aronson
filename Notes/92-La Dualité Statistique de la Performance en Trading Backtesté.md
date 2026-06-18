---
exported: 2026-06-12T08:57:19.249Z
source: NotebookLM
type: note
title: "92-La Dualité Statistique de la Performance en Trading Backtesté"
---

# 92-La Dualité Statistique de la Performance en Trading Backtesté

导出时间: 12/06/2026 10:57:19

---

### **LEGITIMATE USES OF OBSERVED PERFORMANCE**

Voici l’analyse technique des utilisations légitimes de la performance observée (le profit de backtest), une section cruciale où David Aronson distingue le rôle du profit selon que l'on teste une règle unique ou que l'on pratique le minage de données\[1\].

**(AJOUT) Idées clés :**

**Dualité de rôle :** La performance observée sert soit d'estimateur du futur, soit de critère de sélection, mais rarement les deux simultanément\[1\].

**Estimation sans biais :** Pour une règle unique testée isolément, le profit passé est la meilleure approximation (sans biais) du profit futur\[2\].

**Boussole de sélection :** Dans le minage de données, le profit sert de filtre pour identifier quelle règle est statistiquement la plus prometteuse\[3\].

**Validité de la sélection :** White a prouvé mathématiquement que la règle affichant le meilleur profit passé est effectivement celle qui a la plus forte probabilité d'être la meilleure à l'avenir\[3\]\[4\].

**Référence :**

_Legitimate Uses of Observed Performance_, Chapitre 6, pages 270–271\[1\].

**Citation Directe :**

« In single-rule back testing, observed performance serves as an estimator of future performance. In data mining, observed performance serves as a selection criterion. » (Page 270)\[1\].

\--------------------------------------------------------------------------------

**Vision Macro :**

L'enjeu est d'attribuer la bonne fonction statistique au résultat d'un backtest pour éviter de fausses conclusions. David Aronson explique que le profit observé n'est pas une vérité absolue, mais une mesure dont la valeur informative change radicalement selon le processus de recherche utilisé\[1\]\[5\]. Pour une règle isolée issue d'une théorie, le profit est une mesure d'espérance ; pour un ensemble de règles minées, il n'est qu'un outil de tri. La confusion entre ces deux fonctions est, selon l'auteur, la cause majeure des échecs lors du passage au trading réel\[3\]\[6\].

\--------------------------------------------------------------------------------

**Vision Micro :**

**Le cas de la règle unique (Estimateur) :**

**Mécanisme :** En se basant sur les principes de l'échantillonnage, Aronson rappelle qu'une moyenne d'échantillon (le profit du backtest) est un « unbiased estimate » (estimateur sans biais) de la moyenne de la population (le futur)\[2\].

**Propriété :** La règle a autant de chances de faire mieux que de faire moins bien que son résultat historique. Le profit passé est donc son futur le plus probable (Figure 6.4)\[2\].

**Le cas du minage de données (Critère de sélection) :**

**Mécanisme :** Lorsque l'on compare des milliers de règles, le profit perd sa capacité à être un estimateur fiable du montant des gains futurs à cause du biais de minage\[3\]\[7\].

**Utilité résiduelle :** Sa fonction légitime devient celle de **critère de sélection**. White (2000) a démontré que, même si le profit est gonflé par la chance, la règle qui arrive première au backtest est bel et bien celle qui a la plus forte probabilité d'avoir le meilleur mérite réel\[3\]\[4\].

**Paradoxe :** Le minage de données est donc une méthode efficace pour trouver la _meilleure_ règle, mais une méthode trompeuse pour savoir _combien_ elle va rapporter\[8\]\[9\].

\--------------------------------------------------------------------------------

**(AJOUT) Résumé Simplifié :**

Si tu ne testes qu'une seule stratégie bien précise, ton profit passé est une prévision honnête de ce que tu gagneras demain\[2\]. Mais si tu en testes 1 000 pour ne garder que la "championne", le score de cette championne est un mensonge car il est dopé par la chance\[7\]. Ce score te sert uniquement à savoir _quelle_ règle choisir (la boussole), mais il ne te dit pas _combien_ tu vas gagner (le montant), car la chance ne se répétera pas\[3\]\[10\].

\--------------------------------------------------------------------------------

**Actions Concrètes :**

**Vérifier l'origine de la règle :** Si vous avez modifié ne serait-ce qu'un paramètre après avoir vu le résultat, vous n'êtes plus dans l'estimation, mais dans la sélection\[3\].

**Utiliser le profit pour classer :** En situation d'optimisation, utilisez les résultats pour définir l'ordre de priorité de vos stratégies, et non pour vos plans financiers\[1\]\[3\].

**Appliquer White's Reality Check :** C'est le seul moyen de valider que la règle sélectionnée possède un mérite réel au-delà de sa fonction de sélection\[11\].

**Réduire les attentes de ROI :** Prévoyez systématiquement une chute de performance (shrinkage) par rapport au backtest dès qu'une sélection a eu lieu\[12\].

\--------------------------------------------------------------------------------

**(AJOUT) À retenir absolument :**

Règle unique = Le profit est un **estimateur honnête**\[2\].

Minage de données = Le profit est un **outil de tri**\[1\].

La meilleure règle passée est **statistiquement** la plus susceptible d'être la meilleure future\[3\]\[4\].

Le succès du "champion" de backtest est **systématiquement gonflé** par la chance\[7\]\[9\].

Ignorer cette distinction mène à une **déception massive** hors-échantillon\[6\]\[13\].

J'ai terminé l'analyse des utilisations légitimes de la performance observée selon le protocole EBTA.
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
