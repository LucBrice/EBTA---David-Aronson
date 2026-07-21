# Brouillon - Preuve package pre-OOS refusee

## Probleme constate

Le chantier mere `EPIC_MATURITE_MOTEUR_CAMPAGNE_RECHERCHE` a clos ses quatre
lots, mais son Exit criterion global reste non prouve. Le builder Nautilus
calcule deja les rapports pre-OOS R5/R6, puis retourne `DENIED` quand les
preuves humaines externes sont absentes. A ce point, le repertoire persistant
ne contient que `config.json` et `registry.jsonl`; les rapports calcules ne
sont pas materialises et `validate_package_dir()` ne peut pas verifier G5/G6.

## Objectif

Produire sur le chemin de production reel un paquet de preuve partiel et
honnete quand l'acces OOS est refuse : conserver la configuration, le registre,
les rapports strictement pre-OOS, un `gates.json` derive et le rapport du
validateur, sans creer d'artefact OOS ni revendiquer un stade SOP 12 non atteint.

## Classification et test multi-lot

- Classification : `IMPLEMENTATION_DETAIL`.
- Test multi-lot : `SINGLE_CHANTIER`. La materialisation, la derivation des
  gates et la validation sont sequentielles et couvertes par un seul critere de
  sortie. Aucun sous-lot ne peut etre clos independamment.
- Parent narratif : `EPIC_MATURITE_MOTEUR_CAMPAGNE_RECHERCHE`, correctif de la
  Phase 5 decouvert par l'audit global du 2026-07-21.

## Perimetre pressenti

- `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
  pour une primitive bornee de materialisation pre-OOS.
- `Implementation/ebta_engine/package_builder/nautilus_research_package.py`
  pour l'appeler avant le retour `DENIED`.
- `Implementation/ebta_engine/tests/test_nautilus_research_package.py` et tests
  du pilote minimal pour les contrastes.
- `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` pour la trace runtime.

## Invariants et NO GO

- Aucun appel au runner OOS, notamment aucun seed `29`, avant autorisation.
- Aucun `oos_access_log.jsonl`, `reports/oos.json`, serie OOS ou manifeste
  `VALIDATION_READY` en cas de refus.
- G5/G6 derivent des rapports reels R5/R6; G7/G8 restent non-PASS sans preuves.
- Les gates post-OOS/live restent `INCONCLUSIVE` et ne consomment aucune fixture.
- Ne pas modifier `Protocole/`, les schemas, le validateur, les seuils, les
  calibrations, l'API Nautilus ou BACKTRADER.
- Ne pas appeler le writer complet actuel, car il materialise aussi des
  rapports post-OOS/live issus des inputs du pilote.

## Exit criteria

1. Un build sans preuves humaines retourne toujours `DENIED` et n'appelle
   jamais l'OOS.
2. Le repertoire contient les rapports pre-OOS R5/R6 et `reports/gates.json`.
3. Le validateur retourne `FAIL` avec G5/G6 derives et G7/G8 non-PASS.
4. Aucun artefact OOS, manifeste de stade atteint ou preuve humaine fixture
   n'est materialise.
5. Tests cibles, suite complete, Pyrefly, bug-hunter et conformance passent.

## Audit d'architecture du brouillon

### Passe 1 - 2026-07-21

- Risque majeur releve : reutiliser `_write_reports()` tel quel produirait des
  rapports post-OOS/live et des invariants de fixture. Correction : writer
  pre-OOS dedie et liste blanche d'artefacts.
- Risque de faux stade : un manifeste `PRE_OOS_SEALED` ou `VALIDATION_READY`
  serait mensonger quand l'approbation manque. Correction : aucun manifeste.
- Risque de validation ambigue : le statut global doit rester `FAIL`.
  Correction : persister le rapport complet de `validate_package_dir()` et
  tester les gates individuels.

### Passe 2 - 2026-07-21

- Verification des frontieres : la primitive generique appartient au builder
  du pilote, l'orchestration reste dans le builder Nautilus.
- Verification de non-regression : le chemin autorise conserve le writer
  complet existant; seul le retour refuse utilise la nouvelle primitive.
- Convergence : aucun nouvel angle mort majeur; le plan normalise doit rendre
  explicites la liste blanche, la derivation de G0-G14 et le test d'absence
  d'artefacts OOS.

