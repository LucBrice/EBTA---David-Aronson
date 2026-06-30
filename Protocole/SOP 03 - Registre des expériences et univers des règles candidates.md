# SOP 03 — Registre des expériences et univers des règles candidates
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 03 |
| Rôle dans le paquet EBTA | Registre append-only, candidates, familles, runs, matrices et evenements. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## 1. Statut et objet

- **Type :** Standard Operating Procedure méthodologique.
- **Statut :** spécification normative du registre des expériences et de l’univers des candidates.
- **Objet :** définir la source de vérité opposable de l’effort de recherche, des expériences, des candidates et des décisions ayant conduit à la sélection d’une règle ou d’un processus de trading.
- **Portée :** recherche, Test, ouverture OOS, robustesse, paper trading, live trading et retrait.
- **Effet bloquant :** un registre incomplet ou non reproductible interdit l’inférence multiple selon la SOP 02 et l’ouverture de l’OOS concerné.

Cette SOP définit :

- les objets enregistrés et leurs identifiants ;
- la frontière des familles de recherche ;
- les règles de comptage des candidates ;
- le traitement des recherches exhaustives, adaptatives, humaines et ML ;
- le contrat de données nécessaire à la matrice de performance ;
- le journal append-only des événements et décisions ;
- les gates de complétude, d’intégrité et de reproductibilité ;
- le cycle de vie des processus jusqu’à leur retrait.

Un compteur déclaré manuellement ne constitue jamais une preuve suffisante de l’effort de recherche.

---

## 2. Principe fondamental

Toute information historique susceptible d’influencer une décision de recherche consomme de l’information et doit être traçable.

Il n’existe pas :

- d’essai informel gratuit ;
- de test « juste pour voir » ;
- de run avorté effaçable ;
- d’inspection visuelle sans événement d’observation ;
- de candidate oubliable parce qu’elle a perdu ;
- de changement de nom permettant de réinitialiser l’effort de recherche ;
- de déduplication rétrospective destinée à réduire l’univers statistique.

L’objet à documenter n’est pas seulement la règle finalement retenue. Il est le processus complet qui aurait pu produire cette sélection.

---

## 3. Autorité normative et séparation des responsabilités

La SOP 03 est la source de vérité pour :

- l’identité des candidates ;
- leur catalogue et leur lignage ;
- les expériences, runs et événements de décision ;
- les familles de recherche ;
- la complétude de l’univers exposé à la sélection ;
- le contrat et la provenance de la matrice de performance ;
- le scellement et la conservation des artefacts.

Les responsabilités spécialisées restent réparties comme suit :

- **SOP 01 :** estimation et intervalle de confiance sur l’OOS concaténé ;
- **SOP 02 :** transformation statistique de la matrice et inférence multiple ;
- **SOP 04 :** fenêtres, folds, purges, embargos et calendrier Walk-Forward ;
- **SOP 07 :** benchmark, detrending, zero-centering et ordre des transformations.

En cas de contradiction, la SOP spécialisée prévaut dans son domaine. La SOP 03 reste toutefois opposable pour déterminer quelles candidates et quelles décisions doivent être enregistrées et transmises à la SOP 02.

---

## 4. Objets du registre

### 4.1 Projet

Un projet regroupe une intention de recherche, ses hypothèses, ses données, ses versions de processus et son cycle de vie.

Changer le nom ou l’identifiant d’un projet ne crée pas une indépendance statistique.

### 4.2 Hypothèse

Une hypothèse est une proposition économique, comportementale ou statistique falsifiable, accompagnée au minimum de :

- son rationnel ;
- son hypothèse nulle ;
- son benchmark ;
- son univers ;
- sa métrique primaire ;
- son protocole de segmentation ;
- sa date de préenregistrement.

### 4.3 Spécification planifiée

Une spécification planifiée décrit une variante prévue mais qui n’a encore produit aucune information de performance.

Elle est conservée dans le plan de recherche, mais n’est pas encore une candidate évaluée et n’entre pas dans l’univers statistique réalisé.

### 4.4 Candidate

Une candidate est une spécification exécutable unique pour laquelle une performance exploitable a été calculée ou observée.

Une nouvelle candidate est créée dès qu’un changement peut modifier :

- les signaux ;
- les positions ;
- le P&L ;
- la métrique primaire ;
- l’éligibilité ;
- le classement ;
- la sélection finale.

Cela comprend notamment :

