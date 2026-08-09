# Plan d'implementation — Ruff CI cible bugs

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Parent | Epic post-audit `BASELINED`, enfants 1-9 `DONE`. |
| Test multi-lot | `SINGLE_CHANTIER` : configuration, corrections et gate partagent le critere Ruff zero. |
| Ruleset | Exactement `F`, `E9`, `B`, `PLE`, `RUF`. |
| Auto-fix | Interdit ; corrections relues individuellement. |

## Audit IA de promotion

- [x] Ruff 0.16.2 verifie depuis PyPI officiel et installe en environnement temporaire.
- [x] Scan vivant limite a `Implementation/ebta_engine` reproduit.
- [x] 25 findings classes par code et fichier.
- [x] Dix invariants de longueur `zip` relus.
- [x] Aucun finding E9/PLE et aucune exemption necessaire.
- [x] Frontieres runtime, Protocole, BACKTRADER et style fermees.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `mainline` |
| Lifecycle | `TRIAGED` apres routage ; non executable avant baseline |
| Type de chantier | `SINGLE` |
| Classification | `IMPLEMENTATION_DETAIL` |
| Scope | Configurer Ruff cible, corriger 25 findings classes dans `ebta_engine`, pinner/executer le gate CI et renforcer le ratchet. |
| Non-goals | `--select ALL`, formatage, imports sorting, auto-fix, notebooks/scripts/Active/adapters env, nouveaux tests metier, Protocole, BACKTRADER, settings GitHub. |
| Source | Epic parent enfant 10/10 ; audit du 2026-08-08 lignes 493-499, 701-705, 756-760 et 892-894. |
| Exit criteria | Config exacte, 25 findings resolus sans ignore, Ruff zero, ratchet/inventaire/suite verts. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `DONE` |
| Date | 2026-08-09 |
| Autorite normative | Aucune. |
| Autorite executable | `pyproject.toml`, workflow et code moteur cible. |
| Impact protocole | Aucun ; Guardian `IMPLEMENTATION_DETAIL`. |

## Carte d'execution IA

| Champ | Contenu |
| --- | --- |
| Objectif | Faire echouer la CI sur une famille ciblee de bugs statiques. |
| Lecture minimale | Plan, audit, 25 contextes, workflow, ratchet et tests associes. |
| Preuve | Ruff avant/apres, Pyrefly, tests cibles, inventaire et suite. |
| Arret | Finding exigeant changement scientifique, ignore large ou scope hors moteur. |

## 1. Role et non-objectifs

Ruff reste un filet technique. Le lot n'effectue ni nettoyage stylistique ni
refonte. Chaque modification correspond a un finding reproduit et conserve
les invariants EBTA existants.

## 2. Contexte obligatoire a lire avant de coder

1. Bootstrap/cockpit, parent et audit source.
2. `pyproject.toml`, workflow et ratchet supply-chain.
3. Sortie Ruff complete et chacun des 25 contextes.
4. Tests couvrant mapping, package, procedures, signaux et hooks.

## 3. Etat des lieux et classification

| Code | Nombre | Decision |
| --- | ---: | --- |
| B905 | 10 | `strict=True` apres verification des invariants de longueurs egales. |
| F401 | 7 | Retirer 6 imports reellement morts ; declarer `DEFAULT_DATA_ROOT` comme re-export public explicite. |
| RUF046 | 3 | Retirer `int()` autour de `round()` sans `ndigits`. |
| B009 | 2 | Acces directs `OrderSide.BUY/SELL`. |
| B007 | 1 | Renommer variable de boucle `_complexity`. |
| RUF059 | 1 | Renommer le composant inutilise `_np`. |
| RUF012 | 1 | Fixture immutable : tuple d'assets. |

## 4. Gates

| Gate | PASS | Sinon |
| --- | --- | --- |
| Config | target py313 et select exact `F,E9,B,PLE,RUF` | FAIL |
| Pin | `ruff==0.16.2` dans installs exactes | FAIL |
| Commande | `python -m ruff check Implementation/ebta_engine` exacte | FAIL |
| Findings | Ruff 0 | FAIL |
| Exceptions | Aucun noqa/ignore/per-file-ignore nouveau | FAIL |
| Regression | Pyrefly, tests/inventaire/suite verts | FAIL |

## 5. Decision d'architecture

La selection vit dans `[tool.ruff.lint]` pour etre partagee entre CI et
developpeurs. Le workflow n'ajoute aucune GitHub Action : Ruff est installe
par pip avec pin exact et lance par `python -m ruff`.

