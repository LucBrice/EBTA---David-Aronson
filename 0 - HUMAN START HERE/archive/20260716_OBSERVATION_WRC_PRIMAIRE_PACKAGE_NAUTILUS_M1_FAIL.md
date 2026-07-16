# Observation — le WRC primaire reel du package Nautilus M1 est `FAIL`, la cloture de G5 reste bloquee

> Note d'intake, pas un plan. Deposee ici pour audit et structuration, a
> partir de la section 13 ("Cloture") de
> `.ai/backlog/fixes/PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE.md` (statut
> `ACTIVE`, non cloture au 2026-07-16), qui identifie explicitement ce point
> comme **priorite immediate** pour un chantier separe :
>
> > "Priorite immediate : ouvrir un chantier separe sur le WRC primaire reel
> > du package Nautilus M1 / incoherence historique 'R4 package PASS' vs
> > build courant `FAIL` (...). Ne pas forcer `wrc_status = PASS`, ne pas
> > calibrer un seuil silencieusement, ne pas modifier `Protocole/` dans ce
> > chantier G5."

---

## 0. Pourquoi ce document existe

Le chantier `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE` avait un perimetre
initial etroit et deja livre (Phase 1 : reutiliser
`procedure_reports["robustness"]["status"]` dans `gates.json` ; Phase 2 :
preuve de non-regression). Mais en cours d'execution, l'humain a demande de
corriger un blocage annexe (timeout du build Nautilus reel), ce qui a fait
sortir le chantier de son perimetre de fichiers autorise initial (section 5
du plan) et a revele un resultat qu'aucune des deux phases ne pouvait
anticiper : **le WRC primaire reel du package de production Nautilus M1 est
`FAIL`**, alors que le meme perimetre logique avait ete cloture `PASS` cinq
jours plus tot par
`.ai/archive/20260715_PLAN_R4_DONNEES_INTRADAY_REELLES_PACKAGE_PRODUCTION.md`
(commit `3bcfe35`, `closure_reason` : *"R4 complete: M1 real Nautilus package
PASS, GHI bias_filter fixed, total_orders > 0, bug-hunter and conformance
audit PASS."*).

Consequence directe : `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE` ne peut pas
etre ferme via `/close` — son propre critere de verification production
("package Nautilus PASS avant/apres") n'est pas satisfait, et section 13
documente explicitement ce blocage sans le resoudre. C'est le "probleme
encore ouvert" que cette note structure pour permettre un `/start` ulterieur
sur un chantier dedie, distinct de G5.

---

## 1. Constat (verifie dans le code et par execution le 2026-07-16)

### 1.1 Le resultat WRC actuel

Build reel via le venv Nautilus dedie
(`.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m
ebta_engine.package_builder.nautilus_research_package`) : termine (le
timeout initial est resolu), mais retourne `{'status': 'FAIL'}`.

`Implementation/research_packages/nautilus_mvp/reports/wrc.json` (non
versionne, `Implementation/.gitignore` l.3 — reproductible localement) :

```json
{
  "verdict": "FAIL",
  "wrc_pvalue": 0.39492101579684064,
  "exceedance_count": 1974,
  "replications": 5000,
  "observed_statistic": 0.00021329644810180043,
  "power_diagnostics": {
    "candidate_count": 16,
    "negative_mean_candidate_count": 11,
    "negative_mean_candidate_fraction": 0.6875
  }
}
```

`gates.json::gate_failures` en decoule : `"G4 INCONCLUSIVE: missing
['wrc_status']"`, avec `incubation_gate.status = FAIL` et
`economic.global_status = FAIL` en cascade (comportement attendu et deja
correct de `validators/package_validator.py` et `procedures/lifecycle.py`,
corriges par les deux chantiers `DONE` precedents — ce n'est pas ce que
cette note remet en cause).

### 1.2 L'incoherence historique avec R4 (`DONE`, 2026-07-15)

`.ai/checkpoint.json::workstreams[PLAN_R4_DONNEES_INTRADAY_REELLES_PACKAGE_PRODUCTION].closure_reason`
affirme *"M1 real Nautilus package PASS"* au commit `3bcfe35` (2026-07-15).
Le meme perimetre logique (package Nautilus M1 de production) est
aujourd'hui `FAIL` sur le WRC primaire, sans qu'aucune decision humaine
n'ait modifie SOP 02, le seuil `alpha`, ou la famille de candidats
declaree.

Le sujet se decompose en **deux questions distinctes et compatibles** (elles
peuvent etre vraies toutes les deux — ce ne sont PAS des alternatives
exclusives ; l'audit `/evaluate` du 2026-07-16 a corrige leur formulation
initiale en XOR) :

- **Q1 (technique) — le `PASS` de R4 reposait-il sur une NAV degenerescente ?
  Mecanisme deja CONFIRME par archeologie git, plus une simple hypothese.**
  La serie de rendements qui alimente le WRC ne provient PAS de
  `nautilus_mapping.py::_money_float()` (cette fonction n'alimente que les
  couts/fills via `_row_float`/`_extract_costs`). La vraie chaine NAV -> WRC
  est :

  ```text
  nautilus_mapping.py:317   daily_returns = _returns_from_nav(nav)
  nautilus_mapping.py:304   nav <- _extract_nav_series(strategy)  # lit strategy._nav_snapshots
  nautilus_strategy_bridge.py:94-97  _record_nav_snapshot():
        equity = _call_float(self.portfolio, "equity", self._venue)   # <-- fonction reelle
  ```

  C'est `nautilus_strategy_bridge.py::_call_float()` (et non `_money_float`)
  qui recoit le mapping `{Currency: Money}` renvoye par `portfolio.equity()`.
  Verification directe de l'etat du code au commit de cloture R4 `3bcfe35` :

  ```python
  # git show 3bcfe35:...nautilus_strategy_bridge.py  (fonction _call_float)
  def _call_float(obj, name, argument):
      value = getattr(obj, name, None)
      try:
          result = value(argument) if callable(value) else value
      except Exception:
          return 0.0
      try:
          return float(str(result).split()[0])   # PAS de gestion du dict {Currency: Money}
      except Exception:
          return 0.0
  ```

  Sur un mapping `{Currency: Money}`, `str(result).split()[0]` vaut
  `"{<Currency:"`, `float()` echoue -> **`0.0` a chaque barre M1**. Donc au
  commit `3bcfe35`, `_nav_snapshots` etait rempli de `(ts, 0.0, exposure)`,
  d'ou `nav = [0.0, 0.0, ...]` et, via `_returns_from_nav()`
  (`nautilus_mapping.py:443`), `daily_returns` **tous nuls**. Le WRC de R4 a
  donc tres probablement tourne sur des series de rendements degenerescentes,
  et non sur des rendements reels — un `PASS` calcule ainsi n'est pas la
  preuve d'une edge. Le diff non commite du 2026-07-16 corrige exactement ce
  point dans `_call_float` (meme gestion `isinstance(result, dict) and
  len(result) == 1`), et introduit en parallele le meme correctif dans
  `_money_float` (chemin couts/fills) ainsi que `_precomputed_decisions()`
  (nouveau chemin de generation d'ordres, ~70 lignes) — a auditer, mais ces
  deux derniers ne sont pas la chaine NAV -> WRC. Aucun test de regression
  n'asserta une NAV non nulle avant ce diff : le test
  `test_dedicated_venv_m1_segment_records_real_nav_without_false_no_m1`
  (`test_nautilus_phase5_run_segment.py:286-288`, qui verifie
  `min(nav) < max(nav)` et `sum(daily_returns != 0) > 0`) fait justement
  partie du diff non commite, il n'existait pas a `3bcfe35`.

- **Q2 (gouvernance / recherche) — une fois le mecanisme Q1 corrige, la
  famille de candidats a-t-elle une edge, ou le `FAIL` est-il legitime ?**
  Sur l'etat corrige actuel, `wrc.json` montre des rendements desormais reels
  (statistiques par candidat non nulles, `observed_statistic = 0.000213`) et
  `power_diagnostics.negative_mean_candidate_fraction = 0.6875` (11/16
  candidats a moyenne negative). Le `FAIL` courant est donc **un resultat EBTA
  honnete** : la famille ne bat pas la correction multi-tests WRC sur ce
  segment M1. Un WRC `FAIL` n'est pas un bug — c'est exactement la protection
  contre le data snooping que SOP 02 doit produire. Ce n'est PAS a "reparer" :
  c'est a documenter comme verdict de recherche.

Synthese : Q1 est deja essentiellement resolue (le `PASS` de R4 etait un
artefact de NAV nulle, mecanisme confirme au commit `3bcfe35`) ET Q2 l'est
aussi sur l'etat courant (le `FAIL` reel est legitime). Les deux sont vrais
simultanement. Ce qui reste a l'humain n'est donc pas de "trancher A ou B",
mais (a) valider cette lecture et (b) decider quoi faire du `PASS` R4
retrospectivement invalide et du `FAIL` legitime courant (voir section 3).

### 1.3 Le perimetre de fichiers du chantier G5 a deja deborde

Le git status courant montre des modifications non commitees hors du
perimetre de fichiers autorise par
`PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE.md` section 5 (qui n'autorisait
que `build_research_package.py`, `test_nautilus_research_package.py`, et
`HISTORIQUE DES VERSIONS EBTA ENGINE.md`) :

```text
Implementation/ebta_engine/adapters/nautilus_mapping.py            (hors perimetre G5 initial)
Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py    (hors perimetre G5 initial)
Implementation/ebta_engine/package_builder/nautilus_research_package.py  (hors perimetre G5 initial)
Implementation/ebta_engine/tests/test_nautilus_phase5_run_segment.py    (hors perimetre G5 initial)
```

A noter en plus : le diff de `build_research_package.py:378` (dans le
perimetre G5, mais changement de nature statistique) ajoute
`run_secondary=statistical_plan.get("wrc_run_secondary", True)`, et
`wrc.json` du package courant montre `mcpm / romano_wolf / spa: NOT_RUN`.
Le WRC **primaire** conserve bien ses 5000 replications (verifie), mais les
tests secondaires WRC ont ete rendus desactivables et sont desactives pour
ce package M1 long. Ce n'est pas la cause du `FAIL` primaire, mais c'est un
changement du comportement statistique a garder en vue lors de l'audit Q1.

Le plan G5 documente lui-meme cet ecart en section 13 ("Ecart d'execution
assume apres demande utilisateur 'Corrige dans ce cas'"), donc ce n'est pas
une derive silencieuse — mais ces fichiers restent des **modifications non
commitees** au moment de cette note. Tant qu'elles ne sont ni commitees ni
tranchees (conservees ou revertees), le chantier propose en section 4 ne
peut pas etre execute sur un etat stable.

---

## 2. Ce que cette note ne fait PAS

- Ne force aucun `wrc_status` ni `verdict` a `PASS` — interdit explicitement
  par la section 13 du plan G5 dont cette note assure la suite.
- Ne propose aucune modification de `Protocole/`, de SOP 02, du seuil
  `alpha`, ou de la logique `procedures/wrc.py` — ces elements restent geles
  et presumes corrects tant que l'audit propose (section 4) n'a pas conclu
  autrement.
- Ne substitue pas sa lecture technique (Q1 / Q2 de la section 1.2) a la
  validation humaine — le mecanisme d'artefact est confirme dans le code,
  mais la decision de gouvernance qui en decoule (section 3) reste humaine.
- Ne propose pas de commiter en l'etat les fichiers hors perimetre listes
  en section 1.3 — leur sort (commit assume, ou revert vers le perimetre
  initial de G5) est une decision humaine prealable au chantier propose,
  pas une consequence automatique.
- Ne rouvre pas et ne modifie pas
  `.ai/archive/20260715_PLAN_R4_DONNEES_INTRADAY_REELLES_PACKAGE_PRODUCTION.md`
  ni son `closure_reason` dans `.ai/checkpoint.json` — un chantier archive
  `DONE` n'est pas edite retroactivement ; une correction eventuelle de
  narration se ferait par une nouvelle entree tracee, jamais par reecriture
  de l'historique.
- Ne clot pas `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE` — ce plan reste
  `ACTIVE`/non cloture jusqu'a ce qu'une decision humaine explicite le
  permette (voir section 5).

---

## 3. Decision humaine — TRANCHEE le 2026-07-16

La partie technique (section 1.2) etait deja tranchee par le code : Q1 (le
`PASS` R4 reposait sur une NAV nulle, `_call_float` sans gestion dict au
commit `3bcfe35`) et Q2 (le `FAIL` courant est un verdict WRC honnete sur
rendements reels) sont **toutes deux confirmees**. Les deux volets de
gouvernance restants ont ete tranches explicitement par l'utilisateur
(voir section 5, entree 2026-07-16) :

1. **Vis-a-vis de R4 (archive `DONE`)** : **decision = ajouter une entree
   tracee** actant que son `PASS` reposait sur une NAV degenerescente. Le
   `closure_reason` archive de `PLAN_R4_DONNEES_INTRADAY_REELLES_PACKAGE_PRODUCTION`
   n'est PAS reecrit — la correction se fait par une nouvelle entree dans
   `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` et, si le format
   du checkpoint le permet, une entree separee referencant ce chantier
   (jamais une modification du `closure_reason` existant).
2. **Vis-a-vis du `FAIL` courant** : **decision = documenter et clore**. Le
   `FAIL` est accepte comme verdict de recherche legitime (la famille M1
   courante n'a pas d'edge demontrable sur ce segment). Pas de chantier de
   recherche distinct sur la famille de candidats a ce stade — conforme au
   principe EBTA "ne jamais ajuster un parametre pour obtenir `PASS`".

Consequence sur l'ampleur du chantier : **minimal** — documentation (Phase 1
consolidee + Phase 2bis) + reconciliation de G5 (Phase 3). Pas de Phase 2
"chantier de recherche sur la famille" a ouvrir dans l'immediat.

---

## 4. Suite proposee (structure indicative pour un futur chantier `fix` ou `annexe`)

A rediger en plan complet (`Track`, `Lifecycle`, `Scope`, `Non-goals`,
`Source`, `Exit criteria`) au moment du `/start`. La decision de la section 3
etant tranchee (documenter, ne pas rouvrir de recherche sur la famille), le
chantier ci-dessous est **de portee minimale** : verification/preuve +
documentation + reconciliation de G5. Aucune Phase "recherche sur la
famille de candidats" n'est incluse — elle a ete explicitement ecartee.
Squelette propose :

1. **Phase 0 — Stabiliser l'etat du depot.** Trancher le sort des fichiers
   hors perimetre listes en section 1.3 (commit explicite documente, ou
   revert vers le dernier etat connu-bon) avant toute investigation, pour
   ne pas enqueter sur un etat mouvant.
2. **Phase 1 — Consolider le constat d'artefact (Q1, deja largement etabli).**
   Le mecanisme est confirme (section 1.2 : `_call_float` sans gestion dict
   au commit `3bcfe35` -> NAV nulle -> `daily_returns` nuls). Ce qui reste a
   figer formellement : reconstruire le package Nautilus M1 **depuis l'etat
   `3bcfe35`** (via le venv Nautilus) et observer la NAV/les `daily_returns`
   effectivement produits pour prouver mecaniquement le `0.0`. La commande de
   rebuild doit etre figee dans le plan pour rendre l'audit reproductible
   (le package `research_packages/` etant git-ignore, il n'existe aucun
   artefact sauvegarde a comparer — seul le rebuild fait foi). Verifier au
   passage *ce qu'un WRC produit sur une serie de rendements identiquement
   nulle* — c'est la mecanique exacte par laquelle R4 a pu afficher `PASS`.
3. **Phase 2 — Reconstruire une preuve R4 honnete sur l'etat corrige.**
   Reconstruire le package Nautilus M1 de production sur l'etat corrige,
   verifier si `wrc_status` reste `FAIL` (etat courant observe) ou redevient
   `PASS` avec des rendements desormais reels. Documenter le resultat quel
   qu'il soit — ne jamais ajuster un parametre pour obtenir `PASS`. Ajouter
   un critere de sortie qui manquait a R4 : **`total_orders > 0` est
   necessaire mais insuffisant** (des ordres peuvent etre passes pendant que
   `equity()` renvoie 0.0) ; exiger en plus une NAV qui varie
   (`min(nav) < max(nav)` et `sum(daily_returns != 0) > 0`), critere que le
   test `test_dedicated_venv_m1_segment_records_real_nav_without_false_no_m1`
   applique deja.
4. **Phase 2bis — Documenter le verdict de recherche (Q2).** Ajouter une
   entree `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` actant que
   la famille de candidats M1 courante ne passe pas WRC sur ce segment
   (resultat honnete, pas un bug), et que le `PASS` de `PLAN_R4` reposait sur
   une NAV degenerescente — via une nouvelle entree tracee, jamais par
   reecriture de l'archive R4.
5. **Phase 3 — Reconciler `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE`.**
   Une fois l'etat du package de production stabilise et documente,
   revenir sur ce plan pour permettre son `/close` (soit parce que le
   package redevient `PASS` legitimement, soit parce qu'une decision
   humaine explicite accepte de clore G5 independamment du statut WRC
   primaire, puisque G5 et G4 sont des gates distincts).

Non-goals a reprendre tels quels dans le futur plan structure : pas de
modification de `Protocole/`, pas de calibration silencieuse de seuil, pas
de nouvelle regle DN, pas d'extension a la couverture de catalogue
preregistre (DN-030) ni au realisme des scenarios de robustesse (R6), et
**pas de chantier de recherche sur la famille de candidats M1** (decision
section 3 : le `FAIL` est documente et clos, pas investigue plus avant) —
ces sujets restent distincts et deja identifies par ailleurs.

---

## 5. Journal des decisions humaines (autorisations)

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-16 | Demande utilisateur explicite de generer un plan/observation dans `0 - HUMAN START HERE/` pour traiter le probleme encore ouvert documente par la section 13 de `PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE.md`. | Autorise la redaction de cette note d'intake ; n'autorise pas encore son routage via `/start`, ni la decision de gouvernance de la section 3, qui reste une decision humaine explicite a venir. |
| 2026-07-16 | Passage `code-architecture-evaluator` (`/evaluate`), passe 1. Corrections appliquees : (1) le mecanisme NAV -> WRC citait a tort `nautilus_mapping.py::_money_float()` ; verifie dans le code que la vraie chaine est `nautilus_strategy_bridge.py::_record_nav_snapshot -> _call_float` (l.95, l.167), `_money_float` n'alimentant que couts/fills. (2) Hypotheses A/B requalifiees de choix exclusif (XOR) en questions Q1/Q2 compatibles. (3) Q1 confirmee par archeologie git (`_call_float` sans gestion dict au commit `3bcfe35` -> equity 0.0 -> `daily_returns` nuls), plus une simple hypothese. (4) Angle mort ajoute : critere de sortie R4 `total_orders > 0` necessaire mais insuffisant. (5) 5e changement hors-perimetre note (`run_secondary` / WRC secondaire `NOT_RUN`). (6) Rebuild depuis `3bcfe35` fige comme methode d'audit reproductible. | Corrections de precision, sans changer la posture de gouvernance ni les non-goals de la note. |
| 2026-07-16 | Decision humaine explicite (section 3) : (1) Archive R4 -> **ajouter une entree tracee** actant que le `PASS` reposait sur une NAV degenerescente, sans reecrire `closure_reason`. (2) `FAIL` WRC primaire courant -> **documenter et clore** comme verdict de recherche legitime, sans ouvrir de chantier de recherche sur la famille de candidats. | Fixe la portee du futur chantier (section 4) a : verification/preuve + documentation + reconciliation de G5. Exclut explicitement toute investigation supplementaire sur la famille M1. Le sort des fichiers hors perimetre (section 1.3, prealable a la Phase 0) et le routage effectif via `/start` restent des decisions humaines distinctes, non couvertes par cette entree. |
| 2026-07-16 | Decision humaine explicite (section 1.3, Phase 0) : **commiter explicitement** les 4 fichiers hors perimetre G5, plutot que les reverter. Justification verifiee avant decision : 152/152 tests passent (`python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation`), les fichiers sont deja documentes dans `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` (format `AI_MODIFICATION_CHECKLIST`, statut `ACCEPTED`), et reverter aurait reintroduit le bug de NAV nulle en production, contredisant la decision precedente sur la section 3 (le `FAIL` primaire actuel depend de ce correctif pour etre un resultat honnete). | Execute : commit `ebff49d` (7 fichiers : les 4 hors perimetre + 3 fichiers deja autorises couples au meme correctif -- `build_research_package.py`, `test_nautilus_research_package.py`, `HISTORIQUE DES VERSIONS EBTA ENGINE.md`). Phase 0 de la section 4 est desormais completee. `.ai/checkpoint.json` et `.ai/backlog/fixes/PLAN_CORRECTION_GATE_ROBUSTESSE_G5_FIGE.md` (activation du workstream) restent non commites -- decision distincte, non couverte ici. Cette note reste non routee via `/start`. |
