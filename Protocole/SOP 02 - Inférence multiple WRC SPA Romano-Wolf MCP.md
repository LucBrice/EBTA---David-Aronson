# SOP 02 — Inférence multiple : WRC, SPA, Romano–Wolf et MCPM
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 02 |
| Rôle dans le paquet EBTA | Inference multiple sur Test, WRC local, SPA, Romano-Wolf et MCPM. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## 1. Statut et objet

- **Type :** Standard Operating Procedure méthodologique.
- **Statut :** spécification normative de l’inférence multiple sur le segment Test.
- **Objet :** corriger le biais de sélection lorsqu'une règle ou un processus de trading est choisi parmi plusieurs candidates.
- **Test confirmatoire primaire :** White's Reality Check (`WRC`).
- **Seuil primaire :** test unilatéral, $\alpha=0{,}05$.
- **Architecture Walk-Forward :** un WRC local est exécuté dans chaque fold avant l'ouverture de son segment `OOS_k`.

Cette SOP empêche qu'une règle soit déclarée significative sur la base d'une p-value individuelle ignorant l'effort complet de recherche.

Elle définit :

- la population des candidates ;
- la matrice de performances ;
- le WRC primaire ;
- le SPA comme analyse de sensibilité ;
- Romano–Wolf comme procédure d'identification multiple ;
- la Monte Carlo Permutation Method (`MCPM`) comme test secondaire de l'appariement signal–rendement ;
- les règles de dépendance, de rééchantillonnage, de décision et de reproductibilité.

Elle ne définit pas :

- la segmentation temporelle, relevant de la SOP 04 ;
- les formules de detrending, benchmark et zero-centering, relevant de la SOP 07 ;
- l'estimation et l'intervalle de confiance OOS, relevant de la SOP 01 ;
- les gates économiques et les stress-tests, relevant des SOP correspondantes.

En cas de contradiction, la SOP spécialisée prévaut dans son domaine.

---

## 2. Principe fondamental

Lorsqu'un processus examine plusieurs candidates et en sélectionne une, l'objet statistique n'est pas la performance isolée de la gagnante, mais le résultat du processus de sélection :

$$
\max_{m\in\{1,\dots,M\}}\hat{\theta}_m
$$

où :

- $M$ est le nombre de candidates réellement exposées à la sélection ;
- $\hat{\theta}_m$ est la statistique de performance différentielle de la candidate $m$.

Le test doit reproduire la meilleure performance qu'aurait pu produire l'univers complet sous l'hypothèse nulle.

Sont interdits :

- le test isolé de la règle gagnante ;
- l'utilisation du seul compteur $M$ sans séries de performance ;
- la suppression rétrospective de candidates ;
- le choix après observation du test, de la métrique ou du schéma donnant la p-value la plus favorable.

---

## 3. Architecture confirmatoire

### 3.1 Fold unique

Dans une architecture à fold unique :

```text
Train → Test + WRC → gel de la règle → OOS
```

L'OOS n'est ouvert que si le WRC primaire du Test est `PASS`.

### 3.2 Walk-Forward

Dans un véritable Walk-Forward :

```text
Train_k → Test_k + WRC_k → décision de déploiement → OOS_k
```

Le WRC du fold $k$ utilise uniquement les informations disponibles avant `OOS_k`. Un test global calculé après avoir observé des folds futurs ne peut pas autoriser rétroactivement l'ouverture d'un OOS antérieur.

Pour chaque fold :

1. appliquer le processus de calibration et de sélection préenregistré ;
2. construire la matrice locale complète sur `Test_k` ;
3. exécuter le WRC local ;
4. ouvrir `OOS_k` uniquement si le verdict local est `PASS` ;
5. poursuivre les folds suivants selon le calendrier gelé, indépendamment du résultat observé.

### 3.3 Contribution d'un fold non déployé

Après un WRC local `FAIL` :

- la règle n'est pas déployée sur `OOS_k` ;
- le segment temporel reste dans la série OOS globale ;
- l'exposition de la stratégie y est nulle ;
- le rendement correspond au cash ou à la convention de non-déploiement préenregistrée ;
- aucun résultat hypothétique de la règle refusée n'entre dans le verdict OOS.

Exclure ce segment de la concaténation OOS créerait un biais favorable.

