---
name: epic-orchestrator
description: A invoquer quand un brouillon d'intake, une observation, ou une demande humaine decrit plusieurs sous-chantiers distincts qui ne doivent pas etre fusionnes dans un seul plan (ex. plusieurs "lots" independants issus d'un meme audit) — voir "Test de detection" ci-dessous pour un critere verifiable. OBLIGATOIRE, pas optionnel, a deux moments precis : (1) au moment d'auditer/structurer un brouillon via /start, avant de choisir entre gabarit simple ou chantier mere ; (2) au moment de /continue sur un workstream existant — si son plan reussit le test de detection, /continue ne doit PAS demarrer une implementation de code directe, il doit d'abord appliquer ce skill. Structure un chantier mere de suivi qui coordonne l'execution successive de chaque sous-chantier via son propre cycle complet /start -> /evaluate x2 -> baseline -> /continue -> bug-hunter + plan-conformance-audit -> /close, sans jamais fusionner deux lots ni dupliquer leur contenu dans le document de suivi. Ne s'applique pas a un brouillon qui decrit un seul chantier coherent, meme complexe.
---

# Role

Ce depot a deja recree, plusieurs fois, le meme probleme : un audit ou une
observation identifie plusieurs corrections independantes ("lots"), chaque
lot est traite comme une note d'intake isolee, et des que plus d'un lot
existe en parallele, l'humain perd la vue d'ensemble (id a retrouver, ordre
a rededuire, decisions humaines eparpillees dans plusieurs fichiers). Ce
skill existe pour que ce cas produise systematiquement **un seul point
d'ancrage** (le "chantier mere") plutot que des chantiers disperses.

Precedent reel ayant motive ce skill : `.ai/backlog/fixes/EPIC_CLOTURE_ATTESTATIONS_RESIDUELLES_GATES.md`,
qui coordonne trois lots (branchements mecaniques, calcul de puissance
manquant, decision de seuil d'execution) issus d'une meme observation
d'intake. Voir `EXAMPLE_REPORT.md` pour le detail de ce cas, y compris les
erreurs commises et corrigees en le construisant.

# Test de detection (a appliquer, pas a supposer)

Un brouillon, une observation, ou un plan deja route est **multi-lot**
(declenche ce skill) si, pour au moins deux composantes qu'il decrit, les
trois conditions suivantes sont TOUTES vraies :

1. Chaque composante a son propre Exit criteria verifiable **sans dependre
   de l'etat des autres** (fermer l'une ne suppose pas que l'autre soit
   faite).
2. Chaque composante pourrait etre routee, implementee et cloturee dans un
   ordre different de celui propose, sans changer son sens.
3. Un blocage sur une composante (ex. decision humaine en attente) n'empeche
   pas les autres d'avancer.

A l'inverse, un plan reste **single-chantier** (le gabarit normal suffit,
`## 6. Decoupage en phases` de `.ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md`)
si ses phases sont sequentielles et interdependantes : la phase N+1 n'a de
sens que si la phase N est faite, et un seul jeu d'Exit criteria couvre
l'ensemble. Un plan qui a des "Phases" au sens du gabarit n'est pas
automatiquement multi-lot — ne pas confondre decoupage en phases d'un meme
chantier et lots independants.

Exemple deja rencontre dans ce depot : `EPIC_CLOTURE_ATTESTATIONS_RESIDUELLES_GATES`
est multi-lot (Lot C peut se clore sans que A2 ou B soient faits, dans un
ordre qui a ete revise en session sans changer le sens d'aucun lot). A
l'inverse, un plan comme `PLAN_CORRECTION_GATES_MECANIQUES_LOT_C` (un des
lots lui-meme) n'est PAS multi-lot malgre ses deux phases internes (Phase 1
"corriger l'assemblage", Phase 2 "preuve de non-regression") : la Phase 2
n'a de sens que si la Phase 1 est faite, un seul Exit criteria couvre les
deux.

# Quand s'invoquer (deux points de controle obligatoires)

1. **Au moment d'auditer un brouillon via `/start`** : applique le test de
   detection ci-dessus AVANT de choisir la structure (gabarit simple vs
   chantier mere + lots). Documente explicitement le resultat du test dans
   le bandeau de statut du plan que tu rediges — ne le laisse pas implicite.
