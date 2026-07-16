# EPIC — Clore les attestations residuelles de `gates.json` / `invariant_evidence.json` (Lots C, A2, B)

> Note d'intake, redigee en session IA a la demande explicite de l'humain
> (2026-07-16/17), suite au residu `R3 — Preuve vs attestation` de
> `0 - HUMAN START HERE/AUDIT_MATURITE_MOTEUR_RECHERCHE_2026-07-13.md` et a
> l'observation `0 - HUMAN START HERE/archive/20260716_OBSERVATION_GATES_ATTESTATIONS_RESIDUELLES.md`
> (deja convergee apres 3 passes `/evaluate`, deja partiellement executee :
> son Lot A1 a produit `.ai/archive/20260716_PLAN_CORRECTION_GATE_STATISTIQUE_OOS_MASQUE.md`,
> `DONE`). Ce fichier reste `INTAKE`, non executable, tant qu'il n'a pas ete
> route vers `.ai/backlog/` par `/start`.

## Pourquoi ce chantier mere existe

L'observation source decoupait deja le residu en Lots A1/A2/B/C, avec la
decision humaine du 2026-07-16 de les traiter "dans un futur chantier
distinct, jamais fusionne" les uns avec les autres. Cela a fonctionne pour
A1 (clos proprement), mais a laisse A2/B/C sans aucun point d'ancrage commun
dans `.ai/checkpoint.json` : chaque lot redevient une note d'intake isolee
qu'il faut retrouver, re-auditer et re-router independamment, sans lien
mecanique vers les lots freres. C'est la cause directe de la perte de vue
signalee par l'humain en session (2026-07-17) : "on commence a avoir des
sous-chantiers et des chantiers disperses que je n'arrive plus a suivre".

Ce document sert de **chantier mere de suivi** (pas d'implementation directe)
pour les trois lots restants (C, A2, B), avec un ordre d'execution explicite
et un seul id a suivre dans `.ai/checkpoint.json::workstreams` jusqu'a
cloture generale.

## Perimetre couvert (et exclu)

**Inclus** :

- **Lot C** — branchements mecaniques surs : `data_snapshots`,
  `availability_timestamps`, `anti_leakage_report` (G1) ;
  `pre_oos_manifest`, `frozen_config` (G7) ; `validation_ready_manifest`,
  `reproduction_report`, `incubation_approval` (G11) ; `incubation_report`,
  `paper_trading_log`, `monitoring_plan` (G12) ;
  `deployment_certified_manifest` (G13).
- **Lot A2** — `power_check.status` (G9), avec une vraie fonction de
  puissance atteinte a ecrire (calcul manquant, pas un branchement).
- **Lot B** — `execution_report`/`cost_model`/`capacity_grid`/
  `nav_reconciliation` (G6), calcul manquant en amont, necessite une
  decision de seuil humaine (meme nature que
  `.ai/archive/...PLAN_CORRECTION_GATE_ECONOMIQUE_CALIBRATION.md`).

**Exclus explicitement** (hors perimetre de ce chantier mere, non routes ici) :

- **G2** `independent_registry_review` — appel tautologique
  (`review_registry_lineage(candidate_ids, candidate_ids)`), bloque tant
  qu'aucune decision humaine sur la source de verite "registered vs
  influential" n'est prise. Reste en observation pure.
- **G7** `independent_pre_oos_approval`, **G13** `kill_switch`/
  `live_approval`, **G14** `retention_policy`/`incident_log` — attestations
  humaines legitimes par nature ; aucune procedure ne peut les "calculer"
  depuis une simulation. Non touches.

## Ordre d'execution decide en session (2026-07-17)

1. **Lot C d'abord** — verifie en session (lecture directe de
   `procedures/data_availability.py`, `sealing.py`, `reproduction_report.py`,
   `monitoring.py`, `incubation_report.py`, `lifecycle.py`) : les 6 fonctions
   sous-jacentes retournent deja un `status` reel confine a
   `{"PASS", "FAIL", "INCONCLUSIVE"}` (aucune valeur hors-catalogue du type
   `"NOT_VALIDATED"`/`"WATCH"` ne remonte au niveau du `status` retourne),
   donc aucune normalisation ni decision de methode n'est necessaire —
   branchement mecanique pur, meme nature que le Lot A1/G9 deja clos.
