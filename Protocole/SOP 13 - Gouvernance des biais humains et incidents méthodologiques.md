# SOP 13 — Gouvernance des biais humains et incidents méthodologiques
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.1 |
| Date de gel documentaire | 2026-07-01 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | Gouvernance protocole EBTA |
| Rôle dans le paquet EBTA | Définir la prévention, la détection, la qualification et la conséquence des biais humains ou assistés par IA dans une recherche EBTA. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

Version documentaire : 2026-07-01

## 1. Statut et objet

- **Statut :** spécification normative de gouvernance des biais humains, incidents méthodologiques, dérogations et contaminations de recherche.
- **Objet :** protéger le protocole EBTA contre les décisions influencées par résultat, mémoire humaine, communication externe, pression opérationnelle, assistant IA ou sélection opportuniste non capturée par les seuls tests statistiques.
- **Principe :** tout biais détecté devient un événement de recherche opposable. Il doit être enregistré, qualifié, rattaché aux artefacts affectés et traité avant ouverture OOS, validation reproductible, incubation ou live.

Cette SOP ne remplace pas les SOP statistiques. Elle ajoute un contrôle transversal
sur la conduite de recherche qui peut bloquer un gate même si les calculs
statistiques semblent favorables.

---

## 2. Autorités normatives

La SOP 13 consomme et complète :

- SOP 02 pour la correction du data-mining bias par inférence multiple ;
- SOP 03 pour le registre append-only, les familles, runs, observations humaines et événements ;
- SOP 05 pour les stress-tests, scénarios et diagnostics de robustesse ;
- SOP 08 pour les métriques, hurdles, benchmarks, coûts et série primaire ;
- SOP 10 pour l'accès OOS, la contamination, les réexécutions et post-mortems ;
- SOP 12 pour les paquets, checksums, reproduction indépendante et preuves de gates.

Le registre des catégories de biais est `Protocole/BIAS_RISK_REGISTER.md`.
Les formats minimaux sont :

- `Protocole/TEMPLATE - Incident de biais EBTA.md` ;
- `Protocole/TEMPLATE - Dérogation méthodologique EBTA.md`.

---

## 3. Définition d'un incident de biais

Un incident de biais est tout événement, omission, communication, analyse,
interaction humaine ou assistée par IA qui peut modifier ou orienter :

- l'univers de recherche ;
- l'identité d'une candidate ;
- la famille statistique opposable ;
- une métrique, un hurdle, un benchmark ou un coût ;
- un scénario de robustesse ;
- le choix d'ouvrir, fermer, réexécuter ou ignorer un OOS ;
- un verdict, une conclusion, une note de recherche ou une décision de passage.

L'intention n'est pas requise. Un incident involontaire reste un incident s'il
peut influencer une décision EBTA.

---

## 4. Niveaux de gravité

| Niveau | Statut | Définition | Conséquence minimale |
| --- | --- | --- | --- |
| `LEVEL_0` | `INFO` | Observation sans influence plausible sur une décision ou un artefact. | Enregistrement optionnel ou note de contexte. |
| `LEVEL_1` | `MINOR` | Écart mineur avant décision, sans accès à résultat sensible et corrigible sans effet méthodologique. | Correction documentée, revue locale. |
| `LEVEL_2` | `MATERIAL_PRE_OOS` | Biais plausible avant OOS pouvant affecter famille, métrique, seuil, benchmark, coût, scénario ou sélection. | Incident obligatoire, correction avant G-BIAS, revue indépendante. |
| `LEVEL_3` | `OOS_EXPOSURE_RISK` | Accès, communication ou raisonnement pouvant intégrer une information OOS non prévue. | Blocage de l'ouverture ou de la poursuite OOS jusqu'à post-mortem SOP 10/SOP 13. |
| `LEVEL_4` | `CONTAMINATED_DECISION` | Décision déjà prise sous influence plausible d'un résultat sensible ou d'une sélection opportuniste. | Nouvelle candidate/version ou statut bloquant ; le segment exposé peut être `BURNED`. |
| `LEVEL_5` | `IRREPARABLE` | Omission, falsification, sélection opportuniste ou contamination qui rend la preuve non opposable. | `FAIL` méthodologique, archivage, interdiction de réparation sur les mêmes données. |