- la forme logique de la règle ;
- les paramètres et seuils ;
- les indicateurs, transformations ou features ;
- les entrées et sorties ;
- l’horizon ;
- les filtres ;
- l’univers d’actifs ;
- l’actif lorsque le couple règle-actif est sélectionnable ;
- la pondération ou l’agrégation ;
- le sizing influençant la métrique primaire ;
- le benchmark ;
- la transformation ou le nettoyage des données ;
- le modèle de coûts lorsqu’il participe à la sélection ;
- l’architecture ML ;
- les hyperparamètres ;
- une seed sélectionnable ;
- la sous-période sélectionnable ;
- la métrique utilisée pour sélectionner ;
- le prétraitement ;
- la gestion du risque.

Lorsque l’actif peut influencer le classement, l’éligibilité ou la sélection,
le couple `stratégie × actif` fait partie de l’identité logique de la
candidate. Une stratégie abstraite n’est donc pas opposable sans la frontière
d’actifs ou le portefeuille tradable dans lequel elle a été évaluée.

Une modification purement technique sans effet possible sur ces éléments ne crée pas une nouvelle candidate. Elle crée une nouvelle version de code ou un nouveau run.

### 4.5 Run

Un run est l’exécution déterminée d’une candidate sur :

- un snapshot de données ;
- une version de code ;
- une configuration ;
- un environnement ;
- une seed éventuelle ;
- un segment temporel défini.

Plusieurs runs peuvent exécuter la même candidate.

### 4.6 Expérience

Une expérience est un ensemble planifié de runs répondant à une question de recherche explicite.

Elle doit définir avant exécution :

- l’hypothèse ;
- l’espace candidat ou son générateur ;
- les données ;
- la métrique primaire ;
- le sélecteur ;
- la règle d’arrêt ;
- les critères de décision.

### 4.7 Famille de recherche

Une famille de recherche est l’ensemble des candidates évaluées dont les résultats ont pu influencer une même décision sur des données de sélection partagées.

La famille est définie par la circulation de l’information et non par :

- le nom du projet ;
- le notebook ;
- le chercheur ;
- la session ;
- le dossier ;
- le langage de programmation.

### 4.8 Événement d’observation ou de décision

Tout accès humain ou automatisé à une sortie sensible crée un événement, même si aucune décision immédiate n’est déclarée.

Un événement enregistre au minimum :

- l’information rendue accessible ;
- l’objet observé ;
- le chercheur ou processus concerné ;
- le timestamp ;
- la décision éventuelle ;
- les candidates générées ;
- la justification ;
- les liens vers les événements parents.

---

## 5. Quantités de référence

Le registre distingue obligatoirement :

$$
M_{\text{planned}}
=
\text{nombre de spécifications planifiées}
$$

$$
M_{\text{evaluated}}
=
\text{nombre de candidates uniques ayant produit une information exploitable}
$$

$$
M_{\text{family}}
=
\text{nombre de candidates évaluées susceptibles d’avoir influencé la décision}
$$

Seul $M_{\text{family}}$, accompagné des séries complètes correspondantes, décrit l’univers statistique transmis à la SOP 02.

Les quantités $M_1$, $M_2$ ou toute autre ventilation par phase peuvent être conservées à titre descriptif. La formule :

$$
M=M_1+M_2
$$

n’est pas une définition normative générale de l’effort de recherche.

---

## 6. Création et identité d’une candidate

### 6.1 Critère de création

Une spécification devient une candidate lorsqu’une information exploitable de performance est effectivement calculée ou observée.

Une proposition générée mais jamais exécutée et jamais observée :

- reste enregistrée comme spécification planifiée ;
- n’entre pas dans $M_{\text{evaluated}}$ ;
- n’entre pas dans $M_{\text{family}}$.

### 6.2 Représentation canonique

Le `CANDIDATE_ID` est dérivé d’une représentation canonique déterministe de la spécification logique et paramétrique.

La canonicalisation doit notamment :

- ordonner les clés ;
- normaliser les types et unités ;
- normaliser les valeurs par défaut ;
- interdire les champs implicites ;
- référencer les versions de schéma ;
- produire le même résultat pour deux représentations syntaxiquement différentes mais formellement équivalentes.

Le code, le snapshot de données et l’environnement ne font pas partie de l’identité logique de la candidate. Ils participent à l’identité du run.

### 6.3 Déduplication ex ante

Deux spécifications distinctes ne peuvent être traitées comme une seule candidate que si leur équivalence fonctionnelle est démontrée avant toute évaluation par une procédure :

- automatique ;
- déterministe ;
- versionnée ;
- préenregistrée ;
- reproductible ;
- indépendante des résultats de performance.

La procédure peut vérifier, selon le domaine :

