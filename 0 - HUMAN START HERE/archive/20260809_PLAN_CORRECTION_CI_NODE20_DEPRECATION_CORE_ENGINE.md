# Brouillon — Correction Node.js 20 avec contrat supply-chain synchronise

> Statut : `INTAKE`. Ce document remplace le workstream supersede
> `PLAN_CORRECTION_CI_NODE20_DEPRECATION_ACTIONS`. Il n'autorise aucun push.

## Objectif

Supprimer l'avertissement GitHub Actions `Node.js 20 is deprecated` du
workflow `ebta-runtime-suite` en mettant a jour les deux actions officielles
epinglees, tout en synchronisant le contrat executable qui verrouille leurs
SHA sous `Implementation/ebta_engine/tests/test_ci_supply_chain.py`.

## Cause racine et reclassification

Le premier plan avait borne le diff a deux lignes YAML et avait ete route
`GOVERNANCE/common`. L'execution a montre que `EXPECTED_USES` et le scenario
hostile `mutable_tag` figent volontairement les anciennes valeurs. La suite
canonique a donc retourne 2 echecs sur 292 tests apres le bump.

Le precedent `.ai/archive/20260809_PLAN_DURCISSEMENT_WORKFLOW_CI.md`,
proprietaire de ce test, est classe `CONTRACT_ENCODING/core-engine`. Le
remplacement doit reprendre cette classification et ce workflow.

## Triage propose

| Champ | Valeur |
| --- | --- |
| Track | `fix` |
| Lifecycle | `INTAKE`, puis `TRIAGED` apres `/start` |
| Type de chantier | `SINGLE` |
| Classification | `CONTRACT_ENCODING` |
| Scope | Mettre a jour les deux pins SHA/commentaires du workflow et les trois chaines correspondantes du contrat de test supply-chain. |
| Non-goals | Aucun changement des triggers, permissions, etapes, commandes, pins Python ou comportement des tests; aucune modification de `Protocole/`; aucune nouvelle dependance; aucun push implicite. |
| Source | Workstream supersede `PLAN_CORRECTION_CI_NODE20_DEPRECATION_ACTIONS`, suite canonique `FAIL` 2/292, simulation en memoire 8/8 tests supply-chain `PASS`, autorisation humaine `Oui` du 2026-08-09. |
| Exit criteria | Releases officielles prouvees `node24`; diff limite aux deux lignes YAML et trois chaines de test; 8/8 tests supply-chain, Pyrefly, Ruff, 292 tests et schemas `PASS`; run GitHub Actions reel `success` sans warning Node.js 20. |

## Test multi-lot

Resultat : `SINGLE`.

- Le YAML seul echoue le contrat supply-chain.
- Le test seul contredirait le workflow live.
- Les deux changements partagent le meme Exit criteria et le meme rollback.
- Un blocage de l'un empeche l'autre d'etre clos honnetement.

## Etat live verifie

Le 2026-08-09 :

| Action | Tag stable | SHA commit | Runtime | Input requis |
| --- | --- | --- | --- | --- |
| `actions/checkout` | `v7.0.1` | `3d3c42e5aac5ba805825da76410c181273ba90b1` | `node24` | `persist-credentials` present |
| `actions/setup-python` | `v7.0.0` | `5fda3b95a4ea91299a34e894583c3862153e4b97` | `node24` | `python-version` present |

Les tags, SHA et `action.yml` doivent etre resolus de nouveau a
l'implementation. La release `setup-python v7` retire l'input `pip-install`,
qui n'est pas utilise par le workflow EBTA.

## Fichiers autorises

```text
.github/workflows/ebta-runtime-suite.yml
Implementation/ebta_engine/tests/test_ci_supply_chain.py
```

Mutations exactes attendues :

1. `actions/checkout` : `v4.2.2` -> release stable officielle `node24`.
2. `actions/setup-python` : `v5.6.0` -> release stable officielle `node24`.
3. `EXPECTED_USES` : synchroniser les deux valeurs avec le YAML.
4. Scenario `mutable_tag` : remplacer sa chaine source par le nouveau pin
   checkout, en conservant sa mutation vers un tag flottant (`@v7`) afin que
   le test hostile continue d'echouer comme prevu.

