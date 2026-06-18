# SOP 11 — Incubation, passage live et monitoring séquentiel
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 11 |
| Rôle dans le paquet EBTA | Incubation, passage live limite, monitoring sequentiel, suspension et retrait. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## 1. Statut et objet

- **Statut :** spécification normative du passage du processus validé vers l’exploitation.
- **Chemin autorisé :**

```text
PASS OOS global
  → paper trading opérationnel
  → live limité
  → paliers de capital
  → live cible
  → monitoring et gouvernance
```

Cette SOP vérifie l’opérationnalisation du processus gelé. Elle ne constitue ni une nouvelle sélection, ni une réparation de l’alpha, ni un holdout final implicite.

---

## 2. Autorités normatives

La présente SOP consomme :

- le verdict global de la SOP 01 ;
- la gouvernance OOS de la SOP 10 ;
- le paquet reproductible de la SOP 12 ;
- les données point-in-time de la SOP 09A ;
- l’exécution, la capacité et le sizing de la SOP 09B ;
- les métriques et gates de la SOP 08 ;
- le calendrier adaptatif de la SOP 04.

Elle ne peut transformer un statut non `PASS` en autorisation de déploiement.

---

## 3. Prérequis à l’incubation confirmatoire

Avant paper trading :

- verdict statistique `PASS` ;
- gate économique `PASS` ;
- robustesse `PASS` ;
- exécution/capacité `PASS` ;
- aucune invalidité méthodologique ;
- paquet SOP 12 au stade `VALIDATION_READY` et gate de reproduction `PASS` ;
- code et configuration gelés ;
- infrastructure testée ;
- limites de risque et kill switch définis ;
- seuils de monitoring préenregistrés ;
- plan d’incident ;
- propriétaire opérationnel ;
- approbation indépendante.

`NOT_VALIDATED`, `FAIL`, `REJECTED_ECONOMIC` et `INCONCLUSIVE` n’autorisent pas l’incubation confirmatoire.

---

## 4. Rôle du paper trading

Le paper trading vérifie prospectivement :

- réception des données ;
- calcul des features ;
- reproduction des signaux ;
- chronologie des ordres ;
- fills ;
- coûts ;
- positions ;
- risque ;
- infrastructure ;
- monitoring.

Il n’autorise pas :

- réoptimisation ;
- changement de métrique ;
- modification alpha ;
- choix d’un nouveau sizing ;
- requalification du verdict OOS.

---

## 5. Données paper

Utiliser les flux réellement reçus :

- timestamps ;
- latences ;
- erreurs ;
- données manquantes ;
- corrections ;
- univers ;
- corporate actions ;
- versions de schéma.

Conserver les données brutes reçues et les transformations.

Remplacer après coup une donnée défectueuse par un historique nettoyé peut servir au diagnostic, mais ne doit pas masquer l’incident opérationnel.

---

## 6. Reproductibilité des signaux

Pour chaque décision, conserver :

- données d’entrée ;
- version du code ;
- configuration ;
- features ;
- signal attendu ;
- signal produit ;
- écart ;
- cause.

Le même code et la même configuration doivent reproduire le signal dans la tolérance déterministe.

Toute divergence non expliquée est bloquante.

---

## 7. Ordres et fills paper

Les règles sont celles de la SOP 09B.

Journaliser :

- signal ;
- ordre ;
- type ;
- quantité ;
- soumission ;
- première éligibilité ;
- prix théorique ;
- fill simulé ;
- spread ;
- slippage ;
- impact ;
- partial/no fill ;
- position ;
- P&L ;
- coûts.

Il est interdit de supposer tous les ordres remplis.

---

## 8. Durée et minimum informationnel

La durée calendaire est un plancher, non une preuve suffisante.

Préenregistrer :

- jours calendaires ;
- jours de marché ;
- signaux ;
- décisions ;
- ordres ;
- fills ;
- trades clôturés ;
- exposition cumulée ;
- turnover ;
- cycles de recalibration ;
- risques/régimes matériels ;
- incidents admissibles.

Un plancher de 90 jours peut être retenu, mais ne remplace aucun minimum informationnel.

---

## 9. Régimes et risques matériels

