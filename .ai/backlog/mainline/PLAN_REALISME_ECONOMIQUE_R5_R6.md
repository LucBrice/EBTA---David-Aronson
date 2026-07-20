# Plan d'implementation — Realisme economique R5/R6

## 0. Bandeau de statut (a verifier avant toute promotion)

| Champ | Valeur |
|---|---|
| Track | mainline |
| Lifecycle | TRIAGED |
| Type de chantier | SINGLE |
| Scope | Calibrer les frictions NASDAQ/XAUUSD, les propager dans les resultats nets du package Nautilus MVP, puis executer trois stress p50/p95/p99 reellement distincts avec hurdle nul. |
| Non-goals | Modifier le Protocole ; certifier les donnees locales ; simuler une microstructure complete ; toucher BACKTRADER ; ouvrir l'OOS ; relacher un validateur. |
| Source | `0 - HUMAN START HERE/archive/20260721_PLAN_REALISME_ECONOMIQUE_R5_R6.md` |
| Exit criteria | Calibration gelee et reproductible ; couts nets itemises dans NAV/retours ; trois executions distinctes ; `minimum_mean_return=0.0` ; test de contraste echouable ; package valide structurellement avec verdict derive. |

- [x] Aucun chantier actif ne couvre ce perimetre au 2026-07-21.
- [x] Les decisions humaines R5 `1B` et R6 `2A` sont journalisees.
- [x] Le test multi-lot conclut `SINGLE` : R6 depend de l'artefact R5.
- [x] Le brouillon a subi deux passes `/evaluate` convergentes.
- [ ] Routage mecanique par `plan.ps1 start`.
- [ ] Deux passes `/evaluate` du plan route puis baseline pre-implementation.

## Audit IA de promotion

Le code reel a ete relu avant redaction. `CostModel.slippage_bps` existe mais
n'est pas consomme par `map_cost_model_to_venue()`. Nautilus 1.230.0 traite
`FillModel.prob_slippage` comme la probabilite d'un deplacement de prix d'un
tick, pas comme une magnitude en bps. `extract_simulation_result()` calcule la
NAV brute puis ne somme que les commissions. Enfin, le builder transmet les
memes resultats aux trois labels de robustesse avec un seuil `-1.0`.

Le plan corrige le chemin causal complet : source -> calibration -> contrat de
cout -> execution/extraction -> NAV et retours nets -> robustesse -> package.

## Triage

| Question | Reponse |
|---|---|
| Le chantier contient-il plusieurs lots independants ? | Non. R6 consomme directement les quantiles et contrats produits par R5. |
| Une phase peut-elle etre close sans l'autre ? | Non : la preuve finale exige calibration et stress executable dans le meme package. |
| Autorite normative | SOP 05 et SOP 09B, gelees et non modifiees. |
| Autorite executable | `Implementation/ebta_engine/` et artefacts de calibration/package. |
| Risque dominant | Cout cosmetique qui n'affecte pas la serie evaluee, ou confusion spread/slippage/commission. |

## Sous-chantiers

Sans objet (`Type de chantier: SINGLE`). Le decoupage ci-dessous est un chemin
critique de phases interdependantes, pas une orchestration multi-lot.

## Statut

`PENDING / TRIAGED` — route par `/start`, audite deux fois et pret pour la
baseline puis `/continue`.

## Carte d'execution IA (lecture prioritaire pour `/continue`)

| Element | Contrat de reprise |
|---|---|
| Objectif courant | Produire R5 avant de construire R6. |
| Premier geste | Revalider checkpoint/hook/tracking, puis inspecter le diff depuis la baseline. |
| Ordre obligatoire | Phase 0 -> 1 -> 2 -> 3 -> 4. |
| Verrou | Aucune valeur broker non normalisee ne peut entrer dans le moteur. |
| Arret | Une unite/valeur de point introuvable, une composante incomparable ou une preuve locale invalide produit une erreur explicite ou `INCONCLUSIVE`, jamais une hypothese silencieuse. |
| Cloture | bug-hunter complet puis plan-conformance-audit, ensuite seulement `/close`. |

