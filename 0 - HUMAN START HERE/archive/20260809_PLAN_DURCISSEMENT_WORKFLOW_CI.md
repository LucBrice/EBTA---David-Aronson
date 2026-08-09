# Plan — Durcissement du workflow CI

## Intention

Rendre le workflow GitHub Actions local plus reproductible et moins privilegie
sans ajouter d'outil : permissions `contents: read`, credentials checkout non
persistes, actions sur SHA commente et trois dependances pip exactement
versionnees. Ajouter un test stdlib qui empeche le retour aux tags ou aux
installations flottantes.

## Journal de convergence de l'intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Workflow vivant et audit source relus. | Scope limite aux pins, permissions et ratchet ; commandes unittest/JSON conservees. |
| 2 | Tags verifies par `git ls-remote`, versions Python 3.13 observees localement. | SHA et pins exacts disponibles ; aucune decision externe. |
| 3 | Frontieres 7B/8/9/10 relues. | Aucun gitignore, chemin, Pyrefly ou Ruff dans 7A. Convergence. |

## Succes

Le workflow parse, n'utilise aucun tag mutable couvert, n'installe aucune
dependance directe flottante, expose les permissions minimales et la suite
canonique reste verte.