Après un WRC local `INCONCLUSIVE`, le traitement conservateur est identique : aucun déploiement, segment conservé, poursuite mécanique du calendrier si l'architecture le permet.

### 3.4 Verdict global

Les WRC locaux contrôlent les décisions locales de déploiement. Ils ne sont ni moyennés ni combinés en un vote global.

Le verdict final du processus Walk-Forward repose sur la série OOS chronologique concaténée, construite et évaluée selon la SOP 01.

La répétition de tests locaux ne contrôle pas une FWER unique sur toute la durée de vie du processus. Chaque décision est une décision temporelle locale, prise au niveau $\alpha$ préenregistré. Cette limite doit être déclarée. Une gouvernance exigeant un contrôle global séquentiel doit définir séparément une procédure d'alpha-spending avant le premier fold.

---

## 4. Population des candidates

### 4.1 Définition normative

Une candidate appartient à la famille si sa performance a été effectivement calculée et si son résultat était accessible, directement ou indirectement, au processus de sélection.

La famille inclut notamment :

- candidates perdantes ;
- paramètres voisins ;
- variantes abandonnées ;
- niveaux de complexité ;
- règles d'entrée, de sortie, de sizing ou de filtrage comparées ;
- architectures ML et hyperparamètres ;
- seeds pouvant être sélectionnées ;
- benchmarks ou métriques alternatifs ayant influencé une décision ;
- variantes testées manuellement ;
- décisions ou variantes inspirées par des résultats antérieurs ;
- stress-tests utilisés pour choisir ou modifier une règle.

Une variante prévue mais jamais exécutée et jamais observée n'est pas une candidate réalisée. Elle reste documentée dans le plan de recherche.

### 4.2 Seeds

Chaque seed ML est une candidate distincte lorsqu'elle peut être sélectionnée pour son résultat.

Une agrégation de seeds ne constitue une candidate unique que si :

- la règle d'agrégation a été préenregistrée ;
- aucune seed individuelle ne peut être choisie ;
- la sortie agrégée est la seule information accessible au sélecteur.

### 4.3 Catalogue Walk-Forward

Le catalogue global des candidates, leur sémantique et l'algorithme de sélection doivent être identiques entre folds.

Les valeurs de paramètres recalibrées peuvent varier si cette variation est prévue, mais une colonne statistique doit représenter le même processus candidat dans chaque fold.

Ajouter, supprimer ou redéfinir une candidate entre folds crée une nouvelle version du processus. Les résultats ne peuvent alors pas être présentés comme provenant d'un protocole homogène sans nouvelle gouvernance.

### 4.4 Registre incomplet

Une candidate influente sans série reconstructible rend le registre incomplet.

Le verdict est alors `INCONCLUSIVE`. Il est interdit :

- d'exclure silencieusement la candidate ;
- de lui imputer une performance nulle ;
- de limiter le test au sous-univers disponible ;
- d'estimer sa série en fonction de l'effet produit sur le verdict.

---

## 5. Entrées statistiques

### 5.1 Matrice locale

Chaque fold utilise une matrice locale :

$$
D_k=
\begin{bmatrix}
d_{1,1} & \cdots & d_{1,M}\\
\vdots & \ddots & \vdots\\
d_{T_k,1} & \cdots & d_{T_k,M}
\end{bmatrix}
$$

Les colonnes représentent le catalogue commun des candidates. Les lignes représentent les observations temporelles valides de `Test_k`.

### 5.2 Série primaire

L'entrée primaire est le log-rendement quotidien net detrendé :

$$
d_{t,m}=r^{strat,net}_{t,m}-r_t^{reference}
$$

La construction exacte doit suivre la SOP 07 et rester cohérente avec la SOP 01 :

- même fréquence et mêmes timestamps ;
- même unité ;
- même modèle d'exécution ;
- coûts et slippage figés ;
- cash neutralisé dans le gate statistique selon la convention retenue ;
- drift de marché ajusté par l'exposition ;
- jours sans position conservés.

### 5.3 Detrending par fold

Le drift est estimé séparément dans chaque `Test_k`. Les séries detrendées locales ne sont concaténées qu'à des fins descriptives ou d'archivage ; le WRC décisionnel reste local.

### 5.4 Historiques hétérogènes

Les candidates doivent disposer d'un historique homogène dans la famille testée.

Si des historiques structurellement différents sont légitimes :

