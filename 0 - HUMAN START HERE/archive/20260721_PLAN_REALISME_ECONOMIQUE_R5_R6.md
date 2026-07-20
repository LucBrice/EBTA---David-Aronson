# Brouillon humain raffine — Realisme economique R5/R6

Date de preparation : 2026-07-21  
Decision humaine source : `1B`, `2A`  
Parent : `EPIC_MATURITE_MOTEUR_CAMPAGNE_RECHERCHE`

## Intention

Remplacer, dans le chemin de production du package Nautilus MVP, les frais
indicatifs, le slippage nul et les trois scenarios de robustesse inertes par :

1. une calibration R5 reproductible, versionnee et auditable ;
2. des composantes economiques separees (spread, slippage, commission,
   latence et qualite de fill) ;
3. trois executions R6 reellement distinctes aux niveaux p50, p95 et p99 ;
4. un hurdle `minimum_mean_return = 0.0` capable de produire un echec reel.

Le package peut rester rouge. Un verdict `FAIL` ou `INCONCLUSIVE` est un
resultat valide ; il ne doit jamais etre masque.

## Decisions humaines actees

- R5 — choix B provisoire : preuve mixte. Le spread NASDAQ observe dans les
  donnees locales est prioritaire. Plusieurs sources officielles de brokers
  servent de proxys pour XAUUSD, la latence, les fills et, si les unites et
  modeles de compte sont comparables, les frais.
- Une moyenne inter-courtiers n'est calculee que sur une grandeur normalisee
  et comparable. Elle est publiee avec ses constituants ; elle ne transforme
  pas des statistiques heterogenes en observation de marche.
- R6 — choix A : `CENTRAL=p50`, `PLAUSIBLE_BASE=p95`, `EXTREME=p99`, avec
  `minimum_mean_return = 0.0`.
- Les quantiles pilotent les couts et degradations. Les trois scenarios doivent
  relancer le calcul sur des resultats distincts ; renommer trois fois le meme
  resultat est interdit.

## Corpus de calibration a figer

### Preuve empirique locale prioritaire

- 36 CSV tick NASDAQ mensuels couvrant 2023-2025, avec colonnes ask/bid.
- Provenance actuelle : `UNVERIFIED_LOCAL_EXPORT` jusqu'a production d'une
  attestation externe plus forte.
- Le diagnostic exploratoire deja effectue sur un sous-echantillon de janvier
  ne constitue pas la calibration finale. Le chantier doit lire les 36 mois,
  controler les prix invalides/marches croises, documenter la politique
  d'echantillonnage et produire p50/p95/p99 reproductibles.
- Si la source locale est plus defavorable que le proxy broker comparable, la
  source locale gouverne le scenario CENTRAL par prudence.

### Sources broker officielles consultees le 2026-07-21

#### NASDAQ 100 — spread cote en points

| Source officielle | Mesure publiee | Usage autorise |
|---|---:|---|
| IG, US Tech 100 | 1 point en session principale, 2 hors session, 5 pendant les pauses | Point de comparaison de session ; ne pas moyenner les trois regimes entre eux |
| Pepperstone, NAS100 | moyenne 1,2 point, minimum 1, periode avril 2026 | Constituant de la moyenne comparable avec la moyenne publiee |
| IC Markets, USTEC | moyenne 1,807 point, minimum 1 | Constituant de la moyenne comparable avec la moyenne publiee |
| CMC Markets, US NDAQ 100 | minimum 1 point | Borne publiee, pas une moyenne realisee |

Moyenne descriptive demandee par l'humain, sur un chiffre representatif par
broker (`1,0 ; 1,2 ; 1,807 ; 1,0`) : **1,25175 point**. Cette valeur melange
deux moyennes et deux niveaux minimum/session ; elle est donc un indicateur de
comparaison, pas un estimateur scientifique. Elle ne remplace pas le p50 local
NASDAQ s'il est plus conservateur.

#### XAUUSD — spread cote par le broker

