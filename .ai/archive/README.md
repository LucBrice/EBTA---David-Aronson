# Archives IA

Ce dossier conserve les chantiers clotures.

## Regle de routage

`Archives/` a la racine n'est plus une destination active d'archivage.
Les archives restent reparties par autorite :

- `.ai/archive/` conserve les chantiers IA clotures ;
- `Protocole/Archives/` conserve les archives documentaires du protocole ;
- `Implementation/Archives/` est une archive legacy fermee, a ne plus alimenter.

Pour les nouveaux chantiers non normatifs, archiver ici plutot que dans un
dossier central racine.

Un fichier peut etre archive si son cycle de vie est :

- `DONE` : termine avec criteres de sortie satisfaits ;
- `REJECTED` : refuse apres audit ;
- `SUPERSEDED` : remplace par un autre chantier ;
- `ARCHIVED` : historique pur.

Chaque archivage doit conserver la raison de fermeture dans le fichier ou dans
`.ai/checkpoint.json` si le chantier etait suivi par l'etat machine.

Ne pas deplacer une source active citee par `Protocole/` ou `Implementation/`.
Journaliser les deplacements significatifs dans l'historique approprie.

Les fichiers ici sont en lecture seule par convention.
