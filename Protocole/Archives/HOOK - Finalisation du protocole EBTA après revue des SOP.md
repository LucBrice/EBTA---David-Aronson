# HOOK — Finalisation du protocole EBTA après revue des SOP
## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ARCHIVE - HOOK_EXECUTE |
| Version documentaire | EBTA-DOC-1.0 |
| Date de gel documentaire | 2026-06-24 |
| Dernière version gelée | Oui |
| Propriétaire documentaire | Gouvernance protocole EBTA |
| Rôle dans le paquet EBTA | Point de reprise historique ayant conduit a la matrice, au registre, au template, au protocole revise et au manifeste de gel. |
| Référence de gel | Protocole/MANIFESTE DE GEL EBTA.md |

## Fonction du document

Ce fichier constitue le point de reprise de la tâche initiale après la mise au clair individuelle des SOP.

Il doit être rouvert lorsque toutes les discussions consacrées aux SOP sont terminées.

---

## Objectif initial à reprendre

Transformer le protocole EBTA général en un processus :

- déterministe ;
- préenregistrable ;
- reproductible ;
- auditable ;
- protégé contre le data-mining bias, le surapprentissage, le leakage et la contamination OOS.

L’audit initial se trouve dans :

`Protocole/AUDIT METHODOLOGIQUE PROTOCOLE EBTA.md`

Le protocole à finaliser se trouve dans :

`Protocole/PROTOCOLE EBTA.md`

---

## Condition de déclenchement

Reprendre ce hook uniquement lorsque les SOP 01 à 12 ont été revues et que leurs décisions méthodologiques sont considérées comme figées.

Pour chaque SOP, vérifier :

- statut final explicite ;
- absence de question méthodologique bloquante ;
- paramètres normatifs décidés ou renvoyés explicitement vers une configuration préenregistrée ;
- entrées et sorties définies ;
- critères `PASS`, `FAIL`, `INCONCLUSIVE` ou statuts équivalents définis ;
- interdictions et conditions de réexécution définies ;
- responsabilités et preuves à archiver définies.

---

## Prochaine étape après la revue individuelle

La prochaine étape n’est pas de rédiger immédiatement du code.

Il faut d’abord réaliser un **audit transversal de cohérence des SOP**, car des décisions prises séparément peuvent être incompatibles entre elles.

### Étape 1 — Audit transversal

Comparer les SOP sur les thèmes partagés :

1. définition de la candidate ;
2. série de rendement primaire ;
3. detrending, benchmark et cash ;
4. segmentation Train/Test/OOS ;
5. fonctionnement des folds Walk-Forward ;
6. univers des règles soumis aux tests multiples ;
7. métrique et seuil de chaque gate ;
8. statuts et conséquences des verdicts ;
9. robustesse et contamination OOS ;
10. données point-in-time ;
11. coûts, sizing, capacité et exécution ;
12. seeds, hashes, versions et archivage ;
13. incubation et passage live.

Livrable :

`Protocole/MATRICE DE COHERENCE DES SOP EBTA.md`

Cette matrice doit signaler :

- contradictions ;
- doublons ;
- termes employés avec plusieurs sens ;
- paramètres définis dans plusieurs SOP ;
- dépendances manquantes ;
- décisions sans propriétaire documentaire.

### Étape 2 — Registre normatif des décisions

Extraire de toutes les SOP les décisions effectivement figées.

Livrable :

`Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md`

Pour chaque décision, enregistrer :

- identifiant ;
- sujet ;
- valeur ou règle retenue ;
- SOP propriétaire ;
- autres SOP concernées ;
- justification ;
- caractère fixe ou configurable ;
- moment du préenregistrement ;
- preuve attendue.

Ce registre devient l’index de référence. Une règle ne doit pas être redéfinie indépendamment dans plusieurs documents.

### Étape 3 — Annexe de configuration

Séparer les principes méthodologiques des valeurs propres à une recherche ou à une famille de stratégies.

Livrable :

`Protocole/TEMPLATE - Configuration préenregistrée d'une recherche EBTA.md`

