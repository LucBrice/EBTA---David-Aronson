# HOOK Actif : En attente

Le lot annexe `PLAN_IMPLEMENTATION_GOUVERNANCE_BIAIS_EBTA` est termine.

## Dernier lot valide

`Implementation/` encode maintenant le runtime G-BIAS subordonne a
`EBTA-DOC-1.1` :

- schemas et registre runtime des risques de biais ;
- logger d'incidents append-only ;
- checkers pre-OOS pour registre, famille candidate, metriques et robustesse ;
- guard OOS avec blocage pre-OOS et statut `BURNED` en cas d'acces non autorise ;
- gate transversal `G-BIAS` avec verdict `PASS`, `FAIL`, `INCONCLUSIVE` ou
  `BURNED` ;
- validation de paquet compatible via `reports/g_bias.json` ;
- pilote minimal generant un paquet `PASS` avec preuve G-BIAS.

## Validations du dernier lot

- `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation` : PASS, 87 tests.
- `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py` : PASS, package status PASS.
- Checkpoint et tracking JSON : syntaxe + schemas PASS.
- `git diff --check -- Implementation Protocole .ai` : PASS avec avertissements CRLF/LF uniquement.

## Prochaine etape

`STEP_3_BACKTRADER_INTEGRATION` reste pending.

Avant toute modification, lire la gouvernance BACKTRADER indiquee par
`.ai/checkpoint.json`, puis preparer un plan d'adaptation separant clairement
les contrats EBTA des conventions du moteur externe.
