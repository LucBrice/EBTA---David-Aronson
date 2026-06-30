# Conflict Resolution Policy

## Principe

L'IA ne doit pas resoudre silencieusement un conflit normatif. Elle doit rendre
le conflit visible, le classifier, proposer des options, puis attendre une
decision humaine si la resolution modifie la doctrine EBTA.

Documenter un conflit n'est pas le resoudre. Une option recommandee par l'IA
reste une proposition tant qu'elle touche au protocole, aux SOP, aux gates, aux
statuts ou aux seuils EBTA.

## Perimetres couverts

Cette politique couvre les conflits entre :

- deux sources theoriques ;
- une source theorique et le protocole ;
- deux SOP ;
- un SOP et l'implementation ;
- le checkpoint et l'etat reel du repo ;
- une note utilisateur et une decision normative anterieure.

## Classification

- `MINOR_INCONSISTENCY` : incoherence de vocabulaire ou formulation.
- `STRUCTURAL_CONFLICT` : conflit d'organisation ou de responsabilite entre
  fichiers.
- `METHODOLOGICAL_CONFLICT` : conflit sur une regle scientifique ou statistique.
- `IMPLEMENTATION_DRIFT` : le code ne reflete plus le protocole.
- `AUTHORITY_CONFLICT` : deux fichiers pretendent avoir autorite sur le meme
  sujet.
- `STALE_STATE` : checkpoint ou backlog obsolete par rapport au repo.

## Regles de resolution

1. Decrire le conflit de facon neutre.
2. Identifier l'autorite actuelle selon `AGENTS.md`, `.ai/checkpoint.json` et
   `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md`.
3. Si le conflit est executable seulement, corriger `Implementation/` pour le
   réaligner avec `Protocole/`, ou ouvrir une demande normative si le protocole
   est insuffisant.
4. Si le conflit est normatif, ne pas modifier `Protocole/` sans decision
   humaine explicite.
5. Si le checkpoint ou le backlog est stale, verifier l'etat reel du repo avant
   de mettre a jour `.ai/checkpoint.json`.
6. Tracer les decisions dans les registres existants quand la resolution est
   appliquee.

## Template

```md
# Conflict Report

## Conflict ID
## Type
## Fichiers / sources concernes
## Description neutre du conflit
## Autorite actuelle selon le repo
## Risque si non resolu
## Options possibles
## Recommandation IA
## Decision humaine requise ?
## Statut
```

