# Matrice de coherence des SOP EBTA
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - CONTROLE_TRANSVERSAL |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | Gouvernance protocole EBTA |
| Rôle dans le paquet EBTA | Controle de coherence inter-SOP et suivi des points de resolution documentaire. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

Date de reprise : 2026-06-24

## Objet

Cette matrice reprend le processus defini dans :

`Protocole/Archives/HOOK - Finalisation du protocole EBTA après revue des SOP.md`

Elle intervient apres la revue individuelle des SOP 01 a 12 et avant toute
mise a jour du protocole principal.

Objectifs de cette passe :

- verifier le statut documentaire des SOP ;
- comparer les decisions transversales ;
- identifier contradictions, doublons et dependances manquantes ;
- preparer le registre normatif des decisions sans recopier les SOP.

Le protocole principal n'est pas modifie par cette etape.

---

## Verdict transversal

**Verdict : `PARTIAL_READY_FOR_REGISTRY`**

Les SOP 01 a 12 forment une architecture methodologique globalement coherente :

- Walk-Forward obligatoire avec segments `OOS_k` successifs et non chevauchants ;
- aucun holdout final supplementaire ;
- WRC local sur `Test_k` avant chaque ouverture `OOS_k` ;
- OOS concatene comme unique objet confirmatoire global ;
- serie quotidienne complete comme unite statistique primaire ;
- separation stricte entre gate statistique, gate economique, robustesse,
  execution/capacite, incubation et reproductibilite ;
- impossibilite de reparer, reselectionner ou revalider sur un OOS deja ouvert.

Des corrections documentaires restent necessaires avant la mise a jour du
protocole principal :

1. harmoniser le statut explicite des SOP 01, 02 et 03 ;
2. centraliser les definitions proprietaires de la serie primaire, du
   detrending, du benchmark, du cash et des seuils ;
3. produire une taxonomie unique des statuts et stades ;
4. transformer les parametres configurables en template preregistre ;
5. mettre a jour l'audit methodologique sans effacer son diagnostic historique.

---

## Controle de declenchement par SOP