1. former des familles homogènes préenregistrées ;
2. appliquer une correction hiérarchique globale entre familles ;
3. appliquer ensuite la procédure interne prévue dans les familles autorisées.

Aucune valeur manquante ne doit être remplacée par zéro.

### 5.5 Données invalides

Une observation invalide requise par la matrice produit `INCONCLUSIVE` jusqu'à correction technique documentée.

Sont interdits :

- l'imputation arbitraire ;
- la suppression silencieuse d'une date ;
- l'usage discrétionnaire du dernier prix connu ;
- une correction décidée en fonction de la p-value.

---

## 6. Hypothèses et estimand

### 6.1 Hypothèse globale

Pour chaque fold :

$$
H_0:\max_m E[d_{t,m}]\leq0
$$

contre :

$$
H_1:\exists m,\ E[d_{t,m}]>0
$$

Le test est unilatéral.

### 6.2 Hurdle

Le hurdle statistique primaire est :

$$
h_s=0
$$

Le gate économique est séparé. Un rendement minimal économique ne remplace pas rétroactivement l'hypothèse primaire.

### 6.3 Statistique primaire WRC

La statistique primaire est la moyenne :

$$
\hat{\theta}_m=\bar d_m
$$

Le WRC utilise donc :

$$
T_{\max}^{obs}=\max_m \sqrt{T}\,\bar d_m
$$

Le facteur $\sqrt{T}$ peut être omis si la même convention est utilisée dans les statistiques observées et bootstrap.

Sharpe, Profit Factor, drawdown et autres métriques restent descriptifs sauf protocole distinct préenregistré.

---

## 7. Dépendance et rééchantillonnage

### 7.1 Synchronisation transversale

Les mêmes indices temporels bootstrap doivent être appliqués simultanément à toutes les colonnes.

Cette règle préserve :

- l'intercorrélation des candidates ;
- les chocs communs ;
- les régimes de volatilité ;
- la redondance des paramètres voisins.

Rééchantillonner chaque candidate indépendamment est interdit.

### 7.2 Méthode normative

La méthode primaire est le bootstrap stationnaire conjoint.

Le bootstrap IID n'est autorisé que si :

- le protocole IID du projet le valide ;
- aucun rendement ou trade ne se chevauche structurellement ;
- l'horizon de détention n'impose pas de dépendance ;
- la décision a été prise avant les résultats.

L'absence de significativité d'un test d'autocorrélation ne suffit pas à démontrer l'indépendance.

### 7.3 Longueur des blocs

La longueur moyenne des blocs est déterminée mécaniquement par l'algorithme de Politis–White avec correction de Patton–Politis–White.

Elle ne peut être inférieure au minimum structurel imposé notamment par :

- l'horizon maximal de détention ;
- le chevauchement des labels ou rendements ;
- les états persistants de la stratégie ;
- la fréquence de recalibration pertinente.

### 7.4 Frontières

Un bootstrap local ne sort jamais de `Test_k`.

Pour toute analyse descriptive combinant plusieurs segments :

- aucun bloc ne traverse une frontière de fold ;
- le rééchantillonnage est stratifié par fold ;
- les tailles relatives préenregistrées sont conservées.

---

## 8. Zero-centering

Pour le WRC, chaque colonne est centrée séparément :

$$
\tilde d_{t,m}=d_{t,m}-\bar d_m
$$

Le zero-centering :

- impose une espérance empirique nulle ;
- conserve la dispersion de chaque candidate ;
- conserve la dépendance transversale sous rééchantillonnage conjoint ;
- intervient après le detrending et la construction du P&L net.

Il ne doit pas être utilisé :

- pour générer les signaux ;
- pour calculer l'estimation ponctuelle ;
- pour construire l'intervalle de confiance OOS ;
- comme substitut au detrending.

---

## 9. White's Reality Check

### 9.1 Rôle

Le WRC est le test confirmatoire primaire. Il répond à la question :

> La meilleure performance produite par l'univers complet dépasse-t-elle ce qu'aurait vraisemblablement produit ce même processus de recherche sous l'hypothèse nulle ?

### 9.2 Algorithme

Pour chaque réplication $b=1,\dots,B$ :

1. générer un chemin de bootstrap stationnaire dans `Test_k` ;
2. appliquer les mêmes indices à toutes les colonnes zero-centered ;
3. recalculer la statistique de chaque candidate ;
4. réappliquer mécaniquement l'algorithme de sélection préenregistré ;
5. enregistrer la statistique sélectionnée ou maximale :

