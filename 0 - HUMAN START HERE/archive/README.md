# Archive des brouillons humains

Ce dossier conserve les brouillons originaux, tels que deposes par l'humain
dans `0 - HUMAN START HERE/`, une fois qu'ils ont ete promus via `/start`.

## Regle de routage

Quand un brouillon est audite puis integralement reecrit selon
`.ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md` dans
`.ai/backlog/mainline|annexes|fixes/`, le fichier original **n'est jamais
reecrit ni supprime** : `.ai/tools/plan.ps1 start -Path <brouillon>
-RewrittenPath <plan reecrit>` le deplace ici tel quel, prefixe par la date
(`AAAAMMJJ_nom_original.md`), pour garantir sa tracabilite.

Ce dossier est distinct de `.ai/archive/` :

- `0 - HUMAN START HERE/archive/` conserve l'**intention humaine brute**,
  jamais modifiee, archivee au moment de la promotion (`/start`) ;
- `.ai/archive/` conserve le **plan de backlog final** (deja reecrit), archive
  au moment de la cloture (`/close`).

Le chantier correspondant dans `.ai/checkpoint.json` reference les deux
chemins separement : `source_path` pointe vers le plan reecrit,
`original_draft_path` pointe vers le brouillon archive ici.

Les fichiers ici sont en lecture seule par convention — ce sont des preuves
de ce que l'humain a demande a l'origine, pas des documents de travail actifs.
