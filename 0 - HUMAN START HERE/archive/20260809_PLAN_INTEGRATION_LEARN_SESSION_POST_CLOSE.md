# Brouillon — Intégration automatique de la capitalisation `/learn-session` à la fin de chaque `/close`

> Statut de ce document : `INTAKE`, brouillon humain non audité. Il n'a été ni
> routé, ni structuré via `/start`, ni promu vers `.ai/backlog/`. Aucune
> implémentation n'est autorisée par sa seule existence. Il est rédigé pour
> pouvoir être audité et restructuré selon
> `.ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md` par un futur `/start`, sans
> perte de contenu de fond.

---

## 0. Bandeau de statut (à vérifier avant toute promotion)

| Question | Réponse |
| --- | --- |
| Un chantier actif couvre-t-il déjà ce périmètre (`DONE`, `ACTIVE`, ou `SUPERSEDED`) ? | Partiellement. `PLAN_PARTAGE_CROSS_IA_CAPITALISATION_SESSIONS` est `DONE` (archivé sous `.ai/archive/20260809_PLAN_PARTAGE_CROSS_IA_CAPITALISATION_SESSIONS.md`) et a livré le skill canonique `.agents/skills/capture-coding-session-learnings/SKILL.md`, son stub Claude, et le routage manuel `/learn-session` dans `AGENTS.md` et `.ai/workflows/common/WORKFLOW.md`. Ce chantier antérieur excluait explicitement (section « Non-objectifs ») toute persistance automatique et tout déclenchement implicite — il ne couvre donc pas le déclenchement automatique post-`/close` demandé ici. |
| Un verrou de gouvernance actif bloque-t-il ce chantier (ex. « ne pas étendre au-delà du MVP tant que X ») ? | Aucun verrou identifié à ce jour dans `.ai/checkpoint.json` (`active_workstream_id: null` vérifié le 2026-08-09) ni dans `Implementation/Active/HOOK.md` (hook clos, sans lien avec la capitalisation de session). À reconfirmer lors de l'audit `/start`. |
| Ce plan a-t-il besoin d'une décision humaine explicite pour lever ce verrou avant d'être routable via `/start` ? | Non identifié comme bloquant, mais la décision humaine déjà donnée (section 9) couvre uniquement le principe du déclenchement automatique, pas encore le choix `mainline`/`annexe` ni la formulation exacte à insérer dans les fichiers cibles. |
| Ce plan remplace-t-il un document ou chantier existant ? | Non. Il étend `PLAN_PARTAGE_CROSS_IA_CAPITALISATION_SESSIONS` (`DONE`) sans le rouvrir ni contredire sa clôture ; ce chantier antérieur reste `DONE` tel quel. |

---

## 1. Objectif

Faire en sorte qu'à la fin d'une clôture gouvernée par `/close` aboutissant à
une sortie terminale (`DONE`, `BLOCKED`, `REJECTED`, `SUPERSEDED`), l'agent
invoque automatiquement la rétrospective
`.agents/skills/capture-coding-session-learnings/SKILL.md` (capitalisation :
analyse, classification, rapport, proposition de promotion), sans que
l'humain ait à taper séparément `/learn-session`.

`/learn-session` doit rester utilisable manuellement en plus de ce
déclenchement automatique, notamment avant une clôture ou pour une
rétrospective autonome hors cycle `/close`.

## 2. Contexte et problème de babysitting

Le skill de capitalisation existe et fonctionne (`PLAN_PARTAGE_CROSS_IA_CAPITALISATION_SESSIONS`,
`DONE`, 2026-08-09), mais son déclenchement reste entièrement manuel :
l'humain doit se souvenir de taper `/learn-session`, en général juste après
un `/close`, sous peine de perdre la capitalisation de la session qui vient
de se terminer. Ce babysitting répété est le problème concret que ce plan
adresse : transformer un rappel humain récurrent en comportement
conversationnel systématique de `/close`, sans changer ce que la
rétrospective a le droit de faire.

## 3. Décisions humaines déjà actées