$$
T_{\max}^{*(b)}=\max_m T_m^{*(b)}
$$

La p-value est :

$$
\hat p_{WRC}=
\frac{1+\sum_{b=1}^{B}
\mathbf{1}\left(T_{\max}^{*(b)}\geq T_{\max}^{obs}\right)}
{B+1}
$$

### 9.3 Rejeu du processus

« Rejouer la sélection » signifie réappliquer toute règle mécanique ayant déterminé la candidate retenue, notamment :

- classement ;
- filtre d'éligibilité ;
- choix de complexité ;
- tie-break ;
- agrégation préenregistrée ;
- recalibration, si elle fait partie de l'objet statistique testé.

Le bootstrap ne doit pas introduire une optimisation libre absente du protocole réel.

Dans un WRC standard où la sélection est simplement « prendre la meilleure moyenne », le rejeu se réduit au recalcul du maximum.

### 9.4 Limite de puissance

Le WRC peut perdre de la puissance en présence de nombreuses candidates très mauvaises. Cette limite :

- doit être diagnostiquée ;
- ne permet pas de supprimer ces candidates après observation ;
- ne transforme pas un résultat valide non significatif en `INCONCLUSIVE`.

---

## 10. Hansen SPA

### 10.1 Rôle

Le SPA est une analyse secondaire de sensibilité. Il vise à réduire l'influence des candidates clairement mauvaises et utilise une statistique studentisée.

Il ne peut :

- autoriser l'OOS si le WRC primaire échoue ;
- renverser le verdict primaire ;
- être choisi après observation parce que sa p-value est plus faible.

### 10.2 Construction

La procédure doit implémenter explicitement le recentrage et la troncature de Hansen. Un simple zero-centering identique au WRC ne suffit pas à définir un SPA conforme.

Le rapport précise :

- la statistique studentisée ;
- l'estimateur de variance long terme ;
- la règle de troncature ;
- les éventuelles variantes SPA préenregistrées.

---

## 11. Romano–Wolf stepdown

### 11.1 Rôle

Romano–Wolf est exécuté après le rejet du test global lorsqu'il faut identifier les candidates individuelles significatives en contrôlant la Family-Wise Error Rate.

Il ne remplace pas le WRC primaire.

### 11.2 Famille

La procédure porte sur l'univers complet. En présence de familles à historiques homogènes distincts, une correction hiérarchique est obligatoire :

1. correction globale entre familles ;
2. ouverture des familles autorisées ;
3. stepdown interne.

### 11.3 Statistique

La statistique individuelle est studentisée :

$$
T_m=\frac{\sqrt{T}\bar d_m}{\hat\sigma_{LR,m}}
$$

où $\hat\sigma_{LR,m}$ estime la variance long terme selon une méthode préenregistrée compatible avec la dépendance.

### 11.4 Algorithme

1. ordonner les statistiques observées de la plus forte à la plus faible ;
2. tester le maximum sur l'ensemble courant ;
3. retirer l'hypothèse rejetée ;
4. recalculer le maximum sur les hypothèses restantes ;
5. continuer jusqu'au premier non-rejet ;
6. imposer la monotonie des p-values ajustées.

Le rapport publie pour chaque candidate :

- statistique observée ;
- rang ;
- p-value brute ;
- p-value ajustée ;
- étape de sortie ;
- décision.

---

## 12. Monte Carlo Permutation Method

### 12.1 Terminologie

Le sigle `MCPM` désigne exclusivement la **Monte Carlo Permutation Method**.

L'expression « procédure de comparaisons multiples » est écrite en toutes lettres afin d'éviter l'ambiguïté du sigle `MCP`.

### 12.2 Rôle

La MCPM est un test secondaire de la relation causale supposée entre les signaux disponibles et les rendements futurs.

Elle ne remplace pas le WRC primaire et ne construit pas l'intervalle de confiance OOS.

### 12.3 Schéma causal

Il n'existe pas de permutation universelle valide. Le schéma doit être :

- adapté au mécanisme de la stratégie ;
- préenregistré ;
- audité pour vérifier l'échangeabilité requise ;
- commun à toutes les candidates ;
- compatible avec la dépendance temporelle et cross-sectionnelle.

