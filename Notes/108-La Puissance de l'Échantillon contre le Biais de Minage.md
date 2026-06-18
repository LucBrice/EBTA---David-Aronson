---
exported: 2026-06-12T08:57:01.495Z
source: NotebookLM
type: note
title: "108-La Puissance de l'Échantillon contre le Biais de Minage"
---

# 108-La Puissance de l'Échantillon contre le Biais de Minage

导出时间: 12/06/2026 10:57:01

---

### **CH 6 : FACTOR 2 - NUMBER OF OBSERVATIONS USED TO COMPUTE THE PERFORMANCE STATISTIC**

Cette section analyse l'impact de la taille de l'échantillon (le nombre d'observations) sur l'ampleur du biais de minage de données. David Aronson considère ce facteur comme le plus crucial pour la validité des tests\[1\].

\--------------------------------------------------------------------------------

**Idées clés :**

**La primauté de l'échantillon :** De tous les facteurs influençant le biais, la taille de l'échantillon est probablement le plus important\[1\].

**Dilution de la chance :** Plus le nombre d'observations augmente, moins une coïncidence chanceuse (quelques mois très profitables par accident) peut gonfler artificiellement le rendement moyen\[1\].

**Loi des Grands Nombres :** Un échantillon large force la performance observée à converger vers le mérite réel de la règle\[2\].

**Seuil de sécurité :** Avec un échantillon suffisamment grand (ex: 600 mois), l'augmentation du nombre de règles testées n'augmente plus de manière significative le biais de minage\[2\].

\--------------------------------------------------------------------------------

**Référence :**

_Factor 2: Number of Observations Used to Compute the Performance Statistic_ (Pages 299–301).

\--------------------------------------------------------------------------------

**Citation Directe :**

« In fact, of all the factors impacting the size of the bias, sample size may be the most important. The more observations used, the less opportunity there is for a few lucky observations (profitable months) to result in a high mean return. » (Page 299).

\--------------------------------------------------------------------------------

**Vision Macro :**

L'enjeu est la lutte contre le "bruit" temporel. David Aronson explique que le hasard est une force qui domine les petits nombres. En trading, un profit sur une courte période n'a quasiment aucune valeur scientifique. La "vérité" d'une règle ne peut émerger que si elle est soumise à une multitude d'épreuves sur une longue période. C'est l'application de la rigueur statistique pour transformer une intuition incertaine en une connaissance fondée sur des preuves.

\--------------------------------------------------------------------------------

**Vision Micro :**

Le mécanisme de réduction du biais par l'augmentation des observations repose sur la structure de la distribution d'échantillonnage :

**Largeur de la distribution (Figure 6.34) :** Un petit échantillon produit une distribution "large". Cela signifie que la règle a statistiquement beaucoup d'espace pour s'écarter de la réalité par pure chance (gains ou pertes extrêmes)\[1\].

**Resserrement de la distribution :** Un grand échantillon produit une distribution étroite. La performance observée est "prisonnière" du mérite réel, laissant très peu de place aux anomalies chanceuses\[1\].

**L'expérience des ATR (Figure 6.35) :** Aronson a testé des univers de 10 et 100 règles en faisant varier la durée de l'historique de 1 à 1 000 mois.

**Résultat :** Le biais chute de manière exponentielle.

**Constat majeur :** Lorsque l'échantillon atteint environ 600 mois, la différence de biais entre tester 10 règles et en tester 100 devient minuscule\[2\]. Cela signifie qu'un historique long permet au data miner d'être beaucoup plus ambitieux dans ses recherches sans risquer de faux positifs\[2\].

\--------------------------------------------------------------------------------

**Résumé Simplifié :**

Plus tu as de données historiques, moins tu as de chances d'être trompé par un "coup de bol". Si tu testes une stratégie sur 10 mois, un seul bon mois peut te faire croire que tu es un génie. Si tu la testes sur 1 000 mois, la chance finit par s'annuler et seul le talent (le mérite réel) reste visible.

\--------------------------------------------------------------------------------

**Actions Concrètes :**

**Priorité absolue à l'historique :** Avant de chercher à tester de nouvelles règles, cherchez à obtenir l'historique de données le plus long possible pour vos actifs.

**Scepticisme sur le court terme :** Soyez extrêmement méfiant face à des statistiques de performance (Sharpe, rendement) calculées sur un faible nombre de signaux ou d'intervalles de temps\[2\].

**Exploiter les grands échantillons :** Si vous disposez de données sur plusieurs décennies, vous pouvez vous permettre d'optimiser davantage de paramètres car le risque de biais est stabilisé par la masse de données\[2\].

\--------------------------------------------------------------------------------

**À retenir absolument :**

La taille d'échantillon est le **meilleur antidote** au biais de minage.

Peu de données = **Biais massif** (illusion de profit)\[1\].

La Loi des Grands Nombres **travaille pour le trader objectif**\[2\].

À partir de **600 observations**, le biais devient très stable\[2\].

Ne jamais valider une stratégie sur un **historique "maigre"**.

J'ai terminé l'analyse du facteur 2 (nombre d'observations) selon le protocole EBTA.
---

## 引用来源

[1] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
[2] Evidence-Based Technical Analysis - Applying the Scientific Method and Statistical Inference to Trading Signals 2007.pdf
