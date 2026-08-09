# Plan — Chantier mere des ameliorations post-retrospective CI Node.js 20

> Chantier mere de coordination uniquement. Il ne porte aucune implementation
> directe et conserve trois sous-chantiers independants, chacun soumis a son
> propre cycle gouverne `/start -> /evaluate x2 -> baseline -> /continue ->
> audits -> /close`.

## 0. Bandeau de statut (a verifier avant toute promotion)

| Champ | Valeur |
| --- | --- |
| ID | `EPIC_AMELIORATIONS_POST_RETROSPECTIVE_CI_NODE20` |
| Track | `fix` |
| Lifecycle | `TRIAGED` |
| Portee | `meta` — gouvernance IA et outillage du workflow, sans changement scientifique EBTA |
| Classification | `GOVERNANCE` |
| Type de chantier | `MULTI_LOT` — chantier mere de coordination, sans implementation directe |
| Workflow | `common` |
| Source | `0 - HUMAN START HERE/EPIC_AMELIORATIONS_POST_RETROSPECTIVE_CI_NODE20.md` |
| Brouillon archive attendu | `0 - HUMAN START HERE/archive/20260809_EPIC_AMELIORATIONS_POST_RETROSPECTIVE_CI_NODE20.md` |
| Etat actif verifie | `.ai/checkpoint.json::active_workstream_id` vaut `null` le 2026-08-09 |
| Synchronisation Git verifiee | `HEAD` est en avance de 4 commits et en retard de 0 sur `origin/main`; aucun pull n'est requis avant le routage |
| Decision normative requise | Non : aucun lot ne touche `Protocole/`, une SOP, un seuil, un gate ou un verdict EBTA |
| Resultat du test multi-lot | `MULTI_LOT` : pour chacun des Lots 1, 2 et 3, l'Exit criteria est autonome, l'ordre peut changer sans modifier le sens, et un blocage local n'empeche pas les deux autres d'avancer |
| Autorisation actuelle | La decision humaine `Je valide tes propositions` autorise la persistance et le `/start`; elle n'autorise ni commit, ni push, ni publication externe |

## Audit IA de promotion

- [x] Bootstrap lu dans l'ordre impose : `AGENTS.md`, `.ai/README.md`,
      `.ai/checkpoint.json`, hook actif, tracking actif, entree protocolaire,
      checklist de gouvernance et workflow `common`.
- [x] Etat Git verifie apres `git fetch origin` : le checkout n'est pas en
      retard sur `origin/main`.
- [x] Test multi-lot de `epic-orchestrator` applique et documente dans le
      bandeau.
- [x] Passe `/evaluate` 1 : confrontation aux proprietaires et consommateurs
      reels. Deux ecarts du brouillon ont ete corriges dans ce plan :
      `PLAN_INTEGRATION_LEARN_SESSION_POST_CLOSE` est deja `DONE`, et aucun
      `quick_validate.py` n'existe pour `code-architecture-evaluator`.
- [x] Passe `/evaluate` 2 : relecture apres correction. Aucun nouvel angle
      mort majeur ; les trois lots restent independants, les frontieres de
      fichiers sont explicites et aucune extension de schema n'est requise.
- [x] Le brouillon humain reste intact ; ce fichier est une copie normalisee
      nouvelle destinee au backlog `fix`.
- [x] Les modifications humaines sans rapport presentes dans le worktree sont
      hors perimetre et preservees.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `fix` |