Les options possibles comprennent :

- permutation par blocs ;
- décalage circulaire ;
- permutation restreinte par actif, session ou régime ;
- autre transformation justifiée par l'hypothèse nulle.

### 12.4 Multi-actifs

La permutation doit préserver les dépendances contemporaines entre actifs, sauf si l'hypothèse testée justifie explicitement leur rupture.

Permuter chaque actif indépendamment par défaut est interdit.

### 12.5 Recalcul

Pour chaque réplication :

1. conserver les informations et signaux disponibles à la décision ;
2. appliquer la permutation préenregistrée aux rendements futurs ;
3. recalculer entièrement positions, P&L, coûts et statistiques de toutes les candidates ;
4. réappliquer le sélecteur ;
5. enregistrer la statistique maximale.

Permuter uniquement les P&L finaux ou l'ordre des rendements par trade ne constitue pas automatiquement un test valide du timing.

---

## 13. Paramètres préenregistrés

Avant chaque run, enregistrer :

- identifiant du projet et du fold ;
- hypothèses ;
- catalogue et famille des candidates ;
- algorithme complet de sélection ;
- statistique primaire ;
- benchmark, cash et hurdle ;
- période et fréquence ;
- coûts et modèle d'exécution ;
- méthode de detrending ;
- méthode de zero-centering ;
- méthode bootstrap ;
- algorithme de longueur des blocs et minimum structurel ;
- estimateur de variance long terme ;
- nombre de réplications ;
- seed ;
- seuil $\alpha$ ;
- traitement des valeurs manquantes ;
- traitement des historiques hétérogènes ;
- méthode hiérarchique éventuelle ;
- schéma MCPM ;
- critères `PASS`, `FAIL` et `INCONCLUSIVE` ;
- règle de déploiement après verdict.

Valeur normative :

$$
B=5\,000
$$

La seed est dérivée de manière préenregistrée du hash immuable des entrées du run.

---

## 14. Taille informationnelle et précision numérique

### 14.1 Minimum informationnel

Le test requiert :

- une analyse de puissance préenregistrée ;
- un effet minimal pertinent ;
- une hypothèse prudente de variance long terme ;
- un minimum de blocs effectifs propre au projet ;
- une taille suffisante pour estimer la dépendance et les statistiques requises.

Ces seuils sont fixés avant les résultats. Il n'existe pas de minimum universel de 1 000 observations ou 30 trades applicable à tous les projets.

### 14.2 P-value proche du seuil

Le verdict reste mécanique avec $B=5\,000$ :

- `PASS` si $\hat p<\alpha$ ;
- `FAIL` si $\hat p\geq\alpha$.

La proximité de $\alpha$ doit toutefois être signalée avec :

- l'erreur Monte-Carlo estimée ;
- un intervalle numérique autour de la p-value ;
- le nombre d'excédances observées.

Une zone grise numérique ne peut pas être inventée après observation. Une procédure adaptative augmentant $B$ exige une règle d'arrêt préenregistrée dans une version ultérieure du protocole.

---

## 15. Règles de décision locales

### 15.1 `PASS`

Le fold est `PASS` si toutes les conditions suivantes sont satisfaites :

1. registre complet ;
2. matrice reconstructible et valide ;
3. minimum informationnel respecté ;
4. WRC primaire exécuté exactement comme préenregistré ;
5. p-value WRC strictement inférieure à $\alpha$ ;
6. aucune violation de dépendance, de données, de chronologie ou de sélection.

Seul ce verdict autorise le déploiement de la candidate choisie sur `OOS_k`.

Les résultats du SPA, de Romano–Wolf et de la MCPM sont secondaires et ne renversent pas ce verdict.

### 15.2 `FAIL`

Le fold est `FAIL` lorsque :

- le test est techniquement valide ;
- l'information minimale est suffisante ;
- $\hat p_{WRC}\geq\alpha$.

Un grand univers et une faible puissance ne justifient pas `INCONCLUSIVE` si le test prévu reste valide.

### 15.3 `INCONCLUSIVE`

Le fold est `INCONCLUSIVE` lorsqu'aucune inférence défendable ne peut être produite, notamment :

- registre ou matrice incomplet ;
- candidate influente non reconstructible ;
- données invalides non corrigées ;
- historique incompatible avec la méthode prévue ;
- minimum informationnel non atteint ;
- dépendance non traitable ;
- erreur empêchant le rejeu du processus ;
- violation rendant la p-value non interprétable.

