# Instructions agents EBTA

## Architecture MACRO vs MICRO (Workflow IA)

L'architecture de travail pour les IA est scindee en deux niveaux stricts :
- **MACRO (Le Directeur)** : Le dossier `.ai/` gere l'etat global du projet (`checkpoint.json`, `current_plan.md`) et la file d'attente globale (`.ai/backlog/`). Il ne contient aucun code.
- **MICRO (L'Etabli)** : Les dossiers `Active/` (ex: `Implementation/Active/`) contiennent l'execution technique locale (`HOOK.md`, `tracking.json`).

## Bootstrap obligatoire

Avant toute action substantielle dans ce repo, lire dans cet ordre :

1. **MACRO** : `.ai/current_plan.md` et `.ai/checkpoint.json`.
2. **BACKLOG** : Si une nouvelle tache doit etre initiee, consulter `.ai/backlog/` et extraire un "chunk" realisable.
3. **MICRO** : Lire les fichiers actifs declares dans `.ai/checkpoint.json` (notamment `active_hook_path` et `active_tracking_path`).

Les chemins de hook et de tracking sont des variables operationnelles. Ne jamais
les figer dans `AGENTS.md` comme verite permanente.

## Regles de creation de plans (Epics)

Si une IA doit rediger un nouveau plan d'implementation ou un Epic pour qu'il soit execute plus tard :
1. Le fichier DOIT etre depose dans `.ai/backlog/`.
2. Le fichier DOIT imperativement contenir une checklist Markdown (`- [ ]`) avec les sous-taches a executer.
3. Quand un agent execute un chunk du plan, il coche la case (`- [x]`) correspondante.
4. Quand toutes les cases sont cochees, l'agent deplace le fichier vers `.ai/archive/`.

## Relais multi-IA

Le relais multi-IA s'appuie sur le niveau MACRO :

- `.ai/current_plan.md` (intention humaine/IA)
- `.ai/checkpoint.json` (etat machine)
- `.ai/backlog/` (file d'attente des epics/plans)

Ne pas creer de plans dates, checkpoints dates, copies de reprise ou dossiers
paralleles.

Avant une reponse finale, si l'etat du repo, les validations, les fichiers
touches, les risques ou la prochaine action ont change, mettre a jour ces deux
fichiers par overwrite.

`current_plan.md` porte l'intention et la reprise humaine/IA. `checkpoint.json`
porte l'etat machine verifiable. Ces fichiers ne remplacent pas
`Implementation/Active/tracking.json`, le hook actif, l'historique runtime ni
`Protocole/`.

Quand le hook actif ou son JSON de suivi changent, mettre a jour les champs
`active_hook_path` et `active_tracking_path` dans `.ai/checkpoint.json`, puis
ajuster le resume humain dans `.ai/current_plan.md`.

## Autorite EBTA

`Protocole/` reste l'autorite normative. `Implementation/` est une traduction
executable subordonnee. Toute divergence entre les deux rend
`Implementation/` fautif jusqu'a correction ou clarification documentaire.

Ne pas modifier BACKTRADER avant lecture de sa gouvernance locale et sans
demande explicite.
