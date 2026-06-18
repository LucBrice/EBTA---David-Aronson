---
exported: 2026-06-12T08:56:40.184Z
source: NotebookLM
type: note
title: "128-Les Clés de la Puissance Statistique selon David Aronson"
---

# 128-Les Clés de la Puissance Statistique selon David Aronson

导出时间: 12/06/2026 10:56:40

---

D'après les travaux de David Aronson, l'amélioration de Romano-Wolf est une solution technique spécifique pour corriger une perte de puissance liée à la composition de l'univers de minage (critique de Hansen). Cependant, le livre identifie d'autres leviers fondamentaux, plus structurels, pour augmenter la puissance statistique d'un test.

# MOYENS D'AUGMENTER LA PUISSANCE STATISTIQUE D'UN TEST

## Référence

**Titre :**_Statistical Analysis_ (Chapitre 4) ; _Hypothesis Tests and Confidence Intervals_ (Chapitre 5) ; _Data-Mining Bias_ (Chapitre 6).

**Pages :** 176, 179, 299-301, 329-330.

**Thème principal :** Les facteurs influençant la dispersion de la distribution d'échantillonnage et la capacité de détection du mérite réel.

## Idées clés

**L'augmentation de la taille de l'échantillon (**N**)** — C'est le levier le plus puissant. Un N plus élevé rétrécit la distribution d'échantillonnage, rendant le test plus sensible aux petits avantages prédictifs. (Pages 179, 301)\[1\]\[2\].

**La réduction de la variance de la population** — Moins les données de base sont volatiles, plus la distribution d'échantillonnage est étroite, ce qui augmente la puissance du test. (Page 181/Source)\[3\].

**La gestion de la composition de l'univers** — Éviter d'inclure des milliers de règles "pires que le hasard" (règles négatives) qui, sans Romano-Wolf, "gonflent" artificiellement le seuil de significativité. (Page 329)\[4\].

**Le choix de règles à fort mérite** — Une règle possédant un avantage prédictif réel important est plus facile à détecter, car elle s'éloignera plus nettement de la moyenne du hasard. (Page 282)\[5\].

## Citation directe

« Large samples give F-G, the truth that we wish to know, the ability to reveal itself. This is an effect of the Law of Large Numbers: Large samples reduce the role of chance. » (Page 179)\[1\]._(En français : Les grands échantillons donnent à la vérité la capacité de se révéler. C'est l'effet de la Loi des Grands Nombres : les grands échantillons réduisent le rôle du hasard.)_

## Vision macro

L'enjeu de la puissance statistique est d'éviter l'**Erreur de Type II** : rejeter une règle qui a pourtant un vrai talent parce que le test est trop "sourd" pour le percevoir\[6\]\[7\]. Pour Aronson, la puissance n'est pas seulement une affaire d'algorithme (comme Romano-Wolf), c'est une question de **résolution** : plus vous avez de données (N), plus votre "télescope" statistique est précis pour distinguer une étoile (un edge) d'un simple reflet (le bruit)\[8\]\[9\].

## Vision micro

Le fonctionnement de la puissance repose sur la **dispersion de la distribution d'échantillonnage** :

**Mécanisme de l'échantillon (**N**) :** La largeur de la cloche de Gauss est inversement proportionnelle à la racine carrée de N\[10\]. Si vous multipliez le nombre de trades par 100, vous divisez l'incertitude (et donc la zone d'ombre où le talent est confondu avec la chance) par 10\[10\].

**Rapport Signal/Bruit :** La puissance augmente si l'effet que vous cherchez (le rendement attendu) est large par rapport à la variance des rendements\[3\].

**Impact de la sélection (Multiple Comparisons) :** Sans Romano-Wolf, le simple fait d'augmenter le nombre de règles testées (N rules) _diminue_ la puissance effective du test sur chaque règle individuelle, car le seuil de réussite (p-value) devient extrêmement difficile à atteindre pour compenser le biais de minage\[11\]\[12\].

## Exemples du livre

**L'expérience des 200 perles :** Aronson montre qu'avec un échantillon de 20 perles, l'incertitude est grande. En passant à 200 perles, la variation aléatoire devient trois fois plus petite, permettant de voir la "vérité" (la proportion réelle de perles grises) avec beaucoup plus de clarté\[10\]\[13\].

**Le violoniste de l'orchestre :** Dans une audition de musique (faible hasard), le mérite est si évident que le "test" (l'écoute) a une puissance maximale immédiatement. En trading (fort hasard), il faut des centaines d'épreuves pour atteindre la même puissance de détection\[5\].

## Résumé simplifié

Pour rendre un test plus puissant sans changer de méthode mathématique, il faut lui donner "plus à manger". Le moyen le plus simple est d'utiliser beaucoup plus de données (plus de jours, plus de trades). C'est comme passer d'une photo floue à une photo HD : les détails (votre profit réel) deviennent visibles alors qu'ils étaient cachés dans le flou du hasard.

## Actions concrètes

**Ce qu'il faut faire :** Prioriser l'augmentation du nombre d'observations (N) avant toute chose.

**Ce qu'il faut éviter :** Tester des stratégies sur des historiques trop courts (moins de 200-600 points), car même avec Romano-Wolf, le test manquera de puissance pour valider un edge réel\[2\]\[14\].

**Ce qu'il faut mesurer :** La réduction de l'écart-type de votre distribution d'échantillonnage à mesure que vous ajoutez des données.

**Ce qu'il faut tester :** Des règles simples basées sur des théories plausibles (Chapitre 7) pour maximiser les chances d'avoir un "signal" fort dès le départ\[15\]\[16\].

## Limites et erreurs fréquentes

### Limites

**Le livre ne traite pas** d'autres algorithmes de tests multiples concurrents de Romano-Wolf (comme le False Discovery Rate) ; il se concentre sur le WRC et la MCPM.

L'augmentation de N a des **rendements décroissants** : il faut quadrupler les données pour doubler la précision.

### Erreurs fréquentes

Confondre la **puissance du test** (capacité à voir le talent) avec le **profit de la règle** (le talent lui-même).

Croire que l'on peut compenser un manque de données par un test statistique ultra-sophistiqué. **Aucun test ne peut créer de l'information là où il n'y a que du bruit**\[14\]\[17\].

## À retenir absolument

N **(Observations) est le levier n°1** de la puissance.

La puissance est la capacité à **débusquer l'or réel** caché sous le hasard.

L'incertitude diminue quand la **taille de l'échantillon augmente**.

Inclure trop de "règles poubelles" dans un univers de minage **étouffe la puissance** du test.

Un test sans puissance vous fera **abandonner de bonnes stratégies** par erreur.

J'ai terminé l'analyse des moyens d'augmenter la puissance d'un test selon le protocole EBTA.
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
[9] undefined
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[12] undefined
[13] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[15] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[17] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
