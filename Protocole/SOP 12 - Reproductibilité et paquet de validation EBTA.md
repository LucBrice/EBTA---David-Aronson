# SOP 12 — Reproductibilité et paquet de validation EBTA
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - SOP_NORMATIVE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | SOP 12 |
| Rôle dans le paquet EBTA | Paquets de validation, stades, checksums, reproduction et archivage. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## 1. Statut et objet

- **Statut :** spécification normative du paquet de preuve final.
- **Critère :** un tiers indépendant doit pouvoir identifier l’intention, vérifier les entrées, rejouer les calculs et retrouver les verdicts dans les tolérances définies.
- **Portée :** cycle complet, y compris candidates perdantes, erreurs, accès OOS, exécution et lien avec la version live.

Un notebook final, un rapport ou des graphiques ne constituent pas un paquet reproductible.

---

## 2. Principe

Le paquet capture :

- intention ;
- hypothèse ;
- données ;
- code ;
- environnement ;
- configuration ;
- aléatoire ;
- univers complet ;
- résultats ;
- décisions ;
- preuves de gel ;
- accès OOS ;
- exécution ;
- monitoring ;
- versions.

Les résultats perdants et intermédiaires font partie de la preuve.

---

## 3. Stades du paquet

Le paquet progresse par versions immuables. Chaque changement de stade produit un nouveau manifeste et de nouveaux checksums sans écraser les versions antérieures.

### `PRE_OOS_SEALED`

Stade obligatoire avant tout accès OOS. Il contient au minimum :

- identité du projet et de la famille de recherche ;
- hypothèse et plan préenregistrés ;
- code et environnement ;
- données, corrections, splits et calendrier ;
- univers complet et registre des candidates ;
- paramètres, seeds et plan d’analyse ;
- modèle d’exécution préspécifié ;
- manifeste et checksums.

### `VALIDATION_READY`

Stade obligatoire avant incubation. Il ajoute :

- séries OOS passives et concaténées ;
- verdicts statistiques et économiques ;
- preuves des gates ;
- reproduction indépendante de niveau 3 `PASS`.

### `DEPLOYMENT_CERTIFIED`

Stade obligatoire pour le passage live limité. Il ajoute :

- paper trading `PASS` ;
- version live exacte ;
- limites, sizing et kill switch ;
- monitoring versionné ;
- approbation de déploiement.

### `LIFECYCLE_ARCHIVED`

Stade final de conservation. Il ajoute :

- journaux de production et d’incidents ;
- décisions et changements d’état ;
- réconciliations ;
- retrait ou statut actif final ;
- vérification de l’archive.

---

## 4. Autorités normatives

SOP 12 ne redéfinit aucune méthode.

Elle empaquette les preuves produites par :

- SOP 01 à 11 ;
- le registre de la SOP 03 ;
- les gates et reviewers ;
- les artefacts de données et d’exécution.

En cas de contradiction, la SOP propriétaire de la méthode prévaut et le paquet est `FAIL` jusqu’à résolution.

---

## 5. Identité immuable

Inclure :

- `PROJECT_ID` ;
- `RESEARCH_FAMILY_ID` ;
- `HYPOTHESIS_ID` ;
- `PROCESS_VERSION_ID` ;
- `RUN_ID` ;
- `VALIDATION_PACKAGE_ID` ;
- liens parent-enfant ;
- chercheurs ;
- reviewers ;
- dates ;
- statuts.

Un nom de fichier ne constitue pas une identité.

---

## 6. Hypothèse et préenregistrement

Archiver :

- rationnel ;
- hypothèse falsifiable ;
- `H0` ;
- portée ;
- univers ;
- métrique primaire ;
- benchmark ;
- hurdles ;
- No-Go ;
- budget ;
- adaptations autorisées ;
- critères d’arrêt ;
- règles de verdict.

Les versions avant et après résultats restent distinguables.

---

## 7. Code

Archiver :

