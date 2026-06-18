# Protocoles de validation et tests d'hypothèse dans l'EBTA

## Référence

* **Titre :** *Evidence-Based Technical Analysis* (Part 1: Methodological Foundations, Chapter 6: Data Mining Bias - The Bane of Quantitative Technical Analysis)
* **Pages :** Pages 255 à 260, 315 à 322 *(références indicatives du corps de texte principal)*
* **Thème principal :** Le positionnement exact de l'inférence statistique et du test d'hypothèse globale (*White's Reality Check*) au sein du protocole de découpage des données (*Data Splitting*).

---

## Idées clés

1. **La phase de Test est le lieu exclusif du test d'hypothèse corrigé** — C'est au moment de la sélection de la meilleure règle parmi l'univers des règles explorées ($M$) que le test d'inférence doit évaluer la significativité statistique. *(Page 257)*
2. **L'échantillon de Validation (Out-of-Sample / OOS) n'est pas un lieu de décision** — Sa seule et unique fonction est de fournir une estimation pure et non biaisée de la performance future, sans aucune intervention de tests d'hypothèses sélectifs. *(Page 258)*
3. **Le châtiment statistique s'applique à l'univers global** — Pour savoir si la meilleure stratégie bat le hasard, le test doit utiliser la distribution de performance de *toutes* les règles ($M$) calculée sur la période de Test. *(Page 318)*

---

## Citation directe

> "The out-of-sample data must look forward into the future, relative to the data used to search for and select the rule. It must be used only once, to obtain an unbiased estimate of the chosen rule's performance." *(Page 258)*

**Signification :** David Aronson insiste sur le fait que les données de validation (*Out-of-Sample*) sont sacrées. Elles ne doivent servir qu'à mesurer froidement le rendement de la règle finale déjà choisie et validée. Y réaliser des tests d'hypothèse après sélection fausse complètement l'analyse statistique à cause du biais accumulé en amont.

---

## Vision macro

Dans l'approche *Evidence-Based Technical Analysis* (EBTA), l'enjeu majeur est de faire la distinction entre une performance liée au talent (un vrai *edge* mathématique) et une performance liée à la chance (le biais de *data mining*).

Si un chercheur effectue son test d'hypothèse sur la période de validation (*Validation / OOS*), il commet une erreur épistémologique grave : il soumet au test une stratégie qui a *déjà* été présélectionnée pour ses bons résultats. Les tests statistiques classiques présupposent que la stratégie a été choisie au hasard ou dictée par une théorie *a priori*. Positionner le test d'hypothèse ajusté (comme le *White's Reality Check*) à la fin de la phase de **Test** permet d'intégrer le coût statistique des $M$ tentatives infructueuses avant de passer au verdict final de l'OOS.

---

## Vision micro

Le fonctionnement rigoureux se décompose selon la chronologie mathématique suivante :

1. **Phase de Train (Entraînement / In-Sample) :** On calibre les paramètres ou on génère l'ensemble des signaux de l'univers des règles candidates ($M$).
2. **Phase de Test (Sélection et Inférence) :**
   * On applique l'ensemble des $M$ règles sur ces données indépendantes.
   * On identifie la règle maximisant la métrique de performance (ex: le rendement moyen $\bar{f}_m$).
   * On applique le test d'hypothèse sur cette règle gagnante. L'hypothèse nulle ($H_0$) stipule que la performance attendue de la meilleure règle au sein de cet univers de $M$ règles est inférieure ou égale à zéro.
   * Le test calcule une *p-value* ajustée (par Bootstrap/Permutations). Si la *p-value* $<\alpha$ (ex: 0.05), la stratégie survit au châtiment statistique.
3. **Phase de Validation (Out-of-Sample) :** On fait tourner l'unique règle validée. Aucune p-value n'est calculée ici : on enregistre simplement le résultat.

---

## Exemples du livre

David Aronson illustre ce protocole lors de son étude empirique à grande échelle sur plus de 6 400 règles de l'analyse technique appliqué à l'indice S&P 500 :

* **Contexte :** L'univers massif de 6 402 règles est appliqué sur les blocs de données historiques.
* **Ce qu'il démontre :** La meilleure règle affichait un rendement initial impressionnant lors de la phase de sélection (Test). Cependant, lorsque le *White's Reality Check* est appliqué à la fin de cette phase (en confrontant cette performance à la distribution des 6 401 autres règles sous l'hypothèse nulle), la *p-value* ajustée grimpe au-dessus de 0,50.
* **Résultat :** Le test d'hypothèse en phase de Test a prouvé que la meilleure stratégie ne battait pas le hasard. La recherche s'arrête là, évitant ainsi de déployer une stratégie perdante en Validation ou en trading réel.

---

## Résumé simplifié

> **TL;DR : C'est dans la phase de TEST.**
> On utilise le **Train** pour créer les stratégies. On utilise le **Test** pour élire la meilleure et appliquer immédiatement le test d'hypothèse (*White's Reality Check*). Si elle réussit le test, elle gagne le droit d'être évaluée une seule et unique fois dans la phase de **Validation (OOS)** qui fait office de juge final neutre.

---

## Actions concrètes

* **Ce qu'il faut faire :** Exécuter votre test d'hypothèse global (WRC / Romano-Wolf / Bootstrap) sur la période de Test en fournissant au script la matrice de performance de *toutes* vos règles alternatives.
* **Ce qu'il faut éviter :** Choisir la meilleure stratégie sur le Test, l'appliquer sur la Validation (OOS), puis faire un simple *t-test* de Student sur la courbe OOS en pensant valider scientifiquement le modèle.
* **Ce qu'il faut mesurer :** La *p-value* ajustée pour le biais de sélection à la fin de la phase de Test.
* **Ce qu'il faut documenter :** Le nombre total $M$ de configurations, variables et indicateurs qui ont été testés tout au long du processus de recherche.

---

## Limites et erreurs fréquentes

### Limites

* Ce passage ne prouve pas qu'une stratégie ayant validé le test d'hypothèse en phase de Test sera obligatoirement rentable en Validation : les conditions de marché peuvent changer (changement de régime).
* La méthode EBTA implique que si vous modifiez vos règles après un échec au test d'hypothèse en phase de Test, vous augmentez artificiellement $M$ et invalidez la puissance du protocole initial.

### Erreurs fréquentes

* **Confondre l'objectif du Test et de la Validation :** Croire que la phase de Validation sert à tester si la stratégie "bat le hasard". Non, elle sert uniquement à mesurer la performance sans biais.
* **Le "Data Snooping" de Validation :** Regarder le résultat sur l'OOS, s'apercevoir qu'il est mauvais, puis revenir à la phase de Test pour ajuster les paramètres. L'OOS est alors contaminé et perd toute valeur scientifique.

---

## À retenir absolument

* Le test d'hypothèse s'effectue obligatoirement à la fin de la phase de **Test**.
* Le test doit prendre en compte l'historique de **toutes les règles essayées** ($M$), pas seulement la gagnante.
* L'échantillon de **Validation (OOS)** est un thermomètre passif, pas un outil de validation statistique.
* Si le test d'hypothèse en phase de Test échoue, le modèle est jeté à la poubelle sans jamais lire les données de Validation.
* Isoler le test d'hypothèse dans le Test protège l'OOS de tout biais de surapprentissage.
