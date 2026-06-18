# SOP 10 — Gouvernance OOS et gestion des échecs
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 10 |
| Rôle dans le paquet EBTA | Acces OOS, contamination, echecs, post-mortems et reexecutions techniques. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## 1. Statut et objet

- **Statut :** spécification normative de l’accès OOS, de la contamination, des verdicts et des réexécutions.
- **Architecture :** segments `OOS_k` successifs du Walk-Forward ; aucun holdout final supplémentaire.
- **Principe :** une information OOS observée ne redevient jamais vierge pour une version qu’elle a influencée.

Cette SOP définit :

- l’autorisation d’ouverture ;
- les artefacts gelés ;
- les états de l’OOS ;
- la taxonomie des verdicts ;
- les conséquences de chaque verdict ;
- la distinction entre erreur technique et nouvelle recherche ;
- la contamination collective ;
- les conditions exceptionnelles d’une réexécution.

---

## 2. Autorités normatives

La présente SOP applique :

- le gate OOS de la SOP 01 ;
- le WRC local de la SOP 02 ;
- le registre append-only et la revue indépendante de la SOP 03 ;
- le calendrier Walk-Forward de la SOP 04 ;
- la robustesse de la SOP 05 ;
- le gel de la candidate de la SOP 06 ;
- les données, métriques et exécution des SOP 07 à 09B ;
- le scellement pré-OOS et les preuves de la SOP 12.

Elle ne peut autoriser une ouverture interdite par une SOP antérieure.

---

## 3. Principe de virginité

Un segment OOS perd sa virginité dès qu’une information exploitable est révélée, notamment :

- performance ;
- signe ;
- p-value ;
- intervalle ;
- equity curve ;
- trade ;
- actif ;
- sous-période ;
- régime ;
- drawdown ;
- coût ;
- diagnostic.

La contamination ne dépend pas du format. Un graphique ou une conclusion verbale peut contaminer autant qu’un fichier chiffré.

---

## 4. Portée collective

La virginité concerne :

- chercheurs ;
- reviewers ;
- opérateurs ;
- équipes ;
- organisation ;
- projets ;
- agents automatisés ayant reçu les sorties.

Le registre conserve :

- personnes et systèmes ayant accès ;
- projets concernés ;
- fichiers et requêtes ;
- sorties et visualisations ;
- exports ;
- communications ;
- dates et finalités.

Une période largement étudiée ne peut être présentée comme un holdout neuf sans analyse de contamination historique.

---

## 5. Gate d’ouverture de `OOS_k`

L’ouverture exige simultanément :

1. WRC local primaire `PASS` ;
2. SPA, Romano–Wolf et MCPM traités comme secondaires ;
3. robustesse pré-OOS conforme ;
4. exécution, capacité et gate économique conformes ;
5. candidate et processus gelés ;
6. registre complet ;
7. artefacts hashés ;
8. plan d’analyse et sorties autorisées figés ;
9. revue indépendante ;
10. paquet SOP 12 au stade `PRE_OOS_SEALED` ;
11. accès journalisé.

Un SPA favorable ne peut renverser un WRC `FAIL` ou `INCONCLUSIVE`.

---

## 6. Artefacts gelés

Avant autorisation, geler et hasher :

- code ;
- état du worktree nécessaire ;
- configuration ;
- snapshot de données ;
- univers ;
- splits ;
- candidate ;
- seeds ;
- métriques ;
- benchmark ;
- coûts ;
- sizing ;
- modèles de fill et capacité ;
- plan d’analyse ;
- critères de verdict ;
- sorties autorisées ;
- environnement.

Un gel limité aux paramètres finaux est insuffisant.

---

## 7. Gouvernance d’accès

L’OOS est :

- chiffré ou isolé ;
- accessible seulement au pipeline autorisé ;
- associé à un projet et une famille ;
- protégé contre l’exploration directe ;
- journalisé.

Le pipeline ne produit que les sorties préenregistrées.

Toute nouvelle requête exige une autorisation et devient une information consommée.

---

## 8. États de l’OOS