Cette annexe doit notamment contenir :

- univers et période ;
- fréquence et calendrier ;
- benchmark et référence cash ;
- coûts et slippage ;
- métrique primaire ;
- seuil économique ;
- effet minimal détectable ;
- puissance cible ;
- fenêtres Walk-Forward ;
- purge et embargo ;
- méthodes bootstrap ;
- réplications et seeds ;
- tests de robustesse ;
- critères d’incubation et de suspension.

### Étape 4 — Mise à jour du protocole principal

Réviser `Protocole/PROTOCOLE EBTA.md` sans recopier intégralement les SOP.

Le protocole principal doit devenir :

- la carte générale du processus ;
- l’ordre des gates ;
- la liste des livrables ;
- le mécanisme de gouvernance ;
- l’index des SOP applicables.

Chaque détail technique doit être référencé vers sa SOP propriétaire.

### Étape 5 — Vérification de couverture de l’audit

Reprendre chaque constat de :

`Protocole/AUDIT METHODOLOGIQUE PROTOCOLE EBTA.md`

Pour chaque point, attribuer un statut :

- `CLOSED` : décision figée et document propriétaire identifié ;
- `PARTIAL` : procédure présente mais paramètre ou responsabilité manquant ;
- `OPEN` : problème non résolu ;
- `DEFERRED_IMPLEMENTATION` : méthode décidée, implémentation non réalisée.

Mettre à jour l’audit sans supprimer son diagnostic historique.

### Étape 6 — Paquet d’exécution

Une fois la cohérence documentaire validée, produire les artefacts opérationnels :

- formulaires de préenregistrement ;
- checklists de gate ;
- schémas de configuration ;
- formats de rapports ;
- registre des expériences ;
- journal d’accès OOS ;
- manifeste de reproductibilité ;
- tests automatisés des invariants méthodologiques.

Cette étape transforme les SOP en contrôles exécutables.

### Étape 7 — Revue finale et gel

Effectuer une dernière revue indépendante :

- une même recherche doit produire le même verdict pour deux opérateurs ;
- aucune décision discrétionnaire ne doit apparaître après observation des résultats ;
- chaque verdict doit être reconstructible depuis les données, le code et la configuration archivés ;
- chaque modification postérieure doit créer une nouvelle version identifiable.

Après validation :

- attribuer une version au protocole ;
- dater le gel ;
- produire les hashes des documents ;
- archiver le paquet complet ;
- ouvrir une nouvelle version pour toute évolution future.

---

## Ordre de reprise recommandé

1. Relire ce hook.
2. Relire l’audit méthodologique.
3. Recenser les statuts des SOP 01 à 12.
4. Produire la matrice de cohérence.
5. Corriger les contradictions détectées.
6. Produire le registre normatif.
7. Produire le template de préenregistrement.
8. Mettre à jour le protocole principal.
9. Clôturer les constats de l’audit.
10. Préparer les artefacts exécutables.
11. Réaliser la revue finale.
12. Geler et versionner le protocole EBTA.

---

## Message de reprise à donner à Codex

```text
Reprends la finalisation du protocole EBTA à partir de :

Protocole/HOOK - Finalisation du protocole EBTA après revue des SOP.md

Toutes les SOP ont maintenant été clarifiées.

Commence par vérifier leur statut et réaliser l’audit transversal de cohérence.
Ne modifie pas encore le protocole principal avant d’avoir produit la matrice
des contradictions, doublons, dépendances et décisions sans propriétaire.
```

---

## Critère de fin de la tâche initiale

La tâche initiale sera terminée lorsque :

- tous les constats de l’audit seront clôturés ou explicitement différés ;
- toutes les SOP seront cohérentes entre elles ;
- les décisions normatives seront centralisées et traçables ;
- le protocole principal référencera correctement les SOP ;
- un template de préenregistrement sera disponible ;
- les livrables et preuves exigés à chaque gate seront définis ;
- le protocole complet sera versionné, reproductible et prêt pour son implémentation opérationnelle.
