# .codex/

Ce dossier est reserve a **Codex CLI** (OpenAI).

Il ne contient pas de contexte EBTA normatif et ne definit aucune source de
verite projet.

Point d'entree IA officiel du repo :

- `AGENTS.md` a la racine du repo

Le bootstrap racine redirige ensuite vers :

- `.ai/README.md` - regles stables du cockpit IA
- `.ai/checkpoint.json` - etat machine verifiable
- chemins actifs declares dans `.ai/checkpoint.json`

---

*Ce fichier est present uniquement pour eviter toute ambiguite lors du bootstrap
d'un agent Codex.*