```text
SEALED
AUTHORIZED
OPENED
BURNED
INVALID_TECHNICAL
ARCHIVED
```

### `SEALED`

Données protégées, aucune sortie observée.

### `AUTHORIZED`

Gate complet et approbation enregistrée.

### `OPENED`

Pipeline exécuté ou information révélée.

### `BURNED`

Période non vierge pour toute version influencée.

### `INVALID_TECHNICAL`

Le run ne mesure pas le processus gelé à cause d’une erreur objective.

### `ARCHIVED`

Artefacts et journal scellés après décision.

`INVALID_TECHNICAL` ne restaure pas automatiquement `SEALED`.

---

## 9. Fold sans déploiement

Après WRC local `FAIL` ou `INCONCLUSIVE` :

- aucune candidate n’est exécutée sur `OOS_k` ;
- le segment reste dans la série OOS globale ;
- la convention cash/non-déploiement est appliquée ;
- aucun rendement hypothétique du modèle refusé n’est calculé pour le verdict.

Exclure ce segment créerait un biais favorable.

---

## 10. Influence entre folds

Les résultats de `OOS_k` ne peuvent influencer le fold suivant.

Seules sont permises les adaptations :

- codées ;
- préenregistrées ;
- indépendantes du signe, du niveau et des diagnostics OOS ;
- appartenant au processus validé.

Toute autre influence :

- rompt le processus initial ;
- crée une nouvelle version ;
- interdit l’agrégation naïve des OOS antérieurs et postérieurs ;
- ne restaure pas la virginité des données observées.

---

## 11. Taxonomie des verdicts

Les dimensions suivantes restent distinctes :

- validité technique ;
- validité méthodologique ;
- preuve statistique ;
- performance économique ;
- état de contamination.

Le verdict global ne doit pas aplatir les causes.

---

## 12. `PASS`

Le processus est `PASS` seulement si :

- le run est techniquement et méthodologiquement valide ;
- le gate statistique de la SOP 01 est `PASS` ;
- le gate économique est `PASS` ;
- aucun invariant OOS n’est violé.

Seul ce statut autorise l’incubation confirmatoire de la SOP 11.

---

## 13. `NOT_VALIDATED`

Le statut est `NOT_VALIDATED` lorsque :

- le run est valide et informatif ;
- l’estimation primaire est positive ;
- la preuve statistique exigée n’est pas atteinte.

`NOT_VALIDATED` :

- n’est pas `PASS` ;
- n’autorise pas le live ;
- n’autorise pas une retouche ;
- n’autorise pas un retest sur les mêmes observations.

Des folds futurs ne peuvent être ajoutés que si le calendrier et le point d’arrêt étaient préenregistrés indépendamment du résultat.

---

## 14. `FAIL`

Le statut statistique est `FAIL` lorsque le run est valide et suffisamment informatif, mais :

$$
\hat\mu_{OOS}\leq0
$$

selon la SOP 01, ou lorsqu’une violation méthodologique irréparable impose ce statut.

Une borne basse insuffisante avec moyenne positive relève de `NOT_VALIDATED`, non de `FAIL`.

---

## 15. `REJECTED_ECONOMIC`

Le statut est `REJECTED_ECONOMIC` lorsque :

- le gate statistique est `PASS` ;
- mais le rendement net, le risque, le drawdown, les coûts, la capacité ou l’exécutabilité échouent.

Il ne doit pas être présenté comme un échec statistique de l’alpha.

---

## 16. `INCONCLUSIVE`

Le statut est `INCONCLUSIVE` lorsqu’une cause préspécifiée empêche de conclure, notamment :

- données invalides ;
- information insuffisante ;
- série primaire non reconstructible ;
- non-déterminisme hors tolérance ;
- incident externe matériel.

Il n’autorise ni baisse du niveau de confiance, ni changement de métrique, ni réparation du modèle.

---

## 17. `INVALID_TECHNICAL`

Une invalidité technique est une erreur objective qui empêche de mesurer le processus gelé :

- données corrompues ;
- mauvais fichier ;
- exécution interrompue ;
- calcul non conforme ;
- bug de reporting ou d’infrastructure prouvé.

