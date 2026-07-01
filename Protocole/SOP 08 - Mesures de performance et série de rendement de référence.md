# SOP 08 — Mesures de performance et série de rendement de référence
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.1 |
| Date de gel documentaire | 2026-07-01 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 08 |
| Rôle dans le paquet EBTA | Serie de rendement primaire, NAV, metriques et gate economique. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## 1. Statut et objet

- **Statut :** contrat normatif de rendement et de mesure de performance.
- **Unité statistique primaire :** log-rendement quotidien du portefeuille.
- **Métrique statistique primaire :** moyenne arithmétique des log-rendements quotidiens nets detrendés.
- **Sortie économique :** performance réelle nette du portefeuille, distincte de l’alpha detrendé.

Cette SOP fournit une implémentation unique et reproductible des séries et métriques utilisées pour :

- la sélection ;
- l’inférence ;
- l’estimation OOS ;
- les gates économiques ;
- la robustesse ;
- le monitoring.

Elle interdit le metric shopping, les changements d’unité, les annualisations incohérentes et l’utilisation d’une distribution d’échantillonnage correspondant à une autre statistique.

---

## 2. Autorités normatives

La présente SOP applique :

- l’estimand OOS de la SOP 01 ;
- les tests de la SOP 02 ;
- les segments de la SOP 04 ;
- les scénarios de robustesse de la SOP 05 ;
- le detrending de la SOP 07 ;
- les données point-in-time de la SOP 09A ;
- l’exécution et les coûts de la SOP 09B.

Elle ne peut redéfinir après coup une convention déjà figée par une SOP propriétaire.

---

## 3. Contrat canonique du portefeuille

La source de vérité est la valeur liquidative économique du portefeuille dans sa devise de base.

Pour chaque jour `t`, conserver :

- `NAV_open` ;
- `NAV_close` ;
- flux externes ;
- P&L brut ;
- commissions et taxes ;
- spread, slippage et impact ;
- financement et borrow ;
- P&L FX ;
- rendement cash ;
- P&L net ;
- positions et expositions ;
- turnover ;
- indicateurs de qualité.

La NAV doit être réconciliable avec les ordres, fills, positions, cash, coûts et flux.

---

## 4. Flux externes

Les apports et retraits de capital ne sont pas de la performance.

Le contrat définit une convention unique de neutralisation des flux, notamment :

- valorisation avant ou après flux ;
- timestamp du flux ;
- unité de capital ;
- traitement des flux intrajournaliers.

Tous les flux restent journalisés. Une correction silencieuse de la NAV est interdite.

---

## 5. Log-rendement économique quotidien

Après neutralisation des flux externes :

$$
r_t^{strat,net}
=
\log\left(
\frac{V_t^{adj}}{V_{t-1}^{adj}}
\right).
$$

Cette série inclut :

- fills exécutables ;
- coûts ;
- cash ;
- financement ;
- borrow ;
- conversion FX ;
- contraintes et sizing réellement simulés.

Elle est la série économique primaire.

Un rendement simple peut être publié dans un champ séparé :

$$
R_t^{simple}=\exp(r_t^{log})-1.
$$

Il est interdit de mélanger addition, moyenne ou annualisation de rendements simples et logarithmiques.

---

## 6. Série statistique primaire

La série statistique primaire est le log-rendement quotidien net detrendé de la SOP 07 :

$$
d_t=
r_t^{strat,net}
-r_t^{cash}
-e_t\left(
\bar r^{market}
-\bar r^{cash}
\right),
$$

ou sa version multi-actifs.

Le hurdle statistique primaire est :

$$
h_s=0.
$$

La série économique et la série statistique sont conservées séparément.

---

## 7. Fréquence et calendrier

La fréquence primaire est quotidienne.

Le contrat précise :

- calendrier de sessions ;
- timezone ;
- heure de valorisation ;
- traitement des marchés 24/7 ;
- jours fériés ;
- périodes partielles ;
- changement d’heure ;
- règle de journée manquante.

Une stratégie peu active conserve néanmoins une observation par journée de valorisation.

Changer de fréquence crée une nouvelle expérience.

---

## 8. Jours sans exposition et folds sans modèle

Tous les jours restent dans la série.

Un jour sans exposition :

- conserve le rendement économique réel du cash ;
- conserve les frais éventuels ;
- a une contribution statistique neutralisée selon la SOP 01.

Un fold `NO_MODEL`, WRC `FAIL` ou WRC `INCONCLUSIVE` :

