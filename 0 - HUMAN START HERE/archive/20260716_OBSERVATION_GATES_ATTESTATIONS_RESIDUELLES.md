# Observation — `gates.json` : la plupart des booleens de gate restent des attestations codees en dur, alors que les procedures calculent deja un vrai statut pour beaucoup d'entre eux

> Note d'intake, pas un plan. Deposee ici pour triage humain futur, suite au
> "Point 1" (`R3` residuel) identifie dans
> `0 - HUMAN START HERE/AUDIT_MATURITE_MOTEUR_RECHERCHE_2026-07-13.md`
> (section "Suite proposee", 2026-07-16) et dans le meme esprit que le
> precedent deja traite pour le gate economique
> (`0 - HUMAN START HERE/archive/20260710_OBSERVATION_GATE_ECONOMIQUE_BOOLEENS_CODES_EN_DUR.md`,
> devenu `PLAN_CORRECTION_GATE_ECONOMIQUE_CALIBRATION`, `DONE`).

## Constat

`Implementation/ebta_engine/validators/gate_validator.py::GATE_REQUIREMENTS`
(lignes 19-35) definit, pour les gates G0 a G14, une liste de champs requis
dans `reports/gates.json`. `_requirement_satisfied()` (lignes 50-53) exige un
`PASS` pour les champs dont la valeur est un verdict (`PASS`/`FAIL`/
`INCONCLUSIVE`) mais se contente d'un simple `bool(value)` pour tous les
autres champs — c'est-a-dire que n'importe quel litteral `True` ecrit par le
constructeur du package suffit a satisfaire le gate, sans aucun rapport avec
un calcul reel.

