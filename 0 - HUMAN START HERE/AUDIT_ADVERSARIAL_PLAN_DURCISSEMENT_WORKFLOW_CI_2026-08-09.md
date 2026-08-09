# Audit adversarial — PLAN_DURCISSEMENT_WORKFLOW_CI

Date : 2026-08-09

## Verdict

PASS — le contrat local echoue ferme sur les contournements testes.

## Mutations hostiles injectees en memoire

1. Remplacement du SHA checkout par le tag mutable `v4`.
2. Ajout d'une action tierce sur la branche `main`.
3. Remplacement du pin jsonschema par une installation flottante.
4. Elargissement a `contents: write` et restauration des credentials checkout.
5. Affaiblissement de la commande canonique unittest.

Les cinq variantes produisent au moins une erreur de contrat. Le workflow
versionne produit une liste d'erreurs vide.

## Controles complementaires

- Les actions admises sont exactement les deux SHA revus ; une action
  additionnelle echoue.
- Les installations directes sont exactement les trois commandes versionnees ;
  une installation additionnelle echoue.
- Les triggers, le runner, Python 3.13 et les deux validations JSON sont
  conserves.
- Aucune permission d'ecriture, secret, cache, script distant ou setting
  GitHub n'a ete ajoute.

## Limite honnete

Cette preuve couvre le fichier versionne et son ratchet local. Elle ne prouve
ni les settings du depot distant, ni un lock transitif, ni l'absence de
vulnerabilite des dependances ; ces sujets sont explicitement hors scope.