Décision de principe (2026-08-09, humain, portée : conception de ce plan) :
à la fin d'une mission gouvernée par `/close`, l'agent doit lancer
automatiquement la rétrospective de session pour éviter que l'humain doive
la demander séparément.

Séquence cible actée :

```text
/close
→ exécution des gates et audits requis
→ clôture mécanique du workstream
→ validation de l'état final
→ invocation automatique de capture-coding-session-learnings
→ rapport de capitalisation concis
→ proposition de promotion uniquement si un apprentissage satisfait
  le test de promotion du skill
```

Décisions d'architecture déjà arrêtées (2026-08-09, humain) :

1. Le déclenchement appartient au comportement conversationnel de `/close`,
   immédiatement après une clôture et sa validation — pas à un nouveau
   mécanisme séparé.
2. Ne pas intégrer la rétrospective dans `.ai/tools/plan.ps1` : ce backend
   mécanique n'a pas le contexte sémantique complet de la session.
3. Ne pas ajouter de transition à `.ai/workflows/common/WORKFLOW.json` : la
   rétrospective n'est pas un état du workstream.
4. La rétrospective automatique s'exécute après tous les outcomes terminaux
   applicables : `DONE`, `BLOCKED`, `REJECTED`, `SUPERSEDED`.
5. Une erreur de rétrospective reste visible, mais n'annule ni ne transforme
   une clôture déjà valide.
6. L'invocation automatique autorise seulement : l'analyse, la
   classification, le rapport, la proposition de promotion.
7. Elle n'autorise jamais implicitement : création/modification de
   fichiers, commit, push, publication externe, modification de mémoire
   personnelle.
8. `/learn-session` reste utilisable manuellement, notamment avant une
   clôture ou pour une rétrospective autonome.
9. Les verdicts `FAIL`, `DENIED`, `INCONCLUSIVE`, les timeouts et les
   absences de sortie restent littéraux ; la rétrospective ne peut jamais
   les convertir en `PASS`.
10. Ne pas créer de registre chronologique automatique des sessions, de
    nouvelle source de vérité, de RAG, de base vectorielle ou d'agent
    autonome.

## 4. État actuel vérifié (2026-08-09)

- `.ai/checkpoint.json::active_workstream_id` = `null`. Aucun workstream
  `ACTIVE`/`BASELINED` en cours ; le hook actif
  (`Implementation/Active/HOOK.md`) documente une clôture antérieure
  (`PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS`, `DONE`) sans lien
  avec ce sujet.
- `git status` en début de session : `main` est `ahead 4` par rapport à
  `origin/main` (aucun push effectué dans cette session). Le worktree
  contient des changements préexistants et sans rapport avec ce brouillon
  sous `0 - HUMAN START HERE/` :
  - supprimés (working tree) : `0 - HUMAN START HERE/INTAKE_INGESTION_VEILLES_14-18_AGENT_DURABLE_2026-08-03.md`,
    `0 - HUMAN START HERE/PROPOSITION_PIVOT_MOTEUR_NAUTILUS_TRADER.md` ;
  - non suivis : `0 - HUMAN START HERE/PROMPT_BOUCLE_CLOTURE_SUITES_A_PREVOIR.md`,
    `0 - HUMAN START HERE/PROPOSITION_MEMOIRE_INTERCONNECTEE_VEILLES_GRAPHIFY_OBSIDIAN_2026-07-30.md`,
    `0 - HUMAN START HERE/archive/20260731_PROPOSITION_PIVOT_MOTEUR_NAUTILUS_TRADER.md`.
  Ces fichiers ne sont ni créés, ni modifiés, ni supprimés par la session qui
  a rédigé ce brouillon.
- Le skill canonique `.agents/skills/capture-coding-session-learnings/SKILL.md`
  existe, est validé (`quick_validate.py` → « Skill is valid! » lors du
  chantier antérieur), et documente déjà la procédure complète (délimiter la
  session, recueillir les preuves, classer, appliquer le test de promotion,
  router vers le propriétaire, séparer les autorisations, valider et rendre
  compte).
- Le stub `.claude/skills/capture-coding-session-learnings/SKILL.md` (18
  lignes) pointe purement vers le corps canonique, sans le dupliquer.
