# Epic enfant — Durcissement CI et hygiene Git

## Intention

Le lot 7 du durcissement post-audit contient deux chantiers independants et
ne doit pas etre implemente comme un diff composite :

1. securiser le workflow GitHub Actions versionne ;
2. ajouter une politique `.gitignore` racine minimale.

Ce document coordonne ces deux cycles sans modifier directement `.github/`
ou `.gitignore`. Les reglages GitHub externes, rulesets, secrets et push
protection restent hors autorisation.

## Journal de convergence de l'intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Audit source confronte au workflow et a l'absence de `.gitignore` racine. | Deux sorties independantes detectees ; implementation directe interdite. |
| 2 | Frontieres avec enfants 8-10 et action GitHub externe relues. | Pins/permissions restent en 7A ; chemins, Pyrefly et Ruff restent 8-10 ; settings externes hors scope. |
| 3 | Preuves et ordre examines. | 7A puis 7B minimise les conflits ; chacun aura baseline, tests et fermeture propres. Convergence. |

## Succes

Les deux enfants sont `DONE`, le workflow reste fonctionnel et le depot
ignore mecaniquement les artefacts locaux cibles sans cacher de source utile.
