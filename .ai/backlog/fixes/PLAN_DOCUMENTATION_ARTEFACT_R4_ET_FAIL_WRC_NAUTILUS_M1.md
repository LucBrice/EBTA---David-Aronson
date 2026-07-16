# Plan de correction — documenter l'artefact `PASS` R4 et le `FAIL` WRC primaire legitime (Nautilus M1), debloquer la cloture de G5

> Chantier `fix`, suite directe de la section 13 de
> `.ai/backlog/fixes/PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE.md` et de la
> decision humaine du 2026-07-16 tranchee dans le brouillon d'origine
> `0 - HUMAN START HERE/OBSERVATION_WRC_PRIMAIRE_PACKAGE_NAUTILUS_M1_FAIL.md`
> (archive via `plan.ps1 start`). Ce chantier est **de documentation et de
> gouvernance** : il n'ecrit aucune nouvelle logique de calcul, ne force
> aucun statut, ne recalibre aucun seuil. Le correctif de code sous-jacent
> (extraction NAV Nautilus) est deja livre et commite (`ebff49d`).

---

## 0. Bandeau de statut (verifie sur l'etat machine reel)

| Question | Reponse |
| --- | --- |
| Un chantier actif couvre-t-il deja ce perimetre ? | Partiellement : `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE` (`ACTIVE`) a revele le probleme mais s'est arrete avant `/close`. **Precision verifiee (ligne 54 de G5)** : ce blocage venait d'une *attente de l'etape de verification* de G5 (section 9, ligne ~428 : `report["status"] == "PASS"` attendu sur le package MVP), PAS d'un des 5 Exit criteria formels de G5 (qui portent tous sur la propagation de `pre_oos_robustness_verdict`, aucun n'exige un package WRC `PASS`). Ce chantier-ci prend la suite explicitement designee par la section 13 de G5. Il ne duplique pas G5 : G5 = propagation du verdict robustesse pre-OOS vers G5/`gates.json` ; ce chantier = documentation de l'incoherence WRC/R4 + deblocage de la cloture de G5. |
| Un verrou de gouvernance actif bloque-t-il ce chantier ? | Oui, un garde-fou normatif permanent (pas un verrou levable) : interdiction de forcer `wrc_status = PASS`, de calibrer un seuil silencieusement, ou de modifier `Protocole/` (SOP 02) / `procedures/wrc.py`. Ce chantier respecte ce garde-fou par construction (il documente, il ne recalcule pas). |
| Ce plan a-t-il besoin d'une decision humaine explicite avant d'etre routable ? | Non pour le routage : les deux decisions de gouvernance requises sont deja prises (2026-07-16, section 10). Une seule confirmation reste requise a l'interieur du chantier (Phase 3 : accepter de clore G5 independamment du statut WRC primaire, G5 et G4 etant des gates distincts). |
| Ce plan remplace-t-il un document ou chantier existant ? | Non. Il complete G5 (qui reste `ACTIVE` jusqu'a sa cloture en Phase 3) et documente retrospectivement l'archive R4 sans la reecrire. |

> La deuxieme question repond "oui" a un garde-fou *permanent*, pas a un
> verrou *levable* : aucune decision humaine ne peut autoriser a forcer
> `wrc_status = PASS`. Ce plan est routable car il ne demande jamais cette
> levee — il travaille dans le cadre du garde-fou.

---

## Audit IA de promotion

- [x] Plan relu dans le contexte du cockpit actif (`AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json`, `Implementation/Active/HOOK.md`, plan G5, historique moteur).
- [x] Bandeau de statut (section 0) rempli et verifie contre l'etat machine reel (commits `ebff49d`, `50f3e3b` verifies ; `wrc.json` verifie ; `_call_float` au commit `3bcfe35` verifie par `git show`).
- [x] Ce plan est ECRIT COMME NOUVEAU FICHIER dans `.ai/backlog/fixes/` ; le brouillon original reste intact dans `0 - HUMAN START HERE/` jusqu'a l'archivage mecanique par `plan.ps1 start`.
- [x] Chantier classe `fix` (suite d'un chantier `fix`, correction/reconciliation ciblee, pas une nouvelle capacite mainline ni une annexe exploratoire).
- [x] Autorite(s) normative(s) identifiee(s) : SOP 02 (WRC primaire), SOP 08 (NAV/rendements de reference), `REGISTRE DES DECISIONS NORMATIVES EBTA.md`.
- [x] Perimetre de fichiers autorises/interdits explicite (liste fermee, section 5).
- [x] Aucune modification hors perimetre requise pour activer le chantier (le correctif de code est deja commite ; ce chantier ne touche que de la documentation et l'etat machine).
- [x] Prerequis factuels identifies (section 11) : stabilisation du depot deja faite (Phase 0 close par commits).
- [x] Etat des lieux (section 4) verifie : aucune duplication de logique proposee (ce chantier n'ecrit pas de code de calcul).

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `fix` |
| Lifecycle | `TRIAGED` |
| Scope | Documenter, dans les traces normatives et l'etat machine, que le `PASS` clos par R4 le 2026-07-15 etait un artefact d'une NAV degenerescente et que le `FAIL` WRC primaire courant du package Nautilus M1 est un verdict de recherche legitime, puis debloquer et executer la cloture de `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE`. |
| Non-goals | Ne PAS forcer `wrc_status`/`verdict` a `PASS` ; ne PAS calibrer un seuil (`alpha`, seuils SOP 08) ; ne PAS modifier `Protocole/`, SOP 02, `procedures/wrc.py`, ni le code moteur deja commite dans `ebff49d` ; ne PAS reecrire le `closure_reason` archive de R4 ni son fichier d'archive ; ne PAS ouvrir de chantier de recherche sur la famille de candidats M1 (edge non demontrable = documente, pas investigue) ; ne PAS re-executer/modifier BACKTRADER. |
| Source | Section 13 de `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE.md` ("priorite immediate : ouvrir un chantier separe") + decisions humaines explicites du 2026-07-16 (voir section 10), tranchees a partir de `0 - HUMAN START HERE/OBSERVATION_WRC_PRIMAIRE_PACKAGE_NAUTILUS_M1_FAIL.md`. |
| Exit criteria | (1) Une entree tracee dans `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` acte explicitement que le `PASS` R4 reposait sur une NAV degenerescente ET que le `FAIL` WRC primaire courant est un verdict EBTA legitime (famille M1 sans edge demontrable sur ce segment). (2) `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE` est clos via `.ai/tools/plan.ps1 close` (issue `DONE` ou `BLOCKED` explicitement justifiee), et `.ai/checkpoint.json` reflete l'etat. (3) La suite de tests runtime reste `PASS` (152 tests) et aucun `Protocole/`, `procedures/wrc.py` ou seuil n'a ete modifie (verifiable par `git diff`). |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `NON_DEMARRE` |
| Date de creation | 2026-07-16 |
| Date d'activation | - |
| Autorite normative | `Protocole/` (SOP 02 WRC primaire, SOP 08 NAV/rendements, `REGISTRE DES DECISIONS NORMATIVES EBTA.md`) |
| Autorite executable | `Implementation/ebta_engine/` (deja corrige, non retouche ici) ; `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` + `.ai/` pour la trace |
| Changement normatif attendu | Aucun |
| Dependances externes | NautilusTrader via venv dedie (`Implementation/adapters/nautilus_env/venv`), en lecture seule / reproduction facultative (Phase 1). Aucune autre. |

---

## 1. Role de ce document et non-objectifs

| Element | Role |
| --- | --- |
| `Protocole/` (SOP 02, SOP 08) | Autorite normative : ce qui definit un WRC primaire valide et une NAV/serie de rendements de reference. Prime sur tout. |
| `Implementation/ebta_engine/` | Traduction executable. Deja corrigee (`ebff49d`) ; ce chantier ne la retouche pas. |
| `.ai/` (checkpoint, backlog) | Cockpit d'orchestration, non normatif : ne produit jamais un verdict scientifique, seulement l'etat des chantiers. |
| `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` | Artefact de preuve final de ce chantier : la trace documentaire acquittant l'artefact R4 et le `FAIL` legitime. |
| Ce plan | Carte d'execution : quoi documenter, ou, pourquoi, dans quel ordre, et comment clore G5 proprement. |

Non-objectifs (ce que ce document lui-meme ne fait pas) :

- ne pas reecrire `Protocole/` ni aucune SOP ;
- ne pas introduire de regle, seuil ou statut absent de l'autorite normative ;
- ne pas faire du cockpit `.ai/` une source de verdict scientifique ;
- ne pas transformer un constat documentaire en recalcul silencieux du WRC.

---

## 2. Contexte obligatoire a lire avant de coder

1. `0 - HUMAN START HERE/archive/20260716_OBSERVATION_WRC_PRIMAIRE_PACKAGE_NAUTILUS_M1_FAIL.md` — le brouillon d'origine archive (par `plan.ps1 start` le 2026-07-16), qui porte le constat complet (Q1/Q2), les decisions, et le squelette repris ici. **A lire en premier** : tout le raisonnement y est.
2. `.ai/backlog/fixes/PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE.md` section 13 — le chantier parent, son blocage `/close`, et la designation explicite de cette suite.
3. `.ai/checkpoint.json` — etat machine courant : `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE` est `ACTIVE` ; ce chantier apparaitra apres `plan.ps1 start`.
4. `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`, entree "2026-07-16 - Stabilisation du build Nautilus M1 et extraction NAV" — documente deja le correctif technique et conclut "Ne pas forcer `wrc_status` a `PASS`. Une decision humaine ou un chantier dedie est requis" (ce chantier).
5. SOP 02 (WRC primaire) et SOP 08 (NAV/rendements de reference) dans `Protocole/` — pour verifier que documenter un `FAIL` honnete est conforme (le WRC est concu pour produire des `FAIL`), et qu'aucune tolerance ne permet de le convertir en `PASS`.

**Hierarchie d'autorite applicable** (copiee de `CLAUDE.md` / `AGENTS.md`, non inventee) :

```text
1. Protocole/MANIFESTE DE GEL EBTA.md
2. Protocole/PROTOCOLE EBTA.md
3. Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md
4. SOPs (SOP 02, SOP 08, ...)
5. Protocole/PAQUET D'EXECUTION EBTA.md
6. Implementation/
7. Adaptateurs externes (NautilusTrader au bord de l'adaptateur)
```

Regle : si le code contredit l'autorite normative, **c'est le code qui a
tort**. Un WRC primaire `FAIL` est un resultat normatif valide, jamais un
bug a "reparer".

---

## 4. Etat des lieux (avant/apres) — reutiliser avant de recreer

### Ce qui existe deja

| Module actuel | Chemin | Role reel (verifie) | Suffisant pour l'objectif ? |
| --- | --- | --- | --- |
| Extraction NAV Nautilus corrigee | `Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py::_call_float` (l.167) + `nautilus_mapping.py::_money_float` (l.490) | Gerent desormais le mapping `{Currency: Money}` ; NAV non nulle. Deja commite (`ebff49d`). | ✅ ne pas retoucher |
| WRC primaire | `Implementation/ebta_engine/procedures/wrc.py` | Calcule le WRC (5000 replications). Produit le `FAIL` courant sur rendements reels. | ✅ intouchable (gele) |
| Historique moteur | `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` | Journal normatif des versions moteur ; contient deja l'entree du correctif technique. | ⚠️ a etendre (ajouter l'acquittement gouvernance) |
| Backend de cockpit | `.ai/tools/plan.ps1` | Route/active/clot les chantiers et met a jour `checkpoint.json`. | ✅ a utiliser pour la cloture G5 (Phase 3), ne pas editer `checkpoint.json` a la main |
| Preuve du mecanisme d'artefact | `git show 3bcfe35:.../nautilus_strategy_bridge.py` | `_call_float` sans gestion dict au commit de cloture R4 -> equity `0.0` -> `daily_returns` nuls. | ✅ deja etabli, a citer (pas a re-decouvrir) |

### Ce qui manque reellement

| Brique manquante | Ou l'ecrire | Source de la regle | Ce qui existe deja et doit etre reutilise |
| --- | --- | --- | --- |
| Acquittement documentaire de l'artefact R4 + du `FAIL` legitime | Nouvelle entree dans `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` | Decision humaine 2026-07-16 (section 10) ; SOP 02 | L'entree "2026-07-16 - Stabilisation..." existe deja ; ne PAS la reecrire, en AJOUTER une nouvelle qui la reference |
| Cloture propre de G5 | `.ai/tools/plan.ps1 close -Id PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE` | Exit criteria de ce plan + section 13 de G5 | Le mecanisme de cloture existe (`plan.ps1`) ; ne pas l'improviser a la main |

Aucun module de calcul n'est a creer. **Toute proposition d'ecrire une
nouvelle logique WRC/NAV serait une regression** : la logique existe et est
gelee/corrigee.

---

## 5. Decision d'architecture

Principe directeur : **separer strictement la trace documentaire (ce que
ce chantier produit) du calcul scientifique (deja gele/corrige).** Ce
chantier n'ajoute aucune ligne de logique executable ; il rend
verifiable, dans les traces normatives, une conclusion deja etablie par le
code et l'archeologie git.

- Raison 1 (auditabilite) : un futur auditeur qui lit l'archive R4 y voit
  `PASS` ; sans une entree tracee ailleurs, il n'a aucun moyen de savoir que
  ce `PASS` etait un artefact. La trace ferme ce trou sans falsifier
  l'archive (append-only de l'histoire, jamais reecriture).
- Raison 2 (non-contamination normative) : documenter un `FAIL` comme
  legitime au lieu de le "corriger" preserve exactement la protection
  anti-data-snooping que SOP 02 doit produire. Convertir ce `FAIL` en `PASS`
  contaminerait la norme.

### Frontieres explicites

| Couche | Elle fait | Elle NE fait PAS |
| --- | --- | --- |
| Trace documentaire (`HISTORIQUE...md`, `.ai/`) | Acte l'artefact R4 et le `FAIL` legitime ; reconcilie l'etat des chantiers | Ne recalcule aucun WRC, ne touche aucun seuil, ne modifie aucune archive |
| Cockpit (`plan.ps1`, `checkpoint.json`) | Clot G5 et ce chantier | N'emet aucun verdict scientifique |
| Moteur (`ebta_engine/`) | Deja corrige (`ebff49d`) | N'est PAS retouche ici |

### Decisions deja actees

| Decision | Justification |
| --- | --- |
| Correctif code deja commite separement (`ebff49d`) hors de ce chantier | Le correctif est un `fix` moteur, distinct de l'acte documentaire ; separer garde chaque commit mono-sujet (cf. `feedback-commit-message-format`) |
| Etat du depot deja stabilise (commits `ebff49d`, `50f3e3b`) | La "Phase 0 - stabiliser le depot" du brouillon est deja executee ; ce plan la marque close, il ne la re-propose pas |
| Reproduction depuis `3bcfe35` rendue FACULTATIVE | Le mecanisme est deja confirme par `git show` + observation empirique de l'auteur du correctif (NAV=0.0, documentee dans `HISTORIQUE`) ; un rebuild du venv Nautilus a un vieux commit est couteux et fragile pour une certitude marginale |

### Perimetre de fichiers explicite (autorises / interdits)

**Autorises (creer ou modifier)** :

```text
Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md   [MODIFIER - Phase 2 : nouvelle entree d'acquittement]
.ai/backlog/fixes/PLAN_DOCUMENTATION_ARTEFACT_R4_ET_FAIL_WRC_NAUTILUS_M1.md   [MODIFIER - ce plan : sections 13/14 a la cloture]
.ai/checkpoint.json                                     [MODIFIER UNIQUEMENT via .ai/tools/plan.ps1 - Phase 3, jamais a la main]
.ai/backlog/fixes/PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE.md   [MODIFIER section 13 "Resultat final" avant cloture (Phase 3), PUIS deplace par plan.ps1 close vers .ai/archive/. plan.ps1 close n'edite pas le corps markdown - la section 13 doit etre passee de "NON CLOTURE" a l'issue reelle (DONE/BLOCKED) AVANT l'archivage, sinon le fichier archive se contredit]
```

**Interdits (ne jamais modifier dans ce chantier)** :

```text
Protocole/                                              [NORME - intouchable]
Implementation/ebta_engine/procedures/wrc.py            [GELE - logique WRC]
Implementation/ebta_engine/ (tout code moteur)          [DEJA CORRIGE dans ebff49d - ne pas retoucher]
Implementation/ebta_engine/ (seuils, alpha, SOP 08)     [CALIBRATION HUMAINE - ne jamais toucher]
.ai/archive/20260715_PLAN_R4_...PRODUCTION.md           [ARCHIVE DONE - jamais reecrite]
closure_reason de R4 dans .ai/checkpoint.json           [HISTORIQUE - append une trace, jamais reecrire l'existant]
```

---

## 6. Decoupage en phases

> Convention de chunking mecanique respectee (`### Phase <id> - <titre>`,
> labels `Objectif :` / `Actions :` / `Livrables :` / `Critere de sortie :`
> en texte simple suivis de listes `- `), pour `.ai/tools/tasks_from_plan.ps1`.

### Phase 0 - Stabilisation du depot (DEJA EXECUTEE)

Objectif : garantir que le chantier s'execute sur un etat de depot stable.

Classification : GOVERNANCE

Constat (pourquoi cette phase existait) :

- Le brouillon d'origine (section 1.3) listait 4 fichiers hors perimetre G5 non commites ; enqueter sur un etat mouvant est interdit.

Actions :

- (FAIT) Committer le correctif NAV + stabilisation build M1 (`ebff49d`, 7 fichiers, 152/152 tests PASS).
- (FAIT) Committer l'activation du workstream G5 et sa section 13 actualisee (`50f3e3b`, `checkpoint.json` valide contre son schema).

Livrables :

- Commits `ebff49d` et `50f3e3b` (deja presents dans l'historique git).

Critere de sortie :

- `git status` ne montre plus de modification hors perimetre non commitee (verifie : seul le brouillon d'intake reste, il sera archive par `plan.ps1 start`). PHASE CLOSE.

### Phase 1 - Consolider la preuve de l'artefact R4 (Q1)

Objectif : figer, de maniere citable, la preuve que le `PASS` R4 reposait sur une NAV degenerescente.

Classification : GOVERNANCE

Constat (avec preuve) :

- `git show 3bcfe35:Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py` montre `_call_float` avec `float(str(result).split()[0])` et **sans** gestion du mapping `{Currency: Money}` -> `equity()` renvoyait `0.0` a chaque barre M1 au commit de cloture R4.
- `nautilus_mapping.py::_extract_nav_series` lit `strategy._nav_snapshots` (rempli par `_record_nav_snapshot` -> `_call_float`), donc `nav = [0.0, ...]` -> `_returns_from_nav` -> `daily_returns` tous nuls.
- L'auteur du correctif a observe empiriquement NAV=0.0 (motivant le fix), deja documente dans `HISTORIQUE...md`.

Actions :

- Rassembler ces trois elements de preuve dans la redaction de l'entree de Phase 2 (pas de fichier separe).
- (FACULTATIF, si le venv Nautilus est disponible et qu'une preuve empirique supplementaire est jugee utile) reconstruire le package depuis `3bcfe35` et observer `daily_returns` nuls. A ne PAS entreprendre si le rebuild est instable — le mecanisme est deja etabli.

Livrables :

- Bloc de preuve pret a inserer dans l'entree `HISTORIQUE...md` (Phase 2).

Critere de sortie :

- La preuve du mecanisme (git + observation empirique documentee) est formulee et referencable. Aucune re-execution requise pour valider cette phase.

### Phase 2 - Acter l'artefact R4 et le `FAIL` legitime (Q1 + Q2)

Objectif : produire l'artefact de preuve central du chantier (Exit criteria 1).

Classification : GOVERNANCE

Actions :

- Ajouter une NOUVELLE entree datee dans `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` (format du fichier : tableau `| Champ | Valeur |` + sections Contexte/Decision/Impact/Suite), qui reference l'entree "2026-07-16 - Stabilisation..." existante et acte :
  - (Q1) le `PASS` clos par R4 le 2026-07-15 (commit `3bcfe35`) reposait sur une NAV degenerescente (mecanisme de Phase 1), donc n'etait pas une preuve d'edge ;
  - (Q2) le `FAIL` WRC primaire courant (`wrc.json::verdict = "FAIL"`, `wrc_pvalue ~= 0.395`, `11/16` candidats a moyenne negative) est un verdict EBTA legitime : la famille M1 n'a pas d'edge demontrable sur ce segment (conforme a l'objet de SOP 02) ;
  - la lecon operationnelle : le critere de sortie R4 `total_orders > 0` etait necessaire mais insuffisant ; un critere "NAV varie" (`min(nav) < max(nav)` et `sum(daily_returns != 0) > 0`, deja applique par `test_dedicated_venv_m1_segment_records_real_nav_without_false_no_m1`) l'aurait attrape.
- Ne PAS reecrire l'archive R4 ni son `closure_reason` : l'acquittement se fait uniquement par cette nouvelle entree.

Livrables :

- L'entree d'acquittement dans `HISTORIQUE...md`.

Critere de sortie :

- L'entree existe, reference R4 et le commit `3bcfe35`, et ne modifie aucun fichier interdit (verifiable par `git diff --stat`).

### Phase 3 - Reconcilier et clore G5

Objectif : lever le blocage `/close` de G5 et clore les deux chantiers (Exit criteria 2).

Classification : GOVERNANCE

Constat (verifie dans G5, ligne 54 et section 9) :

- Les 5 Exit criteria FORMELS de G5 (section Triage) portent tous sur la propagation de `pre_oos_robustness_verdict` (plus aucun litteral `"PASS"`, test de non-regression a verite connue, test de contraste, suite runtime `PASS`, zero modif de `procedures/`/`risk/`/`validators/`/`governance/`/`manifests/`/`Protocole/`). Aucun n'exige un package Nautilus WRC `PASS`.
- Le blocage `/close` reel venait d'une *attente de l'etape de verification* de G5 (section 9, `report["status"] == "PASS"` attendu sur le package MVP), qui s'est averee fausse — a juste titre, l'executant a halte plutot que de simuler un `PASS`.
- Ce `FAIL` WRC primaire **n'est pas une regression** au sens de la DoD de G5, et ce pour deux raisons distinctes : (a) le *perimetre formel* de G5 ne modifie que `pre_oos_robustness_verdict` dans `_write_reports()`, ce qui ne peut mathematiquement pas affecter le WRC ; (b) le correctif NAV — produit pendant la *session* G5 en debordement de perimetre, puis commite separement (`ebff49d`) — n'est pas une regression mais une *correction* : il rend les `daily_returns` reels (au lieu de tous nuls), ce qui *revele* un `FAIL` honnete au lieu d'en creer un. Un package qui affichait un `PASS` sur des rendements degenerescents n'etait pas "moins casse" ; il etait faussement vert. La DoD "aucune regression" de G5 est donc satisfaite : rien de correct n'a ete casse.
- Conclusion : G5 (gate de robustesse pre-OOS) est un gate DISTINCT de G4 (WRC primaire) ; ses Exit criteria formels sont atteignables, et le `FAIL` legitime acte en Phase 2 ne s'y oppose pas.

Actions :

- Confirmer (decision humaine, section 10) qu'il est acceptable de clore G5 sur ses Exit criteria formels (propagation du verdict robustesse, tous atteignables), l'attente de package `PASS` de sa section 9 etant desormais expliquee (le `FAIL` est legitime et exogene a G5, cf. Phase 2).
- Appliquer, avant `/close`, la procedure `CLAUDE.md` : `bug-hunter` sur les fichiers touches par G5 et `plan-conformance-audit` contre ses Exit criteria (ne clore que si zero bug confirme et aucun Exit criterion manquant).
- **Mettre a jour la section 13 de G5 AVANT l'archivage** : passer "Resultat final : NON CLOTURE au 2026-07-16" a l'issue reelle (ex. "DONE : Exit criteria formels atteints ; l'attente de package PASS de section 9 est expliquee par le `FAIL` legitime et exogene, cf. chantier PLAN_DOCUMENTATION_ARTEFACT_R4_ET_FAIL_WRC_NAUTILUS_M1 et l'entree HISTORIQUE du 2026-07-16"). Sans ce pas, `plan.ps1 close` archiverait un fichier G5 qui se contredit (il n'edite pas le corps markdown).
- Clore G5 via `.ai/tools/plan.ps1 close -Id PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE -Reason "..."` avec l'issue appropriee (`DONE` si son perimetre livre est accepte comme complet ; sinon `BLOCKED` avec raison exacte). Le `-Reason` doit pointer vers l'entree HISTORIQUE de Phase 2 et vers ce chantier.
- Clore ensuite ce chantier-ci (`plan.ps1 close`), une fois ses propres Exit criteria coches (renseigner d'abord sa propre section 13).

Livrables :

- `checkpoint.json` mis a jour par `plan.ps1` (G5 en `DONE`/`BLOCKED`, ce chantier en `DONE`).

Critere de sortie :

- `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE` n'est plus `ACTIVE` ; `.ai/checkpoint.json` valide contre son schema.

### Chemin critique

```mermaid
flowchart LR
    P0["Phase 0 - Stabilisation (FAIT)"] --> P1["Phase 1 - Preuve artefact R4"]
    P1 --> P2["Phase 2 - Acter Q1 + Q2 dans HISTORIQUE"]
    P2 --> P3["Phase 3 - Reconcilier et clore G5"]
```

---

## 7. Artefacts produits

| Etape | Fichier/sortie | Format | Regle source |
| --- | --- | --- | --- |
| Phase 2 | `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` (nouvelle entree) | Markdown (format du fichier) | Decision 2026-07-16 ; SOP 02 |
| Phase 3 | `.ai/checkpoint.json` (via `plan.ps1`) | JSON schema-contraint | `.ai/checkpoint.schema.json` |

---

## 8. Invariants absolus et NO GO

### Invariants (non negociables)

1. Aucune valeur de `wrc_status`/`verdict`/`p-value` n'est ecrite, forcee ou contournee par ce chantier — il ne produit que du texte documentaire et des transitions d'etat de chantier.
2. L'archive R4 (`.ai/archive/20260715_...PRODUCTION.md`) et son `closure_reason` existant ne sont jamais reecrits ; toute correction de narration passe par une entree NOUVELLE et append-only.
3. `Protocole/`, `procedures/wrc.py` et tout seuil calibre restent bit-identiques (verifiable par `git diff`).

### NO GO (grep-ables en revue de diff)

- Modifier `procedures/wrc.py`, un seuil, `alpha`, ou tout fichier sous `Protocole/`.
- Ecrire `wrc_status = "PASS"` ou equivalent nulle part.
- Reecrire une archive `DONE` ou un `closure_reason` existant.
- Retoucher le code moteur deja commite dans `ebff49d`.
- Ouvrir une investigation/refonte de la famille de candidats M1 (hors perimetre, explicitement ecarte).

---

## 9. Verification a chaque etape

Phase 2 (aucun code moteur touche — verifier qu'aucun fichier interdit n'a bouge) :

```powershell
git diff --stat -- "Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md"
git diff --stat -- Protocole Implementation/ebta_engine/procedures/wrc.py
```

La seconde commande DOIT ne rien retourner (aucun fichier interdit modifie).

Phase 3 (etat machine coherent apres cloture) :

```powershell
python -m json.tool .ai/checkpoint.json
python -c "import json, jsonschema; jsonschema.validate(json.load(open('.ai/checkpoint.json', encoding='utf-8')), json.load(open('.ai/checkpoint.schema.json', encoding='utf-8')))"
```

**Regle transversale bloquante** : la suite de tests de reference doit rester `PASS` (le correctif est deja commite ; ce chantier ne doit rien casser) :

```powershell
python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation
```

Attendu : `OK`, 152 tests. Ce chantier ne modifiant aucun code executable, ce nombre doit rester inchange.

**Premier lot executable propose** :

```text
Phase 1 - rassembler la preuve du mecanisme d'artefact (git show 3bcfe35 + entree HISTORIQUE existante)
```

### Execution sans interruption

Ce plan est concu pour un `/continue` de bout en bout. Les seuls arrets legitimes : (1) blocage technique externe (ex. venv Nautilus indisponible SI la reproduction facultative de Phase 1 est tentee — dans ce cas, la sauter et continuer, elle est facultative) ; (2) une decision hors du perimetre section 10 s'avere necessaire (ex. l'issue de cloture de G5 doit etre `BLOCKED` plutot que `DONE`) ; (3) toutes les phases sont terminees et la Definition of Done cochee.

### Autorite decisionnelle accordee

En dehors des levees de gouvernance (section 10) et de l'elargissement du perimetre (section 5), l'IA executante decide seule la redaction exacte de l'entree `HISTORIQUE...md` et les libelles `-Reason` de `plan.ps1`, tant que les invariants (section 8) et les non-goals (Triage) sont respectes.

### Interdiction des raccourcis (aucun faux succes)

- Ne jamais presenter G5 comme clos sans avoir reellement appele `plan.ps1 close` et verifie `checkpoint.json`.
- Ne jamais "documenter un PASS" pour eviter d'ecrire que le package est en `FAIL` : le `FAIL` est le resultat, il doit apparaitre tel quel.
- Ne jamais desactiver/affaiblir un test pour faire passer la suite — elle doit rester `PASS` sans modification de test.

---

## 10. Journal des decisions humaines (autorisations)

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-16 | Archive R4 -> **ajouter une entree tracee** actant que le `PASS` reposait sur une NAV degenerescente, sans reecrire son `closure_reason`. | Autorise la Phase 2 (acquittement Q1) ; interdit toute reecriture de l'archive R4. |
| 2026-07-16 | `FAIL` WRC primaire courant -> **documenter et clore** comme verdict de recherche legitime, sans chantier de recherche sur la famille de candidats. | Autorise la Phase 2 (Q2) et fixe la portee minimale du chantier ; interdit d'ouvrir une investigation sur la famille M1. |
| 2026-07-16 | **Commiter** (plutot que reverter) les 4 fichiers hors perimetre G5. | Execute : commit `ebff49d`. Ferme la Phase 0. |
| [a confirmer en Phase 3] | Accepter de clore G5 sur son perimetre livre, independamment du `FAIL` WRC primaire (G5 = gate robustesse, distinct de G4 = WRC). | Conditionne l'issue de `plan.ps1 close` sur G5 (`DONE` vs `BLOCKED`). A tracer ici avant d'agir. |

---

## 11. Risques et blocages connus

| Risque | Impact | Mitigation / condition de deblocage |
| --- | --- | --- |
| La reproduction facultative depuis `3bcfe35` echoue (venv fragile, vieux commit) | Nulle sur l'Exit criteria : la preuve du mecanisme ne depend pas du rebuild | Sauter la reproduction (Phase 1 la declare facultative) ; s'appuyer sur `git show` + observation deja documentee |
| Ambiguite sur l'issue de cloture de G5 (`DONE` vs `BLOCKED`) | G5 clos avec un statut inexact | Trancher explicitement en Phase 3 (section 10) avant d'appeler `plan.ps1 close` ; appliquer `plan-conformance-audit` d'abord |
| Tentation de "corriger" le `FAIL` en ajustant un parametre | Contamination normative grave (data snooping) | Invariant 1 + NO GO ; le `FAIL` est un livrable, pas un bug |

---

## 12. Definition of Done

- [ ] Phases 1, 2, 3 validees individuellement (section 9) ; Phase 0 deja close.
- [ ] Exit criteria de la section Triage atteint et verifiable (entree `HISTORIQUE...md` presente ; G5 clos ; tests 152 `PASS` ; aucun fichier interdit modifie).
- [ ] Aucune modification hors perimetre (section 5).
- [ ] Aucune regression sur la suite de tests existante (152 tests, inchange).
- [ ] `bug-hunter` (fichiers touches par G5) et `plan-conformance-audit` (Exit criteria de G5) executes avant la cloture de G5, zero bug confirme.
- [ ] Checklist post-modification `.ai/governance/AI_MODIFICATION_CHECKLIST.md` executee (fichiers modifies et pourquoi, fichiers volontairement non modifies, conflits, decisions humaines restantes).
- [ ] Aucun stub/placeholder ; le `FAIL` est documente tel quel, jamais masque.

---

## 13. Cloture

A remplir au moment de `/close`.

| Champ | Valeur |
| --- | --- |
| Resultat final | [a remplir a la cloture] |
| Ecarts par rapport au plan initial | [a remplir a la cloture] |
| Suites a prevoir (hors perimetre de ce plan) | [a remplir — ex. suites deja listees par G5 : DN-030, R6, R5, R7, refonte des booleens auto-attestes de `gates.json`] |

### Resultat d'execution (a dupliquer a chaque session d'execution significative)

| Champ | Valeur |
| --- | --- |
| Date | [a remplir] |
| Phases executees | [a remplir] |
| Artefact produit | [a remplir] |
| Validation | [a remplir] |
| Ecart par rapport au plan | [a remplir] |

---

## 14. Journal d'audits post-hoc

| Date de l'audit | Ce qui a ete corrige | Pourquoi |
| --- | --- | --- |
| 2026-07-16 | Structuration du brouillon `OBSERVATION_WRC_PRIMAIRE_PACKAGE_NAUTILUS_M1_FAIL.md` en plan `fix` conforme au gabarit, lors du `/start`. Reflete l'etat reel post-decisions : Phase 0 (stabilisation depot) marquee DEJA FAITE (commits `ebff49d`, `50f3e3b`) ; reproduction depuis `3bcfe35` rendue facultative (mecanisme deja confirme par git) ; portee reduite a documentation + cloture G5 (pas de chantier de recherche sur la famille, decision humaine section 10). | Le brouillon precedait les decisions humaines et les commits ; le plan route doit refleter l'etat machine reel, pas l'etat au moment de la redaction de la note. |
| 2026-07-16 | Passage `code-architecture-evaluator` (`/evaluate`), passe 1. Corrections : (1) le plan qualifiait "package Nautilus PASS" de critere production bloquant la cloture de G5 — verifie a la ligne 54 de G5 que ses 5 Exit criteria FORMELS portent tous sur la propagation de `pre_oos_robustness_verdict` et qu'aucun n'exige un package WRC `PASS` ; le "package PASS" n'etait qu'une attente de l'etape de verification (G5 section 9). Bandeau section 0 et Constat de Phase 3 reformules en consequence. (2) Ajout du fait, verifie, que le `FAIL` WRC n'est pas une regression introduite par G5 (son perimetre formel ne touche que `pre_oos_robustness_verdict`, pas `wrc.py`/NAV) — renforce la closeabilite de G5 contre un `plan-conformance-audit`. (3) Placeholder `<date>` de la section 2 remplace par le chemin d'archive reel `0 - HUMAN START HERE/archive/20260716_OBSERVATION_...md`. | Eviter qu'une IA executant la Phase 3 ne conclue a tort que G5 est inclôturable (un `plan-conformance-audit` contre ses Exit criteria formels passe), et ancrer la cloture DONE de G5 sur une base verifiable plutot que sur un critere informel mal cite. |
| 2026-07-16 | `/evaluate` passe 2. Angle mort trouve : `plan.ps1 close` (verifie lignes 271-312) deplace le fichier plan vers `.ai/archive/` mais **n'edite pas son corps markdown** ; la section 13 de G5 disant "Resultat final : NON CLOTURE" aurait ete archivee en contradiction avec un statut `DONE`. Corrige : section 5 (perimetre) autorise desormais explicitement l'edition de la section 13 de G5 avant archivage, et Phase 3 ajoute un pas obligatoire "mettre a jour la section 13 de G5 AVANT `plan.ps1 close`". | Sans ce pas, l'archive G5 se serait auto-contredite (statut checkpoint `DONE` vs corps "NON CLOTURE"), un defaut de tracabilite silencieux. |
| 2026-07-16 | `/evaluate` passe 3. Imprecision factuelle trouvee dans la correction de passe 1 : "le diff de G5 ne touche jamais la NAV" est faux au sens de la *session* G5 (le correctif NAV `ebff49d` a ete produit pendant cette session, en debordement de perimetre). Corrige : Constat de Phase 3 distingue desormais le *perimetre formel* de G5 (robustesse, n'affecte pas le WRC) du correctif NAV (produit en session, commite separement) qui est une *correction* revelant un `FAIL` honnete, pas une regression. | Eviter un overclaim qu'un `plan-conformance-audit` ou un relecteur attentif releverait (G5 a bien touche la NAV dans sa session) ; garder l'argument de non-regression exact. |
| 2026-07-16 | `/evaluate` passe 4 — **convergence**. Lecture holistique des phases et du bandeau apres les corrections des passes 1-3 : aucun nouvel angle mort majeur, aucune incoherence introduite. Boucle close (passes 1-3 correctives, passe 4 propre), dans le plafond de 5-6. Aucune correction appliquee a cette passe. | Convention `CLAUDE.md` : la boucle `/evaluate` ne s'arrete que sur une passe qui ne souleve aucun nouvel angle mort majeur. |
