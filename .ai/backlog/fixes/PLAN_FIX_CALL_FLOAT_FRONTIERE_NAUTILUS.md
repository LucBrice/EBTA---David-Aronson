# Plan d'implementation — refus explicite des erreurs `_call_float`

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Un chantier couvre-t-il deja ce perimetre ? | Non. Le chantier de formalisation qui a detecte le defaut est `DONE` et D3 impose un `fix` separe. |
| Un verrou de gouvernance bloque-t-il ce chantier ? | Non. La decision humaine D3 du 2026-07-29 autorise explicitement la correction. |
| Une nouvelle decision humaine est-elle necessaire ? | Non : le comportement actuel est un repli silencieux, pas une alternative methodologique legitime. |
| Ce plan remplace-t-il un chantier existant ? | Non. |

Test `epic-orchestrator` : **SINGLE**. La correction du helper, sa regression et
sa trace historique forment un seul critere de sortie ; elles ne sont ni
permutables ni cloturables independamment.

## Audit IA de promotion

- [x] Cockpit, hook, tracking, gouvernance et workflows applicables relus.
- [x] Defaut revalide dans le code reel avant redaction.
- [x] Brouillon audite en place par deux passes `/evaluate` convergentes.
- [x] API Nautilus verifiee par le cache et l'introspection du venv 1.230.0.
- [x] Perimetre autorise et interdit ferme.
- [x] Autorite normative et executable identifiee.
- [x] Aucun changement de seuil, gate, statut, verdict ou ordre EBTA.
- [x] Plan classe `fix` et `SINGLE`.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `fix` |
| Lifecycle | `TRIAGED` |
| Type de chantier | `SINGLE` |
| Scope | Remplacer le repli silencieux de `_call_float()` par un echec explicite et teste, sans snapshot NAV partiel. |
| Non-goals | Ne pas modifier `Protocole/`, `nautilus_mapping.py`, les schemas, package builders, gates ou verdicts ; ne pas introduire de valeur de remplacement ; ne pas toucher BACKTRADER. |
| Source | Decision humaine D3 du 2026-07-29, exemple adversarial `_call_float`, puis boucle de cloture demandee le 2026-07-30. |
| Exit criteria | Les cas valeur directe et mapping monodevise retournent le float attendu ; exception d'appel, valeur absente/invalide/non finie et mapping vide/multidevise levent un `RuntimeError` contextualise ; `_record_nav_snapshot()` reste atomique ; test cible, suite complete, Pyrefly et `git diff --check` passent ; historique runtime mis a jour. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `NON_DEMARRE` |
| Date de creation | 2026-07-30 |
| Date d'activation | - |
| Autorite normative | `Protocole/` gelé EBTA-DOC-1.1, notamment SOP 08 et SOP 09B ; non modifie. |
| Autorite executable | `Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py`. |
| Changement normatif attendu | Aucun. Classification `ADAPTER_MAPPING`. |
| Dependances externes | `nautilus_trader==1.230.0` dans le venv dedie, disponible et introspecte. |

## Carte d'execution IA

| Champ | Contenu operationnel |
| --- | --- |
| Objectif executable | Faire echouer explicitement toute extraction Nautilus invalide au lieu de fabriquer `0.0`. |
| Autorite et lecture minimale | `AGENTS.md` → workflows commun/core-engine → ce plan → bridge → test Phase 4 → notes API → historique runtime. |
| Perimetre autorise | Bridge, test Phase 4, historique runtime, ce plan et mutations cockpit via `plan.ps1`. |
| Interdits absolus | Aucun changement `Protocole/`, gate, verdict, schema, package builder ou mapping ; aucun fallback numerique. |
| Phase de reprise | Phase 1, apres baseline convergee. |
| Preuve attendue | Test cible, suite complete, Pyrefly, adversarial-tester, Guardian, conformance et `git diff --check`. |
| Arret et escalade | Toute correction exigeant un statut, seuil, gate, verdict ou fichier hors liste fermee. |

## 1. Role de ce document et non-objectifs

Ce plan est la carte d'un correctif de frontiere. `Protocole/` reste normatif ;
le bridge reste une traduction executable subordonnee ; les notes Nautilus
decrivent l'API externe mais ne deviennent pas une norme EBTA.

Non-objectifs :

- ne pas changer la doctrine EBTA ;
- ne pas reconstruire l'extraction NAV ;
- ne pas modifier les packages de recherche existants ;
- ne pas transformer une erreur de frontiere en statut scientifique ;
- ne pas ajouter de dependance.

## 2. Contexte obligatoire

