# Justification de la performance en OOS : le rôle du test d'hypothèse

## Référence

- **Thème :** Rôle respectif du **Test** — statistique — et de l'**OOS** — validation — dans le protocole EBTA.
- **Source :** *Evidence-Based Technical Analysis* de David Aronson, notamment les chapitres 3, 4 et 6.

---

## Idées clés

1. **Le test d'hypothèse précède l'OOS.**

   La justification que la performance n'est pas due à la chance — le « châtiment statistique » — se fait impérativement lors de l'étape de **Test**, et non pendant l'**OOS**.

2. **L'OOS n'est pas un juge statistique.**

   Il sert à mesurer la performance réelle, hors échantillon, d'une règle déjà « certifiée » par les tests statistiques précédents.

3. **La chance est éliminée en amont.**

   Si une règle échoue aux tests statistiques sur l'ensemble de **Test**, elle ne doit jamais atteindre l'étape **OOS**.

4. **L'OOS est une mesure, pas un test.**

   L'**OOS** permet de voir si la performance se maintient, mais on ne peut plus rejeter l'hypothèse nulle $H_0$ sur ces données sans les contaminer.

---

## Citation directe

> “The only way to determine which of these numerous hypotheses might be correct is for predictions to be made that are then compared with new observations.”  
> *(Page 10, note 8)*

**Explication :** Aronson insiste sur le fait que la validité d'une règle repose sur sa capacité à réaliser des prédictions sur des données nouvelles.

Le test d'hypothèse est l'outil qui permet de quantifier si cette performance est le fruit de la structure du marché ou d'une simple coïncidence statistique.

---

## Vision macro

L'approche EBTA sépare deux besoins distincts :

- **La preuve :** est-ce que ma stratégie a une valeur réelle ?
- **L'estimation :** quelle sera sa performance probable en conditions réelles ?

Le test d'hypothèse sur l'ensemble de **Test** répond au besoin de **preuve**.

L'utilisation de l'**OOS** répond au besoin d'**estimation**.

> Si vous confondez les deux, vous utilisez l'OOS pour « valider » trop tard, ou vous faites vos tests statistiques sur l'OOS, ce qui le rend invalide pour toute utilisation future.

---

## Vision micro

Concrètement, voici comment on traite la chance.

### 1. Dans le Test

On utilise des algorithmes intensifs, par exemple le **White's Reality Check**, qui comparent la performance de votre meilleure règle à la distribution des résultats de **toutes** les règles testées pendant la phase de **Train**.

Si la **p-value** est inférieure au seuil choisi, par exemple $0{,}05$, on rejette $H_0$.

On obtient alors une preuve statistique que la performance observée n'est probablement pas uniquement due à la chance.

### 2. Dans l'OOS

On ne teste plus rien statistiquement.

On observe simplement le **drawdown**, le **Sharpe ratio**, le rendement annuel ou d'autres métriques de performance.

Si ces chiffres sont proches de ceux obtenus dans le **Test**, on obtient une confirmation de **stabilité**.

Si la performance s'effondre, cela signifie que la stratégie était probablement surapprise — **overfitting** — ou que le régime de marché a changé.

Mais on ne peut plus « justifier » statistiquement la chance à ce stade.

---

## Exemples du livre

Le livre souligne que beaucoup de traders prennent leurs résultats de **backtest** optimisés, c'est-à-dire ceux du **Train**, et les présentent comme des preuves de succès.

Aronson montre, via des simulations de **Monte Carlo**, que ce comportement est une erreur.

En testant assez de règles, on finit toujours par trouver une combinaison « gagnante » par pur hasard.

L'exemple central est celui de la sélection de règles : sans test statistique avant l'**OOS**, le trader ne fait que sélectionner le bruit statistique.

---

## Résumé simplifié

On ne justifie pas la chance en **OOS**.

On le fait **avant**, dans la phase de **Test**.

- **Phase de Test :** c'est le tribunal statistique. On vérifie si la stratégie bat le hasard. Si elle gagne ici, elle a le droit de passer à l'étape suivante.
- **Phase OOS :** c'est la mise en situation réelle. On ne cherche plus à prouver quoi que ce soit, on mesure simplement comment la stratégie survit au monde réel.

> Si vous attendez l'OOS pour vérifier si c'était de la chance, il est trop tard : les données sont déjà consommées.

---

## Actions concrètes

- **Ce qu'il faut faire :** effectuer les tests de robustesse statistique uniquement sur le segment de données dédié, c'est-à-dire le **Test**.
- **Ce qu'il faut éviter :** utiliser l'**OOS** pour effectuer des tests de significativité ou pour itérer sur la stratégie.
- **Ce qu'il faut mesurer :** la **p-value** globale sur le **Test** avant même de regarder l'**OOS**.
- **Ce qu'il faut documenter :** la procédure complète utilisée sur le **Test** pour prouver l'absence de biais de **data mining**.

---

## Limites et erreurs fréquentes

### Limites

L'**OOS** ne peut pas valider une stratégie qui a échoué aux tests de significativité statistique en amont.

### Erreurs fréquentes

- **L'illusion de validation :** croire qu'un résultat positif en **OOS** suffit à prouver l'absence de chance.

  Un résultat positif en **OOS** peut très bien être le fruit de la chance si le modèle a été sélectionné parmi des milliers d'autres règles sans correction statistique préalable.

- **Contamination :** faire des ajustements sur la règle après avoir vu les résultats **OOS**.

  Une fois vu, l'**OOS** est « brûlé ».

---

## À retenir absolument

1. La justification statistique de la chance se fait dans le **Test**, pas dans l'**OOS**.
2. L'**OOS** sert à mesurer la performance, pas à prouver la validité scientifique.
3. Si une règle n'est pas statistiquement robuste en phase de **Test**, elle est inutilisable.
4. L'**OOS** doit rester une boîte noire vierge jusqu'au test final.
5. Une fois que vous avez regardé l'**OOS**, vous ne pouvez plus l'utiliser pour justifier ou modifier quoi que ce soit.
