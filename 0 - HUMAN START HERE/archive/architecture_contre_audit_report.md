# Contre-audit indépendant — `IA_Diagramme_architecture.drawio`

**Fichier audité :** `.ai/architecture/IA_Diagramme_architecture.drawio` (diagram id `page_process_first`, 71 nœuds, 107 arêtes, 9 calques draw.io)
**Audit de référence :** `0 - HUMAN START HERE/architecture_anomalies_report.md` (ci-après « l'audit initial »)
**Méthode :** lecture directe et exhaustive du XML (aucune inférence visuelle), extraction programmatique de tous les `id`, `source`, `target`, `relation_type`, `component`, `layer_primary`, `layer_related`, `robustness`, `kind`, calques et attributs `visible`. Comparaison ensuite seulement avec l'audit initial.

---

## 0. Executive summary

| Axe | Verdict |
|---|---|
| Exactitude architecturale | Globalement saine ; deux angles morts sérieux côté domaine EBTA (validation scientifique non alimentée, campagnes d'expérimentation orphelines) |
| Machine-readability | Bonne (0 arête cassée, 0 ID dupliqué, vocabulaire `relation_type` 100% conforme, `robustness` 100% conforme) mais **une anomalie de production critique pour l'usage** : 2 des 9 calques sont `visible="0"` par défaut |
| Cohérence des métadonnées | Très bonne (aucun `layer_primary == layer_related`, aucun `layer_primary` manquant) ; 1 arête sans attribut `kind` |
| Cohérence des relations | Bonne ; vocabulaire respecté partout, mais la méthodologie de l'audit initial (comptage brut des flèches) produit plusieurs faux positifs sur les nœuds lus via `relation_type="READ"` |
| Lisibilité du processus | Le chemin principal FLOW est complet et sans impasse ; les deux portes PASS/FAIL (`decision_gate`, `ci_decision`) ont chacune leurs deux branches câblées |
| Angles morts | 2 nouveaux angles morts significatifs non couverts par l'audit initial (tous deux dans la couche domaine EBTA, L01/L03/L04) |

**Verdict final : ARCHITECTURE SAINE AVEC CORRECTIONS MINEURES.** Aucune incohérence ne remet en cause l'architecture générale ; les corrections nécessaires sont ciblées (calques masqués, 2 arêtes manquantes, 2 attributions de robustesse à revoir).

---

## 1. Modèle mental reconstruit (indépendamment)

- **71 nœuds** (`<object component="…" layer_primary="…" …>`), tous avec ID sémantique unique (`node_xxx`).
- **107 arêtes** (`<object relation_type="…" …>` + `<mxCell edge="1" source=… target=…>`), toutes avec ID sémantique unique (`edge_xxx`).
- **9 calques draw.io** réels (`<mxCell id="layer_xxx" parent="0" style="locked=1;" value="…">`), tous référencés par au moins un nœud.
- **Vérification croisée programmatique** : les 71 `source`/`target` référencés par les 107 arêtes correspondent exactement aux 71 nœuds déclarés — **0 arête cassée, 0 nœud orphelin (non référencé par une arête), 0 ID dupliqué** (le seul `id="0"` est la racine `mxGraphModel`, normal en draw.io).
- Vocabulaire `relation_type` : les 107 arêtes n'utilisent **que** `FLOW / USE / READ / WRITE / CONTROL / VALIDATE / OBSERVE / FEEDBACK / DEPLOY` — conformité à 100 %.
- Vocabulaire `robustness` : toutes les valeurs (y compris listes séparées par virgule, ex. `PREVENTION,DETECTION`) appartiennent à `{PREVENTION, DETECTION, CONFINEMENT, RECOVERY, EVIDENCE}` — conformité à 100 %.
- `layer_primary` jamais vide, jamais égal à `layer_related` — conformité à 100 %.

**Processus principal reconstitué (arêtes `relation_type="FLOW"` uniquement) :**

```
User → Objective → Specification → Context Loader → Planner → Task Decomposition
→ Orchestrator → Scheduler → Worker Agent →(USE)→ Tool Router →(USE)→ Tools
→ Sandbox → Artifact → Verification → Decision Gate
   ├─PASS→ Pass → Git Change → Commit → Push → Pull Request → Review → CI → CI Decision
   │         ├─PASS→ Merge → Release →(DEPLOY)→ Target System
   │         └─FAIL→ Repair Loop (rejoint la boucle FAIL ci-dessous)
   └─FAIL→ Repair Loop → Error Evidence → Diagnostic → Root Cause → Correction → Re-Test → Verification (ré-entrée)
```

Les deux portes de décision (`decision_gate`, `ci_decision`) ont chacune une branche PASS et une branche FAIL réellement câblées en XML — **aucun chemin mort, aucune boucle mal refermée**. La boucle de réparation demandée (§7 de la mission) existe telle que spécifiée : `FAIL → repair_loop → error_evidence → diagnostic → root_cause → correction → retest → verification`, plus un feedback explicite `repair_loop --FEEDBACK--> worker_agent` (label « IMPLEMENT », trait pointillé) et un second point d'entrée `ci_decision --FEEDBACK--> repair_loop` (label « FAIL → REPAIR »). Ce sont de vraies arêtes XML, pas une convention graphique.

---

## 2. Faille méthodologique centrale de l'audit initial (à comprendre avant la comparaison)

L'audit initial classe les nœuds en « puits » / « sources » en **comptant les flèches entrantes/sortantes brutes**. Mais la convention de ce diagramme (donnée en exemple dans la mission : *« Context Loader → READ → Memory »*) précise que **la flèche pointe vers l'objet lu**, pas vers le lecteur — c'est-à-dire qu'une arête `relation_type="READ"` dont la cible est un nœud X **ne prouve pas que X n'est jamais lu : elle prouve le contraire**, X est en train d'être lu par la source de l'arête.

L'audit initial n'a pas croisé `relation_type` avec le sens de la flèche : il a traité toute flèche entrante comme une preuve d'écriture et toute absence de flèche sortante comme une preuve de non-lecture. Résultat vérifié dans le XML : sur ses 4 nœuds détaillés en « bug de modélisation » (Evidence Store, Task State, Checkpoint, Memory), **3 ont en réalité au moins une arête `READ` entrante qui prouve leur consultation réelle** ; seul `checkpoint` est un vrai puits mort. Le détail est donné section 3.

Cette faille invalide partiellement (pas totalement) les conclusions de l'audit initial sans invalider son intuition de départ, qui reste souvent légitime une fois reformulée correctement (voir ci-dessous, nœud par nœud).

---

## 3. Anomalies de l'audit initial — classement

| # | Nœud / sujet | Claim de l'audit initial | Verdict | Justification (preuve XML) |
|---|---|---|---|---|
| 1 | `node_checkpoint` | Puits mort, `node_resume` non connecté | **CONFIRMÉE** | 2 arêtes entrantes (`USE` depuis `recovery_controller`, `WRITE` depuis `orchestrator`), **0 arête sortante, aucune de type READ**. `node_resume` n'a aucune arête entrante depuis `checkpoint`. C'est le seul des 4 nœuds « Catégorie A » de l'audit initial qui résiste entièrement à la vérification stricte. |
| 2 | `node_evidence_store` | « 8 IN / 0 OUT — amnésie du système, aucun agent ne relit » | **PARTIELLEMENT CONFIRMÉE** | Le décompte brut (8 entrantes) est exact, mais 1 des 8 est `relation_type="READ"` (`node_human_approval --READ--> node_evidence_store`, label « EVIDENCE ») : l'approbateur humain lit réellement le store avant de trancher. L'affirmation « jamais relu » est donc factuellement fausse. En revanche l'inquiétude de fond reste valide : **aucun agent IA** (worker_agent, orchestrator, planner) ne relit l'historique d'exécution pour apprendre — seule la porte humaine le fait. |
| 3 | `node_task_state` | « 2 IN / 0 OUT — l'orchestrateur n'a pas de flèche pour le consulter » | **PARTIELLEMENT CONFIRMÉE** | Vrai que `orchestrator` ne relit jamais son propre état écrit (`orchestrator --WRITE--> task_state`, aucune relecture par l'orchestrateur). Mais l'arête `scheduler --READ--> task_state` (label « STATE ») existe : un autre composant, le Scheduler, consulte bien l'état des tâches pour décider du prochain dispatch — design défendable (c'est le rôle naturel d'un scheduler). L'affirmation « 0 OUT » au sens « personne ne consulte » est fausse ; le vrai gap, plus précis, est que l'orchestrateur écrit un état qu'il ne relit jamais lui-même. |
| 4 | `node_memory` | « 1 IN / 0 OUT — mémoire morte, écrite mais jamais relue » | **NON CONFIRMÉE (faux positif, direction inversée)** | La seule arête touchant `node_memory` est `context_loader --READ--> memory` (label « READ »). C'est l'exact inverse du diagnostic initial : la mémoire **est lue** par le Context Loader, mais **rien ne l'alimente jamais** — aucune arête `WRITE` ne cible `node_memory` nulle part dans les 107 arêtes. Le vrai bug est « la mémoire ne sera jamais peuplée », pas « la mémoire n'est jamais relue ». C'est l'erreur la plus nette de l'audit initial : il a interprété une arête `READ` comme une `WRITE` sans vérifier l'attribut `relation_type`. |
| 5 | `node_observability` | « 0 IN / 7 OUT — agit à l'aveugle, ajouter TELEMETRY depuis sandbox/CI » | **PARTIELLEMENT CONFIRMÉE** | Le décompte (0 entrante, 7 sortantes) est exact. Mais 6 des 7 sont `relation_type="OBSERVE"`, et la mission elle-même donne l'exemple canonique *« Observability → OBSERVE → Worker Agent »* : par construction, une arête OBSERVE part **toujours** de l'observateur vers l'observé — `node_observability` ne peut structurellement pas avoir d'arête OBSERVE entrante sans violer la convention SOURCE→ACTION→TARGET du diagramme. Ce n'est donc pas un bug. Le correctif proposé (« TELEMETRY ») n'existe d'ailleurs pas dans le vocabulaire officiel. Ceci dit, l'intuition reste partiellement fondée : il n'existe **aucune arête `WRITE`** de type « sandbox/CI émettent des logs vers observability » (distincte d'OBSERVE), ce qui est une vraie lacune mais mal nommée dans l'audit initial. |
| 6 | `node_recovery_controller` | « 0 IN / 5 OUT — déclencheur fantôme, ajouter arête depuis `decision_gate` FAIL » | **CONFIRMÉE** (avec une nuance) | 0 arête entrante confirmée, 5 `USE` sortantes vers retry/timeout/checkpoint/resume/rollback. Vrai déclencheur fantôme. Nuance : la correction suggérée (relier `decision_gate` FAIL) mélangerait deux classes d'échec distinctes — `decision_gate` FAIL est un échec **qualité** (test/contrat), qui alimente déjà `repair_loop`, alors que `recovery_controller` gère des échecs **d'infrastructure** (timeout, crash, retry). Le lien manquant est plutôt « `sandbox`/`worker_agent` signale un incident d'exécution → `recovery_controller` ». |
| 7 | `node_user`, `node_policy` | Sources légitimes | **CONFIRMÉE** | `node_user` (déclencheur humain externe) et `node_policy` (règles statiques préconfigurées) sont bien les deux seuls nœuds dont l'absence d'arête entrante est structurellement normale — exactement le cas d'usage donné en exemple dans la mission (*« Policy → CONTROL → Tool Router »*). |
| 8 | « Validation scientifique initiale » classée source légitime (3ᵉ source) | Source légitime au même titre que User/Policy | **NON CONFIRMÉE** — voir angle mort nouveau §5.1 | `node_scientific_validation` a bien 0 arête entrante, mais contrairement à `policy` (config statique) elle est censée valider des **résultats dynamiques de backtest** à chaque exécution — elle n'a structurellement rien d'axiomatique. L'audit initial la classe « légitime » dans son tableau récapitulatif final sans jamais l'analyser en détail dans son propre tableau « Catégorie B » (qui ne liste que 2 lignes, `node_user` et `node_policy`, pas 3). Voir analyse complète §5.1 : je la reclasse en anomalie de causalité. |
| 9 | `node_target_system` classé puits légitime, avec remarque « une arête de télémétrie vers l'observabilité reste une bonne pratique » (implicite : absente) | — | **DÉJÀ CORRECTE / obsolète** | L'arête existe déjà : `observability --OBSERVE--> target_system`. La remarque de l'audit initial suggère une lacune qui n'existe pas dans le fichier. |
| 10 | Tableau récapitulatif final : « 5 Vrais Bugs » (liste seulement 4 : Evidence, Task State, Checkpoint, Memory) et « 3 Sources Légitimes » (détaille seulement 2 : User, Policy) | — | **Incohérence interne au rapport initial** | Les totaux annoncés dans le résumé (5 puits-bugs, 3 sources légitimes) ne correspondent pas au nombre de lignes réellement détaillées dans les tableaux du même rapport (4 et 2 respectivement). Le 5ᵉ « bug » (« Data ») et la 3ᵉ « source légitime » (validation scientifique) ne sont jamais nommés avec un ID de nœud ni justifiés par un comptage — signe que l'audit initial n'a pas vérifié ces deux entrées avec la même rigueur que les autres. |
| 11 | Nœuds outils (`tool_shell`, `tool_git`, etc.), `node_agent_specializations`, comptage global 71 nœuds / 23 puits / 5 sources | — | **CONFIRMÉE** | Ma reconstruction indépendante retombe exactement sur les mêmes comptes bruts (71 nœuds, 23 nœuds à 0 sortante, 5 nœuds à 0 entrante) — la **topologie brute** de l'audit initial est fiable ; seule l'**interprétation sémantique** de certains nœuds READ est en cause (voir points 2, 3, 4, 5 ci-dessus). |

---

## 4. Faux positifs confirmés (à ne pas corriger tels quels)

1. **`node_memory` « jamais relu »** — faux, c'est l'inverse : jamais écrit. Corriger l'énoncé du problème avant de corriger le diagramme, sinon on risque d'ajouter une arête `READ` redondante (une existe déjà) au lieu de la vraie arête manquante (`WRITE` vers `memory` depuis, par exemple, `correction`/`diagnostic`/`retest`, qui capitaliseraient les leçons apprises).
2. **`node_observability` « nécessite une arête TELEMETRY »** — la relation `OBSERVE` ne peut par construction pas être entrante sur l'observateur ; le vocabulaire « TELEMETRY » n'existe pas dans la charte du diagramme. Si un correctif est voulu, il doit utiliser `WRITE` (comme `error_evidence --WRITE--> evidence_store`), pas inventer un type.
3. **`node_evidence_store` « 0 OUT, jamais relu »** — faux, `human_approval` le lit réellement (arête `READ` existante).
4. **`node_target_system` « manque une arête de télémétrie »** — l'arête existe déjà (`observability --OBSERVE--> target_system`).
5. **Validation scientifique classée « source légitime »** — voir §3 point 8 et §5.1 : c'est en réalité une anomalie de causalité, pas un choix légitime.

---

## 5. Anomalies nouvelles (non couvertes par l'audit initial)

### 5.1 [P1 — IMPORTANT] `node_scientific_validation` n'a aucune arête entrante — la validation scientifique EBTA valide dans le vide

**Preuve XML :** `node_scientific_validation` (kind=`VALIDATOR`, layer_primary=`L04`) a exactement 3 arêtes, **toutes sortantes** : `VALIDATE→artifact`, `FLOW(« DOMAIN VERDICT »)→decision_gate`, `WRITE→evidence_store`. Aucune arête ne relie `node_backtest_engine` (qui produit trades/positions/résultats, `layer_primary=L03`) à `node_scientific_validation`. La seule arête sortante de `backtest_engine` vers l'« amont » du système de qualité passe par `node_artifact` (`WRITE`, label « RESULTS »), pas directement par `scientific_validation`.

**Pourquoi ça compte :** dans la hiérarchie d'autorité de ce dépôt (`Protocole EBTA`), la validation scientifique (WRC/SPA/Romano-Wolf, Walk-Forward, OOS) est la couche la plus critique — c'est elle qui décide si un résultat de backtest reflète un vrai edge ou du bruit. Le diagramme la représente comme émettant un « DOMAIN VERDICT » vers `decision_gate` sans jamais montrer ce qu'elle valide concrètement, ni ce qui déclenche son exécution.

**Brique existante qui pourrait déjà couvrir le besoin :** aucune — ni `node_verification` (qui `USE` explicitement 5 sous-vérifications logicielles — `static_checks`, `software_tests`, `test_quality`, `contract_validation`, `independent_verification` — mais **jamais** `scientific_validation`) ni `node_artifact` ne relient formellement les deux.

**Lacune :** réelle. **Gravité :** IMPORTANT (P1) — ce n'est pas un blocage fonctionnel du diagramme générique, mais c'est une incohérence dans la partie la plus spécifique et la plus critique du domaine EBTA que ce diagramme prétend représenter. **Pertinence actuelle :** oui, immédiate — c'est une omission de câblage, pas une extension future.

### 5.2 [P2 — IMPORTANT] `node_experiment_campaign` est configuré mais jamais exécuté

**Preuve XML :** `node_experiment_campaign` (« Campagnes · variantes · critères de réussite », L01) a une unique arête entrante (`specification --CONTROL--> experiment_campaign`) et **aucune arête sortante**. Rien ne relie les campagnes définies à `node_research_space`, `node_backtest_engine` ou `node_worker_agent`. Le concept de « campagne contrôlée » existe donc dans le graphe comme pure configuration, jamais consommé par le pipeline d'exécution.

**Gravité :** IMPORTANT (P2, moins critique que 5.1 car moins central à l'autorité normative). **Pertinence actuelle :** oui.

### 5.3 [P2 — AMÉLIORATION] `node_data_lifecycle` et `node_data_reproducibility` ne sont pas reliés entre eux

**Preuve XML :** les deux nœuds L02 adjacents (« Data Lifecycle » : ingestion/validation/versionnement, et « Reproducible Data » : version/provenance connues) sont chacun lus indépendamment par `context_loader`, et `data_reproducibility` est en plus lu par `backtest_engine` — mais aucune arête ne va de `data_lifecycle` vers `data_reproducibility`, alors que la provenance/versionnement que revendique le second devrait logiquement être **produite** par le premier.

**Gravité :** AMÉLIORATION (P2/P3) — cohérence conceptuelle plutôt que rupture fonctionnelle grave, cette relation pouvant être considérée comme implicite dans un diagramme de ce niveau d'abstraction.

### 5.4 [P1 — MACHINE-READABILITY, CRITIQUE POUR L'USAGE] Deux calques safety-critical sont masqués par défaut

**Preuve XML (vérifiée, pas une supposition) :**
```
line 312: <mxCell id="layer_feedback_recovery" ... value="02 — FEEDBACK & RECOVERY" visible="0" />
line 530: <mxCell id="layer_control_security" ... value="03 — CONTROL & SECURITY" visible="0" />
```
Ce sont les **deux seuls** calques (sur 9) portant `visible="0"`. Or ce sont précisément les calques qui contiennent : la totalité de la boucle de réparation (`repair_loop`, `error_evidence`, `diagnostic`, `root_cause`, `correction`, `retest`, `recovery_controller`, `retry`, `timeout`, `checkpoint`, `resume`, `rollback`) et la totalité de la couche guardrails/permissions (`policy`, `human_approval`).

**Pourquoi ça compte :** quiconque ouvre ce fichier dans draw.io sans savoir qu'il doit cocher manuellement ces deux calques dans le panneau « Layers » ne verra **ni** la boucle de réparation **ni** la couche de contrôle/sécurité — soit une bonne partie de ce qui rend l'architecture « robuste ». C'est un défaut de production probablement involontaire (état de calque laissé après une session d'édition en mode focalisé), mais c'est une vraie anomalie de machine-readability/lisibilité que l'audit initial (qui a raisonné en pur comptage de degrés, sans jamais inspecter les calques comme demandé au point 9 de la mission) n'a pas du tout couverte.

**Gravité :** IMPORTANT (P1) — trivial à corriger (retirer `visible="0"`), mais à fort impact sur la lisibilité réelle du fichier.

### 5.5 [P3 — MACHINE-READABILITY, MINEUR] Une arête sans attribut `kind`

**Preuve XML :** `edge_verification_to_artifact_validate` (ligne 302) est la seule des 107 arêtes dont le tag `<object>` ne porte pas `kind="RELATION"`, contrairement à toutes les autres. Sans conséquence fonctionnelle mais incohérence de métadonnées pure.

### 5.6 [P3 — DISCUTABLE] Deux attributions de `robustness` probablement artificielles

- `node_pull_request` porte `robustness="PREVENTION,DETECTION"`. Or la Pull Request elle-même est un artefact de coordination : les fonctions P/D réelles sont déjà portées, correctement, par `node_review` (`DETECTION`) et `node_ci` (`DETECTION`) qui s'exécutent *à cause* de la PR. Lui attribuer directement P/D ressemble à l'exact biais que la mission demande de traquer (§8 : « ne pas considérer qu'une brique possède une fonction de robustesse uniquement parce qu'elle contribue globalement à un système robuste »). **Incohérence probable**, pas une erreur certaine — un rapprochement défendable existe (la PR est le point de non-retour qui *rend obligatoires* les contrôles).
- `node_context_loader` porte `robustness="PREVENTION"`. Le rôle premier du nœud est informationnel (charger le contexte), pas préventif. Défendable si on considère que l'absence de contexte est elle-même une classe d'erreur qu'on prévient, mais c'est un classement plus extensif que les autres nœuds `PREVENTION` du graphe (`specification`, `tool_router`, `policy`), qui bloquent activement une action. **Choix discutable mais acceptable.**

### 5.7 [P3 — DOCUMENTATION] En-tête de l'audit initial pointe vers un chemin de fichier différent

Le rapport initial référence `file:///d:/Livre/Veille/IA%20-%20Diagramme%20architecture`, distinct du chemin réellement audité (`.ai/architecture/IA_Diagramme_architecture.drawio` dans ce dépôt EBTA). Le contenu analysé correspond bien, nœud pour nœud, au fichier actuel (mêmes 71 IDs, mêmes comptes 23/5) — il s'agit donc très probablement d'un lien source obsolète ou copié depuis un autre projet, pas d'un audit d'un autre fichier. Sans impact sur le fond, mais à corriger pour la traçabilité documentaire.

---

## 6. Angles morts architecturaux (au-delà de la comparaison avec l'audit initial)

| Angle mort potentiel | Pourquoi il compte | Brique existante | Lacune réelle ? | Gravité | Pertinence |
|---|---|---|---|---|---|
| `scientific_validation` non alimenté par `backtest_engine` (détaillé §5.1) | Cœur de l'autorité normative EBTA | Aucune | Oui | CRITIQUE pour le sous-domaine EBTA / IMPORTANT pour le diagramme générique | Actuelle |
| Calques safety-critical masqués (détaillé §5.4) | Lisibilité/production du livrable lui-même | Aucune | Oui | IMPORTANT | Actuelle |
| `experiment_campaign` orphelin (détaillé §5.2) | Traçabilité de la gouvernance de recherche | Aucune | Oui | IMPORTANT | Actuelle |
| Agrégation logique de `decision_gate` (2 arêtes FLOW entrantes — `verification` et `scientific_validation` — convergent sans nœud d'agrégation explicite) | Ambiguïté sur la sémantique AND/OR de la porte finale | `decision_gate` lui-même, implicitement | Discutable — les diagrammes de processus omettent couramment la logique booléenne exacte | AMÉLIORATION | Actuelle mais mineure |
| Pas de nœud générique de télémétrie *ingérée* (WRITE vers `observability`) distinct des arêtes OBSERVE (détaillé §3 point 5) | Nuance déjà traitée dans la correction du faux positif | `node_observability` existe, juste sans producteur explicite | Partiellement réelle | AMÉLIORATION | Actuelle |
| Absence de tout composant lié à la gouvernance de biais (« G-BIAS » / SOP 13, cf. `governance/` du runtime EBTA) | Élément normatif central du protocole EBTA réel | — | Volontairement hors scope | **PAS une anomalie** — cf. §7 ci-dessous | Domaine, pas générique |

---

## 7. Distinction architecture générique vs EBTA (point 11 de la mission)

Le diagramme est explicitement un modèle générique d'agent IA robuste (« ARCHITECTURE GÉNÉRALE D'UN AGENT IA ROBUSTE — PROCESS-FIRST », titre du calque légende) dont EBTA est un cas d'application limité à 6 nœuds du calque 07 (`data_lifecycle`, `data_reproducibility`, `research_space`, `experiment_campaign`, `backtest_engine`, `scientific_validation`). Je n'ai donc **pas** compté comme anomalie l'absence de composants spécifiquement EBTA comme le registre de biais append-only, le garde d'accès OOS, ou les gates PASS/FAIL/INCONCLUSIVE/BURNED du `bias_gate.py` — ce sont des détails d'implémentation du sous-domaine, hors du niveau d'abstraction visé ici. En revanche, les 6 nœuds EBTA *qui sont présents* devaient être correctement raccordés au reste du graphe — et deux ne le sont pas (§5.1, §5.2), ce qui reste dans le périmètre légitime de l'audit.

---

## 8. Points corrects — à ne pas modifier

- **Intégrité référentielle parfaite** : 0 arête cassée, 0 nœud orphelin, 0 ID dupliqué sur 71 nœuds + 107 arêtes.
- **Vocabulaire `relation_type`** 100 % conforme aux 9 valeurs autorisées.
- **Vocabulaire `robustness`** 100 % conforme aux 5 valeurs autorisées (hors les 2 attributions discutables du §5.6, qui sont des choix de contenu, pas des violations de format).
- **Aucun `layer_primary` vide ni égal à `layer_related`.**
- Les deux portes de décision (`decision_gate`, `ci_decision`) ont chacune leurs branches PASS et FAIL réellement câblées, avec convergence propre de la branche FAIL vers `repair_loop` depuis les deux portes.
- La boucle de réparation complète (FAIL → Error Evidence → Diagnostic → Root Cause → Correction → Re-Test → Verification) et son feedback vers `worker_agent` sont de vraies arêtes XML, exactement dans l'ordre attendu par la mission.
- Classification légitime confirmée pour `node_user`, `node_policy`, et pour l'ensemble des nœuds-outils (`tool_shell`, `tool_git`, `tool_search`, etc.) et `node_agent_specializations` comme puits « catalogue » légitimes.
- Séparation volontaire et documentée entre validation scientifique (L04) et tests logiciels (L08), portée par une annotation XML dédiée (`label_science_separation`) — bon réflexe de documentation intégrée au graphe.

---

## 9. Priorisation consolidée

L'humain a approuvé ces recommandations le 2026-08-19 (workflow léger, sans `/start` complet — cf. §11). Les items marqués **APPLIQUÉ** ont été édités directement dans `.ai/architecture/IA_Diagramme_architecture.drawio` le même jour ; intégrité re-vérifiée après coup (XML bien formé, 71 nœuds / 112 arêtes, 0 arête cassée, 0 orphelin, 0 `visible="0"`, vocabulaire `relation_type`/`robustness` 100 % conforme).

| Priorité | Item | Statut |
|---|---|---|
| **P1** | 5.1 — Relier `scientific_validation` à `backtest_engine` pour qu'elle valide un input réel | **APPLIQUÉ** — nouvelle arête `edge_scientific_validation_to_backtest_engine` (`RESULTS`, `relation_type="READ"`, `scientific_validation` source). Note méthodologique : par construction (cf. §2), cette arête ne change pas le degré entrant brut de `scientific_validation` (toujours 0 IN en comptage naïf de flèches) — c'est attendu, pas un signe d'échec de la correction ; ce qui compte est qu'une arête documente désormais explicitement sa dépendance de données. |
| **P1** | 5.4 — Retirer `visible="0"` sur `layer_feedback_recovery` et `layer_control_security` | **APPLIQUÉ** |
| **P1** (reclassé, oubli de la première passe) | 3 pt.1 — Relier `node_resume` à `node_checkpoint` (le bug le plus solide du contre-audit, confirmé sans nuance, avait été omis de cette table par erreur) | **APPLIQUÉ** — nouvelle arête `edge_resume_to_checkpoint` (`STATE`, `relation_type="READ"`, `resume` source) |
| **P2** | 3.6 — Ajouter une arête `WRITE` vers `node_memory` depuis un nœud producteur de leçons apprises | **APPLIQUÉ** — nouvelle arête `edge_correction_to_memory` (`LESSON`, `relation_type="WRITE"`, `correction` source) |
| **P2** | 5.2 — Relier `node_experiment_campaign` à `node_research_space` ou `node_backtest_engine` | **APPLIQUÉ** — nouvelle arête `edge_experiment_campaign_to_research_space` (`CONTROL`) |
| **P2** | 6 — Clarifier (note ou nœud d'agrégation) la sémantique des deux arêtes FLOW convergeant sur `decision_gate` | **NON APPLIQUÉ** — nécessite une décision humaine sur la logique AND/OR réelle, volontairement non tranchée unilatéralement |
| **P3** | 5.3 — Relier `data_lifecycle` → `data_reproducibility` | **NON APPLIQUÉ** — laissé pour un correctif ultérieur, discrétionnaire |
| **P3** | 5.5 — Ajouter `kind="RELATION"` à `edge_verification_to_artifact_validate` | **APPLIQUÉ** |
| **P3** | 5.6 — Revoir `robustness` de `node_pull_request` (et discuter celle de `node_context_loader`) | **NON APPLIQUÉ** — jugement de contenu, laissé à une décision humaine explicite |
| **P3** | 5.7 — Corriger le chemin de fichier cité en en-tête de l'audit initial | **NON APPLIQUÉ** — concerne un autre fichier (`architecture_anomalies_report.md`), hors mandat de cette correction |
| **P2** (issu du Conseil des 5, 2026-08-19) | `node_memory` n'était alimenté que sur le chemin FAIL (`correction --WRITE--> memory`) ; aucune écriture sur le chemin PASS, donc aucun succès ne génère de leçon apprise. Constat soulevé par le membre « Executor » lors de la délibération sur `node_evidence_store`, validé GO par l'humain. | **APPLIQUÉ** — nouvelle arête `edge_merge_to_memory` (`LESSON`, `relation_type="WRITE"`, `node_merge` source), symétrique de `edge_correction_to_memory` sur le chemin PASS. `node_evidence_store` lui-même reste **non modifié** (verdict NO-GO du Conseil des 5, cf. addendum §12). |

---

## 10. Verdict final

**ARCHITECTURE SAINE AVEC CORRECTIONS MINEURES.**

Le diagramme est structurellement solide : intégrité référentielle parfaite, vocabulaire contrôlé respecté à 100 %, processus principal et boucle de réparation complets et sans impasse. L'audit initial avait identifié la bonne zone de risque (nœuds mémoire/preuve/état mal raccordés) mais sa méthode de comptage brut des flèches, sans croiser `relation_type`, l'a conduit à se tromper de sens sur 3 de ses 4 diagnostics « bug de modélisation » (dont un renversement complet sur `node_memory`) et à mal classer la validation scientifique EBTA comme source légitime alors qu'elle est en réalité non alimentée — ce qui est, à mon sens, l'anomalie la plus importante du fichier au vu de la place centrale de la validation scientifique dans la hiérarchie d'autorité EBTA. L'anomalie la plus surprenante que mon audit indépendant a trouvée et que l'audit initial n'a pas cherchée du tout — le masquage par défaut des deux calques les plus critiques pour la sûreté (réparation, contrôle/sécurité) — est également corrigible en une ligne chacune.

---

## 11. Corrections appliquées (2026-08-19)

La mission initiale était read-only. L'humain a ensuite approuvé la recommandation de traiter les corrections P1/P2 comme un correctif ciblé documentaire (édition directe + checklist post-modification de `.ai/governance/AI_MODIFICATION_CHECKLIST.md`), sans le workflow complet `/start → /evaluate → /continue` — justifié par le fait que `.ai/architecture/IA_Diagramme_architecture.drawio` n'est ni `Protocole/` ni `Implementation/`, et que le changement est documentaire/organisationnel au sens de la checklist, pas normatif.

**Fichiers modifiés :**
- `.ai/architecture/IA_Diagramme_architecture.drawio` — 7 corrections appliquées au total (voir tableau §9, complété §12) : suppression de `visible="0"` sur 2 calques, ajout de 5 arêtes (`scientific_validation→backtest_engine`, `resume→checkpoint`, `correction→memory`, `experiment_campaign→research_space`, `merge→memory`), ajout de `kind="RELATION"` manquant sur 1 arête. Total : 71 nœuds (inchangé) / 112 arêtes (107 → 112, +5) / 9 calques (tous `visible` par défaut).
- `0 - HUMAN START HERE/architecture_contre_audit_report.md` (ce fichier) — mise à jour du statut des recommandations et ajout du compte rendu du Conseil des 5.

**Pourquoi chaque changement :** cf. le détail de chaque anomalie en §5 et §3 (point « checkpoint »), et §12 pour `merge→memory` — chaque arête ajoutée corrige une lacune de causalité vérifiée dans le XML (nœud sans producteur ou sans consommateur réel), pas une préférence esthétique.

**Fichiers volontairement non modifiés :** `Protocole/`, `Implementation/`, `.ai/checkpoint.json`, `0 - HUMAN START HERE/architecture_anomalies_report.md` (l'audit initial — laissé intact pour traçabilité historique, malgré les erreurs qu'il contient, cf. §3). `node_evidence_store` lui-même — non modifié, verdict NO-GO du Conseil des 5 (§12).

**Validation exécutée :** parsing XML (`xml.etree.ElementTree`, bien formé), recomptage programmatique des nœuds/arêtes/références (0 arête cassée, 0 nœud orphelin, 0 doublon d'ID), vérification du vocabulaire `relation_type` et `kind="RELATION"` sur les 112 arêtes, vérification `visible="0"` = 0 occurrence, exécutée après chaque lot d'éditions (y compris après la correction §12, appliquée en une seconde passe le même jour). Pas de validation applicable via `python -m json.tool` / `jsonschema` (fichier `.drawio`, pas `.json`) ; pas de suite de tests concernée (fichier hors `Implementation/ebta_engine/`).

**Décisions humaines encore nécessaires / items volontairement laissés ouverts :**
- 5.2/6 — la sémantique d'agrégation PASS/FAIL de `decision_gate` quand `verification` et `scientific_validation` convergent (AND/OR ?) reste à trancher par un humain.
- 5.3 — lien `data_lifecycle → data_reproducibility` (P3, discrétionnaire).
- 5.6 — les deux attributions de `robustness` discutables (`node_pull_request`, `node_context_loader`) sont un jugement de contenu, non appliqué.
- 5.7 — le chemin de fichier obsolète cité dans `architecture_anomalies_report.md` (fichier distinct, non touché).
- §12 — annotation optionnelle sur `node_evidence_store` (« lecture réservée à la gouvernance humaine, par design ») proposée par le Conseil des 5 mais non appliquée, en attente d'un GO séparé.
- Le routage visuel (waypoints) des 5 nouvelles arêtes est fonctionnellement correct mais approximatif ; une repasse manuelle dans draw.io pour affiner l'esthétique reste possible sans urgence.

---

## 12. Addendum — Conseil des 5 sur `node_evidence_store` (2026-08-19)

Question posée en suivi de ce contre-audit : `node_evidence_store` n'est plus diagnostiqué comme puits mort (il est déjà lu par `node_human_approval`), mais faut-il en plus qu'un agent IA le lise directement pour capitaliser sur l'historique d'exécution ?

**Verdict du Conseil des 5 : NO-GO** sur l'ajout d'une arête `agent → READ → evidence_store`. Convergence forte des cinq membres : même les deux avis favorables à une lecture agent rejettent explicitement `worker_agent` comme source et ne retiendraient au mieux que `context_loader`, à titre conditionnel et non retenu ici. Motifs principaux : (1) le nœud n'a jamais été un vrai défaut — la prémisse motivant la question était déjà fausse ; (2) le diagramme sépare déjà volontairement `node_memory` (connaissance curée) de `evidence_store` (preuves brutes), via une annotation explicite dans le label de `node_memory` ; (3) ouvrir la lecture directe des preuves brutes à un agent est une extension de capacité non demandée, contraire à la règle anti-sur-ingénierie du dépôt (`CLAUDE.md`) ; (4) dans un dépôt centré sur la gouvernance anti-biais, un agent lisant librement l'historique brut des résultats est lui-même un vecteur de biais potentiel. **`node_evidence_store` reste donc inchangé.**

En délibérant, le membre « Executor » a fait remonter un constat distinct et mieux fondé : `node_memory` n'était alimenté **que** sur le chemin FAIL (`correction --WRITE--> memory`), jamais sur le chemin PASS — aucun succès ne générait de leçon apprise. L'humain a validé un **GO** sur ce point précis. Correction appliquée : nouvelle arête `edge_merge_to_memory` (label « LESSON », `relation_type="WRITE"`, source `node_merge`), symétrique de `edge_correction_to_memory` sur le chemin de succès. `node_merge` a été choisi comme point d'écriture (plutôt que `review` ou `release`) car c'est le point d'intégration confirmée, structurellement analogue à `correction` (point de résolution) côté FAIL.

**Non appliqué, laissé en option :** une courte annotation sur `node_evidence_store` clarifiant son rôle de gouvernance humaine par design (miroir de l'annotation déjà présente sur `node_memory`), pour lever toute ambiguïté résiduelle sans toucher au graphe causal — proposée par le Conseil, non tranchée par l'humain à ce stade.
