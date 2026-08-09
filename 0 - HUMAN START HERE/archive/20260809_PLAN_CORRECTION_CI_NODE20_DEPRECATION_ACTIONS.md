# Brouillon — Correction de la dépréciation Node.js 20 dans le workflow CI `ebta-runtime-suite`

> Statut de ce document : `INTAKE`, brouillon humain non audité. Aucune
> implémentation n'est autorisée par sa seule existence. Aucune commande
> `gh`, `git commit` ou `git push` n'a été exécutée pour produire ce
> brouillon — seules des lectures locales et deux requêtes `gh api`
> read-only (releases publiques `actions/checkout`) ont servi à documenter
> l'état constaté ci-dessous.

---

## 0. Bandeau de statut

| Question | Réponse |
| --- | --- |
| Un chantier actif couvre-t-il déjà ce périmètre ? | Non. `.ai/checkpoint.json::active_workstream_id` = `null` (vérifié dans cette session). Le chantier fermé le plus proche, `PLAN_CORRECTION_PYREFLY_CI_WINDLL_LINUX` (voir commit `68eee9a`), a corrigé un problème Pyrefly/plateforme dans ce même workflow, pas la dépréciation Node.js des actions. |
| Un verrou de gouvernance actif bloque-t-il ce chantier ? | Aucun identifié : `.github/workflows/` n'est pas listé parmi les zones protégées de `.ai/governance/AI_MODIFICATION_CHECKLIST.md` (Protocole/, Implementation/, .agents/, .codex/). |
| Décision humaine nécessaire pour lever un verrou ? | Non identifiée comme bloquante ; simple confirmation humaine du principe (bump de version d'action tierce) recommandée avant `/start`, par prudence CI. |
| Ce plan remplace-t-il un chantier existant ? | Non. |

---

## 1. Objectif

Faire disparaître l'avertissement GitHub Actions observé sur le workflow
`runtime-suite` :

```text
Node.js 20 is deprecated. The following actions target Node.js 20 but are
being forced to run on Node.js 24: actions/checkout@11bd71901bbe..., 
actions/setup-python@a26af69be9...
```

en bumpant les deux actions tierces épinglées par SHA vers des versions
publiées qui embarquent nativement un runtime Node.js plus récent, sans
changer le comportement fonctionnel du workflow.

## 2. Contexte

`.github/workflows/ebta-runtime-suite.yml` est le seul workflow CI du
dépôt. Il sert de "verdict indépendant" (voir son en-tête de commentaire,
lignes 3-9) — une preuve produite sur une infrastructure que l'agent de
codage ne contrôle pas et ne peut pas contourner silencieusement avec
`--no-verify`. Deux étapes y épinglent des actions tierces par SHA complet
avec un commentaire de version :

```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
- uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5.6.0
```

GitHub a annoncé la dépréciation des runners d'action Node.js 20
(2025-09-19) ; ces deux versions ciblent encore Node.js 20 en interne et
sont donc actuellement forcées sur Node.js 24 par la plateforme — un
avertissement aujourd'hui, un probable échec dur après la fin de la période
de tolérance annoncée par GitHub.

## 3. État vérifié dans cette session

- Fichier concerné : `.github/workflows/ebta-runtime-suite.yml`, lignes 49
  et 54 (`Checkout` et `Set up Python`).
- Dernière release publique `actions/checkout` au moment de la rédaction :
  `v7.0.1`, SHA de tag `3d3c42e5aac5ba805825da76410c181273ba90b1` (vérifié
  via `gh api repos/actions/checkout/releases/latest` et
  `gh api .../git/refs/tags/v7.0.1`, lecture seule, dépôt public GitHub).
- SHA/version cible pour `actions/setup-python` **non encore vérifié** dans
  cette session (requête interrompue) : à confirmer via
  `gh api repos/actions/setup-python/releases/latest --jq '.tag_name'` puis
  `gh api repos/actions/setup-python/git/refs/tags/<tag>' --jq '.object.sha'`
  au moment de l'implémentation, pas en le devinant depuis ce brouillon.
- Aucun autre fichier du workflow n'est concerné : `pip install` versions
  figées (`jsonschema==4.23.0`, `numpy==2.2.6`, `pandas==2.3.3`,
  `pyrefly==1.1.1`, `ruff==0.16.2`) restent hors scope de cette correction.
- Aucun chantier `.ai/backlog/` ni `.ai/archive/` existant ne couvre déjà ce
  point précis (recherche non exhaustive, à reconfirmer par l'audit
  `/start`).

## 4. Décision humaine requise avant `/start`

Ce brouillon ne fixe pas encore : bumper `actions/checkout` et
`actions/setup-python` vers leurs dernières releases respectives (recommandé,
suit directement l'avertissement GitHub), ou seulement vers la première
version publiée qui abandonne Node.js 20 sans nécessairement prendre le tout
dernier tag (plus conservateur, diff plus petit à auditer). Recommandation :
prendre la dernière release stable de chaque action, car ce sont des actions
GitHub officielles à adoption large et le dépôt n'a pas de contrainte de
compatibilité connue avec une version intermédiaire.

## 5. Non-objectifs

- Ne pas changer la logique du workflow (étapes, ordre, permissions,
  déclencheurs `on: push` / `workflow_dispatch`).
- Ne pas changer les versions épinglées des paquets Python
  (`jsonschema`, `numpy`, `pandas`, `pyrefly`, `ruff`).
- Ne pas modifier `Protocole/`, `Implementation/`, `.ai/`, `.agents/`,
  `.codex/`.
- Ne pas désactiver ou affaiblir une étape du workflow pour faire
  disparaître l'avertissement autrement que par le bump de version.

## 6. Invariants

1. Le workflow doit rester un job unique `ubuntu-latest`, sans changement de
   permissions (`contents: read`).
2. Chaque action bumpée reste épinglée par SHA complet, avec le commentaire
   de version en fin de ligne (convention déjà en place, ligne 49 et 54).
3. Le SHA utilisé doit être vérifié directement depuis le dépôt officiel de
   l'action au moment de l'implémentation (`gh api .../releases/latest` puis
   résolution du tag en SHA), jamais recopié d'une mémoire ou d'un brouillon
   qui pourrait être obsolète.
4. La suite de tests existante du workflow (`unittest discover`, validations
   JSON, Pyrefly, Ruff) doit continuer à passer à l'identique après le bump.

## 7. Risques et modes d'échec

| Risque | Impact | Mitigation |
| --- | --- | --- |
| Une nouvelle version majeure d'`actions/setup-python` change son comportement par défaut (ex. cache, résolution de version Python). | Le job CI échoue après le bump. | Lire le changelog de la version cible avant de bumper ; tester sur une branche ou via `workflow_dispatch` avant de considérer le chantier terminé. |
| Le SHA recopié depuis ce brouillon devient obsolète (une nouvelle release sort entre la rédaction et l'implémentation). | Épinglage sur une version qui n'est déjà plus la dernière. | Invariant §6.3 : toujours revérifier au moment de l'implémentation, ne jamais réutiliser aveuglément le SHA de ce brouillon. |
| L'avertissement Node.js 20 réapparaît pour une des deux actions si la nouvelle version ciblée le supporte encore en interne. | Correction incomplète. | Vérifier explicitement, après le bump, qu'aucun avertissement Node.js 20 ne subsiste dans les logs d'un run CI réel. |

## 8. Phases d'implémentation proposées

### Phase 1 — Résoudre les versions cibles

- Confirmer la dernière release `actions/checkout` (déjà fait dans cette
  session : `v7.0.1` / `3d3c42e5aac5ba805825da76410c181273ba90b1`, à
  revérifier si le temps a passé).
- Résoudre la dernière release `actions/setup-python` (non fait dans cette
  session, à faire à l'implémentation).

### Phase 2 — Bumper le workflow

- Remplacer les deux lignes `uses:` avec le nouveau SHA et le commentaire de
  version à jour.
- Ne toucher aucune autre ligne du fichier.

### Phase 3 — Vérifier en CI réelle

- Pousser sur une branche ou déclencher `workflow_dispatch` (avec
  autorisation humaine explicite de push, cf. règles de permission de ce
  dépôt).
- Confirmer dans les logs du run : plus d'avertissement Node.js 20, toutes
  les étapes existantes toujours `PASS`.

## 9. Tests / preuves attendues

- Lecture du run CI déclenché en Phase 3 : absence du message
  « Node.js 20 is deprecated » dans les logs.
- Toutes les étapes existantes du job (`unittest discover`, Pyrefly, Ruff,
  validations JSON checkpoint/tracking) restent `PASS`.
- `git diff` limité aux deux lignes `uses:` (plus commentaire de version) —
  aucun autre changement dans le fichier.

## 10. Critères de sortie vérifiables

- Le run CI déclenché après le bump ne contient plus l'avertissement
  Node.js 20 pour `actions/checkout` ni pour `actions/setup-python`.
- Le job `runtime-suite` reste entièrement `PASS`.
- Aucun fichier autre que `.github/workflows/ebta-runtime-suite.yml` n'est
  modifié.

## 11. Fichiers autorisés / interdits

**Autorisé** :

```text
.github/workflows/ebta-runtime-suite.yml   [MODIFIER - lignes des deux `uses:` uniquement]
```

**Interdit** :

```text
Protocole/               [NORME - intouchable]
Implementation/          [RUNTIME - hors scope]
.ai/                     [COCKPIT - hors scope]
.agents/ .codex/         [TOOLING - hors scope]
```

## 12. Rollback

Un seul commit ciblé sur `.github/workflows/ebta-runtime-suite.yml` ;
`git revert` de ce commit suffit à restaurer l'état antérieur si le run CI
échoue après le bump. Aucun état persistant, schéma ou donnée n'est affecté.

## 13. Distinction analyse / persistance / commit / push

- Ce brouillon = analyse et proposition seulement ; aucun fichier de
  workflow n'a été modifié pour le produire.
- Une future implémentation nécessite une autorisation humaine séparée pour
  chacune des étapes suivantes : modifier le fichier, committer, pousser
  (le déclenchement réel du workflow CI dépend d'un push ou d'un
  `workflow_dispatch`, donc l'autorisation de push est structurellement
  nécessaire pour produire la preuve de la Phase 3).

---

## 14. Journal des décisions humaines

| Date | Décision | Portée |
| --- | --- | --- |
| 2026-08-09 | Signaler l'avertissement Node.js 20 sur `runtime-suite` et demander qu'un plan soit rédigé avant tout fix. | Autorise uniquement la rédaction de ce brouillon `INTAKE`. N'autorise ni `/start`, ni modification du workflow, ni push. |

## 15. Definition of Done (de ce brouillon)

- [x] Cause de l'avertissement identifiée et documentée avec citation
      exacte du message.
- [x] Fichier et lignes concernés localisés précisément.
- [x] Une version cible vérifiée (`actions/checkout`) ; l'autre marquée
      explicitement comme à revérifier à l'implémentation, pas devinée.
- [x] Aucune modification du workflow ni d'aucun autre fichier.
- [x] Aucun commit, aucun push.
