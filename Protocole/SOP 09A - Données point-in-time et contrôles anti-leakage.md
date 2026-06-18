# SOP 09A — Données point-in-time et contrôles anti-leakage
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 09A |
| Rôle dans le paquet EBTA | Disponibilite point-in-time, snapshots, anti-leakage, purge et embargo cote donnees. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## 1. Statut et objet

- **Statut :** spécification normative de disponibilité temporelle et d’intégrité des données.
- **Objet :** garantir que chaque feature, signal, ordre et décision simulés utilisent exclusivement l’information opérationnellement disponible à l’instant concerné.
- **Sortie :** snapshots immuables, contrats temporels, preuves anti-leakage et verdict de qualité.

Cette SOP couvre :

- look-ahead ;
- latence de publication et de fournisseur ;
- survivorship bias ;
- univers point-in-time ;
- corporate actions ;
- révisions et vintages ;
- alignement multi-sources ;
- données manquantes et stale ;
- transformations apprises ;
- purge et embargo ;
- tests causaux anti-leakage.

---

## 2. Invariant fondamental

Pour toute donnée `x` utilisée par une décision à l’instant `t` :

$$
availability\_time(x)\leq decision\_time(t).
$$

`availability_time` inclut toutes les latences nécessaires :

- publication ;
- disponibilité fournisseur ;
- ingestion ;
- validation ;
- calcul ;
- cutoff opérationnel.

La date économique de l’événement ne constitue pas une preuve de disponibilité.

---

## 3. Autorités normatives

La présente SOP fournit :

- les observations autorisées aux SOP 04 et 06 ;
- les séries de marché utilisées par les SOP 07 et 08 ;
- les timestamps requis par la SOP 09B ;
- les snapshots enregistrés par la SOP 03 ;
- les preuves archivées par la SOP 12.

Elle ne définit pas la logique de signal ni les règles de fill.

---

## 4. Contrat temporel d’un dataset

Chaque dataset et champ matériel définissent :

- `event_time` : instant de l’événement économique ;
- `publication_time` : première publication officielle ;
- `vendor_time` : disponibilité chez le fournisseur ;
- `ingestion_time` : réception par le système ;
- `validation_time` : fin des contrôles nécessaires ;
- `effective_time` ou `availability_time` : première utilisation autorisée ;
- timezone source ;
- timezone canonique ;
- calendrier ;
- fréquence ;
- politique de révision ;
- politique de latence ;
- politique de staleness.

Le moteur utilise `availability_time`, jamais le minimum opportuniste de ces timestamps.

---

## 5. Horloge de décision

Chaque stratégie définit :

```text
observation_cutoff
feature_time
decision_time
calculation_latency
order_submission_time
earliest_fill_time
valuation_time
```

Le contrat est propre au marché, au type d’ordre et à la fréquence.

Une horloge implicite ou reconstruite après le backtest est interdite.

---

## 6. Prix et barres quotidiennes

Pour chaque barre, documenter :

- début et fin ;
- champs OHLCV ;
- moment où chaque champ est complet ;
- latence fournisseur ;
- première décision autorisée ;
- première exécution possible.

Pour une barre quotidienne :

- le close final est disponible après la clôture ;
- un signal utilisant ce close ne peut normalement être exécuté avant l’ouverture suivante ;
- une exécution market-on-close n’est admise que si l’ordre pouvait être calculé et envoyé avant le cutoff réel sans utiliser le close final inconnu.

Décider au close final et remplir au même close est interdit sans preuve opérationnelle.

---

## 7. Barres intrajournalières

Les champs high, low, close et volume complets ne sont disponibles qu’à la fin de la barre, plus la latence.

Le moteur ne peut utiliser :

- le timestamp de début comme disponibilité de la barre complète ;
- le high ou low final avant leur réalisation ;
- une agrégation centered ;
- un index négatif implicite.

La politique de formation, retard et exécution des barres est préenregistrée.

---

## 8. Position et rendement

La position appliquée à une fenêtre de rendement doit avoir été déterminée avant cette fenêtre.

Les tests vérifient explicitement :

- décalage signal → ordre ;
- ordre → fill ;
- fill → position ;
- position → P&L ;
- absence de rendement déjà réalisé dans le signal.

