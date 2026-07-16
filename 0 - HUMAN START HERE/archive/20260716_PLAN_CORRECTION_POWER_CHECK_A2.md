# Brouillon d'intake — Lot A2 : calcul reel de puissance atteinte pour G9 `power_check`

## Constat verifie dans le code reel

Le chantier parent `.ai/backlog/fixes/EPIC_CLOTURE_ATTESTATIONS_RESIDUELLES_GATES.md`
pointe maintenant vers le Lot A2 apres cloture du Lot C (`4e568c5`).

Verification directe 2026-07-16 :

- `Implementation/ebta_engine/procedures/oos_confidence_interval.py::oos_confidence_interval()`
  expose un parametre `power: float = 0.80`.
- La fonction appelle ensuite
  `validate_power_target(power, target_power=0.80)`.
- Aucun appelant courant ne passe `power=` explicitement (`rg power_check|power=`
  ne trouve que les tests et la signature).
- Dans le pipeline pilote, `_procedure_reports()` appelle
  `oos_confidence_interval(...)` sans `power=`.

Effet : `power_check.status` peut passer par construction, car le defaut
`0.80` est valide contre la cible `0.80`. Ce n'est pas un branchement
mecanique comme Lot C ; c'est un calcul manquant.

## Source normative

- `Protocole/SOP 01 - Estimation et intervalle de confiance OOS.md`
  indique que le gate statistique exige une puissance preenregistree d'au
  moins 80 %.
- La section 10.6 precise que l'effet minimal detectible est derive du
  rendement annuel minimal exige par le gate economique :

```text
delta_jour = ln(1 + R_annuel_min) / A
```

- La meme section impose une estimation prudente de la variance long terme,
  tenant compte de l'autocorrelation, calculee exclusivement sur les donnees
  de developpement disponibles avant l'OOS.
- Decision humaine deja actee dans l'EPIC parent : reutiliser le bootstrap
  stationnaire par blocs deja normatif (`procedures/bootstrap.py`) applique
  aux rendements pre-OOS de developpement pour estimer l'erreur type de la
  puissance atteinte.

## Perimetre pressenti

Fichiers probablement a modifier :

- `Implementation/ebta_engine/procedures/oos_confidence_interval.py`
  pour calculer une puissance atteinte reelle au lieu de relayer le defaut
  `power=0.80`.