| SOP | Statut documentaire observe | Entrees / sorties | Statuts / gates | Interdictions et reexecution | Preuves / archivage | Verdict de coherence |
| --- | --- | --- | --- | --- | --- | --- |
| SOP 01 - Estimation et intervalle de confiance OOS | **A harmoniser** : l'en-tete indique encore `Projet a valider avant integration`, malgre un contenu normatif complet. | Serie OOS concatenee du Walk-Forward gele ; sortie statistique et economique. | `PASS`, `NOT_VALIDATED`, `REJECTED_ECONOMIC`, `FAIL`, `INCONCLUSIVE`. | Interdit toute modification retroactive apres OOS ; reexecution limitee aux corrections techniques gouvernees par SOP 10. | Rapport OOS, bootstrap, seeds, puissance, preuves de gel. | Coherent sur le fond ; statut d'en-tete bloquant pour le gel. |
| SOP 02 - Inference multiple | Section `Statut et objet`, mais pas de ligne `Statut : specification normative`. | Matrice locale complete de `Test_k`, WRC local, SPA, Romano-Wolf, MCPM. | `PASS`, `FAIL`, `INCONCLUSIVE` pour le gate Test local. | Interdit OOS apres WRC `FAIL` ou `INCONCLUSIVE`; interdit retrait retrospectif de candidates. | Rapport WRC, catalogue, seeds, hash de matrice. | Coherent ; harmonisation de statut recommandee. |
| SOP 03 - Registre des experiences | Section `Statut et objet`, mais pas de ligne `Statut : specification normative`. | Registre append-only, candidates, runs, familles, matrices, evenements. | `PASS`, `FAIL`, `INCONCLUSIVE` pour completude/integrite du registre ; statuts techniques separes. | Interdit essais informels effacables, deduplication retrospective, candidates oubliees. | Journal JSONL append-only, hashes, lineage, revue independante. | Coherent ; harmonisation de statut recommandee. |
| SOP 04 - Segmentation temporelle et Walk-Forward | Specification normative. | Calendrier Train/Test/OOS, purge, embargo, politiques `NO_MODEL` / `STOP_PROCESS`. | `PASS`, `NOT_VALIDATED`, `REJECTED_ECONOMIC`, `FAIL`, `INCONCLUSIVE`, plus statuts operationnels locaux. | Interdit chevauchement OOS, choix opportuniste du nombre de folds, usage d'OOS pour le fold suivant. | Configuration versionnee, manifeste par fold, livrable global. | Coherent. |
| SOP 05 - Robustesse et gouvernance du holdout | Specification normative. | Plan de robustesse pre-OOS, catalogue de stress-tests, matrice de robustesse. | `PASS`, `NOT_VALIDATED`, `REJECTED_ECONOMIC`, `FAIL`, `INCONCLUSIVE`. | Interdit robustesse decisionnelle apres OOS, choix de variante sur `OOS_k`, holdout final ajoute. | Plan, catalogue, manifeste, matrice et rapport de robustesse. | Coherent ; terme `holdout` clarifie comme fonction de `OOS_k`. |
| SOP 06 - Selection des candidates et complexite | Specification normative. | Snapshot de recherche, trajectoire Train/Test, candidate locale unique ou statut bloquant. | `PASS`, `NOT_VALIDATED`, `REJECTED_ECONOMIC`, `FAIL`, `INCONCLUSIVE`, `NO_MODEL`. | Interdit de tester seulement la gagnante, de forcer une candidate, d'exclure `NO_MODEL` de l'OOS global. | Manifeste de recherche, trajectoire, controles de reproductibilite. | Coherent. |
| SOP 07 - Detrending, benchmark et zero-centering | Specification normative. | Flux signal separe du flux evaluation ; formule de detrending, benchmark, cash, zero-centering. | `PASS`, `FAIL`, `INCONCLUSIVE`. | Interdit detrending des signaux, zero-centering OOS, benchmark choisi apres resultat, double centrage. | Livrable de transformation, series, hashes, controles numeriques. | Coherent ; doublon de formule avec SOP 01 et SOP 08 a centraliser. |
| SOP 08 - Mesures de performance | Contrat normatif. | Serie quotidienne du portefeuille, NAV, metriques statistiques et economiques. | Gate economique `PASS`, `REJECTED_ECONOMIC`, `INCONCLUSIVE`; statut SOP `PASS`, `FAIL`, `INCONCLUSIVE`. | Interdit substitution retroactive de metrique, confusion brut/net/detrende, moyenne de ratios de folds. | Livrable canonique de performance, reconciliation NAV. | Coherent ; proprietaire du contrat de rendement a expliciter dans le registre. |
| SOP 09A - Donnees point-in-time | Specification normative. | Snapshots, disponibilite, latence, purge, embargo, controles anti-leakage. | `PASS`, `FAIL`, `INCONCLUSIVE`, parfois `NOT_VALIDATED` selon impact. | Interdit transformation apprise hors Train, correction opportuniste, embargo ajuste selon performance. | Snapshots immuables, controles anti-leakage, preuves de disponibilite. | Coherent. |
| SOP 09B - Execution, frictions, capacite et sizing | Specification normative. | Signaux vers ordres, fills, positions, couts, capacite, sizing, NAV tradable. | `PASS`, `REJECTED_ECONOMIC`, `FAIL`, `INCONCLUSIVE`. | Interdit changement d'ordre/frictions/sizing apres observation sans nouvelle candidate/version. | Journal d'ordres, fills, couts, capacite, NAV, reconciliation. | Coherent ; interaction avec SOP 05 a indexer. |
| SOP 10 - Gouvernance OOS et echecs | Specification normative. | Gate d'ouverture OOS, contamination, verdicts, post-mortem, reexecution technique. | `PASS`, `NOT_VALIDATED`, `FAIL`, `REJECTED_ECONOMIC`, `INCONCLUSIVE`, `INVALID_TECHNICAL`. | Interdit seconde chance OOS ; reexecution meme-OOS uniquement pour erreur objective, minimale et independante de la performance. | Journal d'acces OOS, post-mortem, preuves d'erreur, versions. | Coherent ; `INVALID_TECHNICAL` doit entrer dans la taxonomie globale. |
| SOP 11 - Incubation, live et monitoring | Specification normative. | Paper trading, live limite, monitoring operationnel/statistique, suspension/retrait. | Paper trading `PASS`, `FAIL`, `INCONCLUSIVE`, `WATCH`; live par paliers. | Interdit incubation d'un statut non `PASS`, reparation alpha pendant paper/live. | Journal d'incubation, live, monitoring, incidents, decisions. | Coherent ; `WATCH` doit etre classe comme statut de monitoring, pas de validation. |
| SOP 12 - Reproductibilite et paquet EBTA | Specification normative. | Paquet de preuve complet, versions immuables, checksums, reproduction. | Stades `PRE_OOS_SEALED`, `VALIDATION_READY`, `DEPLOYMENT_CERTIFIED`, `LIFECYCLE_ARCHIVED`; gates `PASS`, `FAIL`, `INCONCLUSIVE`. | Interdit paquet incomplet, export limite a la gagnante, live avec paquet non valide. | Manifeste, checksums, environnement, donnees, code, decisions, archives. | Coherent ; les stades doivent devenir l'ossature du paquet d'execution. |

