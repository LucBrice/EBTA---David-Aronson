# Audit adversarial — PLAN_CONTRAT_EXIGENCES_GATES_TYPEES

## Verdict

`PASS_ADVERSARIAL` — aucun `FALSE_SUCCESS`, `SILENT_FALLBACK` ou
`NORMATIVE_GAP` residuel dans le perimetre.

## Comportement d'echec attendu

Une valeur qui ne satisfait pas exactement le kind de l'exigence doit etre
rejetee au point d'entree, apparaitre dans `missing`, disparaitre de
`present`, et rendre son gate final `INCONCLUSIVE`. Un kind inconnu doit lever
une erreur explicite.

## Scenarios executes

| Point | Entree hostile | Observation entree et resultat final | Classification |
| --- | --- | --- | --- |
| G10 `economic_report` | `REJECTED_ECONOMIC` | champ `missing`, G10 `INCONCLUSIVE` | `PASS_ADVERSARIAL` |
| G9 `oos_report` | `UNKNOWN` | champ `missing`, G9 `INCONCLUSIVE` | `PASS_ADVERSARIAL` |
| G7 `independent_pre_oos_approval` | `DENIED` | champ `missing`, G7 `INCONCLUSIVE` | `PASS_ADVERSARIAL` |
| G4 `wrc_status` | booleen `True` | champ `missing`, G4 `INCONCLUSIVE` | `PASS_ADVERSARIAL` |
| G0 `config_id` | chaine blanche | champ `missing`, G0 `INCONCLUSIVE` | `PASS_ADVERSARIAL` |
| G13 `live_approval` | entier `1` | champ `missing`, G13 `INCONCLUSIVE` | `PASS_ADVERSARIAL` |
| Evaluateur | kind `unknown` avec valeur `PASS` | `ValueError` explicite | `PASS_ADVERSARIAL` |
| Controle positif | valeurs positives propres aux trois kinds | 15 gates sur 15 `PASS` | `PASS_ADVERSARIAL` |

## Preuve executable durable

Les regressions sont dans
`Implementation/ebta_engine/tests/test_gates.py` : taxonomies negatives et
inconnues, mauvais types, identifiant blanc, alias `True == 1`, kind inconnu,
classification exhaustive et ordre des sorties. La fixture canonique garde
uniquement `live_approval` comme booleen ; tous les pseudo-verdicts sont des
chaines `PASS`.

## Revalidation

- matrice adversariale directe : 7 rejets sur 7 et controle positif 15/15 ;
- tests cibles : 19 tests, `OK` ;
- package minimal : 10 tests, `OK` ;
- suite canonique : 253 tests, `OK`.