- `AGENTS.md` (lignes 52-55) documente déjà `/learn-session` comme commande
  de rétrospective sans transition d'état, avec la même séparation
  d'autorisations (analyse/proposition vs persistance/commit/push).
- `.ai/workflows/common/WORKFLOW.md` documente déjà `/learn-session` (section
  dédiée, lignes ~37-60) comme rétrospective manuelle sans transition
  d'état, et documente séparément la séquence `/close` (lignes ~159-182) en
  7 étapes numérotées se terminant par la validation JSON et le commit de
  fermeture — **sans aucune mention de la rétrospective automatique**.
- `.ai/workflows/common/WORKFLOW.json` ne référence aucune notion de
  rétrospective ; ses transitions terminales (`close_done`, `close_blocked`,
  `close_rejected`, `close_superseded`) n'ont pas de preuve requise liée à
  `/learn-session`, conformément à la décision actée §3.3 de ne pas y
  toucher.
- Aucun fichier `.claude/commands/close.md` ou équivalent n'existe : `/close`
  est un comportement conversationnel décrit par `AGENTS.md` +
  `.ai/workflows/common/WORKFLOW.md`, lu directement par l'agent. Il n'y a
  donc pas d'« adaptateur Claude » séparé pour `/close` à modifier au-delà
  de ces deux fichiers.

## 5. Conflit avec le trigger `SKIP` existant du skill

`.agents/skills/capture-coding-session-learnings/SKILL.md`, ligne 3
(frontmatter `description`), contient aujourd'hui :

> « SKIP pour un simple statut, `/continue` ou `/close` sans demande de
> rétrospective, et pour toute tentative de mémoriser automatiquement une
> conversation. »

Cette règle traite explicitement `/close` comme un cas de `SKIP` par défaut
tant qu'aucune « demande de rétrospective » n'est formulée séparément —
c'est exactement le babysitting que ce plan doit éliminer. Le futur
chantier devra remplacer cette clause par une règle non ambiguë qui :

- déclenche automatiquement la procédure après tout `/close` aboutissant à
  une sortie terminale (§3.4), sans exiger de demande humaine séparée ;
- continue de couvrir `SKIP` pour un simple statut, un `/continue`, ou toute
  tentative de mémorisation automatique d'une conversation *hors* cycle
  `/close` ;
- ne réintroduit pas la mémorisation automatique de contenu que la clause
  actuelle interdit à juste titre (§3.10 : pas de ledger chronologique).

## 6. Périmètre exact (à confirmer/affiner lors de l'audit `/start`)

Fichiers dont l'audit `/start` devra vérifier et borner la modification :

- `.agents/skills/capture-coding-session-learnings/SKILL.md` — corriger le
  frontmatter `TRIGGER`/`SKIP` (§5) et, si nécessaire, ajouter une clause
  procédurale précisant que l'invocation post-`/close` suit exactement les
  mêmes autorisations séparées que l'invocation manuelle (§3.6-3.7).
- `.ai/workflows/common/WORKFLOW.md` — section `/close` (actuellement 7
  étapes) : insérer l'invocation de la rétrospective après l'étape de
  validation de l'état final et avant/indépendamment du commit de fermeture,
  en respectant §3.5 (une erreur de rétrospective n'invalide pas une clôture
  déjà valide) ; section `/learn-session` existante : préciser qu'elle est
  désormais aussi déclenchée automatiquement en fin de `/close`, sans dupliquer
  la procédure détenue par le skill.
- `AGENTS.md` — mise à jour mince de la ligne de routage `/learn-session`
  (actuellement lignes 52-55) si l'audit juge nécessaire de refléter le
  déclenchement automatique au niveau du bootstrap.
- Éventuellement `.claude/skills/capture-coding-session-learnings/SKILL.md`
  — seulement si sa résolution effective ou son texte doivent réellement
  changer ; à ce stade rien ne l'indique puisqu'il ne fait que pointer vers
  le corps canonique.

Le futur `/start` doit vérifier concrètement, fichier par fichier, si une
modification est réellement nécessaire avant de l'inclure dans le périmètre
final — cette liste est une hypothèse de travail, pas une prescription
figée.