Une mauvaise performance, un coût élevé ou un drawdown ne sont pas des bugs.

---

## 18. Conséquences de `FAIL` ou `REJECTED_ECONOMIC`

Après le verdict :

- archiver la version ;
- enregistrer l’échec ;
- interdire toute modification fondée sur les détails OOS ;
- interdire le même OOS pour une descendante influencée ;
- ne pas passer en incubation ;
- attendre des observations réellement futures pour une nouvelle confirmation.

Un post-mortem peut produire de la connaissance, jamais une revalidation sur le même OOS.

---

## 19. Conséquences de `NOT_VALIDATED`

La stratégie n’est pas déployable.

Les options sont :

- poursuivre le calendrier déjà préenregistré ;
- attendre de nouvelles observations futures ;
- archiver ;
- effectuer du paper non confirmatoire clairement étiqueté.

Il est interdit :

- d’allonger l’OOS vers le passé ;
- de changer le niveau de confiance ;
- de changer la métrique ;
- de déclarer un `PASS` économique compensatoire.

---

## 20. Conséquences de `INCONCLUSIVE`

Suivre la politique ex ante :

- correction technique admissible ;
- attente de données futures ;
- archivage ;
- nouveau cycle.

Le statut ne vaut pas autorisation de retester librement.

Dans l’architecture actuelle, « nouvelles données » signifie des observations arrivant réellement après la frontière, non un quatrième segment final découpé dans l’historique déjà utilisé.

---

## 21. Analyse post-mortem

Le post-mortem est étiqueté :

```text
POST_OOS_RESEARCH
```

Il peut examiner :

- données ;
- régime ;
- coûts ;
- exposition ;
- instabilité ;
- outliers ;
- exécution ;
- surapprentissage.

Toute idée issue de cette analyse :

- devient une nouvelle expérience ;
- appartient au registre ;
- conserve le lignage ;
- nécessite des données futures ;
- ne peut être validée sur l’ancien OOS.

---

## 22. Conditions d’une réexécution technique

Une réexécution sur le même OOS exige :

1. erreur objective démontrée indépendamment de la performance ;
2. cause précise ;
3. preuve que la logique alpha, les paramètres économiques et la sélection ne changent pas ;
4. correctif minimal ;
5. revue indépendante ;
6. conservation du run initial ;
7. décision écrite avant le rerun ;
8. absence de comparaison de variantes sur OOS ;
9. nouvel artefact versionné ;
10. journal complet.

---

## 23. Virginité après invalidité

Une revue indépendante détermine :

- quelles sorties ont été révélées ;
- qui y a eu accès ;
- si le niveau ou le signe de performance était visible ;
- si le correctif a pu être influencé ;
- quelle portée reste valide.

La suppression des fichiers ou l’étiquette « bug » ne restaure rien.

---

## 24. Bug affectant la logique économique

Si le bug modifie :

- signal ;
- feature ;
- univers ;
- paramètres ;
- sizing ;
- coûts ;
- fills ;
- positions ;
- série primaire ;
- règle de sélection,

la correction crée une nouvelle candidate/version.

L’ancien OOS est brûlé pour cette version.

---

## 25. Bug de reporting sans effet primaire

Une correction technique peut être admise si une preuve démontre l’invariance de :

- signaux ;
- ordres ;
- fills ;
- positions ;
- séries quotidiennes ;
- métriques ;
- gates.

Le rapport corrigé est une nouvelle version et l’incident reste archivé.

---

## 26. Conception du correctif

Le correctif doit découler de la spécification de l’erreur.

Il ne peut utiliser :

- signe du P&L ;
- niveau de performance ;
- trade défavorable ;
- sous-période ;
- résultat de plusieurs correctifs concurrents.

Tester plusieurs corrections sur le même OOS constitue une nouvelle recherche contaminée.

---

## 27. Famille contaminée

Appartient à la même famille contaminée toute variante motivée par :

- trade OOS ;
- période ;
- actif ;
- régime ;
- risque ;
- coût ;
- exposition ;
- métrique ;
- visualisation ;
- conclusion OOS.

