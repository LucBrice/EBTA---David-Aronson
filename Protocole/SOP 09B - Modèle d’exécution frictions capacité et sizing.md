# SOP 09B — Modèle d’exécution, frictions, capacité et sizing
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 09B |
| Rôle dans le paquet EBTA | Execution, frictions, couts, capacite, sizing et NAV tradable. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## 1. Statut et objet

- **Statut :** spécification normative du moteur économique d’exécution.
- **Objet :** transformer les signaux et le sizing théorique en ordres, fills, positions, coûts, capacité et NAV réellement tradables.
- **Sorties :** alpha scientifique clairement étiqueté et stratégie économique nette complète.

Une preuve d’alpha avant coûts ne suffit jamais à autoriser le live.

---

## 2. Autorités normatives

La présente SOP consomme :

- les signaux gelés de la SOP 06 ;
- les timestamps et prix autorisés de la SOP 09A ;
- les séries et gates économiques de la SOP 08 ;
- les scénarios de robustesse de la SOP 05 ;
- les segments de la SOP 04.

Elle fournit les ordres, fills, positions, coûts, expositions et NAV utilisés par les SOP 07 et 08.

---

## 3. Séparation alpha et stratégie tradable

### 3.1 Alpha scientifique

Mesure du pouvoir prédictif, éventuellement avant certaines frictions, explicitement étiquetée et jamais présentée comme performance déployable.

### 3.2 Stratégie tradable

Performance réelle nette intégrant :

- chronologie ;
- spread ;
- slippage ;
- impact ;
- commissions et taxes ;
- borrow ;
- financement ;
- FX ;
- contraintes ;
- partial fills ;
- capacité.

Les deux séries restent séparées dans tous les rapports et gates.

---

## 4. Chronologie d’exécution

Chaque ordre conserve :

```text
observation_time
signal_time
decision_time
order_submission_time
earliest_fill_time
fill_time
valuation_time
```

L’ordre ne peut être rempli avant `earliest_fill_time`.

Toute donnée utilisée suit la SOP 09A.

---

## 5. Types d’ordre

Le projet préenregistre :

- types autorisés ;
- durée de vie ;
- conditions d’activation ;
- priorité ;
- comportement aux gaps ;
- annulation ;
- report ;
- modification ;
- règles de partial fill.

Changer de type d’ordre après observation crée une nouvelle candidate si la décision est influente.

---

## 6. Ordres market

Un ordre market est rempli :

- au premier prix exécutable après soumission ;
- du côté approprié du carnet ;
- avec spread ;
- slippage ;
- impact ;
- délai ;
- volume disponible.

Un fill au mid, au close ayant généré le signal ou au meilleur prix de barre est interdit comme hypothèse centrale.

---

## 7. Ordres limit

Un ordre limit n’est rempli que si :

1. la condition de prix est atteinte après soumission ;
2. le volume exécutable est suffisant ;
3. la priorité ou probabilité de fill préenregistrée le permet ;
4. les règles d’ambiguïté intrabar sont satisfaites.

Le résultat peut être :

- fill complet ;
- fill partiel ;
- non rempli ;
- expiré ;
- annulé ;
- reporté.

Toucher le prix limite dans une barre n’implique pas automatiquement un fill complet.

---

## 8. Ambiguïté OHLC

Lorsque l’ordre des événements intrabar n’est pas observable :

- utiliser des données plus fines ;
- ou appliquer une convention conservatrice préenregistrée ;
- ou classer le résultat non concluant si l’impact est matériel.

Choisir le chemin OHLC favorable est interdit.

---

## 9. Prix de fill et carnet

Le modèle utilise selon disponibilité :

- bid/ask ;
- trades ;
- profondeur ;
- volume ;
- spread ;
- volatilité ;
- heure ;
- latence ;
- sens ;
- taille de l’ordre.

Le prix théorique, le prix éligible et le prix effectivement simulé sont conservés séparément.

---

## 10. Commissions, taxes et frais

Inclure :

- frais fixes ;
- frais proportionnels ;
- minimum par ordre ;
- frais de bourse ;
- clearing ;
- taxes ;
- frais de conversion ;
- frais réglementaires ;
- rebates si réellement accessibles.

Les barèmes sont versionnés point-in-time par marché, instrument et période.

