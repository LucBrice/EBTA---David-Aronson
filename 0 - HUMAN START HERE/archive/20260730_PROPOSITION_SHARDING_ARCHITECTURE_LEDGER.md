# Proposition — Sharding du registre des veilles dans l'Architecture Ledger

Statut : `INTAKE`. Brouillon depose dans `0 - HUMAN START HERE/` conformement
a `0 - HUMAN START HERE/README.md`. N'est pas executable en l'etat ; a
auditer et router via `/start "0 - HUMAN START HERE/PROPOSITION_SHARDING_ARCHITECTURE_LEDGER.md"`
avant toute implementation.

Origine : conversation du 2026-07-30, apres restructuration du format de
`.ai/architecture/ARCHITECTURE_LEDGER.md` (paliers par pratique). Question
posee par l'humain : le ledger reste-t-il exploitable — en cout de lecture
et en qualite de decision pour `agent-architecte` — s'il doit un jour
absorber de l'ordre de 1000 veilles, sans jamais limiter ou tronquer la
connaissance accumulee ?

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `annexe` |
| Lifecycle | `INTAKE` |
| Scope | Restructurer le stockage du registre des veilles d'`ARCHITECTURE_LEDGER.md` pour que le chemin de lecture courant d'une invocation `agent-architecte` (ledger principal + shard actif) ne depende plus du nombre total de veilles historiques, sans supprimer ni resumer l'historique. Le manifeste historique peut croitre d'une ligne par shard, mais il n'est pas relu integralement a chaque invocation. |
| Non-goals | Ne fixe aucune limite ou seuil de purge. Ne modifie pas le registre des pratiques (Table A/B), deja borne par le nombre de themes. N'introduit ni RAG, ni embeddings, ni base vectorielle (interdit sans decision humaine explicite, voir `CLAUDE.md`). Ne change aucune citation, palier ou condition existante. Ne touche pas `Protocole/` ni `Implementation/`. |
| Source | Conversation humaine du 2026-07-30, suite a la restructuration du ledger en echelles de paliers par pratique. |
| Exit criteria | `ARCHITECTURE_LEDGER.md` ne contient plus le registre brut des veilles ; il contient uniquement le registre des pratiques, le compteur global et un pointeur vers le manifeste. Le registre des veilles complet (13 entrees actuelles) est integralement present dans un shard, sans perte. `.agents/skills/agent-architecte/SKILL.md` lit le ledger + le shard courant determine par `YYYY-MM` lors du chemin courant ; le manifeste complet et les shards clos ne sont lus qu'en cas d'audit, de controle d'integrite ou de recherche historique. Une simulation isolee a 1000 entrees (13 reelles + 987 synthetiques) montre que la taille du fichier principal et le volume du chemin de lecture courant ne varient pas avec le nombre de shards clos. |

## 1. Position actuelle (constat)

`.ai/architecture/ARCHITECTURE_LEDGER.md` contient aujourd'hui deux
registres de nature differente dans le meme fichier :

1. **Registre des pratiques** (Table A + Table B) : croit avec le nombre de
   *themes* distincts, pas avec le nombre de veilles. Le rattachement d'une
   nouvelle veille a une pratique existante est le comportement par defaut
   (`SKILL.md`, etape 4) ; une nouvelle ligne n'apparait que si aucune
   pratique existante ne convient. A 13 veilles, 13 pratiques — mais ce
   ratio n'est pas la norme attendue a grande echelle : la plupart des
   veilles a venir devraient enrichir des pratiques existantes plutot que
   d'en creer de nouvelles.
