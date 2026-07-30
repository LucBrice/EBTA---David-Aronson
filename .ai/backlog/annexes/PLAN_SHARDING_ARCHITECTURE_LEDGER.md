# Plan d'implementation — sharding du registre des veilles de l'Architecture Ledger

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Un chantier actif couvre-t-il deja ce perimetre ? | Non. Aucun workstream du checkpoint ne porte sur le sharding du ledger. |
| Un verrou de gouvernance actif bloque-t-il ce chantier ? | Non. Le chantier est organisationnel dans `.ai/architecture/` et `.agents/skills/`; il ne touche aucune autorite scientifique EBTA. |
| Une decision humaine explicite est-elle necessaire avant routage ? | Non. La decision du 2026-07-30 interdit la purge et exige la conservation integrale ; le plan respecte cette borne. |
| Ce plan remplace-t-il un document ou chantier existant ? | Non. Il restructure un artefact existant sans remplacer le chantier qui l'a cree. |

Test `epic-orchestrator` : **SINGLE**. L'inventaire des consommateurs, la
migration, la mise a jour du skill et la preuve de charge sont sequentiels et
interdependants. Aucun lot ne possede un Exit criteria complet, reordonnable
et cloturable independamment des autres.

## Audit IA de promotion

- [x] `AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json`, le hook et le
      tracking actifs ont ete relus.
- [x] `.ai/governance/AI_MODIFICATION_CHECKLIST.md` et le workflow `common`
      ont ete relus.
- [x] Le brouillon a ete audite en deux passes intake convergentes.
- [x] Le test multi-lot conclut a un chantier unique.
- [x] La promesse de complexite distingue le ledger principal, le chemin de
      lecture courant et le manifeste historique.
- [x] Le perimetre est ferme ; `Protocole/` et `Implementation/` sont
      explicitement interdits.
- [x] Aucun RAG, embedding, base vectorielle, dependance ou agent autonome
      n'est introduit.
- [x] La simulation est isolee hors des artefacts reels.
- [x] Le brouillon original reste distinct de ce plan normalise jusqu'a son
      archivage mecanique par `plan.ps1 start`.

Evidence intake :
`0 - HUMAN START HERE/archive/20260730_PROPOSITION_SHARDING_ARCHITECTURE_LEDGER.md#9-audit-ia-de-promotion`.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `annexe` |
| Lifecycle | `TRIAGED` |
| Type de chantier | `SINGLE` |
| Scope | Extraire le registre individuel des veilles vers des shards mensuels conserves integralement, garder dans le ledger principal les pratiques, le compteur et un pointeur, puis adapter `agent-architecte` afin que son chemin de lecture courant ne depende plus des shards clos. |
| Non-goals | Ne pas purger, tronquer ou resumer une veille ; ne pas modifier les Table A/B, citations, paliers, conditions ou decisions ; ne pas introduire RAG, embeddings, base vectorielle, dependance ou agent autonome ; ne pas toucher `Protocole/`, `Implementation/`, `.ai/checkpoint.schema.json` ni les workflows. |
| Source | Demande humaine du 2026-07-30, archivee apres audit dans `0 - HUMAN START HERE/archive/20260730_PROPOSITION_SHARDING_ARCHITECTURE_LEDGER.md`. |
| Exit criteria | (1) Les 13 lignes reelles sont identiques dans `ledger_veilles/2026-07.md` et absentes du ledger principal. (2) Le manifeste possede une ligne unique `OPEN`, ses compteurs totalisent 13 et son contrat de cloture est explicite. (3) `agent-architecte` lit couramment le ledger + `YYYY-MM.md`, sans manifeste complet ni shard clos, et interdit toute purge. (4) Une simulation temporaire 13 versus 1000 prouve un nombre de lignes constant dans le ledger principal et le chemin courant lorsque la taille du shard actif est tenue constante ; la seule variation du ledger vient des chiffres du compteur (`O(log n)` octets), tandis que le manifeste croit en `O(nombre de mois)`. (5) Aucun artefact synthetique ne subsiste et `git diff --check` passe. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `NON_DEMARRE` |
| Date de creation | 2026-07-30 |
| Date d'activation | - |
| Autorite normative | Aucune autorite scientifique modifiee ; `.ai/architecture/ARCHITECTURE_LEDGER.md` possede la memoire des pratiques et `.agents/skills/agent-architecte/SKILL.md` possede sa procedure. |
| Autorite executable | Aucune : artefacts Markdown et procedure de skill uniquement. |
| Changement normatif attendu | Aucun changement EBTA. Changement organisationnel de gouvernance IA. |
| Dependances externes | PowerShell, Git et outils locaux deja disponibles ; aucune nouvelle dependance. |