## 1. Role de ce document et non-objectifs

Ce document commande la livraison du Lot 2 de
`EPIC_MATURITE_MOTEUR_CAMPAGNE_RECHERCHE`. Il transforme les decisions humaines
en contrats executables et preuves package-visibles.

Il ne certifie ni que les prix locaux proviennent d'un fournisseur nomme, ni
que les claims broker mesurent l'execution de cette machine. `BROKER_PROXY` et
`UNVERIFIED_LOCAL_EXPORT` restent visibles. Un overlay economique mesure le
cout net ; il ne pretend pas reproduire chaque mecanisme de microstructure.

## 2. Contexte obligatoire a lire avant de coder

1. `AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json`, hook et tracking actifs.
2. `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md`.
3. SOP 05 (stress pre-OOS) et SOP 09B (execution, frictions, donnees incompletes).
4. `.ai/governance/AI_MODIFICATION_CHECKLIST.md`.
5. `0 - HUMAN START HERE/archive/20260721_PLAN_REALISME_ECONOMIQUE_R5_R6.md`
   et le parent EPIC, notamment leur journal du 2026-07-21.
6. `Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md`.
7. Contrats, mapping, builder, robustesse et tests cites dans l'etat des lieux.

## 3. Table des gates (points de decision sequentiels)

| Gate | Condition PASS | Sinon |
|---|---|---|
| G0 Sources | Snapshot broker date, URL, unite et limite ; 36 fichiers NASDAQ identifies | STOP calibration |
| G1 Qualite locale | ask/bid valides, exclusions comptees, hashes et quantiles reproductibles | `INCONCLUSIVE` ou correction source |
| G2 Normalisation | Conversion points/bps/monetaire explicite par actif | STOP propagation |
| G3 Ledger | Toute composante est itemisee, horodatee et affecte NAV/retours une fois | STOP R6 |
| G4 Contraste | p50/p95/p99 sont monotones, executes separement et peuvent changer le verdict | STOP package |
| G5 Package | Build reel et `validate_package_dir()` s'executent sans facade | Eligible audit final |

## 4. Etat des lieux (avant/apres) — reutiliser avant de recreer

### Ce qui existe deja

- `CostModel`, `InstrumentConfig` et `SimulationResult` sont les contrats SSoT.
- `map_cost_model_to_venue()` cable FillModel, fee model et LatencyModel.
- `extract_simulation_result()` construit NAV, retours, fills et commissions.
- `risk/robustness.py` derive correctement `PASS`, `REJECTED_ECONOMIC` ou
  `INCONCLUSIVE` a partir de resultats par scenario.
- Le builder accepte deja un `data_root` explicite ou `EBTA_DATA_ROOT`.
- Le package et ses validateurs existent ; ils sont reutilises sans relachement.

### Ce qui manque reellement

- Une calibration canonique et reproductible sur les 36 mois tick NASDAQ.
- Un snapshot multi-brokers XAUUSD/NASDAQ/latence/fill avec limites explicites.
- Un contrat distinct pour spread et magnitude de slippage.
- Une conversion explicite depuis points vers cout economique.
- Un ledger qui affecte les NAV/retours evalues, pas uniquement `total_costs`.
- Trois runs de stress distincts et un seuil reel `0.0`.

## 5. Decision d'architecture

La calibration est un artefact offline versionne, construit par une fonction
pure autant que possible. Le build du package ne depend jamais du reseau. Les
sources broker sont figees dans un snapshot avec leurs metadonnees ; les CSV
locaux restent hors Git et sont designes par chemin/hash.

Le modele economique comporte deux niveaux :

1. les capacites natives Nautilus (commission, probabilite d'un tick de
   slippage, probabilite de fill, latence) ;
2. un ledger d'ajustement net, dans la frontiere adapter, pour les magnitudes
   documentees que Nautilus ne peut pas porter sans confusion.

Ce choix preserve la semantique de l'API et rend visible la limite de l'overlay.
Il est prefere a l'injection du spread dans maker/taker ou `prob_slippage`, qui
creerait un double comptage ou une unite fausse.