Un décalage ajouté après observation pour améliorer le résultat crée une nouvelle candidate.

---

## 9. Fuseaux et calendriers

Les données sont normalisées dans un temps canonique, de préférence UTC, tout en conservant :

- timezone source ;
- offset ;
- daylight saving time ;
- calendrier de marché ;
- sessions partielles ;
- jours fériés ;
- marchés 24/7 ;
- coupures fournisseur.

Une date locale sans timezone n’est pas un timestamp opposable.

---

## 10. Joins multi-sources

Les joins utilisent une logique `as-of` fondée sur la disponibilité.

Le contrat précise :

- clé temporelle ;
- direction du join ;
- tolérance maximale ;
- âge maximal ;
- politique de données simultanées ;
- politique de doublons ;
- statut des lignes non appariées.

Un forward-fill ne peut rendre une valeur disponible avant sa publication.

Un backfill depuis une observation future est interdit.

---

## 11. Univers point-in-time

Pour chaque date, conserver :

- membres admissibles ;
- date d’entrée ;
- date de sortie ;
- motif ;
- statut de cotation ;
- exchange ;
- identifiant historique ;
- données pré-radiation ;
- traitement de delisting ;
- contraintes de disponibilité.

Construire l’historique depuis les constituants actuels est interdit.

Les filtres de liquidité, capitalisation, prix et historique minimal utilisent uniquement les données disponibles à la date, avec lag réaliste.

---

## 12. Delistings et titres disparus

Les titres radiés ou disparus restent dans l’univers historique jusqu’à leur date effective.

Conserver :

- dernier prix exécutable ;
- rendement de delisting si disponible ;
- procédure de liquidation ;
- pertes et coûts ;
- données manquantes ;
- cause de disparition.

Une absence matérielle de données de delisting produit `INCONCLUSIVE` ou `NOT_VALIDATED` selon son impact.

Supprimer les titres disparus est une violation de survivorship.

---

## 13. Corporate actions

Conserver séparément :

- prix bruts exécutables ;
- séries ajustées ;
- facteurs d’ajustement ;
- splits ;
- dividendes ;
- fusions ;
- spin-offs ;
- droits ;
- delistings.

Les indicateurs peuvent utiliser une série ajustée cohérente.

Les fills utilisent des prix exécutables bruts et la comptabilité applique séparément les corporate actions.

Un facteur futur ne peut modifier rétroactivement une décision historique. La procédure d’ajustement doit préserver l’information point-in-time.

---

## 14. Fondamentaux

Pour chaque observation fondamentale :

- période économique ;
- publication réelle ;
- heure ;
- fournisseur ;
- disponibilité opérationnelle ;
- valeur initiale ;
- vintage ;
- révisions ;
- statut d’audit.

La date de fin de période ne vaut pas date de disponibilité.

Les valeurs finales révisées ne peuvent être utilisées historiquement si elles n’étaient pas alors connues.

---

## 15. Données macroéconomiques

Utiliser le vintage disponible à la date de décision.

Conserver :

- release calendar ;
- valeur initiale ;
- révisions successives ;
- surprise par rapport à l’information disponible ;
- latence fournisseur.

Une base macro révisée aujourd’hui ne peut remplacer silencieusement les vintages historiques.

---

## 16. Timestamp inconnu

Si le timestamp exact est indisponible :

1. appliquer un lag conservateur préenregistré ;
2. documenter la provenance et l’incertitude ;
3. exécuter une sensibilité ;
4. classer `INCONCLUSIVE` si le risque matériel ne peut être borné.

Supposer une disponibilité immédiate est interdit.

---

## 17. Données alternatives

Documenter :

- collecte ;
- population couverte ;
- changements de définition ;
- latence ;
- suppressions ;
- backfills ;
- biais fournisseur ;
- disponibilité historique réelle ;
- archivage des vintages.

Un historique reconstruit aujourd’hui n’est utilisable que si sa disponibilité point-in-time peut être démontrée.

Les backfills inconnus du système historique sont exclus.

---

## 18. Données manquantes

Chaque variable possède une politique ex ante parmi :