- commit ;
- tag ;
- hash ;
- branche informative ;
- état exact du worktree ;
- diff/patch ;
- fichiers non suivis nécessaires ;
- sous-modules ;
- scripts d’entrée ;
- tests ;
- configuration ;
- générateurs.

Un commit ne suffit pas si le run dépend d’un worktree sale ou de fichiers non suivis.

---

## 8. Organisation de la logique

La logique métier réside dans des modules ou scripts versionnés et testables.

Les notebooks :

- consomment ces modules ;
- orchestrent ;
- documentent ;
- visualisent.

Une logique critique présente uniquement dans une cellule manuelle non testée produit `FAIL`.

---

## 9. Environnement

Capturer :

- OS ;
- architecture ;
- langage ;
- runtime ;
- dépendances exactes ;
- lockfile ;
- compilateurs ;
- bibliothèques statistiques ;
- BLAS/LAPACK si pertinent ;
- matériel pertinent ;
- locale ;
- timezone ;
- variables non secrètes ;
- nombre de threads ;
- image de conteneur et digest si utilisée.

Une liste de versions majeures non verrouillée est insuffisante.

---

## 10. Secrets

Les secrets ne sont jamais archivés en clair.

Documenter :

- nom logique ;
- rôle ;
- fournisseur ;
- méthode d’injection ;
- droits requis ;
- procédure de rotation ;
- environnement de reproduction.

Les hashes ou valeurs permettant de reconstruire un secret ne sont pas publiés.

---

## 11. Données redistribuables

Pour chaque dataset :

- fournisseur ;
- licence ;
- version/vintage ;
- extraction ;
- requête ;
- schéma ;
- timezone ;
- plage ;
- univers ;
- corporate actions ;
- corrections ;
- qualité ;
- fichiers ;
- hashes.

Le snapshot doit être identique à celui utilisé par le run.

---

## 12. Données non redistribuables

Fournir :

- manifeste ;
- licence et restriction ;
- procédure ou requête d’extraction ;
- version/vintage ;
- fournisseur ;
- paramètres ;
- hashes attendus ;
- schéma ;
- contrôles d’identité ;
- procédure d’accès indépendant contrôlé.

Une simple URL ne permet pas la reproduction.

Une contrainte de licence non résolue peut produire `INCONCLUSIVE`, jamais un `PASS` automatique.

---

## 13. Corrections de données

Toute correction crée une nouvelle version.

Conserver :

- ancienne version ;
- cause ;
- diff ;
- impact ;
- reviewer ;
- nouveaux hashes ;
- runs affectés ;
- décision de réexécution.

Écraser un snapshot invalide la chaîne de preuve.

---

## 14. Splits et calendrier

Archiver dans un format machine-readable :

- dates et indices exacts ;
- folds ;
- Train/Test/OOS ;
- warm-up ;
- purge ;
- embargo ;
- rolling/expanding ;
- pas ;
- calendriers ;
- timezones ;
- états OOS ;
- journal d’accès.

Une description en prose seule est insuffisante.

---

## 15. Registre complet

Exporter :

- expériences ;
- candidates ;
- runs ;
- paramètres ;
- seeds ;
- statuts ;
- décisions ;
- erreurs ;
- runs avortés ;
- snapshots ;
- lignages ;
- séries ;
- accès.

Le nombre `M` de candidates et la population statistique doivent être recalculables.

Un export limité à la gagnante produit `FAIL`.

---

## 16. Matrice statistique

Archiver :

- matrice complète des rendements ;
- dictionnaire des colonnes ;
- ordre des colonnes ;
- dates ;
- qualité ;
- séries detrendées ;
- séries zero-centered ;
- hashes ;
- schéma.

La matrice doit permettre de reproduire le WRC local exact de chaque fold.

---

## 17. Bootstrap et tests

Conserver :

- méthode ;
- hypothèse ;
- statistique ;
- bloc ;
- paramètres ;
- générateur ;
- seed ;
- réplications ;
- ordre ;
- parallélisme ;
- statistiques observées ;
- p-values ;
- distributions simulées ;
- ou une régénération déterministe validée.