### Frontieres explicites (ce que chaque couche fait / ne fait pas)

| Couche | Fait | Ne fait pas |
|---|---|---|
| Calibration | Lit, controle, normalise, calcule et trace les sources | N'exerce aucun verdict EBTA |
| Contrats | Porte des champs types/valides et provenance | N'invente aucune valeur par defaut dite observee |
| Adapter | Configure Nautilus et construit le ledger net | Ne confond pas les composantes |
| Builder | Execute chaque scenario et publie les preuves | Ne reutilise pas un resultat sous trois labels |
| Robustesse | Evalue les resultats fournis | Ne calibre ni ne simule |

### Contrat d'interface entre les couches

- Calibration par actif : `spread`, `slippage`, `latency`, `fill`, `fees`,
  chacun avec unite, provenance et scenarios p50/p95/p99.
- Le JSON canonique stocke des identifiants de fichiers relatifs au data root,
  jamais le chemin absolu propre a cette machine ; le rapport d'execution peut
  montrer le root hors du payload hashe.
- Les spreads locaux sont lus comme decimaux, convertis en unites entieres a la
  precision source et agreges par table de frequences. Les quantiles sont ainsi
  exacts et bornes en memoire sans charger toutes les lignes.
- Le cout d'un fill publie `native_commission`, `spread_cost`,
  `slippage_cost`, `total_execution_cost` et la methode de conversion.
- Un cout en points exige une valeur du point attestee ; a defaut il est
  converti en bps relativement au prix du fill et marque `BROKER_PROXY`.
- Le demi-spread est debite a chaque cote ; la somme aller-retour ne doit pas
  doubler deux fois le spread complet.
- Chaque debit est affecte au premier snapshot `timestamp >= fill_timestamp`,
  puis cumule dans les snapshots suivants. Un fill orphelin est une erreur.
- `daily_returns` est recalcule depuis la NAV nette ; `total_costs` est la somme
  du ledger, commissions natives incluses une seule fois.

### Decisions deja actees

- `1B` : preuve mixte, moyenne uniquement si comparable.
- `2A` : p50/p95/p99 et `minimum_mean_return = 0.0`.
- NASDAQ local prioritaire lorsqu'il est plus conservateur que le proxy.
- Absence de preuve : `INCONCLUSIVE`, pas zero silencieux.

### Structure cible

```text
Implementation/
  calibrations/r5_r6/
    broker_sources.json
    calibration.json
    calibration_report.md
  ebta_engine/package_builder/
    execution_calibration.py
    nautilus_research_package.py
  ebta_engine/adapters/nautilus_mapping.py
  ebta_engine/strategies/contracts.py
  ebta_engine/tests/
```

### Perimetre de fichiers explicite (autorises / interdits)

Autorises :

- `Implementation/ebta_engine/strategies/contracts.py`
- `Implementation/ebta_engine/adapters/nautilus_mapping.py`
- `Implementation/ebta_engine/package_builder/execution_calibration.py` (new)
- `Implementation/ebta_engine/package_builder/nautilus_research_package.py`
- tests cibles sous `Implementation/ebta_engine/tests/`
- `Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md`
- `Implementation/calibrations/r5_r6/**`
- `Implementation/research_packages/nautilus_mvp/**` genere
- `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`

Interdits : `Protocole/**`, `BACKTRADER/**`, validateurs/schemas hors besoin
demontre et nouvel audit, donnees brutes proprietaires, appels reseau au build.

## 6. Decoupage en phases

### Phase 0 - Gel des sources et contrats de calibration

Livrables : snapshot broker (URLs/date/unites/limites), notes API mises a jour,
contrat de calibration et erreurs explicites.

Verification :

```powershell
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_execution_calibration.py
```

### Phase 1 - Calibration NASDAQ et proxy XAUUSD

Lire les 36 CSV tick NASDAQ en chunks, controler ask/bid, compter exclusions,
calculer p50/p95/p99 exacts par frequences decimales, hasher les inputs, puis
produire JSON et Markdown deterministes sans chemin machine dans le hash. Pour
les quatre brokers, publier les constituants des moyennes :
NASDAQ `1.25175` point, XAUUSD `0.1675` point, latence `26.175` ms, sans les
presenter comme observations realisees.