| Source officielle | Mesure publiee | Usage autorise |
|---|---:|---|
| IG, Spot Gold | 0,3 point | Proxy documente |
| Pepperstone, Spot Gold | a partir de 0,1 point | Borne minimale |
| IC Markets, XAUUSD | spread moyen 0,07 dans la fiche produit SCB | Proxy documente, juridiction/compte a conserver |
| CMC Markets, Gold | 0,2 point | Proxy documente |

Moyenne descriptive demandee (`0,3 ; 0,1 ; 0,07 ; 0,2`) : **0,1675 point**.
Elle melange moyenne et minimum et doit rester etiquetee `BROKER_PROXY`, jamais
`OBSERVED_EXECUTION`.

#### Latence et qualite de fill

| Source officielle | Mesure publiee | Limite |
|---|---:|---|
| IG API | 10,7 ms | Mesure broker ancienne, pas aller-retour machine utilisateur |
| Pepperstone | execution a partir de 50 ms ; fill rate 99,32 % | Claim plateforme, perimetre propre au broker |
| IC Markets | moins de 40 ms apres reception | Utiliser 40 ms pour la moyenne prudente |
| CMC Markets | mediane 4 ms | Claim plateforme, periode propre au broker |

Moyenne descriptive de latence (`10,7 ; 50 ; 40 ; 4`) : **26,175 ms**. Elle
ne mesure pas la latence de bout en bout et ne doit pas etre presentee comme
une distribution empirique. Les fill rates et statistiques de slippage ne
sont pas convertis l'un dans l'autre.

### URLs a conserver dans l'artefact source

- https://www.ig.com/en/help-and-support/articles/691241-what-are-ig-s-indices-cfd-product-details
- https://pepperstone.com/en-eu/markets/index-cfds/
- https://www.icmarkets.com/global/en/trading-markets/indices
- https://www.cmcmarkets.com/en-sg/indices
- https://www.ig.com/en/help-and-support/articles/691957-what-are-ig-s-commodities-cfd-product-details
- https://pepperstone.com/en-eu/markets/commodities/
- https://cdn.icmarkets.com/uploads/SCB/Commodity-Specification-Sheet.pdf
- https://www.cmcmarkets.com/en-sg/commodities
- https://www.ig.com/en/trading-platforms/trading-apis/how-to-use-ig-api
- https://www.icmarkets.com/global/jp/trading-pricing/trading-conditions
- https://www.cmcmarkets.com/en/trading-platforms/order-execution
- https://www.ig.com/en/best-execution

## Test de detection multi-lot

Resultat : `SINGLE`.

R5 produit un contrat et un artefact de calibration que R6 consomme directement
pour construire p50/p95/p99. R6 n'est pas executable ni verifiable sans R5 ;
les changements partagent le meme chemin de package, les memes tests de
contraste et la meme preuve finale. Le decoupage reste en phases sequentielles,
pas en sous-chantiers autonomes.

## Etat avant intervention

- `CostModel.slippage_bps` existe, mais le mapping Nautilus ne le consomme pas.
- `map_cost_model_to_venue()` transmet `prob_slippage`, les probabilites de
  fill et la latence.
- Dans NautilusTrader 1.230.0, `FillModel.prob_slippage` est la probabilite
  d'un glissement de **un tick** ; ce champ ne porte pas une magnitude en bps.
- Les maker/taker fees actuels sont indicatifs et non sources.
- Les trois scenarios de robustesse reutilisent aujourd'hui les memes resultats
  avec `minimum_mean_return = -1.0`.
- `risk/robustness.py` calcule deja les verdicts ; il doit etre reutilise.

## Architecture cible

### Contrat de calibration

Un artefact JSON versionne et un rapport Markdown derives par un generateur
deterministe contiennent, par actif et composante :

- source, URL ou chemin, date de consultation/periode ;
- provenance (`OBSERVED_LOCAL` ou `BROKER_PROXY`) et statut d'attestation ;
- unite originale, regle de normalisation, p50/p95/p99 ou borne disponible ;
- constituants et formule de toute moyenne ;
- limites d'extrapolation et politique de fallback ;
- hash des inputs locaux et version du schema de calibration.

Les donnees broker sont un snapshot source versionne ; le build de package ne
depend pas d'Internet et ne scrape rien en execution.

### Contrat de couts

- Etendre le contrat pour representer explicitement le spread, sans le coder
  comme commission ou slippage.
