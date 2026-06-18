---
exported: 2026-06-12T08:56:52.232Z
source: NotebookLM
type: note
title: "117-L'Illusion Statistique entre Performance Backtestée et Réalité Future"
---

# 117-L'Illusion Statistique entre Performance Backtestée et Réalité Future

导出时间: 12/06/2026 10:56:52

---

### **CH 6 : OBSERVED PERFORMANCE AND EXPECTED PERFORMANCE VERSUS NUMBER OF OBSERVATIONS IN A UNIVERSE OF VARIABLE MERIT**

Cette section analyse l'écart entre la performance qu'un trader observe dans son backtest et la performance réelle qu'il peut attendre dans le futur, en fonction du volume de données disponibles\[1\].

**Idées clés :**

**Structure des courbes :** La performance observée (backtest) se situe systématiquement au-dessus de la performance attendue (réelle)\[1\]\[2\].

**Le biais comme écart :** La distance verticale entre ces deux mesures représente mathématiquement le biais de minage de données\[3\].

**Force de la convergence :** À mesure que le nombre d'observations augmente, les deux performances convergent, réduisant ainsi l'ampleur du mensonge statistique\[2\].

**Taille de l'univers :** Un univers de recherche plus vaste (ex: 500 règles contre 10) augmente l'opportunité pour la chance de creuser cet écart\[2\].

**Référence :**

_Observed Performance and Expected Performance versus Number of Observations in a Universe of Variable Merit_, Chapitre 6, pages 316 à 317\[1\]\[4\].

**Citation Directe :**

« The curve of observed performance will always lie above the curve of expected performance because a best-of-selection criterion will always induce some positive bias when luck plays a role in observed performance. » (Page 318)\[2\].

**Vision Macro :**

L'enjeu est l'intégrité de l'estimation du profit futur pour le trader\[5\]. David Aronson explique que le processus de sélection de la "meilleure" règle n'est pas un acte de mesure neutre, mais un mécanisme qui favorise structurellement l'optimisme\[2\]\[6\]. Même avec une quantité massive de données, le profit affiché par le "champion" d'une optimisation restera toujours un indicateur biaisé à la hausse par rapport à la réalité future\[2\].

**Vision Micro :**

Le mécanisme de distorsion entre l'observation et l'attente se décompose ainsi :

**L'asymétrie initiale (Figures 6.53 & 6.54) :** Sur un échantillon très court (à gauche des graphiques), le hasard domine totalement le mérite réel\[3\]. La performance observée est alors démesurément plus élevée que l'espérance de gain réelle\[3\].

**L'action de la Loi des Grands Nombres :** À mesure que l'on avance vers 1 000 mois d'observations, la distribution de performance se resserre\[7\]. La part de chance "diluée" permet à la performance observée de se rapprocher de la vérité du pouvoir prédictif\[2\].

**L'impact de l'exploration :** En comparant les Figures 6.53 (10 règles) et 6.54 (500 règles), on constate que le biais est plus prononcé dans le second cas\[2\]. Plus le chercheur ratisse large, plus il a de chances de tomber sur une règle dont la performance est dopée par une coïncidence heureuse avec les données historiques\[2\].

**Résumé Simplifié :**

Imaginez que vous cherchiez la meilleure équipe de football sur un seul match (échantillon court)\[8\]. Le gagnant aura un score magnifique, mais il ne reflète pas son niveau réel car il a pu gagner par chance\[9\]. Si vous les regardez jouer 1 000 matchs (échantillon large), le score du champion sera beaucoup plus proche de son talent réel, même s'il reste légèrement gonflé par le fait que vous avez spécifiquement choisi celui qui a fini premier\[2\].

**Actions Concrètes :**

**Appliquer une décote systématique :** Ne basez jamais vos attentes de profit sur le chiffre brut de votre backtest optimisé, car il contient toujours une part de chance non récurrente\[2\]\[10\].

**Privilégier la profondeur des données :** Avant d'augmenter la complexité de votre univers de recherche, assurez-vous d'augmenter le nombre d'observations pour forcer la convergence des courbes\[2\]\[11\].

**Évaluer l'écart relatif :** Si le profit observé est massivement supérieur à la moyenne de l'univers, soyez d'autant plus sceptique quant à sa persistance hors-échantillon\[3\].

**À retenir absolument :**

**Observed > Expected** : Le backtest est toujours plus beau que le futur\[2\].

Le **biais de minage** est l'écart vertical entre ces deux valeurs\[3\].

Le **temps (N)** est le seul facteur qui fait converger le mensonge vers la vérité\[2\].

Tester **plus de règles** augmente mécaniquement cet écart\[2\].

La performance réelle est une **chute inévitable** depuis une attente irréaliste\[12\].

J'ai terminé l'analyse de la relation entre performance observée et attendue selon le protocole EBTA.
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
