# Audit adversarial — PLAN_PYREFLY_CI_NOTEBOOK

Date : 2026-08-09

## Verdict

PASS — le gate ne peut pas etre retire ou affaibli silencieusement dans le
contrat CI versionne.

## Scenarios verifies

- Retrait/remplacement de la commande Pyrefly exacte : erreur de contrat.
- Retour a une installation Pyrefly flottante ou retrait du pin : ensemble
  exact des installations en erreur.
- Action, dependance ou commande additionnelle non revue : ensembles exacts
  en erreur.
- Retrait du `package_dir` notebook : test du contenu en erreur et Pyrefly
  retrouve le `missing-argument`.
- Installation de Nautilus dans le workflow : assertion explicite en erreur.

Le gate couvre simultanement `Implementation/ebta_engine` et
`Implementation/notebooks`, surcharge l'interpreteur Windows et ne remplace
que `nautilus_trader.*`.

## Limite honnete

Pyrefly ne detecte pas les verdicts scientifiquement fabriques mais bien les
erreurs de types/imports de son perimetre. Les gardes specialises restent
necessaires.
