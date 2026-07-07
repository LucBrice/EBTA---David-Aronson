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

Pour tout nouveau plan d'implementation, partir du gabarit
[`TEMPLATE_PLAN_IMPLEMENTATION.md`](TEMPLATE_PLAN_IMPLEMENTATION.md). Il couvre
la structure minimale ci-dessus et y ajoute les sections qui permettent a
n'importe quelle IA de codage de reprendre le chantier a froid sans contexte
implicite : bandeau de statut face a l'etat machine courant, lecture
obligatoire, table des gates du pipeline, etat des lieux "reutiliser avant de
recreer", decision d'architecture, decoupage en phases de deblocage puis
d'implementation, invariants non negociables + liste NO GO, journal de
decisions humaines, Definition of Done et journal d'audits post-hoc. Ce
gabarit est lui-meme derive de deux chantiers reels du depot (un plan execute
avec succes et un audit d'architecture qui a evite une duplication de code
deja existant) — voir l'en-tete du fichier pour le detail. C'est un gabarit,
pas un chantier — il ne doit jamais etre active tel quel via `plan.ps1`.

## Cycle de vie

```text
INTAKE -> TRIAGED -> PLANNED -> ACTIVE -> BLOCKED/DONE/REJECTED/SUPERSEDED -> ARCHIVED
```

Un fichier dans `0 - HUMAN START HERE/` est toujours `INTAKE` et non executable.
Un fichier dans `backlog/` n'est executable que si `.ai/checkpoint.json`
le declare explicitement comme `ACTIVE`.

## Flux de travail

1. **Depot humain** : l'humain depose un brouillon dans `0 - HUMAN START HERE/`.
2. **Triage IA** : l'IA audite le brouillon, puis ECRIT UN NOUVEAU FICHIER
   integralement restructure selon le gabarit dans `mainline/`, `annexes/` ou
   `fixes/`. Le brouillon original n'est jamais reecrit ni edite en place :
   `plan.ps1 start` le deplace tel quel vers
   `0 - HUMAN START HERE/archive/` pour tracabilite (voir
   `original_draft_path` dans `.ai/checkpoint.json`).
3. **Checkpoint** : si le chantier est suivi, l'IA ajoute ou met a jour son
   entree dans `.ai/checkpoint.json`.
4. **Activation** : l'IA extrait une tache realisable vers le cockpit actif du
   composant seulement si le chantier est `ACTIVE`.
5. **Fermeture** : `DONE`, `REJECTED` ou `SUPERSEDED` doivent indiquer une
   raison avant archivage.

**Responsabilite :** ce dossier gere le *quoi*. L'execution reelle, le
*comment*, reste dans le cockpit actif du composant concerne.
