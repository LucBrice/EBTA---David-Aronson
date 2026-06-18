---
exported: 2026-06-12T08:57:17.239Z
source: NotebookLM
type: note
title: "94-L'Inférence Statistique : Entre Erreur Aléatoire et Biais Systématique"
---

# 94-L'Inférence Statistique : Entre Erreur Aléatoire et Biais Systématique

导出时间: 12/06/2026 10:57:17

---

### **CH 6 : DATA MINING AND STATISTICAL INFERENCE - UNBIASED ERROR AND SYSTEMATIC ERROR**

Voici l’analyse technique de la distinction fondamentale entre l’erreur sans biais (aléatoire) et l’erreur systématique (biais), telle que David Aronson l’applique à la validité des résultats de trading.

**Idées clés :**

**Définition universelle de l'erreur :** L'erreur est la différence mathématique entre la valeur observée et la valeur réelle (Erreur\=Observeˊ−Reˊel)\[1\].

**Erreur sans biais (Aléatoire) :** Elle est due aux imperfections inhérentes de mesure ; sa valeur attendue (moyenne) sur le long terme est de zéro\[1\]\[2\].

**Erreur systématique (Biais) :** Elle dévie de la vérité de manière consistante dans une direction ; sa moyenne est distinctement différente de zéro\[3\].

**Lien avec le minage :** Un estimateur sans biais ne subit que l'erreur aléatoire, tandis qu'un estimateur biaisé (comme la meilleure règle minée) subit les deux types d'erreurs simultanément\[4\]\[5\].

**Référence :**

_Data Mining and Statistical Inference - Unbiased Error and Systematic Error_ (Pages 272–273).

**Citation Directe :**

« All scientific observations are subject to error. Error is defined as the difference between an observed value and the true value: Error = observed – true. » (Page 272).\[1\]

\--------------------------------------------------------------------------------

**Vision Macro :**

L'enjeu est la fiabilité des conclusions que nous tirons des données financières. David Aronson explique que si l'erreur aléatoire est un "bruit" inévitable que la statistique sait gérer, l'erreur systématique est un "mensonge" structurel qui invalide la recherche\[1\]\[3\]. Pour le trader EBTA, l'objectif est d'identifier si un profit exceptionnel est une simple fluctuation chanceuse (erreur sans biais) ou le résultat d'un processus de sélection qui a artificiellement gonflé les chiffres (erreur systématique)\[5\]\[6\].

\--------------------------------------------------------------------------------

**Vision Micro :**

**L'Erreur Sans Biais (****Unbiased Error****) :**

**Mécanisme :** Elle est "haphazard" (hasardeuse). Par exemple, dans une pesée, elle peut provenir de variations aléatoires de l'humidité ambiante\[7\].

**Propriété :** Elle se distribue de manière égale de chaque côté de la vérité. Si l'on fait la moyenne de milliers d'observations souffrant uniquement de cette erreur, le résultat sera très proche de la vérité car les erreurs positives et négatives s'annulent (Figure 6.6)\[1\]\[3\].

**En Trading :** Le backtest d'une règle unique, sans optimisation, produit une estimation sans biais. Le résultat peut être faux à cause de la chance, mais il n'est pas "truqué" par le processus\[5\]\[8\].

**L'Erreur Systématique ou Biais (****Systematic Error****) :**

**Mécanisme :** Elle pousse les résultats systématiquement d'un côté de la vérité. Par exemple, une balance mal réglée qui sous-estime toujours le poids\[3\]\[7\].

**Propriété :** Faire la moyenne d'observations biaisées ne corrige pas l'erreur ; cela ne fait que confirmer la déviation (Figure 6.7)\[3\].

**En Trading :** Le minage de données (chercher la meilleure règle parmi 1 000) introduit un biais systématique positif. En sélectionnant le maximum, on ne garde que les erreurs de chance positives, ce qui crée un profit artificiellement élevé qui ne peut pas durer\[5\]\[9\].

\--------------------------------------------------------------------------------

**Résumé Simplifié :**

L'erreur sans biais, c'est comme tirer sur une cible : tu rates parfois à gauche, parfois à droite, mais en moyenne tu es au centre. L'erreur systématique, c'est comme avoir un fusil dont le viseur est tordu : tous tes tirs finissent à côté, toujours au même endroit. En trading, le minage de données tord ton viseur statistique et te fait croire que tu es un génie alors que tu as juste sélectionné un "coup de bol"\[1\].

**Exemples du livre pour mieux comprendre :**

**La balance du chimiste :** Des variations d'humidité créent une erreur sans biais (aléatoire). Une balance défectueuse qui affiche toujours 10g de moins crée une erreur systématique (biais)\[7\].

**Les prédictions scolaires :** Toujours prédire une note supérieure à celle que l'on reçoit est un jugement biaisé. Prédire une note parfois trop haute et parfois trop basse est un jugement sans biais, bien qu'imparfait\[2\].

\--------------------------------------------------------------------------------

**Actions Concrètes :**

**Calibrer vos attentes :** Sachez que si vous avez testé plusieurs versions d'une stratégie, votre résultat est mathématiquement infecté par une erreur systématique positive\[4\]\[10\].

**Ne pas confondre précision et justesse :** Une règle qui gagne 50 % en backtest peut être très "précise" sur le passé, mais totalement "fausse" (biaisée) vis-à-vis du futur\[11\]\[12\].

**Utiliser la moyenne comme ancre :** Pour une règle unique, le profit passé est une estimation sans biais du futur ; pour une règle minée, il ne l'est jamais sans correction statistique\[5\].

\--------------------------------------------------------------------------------

**À retenir absolument :**

**Erreur = Observé - Réel**\[1\].

L'erreur sans biais a une **moyenne de zéro** sur le long terme\[1\].

L'erreur systématique (biais) **fausse la vérité** de manière constante\[3\].

Le minage de données transforme les erreurs de chance en un **biais positif systématique**\[5\].

Un estimateur sans biais est la **clé de l'inférence scientifique** en EBTA\[5\]\[11\].

J'ai terminé l'analyse de l'erreur sans biais et de l'erreur systématique selon le protocole EBTA.
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
