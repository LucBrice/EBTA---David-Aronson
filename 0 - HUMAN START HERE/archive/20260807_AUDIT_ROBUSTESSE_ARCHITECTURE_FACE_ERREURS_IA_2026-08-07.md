# Audit — Robustesse de l'architecture face aux erreurs d'agents IA

Date : 7 août 2026
Statut : audit en 5 passes, convergé — puis corrigé par une boucle `/evaluate`
d'intake (2 passes, voir section « Boucle /evaluate d'intake ») déclenchée par
un `/start` humain du 2026-08-07.
Décision d'implémentation : aucune

## Pourquoi cet audit

Demande explicite de l'utilisateur : évaluer la probabilité, la sévérité et
la récurrence des erreurs qu'une IA peut commettre en exécutant des tâches
dans ce repo, et vérifier la capacité de l'architecture actuelle à les
prévenir ou à les détecter. Boucle demandée explicitement jusqu'à
convergence, plafonnée à 6 passes.

- **Passe 1** : documentation du cockpit IA (`AGENTS.md`,
  `.ai/checkpoint.json`, `.ai/governance/`, skills) + exécution de la suite
  de tests (219 tests, 1 erreur d'environnement).
- **Passe 2** : vérification des affirmations de la passe 1 contre le code
  et l'état réel du dépôt (hooks git, workflows, schémas). A corrigé une
  erreur de la passe 1 (un hook `pre-commit` est bien actif) et trouvé un
  vrai angle mort (preuves de workflow non vérifiées en contenu).
- **Passe 3** : lecture réelle du code des zones à risque identifiées
  (`governance/*.py`, `adapters/*.py`) au lieu de grep superficiel. N'a
  trouvé aucun `FALSE_SUCCESS`/`SILENT_FALLBACK` confirmé — les patterns
  `.get()`/`except Exception` repérés en passe 2 se sont révélés bien
  conçus (fail-closed, ou confinés à la frontière adaptateur).
- **Passe 4** : lecture du code de `.ai/tools/plan.ps1` (mécanique réelle de
  vérification des preuves) et mesure de la surface de code des zones
  sensibles (1970 lignes pour `governance/` + `validators/`). N'a fait que
  corroborer un constat déjà posé en passe 2, sans nouvel angle mort.

**Convergence** : deux passes consécutives (3 et 4) sans nouveau blind spot
majeur — arrêt à la passe 4 sur 6 autorisées.

## Constat général

Le repo est structurellement bien au-dessus de la moyenne pour contenir les
erreurs d'IA : hiérarchie d'autorité écrite (`Protocole/` > `Implementation/`
> `.ai/` > `.agents/`), validation multi-couches (schémas JSON stricts,
validators, manifestes SHA-256, logs append-only traités comme entrée non
fiable), 219 tests dont des fixtures volontairement invalides, et des skills
nés d'incidents réels (`bug-hunter`, `adversarial-tester`,
`plan-conformance-audit`, `EBTA_Protocol_Guardian`).

La faiblesse commune identifiée dans les deux passes n'est pas l'absence de
règles, mais leur caractère **procédural plutôt que mécanisé** : la
sécurité repose largement sur la discipline de l'IA exécutante à invoquer
les bons skills, pas sur un gate qui bloquerait physiquement une dérive.

## Points de rupture les plus probables

| Zone | Mécanisme de rupture typique |
|---|---|
| `governance/` (G-BIAS) | Confondre `INCONCLUSIVE` avec un `PASS` implicite, ou combler un champ manquant par une valeur par défaut plausible plutôt que de bloquer. |
| `adapters/` (backtrader, nautilus) | Importer les conventions de l'outil externe comme norme EBTA au lieu de les faire passer par la validation du cœur. |
| `procedures/` (wrc.py, oos_confidence_interval.py, ...) | Modifier un seuil ou une formule statistique sans décision normative enregistrée — changement de méthodologie déguisé en correctif technique. |
| `.ai/checkpoint.json` / `tracking.json` | Édition manuelle incohérente avec l'état réel du repo — déjà survenu par le passé (plusieurs entrées de correction rétroactive dans l'historique du checkpoint). |
| Preuves de workflow (`plan.ps1`, `workflow_state.ps1`) | Le backend vérifie qu'un ID de preuve existe, jamais que son contenu est vrai (limite documentée dans `.ai/workflows/README.md`). Une IA peut satisfaire formellement le gate sans preuve réelle. |
| Frontière `Implementation/` vs `Protocole/` | Réinterpréter silencieusement le protocole au lieu de traiter une divergence comme un bug runtime — inversion de la hiérarchie d'autorité. |

