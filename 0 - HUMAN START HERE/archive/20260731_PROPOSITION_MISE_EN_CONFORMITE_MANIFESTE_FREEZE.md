# Proposition — Mise en conformité du manifeste de reproductibilité `[FREEZE]`

> [!IMPORTANT]
> **Statut : INTAKE non audité, non exécutable.** Ce brouillon décrit un
> chantier potentiel. Il ne modifie ni le `Protocole/`, ni les gates, ni les
> verdicts. Toute promotion passe par `/start`, les audits requis et un nouveau
> plan normalisé dans `.ai/backlog/`.

## 0. Décision demandée

Ouvrir un chantier de mise en conformité `CONTRACT_ENCODING` afin que le
manifeste de reproductibilité encode entièrement le bloc `[FREEZE]` de la
SOP 06 §22.1 :

```text
code_hash
config_hash
data_hash
reviewer
timestamp
```

`config_hash` est déjà produit. La présente proposition vise seulement
`code_hash`, `data_hash` et `timestamp` **dans le manifeste produit**. Elle ne
doit pas créer une nouvelle règle scientifique : elle rend traçable une
exigence normative déjà gelée.

## 1. Constat vérifié

| Autorité / composant | État actuel |
| --- | --- |
| `Protocole/SOP 06` §22.1 | Les trois champs sont explicitement requis au gel. |
| `Protocole/PAQUET D'EXECUTION EBTA.md` §5 | Le manifeste doit couvrir code, données/snapshots, environnement et hashes. |
| `Implementation/ebta_engine/manifests/manifest_builder.py` | Produit `config_hash`, les snapshots déclarés et les hashes des artefacts, mais aucun champ dédié `code_hash`, `data_hash` ou `timestamp`. |
| `PLAN_REPRODUCTIBILITE_OPERATIONNELLE_R7` (`DONE`) | A livré l'empreinte canonique de `config.json`; ce résultat doit être réutilisé, pas réécrit. |
| `PLAN_HORODATAGE_TRANSVERSAL_ET_ATTESTATIONS` (`DONE`) | A livré des horodatages UTC pour les événements et le scellement; ce résultat doit être réutilisé, pas déplacé. |

Le manque ne remet pas en cause la clôture technique du pivot Nautilus. En
revanche, un futur paquet `PRE_OOS_SEALED` ne doit pas être considéré conforme
tant que son manifeste ne porte pas ces trois éléments avec des définitions
vérifiables.

## 2. Objectif et périmètre proposé

### Objectif

Faire produire et vérifier par le runtime un manifeste qui identifie sans
ambiguïté :

1. la version exacte du code qui a exécuté le build ;
2. le contenu exact du ou des snapshots de données utilisés ;
3. l'instant UTC où le manifeste a été produit/scellé.

### Périmètre candidat

- `Implementation/ebta_engine/manifests/manifest_builder.py` ;
- `Implementation/ebta_engine/schemas/reproducibility_manifest.schema.json` ;
- le builder de paquet qui fournit les identités de code et de données ;
- tests ciblés du manifeste, du builder et du validateur ;
- `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` seulement si une
  implémentation est réellement promue et livrée.

### Non-objectifs absolus

- ne pas modifier `Protocole/`, les SOP, les statuts, seuils ou gates ;
- ne pas rouvrir le pivot Nautilus, ni modifier l'adapter Nautilus ;
- ne pas rouvrir ou consommer l'OOS ;
- ne pas changer les calculs WRC, robustesse, OOS ou économiques ;
- ne pas transformer une preuve absente en `PASS` ;
- ne pas re-hasher silencieusement les paquets historiques comme s'ils avaient
  été scellés avec le nouveau contrat.

## 3. Questions à résoudre pendant l'audit de `/start`

Ces questions concernent l'encodage du contrat, non la doctrine. Elles doivent
être résolues par des choix testables avant tout code.