`FAIL` et `INCONCLUSIVE` interdisent le déploiement sur l'OOS du fold.

### 15.4 Candidate transmise

Après `PASS`, seule la candidate désignée par la règle de sélection préenregistrée est transmise à l'OOS.

Romano–Wolf peut identifier plusieurs candidates significatives, mais il ne donne pas le droit d'en choisir une après observation. Un portefeuille de candidates exige une règle d'agrégation préenregistrée et constitue lui-même une candidate.

---

## 16. Gouvernance des modifications et réexécutions

Toute modification méthodologique après visualisation des résultats :

- invalide le run confirmatoire ;
- crée une nouvelle version du processus ;
- doit intégrer l'ensemble des essais antérieurs au registre ;
- exige de nouvelles données non consommées pour une nouvelle confirmation.

Une réexécution sur les mêmes données n'est autorisée que pour une erreur technique objective si :

- l'erreur est indépendante du signe ou du niveau de performance ;
- le correctif ne modifie pas l'hypothèse économique ;
- une revue indépendante l'autorise ;
- le snapshot initial, le run erroné, le correctif et le run corrigé sont archivés.

Une mauvaise p-value n'est jamais une erreur technique.

---

## 17. Livrable obligatoire

Le rapport doit contenir :

```text
[IDENTIFICATION]
project_id:
process_version:
fold_id:
code_hash:
config_hash:
data_hash:
environment_hash:

[HYPOTHESES]
H0:
H1:
alpha:
test_direction: one-sided
statistical_hurdle: 0

[FAMILY]
candidate_catalog_hash:
candidate_count:
selection_algorithm:
missing_candidates: 0
homogeneous_history_families:
hierarchical_correction:

[DATA]
test_dates:
matrix_dimensions:
observation_unit:
benchmark:
detrending_method:
cost_model:
invalid_observations: 0

[RESAMPLING]
primary_test: WRC
bootstrap_method:
block_length_method:
structural_minimum:
effective_blocks:
replications: 5000
seed:

[PRIMARY RESULT]
selected_candidate:
observed_statistic:
exceedance_count:
wrc_pvalue:
monte_carlo_error:
verdict:
oos_deployment_authorized:

[SECONDARY RESULTS]
spa_specification:
spa_pvalue:
romano_wolf_table:
mcpm_scheme:
mcpm_pvalue:

[ARCHIVE]
matrix_path:
bootstrap_indices_path:
replications_path:
registry_path:
report_hash:
```

Doivent être archivés :

- matrice complète ;
- registre de recherche ;
- indices bootstrap et réplications ;
- configurations ;
- code et environnement ;
- seeds ;
- résultats intermédiaires ;
- rapport final et hashes.

---

## 18. Contrôles de reproductibilité

Une reproduction valide doit retrouver :

- les dimensions et le hash de la matrice ;
- la seed ;
- les indices de rééchantillonnage ;
- les statistiques observées ;
- le nombre d'excédances ;
- les p-values ;
- les décisions ;
- la candidate transmise.

Les contrôles minimaux comprennent :

- moyenne zero-centered proche de zéro pour chaque colonne ;
- indices temporels identiques entre colonnes ;
- absence de bloc traversant une frontière ;
- ordre des opérations conforme à la SOP 07 ;
- rejeu déterministe du sélecteur ;
- monotonie des p-values Romano–Wolf ;
- conservation des dépendances prévues par la MCPM.

---

## 19. Erreurs interdites

- Tester seulement la gagnante.
- Fournir uniquement le nombre $M$.
- Retirer les candidates médiocres après observation.
- Omettre les essais manuels ou les seeds sélectionnables.
- Mélanger des historiques incompatibles sans correction hiérarchique.
- Imputer zéro aux candidates ou dates manquantes.
- Rééchantillonner les colonnes indépendamment.
- Laisser un bloc traverser une frontière de fold.
- Utiliser un Test futur pour autoriser un OOS antérieur.
- Exclure de l'OOS les périodes où le WRC local échoue.
- Combiner les p-values locales comme un vote non préenregistré.
- Choisir SPA parce qu'il est plus favorable que le WRC.
- Appeler Romano–Wolf une simple version améliorée du WRC.
- Employer `MCP` indistinctement pour permutation et comparaisons multiples.
- Permuter des P&L finaux sans justification causale.
- Utiliser la MCPM comme intervalle de confiance.
- Zero-center les rendements pour l'estimation OOS.
- Changer de métrique, de bloc, de seed ou de test après observation.
- Accéder à l'OOS après `FAIL` ou `INCONCLUSIVE`.
- Choisir après Romano–Wolf une autre candidate que celle prévue.