## Ce qui est mécanisé aujourd'hui (vérifié, pas supposé)

- Un hook git `pre-commit` réel est installé et actif (pas de
  `core.hooksPath` de redirection). Il bloque un commit touchant les
  fichiers du cockpit IA si `checkpoint.json.updated_at` est antérieur à la
  date du dernier commit. Portée étroite : vérifie la fraîcheur, jamais le
  contenu, les schémas, les tests ou Pyrefly. Contournable par
  `git commit --no-verify`.
- 12 schémas JSON avec `additionalProperties` (35 occurrences) — plutôt
  stricts, pas de sac fourre-tout.
- Aucune CI (pas de `.github/workflows`) : validation JSON schema, suite de
  tests et Pyrefly restent des commandes manuelles listées dans `CLAUDE.md`,
  pas automatisées à chaque changement.

## Ce qui reste procédural (non mécanisé)

- `adversarial-tester` — le skill qui chasse les faux succès et replis
  silencieux — est documenté comme non vérifié par `plan.ps1 close`. Rien
  n'empêche mécaniquement une IA de sauter cette étape.
- La preuve de workflow (`-IntakeAuditEvidence`, `-PlanAuditEvidence` dans
  `.ai/tools/plan.ps1`) n'est vérifiée que par
  `[string]::IsNullOrWhiteSpace` — confirmé en lisant le code (passe 4) :
  n'importe quelle chaîne non vide satisfait le gate, son contenu n'est
  jamais recoupé avec un fichier ou un événement réel.
- `bug-hunter` (Pyrefly) n'est invoqué que par discipline, pas en gate
  automatique avant un commit ou une clôture de chantier.

## Ce qui a été vérifié et confirmé sain (passe 3)

- `governance/bias_gate.py`, `oos_access_guard.py`,
  `preregistration_checker.py` : chaque valeur absente lue via `.get()` est
  traitée comme un signal de blocage explicite (`missing.append(...)`,
  statut `BURNED`/`FAIL`), jamais comme un défaut positif implicite. Pattern
  fail-closed conforme à la doctrine `adversarial-tester`.
- `except Exception` n'apparaît que dans **2 fichiers sur 122** dans tout
  `Implementation/ebta_engine/`, tous deux dans `adapters/` (la frontière
  externe non fiable, où ce pattern est explicitement autorisé par le
  contrat d'adaptateur). La majorité des cas relancent en `RuntimeError`
  explicite ; les deux qui avalent l'exception (`_is_flat`,
  `_is_missing_report_value` dans `nautilus_mapping.py`) le font vers la
  branche de calcul la plus prudente, pas vers un raccourci de succès —
  aucun `FALSE_SUCCESS` confirmé.
- Surface de code des zones sensibles : `governance/` + `validators/` =
  1970 lignes seulement — surface modeste, raisonnablement auditable dans
  son ensemble par un futur passage `adversarial-tester` outillé.

## Passe 5 (ciblée) — risque prioritaire de l'utilisateur : l'agent de codage

L'utilisateur a précisé après la passe 4 que l'enjeu qu'il veut mitiger en
priorité n'est pas l'erreur méthodologique/statistique, mais l'erreur d'un
**agent de codage qui implémente** dans `Implementation/`. Une passe unique,
ciblée sur ce point, a suffi à trouver le mécanisme exact et sa faille
précise (convergence immédiate, pas besoin de boucler davantage sur cette
sous-question) :

- Le workflow `core-engine` (`.ai/workflows/core-engine/WORKFLOW.json:30`)
  **exige déjà**, textuellement, les trois preuves `bug_hunter`,
  `adversarial_tester`, `plan_conformance` avant la transition `ready` qui
  précède `/close`. Le design est correct : ce n'est pas un gate manquant.