- exclusion ;
- neutralisation du signal ;
- blocage du trade ;
- carry-forward borné ;
- imputation point-in-time ;
- statut non concluant.

Le contrat précise :

- seuil de valeurs manquantes ;
- âge maximal ;
- méthode ;
- indicateur d’imputation ;
- conséquence sur le gate.

Une imputation utilisant une observation future est interdite.

---

## 19. Prix stale

Un prix forward-filled conserve son âge.

Définir :

- âge maximal ;
- classe de liquidité ;
- comportement du signal ;
- comportement du sizing ;
- blocage de l’ordre ;
- règle de valorisation ;
- statut de qualité.

Au-delà du seuil, la donnée est neutralisée ou bloquante. Elle ne peut être déclarée fraîche par hypothèse.

---

## 20. Transformations apprises

Toute transformation dont les paramètres dépendent des données est fit exclusivement sur `Train_k`, notamment :

- moyenne et écart-type ;
- quantiles ;
- winsorisation ;
- PCA ;
- sélection de features ;
- encodage ;
- calibration ;
- modèles d’imputation ;
- modèles de régime.

Les paramètres gelés sont appliqués à `Test_k` et `OOS_k`.

Un refit sur Test ou OOS est interdit.

---

## 21. Features et effort de recherche

La sélection de features, la PCA, les méthodes de normalisation et les variantes d’imputation :

- appartiennent au pipeline de recherche ;
- sont enregistrées dans le catalogue ;
- sont comptabilisées dans la famille si elles influencent la sélection ;
- suivent la SOP 06.

Pré-calculer une transformation sur tout l’historique constitue un leakage.

---

## 22. Purge

La purge de la SOP 04 couvre le maximum pertinent de :

- lookbacks ;
- horizons de labels ;
- rendements forward ;
- durée des positions ;
- P&L chevauchants ;
- états de portefeuille ;
- transformations rolling ;
- dépendances aux frontières.

La durée moyenne d’un trade ne suffit pas si le maximum ou le label porte plus loin.

---

## 23. Embargo

L’embargo est ajouté ex ante lorsqu’une dépendance résiduelle justifiée subsiste après la purge.

Le contrat fixe :

- cause ;
- durée ;
- frontières ;
- effet sur la taille d’échantillon ;
- règle de non-adaptation.

L’embargo ne remplace pas la purge et ne peut être modifié selon les performances.

---

## 24. Snapshots immuables

Chaque run référence un snapshot comprenant :

- fournisseur ;
- licence ;
- version/vintage ;
- date d’extraction ;
- requête ;
- fichiers ;
- hashes ;
- schéma ;
- timezone ;
- univers ;
- contrôles qualité ;
- corrections ;
- politiques de timestamps et de révision.

Les fichiers source du snapshot sont immuables.

---

## 25. Correction de données

Une correction :

1. ne modifie pas le snapshot initial ;
2. crée un nouveau snapshot ;
3. documente cause, diff et impact ;
4. crée un nouveau run ;
5. conserve le lignage ;
6. réexécute les étapes affectées ;
7. ne sélectionne pas la version selon sa performance.

Si l’OOS a été observé, la correction suit également la SOP 10.

---

## 26. Tests anti-leakage obligatoires

### 26.1 Test causal de perturbation

Modifier toutes les données après une date `T`.

Résultat attendu :

> aucune feature, décision, position ou ordre antérieur ou égal à `T` ne change.

### 26.2 Disponibilité

Vérifier pour chaque valeur utilisée :

$$
availability\_time\leq decision\_time.
$$

### 26.3 Fenêtres

Détecter :

- centered windows ;
- index négatifs ;
- shifts incorrects ;
- agrégations globales ;
- normalisations futures.

### 26.4 Joins

Auditer :

- direction ;
- tolérance ;
- doublons ;
- lignes non appariées ;
- staleness.

### 26.5 Vintages et univers

Vérifier :

- constituants historiques ;
- révisions ;
- corporate actions ;
- delistings ;
- premières dates valides.

---

## 27. Conséquence d’un test échoué

Un test anti-leakage échoué est bloquant :

