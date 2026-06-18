---
exported: 2026-06-12T08:56:30.130Z
source: NotebookLM
type: note
title: "137-L'indépendance linéaire et les limites de l'analyse technique"
---

# 137-L'indépendance linéaire et les limites de l'analyse technique

导出时间: 12/06/2026 10:56:30

---

# L'INDÉPENDANCE LINÉAIRE DES RENDEMENTS ET LES DÉFIS DE L'ANALYSE TECHNIQUE

## Référence

**Titre exact :**_The Evidence in Favor of EMH_ (L'évidence en faveur de l'EMH).

**Chapitre :** Chapitre 7 : _Theories of Nonrandom Price Motion_.

**Pages :** 341 – 342 (référencé également en page 503\[1\]).

**Thème principal :** L'impact de l'absence de corrélation linéaire entre les prix passés et futurs sur la validité de l'analyse technique.

## Idées clés

**Indépendance linéaire** — Les études d'autocorrélation confirment que les changements de prix (rendements) sont linéairement indépendants les uns des autres\[2\].

**Absence de pouvoir prédictif** — Puisque les rendements sont indépendants, une fonction linéaire basée sur les rendements actuels et passés ne peut pas être utilisée pour prédire les rendements futurs\[2\].

**Validation de la marche aléatoire** — Cette indépendance statistique soutient le modèle de la "marche aléatoire", où le marché n'a pas de mémoire exploitable de ses mouvements passés\[2\]\[3\].

**Limitation des tests classiques** — L'analyse technique traditionnelle, qui repose souvent sur des relations simples entre prix passés et futurs, échoue face à cette réalité statistique\[2\].

## Citation directe

“This means that a linear function of current and past returns cannot be used to predict future returns. Based on these findings, it was concluded by EMH advocates, that security returns are an unpredictable random walk.”\[2\]

_(Traduction : Cela signifie qu'une fonction linéaire des rendements actuels et passés ne peut pas être utilisée pour prédire les rendements futurs. Sur la base de ces résultats, les défenseurs de l'EMH ont conclu que les rendements des titres sont une marche aléatoire imprévisible.)_

## Vision macro

L'enjeu est la **falsification de l'analyse technique** classique. David Aronson explique que si les marchés étaient prévisibles de la manière dont l'analyse technique traditionnelle le prétend, nous devrions observer des corrélations statistiques entre ce qui s'est passé hier et ce qui se passe aujourd'hui\[2\]. L'indépendance linéaire des rendements est l'un des arguments les plus puissants de l'Hypothèse d'Efficience des Marchés (EMH)\[2\]\[4\]. Pour l'EBTA, cela signifie que la majorité des outils "visuels" ou "linéaires" de l'AT sont probablement sans valeur, car ils tentent d'extraire une structure là où les tests statistiques ne trouvent que du vide (du bruit blanc)\[5\]\[6\].

## Vision micro

Le mécanisme statistique qui rend l'AT difficile repose sur l'**autocorrélation** :

**Le test d'autocorrélation :** On mesure la corrélation entre le rendement du jour J et celui du jour J−1, J−2, etc.\[1\].

**Le résultat :** Dans les marchés financiers, ces coefficients de corrélation sont généralement proches de zéro\[2\].

**La conséquence mathématique :** Si la corrélation est nulle, la connaissance du prix passé n'ajoute aucune information pour réduire l'incertitude sur le prix futur\[7\].

**La faille de l'AT classique :** La plupart des indicateurs techniques (moyennes mobiles, momentum) sont des fonctions linéaires du prix. Si le prix est linéairement indépendant, ces indicateurs sont mathématiquement condamnés à ne produire aucun "alpha" (surperformance)\[2\]\[8\].

## Exemples du livre

**L'expérience des pièces de monnaie :** Aronson explique qu'on peut créer un graphique qui ressemble à s'y méprendre à un graphique boursier simplement en lançant une pièce de monnaie (pile = +1,face\=−1)\[3\]\[9\]. Sur ces graphiques, les rendements sont parfaitement indépendants par construction, et pourtant, on y voit apparaître des "épaules-tête-épaules" ou des tendances\[3\]\[10\]. Cela montre que l'apparence de structure ne prouve pas l'absence d'indépendance linéaire.

**Les travaux d'Andrew Lo et MacKinlay :** Bien que l'indépendance linéaire soit la règle, Aronson cite ces auteurs pour montrer que des tests plus complexes (non linéaires) peuvent parfois détecter des structures que l'autocorrélation classique ne voit pas\[11\]\[12\].

## Résumé simplifié

L'indépendance linéaire, c'est comme dire que la bourse est un casino où chaque lancer de dé est totalement nouveau. Si le dé a fait un "6" trois fois de suite, la probabilité qu'il fasse encore un "6" reste exactement la même. L'analyse technique classique essaie de prédire le prochain chiffre en regardant les lancers précédents. Mais comme les chiffres ne sont pas liés entre eux, regarder le passé est inutile. C'est pour cela que la plupart des graphiques sont des "marches aléatoires" : ils bougent, mais sans logique prévisible.

## Actions concrètes

**Ce qu'il faut faire :** Utiliser des tests de significativité rigoureux (comme le WRC) pour vérifier si un profit observé n'est pas juste un accident dans une série de données indépendantes\[13\]\[14\].

**Ce qu'il faut éviter :** Se fier à des indicateurs techniques simples (Moyennes Mobiles, RSI) sans avoir testé leur capacité à battre une marche aléatoire\[15\]\[16\].

**Ce qu'il faut tester :** Explorer des modèles **non linéaires** (comme les réseaux de neurones) ou des tests de **ratio de variance**, car ils peuvent détecter des motifs que l'indépendance linéaire cache\[11\]\[17\].

## Limites et erreurs fréquentes

### Limites

L'indépendance linéaire n'exclut pas l'existence de **dépendances non linéaires** (plus complexes)\[11\].

Elle n'empêche pas l'existence de "primes de risque" (comme le fait que le marché monte sur le très long terme pour rémunérer le capital)\[17\]\[18\].

### Erreurs fréquentes

**L'illusion de l'ordre :** Croire qu'une tendance visuelle sur un graphique prouve que les rendements sont liés, alors que le pur hasard produit les mêmes formes\[19\]\[20\].

**Confondre corrélation et causalité :** Penser qu'un indicateur fonctionne parce qu'il "cause" le mouvement, alors qu'il n'est qu'une répétition accidentelle dans un marché sans mémoire\[21\].

## À retenir absolument

Les rendements passés ne prédisent pas les rendements futurs de manière **linéaire**\[2\].

Le marché se comporte statistiquement comme une **marche aléatoire**\[2\].

L'AT traditionnelle est **mathématiquement désavantagée** par cette absence de mémoire\[2\]\[8\].

Seuls des **tests statistiques poussés** peuvent distinguer le talent de la chance\[6\]\[22\].

La **non-linéarité** est la seule porte de sortie pour trouver un avantage réel\[11\]\[17\].

J'ai terminé l'analyse de l'indépendance linéaire des rendements selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[3] undefined
[4] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] undefined
[7] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[8] undefined
[9] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[15] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[16] undefined
[17] undefined
[18] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[19] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[20] undefined
[21] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[22] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
