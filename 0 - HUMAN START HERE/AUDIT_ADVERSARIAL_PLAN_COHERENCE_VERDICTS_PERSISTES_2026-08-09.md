# Audit adversarial — Coherence des verdicts persistes

## Verdict

`PASS_ADVERSARIAL` — aucun `FALSE_SUCCESS`, `SILENT_FALLBACK` ou
`NORMATIVE_GAP` residuel dans le diff du chantier.

## Matrice

| Point | Entree hostile | Attendu | Observation | Classe |
| --- | --- | --- | --- | --- |
| Helper de copie | Statuts absents/non textuels | Aucune valeur positive inventee | Les trois copies deviennent `INCONCLUSIVE` | `EXPECTED_DEFAULT` |
| Helper de copie | `FAIL` / `REJECTED_ECONOMIC` | Conservation exacte | Valeurs conservees sans coercition | `PASS_ADVERSARIAL` |
| INV-010 | final `PASS`, composant rejete | Refus interne | INV-010 `FAIL` nomme | `PASS_ADVERSARIAL` |
| INV-010 | composants `PASS`, final non-PASS | Refus interne | INV-010 `FAIL` nomme | `PASS_ADVERSARIAL` |
| INV-010 | composants inverses/incomplets | Refus structurel | INV-010 `FAIL` | `PASS_ADVERSARIAL` |
| Package | Copie statistical/economic/final mutee | Package bloque et mismatch nomme | `semantic_errors` cible le champ, status `FAIL` | `PASS_ADVERSARIAL` |
| Package | WRC `PASS`, economic statistical `FAIL` | Divergence bloquante | Mismatch WRC/economic nomme, status `FAIL` | `PASS_ADVERSARIAL` |
| Pipeline | `capacity_pass=False` | Rejet propage, jamais `PASS` | economic/final `REJECTED_ECONOMIC`, copie identique, package `FAIL` | `PASS_ADVERSARIAL` |
| Pre-OOS refuse | Rapport economique absent | Absence visible | Helper unique persiste economic/final `INCONCLUSIVE` | `EXPECTED_DEFAULT` |

## Preuves executables

- `test_persisted_gate_reports_preserve_owner_values_and_fail_closed_on_absence` ;
- trois contrastes INV-010 ;
- mutations des trois copies persistees ;
- divergence WRC/economic ;
- pipeline economique rejete bout en bout ;
- inventaire canonique et suite complete : 266 tests `OK` ;
- recherche du literal positif historique dans le sink : aucune occurrence.

Le validateur observe les artefacts et produit des erreurs ; il ne les repare
jamais. Le fallback `INCONCLUSIVE` est limite a l'absence de verdict et ne
peut donc pas fabriquer un succes.