- l’identité formelle des expressions ;
- l’identité des signaux et positions sur l’ensemble des données admissibles ;
- l’identité des séries de P&L net ;
- des invariants supplémentaires préenregistrés.

Toute tolérance numérique doit être fixée avant évaluation.

### 6.4 Interdiction de la fusion rétroactive

Deux spécifications dont l’identité de signaux, positions ou performances est découverte après observation restent deux candidates si elles étaient séparément sélectionnables.

Une égalité accidentelle sur un snapshot ne permet :

- ni de fusionner rétroactivement leurs identités ;
- ni de réduire $M_{\text{family}}$ ;
- ni de supprimer une colonne après observation.

---

## 7. Identifiants et lignage

Chaque objet reçoit un identifiant immuable :

```text
PROJECT_ID
HYPOTHESIS_ID
PROCESS_VERSION_ID
RESEARCH_FAMILY_ID
EXPERIMENT_ID
PLANNED_SPEC_ID
CANDIDATE_ID
RUN_ID
EVENT_ID
DATA_SNAPSHOT_ID
MATRIX_ID
REVIEW_ID
```

Chaque run référence au minimum :

```text
CANDIDATE_ID
EXPERIMENT_ID
RESEARCH_FAMILY_ID
DATA_SNAPSHOT_ID
CODE_COMMIT
CONFIG_HASH
ENVIRONMENT_HASH
```

Chaque candidate dérivée référence :

- sa ou ses candidates parentes ;
- les observations ayant motivé sa création ;
- son motif de création ;
- la version du processus ;
- la famille dans laquelle l’information a été consommée.

Une modification après observation crée une candidate descendante dans la même famille, sauf si les conditions strictes d’ouverture d’une nouvelle famille sont satisfaites.

---

## 8. Frontière d’une famille de recherche

### 8.1 Inclusion

Une candidate appartient à une famille si :

1. sa performance a été effectivement calculée ou observée ;
2. son résultat était accessible directement ou indirectement au processus de sélection ;
3. elle a pu influencer une décision prise sur des données partagées.

La famille inclut notamment :

- les candidates perdantes ;
- les paramètres voisins ;
- les variantes abandonnées ;
- les niveaux de complexité ;
- les actifs séparément sélectionnables ;
- les seeds sélectionnables ;
- les modèles intermédiaires sélectionnables ;
- les modifications issues d’une inspection humaine ;
- les stress-tests utilisés pour modifier, retenir ou déployer une règle.

### 8.2 Nouvelle famille

Une nouvelle famille statistique n’est autorisée que si :

- les données de sélection sont nouvelles et non partagées ;
- aucun résultat antérieur n’a influencé la nouvelle spécification ou son espace de recherche ;
- aucun holdout consommé n’est recyclé ;
- l’indépendance informationnelle est documentée et approuvée.

Une hypothèse renommée ou reformulée ne suffit pas.

### 8.3 Historiques hétérogènes

Si des candidates disposent d’historiques structurellement incompatibles :

1. elles restent dans le registre global ;
2. des sous-familles homogènes peuvent être définies ex ante ;
3. la méthode hiérarchique requise relève de la SOP 02 ;
4. aucune valeur manquante ne peut être remplacée arbitrairement par zéro.

### 8.4 Walk-Forward

En Walk-Forward :

- un catalogue global versionné définit la sémantique des candidates ;
- chaque fold dispose d’une vue locale immuable du catalogue disponible à cette date ;
- chaque matrice locale est scellée avant son WRC local ;
- le registre global conserve le lignage entre folds ;
- les fenêtres et frontières sont définies par la SOP 04.

Ajouter, supprimer ou redéfinir une candidate entre folds crée une nouvelle version du processus.

---

## 9. Cas particuliers de comptage

### 9.1 Recherche exhaustive

Pour une grille cartésienne :

$$
M=\prod_{j=1}^{p}n_j
$$

uniquement si chaque combinaison :

- constitue une spécification distincte ;
- a effectivement produit une information exploitable ;
- était exposée à la sélection.

La taille théorique de la grille ne remplace pas le nombre réalisé.

### 9.2 Recherche adaptative

Pour un algorithme génétique, bayésien ou guidé :

$$
M_{\text{evaluated}}
=
\left|
\left\{
\text{candidates uniques ayant produit une information exploitable}
\right\}
\right|
$$

Le nombre de générations, d’itérations ou de paramètres théoriques ne remplace pas ce nombre.

### 9.3 Runs interrompus

Un run `ABORTED` ou `FAILED_TECHNICAL` est toujours enregistré.

Il entre dans l’effort réalisé si :

