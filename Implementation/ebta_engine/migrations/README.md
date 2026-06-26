# EBTA Engine Migrations

La version de schema active est `1.0.0` pour `EBTA-ENGINE-0.1.0`.

Aucune migration n'est requise tant qu'aucun artefact persistant cree sous une
ancienne version supportee ne doit etre lu ou transforme. Toute future migration
doit etre:

- deterministe;
- testee;
- journalisee dans `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`;
- sans changement de signification normative.