Utiliser le barème actuel sur tout l’historique est interdit.

---

## 11. Décomposition des frictions

Les composantes sont séparées :

$$
cost_t^{total}
=
commission_t
+tax_t
+spread_t
+slippage_t
+impact_t
+borrow_t
+financing_t
+fx_t.
$$

Le contrat évite de comptabiliser deux fois une même composante, notamment le spread dans le slippage ou l’impact.

---

## 12. Calibration du scénario central

Le scénario central utilise :

- observations historiques disponibles ;
- estimations point-in-time ;
- ou proxy conservateur documenté.

Le contrat précise :

- période de calibration ;
- séparation avec Test/OOS ;
- estimateur ;
- quantiles ;
- traitement des outliers ;
- date de gel ;
- limites d’extrapolation.

Les paramètres ne peuvent être choisis pour préserver l’edge après observation.

---

## 13. Données d’exécution insuffisantes

Lorsque bid/ask, volume, impact ou borrow sont incomplets :

- utiliser un proxy conservateur préenregistré ;
- exécuter des sensibilités ;
- limiter la portée ;
- ou produire `INCONCLUSIVE`/`NOT_VALIDATED` si le risque matériel ne peut être borné.

L’absence de données ne justifie jamais un coût nul.

---

## 14. Impact de marché

L’impact est une fonction monotone préenregistrée de variables pertinentes :

$$
impact
=
f\left(
\frac{Q}{ADV},
\sigma,
spread,
duration,
market\_state
\right).
$$

Le contrat fixe :

- formule ;
- paramètres ;
- unité ;
- bornes ;
- comportement hors domaine ;
- calibration ;
- stress.

L’impact nul pour tout ordre inférieur à 100 % de l’ADV est interdit.

---

## 15. Participation et liquidité

Définir par actif et fenêtre :

- ADV point-in-time ;
- volume disponible ;
- participation moyenne maximale ;
- participation instantanée maximale ;
- nombre de jours d’entrée/sortie ;
- concentration dans le volume ;
- âge des données ;
- règle en marché fermé ou suspendu.

Les plafonds sont appliqués avant le fill.

Utiliser le volume futur est interdit.

---

## 16. Courbe de capacité

Évaluer au minimum :

- capital minimal ;
- capital de départ ;
- capital cible ;
- capital stressé ;
- points intermédiaires matériels.

Pour chaque capital, recalculer endogènement :

- quantités ;
- participation ;
- durée ;
- fills ;
- impact ;
- coûts ;
- contraintes ;
- performance nette ;
- risque.

Multiplier linéairement un P&L de petit capital n’est pas une analyse de capacité.

---

## 17. Capacité maximale

La capacité maximale est le plus grand capital pour lequel tous les gates restent satisfaits :

- hurdle économique ;
- liquidité ;
- délai ;
- participation ;
- drawdown ;
- marge ;
- concentration ;
- exécutabilité.

Le capital cible doit être inférieur ou égal à cette capacité validée.

---

## 18. Ventes à découvert

Le modèle inclut :

- disponibilité d’emprunt ;
- borrow fee ;
- hard-to-borrow ;
- recall ;
- dividendes dus ;
- interdictions ;
- règles locales ;
- squeeze ;
- gaps ;
- impossibilité de maintenir la position.

La disponibilité n’est jamais supposée universelle.

---

## 19. Borrow inconnu

Si le short est matériel et l’historique de borrow indisponible :

- appliquer un proxy conservateur ;
- tester une indisponibilité partielle ou totale ;
- limiter l’univers ;
- ou produire `INCONCLUSIVE`.

Une portée explicitement long-only peut rendre le test de borrow `NOT_APPLICABLE`.

---

## 20. Financement, cash et marge

Inclure par devise :

- rémunération du cash accessible ;
- coût du levier ;
- taux débiteur ;
- coût overnight ;
- marge initiale et maintenance ;
- haircuts ;
- appels de marge ;
- liquidation forcée ;
- collatéral.

Les taux sont point-in-time ou issus d’un proxy conservateur documenté.

---

## 21. Conversion FX

Chaque jour :

- positions ;
- P&L ;
- cash ;
- coûts ;
- financement

sont convertis dans la devise de base avec un taux point-in-time et les spreads/frais applicables.

Une conversion au dernier taux de l’échantillon est interdite.

