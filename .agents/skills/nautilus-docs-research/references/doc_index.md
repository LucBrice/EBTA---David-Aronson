# Index des pages officielles NautilusTrader

Base URL principale : `https://nautilustrader.io/docs/latest/`.

## Portée de cet index — à lire avant d'utiliser la table ci-dessous

Cette table est un **raccourci pour les questions les plus courantes sur ce
repo**, pas un miroir exhaustif du site. La documentation officielle a six
sections de premier niveau (vérifiées le 2026-07-08 par lecture directe de
la page d'accueil de la doc) :

1. **Getting Started** (`docs/latest/getting_started/`) — installation.
2. **Concepts** (`docs/latest/concepts/`) — architecture, data, execution,
   backtesting, live, modèle de domaine. **C'est ce que couvre la table
   ci-dessous**, organisée selon les six blocs déjà utilisés dans
   `0 - HUMAN START HERE/Implementation_plan_Nautilus.md` (Annexe B).
3. **How-To** (`docs/latest/how_to/`) — recettes orientées tâche (ex.
   charger des données externes, écrire/lancer une stratégie).
4. **Tutorials** (`docs/latest/tutorials/`) — parcours pas-à-pas backtest,
   data, stratégies, Rust.
5. **Integrations** (`docs/latest/integrations/`) — adapters de venues et
   fournisseurs de données externes.
6. **Developer Guide** (`docs/latest/developer_guide/`) — détails internes,
   standards de test, procédure de release.

**Plus deux références API séparées, générées depuis le code, hébergées sur
un autre domaine** (redirection confirmée depuis `nautilustrader.io`) :

- **Python API** : `https://nautechsystems.github.io/nautilus_docs/python-api-latest/`
  — organisée par module (`accounting`, `analysis`, `backtest`, `cache`,
  `common`, `config`, `core`, `data`, `execution`, `indicators`, et
  d'autres). **C'est la source la plus fiable pour une signature exacte**
  (générée depuis le code, donc plus proche du comportement réel que les
  pages `concepts/` en prose) — à préférer aux pages `concepts/` dès qu'une
  signature précise doit être citée dans un plan ou du code, en complément
  (pas en remplacement) de la vérification empirique sur le package
  installé (`scripts/introspect_nautilus.py`).
- **Rust API** : `https://nautilustrader.io/docs/rust-api-latest/` — hors
  scope de ce repo (l'adapter EBTA ne touche que la surface Python).

**Si ta question ne rentre dans aucune ligne de la table ci-dessous, ce
n'est PAS une impasse** — voir "Que faire si l'information n'est pas dans la
table" en bas de ce fichier. Ne jamais conclure qu'une information n'existe
pas dans la doc Nautilus simplement parce qu'elle n'est pas dans cette table
: cette table couvre ce qui a déjà servi pour ce repo, pas tout le site.

## Noyau & Architecture

| Page | URL (suffixe après la base) | Utile pour |
|---|---|---|
| Overview | `concepts/overview` | Vue d'ensemble avant tout le reste |
| Architecture | `concepts/architecture` | `NautilusKernel`, `DataEngine`, `ExecutionEngine`, `RiskEngine` |
| Configuration | `concepts/configuration` | Objets `Config` typés, `StrategyConfig`, `BacktestEngineConfig` |
| Rust | `concepts/rust` | Cœur Rust, extensions Cython |
| DST (déterminisme) | `concepts/dst` | Garanties de rejeu — **exclut explicitement le code Python/stratégies**, cf. plan Nautilus §2.1 |
| Event Sourcing | `concepts/event_sourcing` | Traçabilité causale interne (alpha) |
| Message Bus | `concepts/message_bus` | Pub/sub inter-composants |
| Cache | `concepts/cache` | `cache.positions_closed()`, état en mémoire post-run |
| Logging | `concepts/logging` | Logging interne — jamais une source de vérité EBTA |

## Données & Marché

| Page | URL | Utile pour |
|---|---|---|
| Data | `concepts/data` | `DataLoader`, `DataWrangler`, ingestion CSV → objets Nautilus |
| Custom Data | `concepts/custom_data` | Données non-marché (hors scope EBTA actuel) |
| Order Book | `concepts/order_book` | Microstructure L1/L2/L3 (hors scope, données = OHLCV) |
| Instruments | `concepts/instruments` | `CurrencyPair`, `Equity`, `margin_init`/`margin_maint`/`maker_fee`/`taker_fee` |
| Value Types | `concepts/value_types` | Précision fixed-point `Price`/`Quantity`/`Money` |

## Stratégie & Exécution

| Page | URL | Utile pour |
|---|---|---|
| Strategies | `concepts/strategies` | `Strategy`, `StrategyConfig`, `on_bar`, `Clock`, indicateurs |
| Actors | `concepts/actors` | Classe de base sans ordres (monitoring/agrégation) |
| Orders | `concepts/orders` | Types d'ordres (bracket, trailing-stop, TIF) |
| Execution | `concepts/execution` | `ExecutionEngine`, OMS Netting/Hedging |
| Positions | `concepts/positions` | Cycle de vie position, PnL réalisé/latent |

## Comptabilité & Portefeuille

| Page | URL | Utile pour |
|---|---|---|
| Accounting | `concepts/accounting` | Types de compte Cash/Margin/Betting, `MarginModel` |
| Portfolio | `concepts/portfolio` | Vue multi-stratégies (hors scope recherche EBTA actuelle) |

## Backtest, Reporting & Observabilité

| Page | URL | Utile pour |
|---|---|---|
| Backtesting | `concepts/backtesting` | `BacktestEngine`, `BacktestNode`, `engine.reset()`, mode `streaming` |
| Reports | `concepts/reports` | `ReportProvider`, DataFrames ordres/fills/positions |
| Visualization | `concepts/visualization` | Tearsheets — jamais une source de verdict EBTA |
| Installation | `getting_started/installation` | Contraintes plateforme/Python |

## Live & Intégrations

| Page | URL | Utile pour |
|---|---|---|
| Live Trading | `concepts/live` | `TradingNode` — hors scope tant que `DEPLOYMENT_CERTIFIED` (G13) n'est pas atteint |
| Integrations | `integrations/` (index) | Adapters venues externes (Binance, IB, Databento...) |

## How-To, Tutorials, Developer Guide (hors des six blocs Concepts)

| Section | URL | Statut de vérification | Utile pour |
|---|---|---|---|
| How-To — Loading External Data | `how_to/` (index) | **Vérifiée le 2026-07-08** (titre et contenu confirmés par fetch direct) | Charger des CSV dans un catalogue Parquet — directement pertinent pour la Brique N1 (`map_ohlcv_to_bars()`) |
| How-To — Write/Run a Strategy (Rust) | `how_to/` (index) | Vérifiée le 2026-07-08 | Existe mais orienté Rust, moins pertinent pour `GenericPayloadStrategy` (Python) |
| Tutorials | `tutorials/` | **Non vérifiée individuellement** — URL déduite par le pattern `docs/latest/<section>/` confirmé sur deux autres sections | Parcours pas-à-pas — à vérifier par fetch avant de citer un contenu précis |
| Developer Guide | `developer_guide/` | **Non vérifiée individuellement**, même réserve | Standards internes, tests, release — rarement pertinent pour l'usage adapter EBTA |

## Que faire si l'information n'est pas dans la table ci-dessus

Ne jamais s'arrêter à "ce n'est pas dans la table donc ça n'existe pas". Dans
l'ordre :

1. **Vérifier la référence API Python** (`python-api-latest`, voir plus
   haut) — organisée par nom de module Python, souvent le moyen le plus
   rapide de trouver une classe précise sans deviner sa page `concepts/`.
2. **Consulter `how_to/`** — beaucoup de questions opérationnelles concrètes
   (charger des données, écrire une stratégie, lancer un backtest) y sont
   traitées plutôt que dans `concepts/`.
3. **Faire une recherche web réelle**, pas une URL devinée par motif —
   scoper la recherche à `site:nautilustrader.io` ou
   `site:nautechsystems.github.io/nautilus_docs`. **Ne jamais construire une
   URL par déduction de pattern sans la vérifier par un fetch direct** :
   une tentative de deviner `docs/latest/api_reference/` par analogie a
   produit une 404 lors de la construction de cet index — le motif
   `docs/latest/<section>/` n'est pas garanti pour toutes les sections
   (la référence API Python vit sur un domaine et un chemin différents).
4. Si rien n'est trouvé après ces trois étapes, le dire explicitement à
   l'utilisateur/l'IA appelante plutôt que de fabriquer une réponse — c'est
   le même principe que pour une signature non vérifiable empiriquement
   (SKILL.md, étape 4).

## Comment choisir la page (cas courant, dans la table)

1. Identifier le thème de la question (ex. "comment se comporte le fill
   probabiliste ?" → Stratégie & Exécution → `concepts/execution`, puis
   `concepts/orders` si la question porte sur un type d'ordre précis).
2. Récupérer directement l'URL correspondante (outil de fetch web disponible
   dans l'agent courant).
3. Si la réponse touche une signature ou un comportement précis destiné à
   être écrit dans du code ou un document, ne jamais s'arrêter à la doc :
   croiser avec la référence API Python, puis passer à la vérification
   empirique (étape 2 de `SKILL.md`).