## Carte d'execution IA

| Champ | Contenu operationnel |
| --- | --- |
| Objectif executable | Conserver toutes les veilles dans des shards auditables tout en retirant les shards clos du chemin de lecture courant d'`agent-architecte`. |
| Autorite et lecture minimale | Bootstrap repo → ce plan → ledger courant → skill `agent-architecte` → stub Claude → consommateurs trouves par `rg -uu`. |
| Perimetre autorise | Les cinq artefacts fermes de la section 5, plus un repertoire temporaire hors `.ai/architecture/` pour la simulation. |
| Interdits absolus | `Protocole/`, `Implementation/`, Table A/B sur le fond, citations/paliers, purge, RAG/embeddings/vector DB, dependance, artefact synthetique persistant. |
| Phase de reprise | Phase 0 : inventorier les consommateurs et figer la baseline exacte des 13 lignes. |
| Preuve attendue | Comparaison ligne a ligne, sommes/unicite/hash du manifeste, recherches `rg -uu`, simulation isolee 13/1000, absence d'artefact synthetique, `git diff --check`. |
| Arret et escalade | Arreter si un consommateur vivant exige le registre inline, si le nombre/format des lignes reelles diverge, ou si l'objectif exige de modifier une citation, une pratique, le protocole ou le runtime. |

## 1. Role de ce document et non-objectifs

Ce plan gouverne une migration de forme de la memoire des veilles. Il ne
reevalue aucune pratique et ne modifie aucune decision d'architecture
contenue dans le ledger.

La garantie visee est precise :

- le ledger principal ne grandit plus d'une ligne par veille ; seul le
  nombre de chiffres du compteur peut varier en `O(log n)` octets ;
- le chemin courant lit le ledger principal et le shard `YYYY-MM.md` ;
- le manifeste croit d'une ligne par shard, mais n'est pas relu
  integralement a chaque invocation ;
- un audit ou une recherche historique peut toujours relire le manifeste et
  tout shard clos.

Un shard mensuel actif peut encore grossir avec une cadence exceptionnelle
dans un meme mois. Ce risque residuel est explicite et ne justifie aucune
purge ou limite implicite.

## 2. Contexte obligatoire a lire avant de modifier

1. `AGENTS.md`.
2. `.ai/README.md` et `.ai/checkpoint.json`.
3. `.ai/workflows/README.md`, puis `common/WORKFLOW.json` et `WORKFLOW.md`.
4. `.ai/governance/AI_MODIFICATION_CHECKLIST.md`.
5. Le present plan.
6. `.ai/architecture/ARCHITECTURE_LEDGER.md` dans son etat de travail reel.
7. `.agents/skills/agent-architecte/SKILL.md`.
8. `.claude/skills/agent-architecte/SKILL.md`.
9. `.agents/skills/epic-orchestrator/SKILL.md`.

`Protocole/` reste l'autorite scientifique EBTA, mais n'est ni lu en detail
ni modifie par ce chantier. `Implementation/` reste hors scope.

## 3. Table des gates

| Gate | Condition d'entree | Preuve de sortie | NO GO |
| --- | --- | --- | --- |
| G0 — Baseline | Plan `BASELINED`, diff existant compris | Inventaire ferme des consommateurs et extraction exacte des 13 lignes | Modifier le ledger avant d'avoir fige la baseline |
| G1 — Migration | G0 PASS | Shard reel, manifeste et ledger coherents ; 13/13 lignes preservees | Perte, resume ou modification d'une ligne |
| G2 — Procedure | G1 PASS | Skill executable a froid, chemin courant et controles d'integrite explicites | Lire tous les shards ou autoriser une purge |
| G3 — Charge | G2 PASS | Simulation temporaire 13/1000, mesures honnetes et repo sans synthese | Ecrire des donnees fictives dans `.ai/architecture/` |

