# SOP 07 — Detrending, benchmark et zero-centering
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 07 |
| Rôle dans le paquet EBTA | Flux signal/evaluation, detrending, benchmark, cash et zero-centering. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## 1. Statut et objet

- **Statut :** spécification normative des transformations d’évaluation.
- **Périmètre :** Train, Test et OOS, avec règles distinctes selon leur fonction.
- **Principe :** le flux de signal utilise exclusivement l’information réellement disponible ; les transformations ex post restent dans le flux d’évaluation.

Cette SOP sépare trois opérations :

1. detrending du drift de marché ;
2. mesure relative au cash, à un benchmark ou à un hurdle ;
3. zero-centering utilisé pour construire l’hypothèse nulle des tests bootstrap.

Ces opérations ne sont ni synonymes ni interchangeables.

---

## 2. Autorités normatives

La présente SOP applique :

- l’estimand OOS de la SOP 01 ;
- la matrice et le WRC de la SOP 02 ;
- les segments de la SOP 04 ;
- les séries de rendement de la SOP 08 ;
- les conventions point-in-time de la SOP 09A ;
- les coûts, expositions et conversions de la SOP 09B.

La SOP 07 ne définit ni les signaux, ni le sizing, ni les fills.

---

## 3. Séparation obligatoire des flux

### 3.1 Flux signal

Il contient uniquement :

- prix observables ;
- volumes ;
- fondamentaux et macro point-in-time ;
- corporate actions connues ;
- univers disponible ;
- états de portefeuille connus ;
- transformations apprises exclusivement sur les données autorisées.

### 3.2 Flux évaluation

Il contient :

- positions déjà déterminées ;
- rendements de marché ;
- cash et financement ;
- coûts ;
- expositions ;
- benchmarks ;
- transformations de detrending ;
- séries utilisées par l’inférence.

### 3.3 Invariant

> Activer, désactiver ou modifier le flux d’évaluation detrendé ne doit modifier aucun signal, ordre ou sizing.

La vérification doit être déterministe, idéalement bit-à-bit.

---

## 4. Contrat de rendement

La fréquence primaire est quotidienne conformément aux SOP 01 et 08.

Pour un actif :

$$
r_t^{market}=\log\left(\frac{P_t}{P_{t-1}}\right).
$$

Le contrat précise :

- source et champ de prix ;
- ajustement total return ;
- horizon `close-to-close`, `open-to-open` ou autre ;
- timestamp de disponibilité ;
- première position applicable ;
- devise ;
- calendrier ;
- traitement des corporate actions.

Il est interdit d’appliquer un drift `close-to-close` à un P&L `open-to-open` sans correspondance exacte.

---

## 5. Position et anti-lookahead

Si le rendement réalisé pendant la période `t` est `r_t`, l’exposition `e_t` ou la position `s_{t-1}` doit avoir été déterminée avant cette période.

Pour une règle binaire :

$$
a_t=s_{t-1}\left(r_t^{market}-\bar r_S^{market}\right).
$$

Pour une exposition fractionnelle, l’exposition effective décidée avant le rendement est utilisée directement.

---

## 6. Estimand primaire avec cash

L’estimand statistique primaire est celui de la SOP 01 :

$$
d_t=
r_t^{strat,net}
-r_t^{cash}
-e_t\left(
\bar r_S^{market}
-\bar r_S^{cash}
\right).
$$

où :

- `r_t^{strat,net}` est le log-rendement quotidien réel net ;
- `r_t^{cash}` est le log-rendement du cash réellement accessible ;
- `e_t` est l’exposition effective au marché ;
- les moyennes sont estimées sur le segment d’évaluation `S`.

Cette formule :

- neutralise le rendement du cash dans le gate statistique ;
- retire le drift excédentaire du marché proportionnellement à l’exposition ;
- évite une double soustraction du taux sans risque ;
- conserve le cash réel dans la sortie économique.

Le hurdle statistique primaire est :

$$
h_s=0.
$$

---

## 7. Interprétation

Le detrending évalue si la règle choisit mieux les périodes d’exposition qu’une exposition non informative profitant seulement au drift moyen.

Il ne démontre pas à lui seul :

- la rentabilité réelle après coûts ;
- la capacité ;
- l’exécutabilité ;
- la supériorité à un benchmark institutionnel ;
- la stabilité future du drift.

La performance économique réelle reste une sortie distincte de la SOP 08.

---

## 8. Estimation du drift par segment

Le drift est estimé uniquement sur le segment dont la performance est évaluée.

### 8.1 `Train_k`

Pour les scores Train, utiliser exclusivement `Train_k`.

### 8.2 `Test_k`

Pour le WRC local, estimer séparément le drift dans `Test_k`. Aucun point hors de `Test_k` n’entre dans ce calcul.

### 8.3 OOS global

Pour l’estimation confirmatoire :

- concaténer chronologiquement tous les `OOS_k` selon la SOP 04 ;
- estimer une seule fois le drift sur cette série OOS globale ;
- appliquer la formule de la section 6 ;
- ne jamais utiliser ce drift pour modifier les folds.

