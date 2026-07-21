# Plan d'implementation - Preuve package pre-OOS refusee

## 0. Bandeau de statut (a verifier avant toute promotion)

| Question | Reponse |
| --- | --- |
| Un chantier actif couvre-t-il deja ce perimetre ? | L'EPIC parent `EPIC_MATURITE_MOTEUR_CAMPAGNE_RECHERCHE` est actif, mais son plan interdit toute implementation directe. Le present correctif est le sous-chantier supplementaire requis par son audit Phase 5. |
| Un verrou de gouvernance bloque-t-il le chantier ? | Non. Le choix humain `3A` exige que l'absence de preuves humaines produise un refus honnête; il n'exige pas que les preuves pre-OOS calculees disparaissent du disque. |
| Une decision humaine nouvelle est-elle necessaire ? | Non. Aucun seuil, gate, statut ou ordre methodologique ne change. |
| Test multi-lot | `SINGLE_CHANTIER`. Ecriture bornee, derivation des gates et validation sont des phases sequentielles sous un Exit criteria commun. |
| Parent narratif | Sous-chantier correctif 5/5 de `EPIC_MATURITE_MOTEUR_CAMPAGNE_RECHERCHE`, decouvert pendant sa cloture generale. |

## Audit IA de promotion

- [x] Bootstrap repo, hook, tracking, entree protocole et checklist de modification lus.
- [x] SOP 10, SOP 12 et paquet d'execution identifies comme autorites.
- [x] Test `epic-orchestrator` applique : `SINGLE_CHANTIER`.
- [x] Etat reel du builder et des tests inspecte.
- [x] Brouillon audite en deux passes convergentes avant restructuration.
- [x] Aucun changement normatif ni nouvelle dependance requis.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `fix` |
| Lifecycle | `TRIAGED` |
| Type de chantier | `SINGLE_CHANTIER` |
| Scope | Materialiser un paquet de preuve strictement pre-OOS lorsque le builder Nautilus refuse l'ouverture, puis persister le rapport gate-par-gate du validateur. |
| Non-goals | Aucun OOS, manifeste de stade, serie OOS, preuve fixture, changement de seuil, schema, validateur, gate, `Protocole/`, API Nautilus ou BACKTRADER. |
| Source | Audit Phase 5 du parent et brouillon `0 - HUMAN START HERE/PLAN_PREUVE_PACKAGE_PRE_OOS_REFUSE.md`. |
| Exit criteria | Build sans preuve toujours `DENIED`; zero appel OOS; rapports pre-OOS et gates reels materialises; G5/G6 issus des calculs R5/R6; G7/G8 non-PASS; aucun artefact OOS/manifeste; validateur `FAIL` attendu et persiste; tests, Pyrefly, bug-hunter et conformance PASS. |

## Sous-chantiers

Sans objet : plan `SINGLE_CHANTIER`.

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `PRET_A_CLOTURER - IMPLEMENTATION ET AUDITS PASS` |
| Date | 2026-07-21 |
| Classification | `IMPLEMENTATION_DETAIL` |
| Autorite normative | SOP 10 pour le refus d'acces OOS; SOP 12 pour la fidelite du paquet; paquet d'execution pour G0-G14. |

## Carte d'execution IA (lecture prioritaire pour `/continue`)

| Champ | Contenu operationnel |
| --- | --- |
| Objectif executable | Persister les rapports pre-OOS deja calcules avant le retour `DENIED`, sans appeler le writer complet post-OOS. |
| Frontiere | Primitive generique de materialisation dans le builder du pilote; orchestration et retour dans le builder Nautilus. |
| Preuve minimale | Test de contraste sans approbation : rapports G5/G6 presents, G7/G8 non-PASS, seed 29 absent, fichiers OOS/manifeste absents. |
| Arret | Stop si la solution exige un nouveau stade SOP 12, un changement du validateur ou une autorisation OOS. |

## 1. Role de ce document et non-objectifs

Ce plan corrige une perte de preuve : les résultats pre-OOS sont calcules et
utilises pour refuser l'OOS, mais ne sont pas materialises. Il ne cherche pas a
transformer le refus en succes. Le `FAIL` du validateur est une sortie attendue
et explicite tant que les preuves humaines et artefacts OOS manquent.

## 2. Contexte obligatoire a lire avant de coder