- reste dans l’OOS global ;
- utilise la convention de cash/non-déploiement ;
- n’inclut aucun rendement hypothétique de la candidate refusée.

Retirer les jours inactifs est interdit.

---

## 9. Portefeuille multi-actifs

La série primaire est construite à partir du portefeuille réellement tradable après :

- pondérations ;
- sizing ;
- contraintes de capital ;
- positions simultanées ;
- cash ;
- levier ;
- coûts ;
- conversion FX ;
- limites de liquidité.

Si la candidate est un couple `stratégie × actif`, la série primaire est la
série quotidienne tradable de ce couple, après coûts, cash, calendrier et
conversion éventuelle. Si la candidate est un portefeuille multi-actifs fixe,
la série primaire est celle du portefeuille complet.

Il est interdit :

- de moyenner des backtests mono-actif incompatibles ;
- de retenir après observation uniquement les actifs favorables pour construire
  une série agrégée ;
- de sommer des P&L qui utilisent simultanément le même capital ;
- d’ignorer les corrélations et chevauchements de positions.

---

## 10. Métrique statistique primaire

La métrique primaire est :

$$
\hat\mu_d=\bar d=\frac{1}{T}\sum_{t=1}^{T}d_t.
$$

Elle estime directement l’espérance quotidienne de l’alpha net detrendé.

Cette même statistique doit être utilisée de manière cohérente pour :

- la sélection ;
- le WRC ;
- l’estimation OOS ;
- l’intervalle de confiance ;
- le verdict statistique.

---

## 11. Dérogation de métrique

Sharpe, log Profit Factor, Ulcer Performance Index ou une autre statistique ne peuvent devenir primaires que dans une nouvelle spécification préenregistrée comprenant :

- formule exacte ;
- sens d’optimisation ;
- benchmark ;
- hurdle ;
- unité d’observation ;
- distribution d’échantillonnage ;
- test multiple adapté ;
- nouvelle famille de recherche.

Une dérogation ne remplace jamais rétroactivement la métrique d’un run observé.

---

## 12. Annualisation

Si `A` est le nombre de sessions annuelles préenregistré :

### 12.1 Espérance logarithmique

$$
\hat\mu_{ann}^{log}=A\hat\mu_d.
$$

### 12.2 Représentation en rendement simple

$$
\hat R_{ann}^{simple}
=
\exp(A\hat\mu_d)-1.
$$

Cette représentation est dérivée et ne change pas la statistique inférée.

### 12.3 Volatilité

Sous approximation IID :

$$
\sigma_{ann}\approx\sqrt{A}\sigma_d.
$$

En présence de dépendance matérielle, utiliser une variance long terme ou une méthode préenregistrée. Présenter systématiquement `\sqrt A` comme exact est interdit.

---

## 13. CAGR

Pour une NAV économique positive :

$$
CAGR=
\left(
\frac{V_T}{V_0}
\right)^{1/Y}-1.
$$

Le CAGR :

- mesure une croissance composée réalisée ;
- appartient à la sortie économique ;
- ne remplace pas l’espérance statistique primaire ;
- n’est pas défini après ruine ou NAV non positive sans convention spéciale.

---

## 14. Sharpe

Le Sharpe est secondaire sauf nouvelle spécification conforme à la section 11.

$$
SR=
\frac{\bar r-r_f}{\sigma(r-r_f)}.
$$

Le contrat fige :

- série utilisée ;
- fréquence ;
- cash/taux sans risque ;
- estimateur de dispersion ;
- correction de dépendance ;
- annualisation ;
- traitement des jours non exposés ;
- politique en cas de volatilité nulle.

Une volatilité nulle produit une métrique non définie selon un statut préenregistré, jamais un `PASS` automatique.

---

## 15. Profit Factor

$$
PF=
\frac{\sum gains}{|\sum pertes|}.
$$

Le contrat précise :

- unité de trade ;
- regroupement des legs ;
- coûts ;
- trades simultanés ;
- cas sans perte ;
- cas sans gain ;
- usage éventuel de `\log(PF)`.

Le cas sans perte est traité ex ante comme non défini, capé ou statut spécifique. Il ne produit jamais automatiquement une preuve infinie.

---

## 16. Drawdown

Le drawdown économique est calculé sur la NAV réelle nette :

$$
DD_t=
\frac{V_t-\max_{s\le t}V_s}
{\max_{s\le t}V_s}.
$$

Conserver :

- maximum drawdown ;
- durée maximale ;
- temps de récupération ;
- drawdown courant ;
- drawdown absolu ;
- dates de pic, creux et récupération.