| Lifecycle | `TRIAGED` |
| Type de chantier | `MULTI_LOT` — chantier mere de coordination |
| Scope | Coordonner trois correctifs durables reveles par la retrospective du correctif CI Node.js 20 : recherche des consommateurs contractuels pendant `/evaluate`, autorisation explicite d'un cycle pouvant exiger deux pushes, diagnostic actionnable des ancres de preuve invalides. |
| Non-goals | Ne pas implementer les lots dans ce chantier mere. Ne pas fusionner deux lots dans un plan, un commit ou une cloture. Ne pas modifier `Protocole/`, `Implementation/`, BACKTRADER, `.ai/checkpoint.schema.json` ou `.ai/workflows/common/WORKFLOW.json`. Ne pas creer de nouveau skill. Ne pas affaiblir la validation des preuves. Ne pas committer ni pousser sur la seule autorite de `/start`. |
| Source | Retrospective du chantier `PLAN_CORRECTION_CI_NODE20_DEPRECATION_CORE_ENGINE`, commits bornes `704af88`, `54e00f4` et `0d70f77`, run GitHub Actions `31318437757`, puis decision humaine du 2026-08-09 validant les trois propositions. |
| Exit criteria | (1) Les trois lots sont `DONE` ou explicitement differes par decision humaine journalisee. (2) Chaque lot possede son workstream, ses audits, sa baseline, son implementation et sa cloture distincts. (3) L'audit final couvre l'union des fichiers touches depuis la baseline du chantier mere. (4) Aucun brouillon humain parallele n'a ete absorbe ou modifie. |

## Sous-chantiers

| n | ID | Titre | Nature revalidee | Proprietaire cible | Exit criteria autonome | Statut |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | PLAN_EVALUATE_RECHERCHE_CONSOMMATEURS_CONTRACTUELS | Recherche des consommateurs contractuels pendant `/evaluate` | Amelioration d'un skill existant | `.agents/skills/code-architecture-evaluator/SKILL.md` et validateur canonique `skill-creator/scripts/quick_validate.py` | Tout plan visant un workflow, une configuration, un schema ou un manifeste impose la recherche explicite des tests et consommateurs qui figent ses valeurs; la validation choisie par le lot existe et s'execute avec succes. | `DONE` — `cb02758` |
| 2 | PLAN_AUTORISATION_PUBLICATION_DEUX_PUSHES | Autorisation explicite des deux pushes potentiels | Clarification du contrat conversationnel | `.ai/workflows/common/WORKFLOW.md` | Lorsqu'un gate distant exige un push avant `/close`, la demande distingue le push d'implementation et l'eventuel push du commit de fermeture; aucune autorisation implicite ni modification de `WORKFLOW.json`. | `DONE` — `1ba3074` |
| 3 | PLAN_DIAGNOSTIC_ANCRES_PREUVES_WORKFLOW | Diagnostic actionnable des ancres de preuve | Correctif mecanique avec tests | `.ai/tools/workflow_state.ps1` et `.ai/tools/tests/test_workflow_state_machine.ps1` | Une ancre absente reste rejetee; l'erreur expose le slug recherche et les slugs de titres valides; tests positif et negatif `PASS` sans relacher `Test-EvidenceReferenceSubstance`. | `DONE` — `7a6de9b` |

Le `routing_reason` de chaque futur enfant commencera par
`Sous-chantier <n>/3 de EPIC_AMELIORATIONS_POST_RETROSPECTIVE_CI_NODE20`.
Le lien parent/enfant reste narratif : aucune propriete n'est ajoutee au
schema du checkpoint.

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `NON_DEMARRE` — route mais non baseline, non actif et non executable |
| Date de creation | 2026-08-09 |
| Autorite normative | `Protocole/` reste inchange et hors perimetre |
| Autorite procedurale | `.ai/workflows/common/WORKFLOW.md` et `.agents/skills/epic-orchestrator/SKILL.md` |
| Autorite executable | `.ai/tools/plan.ps1` et `.ai/tools/workflow_state.ps1`, chacune dans son lot propre |

## Carte d'execution IA (lecture prioritaire pour `/continue`)

```text
Ce workstream est un coordinateur MULTI_LOT.
INTERDICTION : ne jamais executer directement les modifications des Lots 1-3
depuis ce plan.

Suite immediate apres cloture du Lot 2 :
1. Revalider le Lot 3 contre `workflow_state.ps1` et ses tests courants.
2. Creer uniquement son brouillon humain propre.
3. Executer son cycle complet et le clore.
4. Mettre a jour ce parent, puis auditer et clore le chantier mere.
```

## 1. Role de ce document et non-objectifs

Ce document est l'unique point d'ancrage des trois ameliorations. Il conserve
l'ordre, les decisions humaines, les identifiants enfants et l'etat de leur
cloture sans recopier leurs futurs plans d'implementation.

