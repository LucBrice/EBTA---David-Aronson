# Proposition — Ruff CI cible bugs

## Intention

Ajouter Ruff 0.16.2 au runner avec le seul ruleset `F,E9,B,PLE,RUF`, puis
resoudre les 25 findings vivants apres classification manuelle. Aucun
`--select ALL`, formatage ou auto-fix aveugle.

## Journal de convergence de l'intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Ruff 0.16.2 execute sur `Implementation/ebta_engine`. | 25 findings : B905x10, F401x7, RUF046x3, B009x2, B007/RUF012/RUF059 x1. |
| 2 | Chaque contexte relu et invariants de longueurs verifies. | Corrections locales determinees ; zero ignore/per-file exemption requis. Convergence. |