2. **Lot A2 ensuite** — decouverte en session : contrairement a l'hypothese
   initiale de l'observation source ("le plus urgent... calcul reel"), la
   verification du code (`oos_confidence_interval.py:43`) montre que
   `validate_power_target(power, target_power=0.80)` recoit le meme
   parametre qu'il est cense valider (defaut `0.80`, jamais estime depuis
   l'echantillon) — ce n'est PAS un branchement, c'est un calcul manquant.
   Decision humaine actee en session (2026-07-17, voir section "Journal des
   decisions humaines") : reutiliser le bootstrap stationnaire par blocs
   deja normatif (`procedures/bootstrap.py`, deja gele pour le calcul OOS)
   applique aux rendements pre-OOS de developpement, plutot que d'introduire
   un nouvel estimateur (ex. Newey-West/HAC), pour estimer l'erreur type
   utilisee par le calcul de puissance atteinte prescrit par
   `Protocole/SOP 01` section 10.6.
3. **Lot B en dernier** — necessite une decision de seuil humaine
   explicite (quel critere economique reutiliser pour
   `execution_report`/`nav_reconciliation`, ex. reutiliser l'invariant "NAV
   non plate" deja teste par
   `test_dedicated_venv_m1_segment_records_real_nav_without_false_no_m1`) —
   **cette decision n'est pas encore prise** ; ce chantier mere doit marquer
   une pause explicite avant ce lot et la demander a l'humain le moment
   venu, jamais l'inventer.

## Mecanisme de suivi (sans modification de schema)

`.ai/checkpoint.schema.json` n'a pas de notion de `parent_workstream_id`
(`additionalProperties: false` partout) et
`.ai/governance/AI_MODIFICATION_CHECKLIST.md` n'autorise une mise a jour du
schema que "si le schema existant le permet proprement" — pas d'extension ad
hoc pour ce besoin. Ce chantier utilise donc uniquement les champs deja
existants de `workstream` :

- Ce document devient un workstream `EPIC_CLOTURE_ATTESTATIONS_RESIDUELLES_GATES`
  dans `.ai/checkpoint.json::workstreams`, `track: fix`, qui reste
  `ACTIVE`/`PENDING` tant que tous les lots inclus (C, A2, B) ne sont pas
  `DONE`.
- Chaque lot (C, A2, B) devient son **propre** workstream `fix` distinct
  (obligatoire mecaniquement : `plan.ps1 start` exige un brouillon original
  dans `0 - HUMAN START HERE/` par chantier, jamais un seul brouillon
  partage). Son champ `routing_reason` commence systematiquement par
  `"Sous-chantier <n>/3 de EPIC_CLOTURE_ATTESTATIONS_RESIDUELLES_GATES"` pour
  rester tracable sans lien structurel.
- Ce document (chantier mere) est mis a jour (routing_reason) apres chaque
  cloture de sous-chantier pour refleter l'etat des lots restants, avant de
  demarrer le suivant.
- Le chantier mere n'est clos (`plan.ps1 close`) que lorsque C, A2 et B sont
  tous `DONE` (ou explicitement differes par une nouvelle decision humaine
  documentee ici).

## Non-objectifs

- Ne pas fusionner les 3 lots en un seul commit/chantier d'implementation —
  chacun garde son propre cycle `/start` -> `/evaluate` x2 -> baseline ->
  `/continue` -> bug-hunter + conformance -> `/close`, exactement comme A1.
- Ne pas inventer de decision de seuil pour le Lot B a la place de l'humain.
- Ne pas etendre `.ai/checkpoint.schema.json` (pas de `parent_workstream_id`) ;
  le lien parent/enfant reste narratif (texte de `routing_reason`), pas
  structurel.
- Ne pas toucher G2, G7 (`independent_pre_oos_approval`), G13
  (`kill_switch`/`live_approval`), G14 — hors perimetre par decision humaine
  deja actee dans l'observation source du 2026-07-16.
- Ne pas modifier `Protocole/`, `validators/gate_validator.py`,
  `governance/`, `manifests/`.

## Source

Conversation IA du 2026-07-16/17 : demande humaine explicite de gerer les
lots residuels comme un seul chantier suivi de bout en bout plutot que
disperse. Observation source deja convergee :
`0 - HUMAN START HERE/archive/20260716_OBSERVATION_GATES_ATTESTATIONS_RESIDUELLES.md`.
Plan Lot A1 deja clos : `.ai/archive/20260716_PLAN_CORRECTION_GATE_STATISTIQUE_OOS_MASQUE.md`.

## Exit criteria

Ce chantier mere est `DONE` quand les trois workstreams enfants (Lot C, Lot
A2, Lot B) sont chacun `DONE` dans `.ai/checkpoint.json`, avec pour chacun :
suite runtime complete `PASS`, bug-hunter sans bug confirme ouvert, audit de
conformite sans critere de sortie manquant, et aucune modification hors
perimetre documente pour ce lot precis.

## Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-16 | Demarrer par le Lot A1 (G9 `statistical_gate`) seul parmi A1/A2/B/C (observation source). | Deja execute et clos. |
| 2026-07-17 | Regrouper A2+B+C dans un seul chantier mere suivi, avec enchainement automatique des sous-chantiers jusqu'a cloture generale, sauf pause obligatoire sur toute decision de seuil/methode. | Autorise la creation de ce document et le routage successif de C, A2, B sans repasser par l'humain entre les lots, sauf aux points de decision explicitement identifies. |
| 2026-07-17 | Ordre revise en session : C (mecanique, verifie) avant A2 (calcul manquant, decouvert en session) avant B (decision de seuil deja connue, non tranchee). | Remplace l'ordre initialement propose (A2 d'abord) par C d'abord. |
| 2026-07-17 | Lot A2 : reutiliser le bootstrap stationnaire par blocs deja normatif (`procedures/bootstrap.py`) applique aux rendements pre-OOS de developpement pour estimer l'erreur type de la puissance atteinte, plutot qu'un nouvel estimateur (Newey-West/HAC). | Autorise la redaction et l'implementation du sous-chantier Lot A2 avec cette methode, sans nouvelle consultation humaine sur ce point precis. |

## Suite immediate

Premier sous-chantier a rediger et router : **Lot C**, seul mecaniquement
sur (aucune decision requise, verifie en session sur les 6 fonctions
sous-jacentes).
