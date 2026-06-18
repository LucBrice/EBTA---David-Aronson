# Le rôle de l’OOS : estimation et stabilité dans l’EBTA

## Référence

- **Thème :** Rôle de l'ensemble de validation **OOS** dans l'architecture EBTA.
- **Source :** *Evidence-Based Technical Analysis* de David Aronson, chapitres 3 et 6.

---

## Idées clés

1. **L'OOS est une mesure de performance réelle.**

   Il sert à obtenir une estimation **non biaisée** de ce que la règle aurait produit si elle avait été déployée en temps réel.  
   *(Page 530)*

2. **L'OOS n'est pas un lieu de test statistique.**

   On ne cherche plus à prouver que la règle « bat le hasard » — cela a été fait avant — mais à observer si les performances réelles sont cohérentes avec celles attendues.

3. **L'intervalle de confiance est une clé de lecture.**

   En comparant la performance du **Test** à celle de l'**OOS**, on évalue la **stabilité** de la stratégie.

4. **La dégradation est le signal majeur.**

   Si la performance s'effondre en **OOS**, cela indique une erreur de **data mining** ou de **surapprentissage** — **overfitting** — dans la phase de recherche.

---

## Citation directe

> “Out-of-sample data refers to data not used for back testing the rule.”  
> *(Page 523, note 9)*

**Explication :** David Aronson définit l'**OOS** comme un compartiment étanche.

Toute donnée utilisée pour choisir la règle est, par définition, du **in-sample**.

L'**OOS** est donc tout ce qui reste après, permettant une lecture honnête de la réalité future probable.

---

## Vision macro

L'EBTA repose sur une hiérarchie de la preuve.

L'**OOS** est le thermomètre : il ne dit pas si le patient est en bonne santé — c'est le rôle des tests statistiques de **Test** — il mesure simplement sa température à un instant donné.

Si la température est normale en **OOS**, vous avez une **estimation** valide.

Si elle est anormalement basse, vous avez la preuve que votre diagnostic précédent — **Test** — était erroné ou que le marché a fondamentalement changé.

---

## Vision micro

### 1. L'estimation non biaisée

Le **Train** et le **Test** sont pollués par le processus de sélection, car on a essayé des milliers de règles.

Le résultat observé en **Test** est donc encore potentiellement optimiste.

L'**OOS**, n'ayant jamais été vu par l'algorithme de sélection, fournit une lecture brute, sans l'effet d'aubaine du **data mining**.

### 2. Le rôle de l'intervalle de confiance

Aronson suggère que l'on doit observer la **distribution** de la performance.

Si la performance en **OOS** tombe en dehors de l'**intervalle de confiance** calculé lors de la phase de **Test**, vous avez un signal d'alerte immédiat.

- **Signification :** la règle n'est pas robuste.
- **Conséquence :** le modèle doit être rejeté, même si le **Train** était brillant.

---

## Exemples du livre

Aronson mentionne que la détérioration de la performance d'un système technique en **OOS** est un phénomène documenté, notamment dans l'idée suivante : *Why Have Returns to Technical Analysis Decreased?*

Il souligne que si une performance chute en **OOS**, on ne peut pas simplement l'attribuer à la malchance.

On doit plutôt l'interpréter comme l'incapacité de la règle à généraliser son avantage hors de son environnement d'entraînement.

---

## Résumé simplifié

L'**OOS** n'est pas un outil de décision.

C'est un outil d'observation.

- **Estimation :** vous regardez le rendement moyen, par exemple le **Sharpe Ratio**, sur ces données vierges. C'est votre prévision réaliste.
- **Intervalle de confiance :** vous vérifiez si cette performance est normale par rapport à ce que vos tests statistiques, par exemple le **WRC**, avaient prédit.
- **Action :** si la performance **OOS** est radicalement différente des attentes statistiques, vous arrêtez tout. Vous ne modifiez rien, vous constatez l'échec de la robustesse.

---

## Actions concrètes

- **Ce qu'il faut faire :** garder l'**OOS** hermétiquement scellé jusqu'à la fin.
- **Ce qu'il faut éviter :** utiliser l'**OOS** pour « valider » une règle par un test de **p-value**, car les données sont trop peu nombreuses et déjà consommées intellectuellement dès qu'elles sont regardées.
- **Ce qu'il faut mesurer :** le différentiel de performance entre le **Test** et l'**OOS**.
- **Ce qu'il faut documenter :** l'estimation du rendement attendu basée sur l'**OOS**, pour comparer avec les résultats réels une fois en production.

---

## Limites et erreurs fréquentes

### Limites

L'**OOS** n'est qu'une estimation basée sur un échantillon limité.

Il ne garantit pas la pérennité de l'**edge**.

### Erreurs fréquentes

- **L'erreur de re-validation :** tenter d'utiliser l'**OOS** pour calculer une nouvelle **p-value**.

  C'est une erreur de **data snooping**, car vous utilisez les données pour valider une hypothèse qu'elles ont potentiellement générée si vous avez déjà regardé le résultat.

- **Confondre OOS et Training :** penser que l'on peut itérer pour « serrer » l'intervalle de confiance en **OOS**.

---

## À retenir absolument

1. L'**OOS** mesure la robustesse, il ne la crée pas.
2. Une performance **OOS** significativement inférieure au **Test** signale un surapprentissage.
3. L'**intervalle de confiance** sert à détecter si la performance observée en **OOS** est une anomalie statistique.
4. Si vous modifiez vos paramètres après avoir vu l'**OOS**, vous détruisez toute valeur scientifique.
5. L'EBTA cherche la stabilité de l'estimation, pas la maximisation du profit.