Verification :

```powershell
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m ebta_engine.package_builder.execution_calibration --data-root $env:EBTA_DATA_ROOT --output Implementation\calibrations\r5_r6
# Relancer exactement la commande precedente une seconde fois, puis :
git diff --exit-code -- Implementation/calibrations/r5_r6
```

### Phase 2 - Propagation economique executable

Etendre les contrats avec validations non-negatives et provenance. Configurer
les fonctions natives Nautilus selon leur vraie semantique. Construire le
ledger horodate, netter la NAV, recalculer les retours et publier brut/net.
Tester achat/vente, demi-spread, quantite nulle, timestamps, fill orphelin,
double comptage, compatibilite et serialisation subprocess.

Verification :

```powershell
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_r2_extraction.py
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_phase5_run_segment.py
```

### Phase 3 - Trois stress R6 reels

Construire un `CostModel` par scenario, executer le meme segment avec seeds et
inputs controles, puis envoyer trois listes distinctes a
`compute_robustness_scenarios()`. Verifier monotonie des couts et contraste de
verdict avec `minimum_mean_return = 0.0`.

Verification :

```powershell
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_risk_robustness.py
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_research_package.py
```

### Phase 4 - Package, non-regression et preuves

Regenerer par le chemin reel, accepter son statut, valider la structure, lancer
la suite complete et documenter les resultats dans le plan.

Verification :

```powershell
.\Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m ebta_engine.package_builder.nautilus_research_package
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
python -c "from pathlib import Path; from ebta_engine.validators.package_validator import validate_package_dir; print(validate_package_dir(Path('Implementation/research_packages/nautilus_mvp'))['status'])"
```

### Chemin critique (ordre des phases)

`P0 sources -> P1 calibration -> P2 propagation nette -> P3 stress -> P4 package`

## 7. Artefacts produits

- Snapshot broker avec URLs officielles et date du 2026-07-21.
- Calibration JSON machine-readable et rapport Markdown humain.
- Hashes et rapport qualite des 36 fichiers NASDAQ sans copie des donnees.
- Ledger de couts par composante dans les resultats/package.
- Trois scenarios package-visibles avec resultats et verdicts derives.
- Tests de contraste et historique moteur.

## 8. Invariants absolus et NO GO

### Invariants (non negociables dans le code)

- Le resultat Test reste separe de l'OOS.
- Tout cout est non negatif, itemise et debite exactement une fois.
- Les scenarios sont monotones en adversite et executes distinctement.
- La provenance et la limite d'extrapolation survivent jusqu'au package.
- Un statut rouge est conserve.

### NO GO (actions explicitement interdites — a verifier a chaque revue de diff)

- Encoder le spread comme commission ou probabilite de slippage.
- Soustraire des points directement d'une NAV en dollars.
- Appeler Internet lors du build.
- Transformer fill rate en slippage sans modele documente.
- Fabriquer p50/p95/p99 depuis des valeurs incomparables.
- Modifier un validateur ou un schema pour obtenir artificiellement PASS.
- Mettre `True`, `-1.0`, zero silencieux ou verdict force a la place d'une preuve.
- Toucher `Protocole/` ou BACKTRADER.

## 9. Verification a chaque etape

Apres chaque phase : inspecter `git diff`, executer les tests cibles et verifier
qu'aucun fichier interdit n'est touche.

```powershell
git diff --check
git status --short
python -m compileall Implementation/ebta_engine
```

Avant cloture : appliquer `bug-hunter` sur tous les fichiers moteur touches,
lancer le type-checker configure par le skill, la suite complete, le build et
la validation package, puis `plan-conformance-audit` sur chaque Exit criterion.

### Execution sans interruption

Une fois la baseline creee, `/continue` execute le chemin critique jusqu'a un
resultat verifiable. Une erreur de donnees, d'unite ou de contrat est traitee
dans le perimetre ; si elle exige une nouvelle decision normative, le chantier
s'arrete et l'escalade est journalisee.

### Autorite decisionnelle accordee