---

## 22. Sizing causal

La règle de sizing est préenregistrée et utilise uniquement les informations disponibles avant l’ordre.

Elle définit :

- méthode ;
- capital de référence ;
- risque cible ;
- estimateur ;
- fenêtre ;
- lag ;
- fallback ;
- plafonds ;
- arrondis ;
- minimums ;
- comportement en données manquantes.

Utiliser la volatilité future réalisée est interdit.

---

## 23. Volatility targeting

Un sizing à volatilité cible utilise un estimateur rolling ou expanding point-in-time, laggé.

Le contrat fixe :

- fenêtre ;
- poids ;
- minimum d’observations ;
- plancher/plafond de volatilité ;
- levier maximal ;
- fallback ;
- fréquence de mise à jour.

Une cible modifiée après drawdown sans règle préenregistrée crée une nouvelle version.

---

## 24. Signaux simultanés

Les signaux concurrents sont traités par une règle mécanique :

- scores ;
- priorités ;
- allocation ;
- normalisation ;
- budget de risque ;
- contraintes ;
- tie-break canonique.

Les contraintes sont appliquées conjointement avant la création des ordres.

Remplir intégralement chaque signal comme s’il disposait du capital total est interdit.

---

## 25. Arrondis et minimums

Avant le fill, appliquer :

- lot size ;
- tick size ;
- notionnel minimal ;
- unité contractuelle ;
- fractionnement autorisé ;
- précision ;
- cash résiduel.

Les quantités théoriques et exécutables sont conservées séparément.

---

## 26. Ordre des opérations portefeuille

```text
1. Signaux
2. Scores
3. Sizing théorique
4. Contraintes conjointes
5. Quantités exécutables et arrondis
6. Ordres
7. Fills
8. Positions réalisées
9. Coûts et financement
10. P&L et NAV
```

Les contraintes ne peuvent être appliquées après le calcul du P&L.

---

## 27. Contraintes de portefeuille

Appliquer avant soumission :

- capital ;
- exposition brute et nette ;
- levier ;
- marge ;
- concentration ;
- secteur ;
- actif ;
- corrélation ;
- liquidité ;
- turnover ;
- borrow ;
- capacité.

Le moteur enregistre les signaux rejetés ou réduits et la raison.

---

## 28. Partial fills

Chaque ordre possède un état :

```text
CREATED
SUBMITTED
PARTIALLY_FILLED
FILLED
CANCELLED
EXPIRED
REJECTED
```

Conserver :

- quantité demandée ;
- quantité exécutée ;
- prix ;
- reliquat ;
- temps ;
- priorité ;
- durée de vie ;
- annulation/report ;
- effet sur le signal suivant.

Un partial fill ne devient jamais un fill complet dans la comptabilité.

---

## 29. Ordres non remplis

Un ordre non rempli :

- ne modifie pas la position ;
- reste dans le journal ;
- produit une opportunité manquée ;
- suit la politique d’expiration ou de report ;
- peut influencer les contraintes futures uniquement selon la règle préenregistrée.

Il ne peut être rempli rétroactivement au prix théorique.

---

## 30. Scénario central et stress

Le scénario central est déjà réaliste.

Les stress de la SOP 05 couvrent notamment :

- spread défavorable ;
- latence ;
- volume réduit ;
- impact supérieur ;
- coûts ;
- borrow indisponible ;
- gaps ;
- financement ;
- participation réduite.

Un scénario extrême ne répare pas un scénario central optimiste.

---

## 31. Population de recherche

Une variante de :

- coût ;
- fill ;
- type d’ordre ;
- sizing ;
- contrainte ;
- participation ;
- impact

appartient à l’effort de recherche si elle influence la sélection ou l’ouverture OOS.

Changer ces éléments après Test crée une nouvelle candidate/version.

Un changement fondé sur OOS ne peut être revalidé sur le même OOS.

---

## 32. Gate économique

### `PASS`

- chronologie réalisable ;
- fills plausibles ;
- coûts complets ;
- rendement net au-dessus du hurdle ;
- capacité au moins égale au capital cible ;
- contraintes respectées ;
- scénarios bloquants satisfaits ;
- réconciliation valide.

### `REJECTED_ECONOMIC`

Le gate statistique applicable est satisfait, mais un hurdle économique, de risque, capacité ou exécutabilité échoue.