Le drawdown n’est pas calculé sur l’alpha detrendé pour le gate économique.

---

## 17. Métriques secondaires obligatoires

### Rendement

- moyenne économique périodique ;
- rendement annualisé ;
- CAGR ;
- rendement cumulé.

### Risque

- volatilité ;
- variance long terme ;
- downside deviation ;
- maximum drawdown ;
- durée de drawdown ;
- Ulcer Index ;
- quantiles de pertes ;
- pertes extrêmes.

### Efficacité

- Sharpe ;
- Sortino ;
- Calmar ;
- Profit Factor ;
- gain/perte moyens ;
- expectancy par trade.

### Activité et exécution

- nombre de signaux ;
- ordres ;
- fills ;
- trades clôturés ;
- turnover ;
- exposition ;
- durée de position ;
- participation ;
- coûts ;
- capacité.

Ces métriques sont diagnostiques sauf gate explicitement préenregistré.

---

## 18. Rendements par trade

Les métriques par trade sont secondaires.

Le contrat définit :

- capital de référence ;
- trades simultanés ;
- pyramiding ;
- coûts ;
- partial fills ;
- sorties partielles ;
- regroupement des legs ;
- date d’ouverture et de clôture ;
- P&L réalisé et mark-to-market.

Le nombre de trades, d’actifs ou de couples `stratégie × actif` évalués n’est
pas automatiquement la taille d’échantillon statistique. L’unité primaire reste
la série quotidienne du portefeuille ou de la candidate tradable évaluée.

---

## 19. Gate économique

Le gate économique est distinct du gate statistique.

Les seuils préenregistrés couvrent au minimum :

- rendement réel net ou marge au hurdle économique ;
- maximum drawdown ;
- perte journalière ;
- capacité au capital cible ;
- coûts ;
- liquidité ;
- levier et marge ;
- exécutabilité.

### `PASS`

Tous les seuils bloquants sont satisfaits.

### `REJECTED_ECONOMIC`

Le gate statistique applicable est `PASS`, mais au moins un seuil économique bloquant valide échoue.

### `INCONCLUSIVE`

La preuve économique matérielle est indisponible ou non reconstructible.

Le gate économique n’écrase pas le statut statistique ; les deux sont publiés séparément.

---

## 20. Métriques contradictoires

La hiérarchie est préenregistrée :

1. métrique statistique primaire ;
2. hurdle économique ;
3. gates de risque, capacité et exécution ;
4. diagnostics secondaires.

Une métrique secondaire défavorable ne bloque que si son seuil est explicitement déclaré bloquant.

Un vote discrétionnaire entre métriques est interdit.

---

## 21. Données manquantes

Chaque champ possède :

- règle de présence ;
- statut de qualité ;
- politique d’imputation ;
- tolérance ;
- conséquence sur le gate.

Une NAV ou une référence primaire non reconstructible produit `INCONCLUSIVE` jusqu’à correction.

Imputer silencieusement zéro ou supprimer une date est interdit.

---

## 22. Ruine, NAV nulle ou négative

Une NAV non positive :

- constitue une ruine ou une violation économique bloquante ;
- rend les log-rendements ultérieurs non définis ;
- interrompt le calcul selon une politique préenregistrée ;
- reste visible dans le verdict et le registre.

Il est interdit de remettre artificiellement la NAV à une valeur positive.

---

## 23. Outliers et concentration

La série primaire observée n’est pas winsorisée ou tronquée après les résultats.

Rapporter :

- contribution des meilleures 1 %, 5 % et 10 % périodes ;
- concentration par trade, actif et régime ;
- performance sans les `k` meilleures observations ;
- médiane et moyenne tronquée comme diagnostics ;
- asymétrie et kurtosis.

Tout retrait influençant le verdict est un stress-test préenregistré relevant de la SOP 05.

---

## 24. Réconciliation comptable

Dans une tolérance absolue et relative préenregistrée :

- P&L brut moins coûts égale P&L net ;
- cash et financement sont réconciliés ;
- flux externes sont neutralisés ;
- positions et fills expliquent le P&L ;
- cumul des log-rendements reproduit le ratio de NAV ;
- conversion FX est réconciliée.

Un contrôle visuel n’est pas une preuve.

---

## 25. Implémentation unique

Les formules sont implémentées dans un module versionné unique.

Les notebooks et rapports consomment cette implémentation.

Les tests unitaires couvrent :