Une p-value finale sans procédure n’est pas une preuve suffisante.

---

## 18. Artefacts OOS

Archiver :

- séries `OOS_k` ;
- périodes de cash/non-déploiement ;
- série concaténée ;
- estimand ;
- bootstrap ;
- IC ;
- diagnostics ;
- gates ;
- accès ;
- contamination ;
- verdicts ;
- hashes.

Le meilleur fold ou un graphique global ne remplace pas la série complète.

---

## 19. Exécution et comptabilité

Inclure :

- signaux ;
- ordres ;
- fills ;
- positions ;
- cash ;
- coûts ;
- financement ;
- FX ;
- NAV ;
- sizing ;
- contraintes ;
- capacité ;
- réconciliation.

La série économique de la SOP 08 doit être reproductible à partir de ces artefacts.

---

## 20. Aléatoire et non-déterminisme

Pour chaque composant :

- générateur ;
- algorithme ;
- seed ;
- ordre des opérations ;
- parallélisme ;
- threads ;
- matériel ;
- tolérance absolue ;
- tolérance relative ;
- répétitions ;
- distribution attendue ;
- règle de comparaison ;
- conséquence sur les gates.

Une différence sans seuil préenregistré n’est pas automatiquement acceptable.

---

## 21. Baselines numériques

Les baselines sont sérialisées dans des formats stables.

Inclure :

- séries ;
- tableaux ;
- schémas ;
- hashes ;
- métriques ;
- comptes ;
- première/dernière date ;
- identifiants ;
- verdicts ;
- précision numérique.

Les graphiques sont secondaires.

---

## 22. Preuves de gates

Pour chaque gate :

```text
gate_id
method_version
status
criterion
observed_value
threshold
evidence_path
evidence_hash
reviewer
timestamp
```

Les dérogations sont préexistantes, explicites, approuvées et versionnées.

Aucune dérogation rétroactive n’est admise.

---

## 23. Formats stables

Privilégier :

- JSON/JSONL avec schéma ;
- CSV/Parquet avec schéma ;
- texte UTF-8 ;
- formats ouverts ou documentés.

Définir :

- version du schéma ;
- ordre des colonnes ;
- types ;
- précision ;
- timezone ;
- représentation des valeurs manquantes ;
- compression ;
- endianness si pertinente.

Un fichier propriétaire manuel ne peut être l’unique preuve.

---

## 24. Checksums et manifeste racine

`MANIFEST.json` référence chaque artefact :

- chemin ;
- type ;
- schéma ;
- taille ;
- hash ;
- rôle ;
- provenance ;
- dépendances.

`checksums.sha256` permet une vérification indépendante.

Les checksums sont vérifiés :

- avant reproduction ;
- après transfert ;
- lors des contrôles d’archive.

---

## 25. Structure du paquet

```text
validation_package/
  MANIFEST.json
  README.md
  checksums.sha256
  hypothesis/
  code/
  environment/
  data_manifest/
  splits/
  registry/
  returns/
  execution/
  statistics/
  robustness/
  decisions/
  oos_access/
  monitoring/
  tests/
  reports/
```

---

## 26. Procédure non interactive

Depuis un environnement vierge, une commande ou orchestration documentée doit :

1. vérifier les checksums ;
2. reconstruire l’environnement ;
3. obtenir ou vérifier les données ;
4. exécuter les tests ;
5. rejouer les features et signaux ;
6. rejouer l’exécution ;
7. reconstruire les matrices ;
8. recalculer les tests ;
9. recalculer l’OOS ;
10. évaluer les gates ;
11. produire le rapport de comparaison.

Une intervention manuelle substantielle du chercheur invalide le niveau indépendant.

---

## 27. Niveaux de reproduction

### Niveau 1 — Intégrité

Fichiers, schémas et hashes valides.

### Niveau 2 — Calcul

Même environnement et mêmes sorties dans les tolérances.

