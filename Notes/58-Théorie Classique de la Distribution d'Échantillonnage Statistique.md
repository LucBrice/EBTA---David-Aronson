---
exported: 2026-06-12T08:57:59.424Z
source: NotebookLM
type: note
title: "58-Théorie Classique de la Distribution d'Échantillonnage Statistique"
---

# 58-Théorie Classique de la Distribution d'Échantillonnage Statistique

导出时间: 12/06/2026 10:57:59

---

### **CH 4 - 24 : DERIVING THE SAMPLING DISTRIBUTION - THE CLASSICAL APPROACH**

Voici l'analyse de l'approche classique (analytique) pour dériver la distribution d'échantillonnage, méthode historique développée par Sir Ronald Fisher et Jerzy Neyman\[1\]\[2\].

**(AJOUT) Idées clés :**

**Estimation par le calcul :** L'approche classique utilise la théorie des probabilités et le calcul intégral pour estimer la variabilité à partir d'un seul échantillon\[1\]\[2\].

**Fiabilité de la moyenne :** La moyenne d'un grand échantillon est l'un des meilleurs estimateurs de la "vérité" de la population (Loi des Grands Nombres)\[3\].

**Réduction de l'erreur par la taille :** Plus l'échantillon est grand, plus l'incertitude (la dispersion) diminue de manière prévisible\[5\].

**Convergence vers la Normale :** Quelle que soit la forme des données d'origine, la distribution des moyennes finit par ressembler à une cloche (Théorème Central Limite)\[12\].

**Référence :**

_Deriving the Sampling Distribution: The Classical Approach_, pages 208 à 215\[1\].

**Citation Directe :**

« It utilizes probability theory and integral calculus to derive the sampling distribution on the basis of a single observed sample. It provides estimates of the sampling distribution's dispersion, its mean, and its basic shape (normal). » (Page 208)\[1\].

**Vision Macro :**

L'enjeu est de transformer un backtest unique en un instrument de mesure fiable. Aronson explique que l'approche classique permet de "deviner" mathématiquement la forme de l'infini (la distribution d'échantillonnage) sans avoir à simuler des milliers de mondes\[1\]. C'est le cadre théorique qui permet aux traders de savoir si leur profit passé est une base solide pour parier sur le futur ou s'il n'est qu'un mirage statistique\[18\]\[19\].

**Vision Micro :**

**La Moyenne comme Pivot :** EBTA se concentre sur la moyenne car elle est un estimateur "sans biais"\[3\]. La moyenne de l'échantillon converge vers la moyenne de la population à mesure que N augmente\[3\].