2. **Au moment de `/continue` sur un workstream existant** : avant
   d'implementer la moindre ligne de code, relis son plan
   (`checkpoint.json::workstreams[].source_path`) et reapplique le test de
   detection. Si le plan reussit le test (il coordonne des lots
   independants, meme si ce n'etait pas explicite au moment de sa
   redaction), **l'implementation directe est interdite** — applique
   d'abord la Procedure ci-dessous. Un plan peut reussir ce test alors que
   son auteur ne l'avait pas structure comme un chantier mere (redaction
   initiale imparfaite, ou drift depuis) : le test se rejoue sur l'etat
   actuel du plan, pas sur l'intention d'origine.
3. Une demande humaine explicite de regrouper des sous-chantiers epars pour
   ne pas les perdre de vue declenche aussi ce skill directement, sans
   attendre le prochain `/start`/`/continue` (le declencheur qui a produit
   ce skill).

# Contrainte structurelle a respecter

`.ai/checkpoint.schema.json` n'a pas de notion de `parent_workstream_id`
(`additionalProperties: false` partout) et
`.ai/governance/AI_MODIFICATION_CHECKLIST.md` n'autorise une modification du
schema que si "le schema existant le permet proprement" — **ne jamais
etendre ce schema pour ce besoin**. Le lien parent/enfant reste narratif :

- Le chantier mere devient un workstream normal (`track: fix` ou `mainline`
  selon le cas, `classification` la plus adaptee) dont le `source_path`
  pointe vers un document qui **coordonne sans implementer**.
- Chaque lot devient son propre workstream `fix`/`mainline` distinct
  (obligatoire mecaniquement : `plan.ps1 start` exige un brouillon original
  propre par chantier). Son `routing_reason` commence par
  `"Sous-chantier <n>/<total> de <ID_CHANTIER_MERE>"` pour rester tracable
  sans lien structurel.

# Procedure

## 1. Rediger le chantier mere

Ecrire un document (dans `0 - HUMAN START HERE/` puis restructure et route
comme n'importe quel plan) qui :

- Enumere chaque lot identifie, avec sa nature (mecanique / calcul manquant
  / decision de seuil requise) **verifiee dans le code reel**, pas recopiee
  d'une classification anterieure sans validation (voir garde-fou
  ci-dessous).
- Fixe un ordre d'execution explicite et sa justification.
- Journalise les decisions humaines deja actees (section 10 du gabarit) et
  identifie precisement lesquelles restent a trancher.
- Ne modifie et ne code **rien** lui-meme — son perimetre de fichiers
  autorises se limite a sa propre mise a jour (section "Suite immediate").
- Route-le via `plan.ps1 start -Audited` comme tout plan.

## 2. Boucle par lot, jusqu'a cloture generale

Pour le prochain lot indique par le chantier mere :

1. **Avant de rediger quoi que ce soit** : revalide dans le code reel, tel
   qu'il est aujourd'hui, la nature attribuee a ce lot par le chantier mere
   ou par l'observation source. Une classification peut avoir ete une
   erreur d'estimation initiale (deja arrive : un lot suppose "mecanique" et
   "le plus urgent" s'est revele etre un calcul manquant apres lecture du
   code). Si ta verification contredit le chantier mere, corrige-le d'abord,
   ne redige jamais un plan de lot sur une hypothese que tu sais fausse.
2. Si le plan du lot n'existe pas encore : redige un brouillon dans
   `0 - HUMAN START HERE/`, puis boucle `/evaluate` (skill
   `code-architecture-evaluator`) EN PLACE sur ce brouillon, minimum 2
   passes, corrige entre chaque passe, converge avant de continuer.