1. `AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json` et cockpit runtime.
2. Plan parent actif et ce plan.
3. SOP 10 sections autorisation/scellement et SOP 12 stades du paquet.
4. `Protocole/PAQUET D'EXECUTION EBTA.md` gates G0-G14.
5. `nautilus_research_package.py::build_nautilus_inputs()` et
   `build_nautilus_research_package()`.
6. Builder pilote : préparation, cache pre-OOS, writer complet et validateur.
7. Tests Nautilus et approbations humaines existants.

## 3. Table des gates (points de decision sequentiels)

| Gate | Condition | Echec |
| --- | --- | --- |
| C0 | Le chemin est `DENIED` et aucun runner OOS n'a ete appele. | STOP |
| C1 | Seuls les artefacts de preuve pre-OOS autorises sont ecrits. | STOP |
| C2 | G5/G6 derivent des rapports calcules; G7/G8 restent non-PASS; G9/G10 restent `INCONCLUSIVE`. | STOP |
| C3 | Le validateur retourne et persiste `FAIL` sans erreur de schema sur config/registre. | STOP |
| C4 | Suites et audits finaux sont verts. | Autorise `/close` |

## 4. Etat des lieux (avant/apres) — reutiliser avant de recreer

### Ce qui existe deja

- `prepare_pre_oos_package()` cree durablement config et registre avant Test.
- `_pre_oos_reports()` calcule recherche, selection, WRC, robustesse,
  scellement, G-BIAS et decision d'acces; le résultat est hashé et mis en cache.
- L'execution R5/R6 remplit `execution_report` et trois scenarios distincts.
- `validate_package_dir()` fournit un rapport complet gate-par-gate même si le
  statut global est `FAIL`.

### Ce qui manque reellement

- Le retour `DENIED` intervient avant tout writer de rapports.
- Le writer complet n'est pas reutilisable tel quel : il ecrit des rapports
  OOS/incubation/live et un manifeste `VALIDATION_READY`.
- Le test historique exige exactement deux fichiers, ce qui fige la perte de
  preuve au lieu de verifier l'honnetete du paquet refuse.

## 5. Decision d'architecture

Ajouter une primitive explicite de materialisation `pre_oos_denied`, basee sur
une liste blanche. Elle consomme le cache immuable produit avant autorisation,
derive un `gates.json` complet où tout champ non encore prouvable vaut
`INCONCLUSIVE`, ecrit un `invariant_evidence.json` limite aux faits pre-OOS
reels, n'ecrit aucun artefact OOS et appelle ensuite le validateur.

Cette architecture est retenue parce qu'elle preserve l'ordre chronologique
existant et evite de faire passer les inputs historiques du pilote pour des
preuves post-OOS reelles. Reutiliser le writer complet serait un faux succes.

### Frontieres explicites (ce que chaque couche fait / ne fait pas)

| Couche | Fait | Ne fait pas |
| --- | --- | --- |
| Builder pilote | Derive et ecrit la liste blanche pre-OOS. | N'autorise pas l'OOS et ne cree pas de manifeste. |
| Builder Nautilus | Appelle la primitive sur `DENIED`, puis le validateur. | Ne duplique pas les calculs de gates. |
| Validateur | Rapporte les gates presents/manquants et le statut global. | Ne transforme pas un refus en PASS. |

### Contrat d'interface entre les couches

- Entree : `package_dir`, inputs finalises, cache pre-OOS valide et package
  shape uniquement pour identifier les artefacts hors phase.
- Sortie : dictionnaire du validateur, persiste dans
  `reports/package_validation.json` apres calcul.
- Build outcome : `status=DENIED`, `package_built=false`,
  `pre_oos_evidence_built=true`, `validation_status=FAIL`.

### Decisions deja actees

- Choix `3A` : absence de preuves humaines = non-PASS et OOS `DENIED`.
- Les fixtures restent test-only et ne peuvent servir de preuve globale.
- Le statut global du package peut rester `FAIL` dans l'EPIC parent.

### Structure cible

```text
nautilus_mvp/
  config.json
  registry.jsonl
  reports/
    gates.json
    wrc.json
    robustness.json
    execution.json
    sealing.json
    oos_access_decision.json
    invariant_evidence.json
    ...preuves Train/Test strictement pre-OOS...
    package_validation.json
```

