# Audit adversarial — PLAN_HYGIENE_GITIGNORE_RACINE

Date : 2026-08-09

## Verdict

PASS — la politique locale echoue ferme sur les derives testees.

## Mutations hostiles

Le ratchet injecte quatre variantes en memoire et les rejette toutes :

1. retrait de la protection `.env` ;
2. retrait de l'exception `!.env.example` ;
3. remplacement d'un motif par `.vscode/` ;
4. ajout du motif large `*.md`.

La comparaison de la liste exacte fait egalement echouer toute autre
addition, suppression ou permutation non revue.

## Contrastes Git reels

- Onze artefacts locaux sont ignores par une regle racine attendue.
- `.env.example`, `.vscode/settings.json`, un intake Markdown, une source
  Implementation et un document Protocole restent visibles.
- Aucun fichier deja suivi n'est ignore.

## Limite honnete

Le controle ne constitue ni une detection de secrets, ni un audit de
l'historique Git, ni une politique distante GitHub.