| Sujet | Exigence de décision technique |
| --- | --- |
| `code_hash` | Définir une empreinte déterministe de la surface de code réellement exécutée (liste de fichiers canonique + SHA-256, ou identifiant Git vérifié + empreinte de propreté). Elle ne doit pas dépendre de fichiers locaux non pertinents. |
| `data_hash` | Définir l'agrégation canonique des hashes des `data_snapshots` réellement lus, et refuser un snapshot sans checksum vérifiable. Le checksum distinct déjà existant dans la configuration doit être réutilisé si son périmètre est exact. |
| `timestamp` | Réutiliser une horloge UTC injectable; le timestamp du manifeste doit être distingué des timestamps d'événements et du `sealed_at`, tout en respectant leur ordre causal. |
| Compatibilité | Décider explicitement si le schéma du manifeste évolue de façon compatible ou requiert une migration SemVer; les anciens paquets restent historiques et ne doivent pas être altérés. |
| Anti-autoreférence | S'assurer qu'aucun hash ne couvre un document qui contient son propre hash sans règle de projection canonique. |

Si l'une de ces définitions implique un nouveau gate, un statut, une règle de
scellement ou une exception méthodologique, arrêter et classer
`NORMATIVE_CHANGE_REQUIRED` plutôt que de coder une interprétation.

## 4. Chemin d'exécution proposé

### Phase 0 — Audit et contrat de compatibilité

- Lire SOP 06 §22.1, SOP 12 et le `PAQUET D'EXECUTION EBTA.md` §5.
- Cartographier les sources existantes : `document_hash`, `data_snapshots`,
  checksums, `sealed_at`, horloge injectée et artefacts du manifeste.
- Choisir et documenter les trois définitions canoniques sans dupliquer les
  conventions déjà livrées par R7 et le lot d'horodatage.
- Déterminer le niveau SemVer du schéma et écrire une migration explicite si
  nécessaire.

### Phase 1 — Encodage du manifeste

- Étendre le schéma et `build_manifest()` avec les champs requis, sans changer
  l'autorité des artefacts sous-jacents.
- Transmettre les valeurs explicites depuis le builder; aucune lecture cachée de
  l'environnement dans le cœur du manifeste.
- Produire un timestamp UTC depuis l'horloge injectable du build.

### Phase 2 — Vérifications de non-divergence

- Prouver qu'un même code, mêmes données et même instant injecté donnent le
  même manifeste.
- Prouver qu'une modification de code ou de données change l'empreinte
  concernée, et que des valeurs absentes/incohérentes échouent explicitement.
- Prouver que les hashes d'artefacts existants, `config_hash`, le scellement et
  les événements restent inchangés hors du contrat ajouté.
- Vérifier une migration de paquet historique : lisible comme historique,
  jamais artificiellement requalifiée `PRE_OOS_SEALED`/`PASS`.

### Phase 3 — Validation et clôture éventuelle

- Exécuter les tests ciblés, la suite runtime complète, les validations de
  schéma, puis `git diff --check`.
- Régénérer un paquet de fixture contrôlée et vérifier le manifeste produit.
- Passer `bug-hunter`, l'audit de conformité au plan et les contrôles de
  workflow requis avant toute `/close`.

## 5. Critères de sortie

Le chantier ne peut être déclaré terminé que si :

- le manifeste produit contient `code_hash`, `config_hash`, `data_hash` et un
  `timestamp` UTC au format contrôlé ;
- les trois nouvelles valeurs sont dérivées de sources explicites,
  déterministes et testées ;
- le schéma accepte le nouveau contrat et traite les paquets historiques selon
  une règle explicite, sans migration silencieuse ;
- une donnée ou un code différent invalide l'empreinte correspondante ;
- aucune ouverture OOS, aucun changement de gate/verdict et aucune modification
  de `Protocole/` n'ont eu lieu ;
- la suite complète et les validateurs concernés passent, sans masquer les
  verdicts scientifiques `FAIL` ou `INCONCLUSIVE` existants.

## 6. Références

- `Protocole/SOP 06 - Sélection des règles candidates et optimisation de la complexité.md` §22.1 ;
- `Protocole/SOP 12 - Reproductibilité et paquet de validation EBTA.md` ;
- `Protocole/PAQUET D'EXECUTION EBTA.md` §5 ;
- `.ai/archive/20260720_PLAN_REPRODUCTIBILITE_OPERATIONNELLE_R7.md` ;
- `.ai/archive/20260721_PLAN_HORODATAGE_TRANSVERSAL_ET_ATTESTATIONS.md` ;
- `.ai/archive/20260710_PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md` §5.2 et §8.3.