- un résultat partiel était accessible ;
- ce résultat a influencé la poursuite ou l’arrêt ;
- l’échec lui-même a révélé une information utilisée pour modifier la recherche.

Sinon, il reste traçable sans devenir une candidate évaluée supplémentaire.

### 9.4 Actifs

Le nombre d’actifs ne multiplie pas automatiquement le nombre de candidates.

- Une stratégie de portefeuille fixe produit une candidate de portefeuille.
- Si le meilleur couple règle-actif peut être sélectionné, chaque couple évalué est une candidate.
- Si l’univers d’actifs est sélectionnable ou modifié après observation, une nouvelle candidate ou version de processus est créée.

La frontière normative est la suivante :

- si l’allocation, les pondérations et les actifs sont fixés ex ante, la
  spécification décrit une candidate de portefeuille ;
- si la même logique est appliquée séparément à plusieurs actifs et que le
  processus peut retenir l’actif qui performe le mieux, chaque couple
  `stratégie × actif` évalué est une candidate distincte ;
- si un filtre, un classement ou un seuil d’éligibilité choisit les actifs à
  partir des données de sélection, ce mécanisme appartient au processus de
  recherche et ses sorties doivent rester reconstructibles ;
- aucun actif évalué ne peut être retiré de la famille parce que son résultat
  est médiocre, incomplet ou moins robuste.

L’objectif n’est pas de trouver une stratégie abstraite indépendante de tout
marché, mais d’identifier une spécification tradable : soit un couple
`stratégie × actif`, soit un portefeuille multi-actifs préenregistré.

### 9.5 Modèle de coûts

Une modification du modèle de coûts :

- crée une nouvelle candidate si elle intervient dans la sélection ;
- crée un run ou stress-test distinct si elle est purement descriptive et ne peut influencer la sélection ;
- doit toujours être enregistrée et versionnée.

### 9.6 Robustesse

Un stress-test appartient à la famille statistique lorsqu’il influence :

- la sélection ;
- une modification de règle ;
- la décision d’ouverture OOS ;
- la décision de déploiement.

Un stress-test purement descriptif peut être classé dans une famille secondaire, à condition que son résultat ne soit pas utilisé pour retoucher le processus.

---

## 10. Recherche humaine

Toute information issue notamment de :

- la lecture d’une equity curve ;
- l’inspection d’un trade ;
- l’analyse d’un drawdown ;
- l’observation d’une sous-période ;
- la comparaison visuelle de paramètres ;
- la lecture d’une métrique intermédiaire ;
- la connaissance d’un résultat antérieur ;

crée un événement d’observation.

Le fait qu’aucune décision immédiate ne soit déclarée ne supprime pas l’obligation d’enregistrement.

Toute candidate créée après une telle observation doit référencer l’événement causal.

---

## 11. Règles ML

Le registre ML conserve au minimum :

- les features proposées, utilisées ou retirées ;
- les transformations ;
- les architectures ;
- les hyperparamètres ;
- les seeds ;
- les epochs ;
- les checkpoints ;
- les règles d’arrêt ;
- les fonctions de perte ;
- les métriques de sélection ;
- les résultats de validation interne ;
- les modèles intermédiaires accessibles au sélecteur.

### 11.1 Seeds

Chaque seed est une candidate distincte lorsqu’elle peut être sélectionnée pour son résultat.

Une agrégation de seeds constitue une candidate unique seulement si :

- la règle d’agrégation est préenregistrée ;
- aucune seed individuelle ne peut être choisie ;
- la sortie agrégée est la seule information accessible au sélecteur.

### 11.2 Early stopping et checkpoints

Le modèle final produit par une règle d’arrêt préenregistrée constitue une candidate.

Chaque checkpoint devient une candidate distincte s’il est accessible ou sélectionnable selon ses performances.

Observer plusieurs checkpoints puis retenir le meilleur est une procédure de sélection multiple, même si un seul fichier de modèle est conservé.

---

## 12. Préenregistrement

Avant une expérience, enregistrer au minimum :

- l’hypothèse et $H_0$ ;
- l’univers ;
- le snapshot ou la règle de construction des données ;
- la segmentation prévue ;
- l’espace candidat ou son générateur ;
- la métrique primaire ;
- le benchmark ;
- le modèle de coûts ;
- l’algorithme de sélection ;
- les filtres d’éligibilité ;
- les tie-breaks ;
- la règle d’arrêt ;
- le traitement des échecs ;
- la règle de déduplication ;
- la politique de valeurs manquantes ;
- les critères `PASS`, `FAIL` et `INCONCLUSIVE`.

