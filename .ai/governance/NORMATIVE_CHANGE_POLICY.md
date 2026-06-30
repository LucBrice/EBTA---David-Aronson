# Normative Change Policy

## Principe

Toute modification de `Protocole/` est normative par defaut.

Une modification normative doit etre justifiee par une decision explicite, une
correction de coherence ou une consolidation validee. L'IA ne doit pas modifier
un SOP fige sans raison documentee. L'IA ne doit pas utiliser un SOP non fige
comme autorite contre un SOP fige.

Si les SOP ont une hierarchie numerique ou temporelle, les SOP anterieurs figes
ont priorite sur les SOP posterieurs non valides, sauf decision humaine
explicite documentee.

## Conditions minimales avant modification de `Protocole/`

1. Lire `AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json` et
   `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md`.
2. Lire `Protocole/MANIFESTE DE GEL EBTA.md`.
3. Lire `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md`.
4. Lire `Protocole/MATRICE DE COHERENCE DES SOP EBTA.md`.
5. Identifier les SOP proprietaires et les SOP dependants.
6. Classer le changement : correction documentaire, clarification non
   normative, changement normatif, ou implementation operationnelle.
7. Obtenir une decision humaine explicite si le changement modifie la doctrine.

## Traces obligatoires

Toute modification normative doit indiquer :

- la source du changement ;
- le fichier modifie ;
- la raison ;
- les impacts sur les autres SOP ;
- les impacts possibles sur `Implementation/` ;
- s'il faut mettre a jour le registre de decisions normatives ;
- s'il faut mettre a jour la matrice de coherence ;
- s'il faut mettre a jour le manifeste de gel et l'historique documentaire ;
- s'il faut mettre a jour `Implementation/TRACEABILITY_MATRIX.md`.

## Hierarchie d'autorite proposee

Cette hierarchie doit etre alignee avec les regles deja existantes dans le repo.
Si le repo contient une regle plus precise, la regle plus precise prime.

1. `AGENTS.md` pour le bootstrap IA et les regles globales de navigation.
2. `.ai/checkpoint.json` pour l'etat courant du projet.
3. `Protocole/MANIFESTE DE GEL EBTA.md`, si present, pour les elements geles.
4. `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md`, si present, pour les
   decisions validees.
5. `Protocole/PROTOCOLE EBTA.md` pour la doctrine globale.
6. SOP figes dans `Protocole/`, dans leur ordre logique ou numerique.
7. SOP non figes, uniquement comme brouillons ou candidats.
8. `Implementation/` comme derive executable.
9. `.ai/` comme orchestration et etat IA.
10. `.agents/` et `.codex/` comme adaptateurs ou helpers non normatifs.

## Template de changement normatif

```md
# Normative Change Record

## Change ID
## Date
## Source / demande
## Fichier modifie
## Type de changement
## Justification
## SOP impactes
## Impact implementation
## Conflits verifies
## Decision humaine requise
## Statut
```

