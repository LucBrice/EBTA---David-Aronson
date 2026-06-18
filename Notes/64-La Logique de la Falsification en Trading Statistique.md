---
exported: 2026-06-12T08:57:49.129Z
source: NotebookLM
type: note
title: "64-La Logique de la Falsification en Trading Statistique"
---

# 64-La Logique de la Falsification en Trading Statistique

导出时间: 12/06/2026 10:57:49

---

### **CH 5 - 4 : FALSIFYING A HYPOTHESIS WITH IMPROBABLE EVIDENCE**

Voici l’analyse technique de la procédure de falsification par l'évidence improbable, le moteur logique du test statistique en trading EBTA.

**Idées clés :**

**Logique de la surprise :** Une hypothèse est rejetée lorsque l'on observe un résultat qui serait extrêmement rare ou improbable si cette hypothèse était vraie\[1\]\[2\].

**Le déni du conséquent :** La falsification utilise une forme logique valide (Si P alors Q ; Or Non-Q ; Donc Non-P) pour inférer qu'une supposition de départ est fausse\[3\]\[4\].

**Inversion du fardeau :** En EBTA, on ne cherche pas à prouver qu'une règle est bonne, mais à démontrer que l'idée qu'elle est "nulle" est incompatible avec les profits observés\[5\]\[6\].

**Seuil de rareté :** Par convention, un résultat est jugé "improbable" s'il a moins de 5 % de chances (p-value < 0,05) de se produire sous l'Hypothèse Nulle (H0​)\[5\]\[7\].

**Référence :**

_Falsifying a Hypothesis with Improbable Evidence_, pages 220 à 221 (PDF 168-169 ; Audiobook 130-135).

**Citation Directe :**

« If low probability outcomes are observed—outcomes that would be inconsistent with the truth of the hypothesis—the hypothesis is deemed falsified. » (Page 220).

**Vision Macro :**

L'enjeu est de surmonter le biais de confirmation naturel de l'être humain. David Aronson explique que notre intuition nous pousse à chercher des preuves qui _valident_ nos croyances (inférence informelle). La science, au contraire, avance par **falsification** : elle définit ce qui _ne devrait pas arriver_ si notre théorie était fausse. Si ce "chose" arrive malgré tout (un profit énorme), alors le doute raisonnable sur la validité de la règle est levé. C'est le passage d'une attitude de "croyant" à celle de "détecteur de bêtises" (baloney detector)\[8\]\[9\].

**Vision Micro :**

Le mécanisme de falsification par l'improbable suit une séquence mathématique rigoureuse :

**Supposition (**H0​**) :** On commence par admettre que la règle n'a aucun pouvoir prédictif (rendement attendu ≤0)\[10\]\[11\].

**Attente :** Sous cette hypothèse, la distribution d'échantillonnage nous dit que les profits de backtest doivent se regrouper autour de zéro\[12\]\[13\].

**Observation Improbable :** Le backtest produit un rendement de +20 %. Le test statistique montre que ce score n'avait que 3 % de chances d'apparaître si la règle était réellement nulle\[14\]\[15\].

**Incompatibilité :** Puisque l'événement s'est produit, il y a une contradiction entre l'hypothèse (la règle est nulle) et l'évidence (le profit est là).

**Rejet :** On conclut que l'hypothèse de départ est "probablement fausse", ce qui permet d'accepter l'idée que la règle possède un talent réel\[6\]\[16\].

**Résumé Simplifié :**

Imagine que tu prétendes être un champion de tir à l'arc. Si je te demande de tirer et que tu rates la cible 20 fois de suite, ton échec est une "évidence improbable" pour un champion : ton hypothèse de talent est falsifiée. En trading, c'est l'inverse : si tu gagnes énormément d'argent alors que je pariais que tu n'avais aucune chance, ta performance "falsifie" mon idée que tu es un mauvais trader\[6\]\[17\].

**Exemples du livre pour mieux comprendre :**

**L’analogie du chien :** Si un animal n'a pas quatre pattes, cela prouve de manière certaine que ce n'est pas un chien. L'absence de la caractéristique attendue falsifie l'hypothèse\[3\]\[4\].

**Le test de tennis d'Aronson :** David Aronson se croyait excellent joueur (Hypothèse : 75 % de victoires). Après avoir perdu 20 matchs de suite (évidence hautement improbable sous son hypothèse), il a dû falsifier sa propre croyance et admettre qu'il n'était pas si bon\[17\]\[18\].

**Le Cygne Noir :** L'observation d'un seul cygne noir suffit à falsifier l'hypothèse universelle "tous les cygnes sont blancs", peu importe le nombre de cygnes blancs observés précédemment\[19\]\[20\].

**Actions Concrètes :**

**Adoptez** H0​ **par défaut :** Partez toujours du principe que votre nouvelle stratégie de trading est inutile.

**Cherchez la surprise :** Ne vous réjouissez pas d'un profit avant d'avoir calculé si ce profit est "surprenant" par rapport à ce que le hasard peut faire.

**Utilisez la p-value :** Si votre profit de backtest a une p-value > 0,05, l'évidence n'est pas assez "improbable" pour rejeter la chance. La règle doit être écartée\[7\]\[21\].

**À retenir absolument :**

La science **prouve le faux**, elle ne prouve jamais le "vrai" de manière absolue\[6\]\[22\].

Un profit est une preuve seulement s'il est **statistiquement improbable** sous H0​\[2\]\[16\].

La **p-value** est la mesure de cette improbabilité\[21\]\[23\].

Le **Déni du conséquent** est le seul raisonnement logique valide pour valider un signal\[3\]\[4\].

Falsifier H0​ est une **décision forte** car elle est contrainte par l'évidence\[24\]\[25\].

J'ai terminé l'analyse de la falsification par l'évidence improbable selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] undefined
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] undefined
[5] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[6] undefined
[7] undefined
[8] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[9] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[10] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[11] undefined
[12] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[13] undefined
[14] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[15] undefined
[16] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[17] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[18] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[19] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[20] undefined
[21] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[22] undefined
[23] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[24] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[25] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