Un niveau peut être relevé par revue indépendante. Il ne peut être abaissé que
par preuve positive, datée et indépendante de la performance observée.

---

## 5. Gate transversal `G-BIAS`

`G-BIAS` est un gate transversal de gouvernance. Il ne renumérote pas `G0` à
`G14`. Il doit être explicitement évalué :

1. avant `G8 - Ouverture OOS` ;
2. avant `G11 - Validation reproductible` ;
3. avant toute dérogation méthodologique ;
4. après tout incident `LEVEL_2` ou supérieur ;
5. avant incubation ou live si un incident reste ouvert.

### Conditions `PASS`

`G-BIAS` passe seulement si :

- le registre append-only contient les incidents et revues applicables ;
- les catégories du `BIAS_RISK_REGISTER.md` ont été passées en revue ;
- aucun incident `LEVEL_2` ou supérieur n'est non résolu ;
- les éventuelles dérogations sont préexistantes, approuvées et non réparatrices ;
- aucun résultat OOS, économique, robuste ou reproductible n'a servi à changer une règle décisionnelle ;
- le reviewer indépendant confirme que les artefacts de preuve sont suffisants.

### Sorties possibles

| Sortie | Sens | Conséquence |
| --- | --- | --- |
| `PASS` | Aucun biais ouvert ne menace la décision. | Le gate consommateur peut continuer. |
| `FAIL` | Une violation méthodologique rend la preuve non opposable. | Pas d'ouverture, validation, incubation ou live. |
| `INCONCLUSIVE` | La preuve est insuffisante pour exclure un biais matériel. | Blocage jusqu'à preuve complémentaire ou nouvelle version. |
| `BURNED` | Un segment OOS ou une information sensible a contaminé la décision. | Gouvernance SOP 10 ; les données exposées ne redeviennent pas vierges. |

---

## 6. Catégories minimales de biais

Le registre `BIAS_RISK_REGISTER.md` est la source de vérité de la taxonomie.
Chaque recherche doit au minimum vérifier :

- `BIAIS_SELECTION` : retrait, oubli ou fusion opportuniste de candidates, actifs ou runs ;
- `BIAIS_METRIC_SHOPPING` : choix après résultat d'une métrique, hurdle, benchmark ou coût ;
- `BIAIS_ROBUSTNESS_SHOPPING` : sélection du scénario ou seuil de robustesse favorable ;
- `BIAIS_OOS_PEEKING` : accès, souvenir, communication ou inférence depuis OOS avant autorisation ;
- `BIAIS_REPAIR_AFTER_RESULT` : correction logique, paramètre ou sizing influencé par résultat ;
- `BIAIS_AI_CONTAMINATION` : assistant IA ou outil externe ayant reçu ou réutilisé un résultat sensible ;
- `BIAIS_PUBLICATION_COMMUNICATION` : pression, communication ou narratif influençant la conclusion ;
- `BIAIS_ARCHIVE_OMISSION` : run, incident, note ou artefact défavorable absent du paquet.

---

## 7. Journalisation obligatoire

Tout incident `LEVEL_1` ou supérieur doit produire un événement SOP 03 avec :

- identifiant d'incident ;
- horodatage ;
- acteur ou outil ;
- catégorie de biais ;
- niveau provisoire ;
- artefacts, runs, folds, candidates ou décisions affectés ;
- information sensible éventuellement exposée ;
- description factuelle ;
- mesure immédiate ;
- reviewer assigné ;
- statut final ;
- hash du rapport d'incident.

Un incident ne peut pas être effacé. Une correction est un nouvel événement
compensatoire.

---

## 8. IA, assistants et outils externes

Toute interaction avec une IA, un notebook partagé, un outil de résumé ou un
assistant externe est une exposition de recherche si elle contient :

- résultats Test ou OOS ;
- matrices de performance ;
- rapports de robustesse ;
- métriques économiques ;
- verdicts ;
- artefacts non publiés ;
- hypothèses non préenregistrées mais influencées par résultat.

