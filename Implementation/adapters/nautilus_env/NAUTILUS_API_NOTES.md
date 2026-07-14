# Notes API NautilusTrader — faits vérifiés

Cache versionné de faits vérifiés sur l'API `nautilus_trader`, alimenté par
le skill `nautilus-docs-research`. Chaque entrée distingue :

- **Documenté** : fait trouvé dans la documentation officielle ou la référence
  API Python générée.
- **Vérifié empiriquement** : fait observé sur le package local installé.

Ce fichier est un cache technique, pas une source normative EBTA :
`Protocole/` reste l'autorité.

---

## Statut de vérification locale

### Environnement Python local [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : la référence API consultée est celle de NautilusTrader
  `python-api-latest`, alignée sur la série v1.230.0.
- **Vérifié empiriquement** : `nautilus_trader==1.230.0` est installé dans
  `Implementation/adapters/nautilus_env/venv`.
- **Vérifié empiriquement** : l'installation a été créée avec
  `Implementation/adapters/nautilus_env/setup_nautilus_env.ps1`, via `subst`
  sur `N:\venv`. Le mapping `N:` n'est pas persistant entre shells ; le chemin
  réel du venv fonctionne pour l'introspection.
- **Vérifié empiriquement** : `Implementation/adapters/nautilus_env/setup_env.ps1
  -VenvRelativePath "Implementation\adapters\nautilus_env\venv" -SkipInstall`
  réutilise le venv existant, mappe `N:` sur la racine du repo, importe
  `nautilus_trader==1.230.0`, instancie `BacktestEngine()` et expose
  `type(engine.cache).__name__ == "Cache"`.
- **Vérifié empiriquement** : la convention cible de `setup_env.ps1` cree par
  defaut la venv courte sous `N:\Implementation\.venv-nautilus`; le spike
  Phase 2 utilise explicitement le parametre de compatibilite ci-dessus pour ne
  pas dupliquer une venv lourde deja installee.
- **Preuve locale** :
  `Implementation/adapters/nautilus_env/introspect_nautilus_claims.py` et
  `Implementation/adapters/nautilus_env/INTROSPECTION_2026-07-08.txt`.
- **Date** : 2026-07-09

## Noyau & Architecture

### BacktestEngine / BacktestNode / BacktestRunConfig [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : la documentation officielle distingue `BacktestEngine`
  (niveau bas) et `BacktestNode` (orchestration de `BacktestRunConfig`).
- **Vérifié empiriquement** : `BacktestEngine()`, `BacktestEngineConfig`,
  `BacktestRunConfig` et `BacktestNode(configs: list[BacktestRunConfig])`
  existent dans `nautilus_trader==1.230.0`.
- **Vérifié empiriquement** : `BacktestEngine().cache` est une instance de
  `nautilus_trader.cache.cache.Cache`.
- **Source documentaire** :
  https://nautilustrader.io/docs/latest/concepts/backtesting/ et
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/backtest.html
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 103-107,
  339-401, 1406-1416.
- **Date** : 2026-07-08

### BacktestEngine.add_venue() [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : `BacktestEngine.add_venue()` configure le venue de backtest,
  le type d'OMS, le type de compte, les modèles de fill/frais/latence et
  plusieurs options d'exécution.
- **Vérifié empiriquement** : signature observée :
  `add_venue(self, venue, oms_type, account_type, starting_balances,
  base_currency=None, default_leverage=None, leverages=None,
  margin_model=None, modules=None, fill_model=None, fee_model=None,
  latency_model=None, book_type=BookType.L1_MBP, routing=False,
  reject_stop_orders=True, support_gtd_orders=True,
  support_contingent_orders=True, oto_trigger_mode=OtoTriggerMode.PARTIAL,
  use_position_ids=True, use_random_ids=False, use_reduce_only=True,
  use_message_queue=True, use_market_order_acks=False, bar_execution=True,
  bar_adaptive_high_low_ordering=False, trade_execution=True,
  liquidity_consumption=False, queue_position=False, allow_cash_borrowing=False,
  frozen_account=False, price_protection_points=None, settlement_prices=None)`.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/backtest.html
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 143-149.
- **Date** : 2026-07-08

### BacktestEngine.reset() et nettoyage des runs [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : `reset()` remet l'état de trading à zéro mais conserve les
  composants chargés, les données, les instruments et les venues ; la doc
  demande `clear_data()` et/ou `clear_strategies()` si ces éléments changent.
- **Vérifié empiriquement** : `reset()`, `clear_data()` et `clear_strategies()`
  existent sur `BacktestEngine`; `CacheConfig` expose notamment
  `drop_instruments_on_reset=False`.
- **Source documentaire** :
  https://nautilustrader.io/docs/latest/concepts/backtesting/
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 205-214,
  359-363.
- **Date** : 2026-07-08