Pour une recherche adaptative, il n’est pas nécessaire de connaître ex ante tous les `CANDIDATE_ID`. Le générateur, ses contraintes et ses règles d’adaptation doivent toutefois être préenregistrés.

---

## 13. Données et snapshots

### 13.1 Contenu d’un snapshot

Un `DATA_SNAPSHOT_ID` identifie de manière immuable :

- les données sources ;
- leur schéma ;
- le calendrier ;
- le fuseau horaire ;
- l’univers d’actifs ;
- les ajustements ;
- les règles de nettoyage ;
- les exclusions ;
- les métadonnées fournisseur ;
- les hashes des artefacts pertinents.

Un chemin de fichier seul ne constitue pas un snapshot.

### 13.2 Correction de données

Une correction objective :

- ne remplace jamais silencieusement le snapshot initial ;
- crée un nouveau `DATA_SNAPSHOT_ID` ;
- conserve l’ancien snapshot ;
- relie le run initial, le diagnostic, le correctif et le run corrigé ;
- fait l’objet d’une revue indépendante si elle affecte une décision.

La correction ne doit pas être guidée par le signe ou le niveau de performance.

---

## 14. Contrat de la matrice de performance

### 14.1 Responsabilités

La SOP 03 définit :

- la provenance des colonnes ;
- la complétude du catalogue ;
- le lignage des séries ;
- l’unité temporelle canonique ;
- les règles de scellement.

La SOP 02 définit :

- la série différentielle utilisée ;
- les transformations statistiques ;
- le traitement statistique des historiques homogènes ;
- le bootstrap et les tests multiples.

### 14.2 Matrice locale

Pour chaque famille soumise à la SOP 02, le registre doit pouvoir générer une matrice avec :

- une colonne par candidate de la famille locale ;
- une ligne par journée de marché valide commune ;
- une série de rendement net mark-to-market ;
- un dictionnaire `CANDIDATE_ID → spécification` ;
- les métadonnées de provenance ;
- une politique explicite de données invalides ou manquantes.

### 14.3 Fréquence quotidienne

L’unité temporelle canonique est le rendement journalier.

Pour une stratégie intraday :

- les P&L nets sont agrégés par journée de marché ;
- le calendrier et le fuseau sont préenregistrés ;
- les coûts et ajustements sont appliqués avant agrégation.

Pour une position conservée plusieurs jours :

- le rendement est calculé quotidiennement en mark-to-market ;
- le P&L ne peut pas être reporté uniquement au jour de clôture ;
- le P&L final ne peut pas être réparti artificiellement entre les jours.

Un jour valide sans position reçoit un rendement de stratégie nul avant construction de la série différentielle prévue par la SOP 02 et la SOP 07.

### 14.4 Interdictions

Une candidate ne peut être omise parce que :

- sa performance est négative ;
- elle ressemble à une autre ;
- elle a été abandonnée ;
- elle dégrade la puissance statistique ;
- son run n’a pas été présenté dans le rapport final.

Une observation invalide requise par la matrice produit `INCONCLUSIVE` jusqu’à correction technique documentée.

Sont interdits :

- l’imputation arbitraire ;
- la suppression silencieuse d’une date ;
- l’usage discrétionnaire du dernier prix connu ;
- la correction guidée par la p-value ;
- le remplacement par zéro d’une observation réellement manquante.

### 14.5 Scellement

Avant toute inférence selon la SOP 02, la matrice est scellée avec :

- `MATRIX_ID` ;
- dimensions ;
- catalogue associé ;
- hash du catalogue ;
- hash des données ;
- hash de la matrice ;
- timestamp ;
- identité du producteur ;
- revue indépendante.

---

## 15. Statuts

Les statuts techniques d’un run sont séparés des statuts décisionnels du processus.

### 15.1 Statuts de run

```text
PLANNED
RUNNING
COMPLETED
FAILED_TECHNICAL
ABORTED
INVALID_DATA
SUPERSEDED
ARCHIVED
```

### 15.2 Statuts du processus ou de la candidate sélectionnée

```text
REJECTED
SELECTED
OOS_AUTHORIZED
OOS_OPENED
PAPER
LIVE
RETIRED
```

### 15.3 Transitions

Les transitions autorisées sont définies dans un schéma versionné.

Au minimum :

- `FAILED_TECHNICAL` désigne une incapacité technique objective à produire le résultat prévu ;
- `ABORTED` désigne un arrêt volontaire ou externe avant achèvement ;
- `INVALID_DATA` désigne un run dont les entrées violent le contrat de données ;
- `SUPERSEDED` désigne un artefact remplacé sans être supprimé ;
- `OOS_AUTHORIZED` ne peut être émis qu’après les gates applicables ;
- `OOS_OPENED` est irréversible pour le segment concerné ;
- `RETIRED` clôt l’exploitation sans supprimer l’historique.

