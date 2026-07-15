# Observation — le statut global de package ignore les gates reellement en echec

> Note d'intake, pas un plan. Deposee ici pour audit et structuration, suite
> a la cloture de `PLAN_CORRECTION_GATE_STATISTIQUE_WRC_MASQUE` (2026-07-15)
> et au risque `R3 — Preuve vs attestation` de
> `AUDIT_MATURITE_MOTEUR_RECHERCHE_2026-07-13.md` (section "Suite proposee").

## Constat

La correction WRC deja livree
(`.ai/archive/20260715_PLAN_CORRECTION_GATE_STATISTIQUE_WRC_MASQUE.md`) rend
les artefacts JSON individuels honnetes (`gates.json.wrc_status`,
`economic.json.statistical_status`/`.global_status`,
`incubation_gate.json.status`), mais elle a explicitement laisse hors
perimetre le verdict global `validate_package_dir()["status"]`, qui reste
`PASS` meme quand un WRC reel a echoue. Deux defauts de lecture, verifies
directement dans le code le 2026-07-15 :

1. `validators/gate_validator.py::validate_gates()` (ligne 41) :
   `missing = [name for name in requirements if not evidence.get(name)]`.
   Une chaine `"FAIL"` est truthy en Python — `not "FAIL"` vaut `False` —
   donc un `wrc_status="FAIL"` (G4) ou `pre_oos_robustness_verdict="FAIL"`
   (G5) est compte comme present, jamais comme un echec. Le validateur
   verifie la presence/verite Python d'un champ, jamais sa valeur, alors
   que ces deux champs portent un verdict `"PASS"/"FAIL"/"INCONCLUSIVE"`.
2. `validators/package_validator.py` : `reports/incubation_gate.json` est
   absent de `REQUIRED_PACKAGE_PATHS` (ligne 18-41) et jamais lu ;
   `_semantic_consistency_errors()` (ligne 171-217) ne lit `economic.json`
   que pour verifier la presence de trois cles quand
   `economic_status == "PASS"`, jamais la valeur de `economic.json.global_status`
   ni `.statistical_status`.

Le defaut est deja **prouve mecaniquement** dans le depot :
`tests/test_nautilus_research_package.py::test_real_wrc_fail_reaches_economic_and_incubation_gates`
(livre par le plan WRC) construit un `research_package` reel ou
`wrc["verdict"] == "FAIL"`, `economic["global_status"] == "FAIL"`,
`incubation["status"] == "FAIL"`, et affirme pourtant
`report["status"] == "PASS"` (ligne 65).

**Consequence concrete** : un candidat qui echoue reellement au test WRC (ou
au verdict de robustesse) produit quand meme un package dont le statut global
consulte par un lecteur est `PASS`. C'est exactement le risque `R3` :
attestation structurelle qui masque un echec scientifique reel.

## Ce que cette note ne fait PAS

- Ne propose aucune reecriture de `procedures/wrc.py`,
  `procedures/economic_gate.py`, `procedures/lifecycle.py`, ou
  `procedures/robustness.py` — tous corrects et testes ; le defaut est dans
  la **lecture** qu'en font les deux validateurs.
- Ne couvre pas le defaut de **contenu** distinct du gate robustesse
  (`_write_reports()` ligne 215 fige `pre_oos_robustness_verdict="PASS"` au
  lieu d'appeler la fonction `pre_oos_robustness_verdict()` existante) — meme
  patron que le defaut WRC deja corrige, mais cote contenu ; a traiter par
  un plan `fix` separe pour ne pas melanger correction de validateur et
  correction de contenu.
- Ne couvre pas la refonte des ~35 autres booleens d'attestation de
  `gates.json` — attestations de gouvernance necessitant un vrai mecanisme
  de decision humaine.

## Suite proposee

Transformer cette observation en plan `fix` cible sur les deux validateurs
(`gate_validator.py` : value-check des champs de verdict ; `package_validator.py` :
`incubation_gate.json` requis et lu, `economic.json.global_status` lu), avec
preuve de non-regression par inversion de l'assertion existante deja
construite par le plan WRC, suivant le patron des deux plans precedents de
cette famille.