---

## Matrice thematique de coherence

| Theme transversal | SOP proprietaire proposee | SOP concernees | Decision coherente observee | Ecart / risque | Action avant protocole principal |
| --- | --- | --- | --- | --- | --- |
| 1. Definition de la candidate | SOP 03 | SOP 02, 03, 05, 06, 09A, 09B, 12 | Une candidate est une specification executable ayant produit une information exploitable ; toute variante influente appartient a la famille de recherche. | Definitions reprises dans plusieurs SOP avec des angles differents. Risque faible si SOP 03 est declaree proprietaire. | Dans le registre, attribuer a SOP 03 l'identite logique, le lineage, la deduplication et la famille ; SOP 06 ne possede que la selection locale. |
| 2. Serie de rendement primaire | SOP 08 | SOP 01, 02, 07, 08, 12 | Unite primaire = log-rendement quotidien net detrende du portefeuille ; tous les jours restent dans la chronologie. | Formule et convention cash/benchmark repetees dans SOP 01, 07 et 08. | Declarer SOP 08 proprietaire du contrat de serie ; SOP 07 proprietaire de la transformation ; SOP 01 proprietaire de l'estimation OOS. |
| 3. Detrending, benchmark et cash | SOP 07 | SOP 01, 02, 03, 05, 07, 08, 09B, 12 | Detrending ex post d'evaluation, signaux non detrendes, cash neutralise dans le gate statistique et conserve dans l'economie. | Doublon utile mais dangereux de la formule dans plusieurs SOP. | Centraliser dans le registre : SOP 07 = formule ; SOP 08 = representation de sortie ; SOP 01 = usage dans IC OOS. |
| 4. Segmentation Train/Test/OOS | SOP 04 | SOP 01, 02, 04, 05, 06, 09A, 10, 12 | `Train_k` calibre, `Test_k` selectionne et infere, `OOS_k` estime passivement. | Aucun conflit de fond detecte. | Reporter les fenetres, purges, embargos et pas de deplacement dans le template preregistre. |
| 5. Fonctionnement des folds Walk-Forward | SOP 04 | SOP 01, 02, 04, 05, 06, 07, 08, 10, 12 | Segments `OOS_k` successifs non chevauchants, concaténés pour former l'unique OOS global ; folds non traites comme IID. | SOP 01 autorise des folds futurs si le point d'arret informationnel est preregistre ; SOP 10 reprend cette idee. Il faut expliciter le proprietaire du point d'arret. | Declarer SOP 01 proprietaire du point d'arret informationnel et de la puissance ; SOP 04 proprietaire du calendrier. |
| 6. Univers des regles soumis aux tests multiples | SOP 02 avec source de verite SOP 03 | SOP 02, 03, 05, 06, 12 | WRC local sur l'univers complet et reconstructible ; candidates perdantes et variantes influentes conservees. | SOP 06 selectionne le maximum Test puis soumet la famille complete au WRC ; la phrase doit rester comprise comme selection mecanique, pas comme reduction de la famille. | Dans le registre, distinguer `selected_candidate_id` et `candidate_family_tested`. |
| 7. Metrique et seuil de chaque gate | Plusieurs proprietaires | SOP 01, 02, 05, 06, 08, 09B, 10, 11, 12 | WRC Test a 5 %, IC OOS unilateral 95 %, puissance cible 80 %, gate economique separe, robustesse/execution/reproduction bloquants. | Les seuils fixes et configurables ne sont pas encore separes dans un index unique. | Le registre doit classer chaque seuil comme fixe ou configurable ; le template doit recevoir les valeurs de recherche. |
| 8. Statuts et consequences des verdicts | SOP 10 pour OOS ; SOP proprietaire pour gate local | SOP 01 a 12 | Les statuts bloquants ne peuvent pas devenir `PASS` ; `REJECTED_ECONOMIC` reste distinct du `FAIL` statistique. | Taxonomie dispersee : `NO_MODEL`, `STOP_PROCESS`, `INVALID_TECHNICAL`, `WATCH` et stades SOP 12 ne sont pas encore rattaches a une carte globale. | Creer une table de correspondance dans le registre normatif ou un artefact dedie de taxonomie. |
| 9. Robustesse et contamination OOS | SOP 05 et SOP 10 | SOP 01, 03, 05, 06, 09B, 10, 11, 12 | Robustesse decisionnelle avant `OOS_k`; apres OOS, analyses descriptives seulement ; reexecution technique sous SOP 10. | Aucun conflit de fond. Le titre SOP 05 emploie `holdout`, mais le texte clarifie que ce n'est pas un segment supplementaire. | Dans le protocole principal futur, remplacer toute logique "robustesse apres OOS avant live" par "robustesse pre-OOS + diagnostics post-OOS non decisionnels". |
| 10. Donnees point-in-time | SOP 09A | SOP 03, 04, 06, 07, 08, 09A, 10, 12 | Toute valeur decisionnelle doit etre disponible avant la decision ; transformations apprises sur Train ; snapshots immuables. | Aucun conflit de fond. | Le template doit exiger calendrier de disponibilite, latences, snapshots, corrections et politique purge/embargo. |
| 11. Couts, sizing, capacite et execution | SOP 09B | SOP 05, 08, 09B, 10, 11, 12 | Le scenario central doit etre tradable et inclure couts, impact, borrow, financement, FX, sizing et capacite. | SOP 05 stress-teste les frictions ; SOP 09B definit le moteur central. Risque de redondance si non indexe. | Declarer SOP 09B proprietaire du modele central ; SOP 05 proprietaire des scenarios de robustesse autour de ce modele. |
| 12. Seeds, hashes, versions et archivage | SOP 12 avec registre SOP 03 | SOP 01, 02, 03, 04, 06, 07, 09A, 09B, 10, 12 | Seeds, matrices, snapshots, versions, checksums et acces OOS doivent etre reconstructibles. | Pas de conflit, mais les schemas de noms restent disperses. | Le registre normatif doit indexer les identifiants minimaux ; le paquet SOP 12 doit devenir le point d'assemblage. |
| 13. Incubation et passage live | SOP 11 | SOP 01, 05, 09B, 10, 11, 12 | Seul un vrai `PASS` statistique, economique, robustesse, execution/capacite et reproduction permet l'incubation ; le live progresse par paliers. | `WATCH` est un statut de monitoring et ne doit pas etre confondu avec un verdict de validation. | Ajouter la taxonomie `validation_status` vs `monitoring_status` avant le protocole principal. |