Le plan identifie ex ante les conditions dont l’absence limiterait la preuve :

- volatilité ;
- liquidité ;
- tendance/range ;
- stress de marché ;
- calendrier ;
- financement ;
- capacité.

Il n’est pas nécessaire d’attendre tous les régimes historiques.

Une couverture insuffisante d’un risque matériel peut produire `INCONCLUSIVE` selon une règle bornée, sans prolongation opportuniste indéfinie.

---

## 10. Comparaison paper / modèle

Comparer :

- signal ;
- timing ;
- ordre ;
- fill ;
- coût ;
- exposition ;
- turnover ;
- P&L ;
- drawdown ;
- latence ;
- taux de rejet ;
- données.

Décomposer :

$$
\Delta PnL=
\Delta signal+
\Delta timing+
\Delta fill+
\Delta cost+
\Delta data+
\Delta market.
$$

Une divergence économique n’est attribuée à un régime qu’après exclusion des causes opérationnelles.

---

## 11. Verdict paper

### `PASS`

- minimum informationnel atteint ;
- aucune anomalie critique ouverte ;
- signaux reproductibles ;
- ordres/fills/coûts dans les tolérances ;
- limites de risque respectées ;
- aucune modification alpha.

### `FAIL`

- bug critique ;
- données non fiables ;
- divergence de version ;
- exécution irréaliste ;
- violation de risque ;
- incompatibilité opérationnelle structurelle.

### `INCONCLUSIVE`

- information insuffisante ;
- exposition trop faible ;
- risque matériel non observé ;
- incident externe rendant l’échantillon inutilisable.

`INCONCLUSIVE` prolonge la collecte uniquement selon une règle préenregistrée.

---

## 12. Mauvaise performance paper

Une mauvaise performance :

1. déclenche la décomposition de la section 10 ;
2. n’autorise pas une réoptimisation ;
3. n’autorise pas une nouvelle métrique ;
4. peut conduire à `FAIL`, `INCONCLUSIVE`, `WATCH` ou archivage selon la cause.

Toute modification alpha crée une nouvelle recherche et les observations déjà vues restent contaminées.

---

## 13. Premier live limité

Le premier déploiement utilise :

- capital plafonné ;
- levier réduit ;
- participation réduite ;
- limites renforcées ;
- surveillance accrue ;
- kill switch testé ;
- procédure de rapprochement quotidienne.

Le capital initial est fondé sur le risque et la perte plausible, non sur le rendement espéré.

---

## 14. Détermination du capital initial

Le capital respecte le minimum des limites suivantes :

- budget de risque ;
- perte journalière ;
- drawdown tolérable ;
- liquidité ;
- capacité ;
- marge ;
- concentration ;
- erreur opérationnelle plausible.

Une fraction fixe universelle n’est pas une justification suffisante.

---

## 15. Paliers de capital

Chaque palier préenregistre :

- capital ;
- levier ;
- participation ;
- durée minimale ;
- information minimale ;
- coûts admissibles ;
- capacité requise ;
- drawdown maximal ;
- incidents bloquants ;
- reviewer.

La performance positive seule n’autorise jamais une montée.

---

## 16. Condition de montée

Le passage au palier suivant exige :

- aucun incident critique ;
- exécution conforme ;
- coûts compatibles ;
- capacité suffisante ;
- limites de risque respectées ;
- minimum informationnel atteint ;
- rapprochements complets ;
- approbation indépendante.

La limite supérieure reste le minimum des contraintes de risque, liquidité, capacité, marge et opérations.

---

## 17. Kill switch

Le contrat définit :

- déclencheurs ;
- seuils ;
- données sources ;
- actions ;
- autorité ;
- liquidation ou gel ;
- communications ;
- tests périodiques ;
- réarmement ;
- journal.

Le kill switch opérationnel agit immédiatement et reste distinct du monitoring statistique.

---

## 18. Incidents

Un incident suit :

```text
DETECT
→ CONTAIN
→ RECONCILE
→ CLASSIFY
→ CORRECT
→ TEST
→ REVIEW
→ RESUME or RETIRE
```

Conserver :