**La Loi de la Racine Carrée :** La dispersion (largeur) de la distribution d'échantillonnage est inversement proportionnelle à la racine carrée de la taille de l'échantillon (n![](data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400em" height="1.08em" viewBox="0 0 400000 1080" preserveAspectRatio="xMinYMin slice"><path d="M95,702
c-2.7,0,-7.17,-2.7,-13.5,-8c-5.8,-5.3,-9.5,-10,-9.5,-14
c0,-2,0.3,-3.3,1,-4c1.3,-2.7,23.83,-20.7,67.5,-54
c44.2,-33.3,65.8,-50.3,66.5,-51c1.3,-1.3,3,-2,5,-2c4.7,0,8.7,3.3,12,10
s173,378,173,378c0.7,0,35.3,-71,104,-213c68.7,-142,137.5,-285,206.5,-429
c69,-144,104.5,-217.7,106.5,-221
l0 -0
c5.3,-9.3,12,-14,20,-14
H400000v40H845.2724
s-225.272,467,-225.272,467s-235,486,-235,486c-2.7,4.7,-9,7,-19,7
c-6,0,-10,-1,-12,-3s-194,-422,-194,-422s-65,47,-65,47z
M834 80h400000v40h-400000z"></path></svg>)​)\[9\]\[11\]. Multiplier la taille des données par 10 réduit l'incertitude de 3,16 fois\[9\]\[11\].

**L'Influence de la Population :** Plus les données de base (les rendements quotidiens) sont volatiles, plus la distribution d'échantillonnage sera large ("grasse"), augmentant ainsi le risque d'erreur\[22\]\[23\].

**Le Théorème Central Limite (TCL) :** C'est la "magie" des statistiques. Même si vos rendements sont distribués de manière bizarre ou asymétrique, la distribution de leurs _moyennes_ sera normale (cloche) si vous avez assez de trades (souvent N≥30)\[12\].

**L'Erreur Standard (SE) :** C'est le nom de l'écart-type de la distribution d'échantillonnage\[11\]. Elle est calculée en divisant l'écart-type estimé de la population (σ^) par n![](data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400em" height="1.08em" viewBox="0 0 400000 1080" preserveAspectRatio="xMinYMin slice"><path d="M95,702
c-2.7,0,-7.17,-2.7,-13.5,-8c-5.8,-5.3,-9.5,-10,-9.5,-14
c0,-2,0.3,-3.3,1,-4c1.3,-2.7,23.83,-20.7,67.5,-54
c44.2,-33.3,65.8,-50.3,66.5,-51c1.3,-1.3,3,-2,5,-2c4.7,0,8.7,3.3,12,10
s173,378,173,378c0.7,0,35.3,-71,104,-213c68.7,-142,137.5,-285,206.5,-429
c69,-144,104.5,-217.7,106.5,-221
l0 -0
c5.3,-9.3,12,-14,20,-14
H400000v40H845.2724
s-225.272,467,-225.272,467s-235,486,-235,486c-2.7,4.7,-9,7,-19,7
c-6,0,-10,-1,-12,-3s-194,-422,-194,-422s-65,47,-65,47z
M834 80h400000v40h-400000z"></path></svg>)​\[17\]. Pour éviter de sous-estimer le risque, on divise par n−1 lors de l'estimation de σ^\[17\]\[28\].

**(AJOUT) Résumé Simplifié :**

Les statistiques classiques permettent de dessiner la "courbe de la chance" de ta stratégie sans avoir besoin d'autres données que ton backtest. Elles disent que si tu as beaucoup de trades, ta performance moyenne est probablement proche de la réalité. Elles te donnent aussi une formule (Erreur\=Nombre de trades![](data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400em" height="1.08em" viewBox="0 0 400000 1080" preserveAspectRatio="xMinYMin slice"><path d="M95,702
c-2.7,0,-7.17,-2.7,-13.5,-8c-5.8,-5.3,-9.5,-10,-9.5,-14
c0,-2,0.3,-3.3,1,-4c1.3,-2.7,23.83,-20.7,67.5,-54
c44.2,-33.3,65.8,-50.3,66.5,-51c1.3,-1.3,3,-2,5,-2c4.7,0,8.7,3.3,12,10
s173,378,173,378c0.7,0,35.3,-71,104,-213c68.7,-142,137.5,-285,206.5,-429
c69,-144,104.5,-217.7,106.5,-221
l0 -0
c5.3,-9.3,12,-14,20,-14
H400000v40H845.2724
s-225.272,467,-225.272,467s-235,486,-235,486c-2.7,4.7,-9,7,-19,7
c-6,0,-10,-1,-12,-3s-194,-422,-194,-422s-65,47,-65,47z
M834 80h400000v40h-400000z"></path></svg>)​Volatiliteˊ​) pour savoir précisément à quel point tu dois douter de ton résultat\[4\].

**Exemples du livre pour mieux comprendre :**

**Le pile ou face :** Avec 3 lancers, avoir 100% de têtes est facile ; avec 100 000 lancers, s'éloigner de 0,50 de plus de 0,003 est quasi impossible\[8\].

**La population de 150 lbs :** Si tout le monde pèse exactement 150 lbs (zéro variation), chaque échantillon fera 150 lbs et la distribution d'échantillonnage sera une ligne droite sans aucune erreur\[14\].

**L'écart-type de 100 :** Aronson montre que si la population a un écart-type de 100, un échantillon de 100 trades réduit l'erreur standard à 10\[9\].

**Actions Concrètes :**

**Augmenter** N **:** Ne validez rien avec peu de trades ; cherchez à maximiser la taille de l'échantillon pour "écraser" l'erreur standard\[8\].

**Vérifier le seuil de 30 :** Assurez-vous d'avoir au moins 30 signaux pour que la distribution de votre moyenne commence à ressembler à une cloche normale, rendant vos tests valides\[15\].

**Calculer l'Erreur Standard :** Ne regardez pas seulement votre profit ; divisez l'écart-type de vos trades par la racine carrée de leur nombre pour connaître votre marge d'erreur\[17\]\[28\].

**(AJOUT) À retenir absolument :**

**Moyenne** \= **Vérité** : c'est une estimation soumise à l'erreur standard\[3\].

**Taille = Précision** : l'incertitude diminue avec n![](data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400em" height="1.08em" viewBox="0 0 400000 1080" preserveAspectRatio="xMinYMin slice"><path d="M95,702
c-2.7,0,-7.17,-2.7,-13.5,-8c-5.8,-5.3,-9.5,-10,-9.5,-14
c0,-2,0.3,-3.3,1,-4c1.3,-2.7,23.83,-20.7,67.5,-54
c44.2,-33.3,65.8,-50.3,66.5,-51c1.3,-1.3,3,-2,5,-2c4.7,0,8.7,3.3,12,10
s173,378,173,378c0.7,0,35.3,-71,104,-213c68.7,-142,137.5,-285,206.5,-429
c69,-144,104.5,-217.7,106.5,-221
l0 -0
c5.3,-9.3,12,-14,20,-14
H400000v40H845.2724
s-225.272,467,-225.272,467s-235,486,-235,486c-2.7,4.7,-9,7,-19,7
c-6,0,-10,-1,-12,-3s-194,-422,-194,-422s-65,47,-65,47z
M834 80h400000v40h-400000z"></path></svg>)​\[9\]\[11\].

**TCL = Sécurité** : la forme en cloche protège contre les données "bizarres"\[12\]\[14\].

**Volatilité = Doute** : un marché nerveux rend votre backtest moins fiable\[22\]\[23\].

**Limite classique** : cette méthode suppose que la distribution est normale ; si ce n'est pas le cas, les conclusions sont fausses\[16\]\[33\].

J'ai terminé l'analyse de la dérivation de la distribution d'échantillonnage par l'approche classique selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] undefined
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] undefined
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[9] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] undefined
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] undefined
[15] undefined
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[17] undefined
[18] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[19] undefined
[22] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[23] undefined
[28] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[33] undefined