Le chercheur ne choisit pas librement le statut. Chaque statut exige des critères objectifs et des preuves.

---

## 16. Journal technique append-only

### 16.1 Format normatif

Le registre normatif comprend :

- un journal `JSONL` append-only ;
- un schéma JSON versionné ;
- des vues matérialisées intégralement reconstructibles ;
- un manifeste des artefacts et hashes.

Les vues, tableaux et rapports ne remplacent pas le journal source.

### 16.2 Ordre et intégrité

Chaque événement contient :

- un numéro de séquence monotone ;
- son propre hash ;
- le hash de l’événement précédent ;
- un timestamp ;
- l’identité de l’émetteur ;
- le type d’événement ;
- la charge utile validée par schéma.

Le chaînage cryptographique doit rendre toute suppression, insertion ou modification rétrospective détectable.

### 16.3 Corrections

Un événement existant n’est jamais modifié.

Une correction crée un événement compensatoire contenant :

- l’identifiant de l’événement corrigé ;
- l’ancienne valeur ;
- la nouvelle valeur ;
- le motif ;
- les preuves ;
- l’identité du rôle autorisé ;
- l’approbation indépendante.

---

## 17. Champs obligatoires

### 17.1 Projet et hypothèse

```text
project_id:
hypothesis_id:
process_version_id:
rationale:
falsifiable_hypothesis:
null_hypothesis:
benchmark:
asset_universe:
asset_selection_axis:
primary_metric:
segmentation_protocol:
preregistered_at:
```

### 17.2 Famille

```text
research_family_id:
family_rationale:
shared_selection_data:
decision_target:
candidate_catalog_version:
parent_family_id:
independence_evidence:
```

### 17.3 Candidate

```text
candidate_id:
planned_spec_id:
parent_candidate_ids:
theme:
canonical_spec:
parameters:
direction:
entries:
exits:
sizing:
cost_model:
features:
complexity:
asset_scope:
seed:
creation_reason:
source_event_ids:
```

### 17.4 Run

```text
run_id:
candidate_id:
experiment_id:
research_family_id:
status:
code_commit:
config_hash:
data_snapshot_id:
environment_hash:
seed:
segment:
started_at:
finished_at:
return_series_path:
metrics_path:
log_path:
error_path:
decision_event_id:
```

### 17.5 Événement

```text
event_id:
sequence_number:
event_type:
actor:
observed_information:
affected_object_ids:
decision:
justification:
generated_candidate_ids:
previous_event_hash:
event_hash:
created_at:
```

---

## 18. Gate de complétude

Le gate est évalué au niveau de la famille et de la matrice locale de chaque fold.

### 18.1 `PASS`

Le registre est `PASS` si :

- tous les runs connus sont enregistrés ;
- toutes les candidates évaluées sont identifiables ;
- le lignage des décisions est complet ;
- les observations humaines sont tracées ;
- les séries de performance sont reconstructibles ;
- les snapshots, configurations et environnements sont identifiés ;
- la matrice complète peut être produite ;
- les hashes sont cohérents ;
- la revue indépendante est favorable.

### 18.2 `FAIL`

Le registre est `FAIL` en présence notamment de :

- suppression volontaire d’essais ;
- falsification ou altération du journal ;
- univers sciemment sous-déclaré ;
- résultats supprimés ;
- OOS réutilisé sans traçabilité ;
- contournement délibéré des règles de famille.

### 18.3 `INCONCLUSIVE`

Le registre est `INCONCLUSIVE` lorsqu’aucune conclusion défendable n’est possible, notamment en cas de :

- candidate influente non reconstructible ;
- historique incomplet sans preuve de falsification ;
- série requise perdue ;
- snapshot non identifiable ;
- matrice partiellement perdue ;
- dépendance informationnelle non résolue.

`INCONCLUSIVE` bloque :

- le verdict statistique ;
- le scellement confirmatoire ;
- l’ouverture OOS.

### 18.4 Régularisation

Un statut `INCONCLUSIVE` peut être régularisé uniquement par une reconstruction :

- objective ;
- auditée ;
- documentée ;
- indépendante du niveau de performance ;
- conservant tous les artefacts et diagnostics antérieurs.

Il est interdit de régulariser en réduisant la famille au sous-univers disponible.

---

## 19. Revue indépendante

Une revue indépendante est obligatoire :