Les gates sont sequentiels. Un echec reste `FAIL` et bloque la phase suivante.

## 4. Etat des lieux

### Ce qui existe deja

| Element | Etat reel au 2026-07-30 |
| --- | --- |
| Ledger | `.ai/architecture/ARCHITECTURE_LEDGER.md` contient 13 lignes de veilles, Table A, Table B, revisions et compteur 13. Il porte deja des modifications locales humaines a preserver. |
| Skill cross-IA | `.agents/skills/agent-architecte/SKILL.md` exige la lecture du ledger complet et autorise encore un palliatif de purge explicite. |
| Stub Claude | `.claude/skills/agent-architecte/SKILL.md` pointe vers le skill cross-IA ; il ne parse pas le registre inline. |
| Exemple du skill | `.agents/skills/agent-architecte/EXAMPLE_REPORT.md` cite la creation du ledger comme contexte historique ; il ne parse ni sa table ni ses colonnes. |
| Gouvernance | `AI_MODIFICATION_CHECKLIST.md` recommande le skill sans dependre du format du ledger. |
| Etat projet | Aucun workstream actif et aucun chantier existant de sharding. |

### Ce qui manque reellement

- un emplacement durable pour les lignes individuelles ;
- un manifeste avec contrat d'ouverture/cloture et controle d'integrite ;
- une procedure de lecture qui n'impose pas le manifeste historique sur le
  chemin courant ;
- une preuve reproductible du gain et de l'absence de perte.

## 5. Decision d'architecture

### Frontieres explicites

```text
ARCHITECTURE_LEDGER.md
  pratiques + revisions + compteur global + pointeur
       |
       +--> ledger_veilles/MANIFEST.md
              inventaire des shards, compteurs, etat, hash de cloture
                    |
                    +--> YYYY-MM.md
                           lignes individuelles conservees integralement
```

- Le ledger reste proprietaire des pratiques et du compteur global.
- Le manifeste est proprietaire de l'inventaire des shards, pas du detail
  des veilles.
- Chaque shard est proprietaire des lignes individuelles de son mois.
- Le skill est proprietaire de la sequence de lecture et des controles.

### Contrat d'interface entre les couches

Le nom d'un shard est derive par `YYYY-MM.md`. Le manifeste contient :

```text
shard | statut | date_min | date_max | nombre | sha256_cloture
```

- un seul shard peut etre `OPEN` ;
- un shard `OPEN` recoit uniquement des ajouts et a un hash vide ; sa ligne
  de manifeste est mise a jour en place pour ses dates et son compteur ;
- les lignes sont ordonnees chronologiquement, la ligne `OPEN` est la
  derniere ligne de donnees, et la rotation mensuelle peut donc inspecter
  cette seule ligne sans charger l'historique du manifeste ;
- au premier passage dans un nouveau mois, le shard precedent devient
  `CLOSED`, son SHA-256 canonique est inscrit, le nouveau shard est cree
  `OPEN` ;
- un shard `CLOSED` n'est plus modifie ;
- la somme de `nombre` egale le compteur global du ledger ;
- le manifeste ne contient ni titre, ni fichier source, ni detail d'une
  veille.

Le SHA-256 canonique est calcule sur le contenu Markdown decode en UTF-8,
avec BOM retire, fins de ligne normalisees en LF et une unique fin de ligne
terminale. Il prouve le contenu logique du shard independamment d'une
conversion CRLF/LF par Git.

### Decisions deja actees

- conservation integrale, sans seuil de purge ;
- sharding mensuel ;
- aucun outil semantique ou service externe ;
- aucune reevaluation des pratiques pendant la migration ;
- lecture historique seulement a la demande ou lors d'un controle
  d'integrite.

### Structure cible

```text
.ai/architecture/
  ARCHITECTURE_LEDGER.md
  ledger_veilles/
    MANIFEST.md
    2026-07.md
```

### Perimetre de fichiers explicite

Creer :

```text
.ai/architecture/ledger_veilles/MANIFEST.md
.ai/architecture/ledger_veilles/2026-07.md
```

Modifier :

