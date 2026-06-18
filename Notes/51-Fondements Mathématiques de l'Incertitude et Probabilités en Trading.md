---
exported: 2026-06-12T08:58:06.295Z
source: NotebookLM
type: note
title: "51-Fondements Mathématiques de l'Incertitude et Probabilités en Trading"
---

# 51-Fondements Mathématiques de l'Incertitude et Probabilités en Trading

导出时间: 12/06/2026 10:58:06

---

### **CH 4 - 14 : PROBABILITY**

Voici l’analyse des concepts de probabilité, que David Aronson considère comme le langage mathématique permettant de quantifier l’incertitude inhérente au trading,.

**Idées clés :**

**Définition de la probabilité :** Elle est la fréquence relative d'un événement sur le "très long terme" (un nombre infini d'opportunités) (p. 194),.

**Deux types de probabilités :** La probabilité **théorique** (déduite par la logique) et la probabilité **empirique** (déduite de l'observation), cette dernière étant celle qui concerne le trading (p. 196),.

**L'équivalence Aire-Probabilité :** Dans une fonction de densité, la probabilité d'un résultat est égale à la fraction de la surface totale occupée par ce résultat sur le graphique (p. 200),.

**La Loi des Grands Nombres :** Elle garantit que la fréquence observée dans nos tests finira par converger vers la probabilité réelle à mesure que le nombre d'observations augmente (p. 195),.

**Référence :**

_PROBABILITY_ (Pages 193–202 ; Audiobook Transcriptions 138-149),.

**Citation Directe :**

« Probability is the relative frequency of an event over the long run—the very long run. That is to say, the probability of an event is its relative frequency of occurrence given an infinite number of opportunities for its occurrence. » (Page 194),.

**Vision Macro :**

L'enjeu pour le trader EBTA est de passer d'une vision déterministe ("je sais ce que le marché va faire") à une vision probabiliste ("je connais la fréquence de succès de mon signal"). La probabilité est l'antidote à l'excès de confiance,. Elle permet de transformer le chaos apparent des prix en un modèle structuré où l'incertitude n'est plus ignorée, mais mesurée et intégrée dans la prise de décision,.

**Vision Micro :**

Le mécanisme de la probabilité dans l'analyse technique repose sur trois piliers techniques :

**La Fréquence Relative (**f**) :** Elle est le rapport entre le nombre d'occurrences d'un événement et le nombre total d'opportunités (TotalSucceˋs​),. Elle s'exprime par un nombre entre 0 et 1,.

**La Probabilité Empirique :** Contrairement au lancer de dés (théorique), le trading repose sur l'observation de conditions passées répétées,. Aronson souligne une limite majeure : il est impossible en trading de maintenir des conditions strictement identiques d'un test à l'autre (problème de non-stationnarité), contrairement aux sciences expérimentales,.

**La Densité de Probabilité :** Pour les variables continues (comme les rendements), la probabilité d'obtenir une valeur _exacte_ (ex: gagner exactement 1,234%) est mathématiquement nulle,. Par conséquent, on ne calcule que la probabilité qu'un résultat tombe dans une **plage de valeurs** (ex: gain supérieur à 10%) en mesurant l'aire sous la courbe correspondante,,.

**Résumé Simplifié :**

La probabilité en trading, c'est le pourcentage de chances qu'un signal gagne s'il était testé une infinité de fois. Comme on ne peut pas tester à l'infini, on utilise des backtests. Plus le backtest est long, plus on a de chances que le résultat observé soit proche de la "vraie" probabilité de la stratégie.

**Exemples du livre pour mieux comprendre :**

**Théorique vs Empirique :** La probabilité de faire "Face" est théorique (0,50) car elle repose sur la symétrie de la pièce,. La probabilité qu'il neige sur le **Mont Hood** en juillet est empirique : elle ne peut être connue qu'en comptant les jours de neige passés en juillet,.

**La Statue de la Liberté :** La température mesurée à son pied est une variable continue,. On peut prédire la probabilité qu'il fasse entre 20°C et 25°C, mais pas la probabilité qu'il fasse exactement 22,12345°C,.

**Le "Holy Grail" du parieur :** Aronson illustre la naïveté de celui qui, après 5 "Face" consécutifs, croit avoir trouvé une pièce miracle,. C'est la même erreur qu'un trader qui valide une règle après seulement 5 trades gagnants, ignorant la Loi des Grands Nombres,.

**Actions Concrètes :**

**Calculer la fréquence relative :** Ne dites jamais "ce signal marche souvent", dites "ce signal a gagné dans 62% des 500 cas observés",.

**Exiger des échantillons larges :** Rejetez toute statistique basée sur moins de 30 à 50 observations, car le rôle du hasard y est trop prépondérant,.

**Raisonner en plages de valeurs :** Lors de l'évaluation de vos profits, regardez la probabilité d'atteindre un objectif _ou plus_, plutôt qu'un chiffre fixe,.

**À retenir absolument :**

**Probabilité = Fréquence** sur un horizon infini,.

Le trading utilise uniquement la probabilité **empirique** (basée sur l'histoire),.

L'**aire sous la courbe** est la seule mesure valide de la probabilité en trading,.

La **Loi des Grands Nombres** est le juge final de la validité d'une règle,.

La probabilité d'un prix exact est de **zéro** ; on trade des probabilités d'intervalles,,.

J'ai terminé l'analyse des probabilités selon le protocole EBTA.