2. **Registre des veilles** (table d'index en tete de fichier) : une ligne
   par veille ingeree, croissance strictement lineaire en 1:1.

`SKILL.md`, etape 1, impose de lire le ledger en entier avant toute
invocation. A 1000 veilles, le registre des veilles seul representerait de
l'ordre de 1000 lignes de tableau (~40-60 tokens/ligne), a charger a chaque
invocation meme si une seule veille a change depuis la derniere fois. Le
cout d'ingestion d'une nouvelle veille (etape 2, lecture delta uniquement)
est deja borne et ne pose pas de probleme ; c'est la lecture du *fichier
d'index lui-meme* qui grossit sans borne.

Le gain vise est donc precis : rendre le chemin de lecture **independant du
nombre de shards clos**, pas pretendre qu'un shard mensuel actif est borne
dans l'absolu. Une cadence exceptionnellement forte dans un meme mois reste
le risque residuel explicite de la section 6.

`SKILL.md` documente deja un palliatif : « Si l'index devient genant,
conserver les entrees recentes, le compteur total et la date de la plus
ancienne entree purgee ; ne jamais purger silencieusement. » Ce palliatif
suppose une purge (perte de detail au-dela des entrees recentes) declenchee
par un jugement subjectif (« genant »), ce que l'humain a explicitement
ecarte dans cette conversation : la connaissance doit rester complete et
consultable, pas resumee ou tronquee.

## 2. Decision d'architecture proposee

Principe directeur : **decoupler le cout de lecture de la taille totale de
l'historique**, en gardant 100% de l'historique consultable, jamais en le
limitant.

Le repo applique deja ce principe ailleurs : `.ai/archive/` conserve tous
les plans clos intacts, hors du cockpit actif (`.ai/checkpoint.json`) qui ne
garde que l'etat courant. Cette proposition applique le meme partitionnement
au registre des veilles.

### Structure cible

```text
.ai/architecture/
  ARCHITECTURE_LEDGER.md          # registre des pratiques (Table A/B) + compteur + pointeur
  ledger_veilles/
    2026-07.md                    # shard mensuel, append-only, jamais reecrit apres cloture du mois
    2026-08.md                    # ...
    MANIFEST.md                   # une ligne par shard : statut, plage, compteur, hash de cloture
```

- Chaque **shard mensuel** contient le registre des veilles ingerees ce
  mois-la, au meme format de table qu'aujourd'hui (ID, Date, Sujet, Fichier
  source, Paliers definis, Ingestion). Le shard du mois courant est `OPEN`
  et recoit uniquement des ajouts. Au changement de mois, il passe
  `CLOSED`, recoit son hash de cloture dans le manifeste et n'est plus
  modifie — coherent avec l'ethique append-only deja en vigueur pour
  `registry.jsonl`/`oos_access_log.jsonl`.
- Le **manifeste** (`MANIFEST.md`) est la seule liste qui croit avec le
  temps, mais a raison d'une ligne par mois, pas par veille : a 1000 veilles
  sur ~3 ans au rythme actuel, environ 36 lignes. Il est consultable pour
  audit et controle d'integrite, mais n'appartient pas au chemin de lecture
  courant.
- `ARCHITECTURE_LEDGER.md` ne garde que : le registre des pratiques (deja
  borne par le nombre de themes), un pointeur vers `MANIFEST.md`, et le
  compteur total (`Compteur total de veilles ingerees`). Il ne contient
  plus jamais le detail des veilles individuelles.

### Ce que `agent-architecte` lit desormais (mise a jour de `SKILL.md`, etape 1-2)

1. Lire `ARCHITECTURE_LEDGER.md` (pratiques + compteur + pointeur) — sa
   taille ne depend plus du nombre de veilles.
2. Deriver le shard du mois courant par convention deterministe
   `ledger_veilles/YYYY-MM.md` ; le creer s'il n'existe pas, puis le lire
   pour connaitre le delta des veilles deja ingerees ce mois-ci. Mettre a
   jour la ligne correspondante du manifeste sans relire les shards clos.
3. Comme aujourd'hui, ne lire integralement que les documents de veille
   *nouveaux* (delta), jamais l'historique complet des shards passes.
4. Le controle anti-scellement par rotation (relecture d'une pratique tous
   les 3 invocations) est inchange : il porte sur les pratiques, deja
   bornees, pas sur les shards.
5. Lire le manifeste complet ou un shard clos uniquement pour une recherche
   historique, une reevaluation qui le requiert ou le controle d'integrite
   periodique.

### Ce que cette proposition NE fait PAS

- Ne resume, ne compresse, ni ne supprime aucune veille passee : chaque
  shard clos reste lisible integralement a la demande (ex. audit humain,
  reevaluation d'une pratique differee qui necessite de revisiter une veille
  ancienne).
- Ne change pas le format des lignes du registre des veilles (memes
  colonnes) : seule leur localisation change.
- Ne cree pas d'index de recherche (grep suffit pour retrouver une veille
  par mot-cle ou par ID a travers les shards, sans RAG ni base vectorielle).

## 3. Etat des lieux (avant/apres) — reutiliser avant de recreer

| Element actuel | Chemin | Devenir |
| --- | --- | --- |
| Registre des veilles (13 lignes) | `.ai/architecture/ARCHITECTURE_LEDGER.md`, section "Registre des veilles ingerees" | Deplace tel quel (memes 13 lignes, memes colonnes) vers `.ai/architecture/ledger_veilles/2026-07.md` (les 13 veilles actuelles datent toutes de juillet 2026) |
| Registre des pratiques (Table A/B) | `.ai/architecture/ARCHITECTURE_LEDGER.md` | Reste en place, inchange dans le fond |
| Table des revisions et controle anti-scellement | `.ai/architecture/ARCHITECTURE_LEDGER.md` | Reste en place, inchange dans le fond ; une ligne de revision datee documente la migration |
| Etapes 1-2 et controle anti-scellement de `SKILL.md` | `.agents/skills/agent-architecte/SKILL.md` | Mise a jour pour lire le ledger + shard courant sur le chemin courant, et reserver le manifeste complet aux controles d'integrite ou recherches historiques |