### 8.4 Analyse locale d’un `OOS_k`

Une estimation locale est descriptive. Elle ne remplace pas le verdict fondé sur l’OOS concaténé et n’autorise aucune adaptation.

---

## 9. Caractère ex post du detrending

L’estimation de la moyenne sur le segment complet est une transformation d’évaluation ex post permise par la méthode d’Aronson, à condition que :

- les positions soient déjà figées ;
- le drift ne soit jamais une feature ;
- le drift ne modifie aucun ordre, fill ou sizing ;
- l’objet soit clairement distingué d’un benchmark disponible en temps réel.

Pour le reporting déployable, publier en parallèle la série économique fondée sur des informations point-in-time.

---

## 10. Multi-actifs

Pour `M` actifs :

$$
d_t=
r_t^{strat,net}
-r_t^{cash}
-\sum_{i=1}^{M}
e_{i,t}
\left(
\bar r_{i,S}^{market}
-\bar r_S^{cash}
\right).
$$

Le drift est estimé séparément pour chaque actif sur les périodes correspondant exactement à ses contributions de P&L.

Une autre convention est admissible uniquement si elle est préenregistrée et justifiée :

- benchmark commun ;
- modèle factoriel point-in-time ;
- benchmark de portefeuille.

Soustraire le drift d’un indice unique à tous les actifs sans justification est interdit.

---

## 11. Multidevise

Le contrat précise :

- devise de base ;
- taux FX point-in-time ;
- soldes cash par devise ;
- financement ;
- coûts et spreads FX ;
- heure de conversion ;
- traitement des jours non ouvrés.

Les P&L, coûts, cash et expositions sont convertis quotidiennement dans la devise de base avant le calcul de la série portefeuille.

Utiliser un taux de change final pour convertir rétroactivement l’historique est interdit.

---

## 12. Cash et non-déploiement

Le cash de référence est le rendement réellement accessible dans la devise concernée, net des frais et contraintes.

Un taux théorique peut être utilisé seulement comme approximation conservatrice préenregistrée.

Les jours et segments sans déploiement :

- restent dans la chronologie ;
- conservent le rendement économique réel du cash et les coûts ;
- ont une contribution statistique nulle en l’absence d’autre P&L, après neutralisation du cash.

---

## 13. Benchmark et hurdle

Trois séries doivent rester distinctes.

### 13.1 Alpha detrendé

Série primaire pour l’inférence EBTA, définie à la section 6.

### 13.2 Performance relative à un benchmark

$$
b_t=r_t^{strat,net}-r_t^{benchmark}.
$$

Le benchmark doit être disponible ou reconstructible point-in-time.

### 13.3 Performance économique

Log-rendement réel net de la stratégie, incluant cash, coûts, financement et contraintes.

Le projet peut publier les trois, mais ne peut choisir après les résultats laquelle sert de série primaire.

---

## 14. Coûts et ordre des opérations

L’ordre normatif est :

```text
1. Charger les données point-in-time
2. Générer les signaux
3. Produire les positions/expositions causales
4. Simuler les ordres et fills
5. Construire le rendement économique net
6. Calculer cash et rendements de marché cohérents
7. Appliquer le detrending pondéré par exposition
8. Produire d_t
9. Pour H0 uniquement, zero-center chaque colonne
10. Rééchantillonner conjointement
```

Le zero-centering ne peut pas précéder l’intégration des coûts applicables à la statistique testée.

Une sortie avant coûts peut être publiée comme diagnostic scientifique. Toute autorisation de déploiement exige la sortie nette et le gate économique.

---

## 15. Zero-centering

Pour chaque candidate `m` sur le segment Test applicable :

$$
\bar d_m=\frac{1}{T}\sum_{t=1}^{T}d_{t,m},
$$

$$
\tilde d_{t,m}=d_{t,m}-\bar d_m.
$$

Le zero-centering :

- s’applique séparément à chaque candidate ;
- intervient après la construction de `d_{t,m}` ;
- conserve la dispersion et la dépendance ;
- impose l’hypothèse nulle dans les réplications bootstrap ;
- n’est jamais utilisé pour l’estimation ponctuelle.

---

## 16. Bootstrap conjoint

Les mêmes indices temporels de rééchantillonnage sont appliqués à toutes les colonnes.

Cette synchronisation conserve :

- la dépendance temporelle prévue par le bootstrap ;
- les corrélations contemporaines entre candidates ;
- la distribution du maximum.

Rééchantillonner chaque candidate avec des indices indépendants est interdit.

---

## 17. Interdiction du zero-centering OOS

La série OOS utilisée pour l’estimation et l’intervalle de confiance :

- n’est pas zero-centered ;
- conserve sa moyenne observée ;
- n’utilise pas la distribution du maximum WRC ;
- suit exclusivement la SOP 01.

Zero-center l’OOS détruirait précisément le paramètre à estimer.

---

## 18. Double centrage

Le detrending et le zero-centering sont deux transformations différentes :