### Niveau 3 — Indépendant

Un tiers exécute le paquet sans aide substantielle.

### Niveau 4 — Réimplémentation

Une implémentation indépendante obtient des résultats compatibles.

Le gate final exige au minimum le niveau 3.

---

## 28. Reviewer indépendant

Le rapport de reproduction conserve :

- identité ;
- indépendance ;
- environnement ;
- commandes ;
- dates ;
- sorties ;
- divergences ;
- conclusion ;
- signature ou approbation.

L’auteur seul ne peut certifier le niveau 3.

---

## 29. Tests minimaux

Inclure :

- tests unitaires ;
- schémas ;
- point-in-time ;
- no-lookahead ;
- splits ;
- detrending ;
- zero-centering ;
- statistiques ;
- coûts ;
- types d’ordre ;
- sizing ;
- capacité ;
- déterminisme ;
- comptabilité ;
- baselines ;
- états et gates.

Un rapport `PASS` sans sorties de tests archivées n’est pas une preuve.

---

## 30. Échec de reproduction

Un échec :

- bloque la clôture ;
- bloque le passage live ;
- produit un diagnostic ;
- crée une nouvelle version du paquet après correction ;
- conserve l’ancienne ;
- ne modifie pas la baseline pour la faire correspondre au résultat obtenu.

---

## 31. Contraintes externes

Une licence, dépendance ou infrastructure indisponible produit `INCONCLUSIVE` tant qu’une procédure indépendante équivalente n’est pas validée.

Une procédure équivalente peut utiliser :

- environnement contrôlé ;
- accès supervisé ;
- recalcul chez le fournisseur ;
- comparaison de hashes et contrôles ;
- reviewer indépendant.

---

## 32. Archivage

Le paquet final est :

- immuable ;
- daté ;
- versionné ;
- contrôlé en accès ;
- stocké sur au moins deux supports ou domaines de panne ;
- vérifié périodiquement ;
- lié au registre.

Une archive unique sur le poste du chercheur est insuffisante.

---

## 33. Conservation

Conformément à la SOP 03, conserver au minimum :

- pendant toute la vie du projet ;
- puis dix ans après le statut `RETIRED`.

Les versions antérieures, runs perdants et paquets invalides restent disponibles.

---

## 34. Corrections du paquet

Une correction :

- crée une nouvelle version immuable ;
- conserve l’ancienne ;
- documente cause, diff et impact ;
- recalcule les hashes ;
- reçoit une approbation ;
- identifie les verdicts affectés.

Modifier les fichiers en place puis remplacer les checksums est interdit.

---

## 35. Lien avec la version live

Cette section devient obligatoire au stade `DEPLOYMENT_CERTIFIED`. Elle n’est pas requise pour obtenir `VALIDATION_READY`.

La version déployée référence exactement :

- package ;
- code ;
- configuration ;
- données/processus ;
- modèle de coûts ;
- sizing ;
- monitoring ;
- artefacts de validation.

Toute divergence est détectée, journalisée et gouvernée par les SOP 10 et 11.

Un nom de stratégie ou une branche `main` ne suffit pas.

---

## 36. Monitoring et cycle de vie

Cette section est alimentée aux stades `DEPLOYMENT_CERTIFIED` et `LIFECYCLE_ARCHIVED`.

Le paquet relie :

- seuils ;
- états ;
- paliers ;
- incidents ;
- décisions ;
- versions ;
- réconciliations ;
- retrait.

Les journaux de SOP 11 prolongent la chaîne de preuve du paquet initial.

---

## 37. Artefacts sensibles

Les secrets, licences et données sensibles sont séparés avec :

- contrôle d’accès ;
- inventaire ;
- procédure de récupération ;
- preuve d’intégrité ;
- rôles ;
- journal.

La séparation ne doit pas empêcher l’audit de la dépendance.

---

## 38. Gate de reproduction et gates de stade

### Gate `VALIDATION_READY` — `PASS`

