---
exported: 2026-06-12T08:57:22.136Z
source: NotebookLM
type: note
title: "89-L’Induction face à la Recherche de Règles en Trading"
---

# 89-L’Induction face à la Recherche de Règles en Trading

导出时间: 12/06/2026 10:57:22

---

### **DIFFÉRENCE ENTRE RULE SEARCHING ET RULE INDUCTION**

Voici l’analyse comparative entre la « recherche de règles » (_rule searching_) et l’ « induction de règles » (_rule induction_), deux niveaux distincts de minage de données en analyse technique objective.

**Idées clés :**

**Stabilité vs Évolution :** Le _rule searching_ travaille avec des formes de règles dont la complexité est fixée à l'avance, alors que le _rule induction_ fait évoluer cette complexité de manière autonome\[1\]\[2\].

**Nature de l'univers :** Dans le _rule searching_, on compare des philosophies différentes (tendance vs retour à la moyenne) ; dans le _rule induction_, on fusionne ces philosophies pour en créer de nouvelles\[3\]\[4\].

**Rôle de l'humain vs Machine :** L'humain définit les structures logiques pour le _searching_, tandis que les algorithmes d'apprentissage automatique (_machine learning_) génèrent les structures pour l' _induction_\[4\]\[5\].

**Risque de sur-ajustement :** Le _rule induction_ présente un risque d' _overfitting_ (sur-ajustement) bien plus élevé à cause de la dimension supplémentaire de recherche\[5\].

\--------------------------------------------------------------------------------

**Référence :**

_Rule Searching_ (Pages 266–267) ; _Rule Induction with Variable Complexity_ (Page 267) ; _Complexity Search_ (Pages 457–460)\[1\].

\--------------------------------------------------------------------------------

**Citation Directe :**

« Though rule searching considers a multitude of rule forms, each rule’s complexity remains fixed throughout the course of the search. \[...\] In contrast, rule induction uses machine learning to find the degree of complexity that produces the best performance. » (Pages 267 et 457)\[1\].

\--------------------------------------------------------------------------------

**Vision Macro :**

L'enjeu est de trouver l'équilibre entre la puissance de recherche et la fiabilité statistique. Le **Rule Searching** est une démarche d'exploration : on cherche quelle idée préconçue (ex: "le RSI est-il meilleur que les Moyennes Mobiles ?") fonctionne le mieux\[1\]\[7\]. Le **Rule Induction** est une démarche de synthèse : on part du principe que le marché est trop complexe pour une règle simple et on laisse l'ordinateur construire une solution sur mesure, souvent non linéaire, capable de s'adapter à cette complexité\[2\]\[8\].

\--------------------------------------------------------------------------------

**Vision Micro :**

**Rule Searching (Complexité Fixe) :**

**Mécanisme :** On définit plusieurs "formes" de règles (ex: Cassure de canal, Croisement de moyennes). Chaque forme a un nombre de paramètres fixe (ex: 2 look-backs)\[1\]\[9\].

**Processus :** L'ordinateur balaie toutes les combinaisons de paramètres pour chaque forme et sélectionne le meilleur résultat global\[1\].

**Limitation :** Les règles ne sont jamais combinées entre elles. Si une règle de tendance est testée, elle reste une règle de tendance pure\[1\].

**Rule Induction (Complexité Variable) :**

**Mécanisme :** L'algorithme commence par des règles simples, puis ajoute des opérateurs logiques (AND, OR, IF-THEN) ou des fonctions mathématiques pour les fusionner\[2\]\[4\].

**Processus :** Il utilise le _machine learning_ (réseaux de neurones, algorithmes génétiques) pour augmenter la complexité tant que la performance sur les données de test s'améliore\[4\].

**Innovation :** Il permet de découvrir des synergies. Par exemple, une règle peut n'être profitable que si elle est filtrée par un indicateur de volatilité, ce que le _searching_ classique ne verrait pas s'il teste les deux séparément\[6\]\[11\].

\--------------------------------------------------------------------------------

**Résumé Simplifié :**

Le **Rule Searching**, c'est comme avoir un grand livre de recettes de cuisine et tester laquelle est la meilleure sans jamais changer les ingrédients. Le **Rule Induction**, c'est comme donner tous les ingrédients à un chef robot et le laisser inventer sa propre recette en mélangeant tout jusqu'à ce que le plat soit parfait\[1\]\[4\].

\--------------------------------------------------------------------------------

**Exemples du livre pour mieux comprendre :**

**Exemple de Searching :** L'étude de cas d'Aronson avec **6 402 règles** sur le S&P 500 est un _rule searching_. Il a testé des milliers de variantes de 3 thèmes (Trend, Extremes, Divergence), mais chaque règle restait isolée\[7\].

**Exemple d'Induction :** Utiliser un indicateur RSI comme **filtre** pour un croisement de moyennes mobiles. L'algorithme d'induction décide de lui-même d'ajouter cette condition "Si RSI > X alors ne pas vendre" pour améliorer la performance, augmentant ainsi la complexité de la règle originale\[6\].

\--------------------------------------------------------------------------------

**Actions Concrètes :**

**Pour le Rule Searching :** Documentez scrupuleusement le nombre total de règles et de paramètres testés pour pouvoir appliquer le **White's Reality Check**\[12\]\[14\].

**Pour le Rule Induction :** Utilisez impérativement **trois jeux de données** : _Entraînement_ (pour créer la règle), _Test_ (pour valider la complexité) et _Validation_ (pour l'estimation finale sans biais)\[5\]\[15\].

**Surveillance :** Arrêtez d'ajouter de la complexité dès que la performance sur le jeu de "Test" commence à baisser, même si elle continue de monter sur le jeu d' "Entraînement" (signe d'overfitting)\[10\].

\--------------------------------------------------------------------------------

**À retenir absolument :**

**Rule Searching** = Comparaison de règles à **structure fixe**\[1\].

**Rule Induction** = Création de règles à **structure évolutive**\[2\].

L'induction est plus puissante mais beaucoup plus **dangereuse** (overfitting)\[5\].

La **Loi de Variété Requise d'Ashby** justifie l'induction pour les marchés complexes\[13\].

Le searching est la méthode de base utilisée dans la majorité du livre d'Aronson\[12\].

J'ai terminé l'analyse de la différence entre rule searching et rule induction selon le protocole EBTA.
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