- Normaliser un spread en points au moment du fill : cout aller simple egal a
  la demi-fourchette multipliee par la quantite, puis conversion par un contrat
  explicite de valeur du point. Si la valeur du point n'est pas attestee, une
  representation en bps du prix de fill peut etre utilisee et doit etre
  etiquetee comme proxy ; aucune conversion implicite point -> dollar.
- Conserver les commissions Nautilus comme commissions.
- Conserver `prob_slippage` comme probabilite de mouvement d'un tick dans le
  simulateur ; ne jamais y injecter un nombre de bps.
- Appliquer, dans la frontiere adapter/extraction, un overlay economique
  itemise et deterministe lorsque Nautilus ne modele pas directement la
  magnitude requise. Publier valeur brute, valeur ajustee et decomposition.
- Affecter chaque debit au premier snapshot de NAV dont l'horodatage est
  superieur ou egal au fill, puis le conserver cumulativement. Les fills apres
  le dernier snapshot sont interdits ou rendent le resultat inconclusif ; ils
  ne peuvent pas disparaitre du ledger.
- Ajuster la serie de NAV/retours utilisee par les gates, pas seulement une
  ligne cosmetique de cout total.
- Ne pas compter deux fois le spread dans slippage ou impact.
- Les composantes non calibrees restent explicites ; leur absence peut produire
  `INCONCLUSIVE`, jamais un zero silencieux pretendument observe.

### Scenarios R6

- CENTRAL consomme les valeurs p50 ou, pour une preuve proxy sans distribution,
  la valeur centrale documentee la plus prudente.
- PLAUSIBLE_BASE consomme p95 et degrade aussi latence/fill selon une regle
  explicite et monotone.
- EXTREME consomme p99 ; si une source proxy n'offre aucun quantile, une regle
  conservatrice preregistree est necessaire et son origine doit etre visible.
- Il est interdit de baptiser p50/p95/p99 trois statistiques qui ne sont pas
  des quantiles. Pour les proxys broker clairsemes, publier a la fois le
  quantile descriptif inter-courtiers (methode explicite) et le faible nombre
  d'observations ; si les unites ne sont pas comparables, utiliser une borne ou
  rendre la composante `INCONCLUSIVE`.
- Chaque scenario execute le chemin de simulation/extraction. Les identifiants
  de run et resultats economiques doivent differer lorsque les couts different.
- Le hurdle est `minimum_mean_return = 0.0` pour les trois scenarios.

## Phases imposees

### Phase 0 — Gel des sources et contrat

- Figer le snapshot broker ci-dessus, ses dates, unites et limites.
- Identifier exactement les 36 fichiers NASDAQ ; ne pas les copier dans Git.
- Definir le schema interne de calibration et les erreurs bloquantes.
- Mettre a jour les notes API Nautilus avec la semantique « un tick ».

### Phase 1 — Generateur de calibration R5

- Lire les 36 mois NASDAQ en flux/chunks avec budget memoire borne.
- Valider ask/bid, exclure ou compter explicitement les lignes invalides,
  calculer des quantiles exacts ou une approximation dont l'erreur est testee.
- Produire JSON + Markdown deterministes et hashes des inputs.
- Normaliser les proxys broker sans moyenner des unites non comparables.
- Tester reproductibilite, ordre des fichiers, lignes invalides et fallback.

### Phase 2 — Propagation economique executable

- Etendre les contrats de couts sans rupture silencieuse.
- Propager spread/slippage/commission/latence/fill dans l'adapter et le package.
- Exposer le detail par composante et ajuster NAV/retours avant les gates.
- Tester absence de double comptage, signe des couts, zero volume, achat/vente,
  conversion point/bps, affectation temporelle des debits, fill hors snapshots,
  compatibilite des anciens appels et erreurs de calibration.

### Phase 3 — Stress R6 reel

- Construire CENTRAL/PLAUSIBLE_BASE/EXTREME depuis la calibration gelee.
- Relancer effectivement les segments pour chaque scenario.
- Reutiliser `risk/robustness.py` avec `minimum_mean_return = 0.0`.
- Ajouter un test de contraste : un cout/stress assez severe doit pouvoir faire
  echouer le scenario sans modifier artificiellement le verdict.

