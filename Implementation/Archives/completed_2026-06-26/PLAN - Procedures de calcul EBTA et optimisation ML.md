# PLAN - Procedures de calcul EBTA et optimisation ML

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | ACCEPTED - PLAN_FIGE_AVANT_IMPLEMENTATION |
| Date | 2026-06-25 |
| Version runtime cible | EBTA-ENGINE-0.1.0 |
| Autorite normative | `Protocole/` gele en `EBTA-DOC-1.0` |
| Type | GOVERNANCE / IMPLEMENTATION_DETAIL |
| Impact protocole | NONE |
| Regle | Implementer uniquement selon les decisions de gel ci-dessous. |

## Objectif

Transformer les procedures de calcul citees par le protocole EBTA en modeles
executables, reproductibles et auditables dans `Implementation/ebta_engine/`.

Le but n'est pas de creer une nouvelle methode EBTA. Le but est de montrer
concretement a quoi ressemblent les calculs et processus deja definis par les
SOP, pour que tout futur moteur de backtest puisse les reproduire ou les mapper.

Le lot doit rendre explicite la chaine :

```text
search_space snapshot
  -> optimisation / ML sur Train_k
  -> candidates representatives
  -> selection de complexite sur Test_k
  -> matrice complete des candidates
  -> detrending / zero-centering
  -> WRC local
  -> candidate gelee ou NO_MODEL
  -> OOS passif
  -> IC OOS separe du WRC
```

## Sources normatives principales

| Sujet | Source normative | Role |
| --- | --- | --- |
| Segmentation Train/Test/OOS | SOP 04 | Folds, purge, embargo, ordre temporel |
| Registre candidates | SOP 03 | Univers, candidates influentes, append-only |
| Optimisation / ML / complexite | SOP 06 | Train calibration, Test selection, ML manifest, NO_MODEL |
| WRC / SPA / Romano-Wolf / MCPM | SOP 02 | Inference Test, famille complete, tests secondaires |
| Detrending / zero-centering | SOP 07 | Separation signal/evaluation, WRC H0, OOS non zero-centered |
| Serie primaire / metriques | SOP 08 | Rendements, NAV, mesures de performance |
| IC OOS | SOP 01 | Estimation OOS et intervalle distinct du WRC Test |
| Execution / couts / capacite | SOP 09B | P&L net tradable, couts, fills, sizing |
| Paquet et reproduction | SOP 12 | Manifestes, hashes, reexecution |

## Audit des angles morts actuels

Le runtime actuel valide des artefacts EBTA, mais ne fournit pas encore les
procedures de calcul qui produisent ces artefacts.

| Angle mort | Etat actuel | Risque si non traite | Cible d'implementation |
| --- | --- | --- | --- |
| Snapshot d'espace de recherche | `candidate_space` est un objet libre dans `config.json` | Optimisation non opposable, parametres modifies ex post | Schema / modele `search_space` |
| Optimisation parametrique | Pas de log d'exploration Train/Test | Impossible de prouver quelles variantes ont influence la selection | `optimization_log` append-only ou artefact JSON |
| Machine learning | Aucun manifeste ML executable | Features, fit, hyperparametres et seeds non reproductibles | `ml_manifest` |
| Complexite | Pas de calcul du maximum Test ni tie-breaks | Selection implicite ou visuelle | `complexity_selection_report` |
| Candidate matrix | WRC declare mais matrice complete non produite | Tester seulement la gagnante devient possible | `candidate_matrix` |
| WRC numerique | Rapport fixture, pas d'algorithme | Le gate Test reste declaratif | `wrc.py` + test numerique |
| SPA / Romano-Wolf / MCPM | Non implemente | Tests secondaires impossibles a auditer | Phase secondaire apres WRC |
| Detrending | Preuve declarative seulement | Confusion rendement brut / net / detrende | `detrending.py` |
| Zero-centering | Preuve declarative seulement | Risque d'utiliser zero-centering hors WRC | `zero_centering.py` |
| Bootstrap stationnaire | Non implemente | WRC et IC OOS non reproductibles | `bootstrap.py` |
| IC OOS | Rapport fixture, pas d'algorithme | Risque de reutiliser la distribution WRC Test | `oos_confidence_interval.py` |
| P&L net / execution | Rapports fixture seulement | Le moteur valide des resultats sans montrer leur construction | `returns.py`, futur `execution.py` |
| NO_MODEL / STOP_PROCESS | Statuts cites mais pas de chemin pilote concret | Ambiguite quand aucune candidate admissible | Cas test dedie |
| Reproductibilite stochastique | Seeds dans docs, peu d'usage runtime | Resultats non repetables | seed derivation + logs |