- avant le scellement de chaque matrice ;
- avant l’ouverture de chaque OOS.

Elle vérifie au minimum :

- la conformité au schéma ;
- le lignage ;
- les frontières de famille ;
- le catalogue des candidates ;
- les séries ;
- les décisions humaines ;
- les snapshots ;
- la matrice ;
- les hashes ;
- les transitions de statut ;
- les corrections éventuelles.

La revue est enregistrée sous un `REVIEW_ID` immuable avec :

- l’identité du réviseur ;
- la portée ;
- les preuves examinées ;
- les anomalies ;
- le verdict ;
- le timestamp ;
- le hash du rapport.

Le chercheur principal ne peut pas constituer seul la revue indépendante.

---

## 20. Cycle de vie après OOS

La traçabilité continue après l’ouverture OOS.

Les événements suivants doivent être enregistrés :

- ouverture effective de l’OOS ;
- résultats OOS ;
- stress-tests ;
- décisions de paper trading ;
- incidents d’exécution ;
- modifications de production ;
- décisions de mise en live ;
- suspensions ;
- retrait.

Une variante créée après observation de l’OOS, de la robustesse, du paper ou du live :

- devient une descendante dans une nouvelle version de recherche ;
- conserve le lien avec la famille et les informations consommées ;
- ne réhabilite jamais l’OOS déjà ouvert ;
- exige de nouvelles données non consommées pour toute nouvelle confirmation.

---

## 21. Livrables obligatoires

Pour chaque famille et chaque matrice locale, archiver :

- le journal JSONL ;
- le schéma JSON ;
- les vues matérialisées ;
- le catalogue versionné ;
- le manifeste de complétude ;
- les snapshots de données ou leurs références immuables ;
- les configurations ;
- le code ;
- l’environnement ;
- les seeds ;
- les séries de performance ;
- les métriques ;
- les logs et erreurs ;
- les événements d’observation et de décision ;
- la matrice complète ;
- les rapports de revue ;
- les hashes.

Le manifeste minimal contient :

```text
[IDENTIFICATION]
project_id:
hypothesis_id:
process_version_id:
research_family_id:
fold_id:

[COUNTS]
planned_spec_count:
evaluated_candidate_count:
family_candidate_count:
run_count:
observation_event_count:
decision_event_count:

[CATALOG]
catalog_version:
catalog_hash:
deduplication_rule_version:

[DATA]
data_snapshot_id:
data_hash:
calendar:
timezone:
matrix_frequency: daily

[MATRIX]
matrix_id:
matrix_dimensions:
matrix_hash:
sealed_at:

[REPRODUCIBILITY]
code_commit:
config_hash:
environment_hash:
journal_head_hash:

[REVIEW]
review_id:
review_verdict:
oos_opening_authorized:
```

---

## 22. Reproductibilité

Une reproduction valide doit retrouver exactement :

- les identifiants ;
- l’ordre des événements ;
- la tête de chaîne du journal ;
- le catalogue ;
- les dimensions de la matrice ;
- les hashes des artefacts déterministes ;
- les décisions ;
- la candidate transmise ;
- les transitions de statut.

Pour un composant non déterministe, le protocole doit préenregistrer :

- les seeds ;
- les tolérances numériques ;
- les métriques comparées ;
- les invariants obligatoires ;
- les conditions d’acceptation.

Une tolérance inventée après observation est interdite.

Les contrôles minimaux comprennent :

- validation du schéma ;
- unicité des identifiants ;
- continuité des numéros de séquence ;
- validité du chaînage cryptographique ;
- résolution de tous les liens parents ;
- correspondance catalogue-matrice ;
- absence de candidate influente omise ;
- reproduction du rendement journalier mark-to-market ;
- reproduction du manifeste et des décisions.

---

## 23. Conservation

Les artefacts sont conservés :

- pendant toute la durée de recherche ;
- pendant toute l’utilisation de la stratégie ;
- pendant au moins dix ans après son statut `RETIRED`.

La conservation inclut les artefacts rejetés, invalides, remplacés ou négatifs.

L’archivage ne doit pas rompre :

- les liens de lignage ;
- la capacité de vérification des hashes ;
- la capacité de reconstruire les vues et matrices ;
- l’accès aux preuves de revue.

---

## 24. Erreurs interdites