Absents par contrat : `oos_access_log.jsonl`, `reports/oos.json`,
`reports/economic.json` (G10 final depend de l'OOS), `series/`, `manifests/`
et rapports incubation/live.

### Perimetre de fichiers explicite (autorises / interdits)

Autorises : builder pilote, builder Nautilus, tests correspondants, historique
runtime, ce plan et artefact persistant `nautilus_mvp`. Interdits :
`Protocole/`, schemas, validateurs, gates normatifs, calibrations, mappings
Nautilus, BACKTRADER.

## 6. Decoupage en phases

### Phase 0 - Contrat et liste blanche

- Definir les rapports pre-OOS autorises et les champs G0-G14 derives.
- Ajouter des assertions empechant un cache absent/mute et un statut autre que
  `DENIED`.
- Critere : aucune dependance post-OOS dans la primitive.

### Phase 1 - Materialisation refusee

- Ecrire atomiquement les rapports autorises.
- Laisser absent tout journal/serie/manifeste OOS.
- Appeler depuis le branchement `DENIED` du builder Nautilus.

### Phase 2 - Validation et preuve persistante

- Executer `validate_package_dir()` sur le paquet partiel.
- Persister son rapport et exposer son statut dans le build outcome.
- Regenerer `Implementation/research_packages/nautilus_mvp` sans preuve externe.

### Phase 3 - Non-regression et audits

- Tester seed 29 absent, G5/G6 derives, G7/G8 non-PASS et liste noire absente.
- Lancer tests cibles, suite complete, Pyrefly, bug-hunter et conformance.

### Chemin critique (ordre des phases)

`contrat -> writer -> branchement DENIED -> validation -> audits`.

## 7. Artefacts produits

| Artefact | Role |
| --- | --- |
| Paquet `nautilus_mvp` refuse | Preuve reproductible des calculs pre-OOS et du refus. |
| `reports/gates.json` | Verdicts G0-G14 sans facade post-OOS. |
| `reports/invariant_evidence.json` | Seulement les faits observables avant OOS; evidence absente = `INCONCLUSIVE`. |
| `reports/package_validation.json` | Sortie exacte du validateur. |
| Tests | Contraste permanent contre ouverture/fabrication. |

## 8. Invariants absolus et NO GO

### Invariants (non negociables dans le code)

- Le refus precede tout acces OOS.
- Une absence de preuve humaine ne devient jamais un `PASS`.
- Les rapports ecrits correspondent exactement au cache autorise.
- Toute preuve post-OOS absente reste absente ou `INCONCLUSIVE`.

### NO GO (actions explicitement interdites — a verifier a chaque revue de diff)

- Appeler `_write_reports()` complet sur le chemin refuse.
- Ecrire un manifeste `PRE_OOS_SEALED` ou `VALIDATION_READY` sans scellement PASS.
- Ecrire un journal d'acces ou une serie OOS vide pour satisfaire un chemin.
- Utiliser `TEST_FIXTURE`, modifier le validateur ou assouplir un gate.

## 9. Verification a chaque etape

```powershell
Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m unittest Implementation.ebta_engine.tests.test_nautilus_research_package
Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
Implementation\adapters\nautilus_env\venv\Scripts\pyrefly.exe check Implementation\ebta_engine\package_builder\nautilus_research_package.py Implementation\examples\minimal_pilot_pipeline\build_research_package.py Implementation\ebta_engine\tests\test_nautilus_research_package.py
Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m ebta_engine.package_builder.nautilus_research_package
```

Le build final doit retourner `DENIED`, puis le rapport persiste doit montrer
G5/G6 derives et G7/G8 non-PASS. Le statut global `FAIL` est attendu.

### Execution sans interruption

Les quatre phases sont autorisees par `/continue`; aucune confirmation n'est
necessaire tant qu'aucun seuil, statut, schema ou accès OOS ne change.

### Autorite decisionnelle accordee

L'IA peut choisir les noms de fonctions et factorisations internes minimales,
mais pas les gates, stades ou preuves exigibles.

### Interdiction des raccourcis (aucun faux succes)

Un test vert avec fixture humaine, fichier OOS vide ou manifeste mensonger ne
satisfait aucun Exit criterion.

## 10. Journal des decisions humaines (autorisations)

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-21 | Choix `3A` : preuves humaines explicites et optionnelles; absence `INCONCLUSIVE`/DENIED; fixtures uniquement dans les tests. | Autorise le paquet refuse, interdit toute auto-approbation. |
| 2026-07-21 | `/continue` persistant de l'EPIC. | Autorise le correctif necessaire a son Exit criterion global, selon le cycle enfant de l'orchestrateur. |

## 11. Risques et blocages connus

| Risque | Mitigation |
| --- | --- |
| Writer trop large | Liste blanche et test exact des fichiers interdits. |
| Gates recalcules differemment | Consommer le cache pre-OOS immuable et reutiliser les helpers existants. |
| Faux stade de package | Aucun manifeste sur refus. |
| Rapport de validation auto-referentiel | Valider d'abord, puis persister la sortie; le rapport n'est pas un artefact exige du manifeste. |

## 12. Definition of Done

- [x] Build production sans preuve `DENIED`, zero OOS.
- [x] Rapports pre-OOS et gates materialises.
- [x] G5/G6 reels; G7/G8 non-PASS; G9/G10 et post-OOS `INCONCLUSIVE`.
- [x] Aucun fichier OOS, serie ou manifeste.
- [x] Rapport validateur `FAIL` persiste et reproductible.
- [x] Tests, Pyrefly, bug-hunter et plan-conformance PASS.
- [x] Historique runtime synchronise; parent a synchroniser apres `/close` de cet enfant.

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat final | `PRET_A_CLOTURER` - paquet partiel pre-OOS auditable et refus conserve. |
| Ecarts | G6 reste `INCONCLUSIVE` uniquement sur `capacity_grid`, explicitement non calibree; aucun ecart de perimetre. |
| Suites | Reprendre la cloture generale du parent. |

### Resultat d'execution (a dupliquer a chaque session d'execution significative)

| Date | Phase | Resultat |
| --- | --- | --- |
| 2026-07-21 | Audit preparatoire | Perte de preuve confirmee; chemin correctif borne defini. |
| 2026-07-21 | Implementation | Writer a liste blanche, gates/invariants pre-OOS, validation persistee et serialization config conforme au schema existant. |
| 2026-07-21 | Build reel | 96 executions pre-OOS; `DENIED`; zero OOS; `FAIL` attendu; zero erreur schema/semantique; hash config exact. |

## 14. Journal d'audits post-hoc

| Date | Passe | Conclusion |
| --- | --- | --- |
| 2026-07-21 | Brouillon `/evaluate` 1 | Writer complet interdit; liste blanche et absence de manifeste ajoutees. |
| 2026-07-21 | Brouillon `/evaluate` 2 | Frontieres pilote/Nautilus et preuve de validateur clarifiees; convergence. |
| 2026-07-21 | Plan route `/evaluate` 1 | Angle mort `invariant_evidence` corrige : liste blanche pre-OOS et absence explicite pour toute preuve OOS/stade. |
| 2026-07-21 | Plan route `/evaluate` 2 | `economic.json` retire de la liste blanche : G10 depend de l'OOS et les inputs pilotes pre-OOS ne sont pas une preuve. Contrats de sortie et ordre d'ecriture revalides; convergence. |

### Bug-hunter final - 2026-07-21

| Controle | Resultat |
| --- | --- |
| Pyrefly cible | 0 erreur sur les deux builders et le test Nautilus. |
| Vrais bugs de contrat observes en build | Le config multi-actifs manquait les champs requis `fill_model`/`fee_model` et `instrument_id`/`symbol`/`venue`; la preuve humaine etait serialisee hors schema. Corriges sans modifier le schema. |
| Suite runtime | 208 tests `PASS`. |
| Pilote minimal | `FAIL` attendu G2/G7/G8/G14; zero erreur schema. |

### Plan-conformance-audit final - 2026-07-21

| Exit criterion | Classement | Preuve |
| --- | --- | --- |
| Refus et zero OOS | IMPLEMENTE | Test `test_missing_human_evidence_denies_oos_before_runner_access`; build reel `DENIED`, seed 29 absent. |
| Rapports pre-OOS/G5/G6 | IMPLEMENTE | `build_denied_pre_oos_evidence_package()` et package persistant; robustesse `FAIL`, execution `PASS`, cout 11,564. |
| Gates honnetes | IMPLEMENTE | Validateur : G5/G6/G7/G8 `INCONCLUSIVE` pour leurs exigences exactes; G9-G14 non-PASS. |
| Aucun artefact OOS/manifeste | IMPLEMENTE | Controle de liste noire et test de contraste. |
| Validateur persiste | IMPLEMENTE | `reports/package_validation.json`, statut `FAIL`, `schema_errors=[]`, `semantic_errors=[]`. |
| Audits finaux | IMPLEMENTE | 13 tests cibles, 208 tests complets, Pyrefly 0, diff-check PASS. |

Aucun `Non-goal` viole : `Protocole/`, schemas, validateurs, seuils,
calibrations, mappings Nautilus et BACKTRADER sont inchanges.
