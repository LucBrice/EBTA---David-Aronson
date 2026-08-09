# Audit adversarial — Garde AST des litteraux de verdict

## Verdict

`PASS_ADVERSARIAL` — aucun `FALSE_SUCCESS`, `SILENT_FALLBACK` ou
`NORMATIVE_GAP` residuel.

## Matrice

| Point | Entree hostile | Attendu | Observation | Classe |
| --- | --- | --- | --- | --- |
| Sink persiste | `atomic_write_json(..., {"economic_report": "PASS"})` | Nouvelle occurrence bloquee | `unapproved` contient le sink et status `FAIL` | `PASS_ADVERSARIAL` |
| Baseline | Empreinte supprimee du code mais conservee | Exception morte bloquee | `stale` non vide, status `FAIL` | `PASS_ADVERSARIAL` |
| Annotation | Categorie inconnue | Allowlist refusee | `format_errors` nomme la categorie | `PASS_ADVERSARIAL` |
| Comptage | `expected_count` different | Baseline refusee | `count_mismatch=true` | `PASS_ADVERSARIAL` |
| Syntaxe | Source Python invalide | Aucun fichier ignore | `SyntaxError` propagee | `PASS_ADVERSARIAL` |
| Frontiere | Source marquee symlink | Ne pas suivre | Fichier ignore avant resolution/lecture | `PASS_ADVERSARIAL` |
| Calcul derive | `status = PASS if ... else FAIL` + annotation | Accepte apres revue | Audit `PASS` | `EXPECTED_DEFAULT` |
| Attente de contrat | `statistical_status: PASS` + annotation | Accepte apres revue | Audit `PASS` | `EXPECTED_DEFAULT` |
| Attestation technique | Cle non protegee contenant `status` | Pas de selection par fragment | Zero candidat | `EXPECTED_DEFAULT` |
| Stabilite | Deux lignes inserees avant le sink | Meme empreinte, ligne actualisee | Fingerprint identique, ligne 1 vers 3 | `PASS_ADVERSARIAL` |

## Incident trouve pendant le test

Le prototype faisait remonter `require_oos=True` jusqu'a l'affectation externe
`execution_report`. C'etait un faux positif du scanner : le premier contexte
d'ecriture est maintenant proprietaire du literal et une cle interne non
protegee arrete la remontee. L'inventaire stabilise compte 32 occurrences.

## Preuves

- CLI : 32 candidats, 32 attendus, zero `unapproved`, zero `stale`, status
  `PASS` ;
- 8 tests cibles `OK`, sans `SKIP` ;
- inventaire canonique `OK` ;
- suite complete : 274 tests `OK`.