- manifeste complet ;
- checksums valides ;
- environnement reconstructible ;
- données identifiables ;
- registre complet ;
- tests `PASS` ;
- séries et gates reproduits ;
- niveau 3 réussi ;
- verdict retrouvé.

### Gate `DEPLOYMENT_CERTIFIED` — `PASS`

Exige en plus :

- paper trading `PASS` ;
- version live exacte ;
- limites et kill switch vérifiés ;
- monitoring versionné ;
- approbation de déploiement.

### Gate `LIFECYCLE_ARCHIVED` — `PASS`

Exige en plus :

- journaux de production et d’incidents complets ;
- états et décisions réconciliés ;
- retrait ou statut actif final clairement identifié ;
- archive finale vérifiée.

### `FAIL`

- artefacts manquants ;
- logique manuelle unique ;
- résultats non reproductibles ;
- données différentes non justifiées ;
- seeds inconnues ;
- verdict non recalculable ;
- baseline modifiée après coup.

### `INCONCLUSIVE`

- contrainte externe non résolue ;
- dépendance indisponible ;
- non-déterminisme hors tolérance ;
- reproduction indépendante incomplète.

`INCONCLUSIVE` bloque le passage live.

---

## 39. Livrable de certification

```text
[PACKAGE]
validation_package_id:
package_stage:
project_id:
research_family_id:
process_version_id:
manifest_hash:
checksums_hash:

[REPRODUCTION]
level:
reviewer:
environment_hash:
command:
started_at:
completed_at:

[COMPARISON]
signals_match:
returns_match:
candidate_matrix_match:
tests_match:
oos_match:
gate_match:
tolerance_status:

[LIVE LINK]
deployed_version:
package_reference:
configuration_hash:
monitoring_version:

[VERDICT]
status:
exceptions:
approved_by:
timestamp:
```

---

## 40. Erreurs interdites

- Archiver seulement la gagnante.
- Omettre le worktree sale.
- Re-télécharger des données différentes.
- Conserver seulement les p-values.
- Utiliser des graphiques comme baseline.
- Modifier une baseline après reproduction.
- Laisser la logique dans un notebook manuel.
- Certifier soi-même le niveau indépendant.
- Écraser une ancienne version.
- Passer live avec un paquet `INCONCLUSIVE`.

---

## 41. Sources internes

- `Notes/19-L'Illusion Technique L'Impératif de l'Objectivité Algorithmique.md`
- `Notes/21-La Cohérence Logique Fondement de la Méthode Scientifique en Trading.md`
- `Notes/27-Popper et la Falsification en Analyse Technique Scientifique.md`
- `Notes/31-L'Éthique de la Falsification Science et Rigueur Théorique.md`
- `Notes/33-La Méthode Hypothético-Déductive Science et Rigueur du Trading.md`
- `Notes/36-La Rigueur de la Méthode Scientifique et la Falsification.md`
- `Notes/49-L'Inférence Statistique Les Six Fondements de la Preuve Scientifique.md`
- `Notes/57-L'Échantillon Unique Le Défi de la Variabilité Invisible.md`
- `Notes/159-Méthodologie de Data Mining sur le S&P 500.md`
- `Notes/161-Protocole EBTA La Science de l’Analyse Technique Objective.md`

---

## 42. Décision méthodologique synthétique

> **Le paquet EBTA progresse par versions immuables : `PRE_OOS_SEALED` avant l’ouverture OOS, `VALIDATION_READY` avant l’incubation, `DEPLOYMENT_CERTIFIED` avant le live limité, puis `LIFECYCLE_ARCHIVED` pour la conservation finale. Un tiers indépendant doit pouvoir reconstruire l’environnement et les données, rejouer l’univers complet des candidates, reproduire l’exécution, les tests multiples, l’OOS et tous les gates. Les runs perdants, erreurs, accès OOS et versions antérieures font partie de la preuve. Toute correction crée une nouvelle version et l’ancienne reste conservée au moins dix ans après le retrait.**
