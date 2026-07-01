# 0-README - Comprendre et maintenir le protocole EBTA

## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - POINT_ENTREE |
| Version documentaire | EBTA-DOC-1.1 |
| Date de gel documentaire | 2026-07-01 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | Gouvernance protocole EBTA |
| Rôle dans le paquet EBTA | Point d’entrée humain et IA pour comprendre, maintenir et faire évoluer le protocole. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## Fonction de ce fichier

Lire ce fichier en premier.

Il explique :

- quels documents sont normatifs ;
- quels documents servent à l’historique ;
- quels documents servent à l’exécution future ;
- dans quel ordre lire le dossier ;
- comment faire évoluer le protocole sans casser le gel documentaire.

Le dossier `Protocole/` est gelé en version documentaire `EBTA-DOC-1.1`.
Toute évolution méthodologique future doit ouvrir une nouvelle version.

---

## Lecture rapide

Si tu veux comprendre le protocole en 15 minutes :

1. Lire `PROTOCOLE EBTA.md`.
2. Lire `REGISTRE DES DECISIONS NORMATIVES EBTA.md`.
3. Lire `MANIFESTE DE GEL EBTA.md`.
4. Ouvrir les SOP seulement si tu dois vérifier un détail technique.

Si tu veux appliquer le protocole à une recherche :

1. Lire `PROTOCOLE EBTA.md`.
2. Remplir `TEMPLATE - Configuration préenregistrée d'une recherche EBTA.md`.
3. Suivre `PAQUET D'EXECUTION EBTA.md`.
4. Utiliser les SOP comme autorités détaillées.

Si tu veux modifier le protocole :

1. Lire `MANIFESTE DE GEL EBTA.md`.
2. Lire `MATRICE DE COHERENCE DES SOP EBTA.md`.
3. Lire `REGISTRE DES DECISIONS NORMATIVES EBTA.md`.
4. Identifier les SOP impactées.
5. Ouvrir une nouvelle version documentaire avant tout changement normatif.

---

## Parcours de lecture par profil

Le dossier est volontairement normatif. Il n'est donc pas lu de la même façon
selon le niveau de familiarité avec EBTA.

### Expert extérieur

Objectif : auditer la rigueur scientifique, les biais évités et la cohérence
des décisions.

1. Lire `PROTOCOLE EBTA.md` pour comprendre la séquence des gates.
2. Lire `REGISTRE DES DECISIONS NORMATIVES EBTA.md` pour vérifier les
   décisions opposables et leurs SOP propriétaires.
3. Lire `MATRICE DE COHERENCE DES SOP EBTA.md` pour contrôler les dépendances,
   doublons et risques de contradiction.
4. Ouvrir les SOP propriétaires des points contestés.
5. Lire `PAQUET D'EXECUTION EBTA.md` seulement pour vérifier la traduction
   opérationnelle des exigences documentaires.

### Connaisseur du dossier

Objectif : retrouver rapidement où se trouve une règle, une procédure ou un
livrable sans relire tout le protocole.

1. Lire la carte processuelle dans `PROTOCOLE EBTA.md`.
2. Utiliser les tableaux de lecture du protocole principal pour passer de
   chaque bloc de processus vers sa SOP propriétaire.
3. Vérifier la décision dans `REGISTRE DES DECISIONS NORMATIVES EBTA.md` si la
   règle a un effet de gate, de statut ou d'autorité.
4. Utiliser `PAQUET D'EXECUTION EBTA.md` pour retrouver les artefacts attendus.

### Débutant

Objectif : comprendre le processus avant d'entrer dans les détails normatifs.

1. Lire `PROTOCOLE EBTA.md`, surtout les sections de carte processuelle et de
   boucles locales/globales.
2. Lire le tableau ci-dessous pour savoir quelle SOP ouvrir selon la question.
3. Lire uniquement la SOP concernée, puis revenir au protocole principal.
4. Lire `PAQUET D'EXECUTION EBTA.md` seulement quand il faut produire ou
   vérifier un paquet de recherche.
5. Ne pas commencer par le manifeste : il prouve le gel documentaire, mais il
   n'explique pas le processus.

