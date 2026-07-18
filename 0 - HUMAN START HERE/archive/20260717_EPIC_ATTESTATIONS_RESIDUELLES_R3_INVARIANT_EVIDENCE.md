# Note d'intake — Chantier mere : attestations residuelles R3 (G2/G3/G4/G5/G7/G8/G10), `invariant_evidence.json` et regeneration du package persistant

> Statut : `INTAKE`, non executable. Redige par l'IA a partir d'une demande
> humaine du 2026-07-17 de poursuivre le sujet R3-residuel identifie dans
> `AUDIT_MATURITE_MOTEUR_RECHERCHE_2026-07-13.md` (Partie A, sections 1 et 3)
> apres la cloture de `EPIC_CLOTURE_ATTESTATIONS_RESIDUELLES_GATES` (commit
> `063246b`). Boucle `/evaluate` (code-architecture-evaluator) executee le
> 2026-07-17, convergee apres 2 passes : la passe 1 a trouve deux bugs de
> fond derriere des champs que ce document classait initialement comme
> "branchements mecaniques" (section 1.5) ; la passe 2 a precise les
> sources de derivation G10 et documente une ambiguite de conception
> residuelle sur G2 (section 1.5.1) sans trouver de nouveau blind spot
> majeur. Ce fichier reste `INTAKE` tant qu'un humain ne l'a pas audite et
> route vers `.ai/backlog/` via `/start -Audited`.

---

## 0. Pourquoi ce chantier maintenant

`EPIC_CLOTURE_ATTESTATIONS_RESIDUELLES_GATES` (Lots C, A2, B) a deja corrige
les champs `gates.json` suivants pour qu'ils derivent de statuts de procedure
reels au lieu de litteraux `True` codes en dur :

- G1 : `data_snapshots`, `availability_timestamps`, `anti_leakage_report`
- G7 (partiel) : `pre_oos_manifest`, `frozen_config`
- G9 : `power_report` (deja partiellement fait par le Lot A1 anterieur)
- G11 : `validation_ready_manifest`, `reproduction_report`, `incubation_approval`
- G12 : `incubation_report`, `paper_trading_log`, `monitoring_plan`
- G13 (partiel) : `deployment_certified_manifest`
- G6 : `execution_report`, `cost_model`, `capacity_grid`, `nav_reconciliation`

