# Prompt d'exécution autonome — Plan R1+R2 (moteur de signaux réel + extraction Nautilus)

## CONTEXTE ET ÉTAT INITIAL

Tu reprends l'exécution d'un chantier déjà planifié, audité et routé dans un dépôt EBTA (Evidence-Based Technical Analysis).

**Dépôt** : `D:\Livre\Trading\Trading algorithmic\EBTA - David Aronson`  
**Plan actif** : `.ai/backlog/mainline/PLAN_R1_R2_SIGNAUX_ET_EXTRACTION_NAUTILUS.md`  
**Commit de départ** : `ef90df6` (2026-07-13 — plan planifié, aucun code implémenté)  
**Suite de tests de référence** : 110 tests PASS (`python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`)

---

## INSTRUCTIONS OBLIGATOIRES DE DÉMARRAGE

**Avant d'écrire une seule ligne de code**, tu dois lire dans cet ordre :

1. `AGENTS.md` — règles de gouvernance du dépôt  
2. `.ai/README.md` — cockpit et cycle de vie des chantiers  
3. `.ai/checkpoint.json` — état machine courant  
4. `Implementation/Active/HOOK.md` — état courant du runtime  
5. `.ai/backlog/mainline/PLAN_R1_R2_SIGNAUX_ET_EXTRACTION_NAUTILUS.md` — **plan à exécuter intégralement**  
6. `Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md` — API Nautilus vérifiée empiriquement (multi-timeframe, portfolio, analyzer, ts_event)  
7. `Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py` — code stub actuel à remplacer  
8. `Implementation/ebta_engine/adapters/nautilus_mapping.py` — extracteur bugué à corriger (lignes 276–335)  
9. `Implementation/ebta_engine/strategies/payloads.py` — payloads E–I existants  
10. `Implementation/ebta_engine/strategies/contracts.py` — contrat `SimulationResult` **immuable, ne pas modifier**  
11. `Implementation/ebta_engine/data/local_ohlcv.py` — chargeur de barres existant (1 timeframe/actif)  
12. `Implementation/ebta_engine/data/walk_forward.py` — `WalkForwardSplitter` existant (conserver)

---

## OBJECTIF GLOBAL

Implémenter **intégralement** les phases 0 à 5 du plan R1+R2 :

- **R1** : implémenter un moteur de signaux incrémental natif (state machine barre-par-barre) pour les payloads E, F, G/H/I de la stratégie liquidity sweep, avec test de parité mécanique contre un oracle vectorisé.
- **R2** : corriger l'extraction des métriques de simulation depuis la comptabilité réelle de Nautilus (portfolio/analyzer/rapports), éliminer le bug de reconstruction manuelle.

Le plan définit l'ordre, les dépendances, les gates bloquants et les critères de sortie. Tu dois les respecter rigoureusement.

---

## RÈGLES D'EXÉCUTION ABSOLUES

### 1. Ordre et dépendances — respecter le chemin critique

Exécute les phases **dans cet ordre strict**, sans permuter ni paralléliser :

```
Phase 0 : data/resample.py (resampling causal M1→M3/M15/H1/H4/D1)
Phase 1 : strategies/signals/*.py (oracle vectorisé — port BACKTRADER lecture seule)
Phase 2 : strategies/registry.py (interface IncrementalSignalStrategy + dict d'enregistrement)
Phase 3 : strategies/incremental/*.py (payloads E, F, G/H/I incrémentaux + tests de parité)
Phase 4 : adapters/nautilus_strategy_bridge.py (refactoring bridge → délégateur au registry)
Phase 5 : adapters/nautilus_mapping.py::extract_simulation_result (extraction réelle R2)
```

**Gate bloquant transversal** : avant de commencer chaque phase, la suite de référence doit être PASS :
```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
```
Si elle échoue, corriger avant de continuer. Ne jamais déclarer une phase terminée si ce gate est rouge.

### 2. Vérifications intermédiaires — commandes exactes

Après chaque phase, exécuter la commande de validation correspondante. Ne pas passer à la phase suivante si la vérification échoue :

**Phase 0** :
```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_resample.py
```

