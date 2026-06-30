# Backlog / File d'attente IA

Ce dossier contient les chantiers tries apres passage par `0 - HUMAN START HERE/` ou apres
audit IA.

## Tracks

- `mainline/` : chantier principal qui fait avancer EBTA.
- `annexes/` : chantier utile mais non bloquant.
- `fixes/` : correction bornee, sans changement de direction.

## Regle de structure obligatoire

Tout chantier doit inclure :

- une checklist Markdown (`- [ ]`, `- [x]`) ;
- `Track` ;
- `Lifecycle` ;
- `Scope` ;
- `Non-goals` ;
- `Source` ;
- `Exit criteria`.

## Cycle de vie

```text
INTAKE -> TRIAGED -> PLANNED -> ACTIVE -> BLOCKED/DONE/REJECTED/SUPERSEDED -> ARCHIVED
```

Un fichier dans `0 - HUMAN START HERE/` est toujours `INTAKE` et non executable.
Un fichier dans `backlog/` n'est executable que si `.ai/checkpoint.json`
le declare explicitement comme `ACTIVE`.

## Flux de travail

1. **Depot humain** : l'humain depose un brouillon dans `0 - HUMAN START HERE/`.
2. **Triage IA** : l'IA audite, classe et deplace vers `mainline/`, `annexes/`
   ou `fixes/`.
3. **Checkpoint** : si le chantier est suivi, l'IA ajoute ou met a jour son
   entree dans `.ai/checkpoint.json`.
4. **Activation** : l'IA extrait une tache realisable vers le cockpit actif du
   composant seulement si le chantier est `ACTIVE`.
5. **Fermeture** : `DONE`, `REJECTED` ou `SUPERSEDED` doivent indiquer une
   raison avant archivage.

**Responsabilite :** ce dossier gere le *quoi*. L'execution reelle, le
*comment*, reste dans le cockpit actif du composant concerne.
