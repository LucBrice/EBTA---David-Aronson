# Historique des versions EBTA (Changelog)

## Métadonnées documentaires

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - REGISTRE_EVOLUTION |
| Version documentaire | EBTA-DOC-1.1 |
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

### [EBTA-DOC-1.1] - 2026-07-01
**Nature du changement** : Changement normatif
**Résumé** : Ouverture de la gouvernance des biais humains, organisationnels
et assistés par IA avec création de `SOP 13`, du registre `BIAS_RISK_REGISTER.md`,
des templates d'incident et de dérogation, et du gate transversal `G-BIAS`.
`G-BIAS` ne renumérote pas les gates `G0` à `G14`, mais il devient obligatoire
avant ouverture OOS, avant validation reproductible et après tout incident
matériel.
**Documents impactés** : `0-README - Comprendre et maintenir le protocole
EBTA.md`, `PROTOCOLE EBTA.md`, `REGISTRE DES DECISIONS NORMATIVES EBTA.md`,
`MATRICE DE COHERENCE DES SOP EBTA.md`, `PAQUET D'EXECUTION EBTA.md`,
`SOP 03 - Registre des expériences et univers des règles candidates.md`,
`SOP 05 - Tests de robustesse et gouvernance du holdout.md`,
`SOP 08 - Mesures de performance et série de rendement de référence.md`,
`SOP 10 - Gouvernance OOS et gestion des échecs.md`,
`SOP 12 - Reproductibilité et paquet de validation EBTA.md`,
`SOP 13 - Gouvernance des biais humains et incidents méthodologiques.md`,
`BIAS_RISK_REGISTER.md`, `TEMPLATE - Incident de biais EBTA.md`,
`TEMPLATE - Dérogation méthodologique EBTA.md`, `HISTORIQUE DES VERSIONS
EBTA.md`, `MANIFESTE DE GEL EBTA.md`.
**Justification** : Le protocole corrigeait déjà le data-mining bias par WRC et
familles statistiques, mais ne possédait pas d'autorité explicite pour les biais
de conduite de recherche : incident humain, dérogation réparatrice, metric
shopping, robustness shopping, communication influente ou contamination IA.
`EBTA-DOC-1.1` rend ces risques opposables sans créer de source de vérité
concurrente : SOP 13 est propriétaire, SOP 03 journalise, SOP 10 protège l'OOS
et SOP 12 assemble les preuves.

### [EBTA-DOC-1.0] - 2026-06-29
**Nature du changement** : Clarification documentaire sans changement normatif
**Résumé** : Explicitation transversale de la notion de couple
`stratégie × actif` dans le protocole principal, SOP 03, SOP 08, SOP 09A, le
registre normatif et la matrice de cohérence. La clarification rend visible
qu’un actif sélectionnable appartient à l’identité de la candidate et à la
famille testée par WRC, tandis qu’un portefeuille multi-actifs fixe reste une
candidate de portefeuille.
**Documents impactés** : `PROTOCOLE EBTA.md`, `SOP 03 - Registre des
expériences et univers des règles candidates.md`, `SOP 08 - Mesures de
performance et série de rendement de référence.md`, `SOP 09A - Données
point-in-time et contrôles anti-leakage.md`, `REGISTRE DES DECISIONS
NORMATIVES EBTA.md`, `MATRICE DE COHERENCE DES SOP EBTA.md`, `HISTORIQUE DES
VERSIONS EBTA.md`, `MANIFESTE DE GEL EBTA.md`.
**Justification** : Le protocole prévoyait déjà l’univers d’actifs et le
comptage des couples règle-actif dans SOP 03. La règle était toutefois trop
locale pour guider correctement le futur encodage runtime. Cette clarification
ne change ni l’ordre des gates, ni les statuts, ni les seuils, ni les
propriétaires SOP ; elle évite qu’`Implementation/` encode une doctrine plus
explicite que sa source normative.

### [EBTA-DOC-1.0] - 2026-06-26
**Nature du changement** : Clarification documentaire sans changement normatif
**Résumé** : Mise à jour des pointeurs opérationnels subordonnés dans le
protocole principal après archivage des anciens artefacts runtime terminés. Le
protocole pointe désormais vers le hook actif
`Implementation/Active/HOOK.md`
et vers `Implementation/Active/tracking.json` au lieu des anciens fichiers de
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