### Questions fréquentes et document à ouvrir

| Question | Document à ouvrir en premier | Détail normatif |
| --- | --- | --- |
| Quel est l'ordre global du processus EBTA ? | `PROTOCOLE EBTA.md` | SOP selon le bloc concerné |
| Comment sont créés les folds Walk-Forward ? | `PROTOCOLE EBTA.md` puis `SOP 04` | `SOP 04 - Segmentation temporelle et Walk-Forward.md` |
| Comment éviter le look-ahead et les données indisponibles ? | `SOP 09A` | `SOP 09A - Données point-in-time et contrôles anti-leakage.md` |
| Où sont définies les règles candidates ? | `SOP 03` | `SOP 03 - Registre des expériences et univers des règles candidates.md` |
| Comment choisir la règle candidate dans Train/Test ? | `SOP 06` | `SOP 06 - Sélection des règles candidates et optimisation de la complexité.md` |
| Où intervient la WRC et la correction du data-mining bias ? | `SOP 02` | `SOP 02 - Inférence multiple WRC SPA Romano-Wolf MCP.md` |
| Comment sont évaluées robustesse et sensibilité ? | `SOP 05` | `SOP 05 - Tests de robustesse et gouvernance du holdout.md` |
| Quelle série de rendement sert à l'évaluation ? | `SOP 08` | `SOP 08 - Mesures de performance et série de rendement de référence.md` |
| Comment les coûts, fills, capacité et sizing sont-ils traités ? | `SOP 09B` | `SOP 09B - Modèle d’exécution frictions capacité et sizing.md` |
| Quand l'OOS peut-il être ouvert ? | `SOP 10` | `SOP 10 - Gouvernance OOS et gestion des échecs.md` |
| Comment produire l'estimation OOS finale et son intervalle ? | `SOP 01` | `SOP 01 - Estimation et intervalle de confiance OOS.md` |
| Comment gouverner les biais humains, incidents, dérogations ou contaminations IA ? | `SOP 13` | `SOP 13 - Gouvernance des biais humains et incidents méthodologiques.md` |
| Que se passe-t-il après validation OOS ? | `SOP 11` | `SOP 11 - Incubation passage live et monitoring séquentiel.md` |
| Comment prouver la reproductibilité ? | `SOP 12` | `SOP 12 - Reproductibilité et paquet de validation EBTA.md` |
| Quels artefacts concrets doivent exister ? | `PAQUET D'EXECUTION EBTA.md` | SOP propriétaires citées par artefact |

---

## Classement par utilité

Le premier niveau du dossier `Protocole/` conserve uniquement les documents
utiles à la compréhension, l’application, la maintenance ou l’évolution future du
protocole.

Les documents qui ont surtout servi à construire ou finaliser la version gelée
sont conservés dans `Protocole/Archives/`.

### A. Documents actifs pour comprendre et appliquer le protocole

| Document | Utilité passée | Utilité future |
| --- | --- | --- |
| `PROTOCOLE EBTA.md` | A remplacé l’ancien protocole long et contradictoire par une carte claire. | Point d’entrée normatif principal : ordre des gates, livrables, gouvernance, index SOP. |
| `REGISTRE DES DECISIONS NORMATIVES EBTA.md` | A centralisé les décisions prises pendant la revue des SOP. | Source de vérité pour savoir qui possède chaque règle et éviter les redéfinitions. |
| `BIAS_RISK_REGISTER.md` | Créé en `EBTA-DOC-1.1` pour rendre opposables les catégories de biais humains, méthodologiques et assistés par IA. | Taxonomie minimale à vérifier par `G-BIAS` avant ouverture OOS, validation reproductible, incubation ou live. |
| `TEMPLATE - Configuration préenregistrée d'une recherche EBTA.md` | A séparé principes méthodologiques et paramètres propres à une recherche. | Formulaire à remplir avant chaque recherche EBTA. |
| `TEMPLATE - Incident de biais EBTA.md` | Créé en `EBTA-DOC-1.1` pour standardiser la déclaration d'incident. | Format minimal de journalisation et revue indépendante d'un incident de biais. |
| `TEMPLATE - Dérogation méthodologique EBTA.md` | Créé en `EBTA-DOC-1.1` pour encadrer les exceptions. | Format minimal d'une dérogation admissible, non réparatrice et approuvée. |
| `PAQUET D'EXECUTION EBTA.md` | A transformé les SOP en contrôles opérationnels documentaires. | Base pour créer schémas JSON/JSONL, validateurs, checklists exécutables et tests d’invariants. |
| `MANIFESTE DE GEL EBTA.md` | A figé la version documentaire `EBTA-DOC-1.1` et ses hashes. | Preuve de version, audit d’intégrité, point de départ d’une future version. |