### Mode streaming BacktestEngine [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : la documentation officielle décrit le chunking manuel
  `add_data(batch); run(streaming=True); clear_data(); end()`.
- **Vérifié empiriquement** : `BacktestEngine.run()` accepte
  `streaming: bool = False`; `add_data()`, `clear_data()` et `end()` existent.
- **Source documentaire** :
  https://nautilustrader.io/docs/latest/concepts/backtesting/
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 174-180.
- **Date** : 2026-07-08

## Données & Marché

### BarDataWrangler / BarType.from_str() / Bar [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : `BarDataWrangler` convertit un `DataFrame` OHLCV en `Bar`
  Nautilus ; le quickstart utilise `BarType.from_str(...)` puis
  `BarDataWrangler(...).process(...)`.
- **Vérifié empiriquement** : `BarDataWrangler`, `BarType.from_str()` et `Bar`
  existent ; `BarDataWrangler.process(data: pd.DataFrame,
  default_volume: float = 1000000.0, ts_init_delta: int = 0)` existe.
- **Source documentaire** :
  https://nautilustrader.io/docs/latest/getting_started/quickstart/,
  https://nautilustrader.io/docs/latest/concepts/data/ et
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/model/data.html
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 528-536.
- **Date** : 2026-07-08

### BarDataWrangler et buffers pandas/NumPy Windows [VÉRIFIÉ EMPIRIQUEMENT]

- **Vérifié empiriquement** : dans le spike Phase 2, un `DataFrame` pandas
  construit directement depuis des listes Python a provoque
  `ValueError: buffer source array is read-only` dans
  `BarDataWrangler.process()`.
- **Vérifié empiriquement** : construire les colonnes OHLCV depuis un
  `np.array(..., dtype="float64").copy()`, puis forcer une copie profonde des
  colonnes du `DataFrame`, permet a `BarDataWrangler.process()` de produire les
  barres Nautilus attendues.
- **Preuve locale** :
  `Implementation/adapters/nautilus_env/run_golden_case.py`.
- **Date** : 2026-07-09

### Mapping OHLCV EBTA vers Bar Nautilus [VÉRIFIÉ EMPIRIQUEMENT]

- **Vérifié empiriquement** : `BarType.from_str("NASDAQ.SIM-1-MINUTE-LAST-EXTERNAL")`
  est accepte par NautilusTrader 1.230.0.
- **Vérifié empiriquement** : `map_ohlcv_to_bars()` produit des `Bar` Nautilus
  depuis des `OhlcvBar` EBTA sans perte visible sur `open`, `close`,
  `price_increment` ou `size_increment` dans le cas NASDAQ/XAUUSD Phase 3.
- **Vérifié empiriquement** : lorsque le timestamp source est interprete comme
  ouverture de barre 1 minute, `ts_init_delta=60_000_000_000` donne
  `ts_init = ts_event + 60_000_000_000`, ce qui place l'initialisation a la
  cloture et evite d'utiliser une barre avant sa disponibilite.
- **Preuve locale** :
  `Implementation/ebta_engine/tests/test_nautilus_instrument_nasdaq.py`.
- **Date** : 2026-07-09

### Convention ts_init des barres [DOCUMENTÉ]

- **Documenté** : pour l'exécution sur barres, `ts_init` doit représenter le
  temps de clôture de la barre ; si le timestamp source est à l'ouverture,
  `BarDataWrangler.process()` doit utiliser `ts_init_delta`.
- **Vérifié empiriquement** : la présence du paramètre `ts_init_delta` est
  confirmée sur `BarDataWrangler.process()` ; la sémantique anti-lookahead
  reste une règle documentaire à tester sur données EBTA.
- **Source documentaire** :
  https://nautilustrader.io/docs/latest/concepts/backtesting/
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 528-536.
- **Date** : 2026-07-08

### Price / Quantity fixed-point [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : la référence API Python expose `Price.from_str()` et
  `Price.from_raw()`, avec précision jusqu'à 16 décimales et contraintes de
  bornes fixed-point.
- **Vérifié empiriquement** : `Price.from_str("3000")`,
  `Price.from_str("20000")` et `Price.from_str("9200000000")` passent.
- **Vérifié empiriquement** : `Price.from_str("17014118346046")` échoue car le
  raw calculé sort de `[-9223372036000000000, 9223372036000000000]`.
- **Vérifié empiriquement** : `Price.from_raw(9223372036000000000, 0)` passe
  avec valeur `9223372036`; `Price.from_raw(9223372037000000000, 0)` échoue.
- **Documenté** : sur Windows, seuls les wheels Python en précision
  standard (entiers 64 bits, 9 décimales) sont publiés — MSVC ne supporte
  pas `__int128`, donc la couche Cython/FFI ne peut pas gérer les entiers
  128 bits du mode haute précision (disponible uniquement sur Linux/macOS).
  Ceci explique et corrobore la borne `i64` observée empiriquement ci-dessus
  sur ce poste Windows 11 (décision D4), plutôt qu'un choix arbitraire de
  précision.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/model/objects.html
  et https://nautilustrader.io/docs/latest/concepts/data/
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 109-117,
  715-725.
