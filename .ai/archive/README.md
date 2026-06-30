# Archives IA

Ce dossier conserve les chantiers clotures.

Un fichier peut etre archive si son cycle de vie est :

- `DONE` : termine avec criteres de sortie satisfaits ;
- `REJECTED` : refuse apres audit ;
- `SUPERSEDED` : remplace par un autre chantier ;
- `ARCHIVED` : historique pur.

Chaque archivage doit conserver la raison de fermeture dans le fichier ou dans
`.ai/checkpoint.json` si le chantier etait suivi par l'etat machine.

Les fichiers ici sont en lecture seule par convention.