- cause ;
- portée ;
- positions ;
- ordres ;
- pertes ;
- données ;
- version ;
- correctif ;
- preuves.

Une réparation silencieuse est interdite.

---

## 19. Suspension immédiate

Peuvent déclencher `SUSPENDED` sans attendre une preuve statistique :

- données invalides ;
- ordres dupliqués ;
- position orpheline ;
- exposition excessive ;
- perte limite ;
- violation réglementaire ;
- divergence de code ;
- panne ;
- réconciliation impossible.

La protection opérationnelle ne constitue pas un test d’alpha.

---

## 20. Reprise après suspension

La reprise exige :

- cause identifiée ;
- positions et cash réconciliés ;
- correctif technique validé ;
- preuve de non-modification alpha ;
- tests de non-régression ;
- kill switch opérationnel ;
- approbation indépendante.

Une récupération du P&L ne suffit pas.

---

## 21. Changement alpha en production

Toute modification de :

- logique ;
- feature ;
- univers ;
- paramètre hors recalibration validée ;
- métrique ;
- sizing influent ;
- exécution influente

crée une nouvelle version de recherche soumise au cycle complet.

Un test A/B sur capital réel ne remplace pas la validation.

---

## 22. Recalibration normale

Une stratégie adaptative suit exclusivement :

- la fréquence Walk-Forward validée ;
- les données alors disponibles ;
- le même espace de recherche ;
- les mêmes gates ;
- la même politique `NO_MODEL` ;
- le même versionnement.

Une recalibration exceptionnelle déclenchée par une mauvaise performance est interdite, sauf si cette règle faisait partie du processus initial.

---

## 23. Deux couches de monitoring

### 23.1 Opérationnel continu

Contrôles immédiats de :

- données ;
- code ;
- ordres ;
- positions ;
- cash ;
- coûts ;
- exposition ;
- risque ;
- réglementation ;
- infrastructure.

### 23.2 Statistique planifié

Évaluation :

- à dates fixes ;
- après nombres d’observations fixés ;
- ou selon une procédure séquentielle préenregistrée.

Les deux couches ont des seuils, actions et autorités distincts.

---

## 24. Peeking et erreur séquentielle

Comparer chaque jour à un intervalle fixe et agir à la première sortie multiplie les faux signaux.

Le monitoring statistique utilise :

- calendrier fixe ;
- taille d’information fixe ;
- ou procédure séquentielle valide.

Les seuils ne changent pas après observation.

---

## 25. Procédures séquentielles admissibles

Selon le projet :

- alpha-spending ;
- e-values ;
- SPRT ;
- autre méthode validée.

Le contrat précise :

- hypothèses ;
- statistique ;
- fréquence ;
- horizon ;
- budget d’erreur ;
- frontières ;
- actions ;
- règles d’arrêt ;
- traitement de dépendance.

Répéter quotidiennement un test à 5 % sans correction est interdit.

---

## 26. Baseline de monitoring

La baseline utilise :

- distribution OOS ;
- série économique validée ;
- modèle de coûts ;
- expositions comparables ;
- incertitude ;
- capacité ;
- fréquence.

La performance Test optimisée ou la meilleure année historique ne constituent pas une baseline valide.

---

## 27. Fenêtres

Conserver au minimum :

- court terme opérationnel ;
- moyen terme correspondant au cycle ;
- long terme pour la stabilité de l’edge.

Pour chaque horizon, préenregistrer :

- métriques ;
- seuils ;
- action ;
- minimum d’information ;
- recouvrement ;
- priorité en cas de conflit.

Choisir la fenêtre qui alerte le plus favorablement est interdit.

---

## 28. États de production

```text
ACTIVE
WATCH
REDUCE
SUSPENDED
RETIRED
```

Les transitions sont mécaniques, journalisées et réversibles seulement selon leur contrat.

---

## 29. `WATCH`

`WATCH` implique :

- surveillance renforcée ;
- diagnostic ;
- aucune modification alpha ;
- aucune augmentation de risque ;
- calendrier de revue.

---

## 30. `REDUCE`

`REDUCE` applique une réduction mécanique préenregistrée du capital ou du risque.

Il est interdit :

