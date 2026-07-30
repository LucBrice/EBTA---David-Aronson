# Brouillon — template JSON de preuve de session IA

## Objectif

Créer `.ai/governance/TEMPLATE_PREUVE_SESSION_IA.json`, un exemple JSON valide
et copiable pour relier les affirmations d'une session aux commandes et
artefacts qui les prouvent.

Champs minimaux issus de la veille #2 :

- `task_id`;
- `objective`;
- `tests_executed`;
- `claims`;
- `evidence`.

Le template complète le contrat de commit existant avec :

- `files_modified`;
- `files_not_touched`;
- `risks_remaining`;
- `decisions_required`.

Il porte un marqueur `template_only: true` et des placeholders `<...>`. Une
session réelle doit copier le modèle vers un emplacement décidé par son propre
plan ; elle ne modifie jamais le template et ne peut pas le citer comme preuve.

Chaque `claim` référence un ou plusieurs `evidence_id`. Chaque test porte sa
commande, son résultat réel et son statut fermé `PASS|FAIL|SKIP|NOT_RUN`. Une
preuve porte un type, un chemin/référence et la méthode de vérification.

## Portée

- créer le template JSON ;
- le référencer et documenter ses limites dans `.ai/governance/README.md`.

Hors portée : créer un registre de sessions, un schéma JSON, un validateur, un
gate de clôture, modifier le format de commit, ou stocker une preuve réelle dans
le template.

## Validation

- `python -m json.tool` passe ;
- aucune valeur exemple ne ressemble à une attestation réelle ;
- le README dit explicitement que le template est optionnel et non validé
  mécaniquement ;
- les IDs de preuve utilisés par les claims existent dans l'exemple ;
- les statuts de test du modèle appartiennent au vocabulaire fermé, vérifié par
  une commande ponctuelle de ce chantier sans prétendre créer un validateur
  permanent ;
- `git diff --check`.

## Journal `/evaluate`

| Passe | Résultat |
| --- | --- |
| 1 | Risque de fausse attestation corrigé : marqueur `template_only`, placeholders visibles et interdiction d'utiliser le fichier modèle comme preuve. |
| 2 | Convergence : cohérence claims/evidence et vocabulaire des tests rendus vérifiables par commande ponctuelle ; schéma, registre et gate restent hors scope. |
