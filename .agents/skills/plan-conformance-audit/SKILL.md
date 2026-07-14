---
name: plan-conformance-audit
description: Verifie qu'un chantier de backlog EBTA a effectivement livre ce que son plan d'implementation commandait avant de le cloturer avec /close. A invoquer automatiquement avant tout appel a ".ai/tools/plan.ps1 close", et manuellement a la demande. Compare les "Exit criteria" du plan au git diff depuis l'activation du chantier, distingue implemente / deja present avant le plan (a ne pas re-signaler comme manquant) / manquant / hors-scope, et bloque la cloture si un critere n'est pas atteint.
---

# Role

Tu verifies qu'un chantier de backlog EBTA a livre ce que son plan
commandait, avant qu'il ne soit archive et oublie. `.ai/tools/plan.ps1
close` est un backend purement mecanique (deplace le fichier, met a jour
`.ai/checkpoint.json`) — il ne fait aucun audit semantique par conception.
Ce skill est l'audit semantique qui doit se produire avant, pas apres.

# Quand s'invoquer

- Automatiquement, quand l'utilisateur tape `/close PLAN_ID` — avant
  d'appeler `.ai/tools/plan.ps1 close`, jamais apres.
- Manuellement, a tout moment pendant un chantier ACTIVE, pour verifier
  l'avancement sans le cloturer.

# Procedure

1. **Localiser le plan.** Chercher le workstream `PLAN_ID` dans
   `.ai/checkpoint.json` (`workstreams[].id`), recuperer `source_path`
   (le fichier plan actuel, pas l'original archive) et `last_moved_at`/la
   date d'activation.

2. **Extraire le contrat du plan.** Lire le fichier plan et sa table
   `## Triage` (`Scope`, `Non-goals`, `Exit criteria`) — format defini par
   `.ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md`. Les `Exit criteria` sont
   censes etre des conditions binaires, observables et testables : si un
   plan en manque ou les formule en adjectifs vagues ("propre", "robuste")
   sans metrique, signale-le comme un defaut du plan lui-meme, ne tente pas
   de deviner un critere binaire a sa place.

3. **Determiner la fenetre du chantier.** Baseline = date d'activation
   (section `## Statut`, `Date d'activation`, ou `last_moved_at` au moment ou
   `lifecycle` est passe a `ACTIVE`). Borne haute = date/etat de cloture
   (`last_moved_at` quand `lifecycle` passe a `DONE`/`BLOCKED`), **pas
   "maintenant"** : du travail sans rapport peut avoir touche les memes
   fichiers apres la cloture (ex: un balayage `bug-hunter` ulterieur) — ce
   travail n'appartient pas a ce plan et ne doit ni compter comme livraison
   ni comme derive de perimetre de ce chantier.
   **Attention au travail non commite** : ce repo ne commite pas
   systematiquement apres chaque chantier — `git log` seul peut ne montrer
   aucun historique pour les chemins concernes meme si le chantier est
   `DONE`. Verifier aussi `git status`/`git diff --cached --stat` (working
   tree et index) sur les chemins du `Scope` avant de conclure qu'un critere
   est MANQUANT faute d'historique de commits.

4. **Comparer chaque Exit criterion a l'etat reel du code**, en utilisant
   `git log`/`git diff`/`git diff --cached` sur la fenetre determinee a
   l'etape 3, restreint aux chemins concernes par le `Scope`, plus la
   lecture directe du code et l'execution des tests/commandes de
   verification que le plan lui-meme declare (section verification/tests)
   si le diff seul ne suffit pas a juger (un renommage ou un refactor peut
   satisfaire un critere sans que le diff le montre litteralement ; un test
   de parite peut passer en `SKIP` plutot qu'en `PASS` si des donnees
   externes sont absentes — verifier lequel des deux avant de conclure).
   Classe chaque critere :
   - **IMPLEMENTE** : preuve concrete dans le diff et/ou les tests
     correspondants passent.
   - **DEJA PRESENT AVANT LE PLAN** : la fonctionnalite existait deja avant
     la baseline (verifie via `git log`/`git blame` anterieur a
     l'activation) — ne compte pas comme manquant, le plan n'avait pas a la
     recreer. Le signaler explicitement pour que l'humain sache pourquoi ce
     critere n'a genere aucun diff.
   - **MANQUANT** : aucune preuve, ni avant ni apres la baseline.
   - **HORS-SCOPE / EXTRA** : changements presents dans le diff mais non
     couverts par le `Scope` declare — a signaler separement, ce n'est pas
     forcement une faute mais ca merite d'etre visible (peut indiquer une
     derive de perimetre ou un `Non-goals` viole).

5. **Rapporter** un tableau croise critere -> classification -> preuve
   (chemin de fichier + commit ou ligne). Si un `Non-goals` a ete
   explicitement viole, le signaler au meme niveau qu'un critere MANQUANT.
   Toute ambiguite trouvee dans la redaction meme du plan (un critere qui se
   verifie mal, un champ jamais mis a jour) se signale aussi — ce n'est pas
   a ce skill de trancher silencieusement une redaction imparfaite du plan.

Voir `EXAMPLE_REPORT.md` pour un audit retroactif reel (plan R1/R2), avec
les deux pieges rencontres en le testant : borner la fenetre a la date de
cloture plutot qu'a "maintenant", et verifier `git diff --cached` en plus
de `git log` quand le chantier n'a jamais ete commite.

# Regle de blocage

- Si un ou plusieurs Exit criteria sont **MANQUANT**, ne pas appeler
  `.ai/tools/plan.ps1 close`. Rapporter precisement ce qui manque et laisser
  l'humain decider (completer le travail, re-scoper le plan, ou forcer une
  cloture `BLOCKED` explicite).
- Si tous les criteres sont IMPLEMENTE ou DEJA PRESENT AVANT LE PLAN (et
  qu'aucun `Non-goals` n'a ete viole sans justification), la cloture peut
  proceder normalement via `.ai/tools/plan.ps1 close`.

# Ce que ce skill ne fait pas

- Il ne juge pas la qualite scientifique ou la conformite au Protocole EBTA
  (voir `EBTA_Protocol_Guardian`).
- Il ne cherche pas de bugs de typage ou de correction (voir `bug-hunter`).
- Il ne re-ecrit jamais le plan lui-meme pour le faire correspondre au code
  livre — si le plan et le code divergent, c'est un fait a rapporter, pas un
  document a corriger silencieusement.