**Phase 1** :
```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p "test_signals_*.py"
```

**Phase 2** :
```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_registry.py
```

**Phase 3** :
```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p "test_incremental_parity_*.py"
```
> Si les données M1 sont absentes de `DEFAULT_DATA_ROOT`, les tests de parité doivent émettre `SKIP` avec un message explicite (pas `FAIL`) — voir section "Caveats CI" ci-dessous.

**Phase 4** :
```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_phase4_strategy_costs.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_phase5_run_segment.py
```

**Phase 5** :
```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_r2_extraction.py
python -c "from pathlib import Path; from ebta_engine.validators.package_validator import validate_package_dir; print(validate_package_dir(Path('Implementation/research_packages/nautilus_mvp'))['status'])"
```

### 3. Correction immédiate des erreurs

Si un test échoue, une incohérence est détectée, ou une erreur d'intégration est constatée :
- Corriger immédiatement dans la phase en cours.
- Ne pas passer à la phase suivante tant que le critère de sortie de la phase courante n'est pas vert.
- Ne pas contourner silencieusement un gate bloquant.

### 4. Ne pas s'arrêter en cours de route

Tu ne t'arrêtes pas après une implémentation partielle tant qu'une tâche du plan reste réalisable. Les seules causes d'arrêt légitimes sont :
- Une décision humaine explicite est requise (listée dans le plan section 10 ou identifiée en cours d'exécution).
- Un blocage technique impossible à résoudre sans information externe (ex. données M1 absentes, API Nautilus rompue).
- La limite des 5 phases est atteinte et toutes sont vérifiées.

Dans tous les cas, documenter précisément l'état final (voir section "Rapport de clôture").

---

## INVARIANTS ABSOLUS — JAMAIS VIOLER

1. **Aucune modification de `Protocole/`, `procedures/`, `validators/`, `governance/`, `manifests/`.**
2. **Aucune modification du contrat `SimulationResult`** (`strategies/contracts.py`) — ses champs, types et sémantique sont gelés.
3. **Aucun import de `nautilus_trader` en dehors de `adapters/` et `nautilus_env/`.**
4. **La Strategy ne reçoit jamais le `fold_id` ou le rôle de segment** (Train/Test/OOS) — seulement des barres.
5. **L'oracle vectorisé (`strategies/signals/`) ne produit jamais de décisions en production** — test de parité uniquement.
6. **Aucune dépendance runtime vers BACKTRADER** — portage de logique unique en lecture seule, jamais d'import.
7. **Aucune nouvelle dépendance externe** — `cachetools` délibérément absent ; `pandas`/`numpy`/`tzdata`/`pytz` déjà présents dans le venv et l'interpréteur de base.
8. **Pas de branchement dans `nautilus_research_package.py`** (chemin de production) tant que R4 (`_daily_sample`) n'est pas résolu — chantier séparé, hors scope.

---

## DÉCISIONS D'ARCHITECTURE ACTÉES (ne pas remettre en question)

### Architecture en 5 couches

| # | Couche | Décision |
|---|---|---|
| 1 | Exploration/screening | Pipeline BACKTRADER vectorisée existante — hors EBTA/Nautilus, ne pas toucher |
| 2 | Stratégie/exécution | Incrémental natif barre-par-barre — **investissement prioritaire de ce chantier** |
| 3 | Validation statistique | `procedures/` déjà stables — ne pas modifier |
| 4 | Artefacts/reproductibilité | `package_builder/` déjà stable — ne pas modifier |
| 5 | Portefeuille/live | Délibérément différé — ne rien construire |

### Pattern incrémental natif (jamais signal-replay)

La strategy est une **state machine barre-par-barre** :
- Elle maintient un état interne mis à jour à chaque `on_bar()`.
- Elle ne précalcule pas de séries de décisions futures.
- Elle est identique entre `BacktestEngine` (backtest de recherche) et un nœud live Nautilus.
- L'oracle vectorisé (`strategies/signals/`) sert uniquement à valider mécaniquement la state machine (test de parité), jamais à produire des signaux en production.

### Registry de stratégies

- Interface : `IncrementalSignalStrategy` (Protocol Python).
- Dict : `STRATEGY_REGISTRY: dict[str, type[IncrementalSignalStrategy]]`.
- Règle : ajouter le payload E = créer `strategies/incremental/payload_e.py` + s'enregistrer dans le dict. Ne jamais modifier `nautilus_mapping.py`, `nautilus_research_package.py`, `procedures/` ou `governance/`.

### Extraction réelle R2 (Option A)

- `GenericPayloadStrategy` maintient `self._nav_snapshots: list[tuple[int, float, float]]` (ts_event_nanos, equity, net_exposure) mis à jour **uniquement sur les barres M1** (timeframe de référence, discriminé par `bar.bar_type`).
- `extract_simulation_result` lit cette liste via `engine.trader.strategies[0]._nav_snapshots`.
- Elle est décomposée en 3 fonctions privées : `_extract_nav_series(strategy)`, `_extract_costs(fills_report)`, `_extract_positions(positions_report)`.
- `total_costs` = somme des commissions réelles depuis `generate_order_fills_report()`.

### Injection multi-BarType dans Nautilus

Nautilus **ne resamble pas** les barres lui-même. C'est `run_segment()` qui :
1. Appelle `resample_ohlcv(bars, target_minutes)` pour chaque timeframe (M1, M3, M15, H1, H4, D1).
2. Appelle `map_ohlcv_to_bars()` pour chaque résolution avec le bon `interval_value`/`interval_unit`.
3. Appelle `eng.add_data()` pour chaque série.

---

## DÉTAILS D'IMPLÉMENTATION PAR PHASE

### Phase 0 — `data/resample.py`

**Fonction principale** :
```python
def resample_ohlcv(bars: list[OhlcvBar], target_minutes: int) -> list[OhlcvBar]:
    """Resampling causal right-closed des barres M1 EBTA vers target_minutes.
    
    Sémantique : la barre agrégée couvrant [t_open, t_close] utilise toutes les
    barres M1 dont le timestamp satisfait t_open < ts <= t_close.
    La borne inférieure est exclue, la borne supérieure est incluse.
    Cette sémantique est identique à pd.Grouper(freq='...') avec closed='right'.
    
    Invariant : aucune barre agrégée ne contient de barre M1 dont le timestamp > t_close.
    """
```

**Tests** (`tests/test_resample.py`) :
- Alignment des timestamps (barre H1 produite à l'heure exacte de clôture).
- Conservation du volume (somme des volumes M1 = volume H1).
- Monotonie (timestamps croissants).
- Borne supérieure incluse (une barre M1 à `t=09:00` contribue à la barre H1 se terminant à `09:00`, pas à celle de `10:00`).

---

### Phase 1 — `strategies/signals/*.py` (oracle vectorisé)

**Source** : logique lue en lecture seule depuis `D:\TRADING\ENTREPRISE\...\BACKTRADER\features\` (port unique, jamais d'import runtime vers ce dépôt).

**Modules à créer** (stdlib + pandas/numpy, sans `cachetools`) :

```
strategies/signals/
  __init__.py
  engulfing.py       # detect_engulfing(df: pd.DataFrame) -> pd.Series[bool]
  market_bias.py     # compute_market_bias(df: pd.DataFrame, tf_minutes: int) -> pd.Series[int]
  liquidity.py       # compute_liquidity_pools(df: pd.DataFrame, expiry_days: int) -> pd.Series[list]
  sessions.py        # filter_session(df: pd.DataFrame, session: str) -> pd.Series[bool]  (DST-aware)
  entry_signal.py    # compute_entry_signals(...) -> pd.Series[int]
                     # garde anti-signal-simultané BUY+SELL conservée
                     # anti-lookahead : shift(1)/shift(2) pour biais MTF
```

**Tests** : chaque module a ses propres tests unitaires sur données synthétiques (pas de données réelles requises).

---

### Phase 2 — `strategies/registry.py`

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class IncrementalSignalStrategy(Protocol):
    def on_bar(self, bar: "Bar") -> None: ...
    def should_enter(self) -> tuple[bool, "OrderSide | None"]: ...
    def should_exit(self, bar_count_since_entry: int) -> bool: ...

STRATEGY_REGISTRY: dict[str, type[IncrementalSignalStrategy]] = {}

def get_strategy(payload_code: str) -> type[IncrementalSignalStrategy]:
    if payload_code not in STRATEGY_REGISTRY:
        raise KeyError(f"Unknown payload code: {payload_code!r}. Registered: {sorted(STRATEGY_REGISTRY)}")
    return STRATEGY_REGISTRY[payload_code]
```

**Tests** : `KeyError` sur code inconnu, retourne le bon type une fois les classes créées (stubs acceptables jusqu'en Phase 3).

---

### Phase 3 — `strategies/incremental/*.py`

**Ordre de construction** (ne pas tout implémenter d'un coup) :

1. **Payload E** (le plus simple) : état M1 (2–3 dernières bougies pour l'engulfing) + pool de liquidité M15 (liste avec expiration) + state machine sweep→engulfing→confirmation M3.
2. **Test de parité E** : oracle vectorisé + state machine incrémentale sur le même segment → mêmes timestamps de décision barre par barre.
3. **Payload F** (+biais MTF, mis à jour uniquement sur barres H1/H4/D1) + parité F.
4. **Payloads G/H/I** (+filtre de session depuis `bar.ts_event`) + parité G/H/I.

**Protocole warm-up** :
- `GenericPayloadStrategyConfig` expose `warmup_bar_count: int` (défaut 0).
- `run_segment()` reçoit `warmup_bars: list[OhlcvBar]` (optionnel) concaténés en tête des barres de segment.
- Dans `on_bar()`, la Strategy ignore les ordres pendant les `warmup_bar_count` premières barres — warm-up initialise l'état interne sans produire de trades.

**Tests obligatoires** :
- Parité oracle pour chaque payload (E, F, G/H/I) sur segment réel — ou `SKIP` explicite si données M1 absentes.
- Payloads E, F, G/H/I produisent des décisions différentes sur le même segment.
- Test direction short : `OrderSide.SELL` soumis et position short dans `generate_positions_report()`.
- Test warm-up (R1.7) : pool né avant le warm-up visible à la 1ère barre active ; état froid manque ce pool.
- Test anti-fuite (R1.10) : même candidat, barres identiques étiquetées Train vs OOS → même `SimulationResult`.

---

### Phase 4 — `adapters/nautilus_strategy_bridge.py` (refactoring)

**`GenericPayloadStrategyConfig`** :
```python
class GenericPayloadStrategyConfig(StrategyConfig, frozen=True):
    payload: dict
    instrument_id: InstrumentId
    bar_types: list[str]          # NOUVEAU — liste de BarType strings (M1, M3, M15, H1, H4, D1)
    trade_size: Decimal
    warmup_bar_count: int = 0     # NOUVEAU — nombre de barres de warm-up à ignorer pour les ordres
```

**`GenericPayloadStrategy`** :
- `on_start()` : itérer sur `self.config.bar_types`, appeler `subscribe_bars()` pour chacun.
- `on_bar(bar)` : discriminer par `bar.bar_type` — router vers la state machine incrémentale.
- Mettre à jour `self._nav_snapshots` **uniquement sur les barres M1**.
- `self._venue` dérivé de `self.config.instrument_id.venue` à l'init.
- Si après `warmup_bar_count` barres aucune barre M1 reçue → `logging.warning("[EBTA] No M1 bar received...")` + `{"no_m1_signal": True}` dans les métadonnées.

**Skip golden-case** : décorer `test_nautilus_phase2_golden_case.py` avec `@unittest.skip("Recalibration R2 Phase 5 en cours")` au début de Phase 4 ; retirer après recalibration Phase 5.

---

### Phase 5 — `adapters/nautilus_mapping.py::extract_simulation_result` (R2)

**Décomposition SRP** :
```python
def _extract_nav_series(strategy) -> list[tuple[str, float, float]]:
    """Lit strategy._nav_snapshots → (timestamp_iso, equity, net_exposure) par barre M1."""

def _extract_costs(fills_report) -> float:
    """Somme la colonne 'commission' du rapport de fills."""

def _extract_positions(positions_report) -> list[dict]:
    """Construit la liste EBTA depuis les lignes du rapport."""

def extract_simulation_result(*, candidate_id, instrument_id, source_bars, engine, starting_nav, quantity):
    """Orchestre les 3 fonctions privées + construit SimulationResult."""
```

**Cas NO_MODEL** : dériver depuis `portfolio.is_flat` **ET** rapport de fills vide **ET** `len(strategy._nav_snapshots) == 0`. Attention : `portfolio.is_flat` peut être `True` après annulation d'ordres — vérifier les deux conditions.

**Tests obligatoires** :
- Bug post-sortie éliminé : après clôture, NAV plate (série `equity` constante après le dernier trade).
- `total_costs > 0` sur candidat qui trade avec `maker_fee/taker_fee` non nuls.
- Cas-limite NO_MODEL : ordre soumis puis annulé → `_flat_simulation_result` correct.

**Recalibration golden-case** : retirer le `@skip`, recalibrer `tests/fixtures/nautilus_golden_case/expected_result.py` sur la vraie sortie. Le `result_hash` changera — attendu. Documenter dans `NAUTILUS_API_NOTES.md`.

---

## CAVEATS CI — COMPORTEMENTS ATTENDUS, NE PAS TRAITER COMME ERREURS

1. **Tests de parité avec données M1 absentes** : les tests `test_incremental_parity_*.py` doivent émettre `unittest.SkipTest("M1 data not found at DEFAULT_DATA_ROOT — skip parity test")`, pas `FAIL`. Ce comportement est attendu sur toute machine sans les données réelles.

2. **Golden-case FAIL pendant Phase 4** : `test_nautilus_phase2_golden_case.py` est skippé pendant Phase 4–5 (decorator `@unittest.skip`). Son échec pendant ces phases n'est pas une régression — c'est le signe qu'il faut le recalibrer en Phase 5.

3. **`result_hash` du golden-case différent après R2** : le hash va changer après recalibration. Ce n'est pas une régression. Documenter dans `NAUTILUS_API_NOTES.md` avant de le mettre à jour.

4. **`logging.warning("[EBTA] No M1 bar received...")` en production** : message attendu sur le chemin de production actuel (qui ne fournit qu'1 barre/jour via `_daily_sample`). Trace l'incompatibilité sans bloquer — résolution différée à R4.

---

## PÉRIMÈTRE DE FICHIERS AUTORISÉS ET INTERDITS

### Autorisés (créer ou modifier) :
```
Implementation/ebta_engine/data/resample.py                    [CRÉER]
Implementation/ebta_engine/strategies/signals/                  [CRÉER — 5 modules]
Implementation/ebta_engine/strategies/registry.py               [CRÉER]
Implementation/ebta_engine/strategies/incremental/              [CRÉER — 3 modules]
Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py [MODIFIER]
Implementation/ebta_engine/adapters/nautilus_mapping.py         [MODIFIER — extract_simulation_result]
Implementation/ebta_engine/tests/                               [CRÉER — nouveaux tests]
Implementation/ebta_engine/tests/fixtures/nautilus_golden_case/expected_result.py [MODIFIER — Phase 5]
Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md      [MODIFIER — documenter bascule R2]
```

### Interdits (ne jamais modifier) :
```
Protocole/                                          [NORME — intouchable]
Implementation/ebta_engine/procedures/              [INTOUCHABLE]
Implementation/ebta_engine/validators/              [INTOUCHABLE]
Implementation/ebta_engine/governance/              [INTOUCHABLE]
Implementation/ebta_engine/manifests/               [INTOUCHABLE]
Implementation/ebta_engine/strategies/contracts.py  [CONTRAT GELÉ]
Implementation/ebta_engine/package_builder/nautilus_research_package.py  [HORS SCOPE — bloqué par R4]
Implementation/ebta_engine/data/walk_forward.py     [CONSERVER TEL QUEL]
Implementation/ebta_engine/adapters/nautilus_mapping.py::run_multifold_segments  [CONSERVER]
.ai/checkpoint.json                                 [METTRE À JOUR UNIQUEMENT via plan.ps1]
```

---

## RAPPORT DE CLÔTURE OBLIGATOIRE

À la fin de l'exécution, produire un rapport structuré couvrant :

### 1. Ce qui a été entièrement implémenté
Pour chaque phase (0–5), lister :
- Les fichiers créés ou modifiés.
- Le résultat de la commande de vérification (PASS / SKIP / FAIL + raison).
- Si SKIP : préciser si c'est attendu (caveat CI) ou bloquant.

### 2. Ce qui a été partiellement implémenté
Pour chaque fonctionnalité partiellement traitée :
- Ce qui a été fait.
- Ce qui reste à faire.
- La raison du blocage.

### 3. Ce qui reste à faire
Lister les tâches non démarrées avec la raison (dépendance non résolue, décision humaine requise, données manquantes).

### 4. Ce qui nécessite une décision humaine
Pour chaque point nécessitant une décision :
- Décrire précisément la question.
- Proposer les options disponibles avec leur impact.
- Indiquer quelle option est recommandée et pourquoi.

### 5. Vérification globale finale

Après le rapport de clôture, effectuer une vérification globale et exhaustive de l'ensemble de l'implémentation par rapport au plan initial. Cette vérification est **distincte** des validations intermédiaires — elle couvre l'ensemble, pas seulement la dernière phase.

Exécuter :
```powershell
# Suite complète
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation

# validate_package_dir (si Phase 5 terminée)
python -c "from pathlib import Path; from ebta_engine.validators.package_validator import validate_package_dir; print(validate_package_dir(Path('Implementation/research_packages/nautilus_mvp'))['status'])"

# Vérification no residual stub
python -c "import ast, sys; src=open('Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py').read(); tree=ast.parse(src); print('BUY hardcoded check:', 'OrderSide.BUY' in src)"

# Vérification no total_costs hardcoded
python -c "src=open('Implementation/ebta_engine/adapters/nautilus_mapping.py').read(); print('total_costs=0.0 check:', 'total_costs=0.0' in src)"
```

Confirmer point par point que toutes les fonctionnalités, modifications, tests, et décisions prévues dans le plan ont été implémentées. Si des éléments manquent, les identifier précisément avec leur catégorie (entièrement implémenté / partiellement / reste à faire / décision humaine requise).

---

## RÉFÉRENCE RAPIDE DES CRITÈRES DE SORTIE DU PLAN

| Gate | Condition binaire vérifiable |
|---|---|
| G0 | `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` → PASS avant chaque phase |
| G1 | Test parité payload E → PASS (ou SKIP si données absentes, avec message explicite) |
| G2 | Test parité payload F → PASS (ou SKIP) |
| G3 | Test parité payloads G/H/I → PASS (ou SKIP) |
| G4 | Test direction short : `OrderSide.SELL` → position short dans `generate_positions_report()` → PASS |
| G5 | Test anti-fuite : même `SimulationResult` Train vs OOS sur barres identiques → PASS (NO GO absolu) |
| G6 | Test NAV plate après clôture → PASS ; `total_costs > 0` sur candidat qui trade → PASS ; `validate_package_dir()` → PASS |

**Exit criteria global du plan** (Definition of Done) :
- [ ] Phases 0–5 validées individuellement.
- [ ] Suite 110+ tests PASS (aucune régression).
- [ ] Golden-case recalibré, `result_hash` documenté dans `NAUTILUS_API_NOTES.md`.
- [ ] `validate_package_dir()` PASS après Phase 5.
- [ ] Aucune modification hors périmètre (Protocole, procedures, validators, governance, manifests, contracts.py).
- [ ] `OrderSide.BUY` en dur absent de `on_bar()`.
- [ ] `total_costs=0.0` en dur absent de `extract_simulation_result`.

---

*Ce prompt a été généré le 2026-07-13 depuis le commit `ef90df6`, après 2 passages d'audit d'architecture (`/evaluate`) et correction de 10 angles morts ou violations de principes SOLID.*