- **Date** : 2026-07-08

### Instrument fields margin_init / margin_maint / maker_fee / taker_fee [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : `CurrencyPair`, `Equity` et `FuturesContract` exposent
  `margin_init`, `margin_maint`, `maker_fee` et `taker_fee` dans leurs
  constructeurs.
- **Vérifié empiriquement** : les signatures de `CurrencyPair`, `Equity` et
  `FuturesContract` contiennent ces paramètres.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/model/instruments.html
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 810-816,
  843-849, 876-882.
- **Date** : 2026-07-08

### Cfd / IndexInstrument / Equity pour NASDAQ et XAUUSD [VÉRIFIÉ EMPIRIQUEMENT]

- **Vérifié empiriquement** : `nautilus_trader.model.instruments` expose
  `Cfd`, `IndexInstrument` et `Equity`.
- **Vérifié empiriquement** : `Cfd` accepte `AssetClass.INDEX` et
  `AssetClass.COMMODITY`, `quote_currency`, `price_precision`,
  `size_precision`, `price_increment`, `size_increment`, `margin_init`,
  `margin_maint`, `maker_fee` et `taker_fee`.
- **Vérifié empiriquement** : `IndexInstrument` represente un indice spot non
  directement tradable d'apres sa docstring locale ; Phase 3 retient donc
  `Cfd(..., AssetClass.INDEX, ...)` pour `NASDAQ.SIM`.
- **Vérifié empiriquement** : `build_instrument()` construit `NASDAQ.SIM` comme
  `Cfd` sous-jacent `INDEX` et `XAUUSD.SIM` comme `Cfd` sous-jacent
  `COMMODITY`, avec round-trip des increments `price_increment` et
  `size_increment`.
- **Preuve locale** :
  `Implementation/ebta_engine/adapters/nautilus_mapping.py` et
  `Implementation/ebta_engine/tests/test_nautilus_instrument_nasdaq.py`.
- **Date** : 2026-07-09

### CurrencyPair zero-fee pour cas jouet deterministe [VÉRIFIÉ EMPIRIQUEMENT]

- **Vérifié empiriquement** : `CurrencyPair` accepte `margin_init=0`,
  `margin_maint=0`, `maker_fee=0` et `taker_fee=0` pour l'instrument jouet
  `GOLDEN.SIM`, ce qui permet un cas Phase 2 a cout total nul.
- **Vérifié empiriquement** : les instruments de test preconstruits peuvent
  porter des frais par defaut non nuls ; le cas EBTA deterministe doit donc
  construire explicitement l'instrument au lieu de reutiliser un instrument de
  fournisseur de test si l'attendu manuel exige `total_costs == 0.0`.
- **Preuve locale** :
  `Implementation/adapters/nautilus_env/run_golden_case.py` et
  `Implementation/ebta_engine/tests/fixtures/nautilus_golden_case/expected_result.py`.
- **Date** : 2026-07-09

### ParquetDataCatalog [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : `ParquetDataCatalog` est l'interface Python principale du
  catalogue Parquet, avec backend Rust et fallback PyArrow.
- **Vérifié empiriquement** : `ParquetDataCatalog(path)` existe dans
  `nautilus_trader.persistence.catalog`.
- **Source documentaire** :
  https://nautilustrader.io/docs/latest/concepts/data/ et
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/persistence.html
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 559-569.
- **Date** : 2026-07-08

## Stratégie & Exécution

### Strategy / StrategyConfig [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : `StrategyConfig` est la base des configurations de
  stratégie et expose notamment `strategy_id`, `order_id_tag`, `oms_type`,
  `manage_contingent_orders` et `manage_stop`.
- **Vérifié empiriquement** : `Strategy`, `StrategyConfig` et
  `Strategy.register_indicator_for_bars(self, bar_type, indicator)` existent.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/config.html
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 425-431,
  491-499.
- **Date** : 2026-07-08

### OrderFactory.bracket() / trailing_stop_market() [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : `OrderFactory` fournit les méthodes de construction d'ordres
  dans la surface `common`.
- **Vérifié empiriquement** : `OrderFactory.bracket()` existe, accepte
  notamment `contingency_type`, `entry_*`, `tp_*`, `sl_*` et retourne un
  `OrderList`.
- **Vérifié empiriquement** : `OrderFactory.trailing_stop_market()` existe,
  accepte notamment `trailing_offset`, `activation_price`, `trigger_price`,
  `trigger_type`, `trailing_offset_type` et retourne un
  `TrailingStopMarketOrder`.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/common.html
  et https://nautilustrader.io/docs/latest/concepts/orders/
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 941-946,
  969-977.
- **Date** : 2026-07-08