Il ne code rien, ne cree aucun contrat scientifique, ne devient pas une source
de verite concurrente et ne rend aucun lot executable par sa seule existence.

## 2. Contexte obligatoire a lire avant de coder

1. `AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json` et les chemins actifs
   qu'il declare.
2. `.ai/workflows/common/WORKFLOW.md` et
   `.agents/skills/epic-orchestrator/SKILL.md`.
3. Ce plan parent dans son etat live.
4. Le proprietaire et les consommateurs reels du prochain lot uniquement.
5. Les archives CI :
   `.ai/archive/20260809_PLAN_CORRECTION_CI_NODE20_DEPRECATION_ACTIONS.md` et
   `.ai/archive/20260809_PLAN_CORRECTION_CI_NODE20_DEPRECATION_CORE_ENGINE.md`.

Le plan `PLAN_INTEGRATION_LEARN_SESSION_POST_CLOSE` est maintenant archive et
`DONE`; avant le Lot 2, relire la version courante de `WORKFLOW.md` au lieu de
traiter l'ancien brouillon comme un conflit actif.

## 3. Table des gates (points de decision sequentiels)

| Gate | Condition | Effet si echec |
| --- | --- | --- |
| P0 — parent route | Ce plan est `TRIAGED` et le checkpoint est valide | Aucun enfant n'est cree |
| P1 — nature du prochain lot | La classification et les consommateurs sont reverifies dans le repo live | Corriger d'abord ce parent; ne pas rediger l'enfant sur une hypothese fausse |
| P2 — plan enfant | Deux passes `/evaluate` intake puis deux passes post-route convergent | Ne pas baseliner ni implementer |
| P3 — execution enfant | Baseline attestee, tests et audits propres au lot sans finding ouvert | Ne pas clore le lot |
| P4 — progression parent | Le lot courant est terminal et ce parent est mis a jour | Ne pas ouvrir le lot suivant |
| P5 — cloture parent | Les trois lots sont terminaux et les audits globaux couvrent leur union | Ne pas clore ce chantier mere |

## 4. Etat des lieux (avant/apres) — reutiliser avant de recreer

### Ce qui existe deja

- `code-architecture-evaluator/SKILL.md` contient une analyse d'impact et une
  checklist des dependances inversees, mais ne rend pas encore obligatoire la
  recherche des tests/consommateurs qui figent une configuration, un workflow,
  un schema ou un manifeste.
- `common/WORKFLOW.md` separe deja persistance, commit et push, mais ne traite
  pas explicitement le cas d'un gate distant qui impose un premier push avant
  un commit local de fermeture potentiellement publiable par un second push.
- `Test-EvidenceReferenceSubstance` rejette deja les chemins et ancres
  invalides. Pour une ancre absente, l'erreur ne donne que l'ancre demandee et
  le fichier; elle ne liste pas les slugs de titres acceptables.
- `PLAN_INTEGRATION_LEARN_SESSION_POST_CLOSE` est `DONE` dans le checkpoint et
  son changement est present dans `WORKFLOW.md`; ce n'est plus un brouillon
  concurrent.

### Ce qui manque reellement

- Une obligation concise, dans le skill existant, de rechercher les
  consommateurs contractuels avant de valider une modification de contrat.
- Une formulation d'autorisation couvrant sans ambiguite les deux publications
  potentielles d'un cycle avec gate distant.
- Un diagnostic de slug actionnable qui conserve le rejet fail-closed.
- Pour le Lot 1, une commande de validation existante ou creee dans le perimetre
  de l'enfant : le `quick_validate.py` cite par le brouillon n'existe pas et ne
  doit pas etre invente dans le parent.

## 5. Decision d'architecture

Le parent reste un document de coordination. Chaque amelioration touche un
proprietaire different et possede une preuve independante; les regrouper dans
un meme plan d'implementation augmenterait le couplage des autorisations, des
tests et des clotures sans benefice technique.

### Frontieres explicites (ce que chaque couche fait / ne fait pas)

