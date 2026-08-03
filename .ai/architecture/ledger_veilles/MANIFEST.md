# Manifeste des shards du registre des veilles

Ce manifeste inventorie les shards mensuels sans dupliquer le detail d'une
veille. Les lignes sont ordonnees chronologiquement et la derniere ligne de
donnees est l'unique shard `OPEN`.

Le mois du shard est le **mois d'ingestion**, pas necessairement le mois de
la date de la veille. `date_min` et `date_max` decrivent les dates des
veilles contenues ; une veille ancienne ingeree tardivement reste ajoutee au
shard `OPEN` du mois d'ingestion.

## Contrat

- `OPEN` : le shard du mois courant recoit uniquement des ajouts. Sa ligne
  est mise a jour en place pour `date_min`, `date_max` et `nombre` ;
  `sha256_cloture` reste vide.
- `CLOSED` : le shard ne doit plus etre modifie. Sa ligne est immuable et
  porte son hash canonique.
- Au changement de mois, inspecter uniquement la derniere ligne `OPEN`,
  passer son en-tete a `CLOSED`, calculer le hash canonique de ce contenu
  final, cloturer sa ligne de manifeste, puis ajouter le nouveau shard et sa
  ligne `OPEN`.
- Avant tout ajout, rechercher le nom du fichier source candidat entoure de
  ses delimitateurs Markdown (forme `` `nom.md` ``) avec `rg -F --` dans
  `ledger_veilles/*.md`. Un match existant signifie que la veille est deja
  ingeree et interdit un doublon ; les delimitateurs evitent les collisions
  de sous-chaines et la recherche charge les matches, pas le contenu
  integral des shards.
- Le SHA-256 canonique est calcule sur le Markdown decode en UTF-8, BOM
  retire, fins de ligne normalisees en LF et une unique fin de ligne
  terminale.
- La somme de `nombre` doit egaler le compteur global dans
  `../ARCHITECTURE_LEDGER.md`.
- Une seule ligne peut avoir le statut `OPEN`.
- Toute violation (doublon, compteur divergent, zero ou plusieurs lignes
  `OPEN`, hash manquant/invalide d'un shard `CLOSED`) bloque l'ecriture et
  interdit de declarer l'ingestion reussie.
- Une ingestion est une mutation transactionnelle au niveau du diff :
  ligne du shard `OPEN`, ligne du manifeste et compteur global sont prepares
  ensemble, controles avant commit, puis commites ensemble. Une validation
  en echec doit etre corrigee dans le patch non commite ; ne jamais conserver
  ni publier un etat partiel plausible.
- Une recherche historique ou un controle d'integrite peut lire tout le
  manifeste et les shards requis ; ce n'est pas le chemin de lecture
  courant d'`agent-architecte`.

| shard | statut | date_min | date_max | nombre | sha256_cloture |
| --- | --- | --- | --- | ---: | --- |
| [`2026-07.md`](2026-07.md) | `CLOSED` | 2026-07-17 | 2026-07-29 | 13 | `ca1afd7a5e84a0fa878b80f5639c8052988da4f23cbdda5fb4b4d31e30075be7` |
| [`2026-08.md`](2026-08.md) | `OPEN` | 2026-07-30 | 2026-08-03 | 5 |  |