### `FAIL`

- look-ahead d’exécution ;
- fill impossible présenté comme réel ;
- coûts omis ;
- violation méthodologique ;
- dépendance à une exécution parfaite ;
- comptabilité falsifiée.

### `INCONCLUSIVE`

- impact matériel non calibrable ;
- borrow matériel inconnu ;
- données de volume/spread non fiables ;
- modèle stochastique hors tolérance.

---

## 33. Réconciliation

Dans les tolérances préenregistrées :

- ordres expliquent les fills ;
- fills expliquent les positions ;
- positions expliquent le P&L brut ;
- coûts, financement et FX expliquent le P&L net ;
- cash et flux expliquent la NAV ;
- contraintes expliquent les quantités rejetées.

Un total final proche sans chaîne de réconciliation n’est pas suffisant.

---

## 34. Non-déterminisme

Pour un modèle de fill ou d’impact stochastique :

- générateur ;
- algorithme ;
- seed ;
- ordre ;
- réplications ;
- tolérance ;
- règle d’agrégation

sont préenregistrés.

Changer de seed jusqu’à obtenir un résultat favorable est interdit.

---

## 35. Tests obligatoires

Les tests couvrent :

- frontières temporelles ;
- market, limit, stop et types autorisés ;
- gaps ;
- ambiguïtés OHLC ;
- spread et slippage ;
- impact ;
- commissions/minimums ;
- partial/no fills ;
- annulations ;
- sizing ;
- signaux simultanés ;
- contraintes ;
- short/borrow ;
- financement ;
- FX ;
- marge ;
- arrondis ;
- réconciliation ;
- déterminisme.

---

## 36. Livrable obligatoire

```text
[EXECUTION CONTRACT]
strategy_version:
market:
timezone:
order_types:
timing_rule:
fill_rule_version:

[COST MODEL]
commission_schedule:
spread_model:
slippage_model:
impact_model:
borrow_model:
financing_model:
fx_model:
calibration_period:

[SIZING]
sizing_method:
risk_target:
estimator:
lookback:
lag:
limits:
rounding:

[CAPACITY]
capital_grid:
participation_limits:
capacity_max:
target_capital:

[JOURNALS]
orders_path:
fills_path:
positions_path:
costs_path:
nav_path:
hashes:

[GATES]
execution_status:
economic_status:
capacity_status:
reconciliation_status:
reviewer:
```

---

## 37. Erreurs interdites

- Fill au close ayant produit le signal.
- Fill limit automatique au simple toucher.
- Choix favorable d’un chemin intrabar.
- Coût central nul ou optimiste.
- Double comptage du spread.
- Impact indépendant de la taille.
- Volume futur.
- Borrow universel.
- Volatilité future dans le sizing.
- Somme de backtests incompatibles.
- Partial fill traité comme complet.
- Changement de modèle après OOS.

---

## 38. Sources internes

- `Notes/4-L'Intégrité du Backtesting Biais d'Anticipation et Coûts Réels.md`
- `Notes/152-L'Efficience des Marchés et les Primes de Risque Professionnel.md`
- `Notes/153-La Taxonomie des Quatre Primes de Risque Financières.md`
- `Notes/154-L'Art de Capturer les Primes de Risque Financières.md`
- `Notes/155-La Prime de Risque Action Moteur du Rendement Boursier.md`
- `Notes/156-La prime de risque l'assurance du suivi de tendance.md`
- `Notes/157-La Prime de Liquidité Salaire du Risque et Contre-Tendance.md`
- `Notes/161-Protocole EBTA La Science de l’Analyse Technique Objective.md`

---

## 39. Décision méthodologique synthétique

> **SOP 09B transforme les signaux en un portefeuille réellement tradable par une chaîne causale signal–ordre–fill–position–P&L. Le scénario central intègre des prix exécutables, tous les coûts, l’impact, la capacité, le borrow, le financement, le FX, le sizing et les contraintes. La capacité est recalculée sur une grille de capitaux et le capital cible ne peut dépasser le plus grand niveau où tous les gates restent satisfaits. Les partial fills, rejets et opportunités manquées restent dans le journal. Toute variante influente appartient à la recherche et aucun changement fondé sur OOS ne peut être revalidé sur ce même OOS.**