## 7. Non-objectifs

- Ne pas modifier `.ai/tools/plan.ps1` (décision actée §3.2).
- Ne pas modifier `.ai/workflows/common/WORKFLOW.json` ni introduire de
  nouvelle transition ou de nouvel état lié à la rétrospective (décision
  actée §3.3).
- Ne pas modifier `.ai/checkpoint.schema.json`.
- Ne pas modifier `Protocole/` ni `Implementation/`.
- Ne pas modifier BACKTRADER.
- Ne pas modifier une mémoire personnelle hors dépôt (y compris la copie
  Codex personnelle citée dans le chantier antérieur).
- Ne pas créer de registre chronologique automatique des sessions, de RAG,
  de base vectorielle ou d'agent autonome (décision actée §3.10).
- Ne pas transformer l'invocation automatique en autorisation implicite de
  persistance, commit, push ou publication externe (décision actée §3.7).
- Ne pas modifier la logique interne de classification/promotion du skill
  (§3-4 du `SKILL.md` : `BIEN_FAIT`/`A_REUTILISER`/`ERREUR_OU_FRICTION`/`NON_PROMU`,
  test de promotion) — seul le déclencheur change, pas la procédure.

## 8. Invariants

1. Le déclenchement automatique n'a lieu qu'après une sortie terminale de
   `/close` (`DONE`, `BLOCKED`, `REJECTED`, `SUPERSEDED`) et seulement après
   que la clôture elle-même est valide (gates franchis, JSON validés,
   commit de fermeture effectué ou explicitement en échec documenté).
2. Une clôture mécaniquement valide reste valide même si la rétrospective
   échoue, timeout, ou ne produit aucune sortie ; l'échec de rétrospective
   est rapporté, jamais absorbé ni transformé en `PASS`.
3. L'invocation automatique n'autorise jamais, par elle-même, une écriture
   de fichier, un commit, un push ou une publication externe : ces
   autorisations restent strictement distinctes et doivent être demandées
   séparément si le skill propose une promotion.
4. `/learn-session` reste appelable manuellement à tout moment, avec un
   comportement identique à aujourd'hui.
5. Aucune nouvelle source d'état, de vérité ou de mémoire n'est créée par ce
   chantier ; `WORKFLOW.json` reste strictement inchangé.
6. Les verdicts `FAIL`, `DENIED`, `INCONCLUSIVE`, les timeouts et les
   absences de sortie restent littéraux dans le rapport de capitalisation.

## 9. Risques et modes d'échec

| Risque / mode d'échec | Impact | Mitigation prévue |
| --- | --- | --- |
| L'agent interprète le déclenchement automatique comme une autorisation implicite d'écrire/committer/pousser. | Violation directe des décisions actées §3.6-3.7 ; effet de bord non consenti. | Formulation explicite et redondante dans `SKILL.md` et `WORKFLOW.md` : « analyse et rapport seulement, chaque écriture reste une autorisation séparée ». Cas de test dédié (§10). |
| Une rétrospective automatique en échec (timeout, absence de sortie) est silencieusement ignorée ou masque un vrai problème de clôture. | Perte d'information ; faux sentiment de robustesse. | Invariant §8.2 : l'échec doit être rapporté explicitement dans la sortie de `/close`, jamais avalé. Cas de test dédié (§10). |
| La correction de la clause `SKIP` (§5) est mal formulée et déclenche la rétrospective même hors `/close` (ex. sur un simple statut). | Sur-déclenchement, bruit, dérive vers un babysitting inverse. | Reformulation testée explicitement contre les deux cas : `/close` terminal (doit déclencher) vs statut/`continue` simple (doit rester `SKIP`). |
| Le futur chantier élargit implicitement le périmètre vers `.ai/workflows/common/WORKFLOW.json` pour « simplifier » l'implémentation. | Contredit la décision actée §3.3 ; crée un état machine inutile. | Interdit explicitement en §7 ; à vérifier par `git diff --exit-code -- .ai/workflows/common/WORKFLOW.json` avant `/close` du futur chantier. |
| Une IA différente (Codex ou autre) ne résout pas le même comportement post-`/close` que Claude, faute de lire `WORKFLOW.md` de la même façon. | Divergence cross-IA du comportement automatique, malgré un skill canonique commun. | Forward-test explicite depuis une session IA fraîche (§10) avant de considérer le chantier terminé. |

