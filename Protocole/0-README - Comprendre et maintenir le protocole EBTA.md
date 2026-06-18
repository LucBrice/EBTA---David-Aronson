# 0-README - Comprendre et maintenir le protocole EBTA

## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - POINT_ENTREE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
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

Le dossier `Protocole/` est gelé en version documentaire `EBTA-DOC-1.0`.
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
| `TEMPLATE - Configuration préenregistrée d'une recherche EBTA.md` | A séparé principes méthodologiques et paramètres propres à une recherche. | Formulaire à remplir avant chaque recherche EBTA. |
| `PAQUET D'EXECUTION EBTA.md` | A transformé les SOP en contrôles opérationnels documentaires. | Base pour créer schémas JSON/JSONL, validateurs, checklists exécutables et tests d’invariants. |
| `MANIFESTE DE GEL EBTA.md` | A figé la version documentaire `EBTA-DOC-1.0` et ses hashes. | Preuve de version, audit d’intégrité, point de départ d’une future version. |

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

Gelé en `EBTA-DOC-1.0` :

- architecture Walk-Forward ;
- absence de holdout final supplémentaire ;
- ordre des gates ;
- responsabilités des SOP ;
- décisions normatives du registre ;
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