## Audit complementaire des angles morts processus

Le premier audit ciblait les procedures de calcul. Une comparaison avec l'ordre
des gates G0 a G14 et les invariants INV-001 a INV-016 montre aussi des
procedures de processus a modeliser. Elles ne changent pas le premier lot SOP
06, mais elles doivent rester visibles dans le plan.

| Angle mort processus | Source | Risque si non traite | Cible future |
| --- | --- | --- | --- |
| Donnees point-in-time et disponibilite | SOP 09A, G1, INV-007 | Decisions prises avec donnees non disponibles a la date du fold | `data_availability.py` |
| Construction des folds, purge, embargo, warm-up | SOP 04, G0-G1, INV-001 | Chevauchement OOS, fuite temporelle, frontieres de fold floues | `walk_forward.py` |
| Registre append-only et lineage des candidates | SOP 03, G2, INV-004, INV-013 | Candidates influentes omises ou runs non opposables | `registry_lineage.py` |
| Robustesse pre-OOS | SOP 05, G5, INV-011 | Stress-tests utilisant l'OOS ou variantes non scellees | `robustness.py` |
| Scellement PRE_OOS et controle d'acces OOS | SOP 10, SOP 12, G7-G8, INV-002, INV-012, INV-016 | OOS consulte trop tot ou artefacts modifies apres scellement | `sealing.py`, `oos_access.py` |
| Gate economique separe | SOP 08, SOP 09B, G10, INV-010 | Gate economique confondu avec le gate statistique | `economic_gate.py` |
| Incubation, live limite et lifecycle | SOP 11, SOP 12, G12-G14, INV-014, INV-015 | Passage live sans paquet certifie ou monitoring non controle | `lifecycle.py` |

Ces cibles sont explicitement hors premier lot. Elles seront traitees apres les
procedures statistiques et SOP 06, sauf si un futur audit montre qu'une
dependance doit etre modelisee plus tot.

## Frontiere de conception

### Ce que le moteur doit faire

- fournir des fonctions de reference petites, testables et deterministes ;
- produire des artefacts lisibles qui expliquent les inputs, outputs et choix ;
- rendre impossible de masquer les candidates perdantes ou invalides ;
- montrer ou chaque procedure s'insere dans le Walk-Forward ;
- rester compatible avec un futur adaptateur BACKTRADER.

### Ce que le moteur ne doit pas faire

- inventer un nouveau seuil, statut, gate ou ordre de procedure ;
- remplacer les SOP comme source normative ;
- optimiser une vraie strategie pour chercher de la performance ;
- utiliser l'OOS pour selectionner, departager ou reparer ;
- importer les conventions d'un moteur externe dans le noyau EBTA.

## Architecture cible

