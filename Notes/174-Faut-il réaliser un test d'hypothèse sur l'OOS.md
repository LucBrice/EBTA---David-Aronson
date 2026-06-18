# Faut-il réaliser un test d'hypothèse sur l'OOS ?

C'est une question cruciale qui touche au cœur de la rigueur scientifique dans l'EBTA.

Pour répondre directement : **non, vous ne devez pas réaliser de test d'hypothèse**, au sens de calcul de **p-value**, sur l'ensemble **OOS**.

Voici pourquoi, selon l'approche de David Aronson, cette pratique est à la fois inutile statistiquement et dangereuse pour la validité de votre modèle.

---

## Référence

- **Thème :** La distinction entre preuve statistique — **Test** — et validation empirique — **OOS**.
- **Source :** *Evidence-Based Technical Analysis* de David Aronson, chapitres 3, 4 et 6.

---

## Idées clés

1. **L'OOS est une validation d'un seul échantillon.**

   Le test d'hypothèse, comme le **White's Reality Check**, nécessite de prendre en compte **l'ensemble des règles candidates** testées initialement.

   L'**OOS**, lui, ne contient qu'une seule règle : la gagnante.

   Tester cette règle isolément sur l'**OOS** n'a plus de sens statistique, car le biais de **data mining** a déjà été consommé.

2. **L'OOS confirme la robustesse, il ne la prouve pas.**

   Si vous testez une hypothèse sur l'**OOS**, vous faites une erreur logique.

   Vous essayez de prouver la validité d'une règle avec les mêmes données que celles que vous utilisez pour évaluer sa performance future.

3. **Le risque de contamination est majeur.**

   Effectuer des tests de significativité sur l'**OOS** transforme cet échantillon en jeu de données de test supplémentaire.

   Vous perdez alors votre zone vierge pour le futur.

---

## Citation directe

> “The holdout (out-of-sample) data is used to provide an unbiased estimate of the performance of the rule/signal that has been discovered.”  
> *(Page 530)*

**Explication :** Aronson insiste sur le terme **estimation**.

L'**OOS** est un miroir qui vous montre la réalité.

Si le résultat vous déplaît, vous ne pouvez pas faire un test d'hypothèse pour essayer de le sauver.

Vous devez accepter que votre règle n'est pas robuste.

---

## Vision macro

L'enjeu est de ne pas confondre deux choses :

- **L'inférence statistique :** savoir si un phénomène existe.
- **L'évaluation de performance :** savoir quelle sera la rentabilité future probable.

Le **test d'hypothèse**, effectué sur le **Test**, est votre filtre de sécurité.

Il élimine le bruit.

L'**OOS** est votre test en situation réelle.

Il mesure l'efficacité.

> Si vous demandez à l'OOS de « battre le hasard », vous lui demandez de faire le travail du Test.

Mais l'**OOS** n'est pas armé pour cela.

Il n'a pas la puissance statistique requise, car il ignore tout le processus de recherche effectué en amont.

---

## Vision micro

Voici pourquoi un test statistique sur l'**OOS** est statistiquement faible.

### 1. Taille d'échantillon

Un test de robustesse statistique, comme le **White's Reality Check**, demande de comparer des milliers de stratégies pour ajuster la **p-value**.

Faire cela sur un seul échantillon **OOS**, avec une seule règle, est mathématiquement invalide.

### 2. Le paradoxe du test

Si vous trouvez que votre règle « bat le hasard » en **OOS** avec une **p-value** de $0{,}05$, c'est peut-être simplement parce que vous avez eu de la chance sur cet échantillon spécifique.

Sans la comparaison avec l'univers complet des règles testées initialement, cette **p-value** ne signifie rien.

---

## Résumé simplifié

Imaginez que vous passiez un examen de mathématiques : c'est le **Test**.

Vous passez 100 exercices, et si vous réussissez statistiquement l'examen global, vous avez votre diplôme.

L'**OOS**, c'est votre premier jour de travail réel.

Vous ne repassez pas l'examen de mathématiques au travail.

Vous appliquez simplement ce que vous avez appris.

Si vous échouez au travail, ce n'est pas parce que vous n'avez pas réussi « le test » du travail.

C'est parce que votre diplôme — votre stratégie — ne correspond pas aux exigences réelles.

> On ne justifie pas le succès au travail par un test de p-value. On le mesure par la productivité.

---

## Actions concrètes

- **Ce qu'il faut faire :** effectuer tout le châtiment statistique sur le segment **Test**.
- **Ce qu'il faut observer en OOS :** le rendement, le **drawdown** et la stabilité.
- **Ce qu'il faut comparer :** vérifier si la performance **OOS** est en ligne avec les attentes calculées lors du **Test**.

C'est un test de **cohérence**, pas un test de **significativité**.

---

## Limites et erreurs fréquentes

### Limites

L'**OOS** est une estimation, pas une vérité absolue.

Il est sujet à la variance propre aux marchés financiers.

### Erreurs fréquentes

- **Vouloir réparer :** si l'**OOS** est mauvais, l'erreur classique est de revenir en arrière pour ajuster les paramètres afin que l'**OOS** devienne bon.

  Cela s'appelle du **data snooping** et détruit la valeur de votre modèle.

- **Confondre validation statistique et observation :** croire qu'un test de **p-value** sur l'**OOS** rendrait la stratégie plus solide.

  Au contraire, cela donne une fausse confiance basée sur une manipulation statistique invalide.

---

## À retenir absolument

1. Le test d'hypothèse pour éliminer la chance se fait en amont, dans le **Test**.
2. L'**OOS** est un thermomètre, pas un tribunal.
3. Si la performance en **OOS** ne bat pas le hasard, c'est que votre stratégie n'a pas survécu au monde réel.
4. Aucun test statistique sur l'**OOS** ne pourra transformer une mauvaise stratégie en bonne stratégie.
5. La confiance en votre stratégie vient de la correction statistique effectuée sur le **Test** et de la stabilité observée en **OOS**.