## Fichiers interdits

```text
Protocole/
Implementation/ hors test_ci_supply_chain.py
.agents/
.codex/
toute autre ligne du workflow CI
```

Les mutations `.ai/` sont reservees au cycle mecanique du plan.

## Invariants et NO GO

1. Les deux actions restent epinglees par SHA de commit complet et commentaire
   de tag exact.
2. `permissions: contents: read` et `persist-credentials: false` restent
   inchanges.
3. Aucun test supply-chain n'est supprime, ignore ou relache.
4. `EXPECTED_USES` reste une allowlist exacte, non derivee du YAML sous test.
5. Le scenario hostile `mutable_tag` doit encore prouver qu'un tag flottant
   est refuse.
6. Un `FAIL`, timeout, run absent ou logs inaccessibles ne devient jamais
   `PASS`.
7. Aucun changement scientifique ou normatif EBTA.

## Phases

### Phase 1 — Revalidation externe

Resoudre les releases, tags, SHA, runtime `node24`, changelogs et inputs
depuis les depots officiels.

### Phase 2 — Contrat synchronise

Appliquer les deux lignes YAML et les trois substitutions de chaine du test.

### Phase 3 — Validations locales

Executer :

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_ci_supply_chain.py
python -m pyrefly check --python-interpreter-path python --replace-imports-with-any "nautilus_trader.*" Implementation/ebta_engine Implementation/notebooks
python -m ruff check Implementation/ebta_engine
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
python -c "import json, jsonschema; jsonschema.validate(json.load(open('.ai/checkpoint.json', encoding='utf-8')), json.load(open('.ai/checkpoint.schema.json', encoding='utf-8')))"
python -c "import json, jsonschema; jsonschema.validate(json.load(open('Implementation/Active/tracking.json', encoding='utf-8')), json.load(open('Implementation/Active/tracking.schema.json', encoding='utf-8')))"
```

Appliquer ensuite `bug-hunter`, `adversarial-tester` et
`plan-conformance-audit` avant `/close`.

### Phase 4 — Preuve distante

Apres autorisation humaine explicite de push, verifier un run reel
`ebta-runtime-suite` : conclusion `success` et absence du warning Node.js 20.

## Rollback

Revenir ensemble aux deux anciens pins et aux trois anciennes chaines de test.
Ne jamais ne restaurer qu'un cote du contrat.

## Decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-09 | `Oui` a la proposition de superseder le plan `GOVERNANCE/common` et creer/promouvoir un remplacement `CONTRACT_ENCODING/core-engine` couvrant YAML et test. | Autorise replanification, baseline et implementation locale de ces deux fichiers. N'autorise aucun push. |

## Audit IA intake

| Passe | Verification et correction | Resultat |
| --- | --- | --- |
| 1 | Confrontation au workflow live, a `test_ci_supply_chain.py`, au `FAIL` 2/292 et au precedent `.ai/archive/20260809_PLAN_DURCISSEMENT_WORKFLOW_CI.md`; classification corrigee en `CONTRACT_ENCODING/core-engine`, perimetre et cinq substitutions explicites. | Aucun autre fichier executable requis; aucune modification normative. |
| 2 | Revalidation des releases officielles et simulation en memoire des trois substitutions du test : 8/8 tests supply-chain `PASS`, y compris le scenario hostile; test multi-lot rejoue. | Convergence : chantier `SINGLE`, scope borne et preuves fail-closed. |

## Definition of Done du brouillon

- [x] Cause racine et precedent de classification identifies.
- [x] Perimetre exact des cinq substitutions defini.
- [x] Test multi-lot applique et resultat `SINGLE` justifie.
- [x] Gates `core-engine` et frontiere de push explicites.
- [x] Aucun fichier executable modifie par la creation de ce brouillon.