```text
Implementation/
  implementation_context.json
  ebta_engine/
    procedures/
      __init__.py
      returns.py
      search_space.py
      optimization.py
      ml_manifest.py
      complexity_selection.py
      candidate_matrix.py
      detrending.py
      zero_centering.py
      bootstrap.py
      wrc.py
      oos_confidence_interval.py
      data_availability.py
      walk_forward.py
      registry_lineage.py
      robustness.py
      sealing.py
      oos_access.py
      economic_gate.py
      lifecycle.py
    tests/
      test_procedure_returns.py
      test_procedure_optimization.py
      test_procedure_candidate_matrix.py
      test_procedure_detrending.py
      test_procedure_zero_centering.py
      test_procedure_bootstrap.py
      test_procedure_wrc.py
      test_procedure_oos_ci.py
      test_procedure_data_availability.py
      test_procedure_walk_forward.py
      test_procedure_registry_lineage.py
      test_procedure_robustness.py
      test_procedure_oos_access.py
      test_procedure_economic_gate.py
      test_procedure_lifecycle.py
```

Les modules doivent rester standard-library first tant que possible. Une
dependance statistique externe ne doit etre ajoutee qu'apres decision explicite.

## Contexte JSON de suivi IA

Chaque lot d'implementation doit creer ou mettre a jour un fichier de contexte
machine-readable :

```text
Implementation/implementation_context.json
```

Ce fichier sert a une IA de reprise pour comprendre ce qui est en cours sans
relire tout l'historique de conversation.

Role du fichier :

- identifier le plan actif et le lot actif ;
- lister les phases terminees, en cours et bloquees ;
- garder le prochain module a traiter ;
- enregistrer les fichiers modifies par le lot courant ;
- enregistrer les commandes de verification lancees et leur resultat ;
- signaler les decisions `IMPLEMENTATION_DETAIL`,
  `DOCUMENTATION_CLARIFICATION_NEEDED` ou `NORMATIVE_CHANGE_REQUIRED` ;
- conserver les interdits actifs : pas de `Protocole/`, pas de BACKTRADER, pas
  de dependance externe dans le premier lot.

Structure minimale attendue :

```json
{
  "context_version": "1.0.0",
  "plan_file": "Implementation/PLAN - Procedures de calcul EBTA et optimisation ML.md",
  "runtime_version": "EBTA-ENGINE-0.1.0",
  "active_lot": "Phase 1 + Phase 2",
  "active_scope": ["SOP 06"],
  "completed_phases": [],
  "current_phase": "Phase 1 - Cartographie executable des procedures",
  "next_step": "Create PROCEDURE_CALCULATION_MAP.md",
  "blocked_items": [],
  "touched_files": [],
  "verification_log": [],
  "non_goals": [
    "No Protocole/ change",
    "No BACKTRADER access",
    "No external dependency",
    "No numeric WRC in first lot",
    "No real market data"
  ]
}
```

Ce fichier est un outil de reprise et de controle d'execution. Il ne remplace
pas le plan, l'historique runtime, la matrice de tracabilite ou le protocole.
Toute decision durable doit rester journalisee dans
`Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`.

## Artefacts a ajouter au paquet de recherche

Le paquet actuel reste valide, mais les futurs paquets pilotes devront enrichir
les preuves avec :

```text
research_package/
  reports/
    search_space.json
    optimization_log.json
    ml_manifest.json
    complexity_selection.json
    candidate_matrix.json
    data_availability.json
    fold_schedule.json
    registry_review.json
    robustness.json
    execution.json
    economic.json
    reproduction.json
    wrc.json
    oos.json
```

Ces artefacts ne deviennent contractuels qu'apres implementation et tests. Le
present plan ne change pas encore les schemas.

## Phases d'implementation

### Phase 0 - Gel du plan

Objectif : valider ce plan avant de coder.

Livrables :

- ce fichier relu et accepte ;
- decision explicite sur le scope du premier lot ;
- historique runtime mis a jour.

Definition de fini :

- statut du plan confirme comme `ACCEPTED - PLAN_FIGE_AVANT_IMPLEMENTATION`;
- aucune modification de `Protocole/`;
- aucun code de procedure encore ajoute.

Statut : DONE.

Decisions verrouillees :

- le premier lot de code couvre `Phase 1 + Phase 2` seulement ;
- le premier lot cible SOP 06 uniquement : optimisation, ML, complexite,
  candidates representatives et matrice de candidates ;
