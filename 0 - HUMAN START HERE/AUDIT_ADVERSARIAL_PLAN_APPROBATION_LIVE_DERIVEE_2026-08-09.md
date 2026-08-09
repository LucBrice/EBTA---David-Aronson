# Audit adversarial — PLAN_APPROBATION_LIVE_DERIVEE

## Verdict

`PASS_ADVERSARIAL` — aucun faux succes ou repli silencieux residuel.

## Scenarios executes

| Point | Entree hostile | Entree rejetee | Resultat final | Classe |
| --- | --- | --- | --- | --- |
| Verdict live | `FAIL` | status live non-PASS | deployment `FAIL` | `PASS_ADVERSARIAL` |
| Verdict live | `INCONCLUSIVE` | status live non-PASS | deployment `FAIL` | `PASS_ADVERSARIAL` |
| Verdict live | `WATCH` | status live non-PASS | deployment `FAIL` | `PASS_ADVERSARIAL` |
| Verdict live | `SUSPENDED` | status live non-PASS | deployment `FAIL` | `PASS_ADVERSARIAL` |
| Verdict live | `UNKNOWN` | violation explicite | deployment `FAIL` | `PASS_ADVERSARIAL` |
| Approbation | absente | `INCONCLUSIVE` | deployment `FAIL` | `PASS_ADVERSARIAL` |
| Approbation | mauvais sujet | `subject_id_mismatch` | deployment `FAIL` | `PASS_ADVERSARIAL` |
| Approbation | fixture non autorisee | `test_fixture_not_authorized` | deployment `FAIL` | `PASS_ADVERSARIAL` |
| Approbation | `REJECTED` | `FAIL` | deployment `FAIL` | `PASS_ADVERSARIAL` |
| Controle positif | preuve `EXTERNAL` exacte + verdict `PASS` | deux statuts `PASS` | deployment `PASS` | `PASS_ADVERSARIAL` |

Les tests bout en bout fournissent d'abord un pre-OOS valide, puis prouvent
que verdict live `FAIL` ou preuve absente rendent G13 non-PASS. La recherche
cible retourne zero `live_approval: True` dans le Python de production.

## Revalidation

Matrice directe 10/10, tests cibles verts, suite canonique 259 tests `OK`.
