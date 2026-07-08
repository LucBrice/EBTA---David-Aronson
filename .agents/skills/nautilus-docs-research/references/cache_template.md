# Gabarit du fichier de cache

Ce gabarit décrit la structure attendue de
`Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md`. Le fichier est
créé au premier fait réel à consigner — pas à vide par anticipation.

## En-tête à utiliser pour la création initiale du fichier

```markdown
# Notes API NautilusTrader — faits vérifiés

Cache versionné de faits vérifiés sur l'API `nautilus_trader`, alimenté par
le skill `nautilus-docs-research`. Chaque entrée porte une version
`nautilus_trader` et une date — si la version installée diverge de celle
notée, re-vérifier avant de faire confiance à l'entrée (voir SKILL.md, étape
0). Ce fichier est un cache technique, pas une source normative EBTA :
`Protocole/` reste l'autorité, ce fichier ne documente que des faits d'API
Nautilus.

---
```

Puis une section par thème (mêmes thèmes que `doc_index.md` : Noyau &
Architecture, Données & Marché, Stratégie & Exécution, Comptabilité &
Portefeuille, Backtest/Reporting/Observabilité, Live & Intégrations), chacune
contenant une ou plusieurs entrées au format :

```markdown
### <Symbole ou question précise>

- **Fait vérifié** : <description précise ; signature exacte si applicable>
- **Version nautilus_trader** : <ex. 1.230.0>
- **Date** : <AAAA-MM-JJ>
- **Source** : <URL doc exacte> et/ou "vérifié par introspection sur package
  installé (scripts/introspect_nautilus.py)"
```

## Exemple rempli

```markdown
## Stratégie & Exécution

### OrderFactory.bracket()

- **Fait vérifié** : `OrderFactory.bracket()` existe et accepte
  `contingency_type`, des paramètres `tp_*` (take-profit) et `sl_*`
  (stop-loss) pour construire un ordre à jambes liées (entrée + SL + TP).
- **Version nautilus_trader** : 1.230.0
- **Date** : 2026-07-08
- **Source** : vérifié par introspection sur package installé
  (`scripts/introspect_nautilus.py nautilus_trader.trading.strategy.Strategy`,
  via `self.order_factory`) ; recoupé avec
  `https://nautilustrader.io/docs/latest/concepts/orders`

### OmsType.HEDGING

- **Fait vérifié** : `OmsType.HEDGING` est un membre d'énum réel dans
  `nautilus_trader.model.enums`, permettant des positions multiples
  concurrentes par instrument.
- **Version nautilus_trader** : 1.230.0
- **Date** : 2026-07-08
- **Source** : vérifié par introspection sur package installé
```

## Règle de mise à jour

Si une entrée existe déjà pour un symbole mais que la version installée a
changé : **modifier l'entrée en place** (nouvelle date, nouvelle version,
nouveau résultat), ne pas ajouter une deuxième entrée à côté de l'ancienne
pour le même symbole.

Une entrée qui n'a pu être vérifiée que par la documentation web (package non
installé dans l'environnement courant) doit porter la mention
`[NON VÉRIFIÉ EMPIRIQUEMENT]` juste après le titre de l'entrée.