```text
.ai/architecture/ARCHITECTURE_LEDGER.md
.agents/skills/agent-architecte/SKILL.md
.ai/backlog/annexes/PLAN_SHARDING_ARCHITECTURE_LEDGER.md
```

Autorise seulement pendant validation, sans persistance :

```text
<repertoire temporaire explicite hors .ai/architecture/>
```

Interdit :

```text
Protocole/**
Implementation/**
.claude/skills/agent-architecte/SKILL.md
.ai/checkpoint.schema.json
.ai/workflows/**
CLAUDE.md
```

Le checkpoint ne peut etre modifie que par les transitions mecaniques du
workflow (`start`, `baseline`, `continue`, `ready`, `close`), pas comme
livrable fonctionnel du chantier.

## 6. Decoupage en phases

### Phase 0 — Baseline et consommateurs

Objectif : prouver le nombre, l'ordre, les colonnes et les consommateurs
avant tout deplacement.

Actions :

1. Executer `rg -uu` sur `ARCHITECTURE_LEDGER`, le titre de la section
   inline et le compteur.
2. Classer chaque match vivant entre pointeur, documentation historique et
   consommateur de forme.
3. Extraire les 13 lignes exactes et leur ordre depuis le ledger de travail,
   sans repartir de `HEAD` ni ecraser ses modifications locales.
4. Consigner dans ce plan la commande et le resultat.

Critere de sortie : 13 lignes attendues, colonnes exactes figees, liste
fermee des consommateurs ; toute divergence bloque G0.

### Phase 1 — Migration sans perte

Objectif : separer pratiques et lignes individuelles sans changer leur fond.

Actions :

1. Creer `ledger_veilles/2026-07.md` avec l'en-tete contractuel et les 13
   lignes exactes.
2. Creer `MANIFEST.md` avec le contrat et une ligne unique `2026-07.md`,
   `OPEN`, dates 2026-07-17 a 2026-07-29, compteur 13, hash vide.
3. Retirer uniquement la table individuelle du ledger ; ajouter le pointeur
   vers le manifeste et garder le compteur 13.
4. Ajouter une revision datee qui decrit une migration de forme sans
   reevaluation.
5. Comparer automatiquement les lignes source/destination et les compteurs.

Critere de sortie : egalite 13/13, aucune modification du contenu d'une
ligne, Table A/B et citations inchangees relativement a la baseline de G0.

### Phase 2 — Procedure `agent-architecte`

Objectif : rendre le nouveau contrat executable par une IA a froid.

Actions :

1. Reecrire les etapes 1-2 pour lire le ledger, deriver `YYYY-MM.md`, puis
   lire uniquement le shard actif et les nouveaux documents.
2. Documenter la rotation mensuelle `OPEN` vers `CLOSED`, le hash et la
   creation du nouveau shard ; au changement de mois, inspecter uniquement
   la derniere ligne `OPEN` du manifeste avant de la cloturer.
3. Remplacer le palliatif de purge par l'interdiction de purge et la lecture
   historique a la demande.
4. Ajouter au controle anti-scellement : somme des compteurs, unicite
   `OPEN`, hash des shards `CLOSED`.
5. Verifier que le stub Claude reste un pointeur valide sans modification.

Critere de sortie : aucune instruction n'impose tous les shards sur le
chemin courant, aucune purge n'est autorisee, et chaque transition de mois
est deterministe.

### Phase 3 — Simulation de charge isolee

Objectif : mesurer la propriete annoncee sans contaminer le registre reel.

Actions :

1. Creer un repertoire temporaire explicite.
2. Copier la structure cible, puis generer 987 lignes synthetiques dans des
   shards mensuels clos, en conservant un shard actif de taille identique au
   cas de reference.
3. Mesurer octets et lignes :
   - ledger principal pour 13 et 1000 entrees ;
   - chemin courant `ledger + shard actif` ;
   - manifeste, separement.
4. Prouver : lignes du ledger et du chemin courant constantes a shard actif
   constant ; variation en octets limitee aux chiffres du compteur
   (`O(log n)`) ; manifeste en croissance lineaire avec le nombre de mois.
5. Supprimer le seul repertoire temporaire resolu et verifier qu'aucun
   fichier synthetique n'apparait dans `git status`.
6. Journaliser les mesures reelles dans la section 13.