## 10. Phases d'implémentation (proposées — à revalider par l'audit `/evaluate` du futur chantier)

### Phase 0 — Vérification de la baseline et du non-recouvrement

Objectif : confirmer qu'aucun chantier actif ne couvre déjà ce périmètre et
que l'état vérifié en §4 reste exact au moment du `/start`.

Actions :
- Relire `.ai/checkpoint.json::active_workstream_id` et le hook actif.
- Reconfirmer `git status` / `ahead N` par rapport à `origin/main`.
- Reconfirmer que le skill canonique et le stub Claude n'ont pas changé
  depuis ce brouillon (sinon adapter les phases suivantes).

Critère de sortie : aucun chantier actif conflictuel ; état machine
cohérent avec §4 ou divergences documentées.

### Phase 1 — Corriger la clause `TRIGGER`/`SKIP` du skill canonique

Objectif : lever le conflit décrit en §5 sans réintroduire de mémorisation
automatique interdite.

Actions :
- Reformuler le frontmatter `description` de
  `.agents/skills/capture-coding-session-learnings/SKILL.md` pour
  distinguer explicitement : déclenchement automatique après `/close`
  terminal (§3.4) vs `SKIP` pour statut/`continue`/mémorisation
  automatique hors cycle `/close`.
- Ajouter, si nécessaire dans le corps du skill (section « Autorité et
  non-rôle » ou « Séparer les autorisations »), une clause rappelant que
  l'invocation post-`/close` suit exactement les mêmes autorisations
  séparées que l'invocation manuelle.

Livrables : `SKILL.md` corrigé ; validation `quick_validate.py`.

Critère de sortie : le validateur passe ; la clause ne contient plus
d'ambiguïté entre « déclenchement automatique attendu » et « SKIP par
défaut ».

### Phase 2 — Documenter la séquence dans le workflow commun

Objectif : rendre la séquence cible (§3, bloc `/close → ... → rétrospective
→ rapport → proposition`) explicite et non ambiguë dans
`.ai/workflows/common/WORKFLOW.md`, sans toucher `WORKFLOW.json`.

Actions :
- Étendre la section `/close` existante (actuellement 7 étapes) pour
  insérer l'invocation automatique de la rétrospective après la validation
  de l'état final, avec la règle explicite qu'un échec de rétrospective ne
  transforme ni n'annule une clôture déjà valide.
- Mettre à jour la section `/learn-session` existante pour indiquer qu'elle
  est désormais aussi invoquée automatiquement en fin de `/close`, en
  renvoyant au skill pour la procédure détaillée (pas de duplication).

Livrables : `WORKFLOW.md` modifié ; `WORKFLOW.json` strictement inchangé
(vérifié par diff).

Critère de sortie : une IA froide qui lit uniquement `WORKFLOW.md` sait
que `/close` déclenche automatiquement la rétrospective, dans quelles
conditions, et avec quelles autorisations.

### Phase 3 — Mise à jour mince du bootstrap (si nécessaire)

Objectif : refléter dans `AGENTS.md` le déclenchement automatique sans
dupliquer la procédure.

Actions :
- Évaluer si la ligne de routage actuelle (lignes 52-55) reste suffisante
  telle quelle, ou si elle doit être complétée d'une clause courte
  (« également déclenché automatiquement en fin de `/close`, voir
  `.ai/workflows/common/WORKFLOW.md` »).

Livrables : `AGENTS.md` inchangé ou modifié a minima.

Critère de sortie : cohérence entre `AGENTS.md` et `WORKFLOW.md` sans
duplication de contenu procédural.

### Phase 4 — Tests et forward-tests

Voir §11 pour le détail des cas.

## 11. Tests et forward-tests cross-IA (minimum requis)

