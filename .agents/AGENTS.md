# Instructions agents EBTA - compatibilite

Ce fichier est conserve pour compatibilite avec d'anciens agents.
Il n'est plus une source d'etat projet.

## Source active

Le point d'entree officiel reste `AGENTS.md` a la racine du repo.
Le cockpit IA actif est `.ai/`.

Avant toute action substantielle, lire :

1. `AGENTS.md`
2. `.ai/README.md`
3. `.ai/checkpoint.json`
4. les chemins actifs declares dans `.ai/checkpoint.json`
5. `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md` si la
   tache touche au protocole, a la methode EBTA ou aux decisions normatives.

## Role residuel de `.agents/`

`.agents/` peut contenir de l'outillage, des skills ou de l'historique.
Il ne doit pas porter de plan actif, checkpoint courant ou source d'autorite
projet.

## Regle de creation de plans

Les brouillons humains entrent dans `0 - HUMAN START HERE/`.
L'IA les audite, les classe, puis les deplace dans :

- `.ai/backlog/mainline/`
- `.ai/backlog/annexes/`
- `.ai/backlog/fixes/`

L'etat macro machine-readable est dans `.ai/checkpoint.json`.
L'etat micro runtime reste dans `Implementation/Active/`.