- le WRC numerique est reporte a la Phase 4 ;
- le modele ML pilote reste factice/deterministe et standard-library first ;
- aucune dependance externe n'est autorisee dans le premier lot ;
- les artefacts `search_space.json`, `optimization_log.json`,
  `ml_manifest.json`, `complexity_selection.json` et `candidate_matrix.json`
  restent des artefacts pilotes, pas encore des schemas obligatoires ;
- le pipeline minimal existant reste simple ;
- un second pilote dedie sera cree si necessaire sous
  `Implementation/examples/procedure_sop06_pilot/` ;
- aucune donnee de marche reelle n'est introduite dans le premier lot ;
- BACKTRADER reste non lu et non modifie ;
- `Protocole/` reste gele et non modifie.

### Phase 1 - Cartographie executable des procedures

Objectif : creer la carte `procedure -> SOP -> inputs -> outputs -> artefacts`.

Livrables :

- `Implementation/implementation_context.json` initialise pour le lot actif ;
- `Implementation/PROCEDURE_CALCULATION_MAP.md`;
- entree `TRACEABILITY_MATRIX.md` pour les futurs modules de procedures;
- tests de presence de la carte si pertinent.

Definition de fini :

- le contexte JSON indique le lot actif, le prochain module et les
  verifications executees;
- chaque procedure cite sa SOP proprietaire;
- chaque procedure a un input, output et interdit EBTA explicite.

### Phase 2 - Optimisation / ML / complexite SOP 06

Objectif : combler l'angle mort prioritaire.

Modules :

- `search_space.py`;
- `optimization.py`;
- `ml_manifest.py`;
- `complexity_selection.py`;
- `candidate_matrix.py`.

Artefacts pilotes :

- `reports/search_space.json`;
- `reports/optimization_log.json`;
- `reports/ml_manifest.json`;
- `reports/complexity_selection.json`;
- `reports/candidate_matrix.json`.

Tests minimaux :

- un espace parametrique simple avec 2 ou 3 niveaux;
- un exemple ML factice ou deterministe avec features et hyperparametres;
- un cas ou le maximum Test est selectionne;
- un cas d'egalite resolu par tie-break preenregistre;
- un cas `NO_MODEL`;
- verification que toutes les candidates influentes restent dans la matrice WRC.

Definition de fini :

- meme `Train_k` -> memes candidates representatives;
- meme `Test_k` -> meme complexite selectionnee;
- aucune candidate influente n'est omise;
- OOS n'intervient dans aucune decision de selection.

### Phase 3 - Calculs de performance et transformations SOP 07 / SOP 08 / SOP 09B

Objectif : montrer comment les series candidates sont construites avant WRC et
OOS.

Modules :

- `returns.py`;
- `detrending.py`;
- futur `execution.py` si le niveau de detail execution le justifie.

Tests minimaux :

- calcul de rendement net quotidien sur une petite serie;
- detrending local sur `Test_k`;
- preuve qu'un fit de transformation hors `Train_k` echoue;
- separation entre signal non detrende et evaluation detrendee.

Definition de fini :

- les series candidates avant WRC sont reproductibles;
- les sorties indiquent brut, net, detrende et benchmark;
- aucune transformation apprise n'utilise `Test_k` ou `OOS_k` quand elle doit
  etre fit sur `Train_k`.

### Phase 4 - Zero-centering, bootstrap et WRC SOP 02

Objectif : transformer le gate WRC declaratif en calcul numerique minimal.

Modules :

- `zero_centering.py`;
- `bootstrap.py`;
- `wrc.py`.

Tests minimaux :

- zero-centering par colonne avec moyenne proche de zero;
- indices bootstrap communs a toutes les candidates;
- WRC local sur matrice complete;
- interdiction de tester seulement la gagnante;
- resultat reproductible avec seed fixe.

Definition de fini :

- `wrc.py` produit statistique observee, distribution bootstrap, p-value et
  verdict;
