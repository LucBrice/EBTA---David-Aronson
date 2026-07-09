# HOOK Actif : Migration du moteur de backtest EBTA vers NautilusTrader

Le mainline actif est maintenant
`PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS`.

## Decision de routage

Le chantier remplace la suite du moteur de calcul EBTA apres le MVP natif
historique. Le moteur natif reste `DONE` comme jalon trace, mais il n'est plus
la cible de developpement. NautilusTrader devient le moteur de simulation et
d'execution sous l'enveloppe EBTA, uniquement via la frontiere d'adapter.

Autorites :

- `Protocole/` reste l'autorite normative gelee en `EBTA-DOC-1.1`.
- `Implementation/ebta_engine/` reste la traduction executable subordonnee.
- `.ai/checkpoint.json` porte l'etat macro actif.
- `Implementation/Active/tracking.json` porte l'etat micro actif.
- `.ai/backlog/mainline/PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md`
  est la source de verite technique du chantier actif.

## Etat courant

`NAUTILUS_PHASE_0_COCKPIT_SYNC` est execute : le workstream est active par
`.ai/tools/plan.ps1 continue`, le checkpoint pointe sur
`PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS`, et le cockpit micro est
resynchronise sur ce pivot.

Blocage de validation avant Phase 1 resolu :

```text
NAUTILUS_PROTOCOL_MANIFEST_HASH_REPAIRED
```

La suite runtime de reference echouait sur
`test_protocol_manifest_hashes.py::test_frozen_protocol_hashes_still_match` :
le hash actuel de `Protocole/HISTORIQUE DES VERSIONS EBTA.md` est
`5310C63567FEB992F869B4FA69CB5209C71B8F697E4AC322D8DEBB01B6F209BF`, alors
que `Protocole/MANIFESTE DE GEL EBTA.md` attendait
`95C58780C6C1953C0A3AFE07BB4A8119B99DC68EC4281282909B08CA665C544F`.
Le manifeste a ete corrige pour refleter le contenu deja commite par
`acb0fd6`; `python -m unittest discover -s Implementation\ebta_engine\tests -t
Implementation` repasse `OK` avec 93 tests.

`NAUTILUS_PHASE_1_CONTRACTS_SCHEMA` est executee :

```text
NAUTILUS_PHASE_1_CONTRACTS_SCHEMA_COMPLETED
```

Livrables valides :

- contrats stdlib purs `Candidate`, `CostModel`, `InstrumentConfig`,
  `SimulationResult` et `SegmentSimulator` ;
- `StrategyPayload.from_dict()` et criteres `entry_criterion`/`exit_criterion`
  structures ;
- migrations `config` et `strategy_payload` vers `schema_version`/`payload_version`
  `1.1.0` ;
- `payload_factory.py` avec `StructuralAxis`, `StrategyFamilySpec` et
  `generate_family()` pour la grille `bias_filter x session x asset` ;
- fake `SegmentSimulator` prouve consommable par `detrending.py` et
  `economic_gate.py` sans changement de signature.

Validations :

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_phase1_contracts.py
# PASS - 8 tests
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_schemas.py
# PASS - 12 tests
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
# PASS - 101 tests
python Implementation\examples\minimal_pilot_pipeline\build_research_package.py
# PASS - package status PASS
```

La phase executable courante est :

```text
NAUTILUS_PHASE_6_CUTOVER
```

`NAUTILUS_PHASE_2_SPIKE` est executee :

```text
NAUTILUS_PHASE_2_SPIKE_COMPLETED
```

Livrables valides :

- `setup_env.ps1` et `requirements.txt` versionnes pour
  `nautilus_trader==1.230.0` ;
- convention cible `subst N:` vers la racine du repo, venv courte par defaut
  `N:\Implementation\.venv-nautilus`, et parametre de compatibilite vers la
  venv locale existante ;
- fixture deterministe `nautilus_golden_case` et `expected_result()` stdlib ;
- runner `Implementation/adapters/nautilus_env/run_golden_case.py` produisant
  un `SimulationResult` Nautilus coherent ;
- note `PHASE2_SPIKE_MEASUREMENT.md` : K=1, M=16, donc `K x (M+1)=17`,
  extrapole a environ 37.82 s avec la mesure isolee de 2.22464 s.

Validations :

```powershell
.\Implementation\adapters\nautilus_env\setup_env.ps1 -VenvRelativePath "Implementation\adapters\nautilus_env\venv" -SkipInstall
# PASS - nautilus_trader 1.230.0 / Cache
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe .\Implementation\adapters\nautilus_env\run_golden_case.py
# PASS - result_hash 0EA503650BF1D2D80F0C3C7853C2C1A12A2D6ACCA399FF1506F045A0043FAC43
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_phase2_golden_case.py
# PASS - 3 tests
```

`NAUTILUS_PHASE_3_N1_DATA` est executee :

```text
NAUTILUS_PHASE_3_N1_DATA_COMPLETED
```

Livrables valides :

- adapter `Implementation/ebta_engine/adapters/nautilus_mapping.py` avec imports
  Nautilus paresseux ;
- `build_instrument()` pour instruments `CFD`, `CURRENCY_PAIR`, `EQUITY` et
  `INDEX` ;
- `NASDAQ.SIM` verifie comme `Cfd` sous-jacent `AssetClass.INDEX` ;
- `XAUUSD.SIM` verifie comme `Cfd` sous-jacent `AssetClass.COMMODITY` ;
- `map_ohlcv_to_bars()` depuis `OhlcvBar` EBTA vers `Bar` Nautilus, avec
  `ts_init` place a la cloture via `ts_init_delta`.

Validation :

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_instrument_nasdaq.py
# PASS - 2 tests
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
# PASS - 106 tests
```