### Phase 4 — Package et preuves

- Regenerer le package `nautilus_mvp` par le chemin de production.
- Verifier la presence de la provenance, de la decomposition de couts, des
  scenarios distincts et du verdict derive.
- Executer tests cibles, suite complete, build package et validation package.
- Accepter et expliquer `FAIL`/`INCONCLUSIVE` si c'est le resultat reel.

## Perimetre pressenti

Autorises sous reserve de l'audit du plan normalise :

- `Implementation/ebta_engine/strategies/contracts.py`
- `Implementation/ebta_engine/adapters/nautilus_mapping.py`
- `Implementation/ebta_engine/package_builder/execution_calibration.py` (nouveau)
- `Implementation/ebta_engine/package_builder/nautilus_research_package.py`
- tests cibles sous `Implementation/ebta_engine/tests/`
- `Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md`
- artefacts versionnes sous `Implementation/calibrations/r5_r6/`
- package genere `Implementation/research_packages/nautilus_mvp/`
- historique de versions du moteur si le repo l'exige.

Interdits sans nouvelle decision humaine :

- `Protocole/`
- `BACKTRADER`
- relachement des validateurs/schemas pour faire passer un package
- dependance reseau lors du build
- donnees proprietaires brutes dans Git
- moyenne opaque de brokers, zero silencieux, verdict force.

## Exit criteria

1. Calibration NASDAQ 2023-2025 reproductible sur les 36 fichiers, avec
   provenance, quantiles p50/p95/p99 et controles de qualite publies.
2. Snapshot multi-brokers versionne avec chiffres, URLs, dates, unites,
   formules de moyenne et limites ; XAUUSD reste clairement `BROKER_PROXY`.
3. Spread, slippage, commission, latence et fill ne sont pas confondus ; les
   couts nets affectent les NAV/retours evalues par les gates.
4. CENTRAL/PLAUSIBLE_BASE/EXTREME executent des parametrages et resultats
   distincts, ordonnes de facon monotone et package-visibles.
5. `minimum_mean_return = 0.0`; un test de contraste prouve qu'un scenario peut
   echouer sans hardcoder le verdict.
6. Aucun frais indicatif ou slippage nul silencieux ne subsiste sur le chemin
   de production NASDAQ/XAUUSD vise.
7. Tests cibles, suite complete, build et validation package reels sont
   journalises ; bug-hunter et plan-conformance ne signalent aucun ouvert.

## Journal des audits d'architecture du brouillon

### Passe 1 — 2026-07-21

Constats majeurs integres dans ce brouillon :

- R5/R6 est un flux dependant unique, pas deux lots independants.
- `prob_slippage` Nautilus ne porte qu'un glissement d'un tick ; il ne remplace
  pas un contrat de magnitude.
- Une simple modification du cout total serait une facade si NAV/retours et
  gates continuaient a consommer les resultats bruts.
- Les moyennes broker sont heterogenes ; leurs constituants et limites doivent
  etre publies et la preuve locale conservatrice reste prioritaire.

### Passe 2 — a completer avant `/start`

Date : 2026-07-21. Convergence obtenue apres integration des constats suivants :

- la calibration publiee en points ne peut pas etre soustraite d'une NAV en
  dollars sans contrat de valeur du point ; la conversion point/bps est
  maintenant explicite et testable ;
- un overlay post-simulation doit etre un ledger horodate, affecte aux
  snapshots de NAV et cumulatif, faute de quoi les gates verraient une serie
  economique incoherente ;
- les quatre chiffres broker ne constituent pas magiquement une distribution
  d'execution. Les quantiles inter-courtiers restent descriptifs, avec faible
  effectif et fallback `INCONCLUSIVE` en cas d'incomparabilite ;
- l'overlay mesure un cout economique net et ne pretend pas reproduire le
  chemin microstructurel d'un fill. Cette limite doit apparaitre dans le
  package et interdit toute etiquette `OBSERVED_EXECUTION` pour XAUUSD.

Aucun nouveau blind spot majeur n'est apparu apres ces corrections. Le
brouillon est convergent pour etre normalise par `/start`.