### B. SOP normatives actives

Les SOP sont les autorités détaillées. Elles ne doivent pas être contournées par
le protocole principal.

| SOP | Utilité principale future |
| --- | --- |
| `SOP 01 - Estimation et intervalle de confiance OOS.md` | Estimation OOS, IC, puissance, verdict statistique global. |
| `SOP 02 - Inférence multiple WRC SPA Romano-Wolf MCP.md` | WRC local, SPA, Romano-Wolf, MCPM, correction du data-mining bias. |
| `SOP 03 - Registre des expériences et univers des règles candidates.md` | Registre append-only, candidates, familles, runs, matrices et événements. |
| `SOP 04 - Segmentation temporelle et Walk-Forward.md` | Folds, calendrier, purge, embargo, OOS global. |
| `SOP 05 - Tests de robustesse et gouvernance du holdout.md` | Robustesse pré-OOS et diagnostics post-OOS non réparateurs. |
| `SOP 06 - Sélection des règles candidates et optimisation de la complexité.md` | Sélection locale, complexité, candidate transmise, `NO_MODEL`. |
| `SOP 07 - Detrending benchmark et zero-centering.md` | Detrending, benchmark, cash, zero-centering, séparation signal/évaluation. |
| `SOP 08 - Mesures de performance et série de rendement de référence.md` | Série primaire, NAV, métriques, gate économique. |
| `SOP 09A - Données point-in-time et contrôles anti-leakage.md` | Disponibilité temporelle, snapshots, anti-leakage, purge/embargo côté données. |
| `SOP 09B - Modèle d’exécution frictions capacité et sizing.md` | Ordres, fills, coûts, capacité, sizing, NAV tradable. |
| `SOP 10 - Gouvernance OOS et gestion des échecs.md` | Accès OOS, contamination, échecs, réexécutions techniques. |
| `SOP 11 - Incubation passage live et monitoring séquentiel.md` | Paper trading, live limité, monitoring, suspension, retrait. |
| `SOP 12 - Reproductibilité et paquet de validation EBTA.md` | Paquets, stades, checksums, reproduction, archivage. |
| `SOP 13 - Gouvernance des biais humains et incidents méthodologiques.md` | Incidents de biais, dérogations, contaminations IA, revue indépendante et gate transversal `G-BIAS`. |

### C. Documents de maintenance et de contrôle transversal

| Document | Utilité passée | Utilité future |
| --- | --- | --- |
| `MATRICE DE COHERENCE DES SOP EBTA.md` | A vérifié contradictions, doublons, dépendances et propriétaires après revue individuelle des SOP. | À relire avant toute modification de SOP pour évaluer les impacts transversaux. |
| `HISTORIQUE DES VERSIONS EBTA.md` | N/A (créé post-gel) | Registre central pour journaliser chronologiquement les futures versions et modifications. |
| `0-README - Comprendre et maintenir le protocole EBTA.md` | Ajouté après gel pour rendre le dossier lisible par un humain ou une IA. | Point d’entrée permanent du dossier `Protocole/`. |

### D. Documents archivés

| Document | Utilité passée | Utilité future |
| --- | --- | --- |
| `Archives/AUDIT METHODOLOGIQUE PROTOCOLE EBTA.md` | A identifié les failles de l’ancien protocole et prouvé leur clôture. | Trace d’audit. À consulter si une évolution risque de réintroduire un ancien problème. |
| `Archives/HOOK - Finalisation du protocole EBTA après revue des SOP.md` | A servi de point de reprise après revue individuelle des SOP. | Trace historique. À conserver pour comprendre pourquoi matrice, registre, template et manifeste existent. |

