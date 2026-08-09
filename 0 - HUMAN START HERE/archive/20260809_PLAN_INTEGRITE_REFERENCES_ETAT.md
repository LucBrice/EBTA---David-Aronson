# Proposition — Integrite des references d'etat

## Intention

Corriger les deux pointeurs obsoletes qui disposent d'une archive reelle et
ajouter au pre-commit un controle mecanique des chemins portes par le
checkpoint et le tracking.

Le plan RAG rejete et supprime manuellement ne doit pas recevoir un faux
fichier de remplacement : son absence historique reste une exception exacte,
documentee et verifiee contre son ID, son lifecycle et son motif de cloture.

## Journal de convergence de l'intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Toutes les references `*_path` du checkpoint et `active_scope` du tracking confrontees au disque. | Deux pointeurs corrigibles et une absence historique expliquee confirmes. |
| 2 | Schemas, outils de workflow, hook et tests confrontes aux options null/schema/allowlist. | Pas de migration schema : exception exacte fail-closed et stale-checkee ; garde a chaque commit. Convergence. |
