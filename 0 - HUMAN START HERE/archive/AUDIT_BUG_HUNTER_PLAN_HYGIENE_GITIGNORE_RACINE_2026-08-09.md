# Audit bug-hunter — PLAN_HYGIENE_GITIGNORE_RACINE

Date : 2026-08-09

## Verdict

PASS — aucun bug confirme, repli silencieux ou finding residuel dans 7B.

## Preuves

- 5 tests `RootGitignoreTests` : `OK`.
- Inventaire canonique : `OK`.
- Suite canonique : 284 tests `OK`, 1 skipped preexistant.
- Pyrefly sur le nouveau test : 0 erreur.
- `git ls-files -ci --exclude-standard` : sortie vide.

## Analyse

Le test n'emule pas la syntaxe `.gitignore` : il invoque Git avec
`check-ignore --no-index`. Il exige aussi que la regle gagnante provienne du
`.gitignore` du depot pour chaque cas positif. Les erreurs subprocess ne sont
pas avalees et leurs sorties sont exposees par les assertions.

## Residuel

`.gitignore` ne retire pas un secret deja suivi et ne purge pas l'historique.
Cette limite native n'est pas presentee comme corrigee.
