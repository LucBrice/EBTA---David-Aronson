# Proposition — Hygiene `.gitignore` racine

## Intention

Ajouter une politique racine minimale pour les caches Python, environnements
locaux, secrets `.env`, reglages Claude locaux et fichiers temporaires, sans
masquer les sources, les intakes Markdown ni `.vscode/settings.json`.

## Frontiere

Ce lot ne modifie ni le workflow CI, ni les settings GitHub, ni le protocole,
ni les outils Pyrefly/Ruff. La preuve doit utiliser `git check-ignore` et
verifier qu'aucun fichier deja suivi n'est nouvellement ignore.

## Journal de convergence de l'intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Racine et `Implementation/.gitignore` inspectes ; fichiers suivis controles. | Racine absente, trois regles locales existantes, aucun fichier suivi ignore. |
| 2 | Cas positifs et negatifs confrontes aux frontieres des lots 7A/8/9/10. | Lot atomique : un fichier declaratif, un ratchet stdlib et l'inventaire/historique. Convergence. |