- `Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
  pour fournir a la procedure OOS les rendements pre-OOS de developpement et
  les seuils economiques preregistres deja presents dans `pilot_inputs`.
- `Implementation/examples/minimal_pilot_pipeline/inputs/pilot_inputs.json`
  pour exposer explicitement une serie de rendements pre-OOS de developpement
  utilisable pour l'estimation de variance long terme, plutot que de reutiliser
  une serie OOS ou un score de selection qui n'a pas la meme signification.
- `Implementation/ebta_engine/tests/test_procedure_oos_ci.py`
  pour couvrir la puissance calculee, le cas insuffisant et l'absence de
  fuite OOS dans l'estimation de variance.
- `Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py`
  pour prouver que `gates["power_report"]` derive du
  `oos["power_check"]["status"]` apres calcul reel.

Fichiers interdits :

- `Protocole/` : aucune modification normative.
- `Implementation/ebta_engine/validators/gate_validator.py` : ne pas etendre
  les valeurs de verdict ni la logique de gate.
- `Implementation/ebta_engine/procedures/bootstrap.py` : helper deja
  suffisant, a reutiliser sans le reimplementer.
- Lot B / G6 : hors perimetre, decision humaine de seuil encore manquante.

## Proposition technique initiale

Ajouter un calcul explicite de puissance base sur :

1. `minimum_detectable_daily_effect = log1p(min_annualized_return) / sessions_per_year`,
   ou `min_annualized_return` provient des seuils economiques preregistres.
2. Une estimation bootstrap stationnaire de l'erreur type de la moyenne sur
   la serie pre-OOS de developpement, en reutilisant
   `stationary_block_indices()`.
3. Une conversion de cette erreur type pre-OOS en variance long terme, puis
   une projection sur la taille de la serie OOS globale effectivement
   evaluee. Le bootstrap pre-OOS sert a estimer la dependance et la variance,
   pas a substituer la taille d'echantillon de developpement a la taille OOS.
4. Une approximation normale prudente pour la puissance unilaterale avec
   `statistics.NormalDist` (stdlib, aucune dependance nouvelle) :

```text
se_oos_mean = long_run_std_error / sqrt(oos_observation_count)
z_effect = minimum_detectable_daily_effect / se_oos_mean
achieved_power = Phi(z_effect - z_alpha)
```

avec `alpha = 0.05` pour rester aligne avec le gate statistique existant.

Points a figer dans le plan restructure :

- refuser ou rendre `INCONCLUSIVE` si la serie pre-OOS est absente ou trop
  courte pour estimer une erreur type defendable ;
- ne jamais utiliser `oos_returns` pour estimer la variance long terme de
  puissance ;
- conserver `validate_power_target()` comme validateur de cible, mais lui
  passer une puissance calculee ;
- transmettre cette puissance calculee a `_statistical_verdict()` pour que
  le verdict statistique global reste coherent avec la condition de puissance ;
- corriger le raccord du Lot A1 : `oos_report`, `concatenated_oos_series` et
  `oos_bootstrap_report` peuvent continuer a reflechir le verdict statistique
  global, mais `power_report` doit refleter `oos["power_check"]["status"]`.
  Sinon un `power_check` reellement `INCONCLUSIVE` resterait masque par le
  statut global derive d'une autre condition ;
- eviter qu'un ancien appel passant `power=` continue a produire un `PASS`
  silencieux : soit retirer ce parametre, soit le rendre explicitement
  deprecie/ignore avec tests de non-regression ;
- faire apparaitre dans le rapport `power_check` les entrees factuelles :
  cible, puissance atteinte, MDE quotidien, source de variance, taille
  d'echantillon pre-OOS, taille OOS, nombre de blocs distincts et parametres
  bootstrap.

## Audit `/evaluate` — passe 1

Pertinence : valide sous reserve de correction.
Risque : modere, car le chantier touche une condition de gate statistique.
Cohérence avec l'existant : bonne, si le code reutilise `stationary_block_indices()`
et `statistics.NormalDist` sans dependance nouvelle.

Angle mort corrige dans ce brouillon :

- La version initiale parlait d'une erreur type bootstrap pre-OOS sans
  distinguer l'echantillon de developpement et la taille OOS evaluee. Cela
  aurait pu calculer la puissance avec le mauvais `n`.
- Correction : le plan doit estimer une variance long terme depuis les
  rendements pre-OOS, puis projeter l'erreur type de la moyenne sur
  `oos_observation_count`.

Points de vigilance restant a figer dans le plan restructure :

- Source explicite des rendements pre-OOS dans `pilot_inputs.json`.
- Aucun usage de `oos_returns` pour estimer la variance de puissance.
- Comportement des anciens appels avec `power=` : interdire le faux `PASS`
  par defaut.

## Audit `/evaluate` — passe 2

Pertinence : valide apres correction du raccord G9.
Risque : modere mais borne par des tests unitaires et d'integration simples.
Cohérence avec l'existant : bonne, a condition de ne pas rouvrir G9 hors du
champ `power_report`.

Angle mort corrige dans cette passe :

- Le brouillon ne distinguait pas assez le verdict statistique global
  (`oos["statistical_gate"]`) du sous-controle de puissance
  (`oos["power_check"]["status"]`). Depuis Lot A1, les quatre champs G9
  suivent le meme `oos_gate_value`; A2 doit specialiser `power_report` pour
  ne plus masquer un echec de puissance.

Convergence :

- Aucun nouveau verrou humain n'est identifie : la methode bootstrap
  stationnaire sur rendements pre-OOS est deja actee dans l'EPIC.
- Le plan restructure peut etre redige avec une liste fermee de fichiers et
  des tests binaires.

## Critere de sortie attendu

- `power_check.status` derive d'une puissance calculee, jamais du parametre
  `power` par defaut.
- `gates["power_report"]` reflete ce statut calcule.
- La suite runtime complete reste `PASS`.
- Si le package M1 ou le pilote devient `INCONCLUSIVE`, ce resultat est
  traite comme un verdict EBTA legitime et documente, pas comme une regression.
