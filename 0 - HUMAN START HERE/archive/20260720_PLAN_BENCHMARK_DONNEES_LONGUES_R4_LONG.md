# Brouillon - R4-long : benchmark donnees longues et scalabilite du runner

## But

Produire une preuve reproductible de ce que le moteur EBTA sait reellement
faire sur 1 mois, 3 mois et 1 an de donnees M1, sans ouvrir l'OOS et sans
presenter une projection comme une mesure. Le livrable doit separer la qualite
des donnees, le cout du chargement, le cout du chemin Test pre-OOS, la couverture
temporelle effectivement consommee et le verdict du validateur de package.

## Contexte verifie le 2026-07-20

- R7 est `DONE` : le data root est injectable et le hash de configuration est
  reel.
- Le data root contient 72 CSV mensuels par actif, de janvier 2020 a decembre
  2025, pour `NASDAQ` et `XAUUSD`.
- Un scan integral de 2020 a lu 509 760 lignes par actif. Il n'a trouve aucun
  doublon, aucun timestamp non monotone ou sans timezone, aucun OHLC incoherent
  et aucun volume negatif.
- `build_data_snapshot()` tronque actuellement son comptage a 10 000 barres :
  ce champ ne peut pas attester une fenetre longue.
- `build_nautilus_inputs()` charge toute la fenetre en listes Python, mais son
  `WalkForwardSplitter(2, 2, 1, 1)` ne consomme que quelques jours pour les
  segments Test/OOS. Une duree de fichier plus longue ne signifie donc pas que
  le runner a simule toute cette duree.
- Le runner de production lance 32 segments Test sequentiels en sous-processus.
  L'OOS n'est execute que si les gates pre-OOS l'autorisent ; le chemin reel
  actuel retourne `DENIED` sur `wrc_pass`.
- Le cache API et l'introspection locale confirment
  `nautilus_trader==1.230.0`, le caractere sequentiel de l'orchestration connue
  et l'existence de `BacktestEngine.run/add_data/clear_data/end`. R4-long
  reutilise l'adaptateur existant ; il n'invente pas une API Nautilus.
- Smoke preregistration execute avant promotion : `XAUUSD`, janvier 2020,
  chemin subprocess reel, termine en 47,086 s avec `DENIED(wrc_pass)` et sans
  `oos_access_log.jsonl`, sur une machine disposant d'environ 32 Gio de RAM.

## Test de detection epic-orchestrator

Verdict : `SINGLE_WORKSTREAM`.

Le validateur CSV est un prerequis du benchmark : une erreur de qualite bloque
la mesure et le rapport. Le rapport de scalabilite consomme ensuite les mesures
du validateur et du runner. Les phases ne peuvent donc pas etre reordonnees et
un blocage du validateur contamine les phases suivantes. Les trois conditions
de detection multi-lot ne sont pas reunies.

## Architecture proposee

1. Ajouter un inspecteur CSV streaming, sans materialiser toutes les barres,
   qui retourne pour un actif et une fenetre : nombre exact, bornes observees,
   fichiers touches, header, UTC, ordre strict, doublons, valeurs finies,
   enveloppe OHLC et volumes non negatifs. Il calcule aussi le SHA-256 du
   contenu effectivement lu et publie les trous temporels (nombre, duree
   maximale, distribution) sans les declarer invalides en l'absence d'un
   calendrier de marche normatif. Le snapshot reutilise ce resultat au lieu
   d'appeler le loader avec `max_bars=10_000`.
2. Ajouter un runner de benchmark CLI standard-library-first. Les cellules de
   donnees `(fenetre, actif)` mesurent scan/chargement ; une cellule pipeline
   conjointe par fenetre execute le vrai univers `NASDAQ+XAUUSD` (16 candidats,
   2 folds, donc 32 segments Test attendus). Chaque cellule s'execute dans un
   processus isole avec timeout. Le parent conserve le resultat meme si une
   cellule depasse son budget et distingue `COMPLETED`, `BUDGET_EXCEEDED`,
   `DATA_INVALID` et `ERROR`. Une somme de runs mono-actif ne peut pas etre
   presentee comme la mesure du pipeline conjoint.
3. Mesurer separement : scan qualite, chargement complet, chemin Test pre-OOS
   reel, temps monotone, peak working set agrege de l'arbre de processus
   (parent + descendants Nautilus), nombre de barres chargees, nombre de barres
   reellement simulees, nombre de segments et d'ordres. Le rapport calcule la
   couverture `simule / charge` et interdit d'appeler la projection une mesure.
   Si l'OS ne permet pas la mesure de l'arbre, la cellule est `ERROR` plutot que
   de publier la memoire du seul parent.
   Une instrumentation minimale et optionnelle du builder peut observer les
   longueurs des segments Test et les resultats sans changer leur contenu ni
   l'ordre d'execution ; elle est inactive hors benchmark et couverte par un
   test de non-regression.
4. Executer les fenetres progressives et preenregistrees :
   `2020-01-01..2020-01-31`, `2020-01-01..2020-03-31`,
   `2020-01-01..2020-12-31`. L'absence de cotation le week-end ou le dernier
   jour civil n'est pas une lacune si les fichiers sources sont exhaustifs ;
   les bornes observees restent publiees.
