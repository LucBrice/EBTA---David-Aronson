# Exemple reel : balayage complet de Implementation/ebta_engine/

Cet exemple documente un balayage reel (pas invente), execute apres
l'installation de Pyrefly dans `Implementation/adapters/nautilus_env/venv`.
Il montre la forme attendue du rapport final et illustre les deux
categories de signal sur des cas concrets, y compris les impasses
rencontrees en cours de route — les corriger fait partie du travail.

## Commande de depart

```
Implementation/adapters/nautilus_env/venv/Scripts/python.exe -m pyrefly check Implementation/ebta_engine --output-format min-text
```

Resultat initial : **48 erreurs** reparties sur une quinzaine de fichiers.

## Tri (extrait representatif)

| Fichier:ligne | Message Pyrefly (resume) | Classification | Raison |
| --- | --- | --- | --- |
| `engulfing.py:25` | `no-matching-overload` sur `np.maximum(Series, Series)` | FAUX POSITIF D'OUTILLAGE | pandas implemente `__array_ufunc__`, les stubs numpy ne le declarent pas pour des `Series` |
| `entry_signal.py:101` | `bad-argument-type` sur des `np.ndarray` non parametres passes entre deux fonctions internes | FAUX POSITIF D'OUTILLAGE | chaque annotation `np.ndarray` nue synthetise une instanciation generique distincte pour Pyrefly ; elles ne s'unifient pas entre elles alors que le code est correct a l'execution |
| `wrc.py:239` | `no-matching-overload` sur `sorted(dict, key=dict.get)` | FAUX POSITIF D'OUTILLAGE | `.get` sans defaut elargit le type de retour a `float \| None`, alors que chaque cle existe garantie (on trie les cles du dict lui-meme) |
| **`governance/bias_gate.py:20`** | `candidate_registry: list[dict] \| dict \| None` passe tel quel a `check_registry_completeness(registry_events: list[dict])` | **VRAI BUG** | si un futur appelant suit la signature et passe un `dict` seul (autorise par le type), `for event in enumerate(dict)` itere sur les cles (des `str`), et `event.get(field)` leve `AttributeError` — dans la couche G-BIAS, la plus sensible du repo |
| **`strategies/registry.py:13`** | Appel de `strategy_cls(dict, warmup_bar_count=...)` type-checke contre `object.__init__` | **VRAI BUG** | le `Protocol IncrementalSignalStrategy` ne declarait pas de constructeur, alors que `nautilus_strategy_bridge.py` en depend structurellement pour toute strategie enregistree |
| **`strategies/signals/sessions.py:8`** | `dict.get("tz")` type inferre `str \| float` | **VRAI BUG** | `_SESSION_CONFIG` melangeait des valeurs `str` et `float` dans un seul dict litteral sans `TypedDict` — risque reel de confusion de type si le dict evolue |

Pour les deux vrais bugs de gouvernance/registre : recherche des appelants
reels (`Grep`) a confirme qu'aucun appelant actuel n'emprunte le chemin
dangereux aujourd'hui — le risque etait latent, pas actif. Ca ne change pas
la classification (VRAI BUG reste VRAI BUG), seulement l'urgence relative
signalee dans le rapport final.

## Correctifs types (par cause racine, pas par ligne)

- `np.maximum(a, b)` / `np.minimum(a, b)` sur des `Series` -> remplaces par
  `pd.concat([a, b], axis=1).max(axis=1)` / `.min(axis=1)` : reste dans
  l'API pandas native, aucune ambiguite de stub.
- `np.ndarray` nu en parametre interne -> alias `Any` explicite quand la
  forme numpy exacte n'a pas de valeur pour les appelants (ces helpers sont
  prives, `_sweep_indices`/`_nearest_engulf`), plutot que de se battre avec
  les generiques numpy.
- `sorted(dict, key=dict.get)` -> `sorted(dict, key=lambda k: dict[k])` :
  l'indexation `[]` ne peut pas retourner `None`, contrairement a `.get()`.
- `candidate_registry: list[dict] | dict | None` -> resserre a
  `list[dict] | None` : retire une forme que la moitie du pipeline
  n'a jamais reellement supportee.
- `Protocol` sans constructeur -> ajoute la signature `__init__` exacte
  partagee par toutes les classes deja enregistrees (verifie par lecture
  directe de `payload_e.py`/`payload_f.py`/`payload_ghi.py` avant d'ecrire
  la signature, pas devinee).
- Dict heterogene `str`/`float` -> `TypedDict` dedie.

## Impasse rencontree et comment elle a ete resolue

Une premiere tentative de typer les `np.ndarray` avec
`npt.NDArray[np.float64]` a fait baisser les erreurs de 20 a 7, mais 7
diagnostics ont persiste avec une signature de generique legerement
differente (`numpy.ndarray@2078:7-14` sans le detail du dtype). Plutot que
de s'acharner sur le typage numpy precis, le alias a ete simplifie en
`npt.NDArray[Any]` puis, apres un nouvel echec du meme ordre, en `Any` tout
court pour ces deux helpers prives. Lecon : quand une tentative de typage
plus precis echoue deux fois de suite sur le meme symptome, c'est un signal
pour reculer d'un cran de precision plutot que d'insister — la valeur de
`Any` ici (documenter "c'est un tableau numpy interne, sa forme exacte
n'importe a personne d'exterieur") l'emporte sur la valeur d'un typage
numpy exact que l'outil ne sait pas verifier correctement de toute facon.

## Revalidation finale

```
Implementation/adapters/nautilus_env/venv/Scripts/python.exe -m pyrefly check Implementation/ebta_engine --output-format min-text
# -> INFO 0 errors (13 warnings not shown)

python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation
# -> Ran 139 tests ... OK

python Implementation/examples/minimal_pilot_pipeline/build_research_package.py
# -> {"status": "PASS"}
```

Les 13 avertissements restants (severite inferieure a erreur) n'ont pas ete
traites dans ce passage — a signaler dans le rapport plutot que passes sous
silence, mais ils ne bloquent pas la tache tant qu'ils restent des
avertissements et non des erreurs.

## Forme du rapport final rendu a l'utilisateur

Un tableau { critere / classification / preuve } n'est pas necessaire ici
(ce n'est pas le format de ce skill) — le rapport attendu est une liste par
fichier : faux positifs (avec la raison de la classification) puis vrais
bugs (avec le scenario de defaillance concret que chacun permettait), suivi
de la commande de revalidation et de son resultat.
