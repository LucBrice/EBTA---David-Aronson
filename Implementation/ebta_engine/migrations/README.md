# EBTA Engine Migrations

La version de schema active est `1.1.0` pour le pivot Nautilus.

Les migrations actuelles vivent dans `schema_migrations.py` :

- `migrate_config_1_0_to_1_1()`;
- `migrate_strategy_payload_1_0_to_1_1()`.

Toute migration doit etre :

- deterministe;
- testee;
- journalisee dans `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`;
- sans changement de signification normative.