5. Le benchmark appelle le chemin Test existant et laisse l'autorisation OOS
   decider. Il exige `oos_access_decision.status == DENIED`, zero appel runner
   OOS et aucun `oos_access_log.jsonl`. Une autorisation inattendue est un
   `NO GO`, pas une occasion d'executer l'OOS.
6. Appeler `validate_package_dir()` sur le repertoire pre-OOS produit et
   enregistrer son verdict reel. `FAIL`/`INCONCLUSIVE` ou un build `DENIED`
   sont des constats admissibles ; le rapport ne les transforme jamais en
   `PASS` et n'affirme pas qu'un package final a ete construit.
7. Versionner un rapport JSON canonique et un README de lecture. Les seuils de
   budget sont fixes avant le run canonique ; si la cellule 1 an les depasse,
   le Lot 4 documente la limite et ne se clot qu'apres une correction ou une
   decision humaine explicite acceptant cette limite.
8. Enregistrer l'environnement de preuve : version Python/Nautilus, OS, CPU,
   RAM visible, data root, hash de contenu par fenetre, parametres, horodatages
   UTC de debut/fin et empreinte SHA-256 des fichiers Implementation mesures.
   Le rapport n'utilise pas un hash Git impossible a connaitre avant son propre
   commit comme identifiant de code.

## Perimetre pressenti

Autorise :

- `Implementation/ebta_engine/data/local_ohlcv.py`
- `Implementation/ebta_engine/benchmarks/` (nouveau module)
- `Implementation/ebta_engine/tests/test_local_ohlcv.py`
- `Implementation/ebta_engine/tests/test_long_data_benchmark.py`
- `Implementation/benchmarks/r4_long/README.md`
- `Implementation/benchmarks/r4_long/benchmark_report.json`

Conditionnel, seulement si une instrumentation minimale est indispensable et
testee :

- `Implementation/ebta_engine/package_builder/nautilus_research_package.py`

Interdit : `Protocole/`, schemas du package, gates, seuils R5/R6, approbations
humaines, BACKTRADER, execution OOS, optimisation de strategie.

## Budgets preregistres pour le run canonique

- Les budgets sont des garde-fous operationnels, pas des seuils scientifiques.
- Chaque cellule donnees `(fenetre, actif)` a un timeout dur de **180 secondes**.
  Chaque cellule pipeline conjointe a un timeout dur de **240 secondes**. Le
  plafond d'acceptation memoire est **8 Gio de peak working set agrege** ; il
  est mesure et peut faire echouer la cellule, mais n'est pas presente comme un
  coupe-circuit OS si la plateforme ne sait pas l'imposer sans dependance. Le
  run canonique complet a un timeout dur de **18 minutes**. Ces valeurs sont
  fixees apres le smoke de 47,086 s mono-actif et avant toute mesure canonique
  1/3/12 mois.
- Le budget memoire porte sur le peak working set mesure ; `tracemalloc` seul
  est insuffisant car il ignore les allocations Rust/Nautilus.
- Un run tue par timeout/OOM ne peut jamais etre marque `COMPLETED`.
- Un depassement produit un rapport partiel atomique dans un repertoire
  temporaire puis un remplacement du rapport final ; il ne laisse jamais un
  JSON tronque presente comme preuve canonique.

## Exit criteria

1. Le validateur streaming detecte par tests les headers invalides, timestamps
   naifs/non monotones/dupliques, nombres non finis, OHLC incoherents et volumes
   negatifs ; le snapshot rapporte le compte exact au-dela de 10 000 barres.
2. Les trois fenetres et les deux actifs figurent dans le rapport canonique,
   avec nombre exact de barres, temps, peak RSS, couverture simulee, segments,
   ordres, statut de budget et aucune ambiguite mesure/projection.
   Chaque fenetre contient aussi une mesure pipeline conjointe des 16 candidats
   et 32 segments Test attendus ; une divergence de cardinalite est un echec.
3. Le rapport prouve une exposition OOS nulle : decision `DENIED`, zero segment
   OOS, zero serie OOS et aucun journal d'acces OOS cree.
4. Le verdict reel de `validate_package_dir()` et le statut de build sont
   inclus sans facade ; un package final absent est dit absent.
   Dans ce Lot 4, « package valide » signifie que le validateur est execute et
   retourne un rapport structure sans exception sur l'etat pre-OOS reel ; un
   package final complet reste conditionne par R5/R6 et sera revalide par la
   preuve globale de l'EPIC.
5. Le smoke 1 mois a fixe les budgets avant le run canonique. La cellule 1 an est
   soit `COMPLETED` dans ces budgets, soit la limite est corrigee ou acceptee
   explicitement par l'humain avant cloture.
6. Tests cibles, suite complete, bug-hunter, Pyrefly et plan-conformance-audit
   passent avant `/close`.

## NO GO et arrets

- Ne jamais ouvrir l'OOS pour obtenir une mesure de performance.
- Ne jamais augmenter un budget apres avoir vu un echec canonique sans tracer
  un nouveau run/version et sa justification.
- Ne jamais appeler « benchmark 1 an du runner » un run qui n'a simule que les
  quelques jours du splitter actuel ; publier les deux volumes.
- Arret humain si le budget 1 an est depasse apres une correction raisonnable,
  si une extension normative/schema est requise, ou si le chemin pre-OOS devient
  inopinement `AUTHORIZED`.
