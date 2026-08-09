# Plan brut — Partage cross-IA du skill de capitalisation des sessions

> Statut : `INTAKE` — brouillon humain/IA non executable.
> Ce fichier ne constitue ni un `/start`, ni une autorisation d'implementation,
> ni une source normative EBTA.

## 1. Intention humaine

Rendre le skill `capture-coding-session-learnings` utilisable par toutes les IA
qui travaillent sur EBTA, afin que chaque session de codage puisse augmenter la
valeur de la connaissance partagee et la robustesse des agents suivants.

La commande commune proposee est :

```text
/learn-session
```

Elle doit analyser les preuves de la session, distinguer bonnes pratiques,
erreurs et bruit, puis promouvoir chaque enseignement vers son proprietaire
legitime sans creer de source de verite concurrente.

## 2. Constat actuel

- Le skill existe aujourd'hui uniquement dans le profil personnel Codex :
  `C:/Users/liant/.codex/skills/capture-coding-session-learnings/`.
- Cette installation locale n'est ni versionnee avec EBTA ni automatiquement
  visible par Claude ou par une IA travaillant depuis un autre poste.
- Le depot possede deja le catalogue cross-IA canonique `.agents/skills/`.
- `AGENTS.md` impose deja a toute IA de consulter les triggers correspondants
  sous `.agents/skills/`.
- Claude Code decouvre certains skills par des stubs minces sous
  `.claude/skills/`, lesquels pointent vers la procedure canonique sans la
  dupliquer.
- `.codex/` est seulement un adaptateur Codex et ne doit pas devenir une source
  normative ou une copie concurrente du skill.
- La note memoire personnelle Codex creee durant la session n'est pas partagee
  avec les autres IA. La connaissance durable commune doit donc etre promue
  vers des fichiers versionnes possedant deja une responsabilite claire.

## 3. Resultat du test multi-lot

`SINGLE`.

Les composantes ne sont pas des lots independants : le pointeur Claude, la
commande `/learn-session`, la strategie Codex et les validations de decouverte
dependent toutes de la creation prealable du skill canonique sous
`.agents/skills/`. Un seul jeu de criteres de sortie couvre l'ensemble.

## 4. Classification et routage proposes

| Champ | Proposition |
| --- | --- |
| Track | `annexe` |
| Classification | `GOVERNANCE` |
| Workflow | `common` |
| Autorite scientifique | Aucune ; `Protocole/` reste intact et prioritaire |
| Autorite procedurale | `AGENTS.md` puis `.ai/workflows/common/WORKFLOW.md` |
| Source canonique du skill | `.agents/skills/capture-coding-session-learnings/SKILL.md` |

## 5. Scope

1. Creer la version cross-IA canonique du skill dans `.agents/skills/` a partir
   du skill global Codex valide, en l'adaptant aux destinations et contraintes
   du depot EBTA.
2. Creer un stub Claude pur sous `.claude/skills/` qui ne contient aucune
   procedure dupliquee et pointe immediatement vers le skill canonique.
3. Declarer `/learn-session` comme commande conversationnelle commune dans le
   bootstrap/workflow approprie, sans ajouter de transition au cycle des
   workstreams.
4. Definir comment Codex decouvre la version du depot et mesurer explicitement
   la precedence entre la version EBTA et la copie personnelle homonyme dans
   une nouvelle session Codex.
5. Definir la politique de promotion des apprentissages vers les proprietaires
   existants plutot que vers un nouveau ledger d'etat.
6. Valider le skill, les pointeurs, les triggers, les frontieres d'autorisation
   et l'absence de duplication.

## 6. Non-goals

- Ne pas modifier `Protocole/` ni une SOP.
- Ne pas modifier `Implementation/`, BACKTRADER ou NautilusTrader.
- Ne pas creer un nouveau checkpoint, une nouvelle base memoire, un RAG, des
  embeddings, une base vectorielle ou un agent autonome.
- Ne pas ajouter un etat ou une transition a `.ai/workflows/common/WORKFLOW.json`
  pour une commande qui ne change pas le cycle d'un workstream.
- Ne pas copier la procedure complete dans chaque adaptateur d'IA.
- Ne pas rendre automatique une ecriture memoire, un commit, un push ou une
  publication externe.
- Ne pas enregistrer de secrets, sorties brutes volumineuses ou faits non
  verifies.
- Ne pas transformer une retrospective en autorite scientifique ou en preuve
  de performance de trading.

## 7. Architecture cible