- Mais `Add-WorkflowEvidence` dans `.ai/tools/workflow_state.ps1` (ligne
  ~128) ne valide que le format de l'ID (`^[a-z][a-z0-9_]*$`) et que la
  référence n'est pas vide. Rien ne vérifie que la référence pointe vers un
  artefact de preuve réel. `bug_hunter=ok, tout est passé` satisferait
  mécaniquement le gate.
- **Conclusion pour l'enjeu agent de codage** : le point de défaillance
  n'est pas "il manque un gate", c'est "le gate existe, au bon endroit,
  mais ne vérifie que la forme, jamais la substance". C'est le point de
  levier le plus direct et le moins coûteux à corriger, parce qu'il réutilise
  un mécanisme déjà en place au lieu d'en créer un nouveau.

## Recommandations (à trier / prioriser par l'humain)

1. **Priorité — substantifier la preuve `ready` du workflow `core-engine`** :
   modifier `Add-WorkflowEvidence` dans `.ai/tools/workflow_state.ps1` pour
   que, au minimum pour les IDs `bug_hunter`, `adversarial_tester`,
   `plan_conformance`, la référence doive pointer vers un artefact de preuve
   réel plutôt qu'accepter n'importe quelle chaîne non vide. Corrige
   directement le risque prioritaire de l'utilisateur (agent de codage) sans
   ajouter de nouveau mécanisme.

   Contraintes découvertes par la boucle `/evaluate` d'intake — un
   `Test-Path` naïf est **incorrect** en l'état :

   - les références réelles déjà enregistrées ne sont pas des chemins nus
     mais des chemins avec ancre Markdown
     (`.ai/archive/20260731_PLAN_CORRECTION_MANIFESTE_FREEZE_SOP06.md#resultat-dexecution-...`,
     `.ai/checkpoint.json` ligne 1580) ; il faut découper sur `#` avant de
     tester l'existence, et idéalement vérifier que l'ancre existe
     réellement dans le fichier ;
   - `baseline_commit` porte un SHA (`a4ce82d`) et `legacy_import` une
     phrase libre : la validation doit être **ciblée par ID**, jamais
     globale ;
   - la validation doit rester **à l'écriture** (`Add-WorkflowEvidence`),
     pas dans `Assert-WorkflowState` qui relit l'historique déjà
     enregistré, sous peine de rendre invalides rétroactivement des
     workstreams archivés ;
   - `.ai/tools/tests/test_workflow_state_machine.ps1` doit rester `PASS`.

   **Honnêteté du gain** : l'existence d'un fichier ne prouve pas son
   contenu. Ce durcissement élève le coût de la fraude (il faut produire un
   artefact) sans la rendre impossible. Le présenter comme « la preuve est
   désormais substantifiée » recréerait exactement le pattern *faux succès*
   que ce dépôt combat. Un gain réel supplémentaire suppose d'exiger du
   rapport un verdict lisible par machine et un recoupement avec le diff du
   chantier — à trancher par l'humain, pas à supposer.
2. Étendre le hook `pre-commit` existant (déjà actif) pour, au minimum,
   valider aussi le schéma JSON de `checkpoint.json`/`tracking.json` avant
   tout commit qui les touche — réutilise un mécanisme déjà en place. Une
   variante plus ambitieuse consisterait à lancer Pyrefly ciblé sur les
   fichiers `Implementation/` stagés, mais la suite complète (79 s) est
   probablement trop lente pour un hook `pre-commit` — à réserver, le cas
   échéant, à un hook `pre-push`.

   Précisions de la boucle `/evaluate` d'intake : le hook n'est pas un
   fichier orphelin hors git — sa source versionnée est
   `Implementation/Active/pre_commit_hook.py` (installée via
   `Implementation/Active/INSTALL_GIT_HOOK.md`), et `diff` confirme que la
   copie installée dans `.git/hooks/pre-commit` lui est aujourd'hui
   **identique**. Toute modification doit donc porter sur la source
   versionnée puis être réinstallée. Angle mort résiduel : rien ne détecte
   un drift futur entre la source versionnée et la copie installée, et le
   hook ne se déclenche que si un fichier du cockpit IA est *staged* — un
   commit purement `Implementation/` ne l'active pas, donc cette
   recommandation ne couvre pas le risque prioritaire « agent de codage ».