1. Validation du skill : `quick_validate.py` sur
   `.agents/skills/capture-coding-session-learnings` → succès explicite.
2. Test d'une clôture `DONE` : simuler ou observer un `/close` aboutissant
   à `DONE` et vérifier que la rétrospective démarre automatiquement, sans
   commande `/learn-session` séparée.
3. Test d'une clôture non-`DONE` (`BLOCKED`, `REJECTED` ou `SUPERSEDED`) :
   même vérification, pour confirmer que le déclenchement ne dépend pas de
   l'issue positive de la clôture (décision actée §3.4).
4. Preuve que la rétrospective démarre sans nouvelle intervention humaine
   (pas de question intermédiaire requise pour la déclencher elle-même).
5. Preuve qu'elle ne modifie aucun fichier sans autorisation explicite
   distincte (cas de test : session read-only ou instrumentée, aucune
   écriture observée hors autorisation donnée).
6. Preuve qu'un échec simulé de rétrospective (timeout ou absence de
   sortie) ne falsifie pas la clôture déjà actée : le statut `DONE`/`BLOCKED`/
   `REJECTED`/`SUPERSEDED` du workstream reste inchangé et correctement
   persisté dans `.ai/checkpoint.json`.
7. Preuve que `/learn-session` manuel fonctionne encore à l'identique
   (avant clôture, ou de façon autonome).
8. Preuve que `.ai/workflows/common/WORKFLOW.json`, `.ai/tools/plan.ps1`,
   `Protocole/` et `Implementation/` restent inchangés
   (`git diff --exit-code` sur chacun).
9. Validation JSON du checkpoint et du tracking :
   ```powershell
   python -m json.tool .ai\checkpoint.json
   python -c "import json, jsonschema; jsonschema.validate(json.load(open('.ai/checkpoint.json', encoding='utf-8')), json.load(open('.ai/checkpoint.schema.json', encoding='utf-8')))"
   python -m json.tool Implementation\Active\tracking.json
   python -c "import json, jsonschema; jsonschema.validate(json.load(open('Implementation/Active/tracking.json', encoding='utf-8')), json.load(open('Implementation/Active/tracking.schema.json', encoding='utf-8')))"
   ```
10. `git diff --check` sur les fichiers effectivement touchés par le futur
    chantier.
11. Forward-test cross-IA depuis une session IA fraîche (au minimum une
    session Codex, comme pour le chantier antérieur) : vérifier que la même
    séquence automatique est comprise et déclenchée, pas seulement par
    Claude.

## 12. Critères de sortie vérifiables (Exit criteria, ébauche)

- Un `/close` aboutissant à une sortie terminale (`DONE`, `BLOCKED`,
  `REJECTED`, `SUPERSEDED`) déclenche automatiquement, dans la même
  conversation, l'analyse et le rapport de
  `capture-coding-session-learnings`, sans commande `/learn-session`
  séparée — prouvé par les cas §11.2-11.3.
- Aucune écriture de fichier, commit, push ou publication externe n'est
  produite par le seul fait du déclenchement automatique — prouvé par
  §11.5.
- Un échec de rétrospective n'altère jamais le statut d'une clôture déjà
  valide — prouvé par §11.6.
- `/learn-session` manuel reste fonctionnel à l'identique — prouvé par
  §11.7.
- `WORKFLOW.json`, `plan.ps1`, `Protocole/`, `Implementation/` restent
  inchangés — prouvé par §11.8.
- Toutes les validations JSON et `git diff --check` passent — prouvé par
  §11.9-11.10.
- Le comportement est confirmé reproductible par au moins une IA autre que
  celle qui a implémenté le chantier — prouvé par §11.11.

## 13. Fichiers autorisés et fichiers interdits

**Autorisés (hypothèse de périmètre, à confirmer par l'audit `/start`,
voir §6)** :

```text
.agents/skills/capture-coding-session-learnings/SKILL.md   [MODIFIER]
.ai/workflows/common/WORKFLOW.md                            [MODIFIER]
AGENTS.md                                                    [MODIFIER, mineur, si necessaire]
.claude/skills/capture-coding-session-learnings/SKILL.md    [MODIFIER, seulement si sa resolution doit reellement changer]
```