---

## Contradictions, doublons et dependances manquantes

### C-01 - Statut SOP 01 non finalise

- **Type :** contradiction documentaire.
- **Source :** l'en-tete SOP 01 indique encore `Projet a valider avant integration`.
- **Impact :** le hook exige des SOP dont les decisions sont considerees comme figees. Ce libelle empeche un gel documentaire propre.
- **Resolution proposee :** remplacer le statut par une formule normative alignee avec les autres SOP, sans changer le fond methodologique.
- **Priorite :** haute avant protocole principal.

### C-02 - Statut explicite absent dans SOP 02 et SOP 03

- **Type :** harmonisation documentaire.
- **Source :** les deux SOP contiennent `Type` et `Objet`, mais pas de ligne `Statut : specification normative`.
- **Impact :** faible sur le fond, mais fragilise le controle de declenchement du hook.
- **Resolution proposee :** ajouter un statut explicite, sans modifier les decisions.
- **Priorite :** moyenne.

### C-03 - Definition de la serie primaire et du detrending repetee

- **Type :** doublon normatif.
- **Source :** SOP 01, SOP 07 et SOP 08 contiennent toutes des elements de formule, benchmark, cash et log-rendement net detrende.
- **Impact :** risque de divergence future si une formule est modifiee dans une SOP mais pas dans les autres.
- **Resolution proposee :** declarer :
  - SOP 07 proprietaire de la formule de detrending ;
  - SOP 08 proprietaire du contrat de serie et de performance ;
  - SOP 01 proprietaire de l'estimation et de l'IC OOS.