Changer de nom, seed ou paramètre ne crée pas une indépendance.

---

## 28. Nouvelle hypothèse substantielle

Une nouvelle hypothèse est distincte seulement si :

- son rationnel ne repose pas sur les détails OOS ;
- sa structure est substantiellement différente ;
- son lignage est déclaré ;
- son protocole est préenregistré ;
- sa confirmation utilise des observations futures.

La charge de preuve de l’indépendance appartient au projet.

---

## 29. Journal d’accès

Le journal append-only enregistre :

- identités humaines et systèmes ;
- projet et famille ;
- date/heure ;
- ressource ;
- requête ;
- sortie ;
- visualisation ;
- export ;
- destinataire ;
- justification ;
- approbation.

Toute ouverture ou réouverture exige un gate machine et une approbation humaine indépendante enregistrée.

---

## 30. Livrable obligatoire

```text
[OOS ACCESS]
project_id:
research_family_id:
fold_id:
dataset_id:
status_before:
authorized_by:
opened_at:
users_and_systems:
access_log_hash:

[FROZEN ARTIFACTS]
code_hash:
worktree_hash:
config_hash:
data_hash:
universe_hash:
analysis_plan_hash:
environment_hash:

[RESULT]
technical_validity:
methodological_validity:
statistical_verdict:
economic_verdict:
global_verdict:
oos_status_after:

[CONTAMINATION]
information_revealed:
projects_affected:
family_scope:

[RERUN]
requested:
error_specification:
independent_review:
authorized:
corrective_version:

[NEXT ACTION]
archive:
future_data_required:
paper_non_confirmatory:
incubation_authorized:
```

---

## 31. Contrôles de complétude

Vérifier :

- tous les accès présents ;
- tous les runs présents, y compris décevants ou invalides ;
- états cohérents ;
- artefacts hashés ;
- décisions signées ;
- liens avec SOP 03 ;
- absence de réouverture automatique ;
- conservation de chaque version.

Omettre un run OOS défavorable est une violation méthodologique.

---

## 32. Erreurs interdites

- Réoptimiser après OOS.
- Appeler une mauvaise performance « bug ».
- Retester une correction logique sur le même OOS.
- Utiliser le fold suivant comme examen après réparation.
- Ajouter un holdout historique final.
- Confondre `FAIL` et `REJECTED_ECONOMIC`.
- Transformer `NOT_VALIDATED` ou `INCONCLUSIVE` en `PASS`.
- Considérer une contamination individuelle seulement.
- Omettre une visualisation ou communication du journal.

---

## 33. Sources internes

- `Notes/121-La Validation Hors-Échantillon L'Épreuve de Réalité Statistique.md`
- `Notes/123-L'Éphémère Rigueur Limites des Tests Hors-Échantillon.md`
- `Notes/168-GESTION RIGOUREUSE DE L’ÉCHEC EN VALIDATION OUT-OF-SAMPLE (OOS).md`
- `Notes/171-Le moment du test d'hypothèse dans le processus EBTA.md`
- `Notes/172-Justification de la performance en OOS, rôle du test d'hypothèse.md`
- `Notes/173-Le rôle de l'OOS, estimation et stabilité dans l'EBTA.md`
- `Notes/174-Faut-il réaliser un test d'hypothèse sur l'OOS.md`

---

## 34. Décision méthodologique synthétique

> **Un segment OOS n’est vierge qu’une fois et sa contamination concerne toute l’organisation. Seul un WRC local `PASS`, accompagné de tous les gates pré-OOS et d’artefacts gelés, autorise l’ouverture. Les verdicts `PASS`, `NOT_VALIDATED`, `FAIL`, `REJECTED_ECONOMIC`, `INCONCLUSIVE` et `INVALID_TECHNICAL` restent distincts. Une réexécution même-OOS n’est admise que pour une erreur objective, minimale et indépendante de la performance ; tout changement de logique crée une nouvelle candidate nécessitant des observations futures. Aucun holdout final historique supplémentaire n’est ajouté.**