Critere de sortie : mesures conformes, variation du ledger expliquee
exactement par le compteur, aucun artefact synthetique dans le repo, aucune
promesse de cout superieure aux mesures.

### Chemin critique

```text
Phase 0 -> Phase 1 -> Phase 2 -> Phase 3
```

## 7. Artefacts produits

| Artefact | Nature | Preuve |
| --- | --- | --- |
| `ledger_veilles/2026-07.md` | Historique reel append-only | Egalite des 13 lignes |
| `ledger_veilles/MANIFEST.md` | Inventaire et integrite | Somme 13, unique `OPEN` |
| `ARCHITECTURE_LEDGER.md` | Pratiques + compteur + pointeur | Absence de table individuelle |
| `agent-architecte/SKILL.md` | Procedure de lecture/ecriture | Relecture contractuelle et recherches negatives |
| Section 13 du plan | Rapport de simulation | Mesures 13/1000 et absence de residu |

## 8. Invariants absolus et NO GO

### Invariants

1. Les 13 lignes historiques restent textuellement identiques.
2. Toute nouvelle veille reste conservable et retrouvable.
3. Un shard `CLOSED` n'est jamais reecrit et son hash canonique reste
   verifiable malgre les fins de ligne de la plateforme.
4. Le compteur global egale la somme des compteurs du manifeste.
5. Table A, Table B, citations, paliers et conditions restent inchanges.
6. Le manifeste ne duplique aucun detail individuel.
7. Le chemin courant ne lit aucun shard clos.

### NO GO

- supprimer, tronquer, compresser ou resumer une veille ;
- fabriquer un hash pour un shard encore `OPEN` ;
- modifier le fond du ledger sous couvert de migration ;
- injecter des donnees synthetiques dans `.ai/architecture/` ;
- utiliser RAG, embeddings, base vectorielle ou dependance nouvelle ;
- modifier `Protocole/`, `Implementation/`, le stub Claude ou un workflow ;
- declarer le manifeste constant : sa croissance `O(nombre de mois)` doit
  rester visible.

## 9. Verification a chaque etape

Avant modification :

```powershell
git status --short --branch
git diff -- .ai/architecture/ARCHITECTURE_LEDGER.md
rg -uu -n "ARCHITECTURE_LEDGER|Registre des veilles|Compteur total de veilles" --glob "!.git/**" .
```

Apres Phase 1 :

```powershell
rg -n "^\| V[0-9]{2} " .ai/architecture/ledger_veilles/2026-07.md
rg -n "^\| V[0-9]{2} " .ai/architecture/ARCHITECTURE_LEDGER.md
rg -n "Compteur total de veilles ingerees.*13" .ai/architecture/ARCHITECTURE_LEDGER.md
```

La verification ligne a ligne et la somme du manifeste sont executees par
un script PowerShell temporaire en lecture seule sur les artefacts reels.
Le resultat attendu est `13 identiques`, `somme = 13`, `OPEN = 1`.

Apres Phase 2 :

```powershell
rg -n "purger|purgee|entrees recentes" .agents/skills/agent-architecte/SKILL.md
rg -n "YYYY-MM|OPEN|CLOSED|sha256|manifeste" .agents/skills/agent-architecte/SKILL.md
```

La premiere commande doit ne trouver aucune autorisation de purge ; une
mention d'interdiction explicite est acceptable et doit etre inspectee.

Apres Phase 3 :

```powershell
git status --short
git diff --check -- .ai/architecture .agents/skills/agent-architecte .ai/backlog/annexes/PLAN_SHARDING_ARCHITECTURE_LEDGER.md
```

Le statut ne doit montrer aucun shard synthetique. Les modifications locales
preexistantes hors perimetre, notamment le brouillon humain non lie et le
ledger en cours d'edition avant la baseline, ne doivent pas etre ecrasees.

### Execution sans interruption

Apres `/continue`, executer les quatre phases dans l'ordre sans demander de
confirmation intermediaire tant que les invariants et le perimetre ferme
restent respectes.

Causes d'arret legitimes :

1. divergence des 13 lignes ou de leur schema ;
2. consommateur vivant non prevu qui depend du registre inline ;
3. besoin de modifier un fichier interdit ou une decision de fond ;
4. impossibilite de produire ou verifier les mesures sans dependance
   nouvelle.