**Interdits (hors scope explicite, sauf preuve contraire documentée dans
le futur plan)** :

```text
.ai/tools/plan.ps1                                           [BACKEND MECANIQUE - hors scope, decision actee §3.2]
.ai/workflows/common/WORKFLOW.json                            [CONTRAT D'ETATS - inchange, decision actee §3.3]
.ai/checkpoint.schema.json                                   [SCHEMA - inchange]
Protocole/                                                   [NORME - intouchable]
Implementation/                                               [RUNTIME - hors scope]
BACKTRADER (repo externe)                                    [REFERENCE-ONLY - hors scope]
Toute memoire personnelle hors depot                          [HORS DEPOT - aucune mutation]
```

## 14. Stratégie de rollback

Toutes les modifications prévues (§6, §13) sont des fichiers Markdown de
gouvernance/documentation versionnés par Git, sans migration de schéma ni
effet d'état persistant :

- Chaque phase (§10) doit produire un commit distinct et réversible suivant
  la forme obligatoire du dépôt (`.ai/workflows/common/WORKFLOW.md`,
  section « Forme obligatoire des commits »).
- En cas d'échec de validation (§11) après une phase, revenir au commit
  précédent de ce chantier (`git revert` ciblé, jamais `git reset --hard`
  sur un historique déjà partagé) plutôt que de corriger en aveugle.
- Comme `WORKFLOW.json` et `plan.ps1` restent inchangés (invariant §8.5),
  un rollback complet de ce chantier n'affecte jamais la mécanique de
  clôture existante ni les workstreams déjà `DONE`.
- Si le forward-test cross-IA (§11.11) échoue de façon non résolvable dans
  le périmètre de ce plan, documenter l'échec en section « Cloture » du
  futur plan routé et escalader vers une décision humaine plutôt que de
  livrer un comportement non prouvé sur toutes les IA cibles.

## 15. Exigences d'audit adversarial et de conformité

Le futur chantier issu de ce brouillon doit, avant tout `/close` :

- Appliquer `.agents/skills/bug-hunter/SKILL.md` sur les fichiers
  effectivement touchés (attendu : essentiellement Markdown, mais le skill
  reste le gate standard du dépôt avant clôture).
- Appliquer `.agents/skills/adversarial-tester/SKILL.md` si le diff touche
  une logique dérivée de paramètres ou un comportement conversationnel
  vérifiable mécaniquement (ici : la séquence `/close → rétrospective`),
  conformément à `.ai/governance/AI_MODIFICATION_CHECKLIST.md`, section
  « Après modification », dernier point.
- Appliquer `.agents/skills/plan-conformance-audit/SKILL.md` contre les
  Exit criteria de la section 12 avant toute clôture.
- Documenter un verdict explicite (`PASS_ADVERSARIAL` / `PASS_CONFORMANCE`
  ou équivalent motivé) plutôt qu'une affirmation narrative non prouvée,
  suivant le précédent de
  `.ai/archive/20260809_PLAN_PARTAGE_CROSS_IA_CAPITALISATION_SESSIONS.md`
  (sections 15-16).

## 16. Distinction stricte entre analyse, persistance, commit et push

Cette distinction, déjà actée en §3.6-3.7 et §8.3, doit être préservée
littéralement par le futur chantier à tous les niveaux :