- d’optimiser un nouveau sizing ;
- de masquer les signaux perdants ;
- de fermer seulement les trades défavorables.

---

## 31. `SUSPENDED`

La stratégie ne prend plus de nouveau risque selon le plan de suspension.

Les positions existantes sont gérées selon une procédure préenregistrée.

La reprise suit la section 20.

---

## 32. `RETIRED`

La version est définitivement arrêtée.

Le plan précise :

- liquidation ;
- communications ;
- date ;
- motif ;
- artefacts ;
- conservation ;
- impact sur les stratégies dépendantes.

L’historique n’est jamais supprimé et l’ancien OOS n’est pas réutilisé.

---

## 33. Réconciliation live

Chaque journée réconcilie :

- version déployée ;
- données ;
- signaux ;
- ordres ;
- fills ;
- positions ;
- cash ;
- coûts ;
- financement ;
- NAV ;
- limites.

Un écart matériel bloque ou escalade selon le plan d’incident.

Le seul P&L du broker n’est pas une réconciliation complète.

---

## 34. Changement des seuils de monitoring

Toute modification :

- crée une version de monitoring ;
- documente le motif ;
- reçoit une approbation ;
- s’applique prospectivement ;
- ne requalifie pas rétroactivement les observations.

Une modification influencée par la performance appartient à la gouvernance de recherche.

---

## 35. Livrable obligatoire

```text
[INCUBATION]
strategy_version:
validation_package_id:
validation_package_stage:
start_date:
minimum_calendar_days:
minimum_signals:
minimum_fills:
minimum_exposure:
required_risks:

[TRACKING]
signal_match:
latency:
fill_rate:
slippage_expected:
slippage_realized:
cost_delta:
pnl_delta:

[LIVE STAGE]
state:
capital:
leverage:
participation:
stage_gate:

[RISK]
limits:
kill_switch_status:
drawdown:
reconciliation:

[MONITORING]
operational_rules_version:
statistical_rules_version:
error_budget:
next_review:

[DECISION]
status:
action:
approved_by:
timestamp:
```

Le journal complet est append-only et hashé.

---

## 36. Erreurs interdites

- Incuber un statut autre que `PASS`.
- Utiliser paper pour réoptimiser.
- Déclarer 90 jours suffisants sans information minimale.
- Monter en capital sur performance seule.
- Utiliser un test fixe quotidien sans correction.
- Modifier l’alpha sous `WATCH` ou `REDUCE`.
- Reprendre après suspension sans réconciliation.
- Recalibrer exceptionnellement après pertes.
- Modifier rétroactivement un seuil.
- Supprimer l’historique d’une stratégie retirée.

---

## 37. Sources internes

- `Notes/4-L'Intégrité du Backtesting Biais d'Anticipation et Coûts Réels.md`
- `Notes/71-Inférence Statistique Les Pièges du Trader et Risques d'Erreur.md`
- `Notes/76-L'Estimation Statistique de la Performance en Trading.md`
- `Notes/78-Intervalles de Confiance Mesurer l'Incertitude du Backtesting.md`
- `Notes/121-La Validation Hors-Échantillon L'Épreuve de Réalité Statistique.md`
- `Notes/123-L'Éphémère Rigueur Limites des Tests Hors-Échantillon.md`
- `Notes/168-GESTION RIGOUREUSE DE L’ÉCHEC EN VALIDATION OUT-OF-SAMPLE (OOS).md`
- `Notes/173-Le rôle de l'OOS, estimation et stabilité dans l'EBTA.md`

---

## 38. Décision méthodologique synthétique

> **Seul un processus ayant obtenu un véritable `PASS` statistique et économique peut entrer en incubation confirmatoire. Le paper trading vérifie prospectivement les données, signaux, ordres, fills, coûts, risques et infrastructures du processus gelé ; il ne sert jamais à le réparer. Le live commence à capital limité et progresse par paliers fondés sur le risque, la capacité et la conformité opérationnelle. Le monitoring opérationnel agit immédiatement, tandis que le monitoring statistique suit un calendrier ou une procédure séquentielle préenregistrée contrôlant les consultations répétées. Toute modification alpha repart en recherche.**