### Autorite decisionnelle accordee

L'IA peut choisir la mise en forme Markdown, les commandes locales de
comparaison et le mecanisme temporaire de simulation, sans modifier le
contrat de shards, le perimetre ou une decision humaine.

### Interdiction des raccourcis

Un nombre de lignes, un compteur ou un hash declare sans calcul n'est pas une
preuve. Un test synthetique qui modifie les artefacts reels est un echec, pas
une validation.

## 10. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-30 | Refus de toute limite ou purge ; conservation complete avec cout de lecture maitrise. | Interdit toute suppression, synthese ou fenetre glissante de l'historique. |
| 2026-07-30 | `/start` sur la proposition de sharding. | Autorise audit, normalisation et routage ; n'autorise pas l'implementation avant baseline et `/continue`. |

## 11. Risques et blocages connus

| Risque | Impact | Mitigation |
| --- | --- | --- |
| Modification locale du ledger preexistante | Ecrasement de travail humain | Baseline depuis le fichier de travail reel ; aucune restauration depuis `HEAD`. |
| Shard actif exceptionnellement volumineux | Cout courant eleve pendant un mois | Risque accepte et documente ; futur chantier seulement si observe. |
| Compteur divergent | Historique incomplet ou double compte | Somme du manifeste et unicite `OPEN` a chaque controle. |
| Hash d'un shard clos invalide | Reecriture silencieuse | Recalcul et comparaison au controle d'integrite. |
| Lecture systematique du manifeste | Cout courant lie a l'age | Derivation directe `YYYY-MM`; manifeste reserve aux controles/audits. |
| Simulation mal isolee | Pollution de l'historique reel | Repertoire temporaire resolu, verification du diff avant suppression ciblee. |

## 12. Definition of Done

- [ ] Phases 0 a 3 et gates G0 a G3 `PASS`.
- [ ] Les 13 lignes reelles sont conservees integralement et identiquement.
- [ ] Le ledger principal ne contient plus de ligne individuelle.
- [ ] Manifeste coherent : somme 13, unique `OPEN`, contrat de hash explicite.
- [ ] Skill coherent a froid, sans purge ni lecture historique systematique.
- [ ] Simulation 13/1000 documentee avec assertions honnetes.
- [ ] Aucun artefact synthetique ne subsiste.
- [ ] Table A/B, citations, paliers et conditions inchanges.
- [ ] Aucun fichier hors perimetre fonctionnel modifie.
- [ ] `git diff --check` passe.
- [ ] `bug-hunter` n'est pas applicable faute de code runtime ; la
      conformance du plan reste obligatoire avant `/close`.

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat final | A remplir lors de `/close`. |
| Ecarts par rapport au plan initial | A remplir. |
| Suites a prevoir | A remplir ; ne pas transformer le risque de shard actif volumineux en nouveau chantier sans observation ou demande humaine. |

### Resultat d'execution

| Champ | Valeur |
| --- | --- |
| Date | - |
| Phases executees | - |
| Artefact produit | - |
| Validation | - |
| Mesures 13/1000 | - |
| Ecart par rapport au plan | - |

## 14. Journal d'audits post-hoc

| Date de l'audit | Ce qui a ete corrige | Pourquoi |
| --- | --- | --- |
| 2026-07-30 | Promesse de cout, chemin de lecture, contrat `OPEN/CLOSED`, simulation isolee et test multi-lot. | Deux passes intake ont elimine les affirmations asymptotiques excessives et les risques de pollution du registre reel. |
| 2026-07-30 | Audit post-`/start` passe 1 : compteur `O(log n)`, mise a jour de la ligne `OPEN`, hash canonique UTF-8/LF. | Le compteur interdit un delta octets strictement nul et un hash de bytes plateforme serait instable sous conversion CRLF/LF. |
| 2026-07-30 | Audit post-`/start` passe 2 : classification d'`EXAMPLE_REPORT.md`, derniere ligne `OPEN` et source archivee. | Convergence sans nouvel angle mort majeur ; le consommateur historique ne depend pas du format et la rotation mensuelle ne requiert pas une lecture integrale du manifeste. |