## 4. Phases

### Phase 0 - Verification prealable

Objectif : confirmer qu'aucun autre document ou outil ne lit
`ARCHITECTURE_LEDGER.md` en supposant que le registre des veilles y est
inline (recherche textuelle du chemin dans le repo).

Actions :

- Rechercher avec inclusion des fichiers caches (`rg -uu`) toute reference a
  `ARCHITECTURE_LEDGER.md`, au registre inline et au compteur global hors du
  brouillon lui-meme.
- Inspecter chaque consommateur vivant, notamment le stub
  `.claude/skills/agent-architecte/SKILL.md`, pour distinguer un simple
  pointeur d'une dependance au format inline.

Critere de sortie :

- Liste fermee des fichiers referencant le ledger, avec confirmation qu'
  aucun ne depend du format inline.

### Phase 1 - Creation de la structure de shards

Objectif : deplacer le registre des veilles existant sans perte.

Actions :

- Creer `.ai/architecture/ledger_veilles/2026-07.md` avec les 13 lignes
  actuelles, colonnes identiques.
- Creer `.ai/architecture/ledger_veilles/MANIFEST.md` avec un contrat de
  colonnes explicite (`shard`, `statut`, `date_min`, `date_max`, `nombre`,
  `sha256_cloture`) et une ligne `OPEN` pour ce premier shard (plage de
  dates 2026-07-17 a 2026-07-29, 13 entrees, hash vide tant que juillet
  reste ouvert).
- Retirer la table inline du registre des veilles d'`ARCHITECTURE_LEDGER.md`,
  la remplacer par le compteur global et un renvoi au manifeste.
- Ajouter une ligne datee dans la table des revisions documentant ce
  changement de forme (aucune citation ni palier modifie).

Livrables :

- `.ai/architecture/ledger_veilles/2026-07.md`
- `.ai/architecture/ledger_veilles/MANIFEST.md`
- `ARCHITECTURE_LEDGER.md` mis a jour

Critere de sortie :

- Les 13 veilles restent toutes retrouvables (par lecture directe du
  shard), aucune perdue ni modifiee.
- La somme des compteurs du manifeste vaut le compteur global et la ligne
  du shard courant est unique.

### Phase 2 - Mise a jour de `SKILL.md`

Objectif : faire lire au skill le ledger principal + shard courant au lieu
du registre inline complet, sans imposer la lecture du manifeste historique
a chaque invocation.

Actions :

- Reecrire l'etape 1 de la procedure (`## Procedure`) pour refleter la
  nouvelle sequence de lecture (voir section 2 ci-dessus).
- Documenter la regle de creation d'un nouveau shard mensuel (ex. : au
  premier `agent-architecte` invoque un nouveau mois, cloturer le shard
  precedent avec son hash, creer le shard du mois et ajouter une ligne
  `OPEN` au manifeste).
- Remplacer le palliatif de purge de `## Controle anti-scellement` par la
  regle de conservation integrale et de lecture historique a la demande.
- Ajouter au controle anti-scellement la verification
  `somme(manifeste.nombre) = compteur global`, l'unicite du shard `OPEN` et
  le controle du hash des shards `CLOSED`.

Livrables :

- `.agents/skills/agent-architecte/SKILL.md` mis a jour.

Critere de sortie :

- La procedure decrite reste executable par une IA a froid sans relire
  cette proposition.

### Phase 3 - Simulation de charge (validation du gain)

Objectif : prouver que le cout de lecture du fichier principal ne croit
plus avec le nombre total de veilles.

Actions :

- Creer une copie isolee dans un repertoire temporaire hors de
  `.ai/architecture/` ; ne jamais injecter d'entree synthetique dans les
  shards ou le manifeste reels.
- Y generer 987 entrees synthetiques reparties sur des shards mensuels
  fictifs, pour simuler ~1000 veilles au total.
- Mesurer avant/apres les octets et lignes d'`ARCHITECTURE_LEDGER.md`, puis
  le volume du chemin courant (`ARCHITECTURE_LEDGER.md` + shard actif).
  Mesurer separement la croissance attendue du manifeste, sans la presenter
  comme constante.
- Detruire uniquement le repertoire temporaire explicitement identifie apres
  verification ; aucun fichier synthetique ne doit apparaitre dans le diff
  du repo.

Critere de sortie :

- Ecart de taille de `ARCHITECTURE_LEDGER.md` egal a zero entre le cas 13 et
  le cas 1000 ; volume du chemin courant independant du nombre de shards
  clos ; croissance du manifeste documentee en `O(nombre de mois)` ; aucun
  artefact synthetique ne subsiste dans le repo.

## 5. Invariants absolus et NO GO