```text
.agents/skills/capture-coding-session-learnings/SKILL.md
    |-- lu directement par les IA qui suivent AGENTS.md
    |-- pointe par .claude/skills/capture-coding-session-learnings/SKILL.md
    `-- invoque par /learn-session dans le workflow common
```

Responsabilites :

| Couche | Role | Interdit |
| --- | --- | --- |
| `.agents/skills/.../SKILL.md` | Procedure cross-IA canonique | Porter un etat projet ou une doctrine EBTA |
| `.claude/skills/.../SKILL.md` | Decouverte Claude + pointeur | Paraphraser ou diverger de la procedure canonique |
| `AGENTS.md` | Routeur mince vers la commande | Contenir la procedure complete |
| `.ai/workflows/common/WORKFLOW.md` | Contrat humain de `/learn-session` | Devenir une memoire de sessions |
| Plans, workflows, tests, hooks et skills proprietaires | Recevoir les apprentissages promus | Recevoir du bruit ou une regle hors de leur responsabilite |

## 8. Politique de capitalisation partagee

`/learn-session` doit :

1. delimiter l'objectif, la baseline et la borne finale de la session ;
2. verifier les faits via etat live, commits, diffs, tests et rapports ;
3. classer chaque signal en `BIEN_FAIT`, `A_REUTILISER`,
   `ERREUR_OU_FRICTION` ou `NON_PROMU` ;
4. appliquer un test de promotion : trigger futur, procedure non triviale,
   reutilisabilite, preuve, autorisation et validation ;
5. proposer le proprietaire durable approprie ;
6. persister uniquement ce que la commande humaine autorise explicitement ;
7. rapporter ce qui a ete modifie et ce qui a ete laisse intact.

Destinations autorisees selon la nature de l'enseignement :

- pratique cross-IA reutilisable : skill canonique concerne ;
- regle de cycle projet : workflow proprietaire ;
- erreur mecaniquement detectable : test, hook ou validateur proprietaire ;
- decision ou resultat d'un chantier : plan actif puis archive lors de sa
  cloture normale ;
- nouvelle idee non auditee : `0 - HUMAN START HERE/` en `INTAKE` ;
- changement scientifique : procedure normative separee avec decision humaine.

Il ne doit pas creer par defaut un journal parallele de sessions. La valeur est
obtenue par promotion selective vers les proprietaires existants, pas par
accumulation de transcriptions.

## 9. Phases proposees

### Phase 1 — Canonicaliser le skill

- Creer `.agents/skills/capture-coding-session-learnings/SKILL.md`.
- Conserver le frontmatter minimal `name` + `description`.
- Adapter les destinations de persistance au modele d'autorite EBTA.
- Ajouter des clauses explicites `TRIGGER`, `SKIP`, autorisations et non-role.
- Ne pas ajouter de README, changelog ou ressource non necessaire.

### Phase 2 — Ajouter les adaptateurs de decouverte

- Creer le stub Claude sur le modele des stubs existants.
- Confirmer que Codex decouvre le catalogue `.agents/skills/` dans ce workspace.
- Tester la precedence dans une nouvelle session Codex : la preuve attendue est
  le chemin reel du `SKILL.md` charge, pas seulement la presence du dossier.
- Ne pas modifier, renommer ni supprimer la copie globale Codex dans ce
  chantier. Si elle masque encore la version EBTA, declarer le critere en
  echec et proposer une migration locale separee, soumise a une autorisation
  humaine explicite et a une sauvegarde recuperable.
- Pour toute autre IA future, ajouter seulement un pointeur propre a son
  mecanisme de decouverte si `AGENTS.md` n'est pas lu nativement.

### Phase 3 — Declarer `/learn-session`

- Ajouter une mention courte dans `AGENTS.md`.
- Documenter le contrat complet dans `.ai/workflows/common/WORKFLOW.md`.
- Ne pas modifier `WORKFLOW.json` : la commande ne porte aucune transition de
  workstream.
- Definir que `/learn-session` n'autorise ni commit ni push implicitement.

### Phase 4 — Valider la portabilite et l'absence de faux succes

- Valider le skill canonique avec `quick_validate.py`.
- Verifier mecaniquement que le stub Claude pointe vers le bon fichier et ne
  duplique pas la procedure.
- Verifier qu'une invocation de test retrouve la meme source canonique depuis
  Codex et Claude.
- Tester au moins un cas positif et un cas `NON_PROMU` afin de prouver que le
  skill n'ajoute pas systematiquement une regle ou un nouveau skill.
- Verifier que les verdicts `FAIL`, `DENIED` et `INCONCLUSIVE` restent tels
  quels dans la retrospective.
- Executer `git diff --check` sur le scope.

## 10. Fichiers envisages

```text
.agents/skills/capture-coding-session-learnings/SKILL.md       [CREER]
.claude/skills/capture-coding-session-learnings/SKILL.md      [CREER]
AGENTS.md                                                      [MODIFIER, routeur mince]
.ai/workflows/common/WORKFLOW.md                               [MODIFIER, contrat]
```

Fichiers explicitement hors scope :

```text
Protocole/
Implementation/
.ai/checkpoint.schema.json
.ai/workflows/common/WORKFLOW.json
D:/TRADING/.../BACKTRADER/
C:/Users/liant/.codex/skills/capture-coding-session-learnings/
```

## 11. Risques et controles

| Risque | Controle |
| --- | --- |
| Deux copies du skill divergent | Une seule source canonique versionnee ; precedence mesuree en nouvelle session ; aucune suppression locale implicite |
| La commande cree une nouvelle memoire concurrente | Promotion vers les proprietaires existants ; aucun ledger par defaut |
| Chaque retrospective cree un nouveau skill | Test de promotion + categorie `NON_PROMU` obligatoire |
| Une IA invente un succes | Preuves live et preservation de `FAIL`/`DENIED`/`INCONCLUSIVE` |
| `/learn-session` pousse des changements | Autorisation separee requise pour commit/push/publication |
| Le bootstrap grossit | Une ligne de routage dans `AGENTS.md`, procedure dans le workflow/skill |
| La copie globale masque le skill EBTA | Echec explicite du test de precedence ; migration locale hors chantier et sur autorisation humaine separee |

## 12. Criteres de sortie

- [ ] Le skill canonique existe sous `.agents/skills/` et passe son validateur.
- [ ] Claude et Codex resolvent la meme procedure canonique dans EBTA.
- [ ] Aucun adaptateur ne duplique le corps du skill.
- [ ] `/learn-session` est documente comme commande cross-IA et son contrat est
      non ambigu.
- [ ] La commande distingue analyse, persistance, commit et push ; aucune de ces
      autorisations n'est deduite des autres.
- [ ] Un cas positif produit une promotion justifiee et un cas insuffisant reste
      `NON_PROMU`.
- [ ] Aucun nouveau ledger, etat projet, schema, outil RAG ou dependance n'est
      introduit.
- [ ] `Protocole/`, `Implementation/` et BACKTRADER restent inchanges.
- [ ] Une nouvelle session Codex rapporte le chemin canonique EBTA réellement
      chargé ; si la copie personnelle le masque encore, le chantier reste
      bloque et documente une migration locale separee sans la realiser.
- [ ] Les validations du scope et `git diff --check` passent.

## 13. Decisions humaines deja actees

- 2026-08-09 : consigner les bonnes et mauvaises pratiques de la session et
  transformer cette commande de capitalisation en skill.
- 2026-08-09 : rendre ce skill utilisable par toutes les IA travaillant sur
  EBTA.
- 2026-08-09 : creer d'abord ce plan dans `0 - HUMAN START HERE/`, sans lancer
  automatiquement `/start` ni l'implementation.
- 2026-08-09 : commande `/start` explicite recue ; elle autorise l'audit, la
  restructuration, le routage et la baseline gouvernee, jamais l'implementation
  ni la mutation de la copie personnelle Codex.

## 14. Suite autorisee

La demande courante autorise la promotion gouvernee de ce brouillon par
`/start`. Elle n'autorise ni `/continue`, ni la creation du skill, ni une
mutation hors depot.

Pour l'auditer, le restructurer, le router et archiver son original, utiliser
ensuite :

```text
/start "0 - HUMAN START HERE/PLAN_PARTAGE_CROSS_IA_CAPITALISATION_SESSIONS.md"
```

## 15. Journal de convergence de l'intake

| Passe | Verdict | Corrections appliquees |
| --- | --- | --- |
| 1 — 2026-08-09 | `A_CORRIGER`, risque modere | Le nettoyage destructif de la copie personnelle Codex etait inclus sans autorisation distincte. Il est retire du scope executable ; la decouverte devient un test de precedence en nouvelle session, avec echec explicite si la copie globale masque la source EBTA. La decision `/start` est journalisee et bornee a la promotion. |
| 2 — 2026-08-09 | `CONVERGE`, risque minimal | Le test `epic-orchestrator` confirme `SINGLE` : le skill canonique est un prerequis commun aux adaptateurs, a la commande et aux validations ; aucun second lot independant n'a un jeu d'Exit criteria autonome. Le scope reste organisationnel, sans `Protocole/`, `Implementation/`, BACKTRADER, dependance externe ni mutation hors depot. |
