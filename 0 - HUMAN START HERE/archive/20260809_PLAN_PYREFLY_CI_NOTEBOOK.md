# Proposition — Pyrefly CI et notebook

## Intention

Ajouter Pyrefly epingle au workflow CI, avec un interpreteur CI explicite et
Nautilus remplace par `Any`, puis corriger l'appel notebook sans
`package_dir`. Le notebook utilisera un repertoire temporaire pour ne pas
ecraser un package de recherche persistant.

## Journal de convergence de l'intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Pyproject, version locale, workflow et diagnostic notebook verifies. | Pyrefly 1.1.1 ; erreur `package_dir` reproduite ; chemin Windows du config a neutraliser en CI. |
| 2 | Commande CI confrontee aux dependances et au ratchet supply-chain. | jsonschema/numpy/pandas deja installes ; Nautilus seul remplace ; moteur + notebooks controles. Convergence. |