Or `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
— qui est aussi le chemin de production du package Nautilus MVP, via
`_load_pilot_module()` (`Implementation/ebta_engine/package_builder/nautilus_research_package.py`
ligne 53) — calcule deja, dans `_procedure_reports()` (lignes 332-453), un
vrai champ `status` (`PASS`/`FAIL`/`INCONCLUSIVE`) pour la plupart des
briques concernees, via de vraies procedures testees :

| Procedure deja appelee (calcule un vrai statut) | Fichier : ligne | Champ(s) `gates.json` ignores et ecrits en `True` en dur a la place |
| --- | --- | --- |
| `validate_availability(...)` -> `status` | `procedures/data_availability.py:13,22` | `data_snapshots`, `availability_timestamps`, `anti_leakage_report` (G1) |
| `review_registry_lineage(...)` -> `status` | `procedures/registry_lineage.py:12,27` | `independent_registry_review` (G2) — **piege, voir avertissement ci-dessous** |
| `validate_pre_oos_seal(...)` -> `status` | `procedures/sealing.py:10,20` | `pre_oos_manifest`, `frozen_config` (G7) |
| `oos_confidence_interval(...)` -> `statistical_gate` (reel) + `power_check.status` (**piege, voir Lot A2**) | `procedures/oos_confidence_interval.py:42,59` | `oos_report`, `concatenated_oos_series`, `oos_bootstrap_report`, `power_report` (G9) |
| `validate_reproduction_report(...)` -> `status` | `procedures/reproduction_report.py:25,217` | `validation_ready_manifest`, `reproduction_report`, `incubation_approval` (G11) |
| `validate_monitoring_plan(...)` / `validate_consultation_log(...)` -> `status` | `procedures/monitoring.py:28,87,201` | `monitoring_plan`, `paper_trading_log` (G12) |
| `validate_incubation_report(...)` -> `status` | `procedures/incubation_report.py:21,229` | `incubation_report` (G12, redondant avec `reports/incubation_report.json` deja correct) |
| `deployment_gate(...)` -> `status` | `procedures/lifecycle.py:30,40` | `deployment_certified_manifest` (G13) |

> **Correction post-`/evaluate` (passe 1)** : la version initiale de cette note
> citait par erreur `oos_confidence_interval(...)` comme retournant un champ
> `status` aux lignes 113/119/178 du fichier. C'est faux : ces lignes
> appartiennent a `validate_power_target()` et
> `validate_information_stop_point()`, deux fonctions **jamais appelees**
> dans `_procedure_reports()`. Le vrai champ calcule et disponible dans
> `oos.json` est `statistical_gate` (via `_statistical_verdict()`, ligne 42)
> et `power_check.status` (ligne 59). Corrige ci-dessus.

> **Avertissement (passe 1)** : `review_registry_lineage(candidate_ids,
> candidate_ids)` (`build_research_package.py:452`) est appele avec **le
> meme argument des deux cotes** (`registered_candidates ==
> influential_candidates`) et sans jamais fournir `lineage_events`. Par
> construction, `missing` et `unresolved_children` sont **toujours vides** —
> `registry_review.status` est `PASS` par tautologie, pas par calcul reel.
> Brancher ce champ tel quel dans `gates.json` ne corrigerait rien : ca
> deplacerait l'illusion d'attestation d'un endroit a l'autre. Un vrai fix
> demanderait de repasser des `registered_candidates` (ex. depuis
> `registry.jsonl`) distincts des `influential_candidates` (depuis
> `candidate_matrix.json`) — une decision de source de verite qui n'a pas
> encore ete posee. **G2 reste donc hors perimetre de tout fix mecanique.**

La preuve directe est dans `build_research_package.py::_write_reports()`
(lignes 189-247) : `procedure_reports = _procedure_reports(pilot_inputs)` est
calcule ligne 191, puis le dict `gates` (lignes 193-247) n'en reutilise que
trois valeurs (`selected_candidate_id`, `wrc_status`,
`pre_oos_robustness_verdict` — deja corriges par les chantiers WRC et G5) et
ecrit un litteral `True` pour environ 35 autres champs, alors que
`procedure_reports` contient deja, pour la moitie d'entre eux, un `status`
reel calcule a partir des memes entrees.

**G6 (execution) n'est PAS un cas de "calcul deja fait puis ignore" comme les
8 procedures ci-dessus — c'est un calcul manquant en amont, plus grave.**
`Implementation/ebta_engine/package_builder/nautilus_research_package.py`
ligne 242-252 ecrit `inputs["execution_report"] = {"status": "PASS", ...
"nav_reconciliation": "PASS", ...}` **en dur**, malgre le fait que
`_total_orders(all_simulation_results)` (ligne 247) et
`_total_orders(oos_results)` (ligne 248) sont deja disponibles a cet endroit
et pourraient servir a un vrai calcul (`total_orders > 0`,
`oos_total_orders > 0`, variation de NAV non nulle — exactement la lecon
tiree du `PASS` R4 artefactuel documentee dans
`Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`, entree du
2026-07-16, note 5 de la section "Note a garder dans un coin" de l'audit).
Ce champ alimente les gate booleens `execution_report`, `cost_model`,
`capacity_grid`, `nav_reconciliation` (G6). Aggravant supplementaire verifie
en passe 1 de `/evaluate` : `procedures/lifecycle.py::incubation_gate()`
(lignes 13-27) exige deja `execution_status: "PASS"` et le recoit
correctement depuis `pilot_inputs["execution_report"]["status"]`
(`build_research_package.py:412`) — le mecanisme de propagation vers
`incubation_gate.json` fonctionne bien. Le trou n'est donc pas la
propagation, il est en amont : **aucune fonction ne calcule
`execution_report["status"]`** sur le chemin reel, contrairement aux 8
procedures ci-dessus qui ont chacune une vraie fonction de calcul deja
appelee. G6 est donc, par nature, plus proche du precedent deja corrige
`PLAN_CORRECTION_GATE_ECONOMIQUE_CALIBRATION` (calcul absent a ecrire, seuils
a calibrer par l'humain) que du precedent WRC/G5 (calcul deja present, juste
mal branche).

## Ce qui n'est PAS un defaut (deja documente, hors perimetre)

- `Implementation/ebta_engine/package_builder/economic_calibration.py:51,53`
  laisse `capacity_pass` et `execution_pass` a `True` **explicitement et
  documentee** comme non calibres (commentaire ligne 28) — c'est une
  decision deja actee par
  `.ai/archive/...PLAN_CORRECTION_GATE_ECONOMIQUE_CALIBRATION.md` (2026-07-10),
  pas une regression a corriger ici.
- Les champs de verdict scientifique (`wrc_status`, `pre_oos_robustness_verdict`,
  et les statuts reels dans `wrc.json`/`economic.json`/`robustness.json`/
  `incubation_gate.json`) sont deja corrects et deja verifies par
  `_semantic_consistency_errors()` (`validators/package_validator.py:172-223`).
  Cette note ne les retouche pas.
- Certains champs de `GATE_REQUIREMENTS` sont des attestations de decision
  humaine par nature (ex. `independent_pre_oos_approval` (G7),
  `kill_switch`/`live_approval` (G13), `retention_policy`/`incident_log`
  (G14)) : aucune procedure ne peut les "calculer" depuis une simulation —
  la vraie correction serait de les lire depuis un evenement/registre reel
  (ex. une entree d'approbation dans `registry.jsonl` ou un log
  d'incident), pas de leur inventer un calcul. Cette note ne tranche pas
  cette distinction a la place de l'humain.

## Ce que cette note ne fait PAS

- Elle ne modifie ni `build_research_package.py`, ni
  `nautilus_research_package.py`, ni aucun validateur.
- Elle ne propose pas de perimetre de correction deja tranche : convertir
  les ~35 champs identifies en une seule fois serait un chantier disproportionne
  et risque de style "faux succes" ; le decoupage par lot (section
  "Decoupage propose" plus bas — Lots A1/A2/B/C) reste une decision
  d'architecture et de priorisation qui appartient a l'humain, comme pour
  les chantiers WRC/G5 precedents.
- Elle ne cree pas de chantier actif : ce fichier reste `INTAKE`, non
  executable, tant qu'un humain ne l'a pas audite et route vers
  `.ai/backlog/` (probablement `fixes/`, meme nature que les corrections
  WRC/G5/validators deja closes) selon `.ai/README.md`.

## Decoupage propose (issu de la passe 1 de `/evaluate`, `code-architecture-evaluator`)

Les ~10 champs residuels ne sont pas homogenes en risque. Trois lots
distincts, plutot qu'un seul chantier :

- **Lot A1 — G9 OOS `statistical_gate` uniquement** (le plus urgent : calcul
  reel — `estimate`/`lower_95` sont bien issus des rendements OOS
  bootstrappes reels via `_statistical_verdict()` — jamais propage nulle
  part, contrairement a WRC/robustesse deja corriges). Perimetre mecanique,
  risque faible. Peut faire apparaitre un `FAIL`/`NOT_VALIDATED` sur le
  package M1 courant — a documenter d'avance comme decouverte legitime
  (meme clause que celle deja actee pour le `FAIL` WRC/G5 dans
  `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`), jamais comme
  regression a masquer.
- **Lot A2 — G9 `power_check.status` — PIEGE, verifie en passe 2 de
  `/evaluate`** : ni `build_research_package.py:380-385` ni
  `nautilus_research_package.py` ne passent le kwarg `power` a
  `oos_confidence_interval()` ; il retombe sur le defaut de signature
  `power: float = 0.80` (`oos_confidence_interval.py:22`). La puissance
  n'est donc **jamais estimee depuis l'echantillon OOS reel** (taille,
  effet, variance) — elle est codee en dur exactement egale au seuil
  cible, ce qui rend `validate_power_target(0.80, target_power=0.80)`
  toujours `PASS` par construction (meme piege que G2/`review_registry_lineage`).
  Brancher ce champ tel quel donnerait une fausse impression de puissance
  statistique validee. **A traiter comme un calcul manquant (meme famille
  que le Lot B), pas comme un branchement** : il faut d'abord ecrire une
  vraie fonction de puissance atteinte avant tout branchement de
  `power_check.status`.
- **Lot B — G6 `execution_report`/`nav_reconciliation`** (calcul absent a
  ecrire, pas un branchement — voir ci-dessus). Necessite une decision de
  seuil humaine (ex. reutiliser l'invariant "NAV non plate" deja teste par
  `test_dedicated_venv_m1_segment_records_real_nav_without_false_no_m1`,
  cite dans l'entree HISTORIQUE du 2026-07-16, plutot que d'inventer un
  nouveau critere). Meme nature de decision que
  `PLAN_CORRECTION_GATE_ECONOMIQUE_CALIBRATION`.
- **Lot C — G1/G7/G11/G12/G13 branchements mecaniques surs** (calcul reel
  deja fait et non-vacueux : `data_availability`, `sealing` partiellement,
  `reproduction_report`, `monitoring`/`incubation_report`,
  `deployment_gate`). Risque faible, valeur pratique limitee tant que le
  package n'a pas depasse le stade pre-OOS en conditions reelles — peut etre
  differe.

**Hors perimetre de tout fix mecanique** (a laisser en l'etat, documente) :

- G2 `independent_registry_review` : l'appel actuel est tautologique (voir
  avertissement plus haut) ; corriger demande d'abord une decision humaine
  sur la source de verite "registered vs influential", pas un branchement.
- G7 `independent_pre_oos_approval`, G13 `kill_switch`/`live_approval`, G14 :
  attestations humaines legitimes ; aucune procedure ne peut les "calculer"
  depuis une simulation. A laisser en `True` documente tant qu'aucun
  evenement reel d'approbation/registre n'existe pour les alimenter.

## Perimetre fichiers pressenti (a confirmer au `/start`)

**Autorises** : `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
(`_write_reports`, partage pilote + production Nautilus) ;
`Implementation/ebta_engine/package_builder/nautilus_research_package.py`
(uniquement pour le Lot B, nouvelle fonction de calcul `execution_report`).

