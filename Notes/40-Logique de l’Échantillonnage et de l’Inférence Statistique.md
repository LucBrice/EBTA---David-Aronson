---
exported: 2026-06-12T08:58:17.960Z
source: NotebookLM
type: note
title: "40-Logique de l’Échantillonnage et de l’Inférence Statistique"
---

# 40-Logique de l’Échantillonnage et de l’Inférence Statistique

导出时间: 12/06/2026 10:58:17

---

### **CH 4 - 2 : AN EXAMPLE OF SAMPLING AND STATISTICAL INFERENCE**

Voici l'analyse détaillée de l'exemple fondamental utilisé par David Aronson pour introduire la logique de l'échantillonnage et de l'inférence statistique, en utilisant l'analogie de la "boîte de billes"\[1\]\[2\].

**(AJOUT) Idées clés :**

**Population vs Échantillon :** La population représente la vérité totale (invisible), tandis que l'échantillon est la fenêtre limitée dont nous disposons\[3\].

**L’Inférence comme Saut Inductif :** L’acte de projeter une observation passée (échantillon) vers un futur inconnu (population)\[1\].

**La Variabilité d’Échantillonnage :** Le phénomène inévitable où les résultats fluctuent d’un échantillon à l’autre par pur hasard\[8\].

**Le Centre de Gravité :** La valeur réelle de la population agit comme une force qui maintient les statistiques d'échantillon dans une certaine plage\[9\]\[11\].

**La Loi des Grands Nombres :** Plus l'échantillon est grand, plus le rôle du hasard diminue et plus la vérité se révèle\[12\]\[13\].

**Référence :**

_AN EXAMPLE OF SAMPLING AND STATISTICAL INFERENCE_ (Pages 172–179)\[1\]\[14\].

**Citation Directe :**

« The central concept of statistical inference is extrapolating from samples. A sample of observations is studied, a pattern is discerned, and this pattern is expected to hold for (extrapolated to) cases outside the observed sample. » (Page 173)\[1\].

**Vision Macro :**

L'enjeu est de comprendre pourquoi nous avons besoin des statistiques en trading. Aronson explique que nous ne pouvons jamais observer la "population" complète des rendements d'une stratégie (car elle inclut un futur infini)\[15\]\[16\]. Nous sommes comme un observateur devant une boîte fermée : nous ne voyons que des morceaux (le passé)\[1\]\[2\]. L'inférence statistique est l'outil rationnel qui permet de quantifier notre degré de certitude face à l'inconnu, nous protégeant ainsi contre l'excès de confiance\[17\].

**Vision Micro :**

Le protocole de l'exemple de la boîte de billes se décompose ainsi :

**Le Dispositif :** Une boîte contient un mélange inconnu de billes grises et blanches. L'objectif est de trouver la fraction de billes grises (F−G) dans toute la boîte (la population)\[1\].

**La Contrainte :** Il est interdit de vider la boîte. On ne peut prélever que des échantillons de 20 billes à la fois via un panneau coulissant\[20\].

**L'Observation (La Statistique) :** Dans le premier échantillon, on trouve 13 billes grises sur 20, soit une statistique d'échantillon f−g\=0,65\[23\]\[24\].

**Le Problème de l'Incertitude :** Est-ce que F−G\=0,65 ? C'est peu probable\[24\]\[25\]. On sait avec certitude que F−G n'est ni 0 ni 1 (puisqu'on a vu les deux couleurs), mais la valeur exacte reste floue\[26\]\[27\].

**La Répétition (50 échantillons) :** En répétant l'opération 50 fois, on remarque que f−g change à chaque fois (0,50, 0,60, 0,45, etc.)\[5\]. Cette fluctuation est la **variabilité d'échantillonnage**\[8\]\[29\].

**L'Émergence de l'Ordre :** Malgré le chaos de chaque tirage, les 50 résultats forment une "bosse" (une distribution) centrée autour d'une valeur (environ 0,55)\[30\]\[31\]. C'est ici que l'inférence se produit : on devine que la vérité (F−G) se cache au centre de cette bosse\[30\]\[31\].

**(AJOUT) Résumé Simplifié :**

Imagine que tu as un sac de bonbons. Tu n'as pas le droit de tout regarder. Tu en prends une poignée : il y a 7 fraises et 3 citrons. Tu te dis "il y a environ 70% de fraises dans le sac". Mais si tu en reprends une autre poignée, tu en auras peut-être 5 de chaque. Les statistiques servent à calculer à quel point tu peux faire confiance à ta première poignée pour deviner ce qu'il y a dans tout le sac. Plus ta poignée est grande, plus tu as de chances d'avoir raison.

**Actions Concrètes :**

**Considérer le Backtest comme une "Poignée" :** Ne voyez jamais un profit passé comme une certitude, mais comme un échantillon aléatoire d'un processus plus large\[1\]\[2\].

**Reconnaître la Variabilité :** Acceptez que si vous aviez testé votre stratégie sur une autre période de 10 ans, le résultat aurait été différent par pur hasard\[8\].

**Ne pas sur-interpréter les petits échantillons :** Aronson appelle cela "le crime de la négligence de la taille de l'échantillon"\[33\]. Un test sur 20 trades ne vaut quasiment rien pour l'inférence\[23\]\[24\].

**Chercher le "Centre de Gravité" :** Utilisez des outils comme la moyenne de nombreux sous-échantillons (Bootstrap) pour stabiliser votre estimation de la performance réelle\[9\].

**(AJOUT) À retenir absolument :**

**Échantillon (**f−g**)** \= **Population (**F−G**)**\[3\]\[5\].

**Le hasard crée du bruit** (variabilité) même quand la vérité ne change pas\[9\]\[11\].

**La taille compte :** Seuls les grands échantillons sont de bons miroirs de la réalité\[34\].

**L'inférence est une estimation**, jamais une preuve absolue\[10\]\[40\].

**Stationnarité :** L'inférence ne marche que si personne ne change "secrètement les billes" dans la boîte (marché stable)\[41\].

J'ai terminé l'explication de l'exemple de l'échantillonnage et de l'inférence statistique selon l'EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] undefined
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] undefined
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[9] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[10] undefined
[11] undefined
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[13] undefined
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[15] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[16] undefined
[17] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[20] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[23] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[24] undefined
[25] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[26] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[27] undefined
[29] undefined
[30] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[31] undefined
[33] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[34] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[40] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[41] undefined