1. statut `FAIL` ;
2. cause identifiée ;
3. snapshot et run conservés ;
4. correction auditée ;
5. nouveau snapshot/run ;
6. réexécution complète des étapes affectées ;
7. nouveau gate.

Une estimation qualitative de « faible impact » ne transforme pas le résultat en `PASS`.

---

## 28. Provenance insuffisante

### `INCONCLUSIVE` ou `NOT_VALIDATED`

Lorsque la disponibilité historique ne peut pas être démontrée sans preuve d’usage futur.

### `FAIL`

Lorsque sont démontrés :

- usage futur ;
- survivorship ;
- révision finale utilisée historiquement ;
- exécution au prix impossible ;
- transformation fit sur Test/OOS.

---

## 29. Reproductibilité

À partir des snapshots scellés et de la configuration :

- mêmes données ;
- mêmes features ;
- mêmes signaux ;
- mêmes timestamps ;
- mêmes univers ;
- mêmes flags de qualité

doivent être reproduits dans les tolérances déterministes prévues.

Retélécharger la dernière version fournisseur n’est pas une reproduction.

---

## 30. Livrable obligatoire

```text
[DATASET]
dataset_id:
provider:
license:
version:
vintage:
snapshot_hash:
schema_hash:

[TIME CONTRACT]
event_time:
publication_time:
vendor_time:
ingestion_time:
validation_time:
availability_time:
source_timezone:
canonical_timezone:
calendar:

[UNIVERSE]
membership_snapshot:
entry_exit_policy:
delisting_policy:
liquidity_lag:

[MISSING AND STALE]
missing_policy:
imputation_policy:
max_age:
blocking_threshold:

[TRANSFORMATIONS]
fit_segment:
parameter_hash:
feature_pipeline_hash:

[ANTI_LEAKAGE TESTS]
causal_perturbation:
availability_check:
rolling_window_check:
join_check:
vintage_check:
universe_check:

[VERDICT]
status:
violations:
reviewer:
timestamp:
```

---

## 31. Statuts

### `PASS`

- provenance complète ;
- timestamps opposables ;
- univers point-in-time ;
- corporate actions cohérentes ;
- transformations fit sur Train ;
- snapshots scellés ;
- tous les tests anti-leakage `PASS`.

### `FAIL`

- information future ;
- survivorship ;
- révision finale ;
- fill impossible ;
- transformation fit sur Test/OOS ;
- correction silencieuse.

### `INCONCLUSIVE`

- disponibilité non démontrable ;
- delistings matériels incomplets ;
- corporate actions ambiguës ;
- provenance non vérifiable ;
- risque de staleness non borné.

---

## 32. Erreurs interdites

- Utiliser la date économique comme date de disponibilité.
- Utiliser un close pour décider et remplir au même close sans mécanisme réel.
- Utiliser un join futur.
- Forward-fill sans âge maximal.
- Construire l’univers depuis les survivants.
- Utiliser les dernières révisions macro.
- Ajuster rétroactivement les prix d’une manière informative.
- Fit une transformation sur tout l’historique.
- Sous-dimensionner la purge.
- Écraser un snapshot après correction.

---

## 33. Sources internes

- `Notes/4-L'Intégrité du Backtesting Biais d'Anticipation et Coûts Réels.md`
- `Notes/19-L'Illusion Technique L'Impératif de l'Objectivité Algorithmique.md`
- `Notes/42-L'Échantillonnage Fondement Statistique de la Validation de Trading.md`
- `Notes/121-La Validation Hors-Échantillon L'Épreuve de Réalité Statistique.md`
- `Notes/161-Protocole EBTA La Science de l’Analyse Technique Objective.md`

---

## 34. Décision méthodologique synthétique

> **Toute valeur utilisée par une décision EBTA doit avoir été opérationnellement disponible avant cette décision, après publication, latence, ingestion et validation. Les univers, corporate actions, fondamentaux, données macro et alternatives sont reconstruits point-in-time à partir de snapshots immuables. Toute transformation est apprise uniquement sur Train. La purge couvre toutes les dépendances aux frontières et l’embargo traite seulement les dépendances résiduelles préspécifiées. Un test anti-leakage échoué est bloquant et toute correction crée un nouveau snapshot et un nouveau run.**
