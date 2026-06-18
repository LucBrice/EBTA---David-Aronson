---
exported: 2026-06-12T08:57:50.203Z
source: NotebookLM
type: note
title: "63-L'Essence de l'Hypothèse Statistique en Trading EBTA"
---

# 63-L'Essence de l'Hypothèse Statistique en Trading EBTA

导出时间: 12/06/2026 10:57:50

---

### **CH 5 - 3 : WHAT IS A STATISTICAL HYPOTHESIS?**

Voici l’analyse technique de la définition de l'hypothèse statistique, l'outil qui permet de passer d'une simple intuition sur une règle de trading à une affirmation scientifique quantifiable\[1\].

**Idées clés :**

**Conjecture sur l'inconnu :** Une hypothèse statistique est une supposition sur la valeur d'un paramètre de population (ex: le rendement futur d'une stratégie)\[2\]\[3\].

**Lien avec le paramètre :** En trading EBTA, ce paramètre est généralement le rendement quotidien moyen annualisé sur des données dé-tendancées\[2\]\[4\].

**Point de départ par défaut :** On suppose toujours, avant preuve du contraire, que la règle n'a aucune valeur (rendement ≤0)\[2\]\[5\].

**Mesure de la distance :** Le test d'hypothèse sert à déterminer si le résultat du backtest (statistique d'échantillon) est "proche" ou "loin" de la valeur supposée par l'hypothèse\[2\].

**Référence :**

_What Is a Statistical Hypothesis?_, Chapitre 5, pages 220 à 221\[1\]\[6\].

**Citation Directe :**

« A statistical hypothesis is a conjecture about the value of a population parameter. » (Page 220)\[2\].

**Vision Macro :**

L'enjeu est de remplacer le jugement subjectif par une règle de décision mathématique\[7\]\[8\]. David Aronson explique que sans hypothèse statistique, un trader est incapable de dire si son profit de +20 % est un exploit ou un accident\[9\]. L'hypothèse fournit le cadre de référence : elle définit ce qui est "normal" de voir si la règle est inutile, permettant ainsi d'identifier les performances véritablement exceptionnelles\[10\]\[11\].

**Vision Micro :**

Le mécanisme de l'hypothèse statistique repose sur la confrontation entre deux valeurs :

**Le Paramètre de Population (Inconnu) :** C'est la "vérité" sur la règle, sa performance réelle dans le futur ou sur une infinité de trades\[4\]\[12\]. Puisqu'on ne peut pas l'observer, on émet une hypothèse sur sa valeur (souvent 0)\[2\]\[4\].

**La Statistique d'Échantillon (Connue) :** C'est le résultat concret de votre backtest sur les données historiques\[2\]\[13\].

**La Quantification (p-value) :** Le test transforme la distance entre ces deux valeurs en une probabilité (p) allant de 0 à 1,0\[9\]\[14\].

_Exemple du livre :_ Si vous supposez un rendement de 0 % mais que vous obtenez +20 % avec une p-value de 0,03, cela signifie qu'il n'y a que 3 % de chances qu'une règle inutile produise un tel résultat par pur hasard\[9\]\[15\].

**Résumé Simplifié :**

Une hypothèse statistique, c'est comme poser une règle de base : "Je parie que ma stratégie ne vaut rien (0 % de gain)". Ensuite, tu regardes tes résultats passés. Si tes gains sont tellement énormes qu'il est quasiment impossible qu'ils soient arrivés par chance alors que la règle de base est vraie, tu en conclus que ta stratégie a un vrai talent\[9\]\[11\].

**Exemples du livre pour mieux comprendre :**

**Le test du 20 % :** Aronson illustre une règle avec un profit de +20 %. L'hypothèse statistique est que le rendement réel est ≤0. Si le test conclut qu'un tel profit n'a que 3 % de probabilité d'apparaître sous cette hypothèse, on rejette l'idée que la règle est nulle\[9\].

**La boîte de billes :** L'hypothèse était que la proportion de billes grises (F−G) était d'une certaine valeur. Le test a consisté à comparer la fraction observée dans un petit échantillon (f−g) à cette hypothèse pour voir si l'écart était raisonnable\[4\]\[16\].

**Actions Concrètes :**

**Définissez votre cible :** Avant de backtester, posez explicitement votre hypothèse nulle (H0​ : rendement ≤0)\[2\]\[17\].

**Calculez la p-value :** Ne vous contentez pas d'un profit élevé ; utilisez la distribution d'échantillonnage pour calculer la probabilité que ce profit soit accidentel\[18\]\[19\].

**Appliquez un seuil de rejet :** Fixez une limite (souvent p<0,05) en dessous de laquelle vous considérez que votre hypothèse de "zéro talent" est fausse\[14\]\[20\].

**À retenir absolument :**

C'est une supposition sur le **futur/paramètre**, pas un constat sur le passé\[4\]\[21\].

En EBTA, l'hypothèse par défaut est que le profit attendu est de **zéro**\[2\]\[22\].

Elle est le fondement indispensable du **test de p-value**\[9\]\[23\].

Elle permet de distinguer scientifiquement la **compétence de la chance**\[8\]\[9\].

Une hypothèse n'est jamais "prouvée vraie", elle est seulement "non rejetée" ou "falsifiée"\[10\]\[24\].

J'ai terminé l'analyse de ce qu'est une hypothèse statistique selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[3] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[4] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[5] undefined
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
[19] undefined
[20] undefined
[21] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[22] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[23] undefined
[24] undefined
