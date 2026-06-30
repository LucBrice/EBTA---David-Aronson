# 0 - HUMAN START HERE

Ce dossier est le point d'entree brut pour les idees, demandes, plans et notes
de l'humain.

## Regles

- Tout contenu ici est `INTAKE`.
- Rien ici n'est executable directement.
- L'humain peut deposer un brouillon non structure.
- L'IA lit, audite, structure si besoin, classe et deplace le fichier vers le
  backlog adapte.
- Le deplacement doit etre trace dans `.ai/checkpoint.json` si le chantier
  devient suivi par l'etat machine.

## Commande humaine

Pour demander l'audit et la promotion d'un brouillon, taper dans l'IA :

```text
/start "0 - HUMAN START HERE/NOM_DU_PLAN.md"
```

L'IA doit alors transformer le brouillon en plan conforme avant d'appeler le
backend `.ai/tools/plan.ps1`.

## Sorties possibles

- `.ai/backlog/mainline/` pour le chantier principal.
- `.ai/backlog/annexes/` pour les chantiers utiles mais non bloquants.
- `.ai/backlog/fixes/` pour les corrections bornees.
- `.ai/archive/` pour un brouillon rejete, remplace ou cloture.