1. `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md`.
2. `.ai/governance/AI_MODIFICATION_CHECKLIST.md`.
3. `.ai/workflows/common/WORKFLOW.md` puis `core-engine/WORKFLOW.md`.
4. `Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py`.
5. `Implementation/ebta_engine/tests/test_nautilus_phase4_strategy_costs.py`.
6. `Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md`, section
   Portfolio, confirmee pour 1.230.0 par introspection le 2026-07-30.
7. `.agents/skills/adversarial-tester/EXAMPLE_REPORT.md`.

Hierarchie :

```text
Protocole EBTA
  -> contrats executables Implementation/
    -> bridge Nautilus
      -> API Nautilus 1.230.0
```

Une erreur de l'adaptateur ne peut pas devenir silencieusement une mesure
scientifique exploitable.

## 3. Etat des lieux

| Element | Etat reel | Decision |
| --- | --- | --- |
| `_record_nav_snapshot()` | Lit equity puis exposition et append un tuple. | Conserver la structure ; prouver qu'aucun append n'arrive si une lecture echoue. |
| `_call_float()` | Appelle un attribut/methode, aplati un dict monovaleur, parse le premier token, mais retourne `0.0` sur toute erreur. | Conserver les formes valides ; supprimer les deux replis. |
| Cache API | `Portfolio.equity` et `net_exposure` verifies pour 1.230.0. | Reutiliser ; aucune nouvelle API. |
| Tests Phase 4 | Executent du code bridge dans le venv Nautilus. | Etendre ce test plutot que creer un harness concurrent. |

Manque reel : un contrat fail-closed testant toutes les branches hostiles et
l'atomicite du snapshot.

## 4. Decision d'architecture

Le helper reste local au bridge, mais devient fail-closed :

```text
appel Nautilus -> extraction forme supportee -> conversion float -> isfinite
       |                  |                       |
       +------ erreur contextualisee RuntimeError +
```

Toutes les erreurs d'extraction utilisent `RuntimeError` avec le nom de la
methode. Les exceptions de l'API et de conversion conservent leur cause via
`raise ... from exc`. Un mapping n'est accepté que s'il contient exactement
une valeur. `math.isfinite()` refuse `NaN` et les infinis.

Cette architecture évite un nouveau type public et maintient le correctif
strictement local. Elle ne choisit aucun statut EBTA : l'échec remonte au runner.

### Perimetre de fichiers explicite

Autorises :

```text
Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py      [MODIFIER]
Implementation/ebta_engine/tests/test_nautilus_phase4_strategy_costs.py [MODIFIER]
Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md               [MODIFIER]
.ai/backlog/fixes/PLAN_FIX_CALL_FLOAT_FRONTIERE_NAUTILUS.md          [MODIFIER]
.ai/checkpoint.json                                                   [plan.ps1 seulement]
```

Interdits :

```text
Protocole/
Implementation/ebta_engine/adapters/nautilus_mapping.py
Implementation/ebta_engine/package_builder/
Implementation/ebta_engine/schemas/
Implementation/ebta_engine/validators/
Implementation/research_packages/
BACKTRADER
```

## 5. Decoupage en phases

### Phase 1 - Rendre l'extraction fail-closed

Objectif : supprimer tout repli silencieux de `_call_float()`.

Classification : ADAPTER_MAPPING

Actions :

- importer `math`;
- appeler la methode et lever un `RuntimeError` contextualise avec cause si
  l'appel echoue ;
- refuser les mappings dont la cardinalite n'est pas exactement un ;
- convertir la valeur supportee, puis refuser toute valeur non finie ;
- ne jamais retourner de sentinelle plausible.

Livrables :

- bridge corrige.

Critere de sortie :

- aucune branche d'erreur de `_call_float()` ne retourne `0.0`.

### Phase 2 - Couvrir la frontiere et l'atomicite

Objectif : rendre le comportement hostile reproductible dans le venv Nautilus.

Classification : TEST_FIXTURE

Actions :

- etendre le script subprocess du test Phase 4 avec des doubles minimaux ;
- verifier valeurs directe et mapping monodevise ;
- verifier exception d'appel, `None`, texte invalide, `NaN`, `Inf`, mapping
  vide et mapping multivaleur ;
- appeler directement `_record_nav_snapshot()` sur un double et verifier que
  la liste reste vide si l'exposition echoue après une equity valide.

Livrables :

- regressions ciblees sans mocker la fonction testee.

Critere de sortie :

- le test cible passe et échouerait avec l'ancien fallback `0.0`.

### Phase 3 - Tracer et valider

Objectif : produire les preuves de non-regression et la trace runtime.

Classification : GOVERNANCE

Actions :

- ajouter une entree append-only a l'historique runtime ;
- lancer test cible, suite complete, Pyrefly et hygiene de diff ;
- appliquer Guardian, bug-hunter, adversarial-tester et conformance.

Livrables :

