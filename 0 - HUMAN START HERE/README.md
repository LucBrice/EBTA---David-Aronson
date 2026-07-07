# 0 - HUMAN START HERE

Ce dossier est le point d'entree brut pour les idees, demandes, plans et notes
de l'humain.

## Regles

- Tout contenu ici est `INTAKE`.
- Rien ici n'est executable directement.
- L'humain peut deposer un brouillon non structure.
- L'IA lit, audite, structure si besoin, classe et deplace le fichier vers le
  backlog adapte.
- Le deplacement doit etre trace dans `.ai/checkpoint.json` si le chantier
  devient suivi par l'etat machine.

## Commande humaine

Pour demander l'audit et la promotion d'un brouillon, taper dans l'IA :

```text
/start "0 - HUMAN START HERE/NOM_DU_PLAN.md"
```

L'IA doit alors transformer le brouillon en plan conforme avant d'appeler le
backend `.ai/tools/plan.ps1`.

## Sorties possibles

- `.ai/backlog/mainline/` pour le chantier principal — mais jamais le fichier
  original lui-meme : l'IA y ecrit un **nouveau fichier** integralement
  reecrit selon `.ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md`.
- `.ai/backlog/annexes/` pour les chantiers utiles mais non bloquants (meme
  regle : nouveau fichier reecrit, pas le brouillon deplace).
- `.ai/backlog/fixes/` pour les corrections bornees (idem).
- `archive/` (dans ce dossier) pour le brouillon original, une fois la version
  reecrite creee dans le backlog — voir ci-dessous.
- `.ai/archive/` pour un brouillon rejete avant toute reecriture.

## Archivage du brouillon original

Le brouillon depose ici n'est **jamais reecrit ni edite en place**. Quand
`/start` aboutit, `.ai/tools/plan.ps1 start -Path <ce brouillon>
-RewrittenPath <plan reecrit deja ecrit dans le backlog>` deplace
automatiquement le brouillon original vers `archive/` (prefixe par la date),
pendant que la version structuree et detaillee apparait dans
`.ai/backlog/mainline|annexes|fixes/`. Les deux chemins restent traces
separement dans `.ai/checkpoint.json` (`source_path` pour le plan reecrit,
`original_draft_path` pour le brouillon archive) — rien n'est perdu, rien
n'est ecrase.
