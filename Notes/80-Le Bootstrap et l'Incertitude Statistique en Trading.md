---
exported: 2026-06-12T08:57:32.584Z
source: NotebookLM
type: note
title: "80 - Le Bootstrap et l'Incertitude Statistique en Trading"
---

# 80 - Le Bootstrap et l'Incertitude Statistique en Trading

导出时间: 12/06/2026 10:57:32

---

### **CH 5 - 6 : GENERATING CONFIDENCE INTERVALS WITH THE BOOTSTRAP**

Voici l’analyse technique de la génération des intervalles de confiance (IC) par la méthode Bootstrap, une alternative informatique puissante aux formules classiques pour quantifier l'incertitude d'une stratégie de trading\[1\]\[2\].

**Idées clés :**

**Méthode des centiles :** La procédure privilégiée par Aronson est la "méthode des centiles bootstrap", réputée pour sa simplicité et son efficacité\[2\]\[3\].

**Inapplicabilité de Monte Carlo :** Contrairement au Bootstrap, la méthode de permutation de Monte Carlo ne peut pas être utilisée pour générer des IC car elle ne teste pas de paramètre de population comme le rendement moyen\[2\]\[4\].

**Élagage statistique :** L'IC est formé en triant des milliers de moyennes simulées et en retirant un pourcentage déterminé de valeurs extrêmes aux deux extrémités\[3\]\[5\].

**Convergence :** La validité de l'intervalle repose sur le "Bootstrap Theorem", assurant que la distribution simulée converge vers la vérité à mesure que l'échantillon grandit\[6\]\[7\].

**Référence :**

_Generating Confidence Intervals with the Bootstrap_, pages 248 à 250\[2\]\[4\].

**Citation Directe :**

« The bootstrap percentile method, is popular, easy to use, and generally gives good results. » (Page 248)\[2\].

**Vision Macro :**

L'enjeu est de s'affranchir de l'hypothèse (souvent fausse en trading) que les rendements suivent une loi normale (courbe en cloche parfaite)\[8\]\[9\]. En utilisant le Bootstrap pour créer des intervalles de confiance, le trader laisse les données "parler d'elles-mêmes"\[10\]\[11\]. Cela permet d'obtenir une fourchette de performance future beaucoup plus réaliste, reflétant les particularités (pics, queues épaisses) du comportement historique de la règle\[2\]\[12\].

**Vision Micro :**

La procédure technique (méthode des centiles) suit ces étapes rigoureuses :

**Rééchantillonnage :** On effectue 5 000 tirages avec remise à partir de l'échantillon original (contrairement au test de p-value, on ne procède **pas** au zéro-centrage ici, car on veut centrer la distribution sur le profit réel)\[3\]\[13\].

**Calcul des moyennes :** On calcule la moyenne pour chacune des 5 000 simulations\[3\].

**Tri par rang :** L'ordinateur classe ces 5 000 valeurs de la plus élevée à la plus basse\[3\].

**Détermination du seuil d'élagage (**X**) :** On utilise la formule :X\=2100−Niveau de Confiance Deˊsireˊ​

**Élimination des extrêmes :**

_Exemple pour un IC à 90 % :_ On retire les 5 % les plus hauts (250 valeurs) et les 5 % les plus bas (250 valeurs)\[5\].

**Fixation des bornes :** La valeur la plus haute restante devient la borne supérieure, et la plus basse restante devient la borne inférieure\[5\].

**Résumé Simplifié :**

Pour trouver la marge d'erreur de ton profit, on crée 5 000 versions imaginaires de ton passé en mélangeant tes jours de trading\[3\]\[11\]. On range les 5 000 résultats du meilleur au pire. Si tu veux être sûr à 90 %, on jette les 250 meilleurs et les 250 pires\[5\]. Ce qui reste au milieu est ton intervalle de confiance : c'est là où ton talent se situe probablement\[2\]\[14\].

**Exemples du livre pour mieux comprendre :**

**L'IC à 90 % :** Sur 5 000 moyennes triées, Aronson explique qu'il faut supprimer les 250 valeurs de chaque côté. Si la valeur la plus haute après élagage est 12 % et la plus basse est 2 %, alors l'IC est \[2 % ; 12 %\]\[5\]\[14\].

**L'IC à 99 % :** Pour être plus "certain", on n'élimine que les 25 valeurs les plus extrêmes (0,5 %) de chaque côté. L'intervalle résultant est mécaniquement beaucoup plus large, perdant en précision ce qu'il gagne en confiance\[5\]\[15\].

**Actions Concrètes :**

**Utilisez 5 000 itérations :** C'est le nombre nécessaire pour que les bornes de l'intervalle soient stables d'un calcul à l'autre\[3\]\[16\].

**Ne cherchez pas d'IC avec Monte Carlo :** Si votre logiciel propose un intervalle de confiance via une permutation de Monte Carlo, c'est une erreur conceptuelle selon EBTA\[4\].

**Appliquez le tri par rang :** Assurez-vous que votre algorithme classe bien l'intégralité des moyennes simulées avant d'appliquer les coupures de centiles\[3\].

**Vérifiez la taille** N **:** Chaque simulation bootstrap doit comporter exactement le même nombre de jours que votre backtest initial\[17\]\[18\].

**À retenir absolument :**

L'IC Bootstrap utilise la **méthode des centiles**\[2\]\[3\].

Il nécessite **5 000 simulations** pour être statistiquement fiable\[3\].

Il ne nécessite **pas de zéro-centrage** (contrairement à la p-value)\[13\].

**Plus de confiance = Moins de précision** (intervalle plus large)\[15\].

C'est l'outil qui définit la **marge d'erreur** de votre espérance de gain\[1\]\[19\].

J'ai terminé l'analyse de la génération des intervalles de confiance avec le Bootstrap selon le protocole EBTA.
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
[18] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[19] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
