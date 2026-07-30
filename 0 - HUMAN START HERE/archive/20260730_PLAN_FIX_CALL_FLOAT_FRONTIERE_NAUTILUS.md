# Brouillon — supprimer le repli silencieux de `_call_float`

## Intention

Corriger le défaut confirmé dans
`Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py::_call_float` :
une exception de l'API Nautilus ou une valeur non convertible est actuellement
transformée en `0.0`, valeur métier plausible ensuite enregistrée dans les
snapshots NAV/exposition.

La décision humaine D3 du 2026-07-29 autorise un chantier `fix` séparé.

## État réel vérifié

- `_record_nav_snapshot()` appelle `_call_float()` pour
  `Portfolio.equity(venue)` et `Portfolio.net_exposure(instrument_id)`.
- `_call_float()` capture aujourd'hui toute exception d'appel et de conversion,
  puis retourne `0.0`.
- Le cache `NAUTILUS_API_NOTES.md` et l'introspection locale confirment
  `Portfolio.equity` et `Portfolio.net_exposure` avec
  `nautilus_trader==1.230.0`.
- Le support du mapping monodevise `{Currency: Money}` existe déjà et doit être
  conservé.
- Le changement est un `ADAPTER_MAPPING` correctif. Il ne modifie aucun seuil,
  gate, statut, verdict ni ordre méthodologique EBTA.

## Résultat attendu

1. Une exception levée par une méthode Nautilus traverse la frontière sous
   forme d'un `RuntimeError` contextualisé par le nom de méthode, avec
   chaînage de la cause originale ; elle ne devient jamais `0.0`.
2. Une valeur absente ou non convertible produit également un `RuntimeError`
   contextualisé ; toutes les défaillances d'extraction partagent ainsi un
   contrat unique à la frontière.
3. Une valeur numérique directe et un mapping monodevise valide restent
   convertis en `float`.
4. Un mapping vide ou multidevise ambigu est refusé explicitement.
5. Une valeur `NaN` ou infinie est refusée : un nombre non fini ne constitue
   pas une mesure NAV/exposition exploitable.
6. `_record_nav_snapshot()` n'ajoute aucun snapshot lorsque l'extraction
   d'equity ou d'exposition échoue.

## Portée proposée

Fichiers modifiables :

- `Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py`
- `Implementation/ebta_engine/tests/test_nautilus_phase4_strategy_costs.py`
- `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`
- le futur plan `fix` et les fichiers mécaniques du cockpit gérés par
  `plan.ps1`

Hors portée :

- `Protocole/`
- les seuils, gates et verdicts EBTA
- `nautilus_mapping.py`, les schémas et les package builders
- toute valeur de remplacement inventée (`0.0`, `NaN`, `None`)
- toute modification de BACKTRADER

## Vérifications minimales

- test dédié exécuté dans le venv Nautilus couvrant valeur directe, mapping
  monodevise, exception d'appel avec cause chaînée, valeur absente/invalide/non
  finie, mapping vide/multidevise et absence de snapshot partiel par appel
  direct de `GenericPayloadStrategy._record_nav_snapshot()` sur un double
  minimal ;
- commande ciblée :
  `python -m unittest Implementation.ebta_engine.tests.test_nautilus_phase4_strategy_costs` ;
- suite complète :
  `python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation` ;
- Pyrefly sur le bridge et le test touchés ;
- `adversarial-tester`, `bug-hunter`, `EBTA_Protocol_Guardian` et
  `plan-conformance-audit` avant clôture ;
- `git diff --check`.

## Journal de convergence `/evaluate`

| Passe | Résultat | Corrections |
| --- | --- | --- |
| 1 | Angles morts corrigés | Type d'erreur et cause chaînée figés ; rejet des nombres non finis ; preuve directe d'atomicité du snapshot ajoutée. |
| 2 | Convergence | Contrat d'erreur uniformisé et commande de régression ciblée rendue explicite ; aucun nouvel angle mort majeur. |