---

## Ordre de lecture recommandé

### Pour un humain qui découvre le dossier

1. `0-README - Comprendre et maintenir le protocole EBTA.md`
2. `PROTOCOLE EBTA.md`
3. `MANIFESTE DE GEL EBTA.md`
4. `REGISTRE DES DECISIONS NORMATIVES EBTA.md`
5. `PAQUET D'EXECUTION EBTA.md`
6. SOP concernées selon le besoin

### Pour une IA qui doit répondre sur le protocole

1. `0-README - Comprendre et maintenir le protocole EBTA.md`
2. `PROTOCOLE EBTA.md`
3. `REGISTRE DES DECISIONS NORMATIVES EBTA.md`
4. `MANIFESTE DE GEL EBTA.md`
5. `MATRICE DE COHERENCE DES SOP EBTA.md`
6. SOP propriétaires du sujet demandé

### Pour une IA qui doit modifier le protocole

1. Lire le manifeste de gel.
2. Identifier si la demande est :
   - correction documentaire ;
   - clarification sans changement normatif ;
   - changement normatif ;
   - implémentation opérationnelle.
3. Si changement normatif, ouvrir une nouvelle version documentaire.
4. Mettre à jour au minimum :
   - SOP concernées ;
   - registre normatif ;
   - protocole principal si l’ordre des gates change ;
   - matrice de cohérence ;
   - historique des versions (Changelog) ;
   - manifeste de gel.

---

## Règles de maintenance

### Correction documentaire simple

Exemples :

- faute de frappe ;
- lien cassé ;
- clarification sans changement de règle.

Action :

- corriger le fichier ;
- recalculer le hash dans le manifeste ;
- ne pas changer la version documentaire si le sens normatif ne change pas.

### Changement normatif

Exemples :

- modifier un seuil ;
- changer l’ordre des gates ;
- changer le rôle d’une SOP ;
- autoriser une action auparavant interdite ;
- changer la définition d’une candidate, de l’OOS ou d’un verdict.

Action :

- ouvrir une nouvelle version documentaire ;
- modifier les SOP propriétaires ;
- mettre à jour le registre normatif ;
- vérifier la matrice de cohérence ;
- mettre à jour le protocole principal si nécessaire ;
- ajouter une entrée détaillée dans `HISTORIQUE DES VERSIONS EBTA.md` ;
- produire un nouveau manifeste de gel.

### Implémentation opérationnelle

Exemples :

- schémas JSON ;
- registres JSONL ;
- validateurs d’invariants ;
- générateurs de manifestes ;
- tests automatisés.

Action :

- utiliser `PAQUET D'EXECUTION EBTA.md` comme cahier des charges ;
- ne pas modifier les décisions normatives sauf besoin explicite ;
- relier chaque contrôle automatisé à une SOP propriétaire.

---

## Ce qui est gelé et ce qui ne l’est pas

Gelé en `EBTA-DOC-1.1` :

- architecture Walk-Forward ;
- absence de holdout final supplémentaire ;
- ordre des gates ;
- responsabilités des SOP ;
- décisions normatives du registre ;
- gouvernance des biais humains et assistés par IA par SOP 13 et `G-BIAS` ;
- template de configuration ;
- paquet d’exécution documentaire ;
- manifeste de hashes.

Non encore implémenté :

- schémas machine-readable ;
- formulaires exécutables ;
- registres JSONL réels ;
- journal d’accès OOS automatisé ;
- tests automatisés des invariants ;
- intégration dans un pipeline de recherche.

Ces éléments sont `DEFERRED_IMPLEMENTATION`, pas des problèmes méthodologiques
ouverts.

---

## Règle d’or

Ne jamais modifier une SOP isolément sans vérifier :

1. le registre normatif ;
2. la matrice de cohérence ;
3. le protocole principal ;
4. le manifeste de gel ;
5. les SOP dépendantes.