Ce meme EPIC a deja explicitement exclu du perimetre, par decision humaine
journalisee le 2026-07-16 (section 10 de l'EPIC clos) : `independent_registry_review`
(G2), `independent_pre_oos_approval` (G7), `kill_switch`/`live_approval` (G13),
`retention_policy`/`incident_log` (G14) — traites comme des attestations
humaines/de gouvernance legitimement declaratives, hors perimetre d'un moteur
de recherche.

Verification directe du code au 2026-07-17
(`Implementation/examples/minimal_pilot_pipeline/build_research_package.py:255-309`,
chemin partage par le pilote et par la production Nautilus via
`nautilus_research_package.py::build_nautilus_research_package()`) : il reste
des champs `gates.json` qui n'ont jamais ete traites par C/A2/B ni exclus par
la decision du 2026-07-16, un fichier `invariant_evidence.json` qui contient
des valeurs fabriquees plutot que derivees, et — decouvert lors de la passe 1
de `/evaluate` — deux fonctions deja existantes qui, si elles etaient
reutilisees telles quelles, reproduiraient le meme piege que celui deja
rencontre avec `power_check` au Lot A2 (un calcul qui se valide lui-meme).

---

## 1. Etat des lieux verifie dans le code (2026-07-17, mis a jour apres passe 1 `/evaluate`)

### 1.1 Champs `gates.json` encore des litteraux non traites, par gate reel (`validators/gate_validator.py::GATE_REQUIREMENTS`)

| Gate | Champs concernes | Ligne(s) dans `build_research_package.py` | Valeur actuelle |
| --- | --- | --- | --- |
| G2 | `registry_initialized`, `candidate_catalog`, `local_matrix` | 265-267 | `True` litteral |
| G3 | `selection_rule`, `train_only_calibration_log` | 269-270 | `True` litteral |
| G4 | `wrc_report`, `wrc_family_matrix` | 272, 274 | `True` litteral (a cote de `wrc_status` deja reel) |
| G5 | `robustness_report`, `robustness_matrix` | 275-276 | `True` litteral (a cote de `pre_oos_robustness_verdict` deja reel) |
| G7 (residuel) | `test_reports` | 284 | `True` litteral — voir 1.6, aucune source de derivation identifiee |
| G8 | `oos_access_log`, `opening_authorization`, `single_oos_execution_log` | 286-288 | `True` litteral |
| G10 | `economic_report`, `statistical_gate_report`, `economic_gate_report` | 293-295 | `True` litteral (un statut reel existe deja a cote : `economic["economic_status"]`, `economic["failures"]`) |

Note (correction post-passe-1) : le regroupement initial en deux "familles"
informelles ("registre/pre-OOS" et "acces OOS") melangeait des champs
appartenant a des gates distincts. Le decoupage en Lot D/Lot E ci-dessous
(section 4) suit desormais la table `GATE_REQUIREMENTS` reelle, pas une
intuition thematique.

### 1.2 Champs deja explicitement hors perimetre (decision humaine 2026-07-16, reaffirmee aujourd'hui)

`independent_registry_review` (G2), `independent_pre_oos_approval` (G7),
`live_version_id`/`kill_switch`/`live_approval`/`lifecycle_archive`/`incident_log`/`retention_policy`
(G13/G14). Decision humaine du 2026-07-17 (ce document) : **reconduite a
l'identique**. Ce chantier ne rouvre pas ce sujet ; il documente seulement,
au moment de la cloture, pourquoi ces champs restent des attestations
declaratives legitimes (aucune boucle post-OOS/live reelle n'existe dans ce
repo — cf. `AUDIT_MATURITE_MOTEUR_RECHERCHE_2026-07-13.md` H2/H3).

### 1.3 `invariant_evidence.json` — valeurs fabriquees identifiees

Dans `_write_reports()` (meme fichier, lignes 310-360) :

- `pre_oos_sealed_at`: literal `"2023-01-01T00:00:00Z"`, jamais derive du
  vrai horodatage de scellement (`sealing.json`/`procedures/sealing.py`).
- `oos_openings`: `wrc_local_status: "PASS"` code en dur pour **chaque**
  fold, independamment du verdict WRC reel de ce fold — c'est la forme la
  plus grave identifiee : une fausse preuve positive par fold, pas seulement
  une attestation optimiste globale.
- `transformation_fits`: entree unique fixe `{"name": "scaler", "fit_segment": "Train_k"}`,
  jamais derivee des transformations reellement appliquees par fold/candidat.
- `decision_events`: horodatages litteraux fixes, jamais derives des
  evenements reels de `registry.jsonl`/`oos_access_log.jsonl`.

### 1.4 Package persistant obsolete

`Implementation/research_packages/nautilus_mvp/reports/gates.json` n'a pas
ete regenere depuis la cloture du Lot B (`6f0b212`) : il contient encore
`execution_report=true`, `cost_model=true`, `capacity_grid=true`,
`nav_reconciliation=true` en litteraux d'avant-correction, verifie par lecture
directe du fichier le 2026-07-17.

### 1.5 Deux bugs de fond trouves lors de la passe 1 `/evaluate` (2026-07-17)

Decision humaine actee aujourd'hui : **ces deux bugs sont integres au
perimetre de Lot D et Lot E respectivement** (pas de sous-chantier separe).
Ce ne sont pas de simples branchements de champ comme pour Lot C ; ce sont
des corrections de calcul, sur le meme modele que la correction A2.

1. **G2 — `review_registry_lineage()` structurellement tautologique.**
   `Implementation/ebta_engine/procedures/registry_lineage.py::review_registry_lineage()`
   calcule `missing = set(influential_candidates).difference(registered_candidates)`.
   `build_research_package.py:516` l'appelle avec
   `review_registry_lineage(candidate_ids, candidate_ids)` — **la meme liste
   des deux cotes**, et sans `lineage_events`. Consequence : `missing` et
   `unresolved_lineage_events` sont TOUJOURS vides, donc `status` est
   TOUJOURS `"PASS"`, independamment de l'etat reel du registre. Deriver
   `registry_initialized`/`candidate_catalog`/`local_matrix` (G2) de ce
   rapport tel quel ne ferait que remplacer un `True` litteral par un
   `"PASS"` tout aussi automatique.
   Correction requise dans le perimetre du Lot D : lire les
   `registered_candidates` reels depuis les evenements `REGISTER_CANDIDATE`
   deja ecrits dans `registry.jsonl` par `_write_registry()`
   (meme fichier, lignes 149-182), au lieu de reutiliser `candidate_ids` en
   memoire pour les deux arguments.
   Verifie en passe 2 `/evaluate` : cette correction suppose une distinction
   reelle entre candidats "enregistres" et candidats "influents". Or
   `_write_registry()` enregistre aujourd'hui TOUS les candidats de
   `search_space["candidates"]` pour CHAQUE fold, sans filtrage, et
   `invariant_evidence.json` utilise deja `candidate_ids` identique pour
   `registered_candidates`, `influential_candidates` et
   `applicable_candidates` (lignes 324-326) — rien dans le pipeline actuel ne
   calcule encore une veritable notion de sous-ensemble "influent" distinct
   de "enregistre". Le Lot D devra trancher a son propre `/start` : soit une
   distinction reelle est identifiee/construite (ex. candidats ayant
   effectivement atteint le test WRC vs univers complet enregistre), soit
   `registry_review` doit etre redefini comme un controle de presence/
   coherence plus modeste et documente comme tel, plutot que suppose ici.

2. **G8 — `wrc_pass` fige a `True` dans `_oos_access_request()`.**
   `build_research_package.py:520-530::_oos_access_request()` construit la
   requete d'autorisation d'acces OOS avec `"wrc_pass": True` en litteral,
   jamais `wrc["verdict"] == "PASS"` alors que ce verdict est deja calcule au
   meme endroit (`procedure_reports["wrc"]`, disponible avant l'appel ligne
   458). Le package `nautilus_mvp` courant a `wrc_status = "FAIL"`
   (verifie dans `reports/gates.json`) mais
   `procedures/oos_access.py::authorize_oos_access()` — deja appele et
   deja stocke dans `procedure_reports["oos_access_decision"]`, simplement
   jamais propage vers `gates.json` — considere aujourd'hui la condition
   WRC comme toujours satisfaite. C'est une resurgence du meme type de bug
   que celui corrige par `PLAN_CORRECTION_GATE_STATISTIQUE_WRC_MASQUE`
   (2026-07-15), non detecte a l'epoque parce que ce plan ne couvrait que
   G4/G10/G11, pas G8.
   Correction requise dans le perimetre du Lot E :
   `"wrc_pass": wrc["verdict"] == "PASS"` dans `_oos_access_request()`,
   avant de propager `procedure_reports["oos_access_decision"]["status"]`
   vers `oos_access_log`/`opening_authorization`/`single_oos_execution_log`.

Correction de reference (passe 1) : ce document citait initialement
`governance/oos_access_guard.py` comme mecanisme reutilisable pour Lot E.
Verification directe (`rg oos_access_guard` sur `Implementation/ebta_engine`) :
ce module n'est jamais importe ni appele par `build_research_package.py` ni
par `nautilus_research_package.py` — il n'est reference que par lui-meme et
par `governance/bias_registry.py`. Le vrai point de calcul deja branche dans
le chemin de production est `procedures/oos_access.py::authorize_oos_access()`
(deja appele, resultat deja stocke, simplement non propage vers `gates.json`).

### 1.6 Ambiguite non resolue : `test_reports` (G7)

Aucune fonction de `_procedure_reports()` ne produit de rapport nommable ou
assimilable a `test_reports`. Recherche dans
`Protocole/PAQUET D'EXECUTION EBTA.md` : la chaine `test_reports` n'apparait
nulle part — G7 est decrit en prose ("hypothese, configuration, registre,
donnees, code et environnement presents") sans mapping 1:1 explicite vers ce
nom de champ. Ce point reste ouvert et doit etre tranche au `/start` du Lot D
plutot que suppose : soit une source de derivation legitime est identifiee
(a documenter), soit ce champ doit etre traite comme une attestation
declarative documentee au meme titre que celles de la section 1.2, avec
justification explicite.

---

## 2. Decisions humaines actees (2026-07-17)

| Sujet | Decision |
| --- | --- |
| Champs post-OOS/live (`kill_switch`, `live_approval`, `incident_log`, `retention_policy`, et par extension `live_version_id`/`lifecycle_archive` deja exclus le 2026-07-16) | **Documenter comme hors perimetre**, pas construire un mecanisme reel. Ce sont des attestations de gouvernance humaine/operationnelle que le moteur de recherche ne peut pas prouver mecaniquement sans un vrai cycle live qui n'existe pas dans ce repo. Reconduit a l'identique de la decision du 2026-07-16 ; aucune extension de perimetre live n'est autorisee par ce chantier. |
| Decoupage du travail restant | **Deux lots distincts** : Lot D (G2/G3/G4/G5/G7-residuel/G10) et Lot E (G8), chacun avec son propre cycle `/start` -> `/evaluate` x2 -> baseline -> `/continue` -> bug-hunter + conformance -> `/close`, sur le meme modele que Lots C/A2/B. |
| Regeneration du package persistant `nautilus_mvp` | **Incluse dans ce chantier**, comme derniere phase, une fois Lot D et Lot E clos, pour que l'artefact persistant reflete les corrections C/A2/B/D/E, preuve finale `validate_package_dir()`. |
| Bugs de fond section 1.5 (registre tautologique, `wrc_pass` fige) | **Integres aux Lots D et E existants respectivement** (pas de sous-chantier separe). Ce sont des corrections de calcul necessaires pour que le branchement des champs `gates.json` ait un sens, pas un elargissement hors sujet. |

`invariant_evidence.json` (section 1.3) n'a pas encore de decision de
decoupage explicite : il est propose comme un troisieme lot (Lot F) dans la
section 4, a confirmer ou modifier par l'humain au moment du `/start` de ce
chantier mere, plutot que suppose ici.

---

## 3. Perimetre et non-objectifs

Scope : corriger les champs `gates.json` du tableau 1.1 (G2/G3/G4/G5/G7-residuel/G8/G10)
pour qu'ils derivent de rapports/registres reels au lieu de litteraux `True`,
en corrigeant au passage les deux bugs de fond identifies en 1.5 (condition
necessaire pour que la derivation soit reelle et non tautologique) ; corriger
les quatre valeurs fabriquees de `invariant_evidence.json` (section 1.3) ;
puis regenerer et valider le package persistant `nautilus_mvp`.

Non-objectifs :

- ne pas rouvrir G2 (`independent_registry_review`), G7 (`independent_pre_oos_approval`),
  G13/G14 deja exclus (section 1.2) ;
- ne pas construire un vrai cycle paper trading / deploiement live / kill
  switch ;
- ne pas modifier `Protocole/`, les SOP, `validators/gate_validator.py::VERDICT_VALUES`
  ou `GATE_REQUIREMENTS`, les manifests, la gouvernance G-BIAS, ni les lots
  C/A2/B deja clos ;
- ne pas introduire de nouveau statut de gate ni de nouvel appel API Nautilus ;
- ne pas fusionner Lot D et Lot E dans un seul commit/cycle `/evaluate` ;
- ne pas supposer qu'un champ converti en statut calcule doit necessairement
  rester `PASS` sur le package persistant courant : un basculement vers
  `FAIL`/`INCONCLUSIVE` sur un gate jusque-la vert (ex. G2 si le registre reel
  s'avere incomplet) est un succes du chantier, pas un echec, au meme titre
  que ce qui a deja ete accepte pour G4/G5/G9.

---

## 4. Decoupage propose (a confirmer/ajuster au `/start`)

1. **Lot D — G2/G3/G4/G5/G7-residuel/G10.**
   - Corriger `review_registry_lineage()` / son appelant pour lire les
     `registered_candidates` reels depuis `registry.jsonl` (section 1.5.1),
     puis deriver `registry_initialized`/`candidate_catalog`/`local_matrix`
     (G2) de ce statut corrige.
   - Deriver `selection_rule`/`train_only_calibration_log` (G3) d'une source
     a identifier au `/start` (candidate_matrix/optimization_log deja
     calcules).
   - Deriver `wrc_report`/`wrc_family_matrix` (G4) de la presence/coherence
     du rapport WRC deja calcule (`procedure_reports["wrc"]`).
   - Deriver `robustness_report`/`robustness_matrix` (G5) du rapport de
     robustesse deja calcule (`procedure_reports["robustness"]`).
   - Trancher `test_reports` (G7 residuel, section 1.6) avant implementation.
   - Deriver `economic_report`/`statistical_gate_report`/`economic_gate_report`
     (G10) des trois champs deja retournes separement par
     `economic_gate_report()` (`Implementation/ebta_engine/procedures/economic_gate.py:14-40`) :
     `economic_status`, `statistical_status`, `global_status` respectivement —
     verifie en passe 2 `/evaluate`, les trois sources existent deja et sont
     distinctes, pas un seul bloc a deviner.
2. **Lot E — G8.**
   - Corriger `_oos_access_request()` pour utiliser
     `wrc["verdict"] == "PASS"` au lieu de `True` fige (section 1.5.2).
   - Deriver `oos_access_log`/`opening_authorization`/`single_oos_execution_log`
     de `procedure_reports["oos_access_decision"]["status"]`, deja calcule
     par `procedures/oos_access.py::authorize_oos_access()` mais jamais
     propage vers `gates.json`.
   - Test de contraste obligatoire avant `/close` : un cas ou WRC est reel
     `FAIL` (deja disponible : le package `nautilus_mvp` courant) doit
     produire `oos_access_decision.status = "DENIED"` et les trois champs
     G8 ne doivent plus pouvoir afficher un acces autorise.
3. **Lot F (propose) — `invariant_evidence.json` non fabrique.** Remplacer
   `pre_oos_sealed_at`, `oos_openings[].wrc_local_status`, `transformation_fits`
   et `decision_events` par des valeurs derivees des rapports/logs reels
   (`sealing.json`, verdict WRC par fold reel, transformations reellement
   appliquees, evenements reels de `registry.jsonl`/`oos_access_log.jsonl`).
4. **Phase finale — regeneration du package persistant.** Reconstruire
   `Implementation/research_packages/nautilus_mvp` apres cloture de D/E(/F) et
   verifier `validate_package_dir()`. Documenter explicitement, gate par
   gate, le statut attendu apres regeneration (y compris si un gate
   jusque-la `PASS` bascule en `FAIL`/`INCONCLUSIVE` — cf. section 3).

Verification transversale a ajouter a chaque sous-chantier (angle mort
identifie en passe 1) : mettre a jour `Implementation/TRACEABILITY_MATRIX.md`
et verifier `Protocole/MATRICE DE COHERENCE DES SOP EBTA.md` si applicable,
conformement a `.ai/governance/AI_MODIFICATION_CHECKLIST.md`.

---

## 5. Suite attendue

Ce document reste une note d'intake. La suite normale, suivant le workflow du
depot :

1. Humain audite/ajuste cette note (notamment le perimetre exact du Lot F et
   la source de derivation de `test_reports`, section 1.6).
2. `/start "0 - HUMAN START HERE/EPIC_ATTESTATIONS_RESIDUELLES_R3_INVARIANT_EVIDENCE.md"`
   route un plan mere formatte selon `.ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md`,
   sur le meme modele que `EPIC_CLOTURE_ATTESTATIONS_RESIDUELLES_GATES.md`.
3. Boucle `/evaluate` (minimum 2 passes) sur le plan mere avant `/continue` —
   passe 1 deja executee (section 1.5), passe 2 a faire sur cette version
   mise a jour.
4. Chaque sous-chantier (Lot D, Lot E, Lot F, regeneration) suit son propre
   cycle complet `/start` -> `/evaluate` x2 -> baseline -> `/continue` ->
   bug-hunter + `plan-conformance-audit` -> `/close`.