- flux externes ;
- jours sans position ;
- cash ;
- coûts ;
- NAV multi-actifs ;
- rendements simple/log ;
- annualisation ;
- volatilité nulle ;
- Profit Factor sans perte ;
- ruine ;
- données manquantes ;
- drawdown ;
- réconciliation.

---

## 26. Changement de contrat

Changer :

- fréquence ;
- unité ;
- métrique ;
- benchmark ;
- hurdle ;
- coûts ;
- annualisation ;
- règle d’outlier

crée une nouvelle spécification et, si le résultat peut influencer la décision, une nouvelle candidate dans la famille de recherche.

Les données déjà observées ne redeviennent pas vierges.

---

## 27. Sorties par fold et globale

Conserver les diagnostics de chaque fold.

Le verdict OOS global est calculé sur la série quotidienne concaténée, pas sur :

- la moyenne des Sharpes ;
- la moyenne des CAGRs ;
- le vote des folds ;
- le meilleur fold.

---

## 28. Livrable canonique

```text
[RETURN CONTRACT]
frequency:
calendar:
timezone:
valuation_time:
base_currency:
flow_convention:

[DAILY SERIES]
date:
nav_open:
external_flows:
gross_pnl:
costs:
cash_return:
financing:
fx_pnl:
net_pnl:
nav_close:
economic_log_return:
detrended_log_return:
benchmark_return:
exposure:
turnover:
quality_status:

[PRIMARY METRIC]
name:
formula_version:
direction:
statistical_hurdle:
annualization:

[ECONOMIC GATE]
return_hurdle:
max_drawdown:
capacity_target:
cost_limit:
liquidity_limit:

[SECONDARY METRICS]
formulas:
risk_gates:

[RECONCILIATION]
tolerance_abs:
tolerance_rel:
status:
hashes:
```

---

## 29. Statuts de la SOP

### `PASS`

- contrat complet et préenregistré ;
- séries primaire et économique reconstructibles ;
- métrique implémentée une seule fois ;
- réconciliation valide ;
- cohérence sélection/test/OOS ;
- cas limites traités.

### `FAIL`

- metric shopping ;
- omission de coûts ;
- jours retirés ;
- annualisation trompeuse ;
- brut/net/detrendé confondus ;
- distribution statistique inadéquate ;
- NAV artificiellement corrigée.

### `INCONCLUSIVE`

- série primaire incomplète ;
- benchmark ou cash non reconstructible ;
- conventions historiques inconnues ;
- réconciliation non résolue.

---

## 30. Erreurs interdites

- Sélectionner au Sharpe puis tester la moyenne.
- Présenter le CAGR comme espérance.
- Utiliser `\sqrt A` sans hypothèse.
- Retirer les jours sans position.
- Moyenner les ratios de folds.
- Mélanger rendements simples et logarithmiques.
- Ignorer le cash ou les flux externes.
- Traiter un ratio non défini comme infini favorable.
- Winsoriser après observation.
- Changer de métrique après un résultat décevant.
- Changer hurdle, benchmark, coût ou convention économique après résultat pour obtenir `G-BIAS PASS`.

---

## 31. Relation avec SOP 13

La SOP 13 gouverne les biais de métrique, hurdle, benchmark, coût et
interprétation économique. Tout changement du contrat de performance après
observation d'un résultat sensible doit être journalisé comme incident ou
nouvelle version, jamais comme simple ajustement de reporting.

---

## 32. Sources internes

- `Notes/50-Statistiques Descriptives L'Architecture des Données de Trading.md`
- `Notes/76-L'Estimation Statistique de la Performance en Trading.md`
- `Notes/77-L'Art de l'Estimation Ponctuelle en Trading Objectif.md`
- `Notes/78-Intervalles de Confiance Mesurer l'Incertitude du Backtesting.md`
- `Notes/Question Analyse Technique des Estimateurs et Mesures de Performance Financière.md`
- `Notes/3-L'Art du Détrendage et de l'Évaluation des Règles de Trading.md`

---

## 33. Décision méthodologique synthétique

> **La représentation canonique EBTA est une série quotidienne complète du portefeuille. L’inférence porte sur la moyenne des log-rendements quotidiens nets detrendés ; le gate économique porte séparément sur la NAV réelle nette, le cash, les coûts, le risque, la capacité et l’exécutabilité. Tous les jours, y compris les périodes sans modèle ou sans exposition, restent dans la chronologie. Les métriques secondaires ne remplacent jamais rétroactivement la métrique primaire. Le verdict global est calculé sur l’OOS concaténé et toutes les séries doivent réconcilier la NAV dans une tolérance préenregistrée.**