---

## 20. Relations normatives avec les autres SOP

### SOP 01 — Estimation OOS

La SOP 02 décide localement si le processus peut prendre une exposition sur `OOS_k`. La SOP 01 estime ensuite la performance du processus Walk-Forward gelé sur tous les segments OOS concaténés, y compris les périodes de non-déploiement.

La distribution WRC n'est jamais réutilisée pour construire l'intervalle de confiance OOS.

### SOP 04 — Segmentation et Walk-Forward

La SOP 04 définit :

- les fenêtres ;
- le calendrier ;
- les purges et embargos ;
- les frontières ;
- les règles de recalibration.

La SOP 02 définit l'inférence multiple exécutée dans chaque `Test_k`.

### SOP 07 — Detrending et zero-centering

La SOP 07 est la source de vérité pour :

- le flux signal ;
- le flux d'évaluation ;
- le benchmark ;
- le detrending ;
- le zero-centering ;
- l'ordre des transformations.

---

## 21. Modifications requises dans le protocole principal

Après adoption de cette SOP, `PROTOCOLE EBTA.md` doit être corrigé pour :

1. distinguer WRC, SPA, Romano–Wolf et MCPM ;
2. supprimer l'expression ambiguë « WRC version Romano–Wolf » ;
3. remplacer `MCP` par `MCPM` lorsqu'il s'agit de permutation ;
4. imposer la matrice complète plutôt que le seul compteur $M$ ;
5. définir le WRC comme test primaire et le SPA comme sensibilité ;
6. placer un WRC local avant chaque OOS en Walk-Forward ;
7. interdire un test global futur autorisant rétroactivement des OOS antérieurs ;
8. conserver dans l'OOS global les périodes de non-déploiement ;
9. supprimer toute réutilisation de la distribution WRC pour l'IC OOS ;
10. aligner les verdicts avec les SOP 01, 04 et 07.

La mise en production documentaire est interdite tant que ces contradictions persistent.

---

## 22. Sources internes

- `Protocole/SOP 01 - Estimation et intervalle de confiance OOS.md`
- `Protocole/SOP 04 - Segmentation temporelle et Walk-Forward.md`
- `Protocole/SOP 07 - Detrending benchmark et zero-centering.md`
- `Protocole/Archives/AUDIT METHODOLOGIQUE PROTOCOLE EBTA.md`
- `Notes/73-Le Bootstrap Valider la Performance en Trading par Rééchantillonnage.md`
- `Notes/74-White’s Reality Check L'Antidote au Biais de Minage de Données.md`
- `Notes/75-Méthode de Monte Carlo L'Antidote au Hasard en Trading.md`
- `Notes/125-Le White's Reality Check Valider le Minage de Données.md`
- `Notes/126-Validation Statistique par Permutation de Monte Carlo.md`
- `Notes/127-Optimisation de la Puissance Statistique en Minage de Données.md`
- `Notes/128-Les Clés de la Puissance Statistique selon David Aronson.md`
- `Notes/Bootstrap et Monte Carlo la méthode.md`
- `Notes/Éliminer les Biais Detrending et Zero-Centering - comparaisons.md`

---

## 23. Décision méthodologique synthétique

> **Dans chaque fold, le White's Reality Check teste au niveau unilatéral de 5 % l'univers complet et reconstructible des candidates sur le segment Test disponible à cette date. Le bootstrap stationnaire est conjoint, zero-centered et respecte la dépendance temporelle. Seul un WRC local `PASS` autorise une exposition sur l'OOS suivant. Après `FAIL` ou `INCONCLUSIVE`, le processus reste à exposition nulle pendant ce segment, qui demeure dans l'OOS global. Le SPA est une sensibilité, Romano–Wolf identifie les rejets individuels après rejet global, et la MCPM teste secondairement l'appariement signal–rendement. Le verdict final du Walk-Forward repose sur l'OOS concaténé selon la SOP 01.**