3. Ajouter une garde d'environnement minimale dans
   `Implementation/ebta_engine/benchmarks/long_data.py:487` — point de
   rupture mineur trouvé pendant l'audit, correction triviale.

   Cause racine prouvée (exécution du 2026-08-07 pendant la boucle
   `/evaluate` d'intake, et non plus supposée) : `219 tests, 1 error`.
   `test_long_data_benchmark.py:105` appelle `run_benchmark`, qui appelle
   `long_data.py:138 -> _environment_report() -> long_data.py:487`, où
   `importlib.metadata.version("nautilus_trader")` lève
   `PackageNotFoundError` hors du venv Nautilus. L'échec est bien à
   l'exécution du test, pas à l'import du module — la garde doit donc
   porter sur cet appel précis, en enregistrant une valeur explicite du
   type `null`/`"NOT_INSTALLED"` dans le rapport plutôt qu'en masquant
   l'absence.
4. Un passage `adversarial-tester` outillé (pas une lecture d'audit) sur
   `governance/*.py` (bias_gate.py, oos_access_guard.py,
   preregistration_checker.py — tous utilisent `.get()`/`except Exception`)
   pour confirmer qu'aucun repli silencieux n'y est déjà présent.
5. Isoler les tests dépendant de l'environnement Nautilus dans un groupe
   distinct de la suite stdlib-only, pour qu'un échec d'environnement ne se
   noie pas dans le même run qu'un échec de logique métier.

   Impact non mentionné à l'origine, relevé par la boucle `/evaluate`
   d'intake : la commande de découverte
   `python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation`
   est la commande de référence citée dans `CLAUDE.md` et enregistrée dans
   `.ai/checkpoint.json::validation.commands`. Toute segmentation de la
   suite oblige à mettre à jour ces deux références de façon cohérente,
   sous peine de créer une commande canonique qui ne correspond plus à ce
   qui est réellement exécuté.

## Boucle `/evaluate` d'intake (2026-08-07, `/start` humain)

Cette section n'est pas une passe d'audit de robustesse supplémentaire :
c'est le journal de la boucle `code-architecture-evaluator` exigée par
`.ai/workflows/common/WORKFLOW.md` avant toute promotion via `/start`. Elle
audite **ce document en tant que brouillon routable**, pas l'architecture du
dépôt.

### Passe 1 — confrontation des affirmations au code réel

Toutes les affirmations factuelles du document ont été revérifiées
indépendamment et sont **confirmées** : `workflow_state.ps1:128-133` et
`:174`, `core-engine/WORKFLOW.json:30`, hook `pre-commit` installé sans
`core.hooksPath`, absence de `.github/`, et `long_data.py:487`
(219 tests / 1 erreur reproduite). Angles morts trouvés, tous corrigés
ci-dessus dans les recommandations 1, 2, 3 et 5, plus :

- **Multi-lot non déclaré.** Le test de détection de
  `.agents/skills/epic-orchestrator/SKILL.md` est **satisfait** : les cinq
  recommandations ont chacune un Exit criteria vérifiable indépendamment,
  peuvent être routées dans un ordre différent, et un blocage sur l'une
  n'empêche pas les autres d'avancer. Ce document doit donc être promu
  comme **chantier mère coordonnant cinq lots**, jamais comme un plan
  d'implémentation unique.
- **Aucun Exit criteria binaire.** Aucune recommandation n'énonce de
  condition observable de fin ; `plan.ps1 start` refuserait le plan.
- **Auto-référence.** Le chantier qui durcit le gate `ready` sera lui-même
  clos *par* ce gate. À trancher explicitement avant implémentation.
- **Verrou de gouvernance non évalué.** Les recommandations 3 et 5 touchent
  `Implementation/`, que `.ai/governance/AI_MODIFICATION_CHECKLIST.md`
  protège d'une modification sans décision humaine explicite.

### Passe 2 — angles morts nouveaux (non convergée)

- **Portée réelle du risque de régression, affinée.** La lecture de
  `.ai/tools/plan.ps1` montre que `Assert-WorkflowState` n'est appliqué à
  **tous** les workstreams que dans la branche `migrate-workflows`
  (`plan.ps1:502-515`), administrative et one-shot ; les autres actions ne
  valident que le workstream ciblé via `Move-WorkflowStage`. Le risque de
  casser rétroactivement les 40+ workstreams archivés est donc **réel mais
  confiné à `migrate-workflows`** — ce qui renforce, sans la contredire, la
  contrainte « valider à l'écriture seulement » de la recommandation 1.
- **Le workflow n'est pas un choix libre — il est dérivé mécaniquement.**
  `common/WORKFLOW.json:30` n'exige que `plan_conformance` à `ready`, alors
  que `core-engine/WORKFLOW.json:30` exige les trois preuves. Le risque
  apparent (router le lot 1 sous `common` pour le soustraire au gate qu'il
  durcit) est en réalité **fermé mécaniquement** :
  `workflow_state.ps1::Get-LegacyWorkflowId:184` impose `core-engine` dès
  que la classification est `IMPLEMENTATION_DETAIL`, `CONTRACT_ENCODING`,
  `TEST_FIXTURE` ou `ADAPTER_MAPPING`, et `plan.ps1:283` refuse tout
  workflow qui ne correspond pas à la classification déclarée. Le lot 1
  modifie du code d'outillage (`.ai/tools/workflow_state.ps1`) : classé
  `IMPLEMENTATION_DETAIL`, il sera donc soumis aux trois preuves — y
  compris celle qu'il vient lui-même de durcir. L'auto-référence relevée en
  passe 1 se résout ainsi sans arbitrage humain.
- **Ordre des lots contraint par une dépendance de contrat.** Le lot 4
  (passage `adversarial-tester` outillé) *produit* un rapport ; le lot 1
  *définit* ce qui constitue une preuve recevable. Exécuter le lot 4 avant
  le lot 1 produirait un rapport à refaire. Ordre retenu : lot 1 d'abord
  (il fixe le contrat), lot 4 ensuite comme premier producteur soumis à ce
  contrat — donc test grandeur nature du correctif.
- **Effet de bord du hook sur le lot 1.** `Implementation/Active/pre_commit_hook.py:20`
  place `.ai/tools/` dans `RELAY_PREFIXES` : tout commit du lot 1 déclenche
  le contrôle de fraîcheur et sera **bloqué** si `checkpoint.updated_at` est
  antérieur à la date du dernier commit. Contrainte opérationnelle bénigne
  mais à connaître avant de committer.

### Passe 3 — convergence (deux points mineurs, aucun angle mort majeur)

Le périmètre des cinq lots est stable, aucune affirmation n'est infirmée et
aucune recommandation structurante nouvelle n'apparaît. Deux points mineurs,
consignés pour ne pas être perdus, sans rouvrir la boucle :

- **Écart entre un constat et les recommandations.** Le document constate
  « Aucune CI (pas de `.github/workflows`) » mais aucune des cinq
  recommandations n'y répond. Ce n'est pas nécessairement une omission —
  introduire une CI est une décision d'outillage qui appartient à l'humain,
  pas à l'IA. À poser comme **question ouverte** au triage humain, pas à
  transformer d'office en sixième lot.
- **Le skill producteur de cet audit n'est pas versionné.**
  `.agents/skills/robustness-audit-coding-agent/SKILL.md` existe et est
  fonctionnel, mais `git status` le donne encore non suivi (`??`). Il
  documente la procédure de ré-audit qui servira à vérifier que le lot 1
  ferme réellement le gate. Le committer relève de la baseline de ce
  chantier, pas d'un lot d'implémentation.

Boucle arrêtée à 3 passes sur 6 autorisées, conformément à
`.ai/workflows/common/WORKFLOW.md`.

## Non-goals de cet audit

- Aucune modification de `Protocole/`, `Implementation/` ou `.ai/` n'a été
  faite.
- Aucun `adversarial-tester` outillé n'a été exécuté (recommandation 4
  ci-dessus le propose comme suite, pas comme fait accompli).
- Ce document ne tranche aucune priorité ; il liste des constats et des
  pistes pour triage humain.

## Source

Conversation Claude Code du 2026-08-07, audit en 5 passes sur demande
explicite de l'utilisateur (4 passes générales convergées, 1 passe ciblée
sur le risque prioritaire agent de codage, convergée en une seule passe).