- le rapport WRC conserve la famille complete applicable;
- SPA / Romano-Wolf restent explicitement secondaires si non implementes dans
  ce lot.

### Phase 5 - IC OOS SOP 01

Objectif : calculer l'intervalle OOS sans reutiliser la distribution WRC Test.

Module :

- `oos_confidence_interval.py`.

Tests minimaux :

- bootstrap OOS separe;
- serie OOS concatenee;
- intervalle reproductible avec seed fixe;
- echec si la source de bootstrap indique WRC Test.

Definition de fini :

- l'IC OOS est construit sur la serie OOS, pas sur le WRC;
- le rapport OOS expose estimation, IC, methode et seed.

### Phase 6 - Procedures de gouvernance non statistiques

Objectif : modeliser les procedures qui entourent les calculs statistiques sans
les confondre avec eux.

Modules :

- `data_availability.py`;
- `walk_forward.py`;
- `registry_lineage.py`;
- `robustness.py`;
- `sealing.py`;
- `oos_access.py`;
- `economic_gate.py`;
- `lifecycle.py`.

Tests minimaux :

- une decision refusee si une donnee n'est pas disponible a sa date ;
- un calendrier refusant le chevauchement OOS ;
- une candidate influente absente du registre detectee ;
- une robustesse pre-OOS qui echoue si elle consomme l'OOS ;
- un acces OOS refuse avant `PRE_OOS_SEALED` ;
- un gate economique publie separement du gate statistique ;
- une incubation refusee avant `VALIDATION_READY`.

Definition de fini :

- les gates G0, G1, G2, G5, G7, G8, G10, G12, G13 et G14 disposent d'un modele
  de procedure ou d'un point de validation explicite ;
- les procedures restent subordonnees aux SOP proprietaires ;
- aucune procedure de gouvernance ne remplace un verdict statistique.

### Phase 7 - Integration dans le pipeline pilote

Objectif : remplacer les rapports factices du pilote par des rapports produits
par les procedures.

Livrables :

- mise a jour de `Implementation/examples/minimal_pilot_pipeline/`;
- ou creation d'un `procedure_pilot_pipeline/` separe si le changement devient
  trop large;
- paquet `research_package/` valide.

Definition de fini :

- `validate_package_dir()` retourne `PASS`;
- les tests runtime passent;
- les rapports pilotes sont issus des modules `procedures/`.

### Phase 8 - Pre-adaptation BACKTRADER

Objectif : preparer le mapping vers un moteur externe sans lire ni modifier
BACKTRADER dans ce lot.

Livrables :

- liste des sorties que BACKTRADER devra fournir;
- mapping `external engine outputs -> EBTA procedure inputs`;
- erreurs contractuelles attendues.

Definition de fini :

- BACKTRADER pourra etre ouvert plus tard avec une cible precise;
- aucune dette ou convention BACKTRADER n'entre dans le noyau EBTA.

## Ordre recommande des prochains lots

1. Implementer Phase 1 et Phase 2 ensemble.
2. Tester apres chaque module significatif.
3. Implementer Phase 3.
4. Implementer Phase 4.
5. Implementer Phase 5.
6. Implementer Phase 6.
7. Brancher le pipeline pilote sur les procedures.
8. Seulement ensuite ouvrir une discussion d'adaptation BACKTRADER.

## Perimetre fige du premier lot

Le premier lot d'implementation est :

```text
Phase 1 + Phase 2 seulement.
Standard-library first.
SOP 06 uniquement.
ML factice/deterministe.
Nouveaux artefacts pilotes non encore schemas obligatoires.
Second pilote dedie procedure_sop06_pilot si necessaire.
Pas de WRC numerique.
Pas de donnees de marche reelles.
Pas de BACKTRADER.
Pas de changement Protocole/.
```

Ce gel limite le risque : il comble l'angle mort optimisation/ML sans melanger
tout de suite WRC numerique, IC OOS et donnees de marche reelles.