| Niveau | Ce qu'il autorise | Ce qu'il n'autorise jamais |
| --- | --- | --- |
| Déclenchement automatique post-`/close` | Analyse des preuves bornées de la session ; classification ; rapport ; proposition de promotion. | Toute écriture, tout commit, tout push, toute publication externe. |
| Autorisation de persistance (si donnée séparément par l'humain) | Création/modification des fichiers cibles identifiés par le test de promotion du skill. | Un commit automatique de ces fichiers. |
| Autorisation de commit (si donnée séparément) | Un commit local suivant la forme obligatoire du dépôt. | Un push ou une publication externe. |
| Autorisation de push/publication (si donnée séparément) | Le push ou la publication explicitement demandés. | Toute extension à un contenu non explicitement autorisé. |

Chaque ligne du tableau exige sa propre autorisation humaine explicite ;
aucune n'est déductible d'une autre, y compris à l'intérieur du futur
chantier d'implémentation lui-même.

---

## 17. Journal des décisions humaines (autorisations)

| Date | Décision | Portée |
| --- | --- | --- |
| 2026-08-09 | Décider que `/close` doit déclencher automatiquement la rétrospective de capitalisation, selon la séquence et les 10 décisions d'architecture reportées en §3. | Autorise la rédaction de ce brouillon `INTAKE` sous `0 - HUMAN START HERE/`. N'autorise ni `/start`, ni `/continue`, ni `/close`, ni implémentation, ni commit, ni push. |

---

## 18. Definition of Done (de ce brouillon, pas du futur chantier)

- [x] Lecture complète et dans l'ordre de `AGENTS.md`, `.ai/README.md`,
      `.ai/checkpoint.json`, des chemins actifs déclarés, de
      `.ai/governance/AI_MODIFICATION_CHECKLIST.md`,
      `.ai/workflows/README.md`, `.ai/workflows/common/WORKFLOW.md`,
      `.ai/workflows/common/WORKFLOW.json`,
      `.agents/skills/capture-coding-session-learnings/SKILL.md`, et de
      `.ai/archive/20260809_PLAN_PARTAGE_CROSS_IA_CAPITALISATION_SESSIONS.md`.
- [x] État Git live vérifié (`ahead 4`, fichiers préexistants sans rapport
      dans `0 - HUMAN START HERE/`), confirmé plutôt que recopié de la
      session précédente.
- [x] Conflit avec la clause `SKIP` actuelle du skill identifié et documenté
      (§5).
- [x] Toutes les sections demandées sont présentes : objectif, contexte,
      décisions actées, état vérifié, conflit `SKIP`, périmètre, non-objectifs,
      invariants, risques, phases, tests/forward-tests, critères de sortie,
      fichiers autorisés/interdits, rollback, exigences d'audit, distinction
      analyse/persistance/commit/push.
- [x] Aucune commande `/start`, `/continue` ou `/close` exécutée.
- [x] Aucun commit créé, aucun push effectué.
- [x] Aucun fichier préexistant du worktree modifié par la rédaction de ce
      brouillon.

---

## 19. Journal de convergence de l'intake

| Passe | Verdict | Corrections appliquées |
| --- | --- | --- |
| 1 — 2026-08-09 | `A_CORRIGER`, risque modéré | §10 Phase 2 et §6 formulaient le point d'insertion de la rétrospective comme « après la validation de l'état final et avant/indépendamment du commit de fermeture ». Formulation à deux branches non tranchées : une IA pouvait légitimement exécuter la rétrospective entre l'étape 5 (validation JSON) et l'étape 6 (commit de fermeture, limité *exactement* aux fichiers de fermeture) de `.ai/workflows/common/WORKFLOW.md` section `/close`, avec un risque concret qu'un artefact d'analyse produit par la rétrospective se retrouve inclus dans ce commit — violation directe de l'invariant §8.3 (aucun commit implicite via le déclenchement automatique). |
| 2 — 2026-08-09 | `CONVERGE`, risque minimal | Le point d'insertion est désormais ancré précisément sur la résolution effective de l'étape 6 (branche commit-réussi) ou de l'étape 7 (branche échec-rapporté) de `WORKFLOW.md` section `/close`, jamais entre les étapes 4 et 6. La reformulation supprime toute lecture « avant le commit » et reste cohérente avec l'invariant §8.1 (commit de fermeture effectué ou explicitement en échec documenté). Aucun nouvel angle mort majeur relevé sur le reste du brouillon (périmètre de fichiers, non-objectifs, invariants, risques, tests/forward-tests, rollback : vérifiés conformes à l'état réel du dépôt lors de l'audit `code-architecture-evaluator`, sans hallucination détectée). Ce correctif est reporté dans le plan restructuré promu via `/start` ; le brouillon original ci-dessus reste inchangé pour le reste de son contenu de fond. |