| Couche | Fait | Ne fait pas |
| --- | --- | --- |
| Parent | Ordonne, journalise, pointe vers les enfants et controle la cloture globale | Modifier les proprietaires des Lots 1-3 |
| Enfant | Definit et execute un seul correctif avec ses consommateurs, tests et audits | Absorber un autre lot ou modifier le parent hors mise a jour de statut convenue |
| `plan.ps1` | Persiste les transitions autorisees dans le checkpoint | Creer une hierarchie parent/enfant ou attester la veracite semantique des preuves |

### Contrat d'interface entre les couches

- Chaque enfant est un workstream normal et autonome.
- Son `routing_reason` porte le lien narratif vers ce parent.
- Ce parent enregistre uniquement l'identifiant, l'etat terminal et la preuve
  de cloture de l'enfant.
- Un blocage ou report sur un lot ne bloque pas l'execution des autres, sous
  reserve d'une revalidation de l'ordre dans ce parent.

### Decisions deja actees

- Les trois propositions sont acceptees pour persistance.
- L'ordre propose est 1, 2, 3; il est organisationnel, pas technique.
- Aucun commit ou push n'est inclus dans l'autorisation actuelle.

### Structure cible

```text
EPIC_AMELIORATIONS_POST_RETROSPECTIVE_CI_NODE20
|- Lot 1 : consommateurs contractuels pendant /evaluate
|- Lot 2 : autorisation explicite des deux pushes potentiels
`- Lot 3 : diagnostic des ancres de preuve
```

### Perimetre de fichiers explicite (autorises / interdits)

Autorise pour ce chantier mere :

```text
.ai/backlog/fixes/EPIC_AMELIORATIONS_POST_RETROSPECTIVE_CI_NODE20.md
```

Mutation mecanique autorisee uniquement via `plan.ps1` :

```text
.ai/checkpoint.json
0 - HUMAN START HERE/archive/20260809_EPIC_AMELIORATIONS_POST_RETROSPECTIVE_CI_NODE20.md
```

Interdit au parent :

```text
Protocole/
Implementation/
.agents/skills/code-architecture-evaluator/SKILL.md
.ai/workflows/common/WORKFLOW.md
.ai/workflows/common/WORKFLOW.json
.ai/tools/workflow_state.ps1
.ai/tools/tests/test_workflow_state_machine.ps1
.ai/checkpoint.schema.json
```

## 6. Decoupage en phases

### Phase 1 - Sous-chantier 1 : consommateurs contractuels

Objectif : revalider, rediger, router, baseliner, executer, auditer et clore
le Lot 1 dans un workstream distinct.

Classification : GOVERNANCE

Actions :

- Identifier la validation reelle du skill avant d'ecrire l'Exit criteria de
  l'enfant; le lot a trouve et execute le validateur canonique du skill
  systeme `skill-creator/scripts/quick_validate.py`.
- Appliquer le cycle complet prescrit par `epic-orchestrator`.
- Reporter ici l'id, le statut terminal et la preuve de cloture.

Livrables :

- Plan enfant du Lot 1 et workstream terminal distinct.
- Mise a jour de ce parent vers le prochain lot realisable.

Critere de sortie :

- L'Exit criteria autonome du Lot 1 est prouve et aucun audit requis ne garde
  de finding ouvert.

Statut : `DONE` le 2026-08-09. Baseline `2a18343`, attestation `6234cae`,
cloture et implementation `cb02758`. `quick_validate`, forward-test,
adversarial-tester et plan-conformance-audit `PASS`; bug-hunter
`NON_APPLICABLE` car aucun fichier `Implementation/` n'a ete touche.

### Phase 2 - Sous-chantier 2 : autorisation de deux pushes potentiels

Objectif : revalider puis traiter le contrat conversationnel de publication
dans un workstream distinct.

Classification : GOVERNANCE

Actions :

- Rebaseliner l'enfant sur le `WORKFLOW.md` live, qui inclut deja
  l'integration post-close de `/learn-session`.
- Appliquer le cycle complet prescrit par `epic-orchestrator`.
- Reporter ici l'id, le statut terminal et la preuve de cloture.

Livrables :

- Plan enfant du Lot 2 et workstream terminal distinct.
- Mise a jour de ce parent vers le prochain lot realisable.

Critere de sortie :

- La portee d'autorisation des deux pushes potentiels est non ambigue et le
  lot n'a modifie ni `WORKFLOW.json`, ni les transitions executables.

Statut : `DONE` le 2026-08-09. Baseline `4c74d6a`, attestation `660411d`,
cloture et clarification `1ba3074`. Workflow state machine, assertions
contractuelles, adversarial-tester et plan-conformance-audit `PASS`;
bug-hunter `NON_APPLICABLE` car aucun fichier `Implementation/` n'a ete touche.

### Phase 3 - Sous-chantier 3 : diagnostic des ancres de preuve

Objectif : revalider puis ameliorer le diagnostic fail-closed dans un
workstream distinct.

Classification : IMPLEMENTATION_DETAIL

Actions :

- Verifier la fonction et les tests live avant de definir le diff enfant.
- Appliquer le cycle complet prescrit par `epic-orchestrator`, y compris les
  audits requis pour un artefact de workflow persiste.
- Reporter ici l'id, le statut terminal et la preuve de cloture.

Livrables :

- Plan enfant du Lot 3 et workstream terminal distinct.
- Diagnostic teste sans relachement de la validation des preuves.

Critere de sortie :

- Les cas d'ancre valide et invalide passent; l'invalide reste rejete et son
  message expose les seuls slugs de titres utiles.

Statut : `DONE` le 2026-08-09. Baseline `ff13683`, attestation `1ce398d`,
cloture et correctif `7a6de9b`. Harnais workflow, adversarial-tester et
plan-conformance-audit `PASS`; bug-hunter `NON_APPLICABLE` car aucun fichier
`Implementation/` n'a ete touche.

### Chemin critique (ordre des phases)

```mermaid
flowchart LR
    P1[Lot 1] --> U1[Mise a jour parent]
    U1 --> P2[Lot 2]
    P2 --> U2[Mise a jour parent]
    U2 --> P3[Lot 3]
    P3 --> A[Audits globaux parent]
    A --> C[Cloture parent]