1. Aucun shard clos n'est jamais reecrit ni resume — append-only strict,
   comme `registry.jsonl`.
2. Aucune veille n'est supprimee, meme "ancienne" — pas de seuil de purge,
   conformement a la demande humaine explicite de cette conversation.
3. Le manifeste ne contient jamais le detail d'une veille (titre, fichier
   source) — seulement des metadonnees de shard (plage, compteur) — sinon il
   recree le meme probleme de croissance lineaire un niveau plus haut.
4. Ne pas introduire de recherche semantique, d'embeddings ou de base
   vectorielle pour naviguer les shards : `grep`/lecture directe suffit a
   l'echelle visee et reste stdlib/outil-libre, conformement a l'interdiction
   du `CLAUDE.md` racine sans decision humaine explicite.

## 6. Risques et blocages connus

| Risque | Impact | Mitigation |
| --- | --- | --- |
| Une pratique differee necessite de revisiter une veille ancienne (ex. reevaluation apres plusieurs annees) | Lecture d'un shard ancien, cout ponctuel mais borne (un seul mois, pas tout l'historique) | Accepte : c'est le cout normal d'un audit ponctuel, pas d'une lecture systematique a chaque invocation |
| Cadence d'ingestion tres irreguliere (ex. 50 veilles en un seul jour) | Un shard mensuel pourrait devenir disproportionne un mois donne | Hors scope de cette proposition ; a re-evaluer seulement si constate en pratique, pas anticipe ici |
| Divergence entre le compteur global d'`ARCHITECTURE_LEDGER.md` et la somme des compteurs de shards | Incoherence detectable mais silencieuse | Ajouter une verification manuelle simple (somme des shards = compteur global) au controle anti-scellement existant, a preciser en Phase 2 |
| Manifeste relu integralement a chaque invocation | Le cout courant redevient dependant de l'age du registre, quoique plus lentement | La procedure derive directement `YYYY-MM.md`; le manifeste complet est reserve aux audits, recherches historiques et controles d'integrite |

## 7. Definition of Done

- [ ] Phase 0 a 3 executees et verifiees.
- [ ] `ARCHITECTURE_LEDGER.md` ne contient plus le detail des veilles :
      seulement les pratiques, le compteur global et le pointeur vers le
      manifeste.
- [ ] Les 13 veilles existantes restent integralement retrouvables sans
      perte ni resume.
- [ ] `SKILL.md` mis a jour et relu pour coherence interne.
- [ ] Simulation de charge (Phase 3) documentee, fichiers synthetiques
      supprimes.
- [ ] Aucune citation, palier ou condition de pratique modifiee.
- [ ] Table des revisions d'`ARCHITECTURE_LEDGER.md` mise a jour (append
      only).

## 8. Journal des decisions humaines (autorisations)

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-30 | L'humain refuse explicitement toute solution a base de seuil/limite de purge ; exige que la connaissance reste complete tout en gardant un cout de lecture maitrise. | Ecarte toute variante de cette proposition qui tronquerait ou resumerait l'historique des veilles. |

## 9. Audit IA de promotion

### Test multi-lot `epic-orchestrator`

Verdict : **single-chantier**. Les quatre phases ne possedent pas de criteres
de sortie autonomes et reordonnables : la migration depend de l'inventaire
des consommateurs, la mise a jour du skill depend du contrat de shards, et
la simulation valide la structure produite. Un blocage sur la migration
empeche les phases suivantes d'avoir un objet reel a verifier.

### Passe intake 1 — 2026-07-30

- Correction de la promesse de complexite : le ledger principal et le
  chemin courant sont independants des shards clos ; le manifeste croit
  honnetement en `O(nombre de mois)`.
- Retrait du manifeste complet du chemin de lecture systematique ; le shard
  courant est derive par `YYYY-MM`.
- Formalisation des etats `OPEN`/`CLOSED`, du hash de cloture et des
  controles de coherence.
- Isolation obligatoire de la simulation dans un repertoire temporaire.
- Recherche de dependances elargie aux fichiers caches avec `rg -uu`.

### Passe intake 2 — 2026-07-30

Relecture contre l'etat reel du repo apres corrections : aucun angle mort
majeur nouveau. Les consommateurs vivants identifies sont le skill
cross-IA, son stub Claude pointeur, le ledger lui-meme et la gouvernance qui
recommande le skill ; seul le skill cross-IA depend de la forme du registre.
Le plan peut etre normalise et route sans modifier `Protocole/`,
`Implementation/`, le ledger actuellement en cours d'edition, ni son skill.

---

Ce brouillon n'est pas encore audite. Prochaine etape suggeree : boucle
`/evaluate` (minimum 2 passes) une fois `/start` execute, avant tout
`/continue`, conformement a `CLAUDE.md`.