3. `/start` : structure le plan selon
   `.ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md`, route-le
   (`plan.ps1 start -Audited`). Si un plan de ce lot existe deja et est
   `TRIAGED` (redige lors d'une session anterieure), passe directement a
   l'etape suivante sur ce plan existant.
4. Boucle `/evaluate` a nouveau sur le plan restructure et route, minimum 2
   passes, converge. Ne pas sauter cette seconde boucle sous pretexte que la
   premiere (etape 2) a converge — un plan pleinement structure contre le
   gabarit peut reveler un angle mort absent du brouillon.
5. Valide `.ai/checkpoint.json` (syntaxe + schema) suite au `plan.ps1 start`.
   Si la validation echoue, corrige avant de committer quoi que ce soit.
   Sinon, commit la baseline pre-implementation du plan converge (format de
   commit du depot, voir `AGENTS.md`).
6. `plan.ps1 continue`, implemente exactement ce que le plan du lot
   prescrit, verifie avec la suite de tests du depot a chaque phase.
7. Applique `.agents/skills/bug-hunter/SKILL.md` puis
   `.agents/skills/plan-conformance-audit/SKILL.md` sur les fichiers
   touches par CE lot. Si l'un des deux releve un probleme ouvert,
   corrige-le avant de continuer.
8. `plan.ps1 close -Outcome DONE`. Valide `.ai/checkpoint.json` (et
   `Implementation/Active/tracking.json` si touche) contre leur schema.
   Seulement si la validation passe : commit scope aux fichiers touches par
   la cloture.
9. Mets a jour le chantier mere (section "Suite immediate"/decisions) pour
   refleter la cloture et pointer vers le lot suivant.
10. Si le lot suivant necessite une decision humaine non encore tranchee
    (deja identifiee dans le chantier mere, ou decouverte a l'etape 1
    ci-dessus) : arrete-toi, demande-la explicitement, journalise la reponse
    dans le chantier mere, puis reprends depuis l'etape 1 pour ce lot.
    N'invente jamais une decision de seuil ou de methode a la place de
    l'humain.
11. Sinon, reprends depuis l'etape 1 pour le lot suivant.

## 3. Cloture generale du chantier mere

Quand plus aucun lot ne reste (tous `DONE`, ou explicitement differes par
une decision humaine journalisee) :

1. Applique `.agents/skills/bug-hunter/SKILL.md` en balayage complet sur
   l'union des fichiers touches par TOUS les lots executes — identifie cette
   union via `git diff --stat <commit-de-baseline-du-chantier-mere>..HEAD`,
   pas seulement les fichiers du dernier lot clos.
2. Applique `.agents/skills/plan-conformance-audit/SKILL.md` contre les Exit
   criteria du chantier mere lui-meme (pas seulement ceux de chaque lot).
3. Si l'un des deux releve un probleme, corrige-le (ou ouvre un lot
   supplementaire si la correction depasse le perimetre d'un lot deja clos).
4. `plan.ps1 close` sur le chantier mere. Valide `.ai/checkpoint.json`
   contre son schema ; seulement si la validation passe, commit avec la
   section Cloture remplie.

# Regle de blocage

- Ne jamais lancer `plan.ps1 continue` puis coder directement sur un
  workstream dont le plan reussit le test de detection sans etre passe par
  la Procedure ci-dessous — ce n'est pas une preference, c'est bloquant au
  meme titre que l'interdiction de `plan.ps1 close` sans bug-hunter/
  plan-conformance-audit.
- Ne jamais fusionner deux lots dans un seul commit, une seule boucle
  `/evaluate`, ou une seule cloture.
- Ne jamais rediger le plan d'un lot sur une classification non revalidee
  dans le code reel (etape 1 de la boucle).
- Ne jamais inventer une decision de seuil, de methode statistique, ou de
  norme a la place de l'humain — s'arreter et demander.
- Ne jamais etendre `.ai/checkpoint.schema.json` pour representer le lien
  parent/enfant.

# Ce que ce skill ne fait pas

- Il ne remplace pas `code-architecture-evaluator`, `bug-hunter`, ou
  `plan-conformance-audit` — il les invoque, au niveau du lot et au niveau
  du chantier mere.
- Il ne decide pas a la place de l'humain quel lot traiter en premier ni
  quelle decision de seuil/methode retenir — il structure la coordination,
  jamais le jugement de fond.
- Il ne cree pas de hierarchie structurelle dans `.ai/checkpoint.json` — le
  lien parent/enfant reste toujours narratif (voir "Contrainte structurelle
  a respecter").