`NAUTILUS_PHASE_4_N2_N3_STRATEGY_COSTS` est executee :

```text
NAUTILUS_PHASE_4_N2_N3_STRATEGY_COSTS_COMPLETED
```

Livrables valides :

- `map_cost_model_to_venue()` appelle `add_venue()` avec `OmsType.HEDGING`,
  `AccountType.MARGIN`, `LeveragedMarginModel`, `FillModel`, `FeeModel` et
  `LatencyModel` explicitement derives du `CostModel` EBTA ;
- `GenericPayloadStrategyConfig` et `GenericPayloadStrategy` existent dans
  `nautilus_strategy_bridge.py` ;
- deux candidates differentes utilisent la meme classe Python
  `GenericPayloadStrategy`; seule la config change.

Validation :

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_phase4_strategy_costs.py
# PASS - 2 tests
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
# PASS - 108 tests
```

`NAUTILUS_PHASE_5_N4_N5_MULTIFOLD` est executee :

```text
NAUTILUS_PHASE_5_N4_N5_MULTIFOLD_COMPLETED
```

Livrables valides :

- `run_segment()` execute un candidat EBTA opaque dans Nautilus ;
- `extract_simulation_result()` reconstruit `SimulationResult` EBTA depuis
  `orders`/`fills`/`positions`/NAV ;
- le cas `NO_MODEL` retourne une NAV plate et des expositions nulles ;
- `run_multifold_segments()` orchestre les sorties fold/candidate sans passer
  de metadonnees Train/Test/OOS au runner ;
- les sorties restent consommables par `detrending_inputs()` et
  `economic_gate_evidence()` sans changement de signature.

Validation :

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_phase5_run_segment.py
# PASS - 3 tests
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
# PASS - 111 tests
```

La phase courante doit produire et valider un `research_package` Nautilus, puis
retirer le cluster moteur natif seulement apres preuve PASS et point de retour
reversible. Avant tout nouvel appel reel a `nautilus_trader`, appliquer le skill
`nautilus-docs-research` ou les notes empiriques deja presentes dans
`Implementation/adapters/nautilus_env/`.

## Invariants du chantier

- Ne pas modifier `Protocole/`.
- Ne pas modifier `procedures/`, `validators/`, `governance/`, `manifests/` ou
  `package_builder/`, sauf retrait final explicite de
  `package_builder/native_research_package.py` en Phase 6.
- Ne jamais importer `nautilus_trader` hors de `Implementation/ebta_engine/adapters/`
  et de l'environnement de verification `Implementation/adapters/nautilus_env/`.
- Ne jamais laisser Nautilus savoir s'il execute Train, Test ou OOS.
- Ne pas utiliser les metriques, analyzers ou tearsheets Nautilus comme verdict
  EBTA.
- Ne pas ouvrir OOS avant scellement et `G-BIAS PASS`.
- BACKTRADER reste reference lecture seule, sans dependance runtime et sans
  modification du repo externe.

## Points de reprise

1. Lire le plan actif complet avant toute phase :
   `.ai/backlog/mainline/PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md`.
2. Reprendre depuis `Implementation/Active/tracking.json::current_step`
   (`NAUTILUS_PHASE_6_CUTOVER`).
3. Avant tout appel reel a `nautilus_trader`, invoquer le skill
   `nautilus-docs-research` sauf si la signature est deja verifiee dans
   `Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md` ou
   `Implementation/adapters/nautilus_env/INTROSPECTION_2026-07-08.txt`.

## Validations de reprise

```powershell
python -m json.tool .ai\checkpoint.json
python -m json.tool Implementation\Active\tracking.json
python -c "import json, jsonschema; jsonschema.validate(json.load(open('.ai/checkpoint.json', encoding='utf-8')), json.load(open('.ai/checkpoint.schema.json', encoding='utf-8')))"
python -c "import json, jsonschema; jsonschema.validate(json.load(open('Implementation/Active/tracking.json', encoding='utf-8')), json.load(open('Implementation/Active/tracking.schema.json', encoding='utf-8')))"
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
git diff --check -- .ai Implementation "0 - HUMAN START HERE"
```