- **Priorite :** haute avant registre normatif.

### C-04 - Taxonomie globale des statuts non centralisee

- **Type :** dependance manquante.
- **Source :** les statuts sont coherents localement mais disperses :
  `PASS`, `NOT_VALIDATED`, `REJECTED_ECONOMIC`, `FAIL`, `INCONCLUSIVE`,
  `NO_MODEL`, `STOP_PROCESS`, `INVALID_TECHNICAL`, `WATCH`,
  `PRE_OOS_SEALED`, `VALIDATION_READY`, `DEPLOYMENT_CERTIFIED`,
  `LIFECYCLE_ARCHIVED`.
- **Impact :** risque d'ambiguite dans le protocole principal et les futurs artefacts executables.
- **Resolution proposee :** produire une table globale distinguant :
  - verdicts de validation ;
  - statuts techniques ;
  - politiques locales de fold ;
  - statuts de monitoring ;
  - stades de paquet SOP 12.
- **Priorite :** haute avant protocole principal.

### C-05 - Gates pre-OOS a orchestrer explicitement

- **Type :** dependance de workflow.
- **Source :** SOP 06 exige WRC, stabilite, robustesse et execution ; SOP 05 possede la robustesse ; SOP 09B possede execution/capacite ; SOP 12 possede `PRE_OOS_SEALED`.
- **Impact :** aucun conflit, mais le protocole principal devra montrer l'ordre exact des dependances avant ouverture `OOS_k`.
- **Resolution proposee :** dans le registre, creer une decision normative `PRE_OOS_OPENING_GATE` listant les sous-gates et leurs SOP proprietaires.
- **Priorite :** haute.

### C-06 - Parametres configurables non encore extraits

- **Type :** livrable manquant prevu par le hook.
- **Source :** fenetres Walk-Forward, purge, embargo, benchmark, cash, couts, slippage, hurdle economique, MDE, puissance, longueur de blocs, nombre de replications, seeds, scenarios de robustesse et criteres d'incubation.
- **Impact :** sans template de configuration, le protocole reste difficilement preregistrable.
- **Resolution proposee :** produire `TEMPLATE - Configuration préenregistrée d'une recherche EBTA.md` apres le registre normatif.
- **Priorite :** haute.

### C-07 - Audit methodologique encore historique

