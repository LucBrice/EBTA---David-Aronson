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
- **Preuve locale** :
  `Implementation/adapters/nautilus_env/introspect_nautilus_claims.py` et
  `Implementation/adapters/nautilus_env/INTROSPECTION_2026-07-08.txt`.
- **Date** : 2026-07-08

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
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/backtest.html
  et https://nautilustrader.io/docs/latest/concepts/backtesting/
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 107-109,
  1190-1206, 1262-1275.
- **Date** : 2026-07-08

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
- **Limite EBTA** : la reconstruction de `daily_returns`/`daily_exposure`
  depuis ces surfaces reste à tester sur un vrai segment EBTA ; ces rapports
  ne deviennent jamais un verdict méthodologique prêt à consommer.
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/cache.html
  et https://nautilustrader.io/docs/latest/concepts/reports/
- **Preuve locale** : `INTROSPECTION_2026-07-08.txt`, lignes 1369-1377,
  1396-1402.
- **Date** : 2026-07-08

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
- **Source documentaire** :
  https://nautechsystems.github.io/nautilus_docs/python-api-latest/config.html
- **Preuve locale** : introspection complémentaire du 2026-07-08 (session
  d'audit) — construction réelle via le venv
  `Implementation/adapters/nautilus_env/venv`.
- **Date** : 2026-07-08

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