### Clock.set_time_alert() / set_timer() [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : la référence API Python documente `Clock.set_time_alert`,
  `Clock.set_time_alert_ns`, `Clock.set_timer` et `Clock.set_timer_ns`.
- **Vérifié empiriquement** : les quatre méthodes existent identiquement sur
  `Clock`, `TestClock` et `LiveClock` (`nautilus_trader.common.component`).
  Signatures observées :
  `set_time_alert(self, name, alert_time, callback=None, override=False, allow_past=True)`,
  `set_time_alert_ns(self, name, alert_time_ns, callback=None, allow_past=True)`,
  `set_timer(self, name, interval, start_time=None, stop_time=None, callback=None, allow_past=True, fire_immediately=False)`,
  `set_timer_ns(self, name, interval_ns, start_time_ns, stop_time_ns, callback=None, allow_past=True, fire_immediately=False)`.
- **Attention** : appeler `set_time_alert()`/`set_timer()` sur une `TestClock`
  fraîchement instanciée hors d'un kernel Nautilus provoque un panic Rust
  (`Condition failed: No callbacks provided`, `crates/common/src/ffi/clock.rs`)
  — ces méthodes supposent un composant déjà câblé (ex. dans `Strategy.on_start()`),
  pas un objet `Clock`/`TestClock` isolé construit à la main pour un test unitaire naïf.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/common.html