- **Type :** dependance de cloture.
- **Source :** l'audit initial liste les sections a renforcer et des SOP "generees".
- **Impact :** le diagnostic historique doit etre conserve, mais chaque constat doit recevoir `CLOSED`, `PARTIAL`, `OPEN` ou `DEFERRED_IMPLEMENTATION`.
- **Resolution proposee :** ne mettre a jour l'audit qu'apres la matrice et le registre, pour disposer des proprietaires documentaires exacts.
- **Priorite :** moyenne avant gel.

---

## Decisions sans proprietaire unique a enregistrer

| Decision / parametre | Proprietaire recommande | Nature |
| --- | --- | --- |
| Identite logique d'une candidate | SOP 03 | Fixe |
| Famille statistique opposable | SOP 03 + SOP 02 | Fixe |
| Candidate transmise vers `OOS_k` | SOP 06 | Fixe par procedure |
| Population testee par WRC | SOP 02 avec registre SOP 03 | Fixe par procedure |
| Serie primaire quotidienne | SOP 08 | Fixe |
| Formule de detrending | SOP 07 | Fixe |
| Estimation et IC OOS | SOP 01 | Fixe |
| Puissance cible minimale | SOP 01 | Fixe si le protocole conserve 80 % |
| Nombre de replications bootstrap OOS | SOP 01 | Fixe dans la version documentaire `EBTA-DOC-1.0` |
| Seuil WRC primaire | SOP 02 | Fixe si le protocole conserve 5 % |
| Fenetres Train/Test/OOS | SOP 04 / configuration | Configurable preregistre |
| Purge et embargo | SOP 04 + SOP 09A / configuration | Configurable preregistre |
| Benchmark et cash | SOP 07 / configuration | Configurable preregistre |
| Hurdle economique | SOP 08 / configuration | Configurable preregistre |
| Modele central d'execution | SOP 09B / configuration | Configurable preregistre |
| Scenarios de robustesse | SOP 05 / configuration | Configurable preregistre |
| Gate d'ouverture `OOS_k` | SOP 10 avec dependances SOP 02, 05, 06, 09A, 09B, 12 | Fixe par procedure |
| Criteres d'incubation | SOP 11 / configuration | Configurable preregistre |
| Stades du paquet de preuve | SOP 12 | Fixe |

---

## Suivi de résolution

| Date | Point | Statut | Preuve |
| --- | --- | --- | --- |
| 2026-06-24 | C-01 - Statut SOP 01 non finalise | `CLOSED` | SOP 01 indique désormais `spécification normative de l’estimation et du verdict OOS`. |
| 2026-06-24 | C-02 - Statut explicite absent dans SOP 02 et SOP 03 | `CLOSED` | SOP 02 et SOP 03 contiennent désormais une ligne `Statut` normative explicite. |
| 2026-06-24 | Registre normatif | `CREATED` | `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md`. |
| 2026-06-24 | Template de configuration | `CREATED` | `Protocole/TEMPLATE - Configuration préenregistrée d'une recherche EBTA.md`. |
| 2026-06-24 | Protocole principal | `UPDATED` | `Protocole/PROTOCOLE EBTA.md` révisé comme carte générale et index des SOP. |
| 2026-06-24 | Audit méthodologique | `CLOSED_WITH_DEFERRED_IMPLEMENTATION` | Chaque constat reçoit un statut ; les artefacts exécutables restent à produire. |
| 2026-06-24 | Paquet d’exécution documentaire | `CREATED` | `Protocole/PAQUET D'EXECUTION EBTA.md`. |
| 2026-06-24 | C-03 à C-06 | `CLOSED_FOR_DOCUMENTATION` | Les propriétaires, statuts et paramètres sont indexés dans les livrables documentaires. |
| 2026-06-24 | Revue finale et gel documentaire | `CLOSED` | Version documentaire `EBTA-DOC-1.0`, manifeste de hashes dans `Protocole/MANIFESTE DE GEL EBTA.md`. |

---

## Prochaine etape recommandee

Avant de modifier `Protocole/PROTOCOLE EBTA.md`, effectuer dans cet ordre :

1. ouvrir une nouvelle version documentaire pour toute évolution méthodologique future ou lancer l’implémentation machine-readable du paquet d’exécution.