- Compter seulement les règles terminées.
- Compter seulement la grille finale.
- Confondre spécifications planifiées et candidates évaluées.
- Fournir uniquement un compteur sans séries.
- Oublier les essais manuels.
- Omettre un accès humain à une sortie sensible.
- Réinitialiser l’effort après un échec ou un changement de nom.
- Multiplier mécaniquement règles × actifs.
- Compter une recherche adaptative par nombre d’itérations.
- Supprimer les règles négatives.
- Fusionner après observation deux spécifications séparément sélectionnables.
- Dédupliquer à partir de la performance observée.
- Ne conserver que les métriques agrégées.
- Écraser un snapshot corrigé.
- Modifier un événement existant.
- Corriger sans événement compensatoire.
- Utiliser une valeur manquante comme rendement nul.
- Calculer uniquement le P&L réalisé pour une position multi-jours.
- Ouvrir l’OOS sans revue indépendante.
- Réutiliser un OOS consommé pour confirmer une descendante.
- Réduire une famille incomplète au sous-univers reconstructible.
- Détruire les artefacts après rejet ou retrait.

---

## 25. Relations normatives avec les autres SOP

### SOP 01 — Estimation OOS

La SOP 03 enregistre l’ouverture, les résultats et le cycle de vie OOS. La SOP 01 définit l’estimation et l’intervalle de confiance sur la série OOS concaténée.

### SOP 02 — Inférence multiple

La SOP 03 fournit :

- la population opposable des candidates ;
- le catalogue ;
- les séries sources ;
- la matrice scellée ;
- le gate de complétude.

La SOP 02 transforme cette matrice et exécute WRC, SPA, Romano–Wolf et MCPM selon son propre domaine normatif.

### SOP 04 — Segmentation et Walk-Forward

La SOP 04 définit les fenêtres, folds, purges, embargos et calendriers. La SOP 03 enregistre les catalogues, runs, événements et matrices locales associés.

### SOP 07 — Detrending et zero-centering

La SOP 07 définit le benchmark, le detrending, le zero-centering et l’ordre des transformations. La SOP 03 conserve les entrées, sorties, versions et hashes permettant de les reproduire.

---

## 26. Modifications requises dans le protocole principal

Après adoption de cette SOP, `PROTOCOLE EBTA.md` doit :

1. définir la SOP 03 comme source de vérité du registre et des familles ;
2. remplacer le simple compteur global par un univers reconstructible ;
3. distinguer $M_{\text{planned}}$, $M_{\text{evaluated}}$ et $M_{\text{family}}$ ;
4. conserver $M_1$ et $M_2$ uniquement comme ventilations descriptives ;
5. imposer une matrice complète plutôt qu’un seul nombre $M$ ;
6. intégrer les observations humaines et recherches adaptatives ;
7. aligner les règles Walk-Forward avec le catalogue global versionné et les matrices locales ;
8. interdire toute déduplication rétroactive ;
9. imposer la revue indépendante avant scellement et ouverture OOS ;
10. aligner la conservation et le cycle de vie jusqu’au retrait.

---

## 27. Sources internes

- `Protocole/PROTOCOLE EBTA.md`
- `Protocole/SOP 01 - Estimation et intervalle de confiance OOS.md`
- `Protocole/SOP 02 - Inférence multiple WRC SPA Romano-Wolf MCP.md`
- `Protocole/SOP 04 - Segmentation temporelle et Walk-Forward.md`
- `Protocole/SOP 07 - Detrending benchmark et zero-centering.md`
- `Notes/82-L'Illusion du Minage de Données et le Mirage du Profit.md`
- `Notes/85-Le Minage de Données comme Procédure de Comparaisons Multiples.md`
- `Notes/86-Optimisation des Paramètres et Minage de Données Financières.md`
- `Notes/87-La Recherche de Règles en Minage de Données Financières.md`
- `Notes/88-L'Induction de Règles à Complexité Variable en Trading Objectif.md`
- `Notes/89-L’Induction face à la Recherche de Règles en Trading.md`
- `Notes/90-Analyse Comparative de la Recherche et de l'Induction de Règles.md`
- `Notes/129-L'Art de Discipliner le Minage de Données Financières.md`
- `Notes/159-Méthodologie de Data Mining sur le S&P 500.md`

---

## 28. Décision méthodologique synthétique

> **Le registre append-only constitue la source de vérité opposable de l’effort de recherche. Toute spécification ayant produit une information exploitable et susceptible d’influencer une décision appartient à la famille pertinente. Les candidates, runs, observations humaines, snapshots, lignages et séries doivent rester reconstructibles. La matrice quotidienne mark-to-market est scellée et revue indépendamment avant toute inférence et avant toute ouverture OOS. Une déduplication n’est admise qu’ex ante par une procédure automatique préenregistrée. Toute information consommée après l’OOS crée une nouvelle version de recherche sans restaurer la virginité des données déjà ouvertes.**