**Interdits** : `Protocole/`, tout fichier sous `procedures/` (les 8
fonctions citees sont deja correctes et ne doivent pas etre modifiees, seul
leur resultat doit etre branche), `validators/`, `governance/`,
`manifests/`.

**Garde de non-regression** : `_write_reports()` est partage par le pilote
minimal (`test_minimal_pilot_pipeline.py`) et le chemin de production
Nautilus. Tout changement doit etre verifie sur les deux ; si les fixtures
statiques du pilote (`pilot_inputs.json`) ne produisent pas naturellement un
`PASS` sur un champ nouvellement derive, corriger la fixture du pilote fait
partie du perimetre du chantier (ce n'est pas hors-sujet).

## Questions ouvertes pour l'humain — TRANCHEES le 2026-07-16

1. ~~Parmi les lots A1/A2/B/C ci-dessus, par lequel commencer ?~~
   **Decision : Lot A1 seul.** C'est le seul lot a router via `/start`
   immediatement. Justification humaine implicite dans le choix : c'est le
   lot le plus sur (calcul deja reel, rien a calibrer), meme gabarit que les
   fix WRC/G5 deja clos rapidement — la note ne doit donc PAS etre
   restructuree en un seul chantier "tous lots" au `/start` : seul le
   perimetre A1 (`oos.json::statistical_gate` -> gates.json G9) doit etre
   repris dans le plan structure. A2, B, C restent a l'etat d'observation
   ci-dessus, non routes.
2. ~~Lot C : executer maintenant ou differer ?~~ **Decision : differe
   explicitement.** Aucune action sur G1/G7/G11/G12/G13 tant que le package
   n'atteint pas incubation/deploiement en conditions reelles. Ne pas
   ouvrir de chantier dessus sans nouvelle decision humaine.
3. ~~G2 et A2 : regrouper avec B, ou geler indefiniment, ou traiter seuls ?~~
   **Decision : regrouper G2 (registry_review tautologique) + A2
   (power_check vacueux) avec le Lot B (execution_report/nav_reconciliation)
   dans un futur chantier distinct, apres A1.** Motif : les trois partagent
   la meme nature de decision (calcul manquant a ecrire + seuil/source de
   verite a calibrer par l'humain, pas un branchement mecanique) — a
   traiter comme un second chantier `fix`, jamais mélangé avec A1.

## Suite immediate

Seul le **Lot A1** est pret pour `/start` maintenant :
`"0 - HUMAN START HERE/OBSERVATION_GATES_ATTESTATIONS_RESIDUELLES.md"`,
avec pour perimetre exclusif : brancher `oos.json::statistical_gate` (deja
calcule, reel, non-vacueux) dans les 4 champs `gates.json` du gate G9
(`oos_report`, `concatenated_oos_series`, `oos_bootstrap_report`,
`power_report`), dans `build_research_package.py::_write_reports()`
uniquement (partage pilote + production Nautilus, cf. garde de
non-regression `test_minimal_pilot_pipeline.py:55` plus haut).

Un second chantier `fix` (G2 + A2 + Lot B — "calculs manquants residuels
G2/G6/G9-power") sera ouvert separement plus tard, apres A1, sur nouvelle
decision de priorisation. Le Lot C reste hors feuille de route tant qu'aucune
decision humaine ne le reactive.