L'usage d'une IA est autorisé pour documenter, auditer, implémenter ou vérifier
un protocole si les informations sensibles consommées sont connues et
journalisées. Si une IA propose une modification après avoir vu un résultat
sensible, la proposition est présumée contaminée jusqu'à preuve contraire.

---

## 9. Dérogations méthodologiques

Une dérogation est admise uniquement si elle est :

- explicitement documentée avant la décision affectée ;
- rattachée à une contrainte objective ;
- limitée dans le temps et dans le périmètre ;
- approuvée indépendamment ;
- sans effet réparateur sur un résultat observé ;
- incluse dans le paquet SOP 12.

Une dérogation ne peut jamais :

- réouvrir un OOS consommé ;
- transformer `FAIL`, `INCONCLUSIVE`, `NOT_VALIDATED` ou `REJECTED_ECONOMIC` en `PASS` ;
- retirer un run défavorable ;
- changer métrique, hurdle, benchmark, coût, scénario, sizing ou univers après observation ;
- masquer une contamination par une justification narrative.

---

## 10. Paquet de preuve `G-BIAS`

Le paquet minimal contient :

- checklist `G-BIAS` signée ;
- extrait du registre des incidents ;
- revue du `BIAS_RISK_REGISTER.md` ;
- incidents et dérogations applicables ;
- analyse d'impact sur candidates, folds, OOS, métriques, robustesse et paquets ;
- décision `PASS`, `FAIL`, `INCONCLUSIVE` ou `BURNED` ;
- reviewer indépendant ;
- hashes et chemins des preuves.

Le paquet `G-BIAS` est requis dans `PRE_OOS_SEALED` pour l'ouverture OOS et
dans `VALIDATION_READY` pour la validation reproductible.

---

## 11. Relations normatives avec les autres SOP

### SOP 03 — Registre des expériences

La SOP 03 conserve les incidents, corrections, dérogations, observations
humaines, interactions IA et décisions `G-BIAS` dans la chaîne append-only.

### SOP 05 — Robustesse

La SOP 05 fournit les scénarios et verdicts. La SOP 13 qualifie les biais de
choix, retrait, reclassification ou réparation des scénarios après observation.

### SOP 08 — Mesures de performance

La SOP 08 possède la série, les métriques et le gate économique. La SOP 13
interdit le metric shopping, le hurdle shopping, le benchmark shopping et la
réinterprétation économique influencée par résultat.

### SOP 10 — OOS

La SOP 10 possède la virginité OOS et les réexécutions. La SOP 13 qualifie les
biais d'exposition, de communication, de mémoire ou d'assistance IA qui peuvent
contaminer la décision avant ou après ouverture OOS.

### SOP 12 — Reproductibilité

La SOP 12 assemble les preuves. Elle doit inclure les artefacts `G-BIAS`, les
incidents et les dérogations dans les paquets concernés.

---

## 12. Erreurs interdites

- Conclure `G-BIAS PASS` sans revue indépendante.
- Traiter un incident humain comme une simple note non opposable.
- Documenter un biais après résultat pour justifier une décision déjà prise.
- Changer métrique, hurdle, benchmark, coût, univers ou scénario après résultat.
- Retirer un run, actif, fold, incident ou artefact défavorable du paquet.
- Utiliser une IA ayant vu l'OOS pour proposer une réparation méthodologique.
- Assimiler absence d'intention et absence de biais.
- Réparer une contamination OOS par dérogation.

---

## 13. Décision méthodologique synthétique

> **EBTA ne protège pas seulement contre les biais statistiques par les tests multiples ; il protège aussi contre les biais humains, organisationnels et assistés par IA. Tout incident susceptible d'influencer une décision devient un événement append-only, qualifié selon une gravité opposable. Le gate transversal `G-BIAS` est obligatoire avant ouverture OOS et avant validation reproductible. Une dérogation ne peut jamais réparer un résultat observé, restaurer un OOS consommé ou transformer une preuve insuffisante en `PASS`.**