- le detrending retire le drift de marché pondéré par exposition ;
- le zero-centering retire la moyenne de chaque série candidate afin de simuler `H0`.

Les appliquer dans cet ordre est valide.

Soustraire deux fois le même cash, benchmark, drift ou moyenne par erreur est interdit.

---

## 19. Corporate actions et données de référence

Les rendements utilisent une convention cohérente avec :

- splits ;
- dividendes ;
- fusions ;
- spin-offs ;
- delistings ;
- total return.

Une incohérence matérielle ou non reconstructible produit `INCONCLUSIVE` jusqu’à correction selon la SOP 09A.

---

## 20. Contrôles numériques

Vérifier :

- moyenne du rendement de marché detrendé dans la tolérance de zéro ;
- moyenne de chaque colonne zero-centered dans la tolérance de zéro ;
- variance non modifiée au-delà de la tolérance numérique ;
- timestamps et nombre de lignes conservés ;
- positions identiques avec et sans flux d’évaluation ;
- cohérence actif/horizon/prix ;
- absence de valeurs futures ;
- réconciliation avec les séries de la SOP 08.

La tolérance absolue et relative est préenregistrée selon la précision numérique. Une égalité flottante universelle exacte n’est pas exigée.

---

## 21. Données ou benchmark indisponibles

Une politique préenregistrée peut prévoir :

- exclusion traçable ;
- proxy conservateur ;
- blocage du calcul ;
- statut non concluant.

Si la série primaire ne peut pas être reconstruite, le verdict est `INCONCLUSIVE` ou `NOT_VALIDATED`, jamais `PASS`.

Changer de benchmark après observation crée une nouvelle spécification et ne restaure pas la virginité des données.

---

## 22. Statuts

### `PASS`

- flux signal et évaluation séparés ;
- contrat de rendement complet ;
- formule cash/exposition conforme ;
- drift estimé sur le bon segment ;
- benchmark préenregistré ;
- zero-centering réservé à `H0` ;
- contrôles numériques satisfaits.

### `FAIL`

- information future dans le signal ;
- drift futur utilisé pour décider ;
- double comptage ;
- benchmark modifié après observation ;
- série économique confondue avec alpha detrendé ;
- OOS zero-centered ;
- indices bootstrap non conjoints.

### `INCONCLUSIVE`

- prix ou corporate actions non reconstructibles ;
- cash/benchmark matériel indisponible ;
- méthode historique inconnue ;
- tolérances numériques dépassées sans cause identifiée.

---

## 23. Livrable obligatoire

```text
[RETURN CONTRACT]
frequency:
price_field:
return_horizon:
valuation_time:
base_currency:

[DETRENDING]
segment_id:
market_series:
cash_series:
exposure_series:
market_drift:
cash_drift:
formula_version:

[BENCHMARK]
benchmark_id:
availability_rule:
hurdle_statistical:
hurdle_economic:

[ZERO_CENTERING]
candidate_matrix_hash:
column_means:
tolerance_abs:
tolerance_rel:
joint_bootstrap:

[OUTPUTS]
economic_return_path:
detrended_return_path:
benchmark_relative_path:
zero_centered_matrix_path:
hashes:
```

Conserver les séries avant et après chaque transformation.

---

## 24. Erreurs interdites

- Utiliser des prix detrendés comme features.
- Employer une exposition connue après le rendement.
- Detrender sur une période future.
- Mélanger horizons de prix et d’exécution.
- Oublier le cash.
- Soustraire deux fois le taux sans risque.
- Zero-center avant coûts.
- Zero-center l’OOS.
- Réutiliser la distribution WRC pour l’IC OOS.
- Choisir un benchmark favorable après résultats.

---

## 25. Sources internes

- `Notes/3-L'Art du Détrendage et de l'Évaluation des Règles de Trading.md`
- `Notes/3.1-Le Détrendage (explication supplémentaire) Distinguer le Talent de la Chance du Marché.md`
- `Notes/12-L'Illusion du Backtest Biais de Position et Tendance Marché.md`
- `Notes/13-L'Illusion du Profit Démasquer le Biais de Tendance en Backtesting.md`
- `Notes/Detrending - La méthode - benchmark selon Aronson.md`
- `Notes/Le Zero-Centering la méthode.md`
- `Notes/Éliminer les Biais Detrending et Zero-Centering - comparaisons.md`
- `Notes/BLP1 - La Méthode Aronson Détrendage et Validation Statistique du Profit.md`

---

## 26. Décision méthodologique synthétique

> **Les signaux sont produits exclusivement à partir de données point-in-time non detrendées. L’inférence EBTA utilise le log-rendement quotidien net de la stratégie, neutralise le cash et retire le drift excédentaire du marché proportionnellement aux expositions effectives. Le drift Test est estimé localement dans chaque `Test_k`; le drift OOS est estimé une seule fois sur l’OOS concaténé. Le zero-centering s’applique séparément à chaque candidate uniquement pour construire `H0` dans le bootstrap conjoint. Il ne remplace jamais le detrending et n’est jamais appliqué à l’estimation OOS.**
