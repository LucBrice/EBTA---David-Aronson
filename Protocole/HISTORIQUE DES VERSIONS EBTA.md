# Historique des versions EBTA (Changelog)

## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - REGISTRE_EVOLUTION |
| Version documentaire | EBTA-DOC-1.0 |
| Date de création | 2026-06-24 |
| Propriétaire documentaire | Gouvernance protocole EBTA |
| Rôle dans le paquet EBTA | Journaliser chronologiquement toutes les évolutions du protocole EBTA. |

## Fonction de ce fichier

Ce registre suit l'évolution des règles et de la documentation du protocole EBTA.
Conformément au `0-README - Comprendre et maintenir le protocole EBTA.md`, toute **évolution normative** ou **ajout documentaire significatif** doit être documenté ici.

### Format attendu pour une nouvelle entrée

```markdown
### [Version] - AAAA-MM-JJ
**Nature du changement** : (Correction / Changement normatif / Ajout)
**Résumé** : Description courte du changement.
**Documents impactés** : Liste des fichiers modifiés.
**Justification** : Pourquoi ce changement était nécessaire (référence au registre normatif si applicable).
```

---

## Historique

### [EBTA-DOC-1.0] - 2026-06-26
**Nature du changement** : Clarification documentaire sans changement normatif
**Résumé** : Mise à jour des pointeurs opérationnels subordonnés dans le
protocole principal après archivage des anciens artefacts runtime terminés. Le
protocole pointe désormais vers le hook actif
`Implementation/HOOK - Plan actif stabilisation archive et pipeline pilote.md`
et vers `Implementation/task_tracking.json` au lieu des anciens fichiers de
reprise archivés.
**Documents impactés** : `PROTOCOLE EBTA.md`,
`HISTORIQUE DES VERSIONS EBTA.md`, `MANIFESTE DE GEL EBTA.md`.
**Justification** : Réduire la pollution du dossier `Implementation/` en
déplaçant les hooks/plans/contextes terminés vers
`Implementation/Archives/completed_2026-06-26/`, tout en conservant la
traçabilité. Aucun ordre de gate, statut, seuil, propriétaire SOP ni règle EBTA
n'est modifié.

### [EBTA-DOC-1.0] - 2026-06-26
**Nature du changement** : Clarification documentaire sans changement normatif
**Résumé** : Enrichissement du protocole principal avec une carte processuelle
complète, les boucles locales et globales EBTA, puis simplification de la
section de reprise pour éviter de dupliquer l’ordre de lecture déjà centralisé
dans le `0-README`. Les diagrammes processuels sont accompagnés de tableaux de
lecture indiquant les SOP propriétaires de chaque étape. Ajout dans le
`0-README` d'un parcours par profil de lecteur et d'une table de routage
question -> document/SOP pour faciliter la découverte sans réécrire les SOP.
**Documents impactés** : `0-README - Comprendre et maintenir le protocole EBTA.md`,
`PROTOCOLE EBTA.md`, `HISTORIQUE DES VERSIONS EBTA.md`, `MANIFESTE DE GEL EBTA.md`.
**Justification** : Le protocole principal restait normativement correct mais
trop plat pour servir de point d’entrée processuel. La clarification restaure
la lisibilité du processus tout en gardant le `0-README` comme point d’entrée
documentaire. L’ajout de références SOP dans les diagrammes facilite le passage
du schéma général vers les procédures détaillées. Le parcours par profil évite
une réécriture lourde des SOP, qui restent les autorités détaillées, tout en
aidant l'expert extérieur, le connaisseur et le débutant à ouvrir les bons
documents. Aucun ordre de gate, statut, propriétaire SOP ni élément d'autorité
n'est modifié.

### [EBTA-DOC-1.0] - 2026-06-24
**Nature du changement** : Ajout documentaire (Maintenance)
**Résumé** : Création de ce registre d'évolution (Historique des versions) et de l'agent "Gardien du Protocole".
**Documents impactés** : `0-README - Comprendre et maintenir le protocole EBTA.md`, `MANIFESTE DE GEL EBTA.md`, création locale de la compétence (Skill) de l'agent.
**Justification** : Assurer la traçabilité des futures évolutions du protocole après le gel initial.

### [EBTA-DOC-1.0] - 2026-06-24
**Nature du changement** : Gel initial
**Résumé** : Version initiale gelée du protocole EBTA après revue des SOP 01 à 12, audit de cohérence et création du manifeste.
**Documents impactés** : L'ensemble du dossier `Protocole/`.
**Justification** : Point de départ robuste et opposable pour l'Evidence-Based Technical Analysis.
