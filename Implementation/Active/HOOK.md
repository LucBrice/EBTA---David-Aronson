# HOOK Actif : En attente

Le lot `STEP_2B_STRATEGIE_ACTIF_RUNTIME` est termine.

## Dernier lot valide

`Implementation/` encode maintenant la clarification `strategie x actif` :

- `asset_universe` et `asset_selection_axis` dans le search space ;
- comptage des candidates par actif ;
- matrice candidate avec mapping candidat-actif ;
- `INV-017` pour rejeter une WRC incomplete par couple `strategie x actif` ;
- fixture pilote multi-actifs validee.

## Prochaine etape

`STEP_3_BACKTRADER_INTEGRATION` reste pending.

Avant toute modification, lire la gouvernance BACKTRADER indiquee par
`.ai/current_plan.md`, puis preparer un plan d'adaptation separant clairement
les contrats EBTA des conventions du moteur externe.