L'IA peut choisir les noms internes, la methode de quantile documentee, le
chunking et l'organisation des tests. Elle ne peut ni changer le hurdle `0.0`,
ni reclasser un proxy en observation, ni inventer une valeur du point.

### Interdiction des raccourcis (aucun faux succes)

Un test fixture-only ne prouve pas la calibration reelle. Une ligne de cout
dans un rapport ne prouve pas que la gate a consomme le net. Trois labels ne
prouvent pas trois executions. Chaque preuve doit suivre le chemin de production.

## 10. Journal des decisions humaines (autorisations)

| Date | Decision | Effet |
|---|---|---|
| 2026-07-21 | `1B` : rechercher plusieurs brokers et utiliser une moyenne lorsque pertinent | Autorise le proxy multi-brokers avec provenance/normalisation ; NASDAQ local prioritaire |
| 2026-07-21 | `2A` : scenarios p50/p95/p99 | Fixe les trois niveaux d'adversite |
| 2026-07-21 | Reutiliser `minimum_mean_return = 0.0` | Fixe le hurdle reel et echouable |

## 11. Risques et blocages connus

| Risque | Mitigation |
|---|---|
| Faible effectif broker | Publier N, constituants et limites ; `INCONCLUSIVE` si incomparable |
| Valeur du point inconnue | Conversion bps explicite ou STOP ; jamais point=dollar implicite |
| Overlay cosmetique | Ledger horodate, NAV nette et retours recalcules testes |
| Fill apres dernier snapshot | Erreur explicite, pas de cout perdu |
| Explosion du temps de build x3 | Tests cibles, budget documente, parallelisme existant preserve |
| Anciennes fixtures cassees | Compatibilite explicite sans conserver les valeurs indicatives en production |
| Quantiles locaux trop volumineux | Table de frequences sur entiers decimaux ; pas de liste de tous les ticks en memoire |

## 12. Definition of Done

- [ ] Les 36 fichiers NASDAQ ont un rapport qualite/hash et p50/p95/p99 reproductibles.
- [ ] Le snapshot broker contient valeurs, URLs, dates, unites, N, formule et limites.
- [ ] XAUUSD reste `BROKER_PROXY`; aucune provenance n'est surevaluee.
- [ ] Spread, slippage, commission, latence et fill sont separes.
- [ ] La NAV et les retours utilises par les gates sont nets des couts itemises.
- [ ] Trois executions distinctes alimentent CENTRAL/PLAUSIBLE_BASE/EXTREME.
- [ ] Les trois seuils `minimum_mean_return` valent `0.0`.
- [ ] Un test de contraste prouve un rejet economique possible.
- [ ] Build et validation package reels sont journalises, meme si le statut est rouge.
- [ ] Suite complete, bug-hunter et plan-conformance-audit sont propres.

## 13. Cloture

Ne fermer qu'apres satisfaction binaire de la Definition of Done. Appliquer
bug-hunter puis plan-conformance-audit avant `plan.ps1 close`; valider les JSON
de cockpit touches et creer uniquement le commit de cloture autorise.

### Resultat d'execution (a dupliquer a chaque session d'execution significative)

| Date | Phase | Modifications | Validations | Resultat |
|---|---|---|---|---|
| 2026-07-21 | Preparation | Recherche broker, brouillon et plan normalise | `/evaluate` brouillon x2 | Pret pour routage |

## 14. Journal d'audits post-hoc

| Date | Audit | Conclusion |
|---|---|---|
| 2026-07-21 | Brouillon passe 1 | Contrat unites, semantique Nautilus et chemin gate incomplets puis corriges |
| 2026-07-21 | Brouillon passe 2 | Ledger horodate, conversion points/bps et limites proxy ajoutes ; convergence |
| 2026-07-21 | Plan route `/evaluate` 1 | Pointeur du brouillon archive et commandes Python/module invalides corriges ; architecture conservee |
| 2026-07-21 | Plan route `/evaluate` 2 | Quantiles locaux exacts et bornes en memoire ; chemins machine exclus du hash canonique ; aucun nouveau blind spot majeur, convergence |