- historique et rapport de gates dans la section Cloture.

Critere de sortie :

- toutes les validations passent et aucun gate ouvert ne subsiste.

## 6. Artefacts produits

| Etape | Artefact | Preuve |
| --- | --- | --- |
| Phase 1 | Bridge fail-closed | diff + test hostile |
| Phase 2 | Regression dans le test Phase 4 | unittest cible |
| Phase 3 | Entree historique et preuves | suite, Pyrefly, skills |

## 7. Invariants absolus et NO GO

Invariants :

1. Une mesure inconnue n'est jamais remplacee par une valeur plausible.
2. Un snapshot est append uniquement après deux extractions valides.
3. La cause technique originale reste chainee.
4. Aucun contrat normatif EBTA ne change.

NO GO :

- retourner `0.0`, `None`, `NaN` ou une valeur par defaut sur erreur ;
- capturer une exception sans la relever ;
- accepter un mapping multidevise en choisissant arbitrairement une valeur ;
- modifier un gate ou un verdict pour absorber l'erreur ;
- affaiblir ou skipper un test.

## 8. Verification a chaque etape

```powershell
python -m unittest Implementation.ebta_engine.tests.test_nautilus_phase4_strategy_costs

python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation

Implementation/adapters/nautilus_env/venv/Scripts/python.exe -m pyrefly check `
  Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py `
  Implementation/ebta_engine/tests/test_nautilus_phase4_strategy_costs.py `
  --output-format min-text

git diff --check
```

Le test cible doit réellement exécuter les cas de frontière dans le venv ; un
`SKIP` n'est pas un `PASS`.

### Execution sans interruption

Après baseline, exécuter les trois phases sans retour humain tant que le
perimetre fermé suffit. S'arrêter uniquement pour une dépendance indisponible,
un besoin normatif ou un fichier indispensable hors scope.

### Autorite decisionnelle accordee

L'IA peut choisir la formulation précise des messages d'erreur et les doubles
de test, sans changer le type `RuntimeError`, les cas couverts ni le périmètre.

### Interdiction des raccourcis

Toute validation échouée doit être corrigée à la cause. Aucun skip, fallback,
stub ou gate artificiellement vert n'est admissible.

## 9. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-29 | D3 — OUI, `_call_float` est route comme chantier `fix` separe. | Autorise la correction du bridge dans ce plan, sans changement normatif. |
| 2026-07-30 | Executer la boucle de cloture des suites. | Autorise l'enchainement `/start` → `/continue` → `/close` de ce sujet. |

## 10. Risques et blocages connus

| Risque | Impact | Mitigation |
| --- | --- | --- |
| Test lance hors venv | Import Nautilus impossible ou skip trompeur | Sous-processus explicite vers le venv et assertion de sortie. |
| Erreur trop generique | Diagnostic difficile | Nom de methode et cause chainee. |
| Snapshot partiel | NAV/exposition incoherentes | Test direct avec equity valide puis exposition en erreur. |
| Rejet d'une forme Nautilus valide | Regression runtime | Conserver valeur directe, premier token de `Money` et mapping monovaleur. |

## 11. Definition of Done

- [ ] Trois phases terminees.
- [ ] Tous les Exit criteria sont prouves.
- [ ] Aucun fichier hors perimetre modifie.
- [ ] Test cible sans skip et suite complete PASS.
- [ ] Pyrefly zero erreur sur les fichiers touches.
- [ ] Historique runtime mis a jour append-only.
- [ ] Guardian conclut `CONFORME`.
- [ ] Bug-hunter : zero bug confirme ouvert.
- [ ] Adversarial-tester : aucun fallback silencieux restant.
- [ ] Plan-conformance : aucun critere manquant.
- [ ] `git diff --check` PASS.

## 12. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat final | A remplir apres gates. |
| Ecarts par rapport au plan initial | A remplir. |
| Suites a prevoir | A remplir ; ne pas inventer de suite si aucune preuve ne l'exige. |

## 13. Journal d'audits post-hoc

| Date | Passe | Correction |
| --- | --- | --- |
| 2026-07-30 | Intake 1 | Type d'erreur, cause chainee, nombres non finis et atomicite rendus explicites. |
| 2026-07-30 | Intake 2 | Contrat d'erreur uniformise et commande cible ajoutee ; convergence. |
| 2026-07-30 | Plan normalise 1 | Autorites SOP 08/09B relues integralement ; confirmation que l'imputation silencieuse de zero et une NAV non reconstructible sont interdites. Aucun changement de perimetre requis. |
| 2026-07-30 | Plan normalise 2 | Controle du chemin de test subprocess, de l'atomicite et du contrat d'exception ; aucun nouvel angle mort majeur, convergence atteinte. |
