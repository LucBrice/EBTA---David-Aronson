# Registre des risques de biais EBTA
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - REGISTRE_NORMATIF |
| Version documentaire | EBTA-DOC-1.1 |
| Date de gel documentaire | 2026-07-01 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 13 |
| Rôle dans le paquet EBTA | Taxonomie minimale des biais humains, méthodologiques, organisationnels et assistés par IA à contrôler par G-BIAS. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

Version documentaire : 2026-07-01

## Fonction

Ce registre définit les catégories minimales de biais à vérifier dans une
recherche EBTA. Il ne remplace pas le registre append-only de SOP 03 : il sert
de référentiel de classification pour les incidents et pour le gate `G-BIAS`.

---

## Niveaux applicables

Les niveaux `LEVEL_0` à `LEVEL_5` sont définis dans SOP 13. Chaque risque ci-dessous
doit être évalué au niveau réel de l'incident observé, pas au niveau théorique
indiqué par défaut.

---

## Taxonomie minimale

| ID | Catégorie | Description | Signaux d'alerte | Gravité par défaut | SOP propriétaires |
| --- | --- | --- | --- | --- | --- |
| `BIAIS_SELECTION` | Sélection opportuniste | Retrait, oubli, fusion ou promotion de candidates, actifs, folds ou runs selon leurs résultats. | Famille modifiée après observation ; actifs perdants absents ; matrice incomplète. | `LEVEL_2` | SOP 03, SOP 06, SOP 13 |
| `BIAIS_DATA_MINING_SCOPE` | Frontière statistique réduite | Réduction ex post de la population soumise au WRC ou séparation artificielle de familles liées. | WRC sur gagnante seule ; familles découpées après résultat. | `LEVEL_3` | SOP 02, SOP 03, SOP 13 |
| `BIAIS_METRIC_SHOPPING` | Metric shopping | Changement ou repondération de métrique primaire après résultat. | Sharpe, CAGR, PF ou drawdown deviennent critère principal après observation. | `LEVEL_3` | SOP 08, SOP 13 |
| `BIAIS_HURDLE_SHOPPING` | Hurdle shopping | Modification opportuniste d'un seuil économique, statistique ou de robustesse. | Seuil abaissé faute de preuve ; hurdle recalibré sur résultat. | `LEVEL_3` | SOP 01, SOP 05, SOP 08, SOP 13 |
| `BIAIS_BENCHMARK_SHOPPING` | Benchmark shopping | Benchmark, cash ou convention de detrending choisi selon le résultat. | Plusieurs benchmarks essayés et seul le favorable conservé. | `LEVEL_3` | SOP 07, SOP 08, SOP 13 |
| `BIAIS_COST_SHOPPING` | Coût ou exécution opportuniste | Choix de coût, slippage, impact, capacité ou sizing selon performance. | Coûts réduits après échec ; capital cible choisi au meilleur point. | `LEVEL_3` | SOP 09B, SOP 08, SOP 13 |
| `BIAIS_ROBUSTNESS_SHOPPING` | Robustesse opportuniste | Choix, retrait ou reclassification de scénarios de robustesse selon résultat. | Scénario échoué devient extrême ; voisinage réduit après observation. | `LEVEL_2` | SOP 05, SOP 13 |
| `BIAIS_OOS_PEEKING` | OOS peeking | Accès direct ou indirect à une information OOS avant autorisation ou avant décision gelée. | Lecture de fichier OOS ; résumé de résultat ; souvenir partagé. | `LEVEL_4` | SOP 10, SOP 13 |
| `BIAIS_REPAIR_AFTER_RESULT` | Réparation après résultat | Modification logique, paramètre, données ou sizing influencée par un résultat Test/OOS. | Bug invoqué sans preuve indépendante ; patch testé sur même OOS. | `LEVEL_4` | SOP 03, SOP 10, SOP 13 |
| `BIAIS_STOPPING` | Arrêt opportuniste | Arrêt, prolongement ou ajout de folds selon significativité ou P&L observé. | Point d'arrêt déplacé ; folds futurs ajoutés après échec. | `LEVEL_3` | SOP 01, SOP 04, SOP 13 |
| `BIAIS_REPORTING` | Narratif ou reporting sélectif | Présentation sélective des résultats, graphiques ou conclusions. | Seuls rapports favorables conservés ; limitations absentes. | `LEVEL_2` | SOP 12, SOP 13 |
| `BIAIS_ARCHIVE_OMISSION` | Omission d'archive | Artefact, incident, run, note ou version défavorable non conservé. | Paquet sans runs perdants ; historique écrasé. | `LEVEL_3` | SOP 03, SOP 12, SOP 13 |
| `BIAIS_AI_CONTAMINATION` | Contamination IA | Assistant IA ou outil externe a vu un résultat sensible et propose une décision ou réparation. | Prompt avec OOS ; suggestion de seuil après résultat ; résumé contaminé. | `LEVEL_3` | SOP 10, SOP 12, SOP 13 |
| `BIAIS_COMMUNICATION` | Communication influente | Pression, commentaire ou communication externe influence une décision EBTA. | Conclusion adaptée à un destinataire ; live poussé malgré gate incomplet. | `LEVEL_2` | SOP 11, SOP 12, SOP 13 |
| `BIAIS_DEVIATION` | Dérogation abusive | Dérogation utilisée pour contourner une interdiction ou réparer une preuve. | Dérogation rédigée après résultat ; exception permanente. | `LEVEL_4` | SOP 12, SOP 13 |

---

## Contrôle minimal par gate

| Moment | Catégories à vérifier explicitement |
| --- | --- |
| Avant `G8` | `BIAIS_SELECTION`, `BIAIS_DATA_MINING_SCOPE`, `BIAIS_ROBUSTNESS_SHOPPING`, `BIAIS_COST_SHOPPING`, `BIAIS_OOS_PEEKING`, `BIAIS_AI_CONTAMINATION` |
| Avant `G11` | Toutes les catégories, avec focus sur reporting, archive, reproduction, OOS et dérogations |
| Avant incubation/live | `BIAIS_REPORTING`, `BIAIS_COMMUNICATION`, `BIAIS_DEVIATION`, `BIAIS_ARCHIVE_OMISSION` |
| Après incident | Catégorie déclarée, catégories voisines et impact sur toutes les SOP consommatrices |

---

## Décision synthétique

> **Ce registre rend les biais humains et assistés par IA opposables. Une recherche EBTA ne peut pas être validée seulement parce que ses calculs passent ; elle doit aussi prouver que ses décisions, communications, corrections, dérogations et archives n'ont pas été orientées par les résultats observés.**