```

Cet ordre est une preference de coordination. Les Exit criteria et les
blocages restent independants; le parent peut journaliser un reordonnancement
sans changer le sens d'un lot.

## 7. Artefacts produits

| Etape | Fichier/sortie | Format | Regle source |
| --- | --- | --- | --- |
| Coordination | Ce plan parent, mis a jour apres chaque lot | Markdown | `epic-orchestrator` |
| Lot 1 | Plan enfant puis modification du skill existant | Markdown | Workflow `common` |
| Lot 2 | Plan enfant puis clarification du workflow | Markdown | Workflow `common` |
| Lot 3 | Plan enfant, correctif PowerShell et tests | Markdown/PowerShell | Workflow `common` |

## 8. Invariants absolus et NO GO

### Invariants (non negociables dans le code)

1. Le parent ne porte aucune implementation des Lots 1-3.
2. Chaque lot possede un workstream, une baseline, un diff, des audits et une
   cloture distincts.
3. Le Lot 3 reste fail-closed : une ancre invalide ne devient jamais une preuve
   acceptable.
4. Une autorisation de persistance, commit ou premier push ne vaut jamais
   autorisation implicite du second push potentiel.
5. Le lien parent/enfant reste narratif sans changement de schema.

### NO GO (actions explicitement interdites — a verifier a chaque revue de diff)

- Fusionner deux lots ou leurs commits.
- Modifier `Protocole/`, `Implementation/` ou BACKTRADER.
- Creer un nouveau skill pour le Lot 1.
- Prescrire ou invoquer un script de validation absent.
- Modifier `WORKFLOW.json` pour une clarification conversationnelle.
- Afficher le contenu des preuves dans le diagnostic du Lot 3.
- Committer ou pousser sur la seule autorite de ce `/start`.

## 9. Verification a chaque etape

Apres le routage du parent :

```powershell
python -m json.tool .ai\checkpoint.json
python -c "import json, jsonschema; jsonschema.validate(json.load(open('.ai/checkpoint.json', encoding='utf-8')), json.load(open('.ai/checkpoint.schema.json', encoding='utf-8')))"
git diff --check -- .ai
```

Pour chaque enfant, le plan propre declare les commandes exactes de son
perimetre. Aucune commande absente du depot ne vaut preuve.

Premier lot executable propose apres convergence et baseline de ce parent :

```text
Creer uniquement le brouillon du Lot 1 apres revalidation de son proprietaire
et de ses consommateurs live.
```

### Execution sans interruption

Le parent enchaine les lots realisables sans demander de confirmation sur des
details deja bornes. Il s'arrete uniquement pour un blocage externe, une
decision hors perimetre, une extension de fichiers ou la fin verifiee de tous
les lots. Un lot bloque n'empeche pas de reevaluer et d'avancer un autre lot.

### Autorite decisionnelle accordee

L'IA peut maintenir ce document de coordination et preparer les cycles enfants
dans les frontieres declarees. Toute implementation reste soumise a la
baseline propre de l'enfant. Commit, push et publication exigent leurs
autorisations distinctes.

### Interdiction des raccourcis (aucun faux succes)

Un test en echec, un timeout, une absence de sortie, une preuve invalide ou un
audit avec finding ouvert reste non-PASS. Aucun test ne peut etre desactive ou
affaibli pour clore un lot.

## 10. Journal des decisions humaines (autorisations)

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-09 | `Je valide tes propositions`. | Autorise la persistance du chantier mere et confirme les trois orientations. N'autorise ni commit, ni push, ni publication externe. |
| 2026-08-09 | Lot 1 clos `DONE` par `cb02758`. | Gate contractuelle ajoutee au skill; autorise la reprise de la coordination sur le Lot 2 sans fusionner les lots. |
| 2026-08-09 | Lot 2 clos `DONE` par `1ba3074`. | Contrat A/B ajoute au workflow conversationnel sans changement executable; autorise l'ouverture du Lot 3. |
| 2026-08-09 | Lot 3 clos `DONE` par `7a6de9b`. | Diagnostic fail-closed et regressions livres; autorise l'audit global puis la cloture du parent. |

## 11. Risques et blocages connus

| Risque | Impact | Mitigation / condition de deblocage |
| --- | --- | --- |
| Le Lot 1 cible une validation inexistante | Risque clos : validateur canonique du skill systeme trouve et execute | `quick_validate.py` PASS et forward-test comportemental PASS dans `cb02758` |
| Le Lot 2 entre en collision avec un changement ulterieur de `WORKFLOW.md` | Clarification redigee sur une base obsolete | Relecture et rebaseline live juste avant le plan enfant |
| Le diagnostic du Lot 3 devient verbeux ou divulgue une preuve | Bruit ou exposition de contenu | Limiter la sortie aux slugs de titres, avec tests exacts |
| Le parent est traite comme un plan d'implementation directe | Fusion des autorisations et clotures | Carte d'execution et invariant MULTI_LOT bloquants |

## 12. Definition of Done

- [ ] Portee `meta`, track `fix`, classification `GOVERNANCE` et workflow
      `common` restent coherents avec le sujet reel.
- [ ] Lots 1, 2 et 3 `DONE` ou explicitement differes par decision humaine.
- [ ] Chaque lot possede son propre cycle complet et son propre commit.
- [ ] Audit final bug-hunter applicable sur l'union des fichiers touches par
      les lots, depuis la baseline du parent, sans finding ouvert.
- [ ] Audit de conformite du parent contre ses Exit criteria sans manque.
- [ ] Aucun fichier humain parallele absorbe ou modifie.
- [ ] Checkpoint valide apres chaque transition.
- [ ] Aucun commit ou push realise sans autorisation correspondante.

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat final | A renseigner lors de `/close` |
| Ecarts par rapport au plan initial | A renseigner lors de `/close` |
| Suites a prevoir (hors perimetre de ce plan) | A renseigner lors de `/close`; aucune cascade automatique |

### Resultat d'execution (a dupliquer a chaque session d'execution significative)

| Champ | Valeur |
| --- | --- |
| Date | 2026-08-09 |
| Phases executees | Promotion/baseline du parent puis Lots 1, 2 et 3 complets |
| Artefact produit | Gate 2 bis du skill `/evaluate`; contrat A/B; diagnostic d'ancres et regressions |
| Validation | Trois lots `DONE`; validations propres, adversarial et conformite PASS; checkpoint valide |
| Ecart par rapport au plan | Lot 2 a corrige le proprietaire documentaire; Lot 3 a remplace une fixture sans-titre invalide apres un premier `FAIL_TEST`; aucun relachement fonctionnel |

## 14. Journal d'audits post-hoc

### Journal de convergence de l'intake

| Passe | Date | Constat | Correction appliquee | Resultat |
| --- | --- | --- | --- | --- |
| `/evaluate` 1 | 2026-08-09 | Le brouillon traite encore `PLAN_INTEGRATION_LEARN_SESSION_POST_CLOSE` comme non suivi, alors qu'il est `DONE`; il prescrit `quick_validate.py`, absent du depot; les trois proprietaires et leurs consommateurs reels confirment toutefois trois Exit criteria autonomes. | Etat live actualise; collision reclassee en obligation de relecture live; preuve inexistante retiree et remplacee par l'obligation d'identifier une validation executable dans le lot enfant. | Corrections majeures appliquees; seconde passe requise. |
| `/evaluate` 2 | 2026-08-09 | Relecture du plan corrige contre le checkpoint, `WORKFLOW.md`, le skill cible, `workflow_state.ps1` et ses tests. Aucune dependance technique entre les trois lots; aucun besoin de schema ou de changement normatif. | Frontieres parent/enfants, gates de progression, perimetres et commandes de validation du parent rendus explicites. | `CONVERGE` — aucun nouvel angle mort majeur. |

### Journal d'audits post-route

#### Passe 1 — `/evaluate` du plan normalise

1. **Resume executif** : `VALIDE`, risque `MINIMAL` pour le parent lui-meme,
   coherence forte avec le workflow `common` et le garde-fou multi-lot.
2. **Points forts** : les trois proprietaires sont distincts; chaque Exit
   criteria est autonome; le parent n'autorise aucune implementation directe;
   le checkpoint n'est pas etendu.
3. **Points faibles et incoherences** : aucun blocage. Point de vigilance
   modere : une commande de validation enfant ne peut pas etre figee par le
   parent avant l'inventaire live de ses consommateurs; le cas
   `quick_validate.py` absent demontre ce risque.
4. **Angles morts** : migration de donnees, deploiement et monitoring sont non
   applicables au parent documentaire; ruptures de contrat, tests,
   dependances inversees et documentation sont explicitement delegues a
   chaque plan enfant apres revalidation live.
5. **Standards** : responsabilite unique respectee par la separation
   parent/ Lots 1-3; dependances inversees traitees par l'inventaire impose
   avant redaction de chaque enfant; aucune nouvelle abstraction proposee.
6. **Plan rectifie** : conserver les trois phases de coordination et
   l'interdiction de prescrire une validation absente; aucune modification
   structurelle supplementaire necessaire.

Resultat : `CONVERGE`, sans finding bloquant.

#### Passe 2 — contre-audit apres la passe 1

1. **Resume executif** : `VALIDE`, risque residuel `MINIMAL`, aucune decision
   humaine manquante avant baseline du parent.
2. **Points forts** : la Carte d'execution interdit `/continue` direct sur le
   parent; les IDs enfants sont parsables par `plan.ps1`; les autorisations de
   commit et de push restent separees.
3. **Points faibles et incoherences** : aucun nouvel ecart majeur; les risques
   restants sont locaux aux futurs enfants et deja assortis d'une condition de
   deblocage en section 11.
4. **Angles morts** : les huit familles de la checklist du skill ont ete
   rejouees; aucune ne requiert d'elargir le perimetre du parent.
5. **Standards** : separation des responsabilites, faible couplage et
   validation fail-closed preserves.
6. **Plan rectifie** : aucune nouvelle correction; plan pret a etre fige en
   baseline pre-implementation.

Resultat : `CONVERGE` en 2 passes post-route, aucun nouvel angle mort majeur.
