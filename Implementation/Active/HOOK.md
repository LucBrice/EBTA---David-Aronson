# HOOK Actif : Moteur de backtest natif EBTA

Le mainline actif est maintenant
`PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NATIF`.

## Decision de routage

Le plan `STEP_3_BACKTRADER_INTEGRATION` est remplace. BACKTRADER n'est plus un
moteur a integrer durablement ; il devient une reference historique et
technique a auditer en lecture seule pour reecrire un moteur EBTA natif.

Autorites :

- `Protocole/` reste l'autorite normative gelee en `EBTA-DOC-1.1`.
- `Implementation/ebta_engine/` reste la traduction executable subordonnee.
- `.ai/checkpoint.json` porte l'etat macro actif.
- `Implementation/Active/tracking.json` porte l'etat micro actif.

## Etat courant

`NATIVE_ENGINE_PHASE_8_COMPLETED` est atteint.

Phases -1 a 8 executees dans `Implementation/` :

- autorisation et lecture seule BACKTRADER tracees ;
- gouvernance BACKTRADER lue avant inventaire de code ;
- provenance XAUUSD/NASDAQ documentee depuis
  `D:\TRADING\ENTREPRISE\0 - Phase de lancement\Strategie de trading\0 - Backtest\Data` ;
- `Implementation/NATIVE_ENGINE_PROCEDURE_MAPPING.md` remplace le mapping
  moteur externe ;
- moteur natif MVP ajoute sous `Implementation/ebta_engine/` ;
- package reel genere sous `Implementation/research_packages/native_mvp` ;
- notebooks d'orchestration ajoutes sous `Implementation/notebooks/`.

## Prochaine action

Aucune action Phase -1 a Phase 8 restante.

Si le travail reprend, repartir de :

- `Implementation/research_packages/native_mvp` pour inspecter le package
  genere ;
- `Implementation/ebta_engine/package_builder/native_research_package.py` pour
  la verticale native ;
- `Implementation/notebooks/` pour le cockpit Jupyter.

## Blocages volontaires

Ne pas demarrer d'extension au-dela du MVP tant que :

- le package natif courant ne reste pas `PASS` avec `validate_package_dir()` ;
- la suite runtime complete ne reste pas `PASS` ;
- le gap licence/vendor des donnees locales n'est pas tranche si l'execution
  devient une recherche reelle et non un MVP d'architecture.

Decision humaine recue le 2026-07-02 : `1A, 2B, 3A`.
Elle autorise la lecture seule BACKTRADER, fixe la source de donnees MVP et
autorise les modifications `Implementation/` jusqu'a la Phase 8, sans toucher
`Protocole/`.

## Non-objectifs

- pas de modification de `Protocole/` ;
- pas de dependance runtime BACKTRADER ;
- pas de modification du repository BACKTRADER ;
- pas de notebook source de verdict ;
- pas d'ouverture OOS avant scellement ;
- pas de selection winner-only.

## Validations de reprise

```powershell
python -m json.tool .ai\checkpoint.json
python -m json.tool Implementation\Active\tracking.json
python -c "import json, jsonschema; jsonschema.validate(json.load(open('.ai/checkpoint.json', encoding='utf-8')), json.load(open('.ai/checkpoint.schema.json', encoding='utf-8')))"
python -c "import json, jsonschema; jsonschema.validate(json.load(open('Implementation/Active/tracking.json', encoding='utf-8')), json.load(open('Implementation/Active/tracking.schema.json', encoding='utf-8')))"
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
cd Implementation; python -m ebta_engine.package_builder.native_research_package
git diff --check -- .ai Implementation
```