Tous les `zip` concernes portent des series construites ensemble ou precedees
d'une verification d'egalite ; `strict=True` transforme une divergence future
en erreur visible plutot qu'en troncature silencieuse.

## 6. Perimetre de fichiers

Autorises : `pyproject.toml`, workflow CI, ratchet/inventaire/historique, le
plan et ses trois audits, plus exactement les fichiers Ruff suivants :

```text
Implementation/ebta_engine/adapters/nautilus_mapping.py
Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py
Implementation/ebta_engine/package_builder/execution_calibration.py
Implementation/ebta_engine/package_builder/nautilus_research_package.py
Implementation/ebta_engine/procedures/detrending.py
Implementation/ebta_engine/procedures/optimization.py
Implementation/ebta_engine/procedures/search_space.py
Implementation/ebta_engine/strategies/payload_factory.py
Implementation/ebta_engine/strategies/signals/engulfing.py
Implementation/ebta_engine/strategies/signals/entry_signal.py
Implementation/ebta_engine/strategies/signals/liquidity.py
Implementation/ebta_engine/tests/test_git_hooks.py
Implementation/ebta_engine/tests/test_long_data_benchmark.py
Implementation/ebta_engine/tests/test_manifest_hashes.py
Implementation/ebta_engine/tests/test_nautilus_phase2_golden_case.py
Implementation/ebta_engine/tests/test_nautilus_phase5_run_segment.py
Implementation/ebta_engine/validators/verdict_literal_guard.py
```

Interdits : Implementation hors liste, notebooks, Active, adapters env,
Protocole, BACKTRADER, settings GitHub et toute correction non issue du scan.

## 7. Decoupage en phases

1. Configurer Ruff et corriger manuellement les 25 findings.
2. Ajouter pin/commande CI et ratchet exact avec mutation hostile.
3. Executer Ruff, Pyrefly, tests cibles, inventaire, suite et audits.

## 8. Invariants et NO GO

1. Aucun seuil/verdict/calcul scientifique n'est change.
2. `strict=True` seulement quand les longueurs doivent etre egales.
3. Aucun `noqa`, ignore ou exclusion nouvelle.
4. Aucune correction hors des 25 findings reproduits.
5. Le ruleset ne s'elargit pas silencieusement.

NO GO : `--fix`, `--unsafe-fixes`, formatter, `ALL`, suppression de code
utilise, changement d'API ou adaptation scientifique.

## 9. Verification a chaque etape

```powershell
python -m ruff check Implementation/ebta_engine
python -m pyrefly check --python-interpreter-path python --replace-imports-with-any "nautilus_trader.*" Implementation/ebta_engine Implementation/notebooks
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_ci_supply_chain.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
git diff --check
```

## 10. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-08 | Audit consolide. | Ruff cible bugs uniquement, pas `ALL`. |
| 2026-08-09 | `/continue` persistant. | Autorise l'enfant 10 local. |

## 11. Risques

| Risque | Mitigation |
| --- | --- |
| Nettoyage massif | Liste de 25 findings figee et fichiers exacts. |
| `zip` change de comportement | Invariants relus, suite et tests cibles. |
| Nouvelle version change rules | Pin 0.16.2. |
| Faux zero par ignore | Interdiction mecanique/documentee des ignores nouveaux. |
| CI distante non executee | Venv equivalent local ; run distant non revendique. |

## 12. Definition of Done

- [x] Config et pin Ruff exacts.
- [x] 25 findings resolus, aucun ignore ajoute.
- [x] Commande CI et ratchet exacts.
- [x] Ruff et Pyrefly zero erreur.
- [x] Inventaire et suite complete verts.
- [x] Audits sans finding bloquant.
- [x] Aucun fichier interdit touche.

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat | Ruff 0.16.2 : 25 -> 0 finding ; Pyrefly 0 erreur ; 8 tests CI + inventaire verts ; YAML_PASS ; suite canonique 292 tests `OK` (1 skipped). |
| Ecart | Classification F401 raffinee empiriquement : `DEFAULT_DATA_ROOT` est un re-export public requis par le runner Nautilus, conserve via alias explicite sans `noqa`. |
| Suite | Audit global et cloture de l'epic parent. |

## 14. Journal d'audits post-route

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | 25 findings confrontes aux contextes et invariants. | Chaque correction determinee ; aucun ignore requis. |
| 2 | Scope confronte aux 42 findings de tout Implementation. | Limite au moteur conforme a l'audit ; scripts/Active/env hors scope. Convergence. |

## Journal de convergence de l'intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Ruff vivant reproduit. | 25 findings moteur, ecart historique explique. |
| 2 | Classification et frontieres relues. | Corrections atomiques et ruleset cible converges. |