- **Preuve locale** : introspection complémentaire du 2026-07-08 (session
  d'audit), non incluse dans `introspect_nautilus_claims.py` d'origine —
  `inspect.signature`/`getattr` sur `Clock`, `TestClock`, `LiveClock` via
  le venv `Implementation/adapters/nautilus_env/venv`.
- **Date** : 2026-07-08

### OmsType.HEDGING / AccountType.MARGIN [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : `BacktestEngine.add_venue()` prend `oms_type` et
  `account_type`; la documentation montre des exemples de compte `MARGIN`.
- **Vérifié empiriquement** : `OmsType.HEDGING` vaut `<OmsType.HEDGING: 2>` et
  `AccountType.MARGIN` vaut `<AccountType.MARGIN: 2>`.
- **Source documentaire** :
  https://nautilustrader.io/docs/latest/concepts/backtesting/ et
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/cache.html
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 1000-1018,
  111-112.
- **Date** : 2026-07-08

### FillModel / FeeModel / LatencyModel [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : la référence API Python expose les modèles de fill/frais et
  `LatencyModel`.
- **Vérifié empiriquement** : `FillModel(prob_fill_on_limit=0.5,
  prob_slippage=0.25, random_seed=42)` s'instancie.
- **Vérifié empiriquement** : classes présentes :
  `FillModel`, `BestPriceFillModel`, `ThreeTierFillModel`,
  `SizeAwareFillModel`, `TwoTierFillModel`, `VolumeSensitiveFillModel`,
  `MarketHoursFillModel`, `OneTickSlippageFillModel`,
  `CompetitionAwareFillModel`, `LimitOrderPartialFillModel`,
  `ProbabilisticFillModel`, `MakerTakerFeeModel`, `FixedFeeModel`,
  `PerContractFeeModel`, `LatencyModel`.
- **Vérifié empiriquement** : `MakerTakerFeeModel()` et
  `LatencyModel(base_latency_nanos=1_000_000)` s'instancient ; la propriété
  `base_latency_nanos` vaut `1000000`.
- **Vérifié empiriquement** : `map_cost_model_to_venue()` instancie
  explicitement `FillModel`, `MakerTakerFeeModel`, `LatencyModel` et
  `LeveragedMarginModel`, puis les transmet a `add_venue()` avec
  `OmsType.HEDGING` et `AccountType.MARGIN`. Aucun modele Nautilus par defaut
  implicite n'est utilise dans le test Phase 4.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/backtest.html
  et https://nautilustrader.io/docs/latest/concepts/backtesting/
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 107-109,
  1190-1206, 1262-1275 ; `Implementation/ebta_engine/tests/test_nautilus_phase4_strategy_costs.py`.
- **Date** : 2026-07-09

## Comptabilité & Portefeuille

### MarginModel / StandardMarginModel / LeveragedMarginModel [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : la référence API Python expose `MarginModel`,
  `StandardMarginModel` et `LeveragedMarginModel`; `BacktestEngine.add_venue()`
  expose un paramètre `margin_model`.
- **Vérifié empiriquement** : les classes sont implémentées dans
  `nautilus_trader.accounting.margin_models` et sont aussi accessibles depuis
  `nautilus_trader.backtest.models`.
- **Vérifié empiriquement** : `LeveragedMarginModel()` s'instancie.
- **Vérifié empiriquement** : `StandardMarginModel` calcule la marge initiale
  comme `notional_value * instrument.margin_init`; `LeveragedMarginModel`
  applique `(notional_value / leverage) * instrument.margin_init`.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/backtest.html
  et https://nautechsystems.github.io/nautilus_docs/python-api-latest/config.html
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 110-111,
  1295-1339.
- **Date** : 2026-07-08

## Backtest, Reporting & Observabilité

### Cache.positions_closed() / BacktestResult / get_result() [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : la référence API Python expose `Cache` et les pages
  officielles décrivent les rapports de backtest.
- **Vérifié empiriquement** : `Cache.positions_closed(self, venue=None,
  instrument_id=None, strategy_id=None, account_id=None) -> list` existe.
- **Vérifié empiriquement** : `BacktestResult` expose un constructeur avec
  `summary`, `stats_pnls` et `stats_returns`; `BacktestEngine.get_result()`
  existe.
- **Vérifié empiriquement** : `run_segment()` peut executer un candidat EBTA
  golden-case dans `BacktestEngine`, puis `extract_simulation_result()`
  reconstruit `orders`, `fills`, `positions`, `nav`, `daily_returns` et
  `daily_exposure` sous contrat EBTA. Un cas `NO_MODEL` sans trade retourne une
  NAV plate et des expositions nulles.
- **Limite EBTA** : la reconstruction de `daily_returns`/`daily_exposure`
  depuis ces surfaces reste à tester sur un vrai segment EBTA ; ces rapports
  ne deviennent jamais un verdict méthodologique prêt à consommer.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/cache.html
  et https://nautilustrader.io/docs/latest/concepts/reports/
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 1369-1377,
  1396-1402 ; `Implementation/ebta_engine/tests/test_nautilus_phase5_run_segment.py`.
- **Date** : 2026-07-09

### Extraction de performance réelle : Portfolio / PortfolioAnalyzer / Trader reports [VÉRIFIÉ EMPIRIQUEMENT]

- **Vérifié empiriquement** : `PortfolioAnalyzer`
  (`nautilus_trader.analysis.analyzer`) expose `add_return`, `add_positions`,
  `calculate_statistics`, `returns()`, `portfolio_returns()`,
  `position_returns()`, `realized_pnls()`, `total_pnl()`,
  `total_pnl_percentage()`, `get_performance_stats_pnls()`,
  `get_performance_stats_returns()`,
  `get_performance_stats_returns_vs_benchmark()`,
  `register_statistic()` / `deregister_statistic()`.
- **Vérifié empiriquement** : `Portfolio`
  (`nautilus_trader.portfolio.portfolio`) expose les attributs/méthodes
  `account`, `analyzer`, `equity`, `net_exposure`, `net_exposures`,
  `realized_pnl`, `realized_pnls`, `unrealized_pnl`, `unrealized_pnls`,
  `total_pnl`, `total_pnls`, `is_flat`, `is_completely_flat`, `is_net_long`,
  `is_net_short`, `margins_init`, `margins_maint`, `mark_values`.
- **Vérifié empiriquement** : `Trader`
  (`nautilus_trader.trading.trader`) expose `generate_account_report(venue)`,
  `generate_positions_report()`, `generate_order_fills_report()`,
  `generate_fills_report()`, `generate_orders_report()`.
- **Vérifié empiriquement** : `BacktestResult`
  (`nautilus_trader.backtest.results`, retourné par
  `BacktestEngine.get_result()`) porte `total_orders`, `total_positions`,
  `total_events`, `stats_pnls: dict[str, dict[str, float]]`,
  `stats_returns: dict[str, float]`, `summary: dict[str, str]`.
- **Conséquence pour EBTA (R2)** : la NAV/PnL/coûts réels doivent être lus via
  `engine.portfolio.analyzer` (returns, realized_pnls) et
  `engine.trader.generate_positions_report()` (colonne commissions/realized
  PnL), au lieu de la reconstruction manuelle actuelle de
  `extract_simulation_result()` (buy-and-hold mark-to-market, `total_costs`
  codé à 0). Une série NAV instantanée nécessite d'échantillonner
  `portfolio.equity`/`account` par barre (via un snapshot dans la Strategy)
  ou de dériver la NAV cumulée depuis `analyzer.returns()`.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/analysis.html
  et https://nautilustrader.io/docs/latest/concepts/reports/
- **Preuve locale** : introspection du 2026-07-13 via
  `scripts/introspect_nautilus.py` sur le venv
  `Implementation/adapters/nautilus_env/venv` (PortfolioAnalyzer, Portfolio,
  Trader, BacktestResult).
- **Date** : 2026-07-13

### Recalibration R2 du golden-case EBTA [VÉRIFIÉ EMPIRIQUEMENT]

- **Vérifié empiriquement** : après le refactoring R1/R2, le chemin
  `run_segment()` ne fabrique plus d'ordre sur une source déclarée `DAY` et ne
  la traite plus comme du M1. Le golden-case `GOLDEN.SIM-1-DAY-LAST-EXTERNAL`
  devient donc un cas visible `no_m1_signal` : aucun ordre, aucun fill, aucune
  position, NAV plate à `1000.0`.
- **Vérifié empiriquement** : le nouveau `result_hash` du golden-case
  `run_segment()` recalibré est
  `F057B2EBD53F22A922AB21130A8038D4893DC6AC550D18EA62C2D43ADDDF9A77`.
- **Conséquence pour EBTA (R2)** : `extract_simulation_result()` consomme les
  snapshots NAV M1 de `GenericPayloadStrategy._nav_snapshots` quand ils
  existent ; sinon, une source non-M1 reste explicitement tracée par
  `metadata.no_m1_signal` au lieu de produire un faux trade.
- **Preuve locale** :
  `Implementation/ebta_engine/tests/test_nautilus_phase5_run_segment.py`,
  `Implementation/ebta_engine/tests/test_r2_extraction.py`, et exécution
  directe via le venv `Implementation/adapters/nautilus_env/venv`.
- **Date** : 2026-07-13

### Modules d'indicateurs `averages`/`momentum`/`trend`/`volatility`/`volume` [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : la référence API Python liste des indicateurs par
  catégorie (moyennes mobiles, momentum, tendance, volatilité, volume) sans
  toujours nommer explicitement le module Python correspondant dans les
  pages `concepts/`.
- **Vérifié empiriquement** : les cinq modules s'importent directement et
  contiennent des classes d'indicateurs réelles :
  `nautilus_trader.indicators.averages` (`AdaptiveMovingAverage`,
  `ExponentialMovingAverage`, `HullMovingAverage`, ...),
  `nautilus_trader.indicators.momentum` (`RelativeStrengthIndex`,
  `ChandeMomentumOscillator`, `CommodityChannelIndex`, ...),
  `nautilus_trader.indicators.trend` (`AroonOscillator`, `IchimokuCloud`,
  `DirectionalMovement`, ...), `nautilus_trader.indicators.volatility`
  (`AverageTrueRange`, `BollingerBands`, `DonchianChannel`, ...),
  `nautilus_trader.indicators.volume` (`OnBalanceVolume`,
  `VolumeWeightedAveragePrice`, `KlingerVolumeOscillator`, ...).
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/indicators.html
  et arborescence source `nautilus_trader/indicators/*.pyx` (GitHub,
  `develop`).
- **Preuve locale** : introspection complémentaire du 2026-07-08 (session
  d'audit) — import direct des cinq modules via le venv
  `Implementation/adapters/nautilus_env/venv`.
- **Date** : 2026-07-08

### `StrategyConfig` sous-classée avec `frozen=True` [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : `StrategyConfig` est une base `msgspec.Struct`
  (`NautilusConfig`) ; le pattern `class FooConfig(StrategyConfig,
  frozen=True):` est l'idiome standard utilisé dans les exemples officiels
  de stratégies.
- **Vérifié empiriquement** : une sous-classe
  `class GenericPayloadStrategyConfig(StrategyConfig, frozen=True): payload: dict`
  s'instancie normalement (`GenericPayloadStrategyConfig(payload={...})`) et
  toute tentative de mutation d'attribut après construction lève
  `AttributeError: immutable type: 'GenericPayloadStrategyConfig'`.
- **Vérifié empiriquement** : `GenericPayloadStrategy` s'instancie avec deux
  `GenericPayloadStrategyConfig` differents, issus de candidates differentes,
  tout en conservant exactement la meme classe Python. Seule la config varie.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/config.html
- **Preuve locale** : introspection complémentaire du 2026-07-08 (session
  d'audit) — construction réelle via le venv
  `Implementation/adapters/nautilus_env/venv` ;
  `Implementation/ebta_engine/tests/test_nautilus_phase4_strategy_costs.py`.
- **Date** : 2026-07-09

### FeeModel "par défaut" (sans paramètre requis) pour un venue simulé [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : `nautilus_trader.backtest.models` expose `FeeModel`
  (classe abstraite), `MakerTakerFeeModel`, `FixedFeeModel` et
  `PerContractFeeModel`.
- **Vérifié empiriquement** : seul `MakerTakerFeeModel(config=None)` s'instancie
  sans argument obligatoire — il dérive la commission du `maker_fee`/`taker_fee`
  déjà présents sur l'instrument (`InstrumentConfig.maker_fee`/`taker_fee`,
  `strategies/contracts.py`), et de la valeur notionnelle du trade.
  `FixedFeeModel` et `PerContractFeeModel` lèvent `ValueError` si ni
  `commission` ni `config` ne sont fournis (aucune valeur par défaut
  implicite) — ils exigent donc une décision de calibration humaine
  supplémentaire (montant de commission), contrairement à `MakerTakerFeeModel`.
- **Vérifié empiriquement** : `BacktestEngine.add_venue(fee_model=None)`
  (paramètre optionnel, défaut `None`) a été exercé (Phase 4,
  `test_nautilus_phase4_strategy_costs.py`) en passant toujours un modèle
  explicite (`MakerTakerFeeModel()`), jamais en laissant `fee_model=None` —
  le comportement interne exact de `SimulatedExchange` quand `fee_model=None`
  n'est pas exposé publiquement par l'API Python (pas d'attribut
  `get_exchange()`/`exchanges` accessible sur `BacktestEngine` pour
  l'inspecter directement) et n'a donc **pas** été vérifié empiriquement ici.
- **Conséquence pour EBTA** : le "modèle de frais par défaut" le plus proche
  d'un défaut Nautilus au sens propre (parameterless, pas de valeur à choisir
  soi-même) est `MakerTakerFeeModel()`. Il reste néanmoins **sans effet tant
  que `maker_fee`/`taker_fee` valent `"0"`** sur l'instrument — c'est le cas
  actuel de `_instrument_config()` dans
  `package_builder/nautilus_research_package.py`. Rendre `costs_pass`
  non-trivial exige donc soit de fixer des `maker_fee`/`taker_fee` non nuls
  (nouvelle décision de calibration humaine), soit d'accepter explicitement
  des coûts nuls comme hypothèse MVP tracée.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/backtest.html
- **Preuve locale** : introspection interactive du 2026-07-10 via
  `Implementation/adapters/nautilus_env/venv` (`MakerTakerFeeModel()`,
  `FixedFeeModel.__doc__`, `PerContractFeeModel.__doc__` — `ValueError` si
  `commission`/`config` absents pour ces deux dernières classes).
- **Date** : 2026-07-10

### BacktestNode / BacktestRunConfig — absence de recherche paramétrique native [VÉRIFIÉ EMPIRIQUEMENT]

- **Documenté** : `concepts/backtesting` décrit `BacktestNode` comme
  orchestrant plusieurs `BacktestEngine`, chacun défini par un
  `BacktestRunConfig` : « Multiple configurations can be bundled into a list
  and processed by the node in one run. » Aucune mention de parameter sweep,
  grid search, optimisation automatique ou exécution parallèle/distribuée
  dans cette page.
- **Vérifié empiriquement** : `BacktestNode(configs: list[BacktestRunConfig])`
  et `BacktestRunConfig(venues, data, engine=None, chunk_size=None,
  raise_exception=False, dispose_on_completion=True, start=None, end=None,
  data_clients=None)` — confirmés par introspection de signature.
- **Vérifié empiriquement** : le code source de `BacktestNode.run()` est une
  simple boucle `for config in self._configs.values(): ... self._run(...)`,
  strictement **séquentielle** (docstring : « will synchronously execute the
  list of loaded backtest run configs »). Aucun multiprocessing, aucun thread,
  aucune dépendance à `ray`/`dask`/`joblib` dans les imports de
  `nautilus_trader.backtest.node` ni installée dans le venv.
- **Vérifié empiriquement** : recherche exhaustive de tous les sous-modules de
  `nautilus_trader` (`pkgutil.walk_packages`) pour toute correspondance
  `optim`/`sweep`/`grid`/`search`/`param` — seul résultat :
  `nautilus_trader.examples.strategies.grid_market_maker`, qui est une
  stratégie d'exemple de market-making en grille de prix, **sans rapport**
  avec un grid search de paramètres. Aucun module d'optimisation/exploration
  de variantes n'existe dans `nautilus_trader==1.230.0`.
- **Précision (2026-07-13, suite à une carte marketing du site nautilustrader.io
  « Iterate faster — Run high-throughput backtests across large parameter
  spaces without changing strategy logic », lien « Learn more » vérifié
  pointant exactement vers `concepts/configuration/`)** : cette page,
  entièrement relue, ne décrit que l'architecture des structs de configuration
  typées (defaults, champs optionnels, rejet de champs inconnus à la
  désérialisation) — **aucun mécanisme de génération automatique de variantes
  depuis un espace de paramètres n'y est décrit**. La promesse réelle et
  vérifiée est plus étroite que le slogan : parce que toute la paramétrisation
  d'une stratégie passe par un `StrategyConfig`/`BacktestRunConfig` typé et
  sérialisable, on peut faire varier les paramètres **sans modifier le code de
  la classe `Strategy`** — et `BacktestNode` peut traiter une grande liste de
  ces configs en un seul appel, chaque run bénéficiant du cœur Rust pour la
  vitesse. Mais **construire la liste des configs (le balayage lui-même) reste
  entièrement à la charge de l'appelant** ; il n'y a ni générateur de grille
  ni parallélisme (cf. `BacktestNode.run()` ci-dessus, boucle séquentielle).
- **Conséquence pour EBTA** : Nautilus est un moteur d'exécution
  event-driven (backtest + live) dont l'architecture de configuration sert
  bien la recherche à grande échelle (paramètres découplés du code de
  stratégie, exécution rapide par run), mais qui n'est pas lui-même un outil
  de recherche. Le balayage de grilles de candidats, la génération de
  familles de payloads, et l'orchestration de campagnes massives de runs
  restent entièrement à la charge d'EBTA (`strategies/payload_factory.py`,
  `procedures/search_space.py`, et l'orchestrateur `package_builder/`), pas de
  Nautilus lui-même. Le parallélisme éventuel (multiprocessing/distribution)
  devra être construit côté EBTA au-dessus des runs
  `BacktestNode`/`BacktestEngine` individuels, pas délégué à une capacité
  native de Nautilus qui n'existe pas.
- **Source documentaire** :
  https://nautilustrader.io/docs/latest/concepts/backtesting
- **Preuve locale** : introspection du 2026-07-13 via
  `scripts/introspect_nautilus.py`, lecture directe du code source de
  `BacktestNode.run()`, et recherche exhaustive de sous-modules, sur le venv
  `Implementation/adapters/nautilus_env/venv`.
- **Date** : 2026-07-13

### Souscription multi-timeframe dans une seule Strategy [VÉRIFIÉ EMPIRIQUEMENT]

- **Vérifié empiriquement** : `Strategy.subscribe_bars(bar_type, client_id=None,
  update_catalog=False, params=None)` peut être appelé plusieurs fois avec des
  `BarType` différents (ex. M1, M3, M15, H1, H4, D1) dans `on_start()`.
- **Vérifié empiriquement** (lecture du code source de l'exemple officiel
  `nautilus_trader.examples.strategies.subscribe.SubscribeStrategy`) : une
  **seule** méthode `on_bar(self, bar: Bar)` reçoit les barres de **tous** les
  `BarType` souscrits — il n'existe pas de callback séparé par timeframe. Le
  code de `on_bar()` doit donc discriminer explicitement via `bar.bar_type`
  (comparé aux `BarType` construits pour chaque timeframe) pour router vers
  la bonne logique d'état interne (M1 → détection sweep/engulfing, H1/H4/D1 →
  mise à jour du biais MTF, etc.).
- **Conséquence pour EBTA (R1, stratégie liquidity sweep)** : une seule
  `GenericPayloadStrategy` (ou son successeur) peut souscrire à M1, M3,
  M15/LQ, H1, H4, D1 simultanément et maintenir un état interne par timeframe
  (dernier biais H1/H4/D1 connu, pools de liquidité M15 actifs, fenêtre de
  bougies M1 récentes pour l'engulfing), mis à jour uniquement quand
  `bar.bar_type` correspond.
- **Source documentaire** : aucune page `concepts/` ne détaille explicitement
  ce point de routage multi-timeframe ; confirmé uniquement par lecture directe
  du code source de l'exemple officiel embarqué dans le package installé.
- **Preuve locale** : introspection du 2026-07-13, lecture de
  `nautilus_trader/examples/strategies/subscribe.py` sur le venv
  `Implementation/adapters/nautilus_env/venv`.
- **Date** : 2026-07-13

### Bar.ts_event et conversion en timestamp [VÉRIFIÉ EMPIRIQUEMENT]

- **Vérifié empiriquement** : `Bar` (`nautilus_trader.model.data`) expose
  `ts_event` et `ts_init` comme entiers nanosecondes Unix (attributs publics),
  ainsi que `open`, `high`, `low`, `close`, `volume`, `bar_type`.
- **Vérifié empiriquement** : `nautilus_trader.core.datetime.unix_nanos_to_dt(ts_event)`
  retourne un `pandas.Timestamp` timezone-aware UTC (ex.
  `unix_nanos_to_dt(1577880000000000000)` → `Timestamp('2020-01-01 12:00:00+0000',
  tz='UTC')`).
- **Conséquence pour EBTA (R1)** : dans `Strategy.on_bar(bar)`, la clé de
  correspondance avec une série de décisions précalculée (pandas, indexée par
  timestamp) doit être `unix_nanos_to_dt(bar.ts_event).isoformat()` (ou
  l'objet `Timestamp` lui-même), jamais un recalcul manuel de date depuis
  `ts_event`.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/model/data.html
  et https://nautechsystems.github.io/nautilus_docs/python-api-latest/core.html
- **Preuve locale** : introspection du 2026-07-13 via
  `scripts/introspect_nautilus.py` et appel direct de
  `unix_nanos_to_dt` sur le venv
  `Implementation/adapters/nautilus_env/venv`.
- **Date** : 2026-07-13

## Live & Intégrations

### TradingNode et recherche-vers-live [DOCUMENTÉ]

- **Documenté** : la documentation officielle présente NautilusTrader comme un
  moteur qui réduit l'écart recherche-production ; la référence API expose la
  surface `live`.
- **Vérifié empiriquement** : non inclus dans le script ciblé du 2026-07-08 ;
  sans effet immédiat sur les briques N1-N5.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/ et
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/live.html
- **Date** : 2026-07-08
