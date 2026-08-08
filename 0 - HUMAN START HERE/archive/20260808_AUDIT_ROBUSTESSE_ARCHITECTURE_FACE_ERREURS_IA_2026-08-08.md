# Audit — Suivi post-renforcement (chantier `EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE`)

Date : 8 août 2026
Statut : trois passes de re-vérification directe (code + comportement
observé), convergées sur deux sessions distinctes du même jour — aucun angle
mort majeur non déjà consigné, à l'exception du point structurel « CI sans
branch protection » ajouté par la Partie C. Complète, en fin de journée, la
passe ciblée initiale sur le lot 1 (Partie A) par un balayage des six lots +
l'extension `pre-push` (Partie B), puis par une contre-vérification
indépendante produite dans une session séparée sans connaissance préalable
des Parties A/B (Partie C).
Décision d'implémentation : aucune — audit seul, conformément au skill
`robustness-audit-coding-agent`

## Partie A — Passe ciblée initiale : le lot 1 ferme-t-il le gate `ready` ?
Source : re-vérification demandée explicitement par l'utilisateur, du
correctif listé dans `LISTE_COMMITS_SESSION_2026-08-08.md` (chantier
`EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE`, lot 1) contre le point trouvé par
`archive/20260807_AUDIT_ROBUSTESSE_ARCHITECTURE_FACE_ERREURS_IA_2026-08-07.md`

## Question posée

L'audit du 2026-08-07 (recommandation 1, priorité) avait localisé le point de
défaillance suivant, pour le risque prioritaire « agent de codage qui
implémente dans `Implementation/` » :

> `Add-WorkflowEvidence` dans `.ai/tools/workflow_state.ps1` (ligne ~128) ne
> valide que le format de l'ID et que la référence n'est pas vide. Rien ne
> vérifie que la référence pointe vers un artefact de preuve réel.
> `bug_hunter=ok, tout est passé` satisferait mécaniquement le gate `ready`
> du workflow `core-engine`.

Question de cette passe : le lot 1 (commits `97512ce`, `96de940`, `903baa0`,
`2a29ccd`) ferme-t-il réellement ce point, sans en rouvrir un nouveau ?

## Vérification directe (code lu, pas la doc ni le message de commit)

1. **`Get-SubstantiatedEvidenceIds`** (`workflow_state.ps1:120-133`) — retourne
   exactement `bug_hunter`, `adversarial_tester`, `plan_conformance`. Confirmé
   identique à `required_evidence` de la transition `ready` du contrat
   `core-engine/WORKFLOW.json:30`. `baseline_commit` et `legacy_import` en
   sont exclus, conforme à la contrainte de l'audit fondateur (formats SHA /
   texte libre, pas des chemins de fichier).
2. **`Test-EvidenceReferenceSubstance`** (`workflow_state.ps1:150-209`) —
   découpe `chemin#ancre` sur le premier `#`, rejette une racine absolue ou
   une traversée `..`, exige `Test-Path -PathType Leaf` sur le chemin
   relatif au dépôt, et si une ancre est fournie, vérifie qu'elle correspond
   à un titre Markdown réel du fichier (best-effort documenté, caveat
   explicite sur la translittération). Un `#` suivi de rien est rejeté
   explicitement (pas de repli silencieux vers « pas d'ancre »).
3. **`Add-WorkflowEvidence`** (`workflow_state.ps1:211-241`) — pour les IDs
   substantifiés, exige `-RepoRoot` (sinon `throw` explicite, fail-closed) et
   appelle `Test-EvidenceReferenceSubstance` avant d'enregistrer l'entrée.
   La validation reste bien **à l'écriture**, `Assert-WorkflowState`
   (:82-107) n'a pas été touché — donc aucun workstream archivé n'est
   revalidé rétroactivement, conforme à la contrainte de l'audit fondateur.
4. **Points d'appel réels** (`plan.ps1`) — `grep` confirme que les trois
   appels à `Add-WorkflowEvidence`/`Add-WorkflowEvidenceArguments` touchant
   des IDs substantifiés (`ready`, ligne 437 ; `baseline`, ligne 389-390 ;
   `start`, ligne 287) passent systématiquement `-RepoRoot $repoRoot`. Le
   `throw` fail-closed pour `RepoRoot` manquant n'est donc jamais atteint en
   usage réel — vérifié par lecture, pas supposé.

## Comportement réel observé (pas seulement lu)

Exécution de `.ai/tools/tests/test_workflow_state_machine.ps1` depuis la
racine du dépôt EBTA :

```
workflow_state_machine=PASS
```

Le test contient une **preuve négative explicite** (lignes 54-82) qui répète
exactement le scénario du point de rupture trouvé le 2026-08-07 :
`Add-WorkflowEvidence -Id bug_hunter -Reference "chaine_arbitraire_sans_artefact"`
lève désormais une erreur (`Assert-Throws`), alors que le commentaire du test
indique explicitement : « ce cas doit échouer sur le code antérieur au lot,
et réussir après ». Couvre aussi : ancre Markdown inexistante, `#` sans
ancre, ID non substantifié non affecté (`intake_audit` toujours accepté sans
`-RepoRoot`), et un scénario d'intégration bout-en-bout via `plan.ps1 ready`
qui rejette `plan_conformance=test:report` puis accepte une référence réelle
vers `PLAN_TEST.md`.

`git status --porcelain` après exécution : aucune modification résiduelle
imputable au test (fichiers `.mmd` régénérés à l'identique, dépôt temporaire
d'intégration auto-nettoyé). Les seules entrées modifiées/non suivies
présentes préexistaient à cette vérification.

## Verdict

**Le point trouvé par l'audit du 2026-08-07 est fermé.** Le gate `ready` du
workflow `core-engine` n'accepte plus une preuve `bug_hunter` /
`adversarial_tester` / `plan_conformance` non substantifiée — vérifié par
lecture du code d'application ligne par ligne et par exécution réelle d'un
test qui reproduit littéralement le scénario de contournement décrit dans
l'audit fondateur.

## Nouveau gate ouvert ? Résidu déjà consigné, pas un angle mort caché

Aucun nouveau point de rupture non anticipé n'a été trouvé. Un résidu
existe, mais il était **déjà nommé et accepté comme tel** par l'audit
fondateur (section « Honnêteté du gain ») : la vérification prouve
l'**existence** d'un fichier, jamais son **contenu**. Un agent de codage
pourrait toujours faire pointer `bug_hunter` vers un fichier réel mais non
pertinent (ex. `README.md`) et satisfaire mécaniquement le gate. Ce n'est pas
une régression introduite par le lot 1 : c'est le même résidu que l'audit du
2026-08-07 avait explicitement laissé au tri humain (« Un gain réel
supplémentaire suppose d'exiger du rapport un verdict lisible par machine et
un recoupement avec le diff du chantier — à trancher par l'humain, pas à
supposer »). Le coût de la fraude a augmenté (produire un artefact réel),
il n'a pas été rendu nul — cette nuance doit être conservée telle quelle,
pas arrondie en « le risque est éliminé ».

## Ce qui est mécanisé et vérifié vs ce qui reste procédural

- **Mécanisé et vérifié directement** (confiance haute sur ce point précis) :
  existence de fichier + ancre Markdown pour les 3 IDs substantifiés, à
  l'écriture, avec test de non-régression exécuté et passant.
- **Reste procédural** (hors périmètre de ce lot, déjà consigné) :
  substance sémantique du contenu de l'artefact référencé ; recoupement
  automatique preuve ↔ diff du chantier ; invocation effective des skills
  `bug-hunter`/`adversarial-tester` reste une question de discipline, pas de
  gate mécanique supplémentaire.

## Non-goals de cette passe

Aucune modification de `Protocole/`, `Implementation/` ou `.ai/` n'a été
faite. Aucune ré-exécution du reste de la boucle 6-passes de l'audit
fondateur : question ciblée unique, conformément à la clause « passe ciblée »
du skill `robustness-audit-coding-agent`.

## Niveau de confiance

- **Sur ce qui a été vérifié directement** (fermeture du point précis
  identifié le 2026-08-07) : haute — code lu ligne par ligne, contrat JSON
  recoupé, points d'appel réels vérifiés par grep, test exécuté avec
  résultat `PASS` observé, `git status` vérifié après exécution.
- **Sur l'exhaustivité de la couverture** : limitée à cette question précise.
  N'a pas ré-audité les lots 2 à 6 ni relu l'intégralité de `plan.ps1`
  au-delà des points d'appel de `Add-WorkflowEvidence`.

---

## Partie B — Où en est le dépôt après les six lots + l'extension `pre-push` ?

Question posée par l'utilisateur en fin de journée : après tout ce travail de
renforcement (`EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE`, six lots, plus
l'extension `pre-push` à la synchronisation git listée dans
`LISTE_COMMITS_SESSION_2026-08-08.md`), où en est réellement la robustesse du
dépôt ? Deux passes de vérification directe, convergées.

### Passe 1 — état machine, suite de tests, document de clôture

- `.ai/checkpoint.json` : les six workstreams de lots + le chantier mère sont
  tous `status: DONE` (`PLAN_ISOLATION_TESTS_DEPENDANTS_NAUTILUS` en
  `lifecycle: REJECTED`, conforme à la décision humaine journalisée), plus
  `PLAN_EXTENSION_PRE_PUSH_SYNC_GIT_TOUTES_IA` en `DONE` — vérifié par lecture
  machine du fichier, pas par le récit du document de clôture.
- Suite de tests complète exécutée depuis la racine du dépôt :
  **`Ran 242 tests ... OK`** (0 échec, 0 erreur), contre `219 tests, 1 error`
  au moment de l'audit du 07/08. Les 23 tests supplémentaires correspondent
  aux preuves négatives ajoutées par les lots 1, 2, 4 et 6 (doctrine
  `adversarial-tester` : exiger l'échec au point d'entrée), pas à une dérive
  silencieuse de périmètre.
- Le document de clôture (`.ai/archive/20260808_EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE.md`)
  est lui-même rédigé au niveau d'exigence attendu : décisions humaines
  journalisées avant action, honnêteté explicite sur la portée du lot 1
  (« durcir la forme d'une preuve n'est pas prouver son contenu »), refus du
  lot 5 motivé par une vérification factuelle et non par confort.

### Passe 2 — vérification directe du code, pas du récit de clôture

| Lot | Mécanisme | Vérifié comment | Résultat |
| --- | --- | --- | --- |
| 1 | Substantiation des preuves `ready` | Code lu ligne par ligne + test exécuté (voir Partie A) | Confirmé fermé |
| 2 | `pre-commit` (staleness + schéma JSON) et `pre-push` (suite complète + anti-non-fast-forward) | Lecture intégrale des deux hooks (`Implementation/Active/pre_commit_hook.py`, `pre_push_hook.py`) ; `git diff --no-index` entre source versionnée et copie installée dans `.git/hooks/` ; `git config core.hooksPath` vide (pas de redirection silencieuse) | Sources et copies installées identiques ; aucune redirection ; downgrade `jsonschema` absent annoncé explicitement, jamais silencieux |
| 3 | Garde d'environnement `long_data.py:487` | Lecture du code : `except` ciblé sur `PackageNotFoundError` uniquement, sentinelle `"NOT_INSTALLED"` explicite | Confirmé — plus aucune erreur d'environnement dans la suite (242 tests OK) |
| 4 | Correction du repli silencieux `incident_logger.py` | Lecture du code : `load_incidents` lève désormais `IncidentLogNotFound` (sous-classe de `FileNotFoundError`) au lieu de renvoyer `[]` sur un log absent, avec docstring expliquant explicitement le risque évité | Confirmé — fail-closed, plus de confusion "aucun incident" / "log introuvable" |
| 6 | CI GitHub indépendante | Lecture de `.github/workflows/ebta-runtime-suite.yml` (suite unittest + validation schéma des deux JSON d'état) ; **vérification indépendante via `gh run view`** des deux runs cités par le document de clôture | Run `31247122326` confirmé **réellement rouge** (`Run the canonical EBTA runtime test suite` en échec, `exit code 1`) ; run `31247299075` confirmé **réellement vert** après revert. Preuve d'indépendance non fabriquée. |
| Extension `pre-push` sync git | `check_non_fastforward` (hard-block) et `warn_if_behind_origin_main` (avertissement non bloquant, jamais de faux "à jour" silencieux sur échec de `fetch`/`rev-list`) | Lecture du code : les trois issues (à jour / en retard / vérification impossible) sont distinguées explicitement, aucun repli vers "silencieux = OK" | Confirmé fail-closed sur l'incertitude |

Mesures complémentaires (méthode de calibrage du skill) :

- `except Exception` dans tout `Implementation/ebta_engine/` **hors `adapters/`** : **0 occurrence** (contre 0 dans `governance/`/`validators/` et 2 confinées à `adapters/` lors de l'audit du 07/08 — situation stable, toujours confinée à la frontière externe).
- `additionalProperties` dans les schémas JSON : 58 occurrences (vs 35 le 07/08) — la rigueur de schéma n'a pas régressé, elle s'est étendue (nouveaux schémas `checkpoint.schema.json`/`tracking.schema.json` désormais validés en CI).
- `governance/` + `validators/` : 1713 lignes — surface toujours modeste, auditable dans son ensemble.

### Ce qui a changé, concrètement, par rapport au 7 août

| Avant (07/08) | Après (08/08, vérifié) |
| --- | --- |
| `bug_hunter=ok` (chaîne arbitraire) satisfaisait le gate `ready` | Doit pointer vers un fichier réel du dépôt (existence vérifiée, ancre Markdown vérifiée si fournie) |
| `pre-commit` seul, ne se déclenche que si un fichier du cockpit IA est staged — un commit pur `Implementation/` y échappe | `pre-push` s'exécute sur **tout** push, quels que soient les fichiers modifiés — comble exactement ce trou |
| Aucune CI — la seule preuve d'exécution des tests était auto-rapportée par l'agent, sur sa propre machine | CI GitHub réelle, vérifiée indépendamment par cette passe comme ayant produit un vrai rouge puis un vrai vert |
| `incident_logger.load_incidents` sur un chemin absent : repli silencieux vers `[]` (« aucun incident » indistinct de « log introuvable ») | Lève `IncidentLogNotFound` explicitement |
| `219 tests, 1 error` (erreur d'environnement Nautilus non gardée) | `242 tests, OK` |

### Ce qui reste procédural — inchangé, et à ne pas présenter comme résolu

- **`bug-hunter` (Pyrefly)** n'est toujours exécuté que par discipline : ni la
  CI ni aucun hook local ne le lance automatiquement. Le lot 1 exige
  désormais qu'un rapport existe quelque part, mais rien ne vérifie que ce
  rapport provient d'une exécution réelle de Pyrefly plutôt que d'un fichier
  rédigé à la main.
- **Substance sémantique des preuves `bug_hunter`/`adversarial_tester`/`plan_conformance`** :
  la preuve d'existence de fichier (lot 1) n'est pas une preuve de contenu —
  limite assumée explicitement par le chantier lui-même (invariant 5 de son
  propre plan), pas une découverte de cette passe.
- **`--no-verify` local** contourne toujours `pre-commit` et `pre-push` sans
  laisser de trace locale — c'est précisément la raison d'être du lot 6 (CI),
  qui ne prévient pas mais ne peut pas être sauté silencieusement.

### Verdict global

Les cinq points de rupture les plus probables identifiés le 7 août sont
**tous couverts par un mécanisme aujourd'hui vérifié en code et, pour la CI,
en comportement observé indépendamment** — à l'exception du point
méthodologique/statistique (hors périmètre de ce skill) et de la substance
sémantique des rapports de preuve, explicitement laissée au tri humain par le
chantier lui-même. Rien dans cette passe n'a trouvé de nouveau gate ouvert
par inadvertance ; la seule chose qui a changé par rapport aux intentions du
chantier est le compte de tests littéral (219 → 232 → 242), écart de
rédaction déjà assumé et documenté dans le plan de clôture.

### Niveau de confiance (Partie B)

- **Sur ce qui a été vérifié directement** : haute — code des cinq
  mécanismes lu ligne par ligne, suite de tests exécutée avec résultat
  observé, deux runs CI vérifiés indépendamment via `gh run view` (source
  externe à ce dépôt, pas le récit du document de clôture).
- **Sur l'exhaustivité de la couverture** : modérée — n'a pas ré-exécuté
  `adversarial-tester` de façon outillée sur `governance/` (le lot 4 l'a
  fait ; cette passe s'est appuyée sur son rapport et sur une mesure
  indépendante de `except Exception`, pas sur une ré-exécution complète du
  skill) et n'a pas relu `plan.ps1` dans son intégralité au-delà des points
  déjà couverts par la Partie A.

---

## Partie C — Contre-vérification indépendante à froid (nouvelle session, 2026-08-08)

Demande utilisateur, dans une conversation distincte des Parties A/B et sans
avoir lu ce document au préalable : « refaire un audit à froid comme à
l'époque du 1er audit », pour mesurer la robustesse actuelle. Cette partie a
été produite en relisant le code par elle-même (hooks, `workflow_state.ps1`,
`incident_logger.py`, `long_data.py`, `ebta-runtime-suite.yml`) avant de
découvrir que les Parties A et B existaient déjà pour la même date. Elle sert
de **contre-preuve indépendante** (deux passes produites séparément
convergent-elles ?) plutôt que de répétition.

### Corroboration indépendante des Parties A et B

Vérifiés à nouveau, séparément, avec le même résultat :

- `Get-SubstantiatedEvidenceIds` / `Test-EvidenceReferenceSubstance` /
  `Add-WorkflowEvidence` (`workflow_state.ps1:120-241`) : mêmes lignes, même
  lecture — fail-closed, existence de fichier + ancre Markdown exigées pour
  `bug_hunter`/`adversarial_tester`/`plan_conformance`, jamais de repli
  silencieux.
- `.ai/tools/tests/test_workflow_state_machine.ps1` exécuté indépendamment
  depuis cette session : `workflow_state_machine=PASS`.
- `Implementation/Active/pre_commit_hook.py` et `pre_push_hook.py` lus
  intégralement ; `diff` entre source versionnée et `.git/hooks/` installés :
  identiques, aucune dérive.
- `incident_logger.py::IncidentLogNotFound` : confirmé fail-closed par
  lecture du diff du commit `8eaae06`.
- `long_data.py:495-507` : `except` ciblé sur
  `importlib.metadata.PackageNotFoundError` uniquement, sentinelle
  `"NOT_INSTALLED"` explicite.
- Suite de tests complète, exécutée depuis cette session, indépendamment :
  **`Ran 242 tests in 58.453s` / `OK`**, exit code 0 — même chiffre que la
  Partie B.
- `.github/workflows/ebta-runtime-suite.yml` lu intégralement : suite
  unittest + validation schéma des deux JSON d'état, portée volontairement
  limitée (pas de simulation du venv Nautilus), avec justification écrite
  dans le fichier lui-même.
- Lot 5 (isolation tests Nautilus) : confirmé `REJECTED` par décision
  humaine journalisée dans `.ai/archive/20260808_EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE.md`
  section 10, pas un oubli — devenu superflu de toute façon puisque le lot 3
  a supprimé la cause racine de l'échec d'environnement.

Deux passes indépendantes (Parties A/B produites plus tôt dans la journée,
Partie C produite séparément sans les lire d'abord) aboutissant au même
verdict sur les mêmes mécanismes est un signal de confiance plus fort qu'une
passe unique, quelle que soit sa rigueur — c'est exactement le principe
« ne jamais accepter une affirmation sur la seule foi d'un document » appliqué
récursivement au document d'audit lui-même.

### Écart mineur relevé (précision, pas contradiction)

La Partie B mesure `governance/` + `validators/` à 1713 lignes. Un recomptage
indépendant dans cette passe (`wc -l` sur les fichiers `.py` de premier
niveau des deux dossiers, hors `tests/`) donne **1992 lignes**
(1161 `governance/` + 831 `validators/`), identique à la méthodologie de
l'audit fondateur du 07/08 (qui annonçait 1970). L'écart avec le chiffre de
la Partie B vient probablement d'une portée de comptage différente (peut-être
un sous-dossier exclu) plutôt que d'une régression de la surface auditée : la
tendance (surface stable, modeste, auditable dans son ensemble) reste
confirmée quel que soit le chiffre retenu. Signalé pour traçabilité, sans
impact sur le verdict.

### Angle mort non couvert par les Parties A/B : la CI ne bloque rien

Vérification indépendante, absente des Parties A et B : **la CI GitHub
(lot 6) produit un verdict, mais ne conditionne aucun gate.**

```
$ gh api repos/LucBrice/EBTA---David-Aronson/branches/main/protection
{"message":"Branch not protected","documentation_url":"...","status":"404"}

$ gh api repos/LucBrice/EBTA---David-Aronson/rulesets
[]
```

Confirmé par deux appels API GitHub indépendants : la branche `main` n'a
**aucune règle de protection** et **aucun ruleset** actif. Conséquence
concrète : un push direct sur `main` (le mode de fonctionnement actuel de ce
dépôt, confirmé par `git log` — tous les commits récents sont des commits
directs sur `main`, pas des PR) atterrit immédiatement, que la CI passe ou
non. Le commentaire du fichier `ebta-runtime-suite.yml` lui-même est honnête
sur ce point (« infrastructure the agent does not control and cannot
silently skip ») — il ne prétend pas bloquer, seulement fournir un verdict
non auto-rapporté. Mais la distinction entre « verdict indépendant visible »
et « gate qui empêche l'atterrissage » n'était pas explicitée dans les
Parties A/B, qui décrivent le lot 6 comme fermant le risque CI sans préciser
cette limite.

**Scénario concret non couvert** : un agent de codage pousse un commit qui
casse la suite de tests. Le hook local `pre-push` (Lot 2) bloquerait ce push
*si* il s'exécute réellement — mais il reste contournable localement par
`--no-verify` sans laisser de trace côté serveur. Si contourné (ou si le
hook n'est pas installé sur la machine qui pousse — rien ne force son
installation, voir `Implementation/Active/INSTALL_GIT_HOOK.md`), le commit
cassé atterrit sur `main`, la CI tourne après coup et devient rouge, mais
rien n'empêche un travail ultérieur (humain ou IA) de continuer à construire
sur ce `main` cassé jusqu'à ce que quelqu'un remarque le X rouge. Ce n'est
pas une régression introduite par le lot 6 — c'est un plafond structurel de
« CI sans branch protection », inhérent au choix (probablement délibéré, à
confirmer) de ne pas configurer de règle de protection sur un dépôt à
développeur unique.

## Recommandations (Partie C, à trier par l'humain)

1. **Décision à clarifier, pas nécessairement une action** : l'absence de
   branch protection sur `main` est-elle un choix assumé (dépôt solo, la CI
   sert d'alerte a posteriori et suffit) ou un oubli du lot 6 ? Si un gate
   réel est souhaité, GitHub permet une règle « Require status checks to
   pass before merging » — mais cela suppose de passer par des PR au lieu de
   push directs sur `main`, ce qui est un changement de workflow, pas une
   simple case à cocher. Ne pas configurer cela sans décision humaine
   explicite : cela changerait la façon dont ce dépôt solo travaille au
   quotidien.
2. S'assurer que `Implementation/Active/INSTALL_GIT_HOOK.md` est
   effectivement suivi sur toute machine/environnement d'où une IA pousse
   vers ce dépôt — rien ne le vérifie mécaniquement aujourd'hui (l'existence
   du hook côté serveur ne peut pas être imposée sans branch protection, cf.
   point 1).
3. Corriger le chiffre `governance/`+`validators/` de la Partie B (1713 vers
   1992, ou clarifier la méthodologie de comptage utilisée) — cosmétique,
   sans urgence.

## Non-goals de cette passe

Aucune modification de `Protocole/`, `Implementation/`, `.ai/` ou
`.github/`. Aucune configuration de branch protection effectuée — trouvaille
seule, décision laissée à l'humain (recommandation 1 ci-dessus). Aucune
ré-exécution outillée d'`adversarial-tester` sur `governance/` (la Partie B
s'appuie déjà sur le rapport du lot 4 ; cette passe ne l'a pas refait non
plus).

## Niveau de confiance (Partie C)

- **Sur ce qui a été vérifié directement** : haute — code relu
  indépendamment ligne par ligne pour les six mécanismes, suite de tests
  ré-exécutée avec résultat observé (`242 tests, OK`), absence de branch
  protection confirmée par deux appels API GitHub distincts (`protection` et
  `rulesets`), hooks installés comparés octet-pour-octet à leur source.
- **Sur l'exhaustivité de la couverture** : modérée-haute — corrobore
  indépendamment l'essentiel des Parties A/B (bon signal de convergence
  inter-sessions), ajoute un angle (gouvernance GitHub au niveau branche) non
  couvert par elles, mais ne réaudite pas `Protocole/` ni la couche
  méthodologique/statistique (hors périmètre de ce skill), et ne relit pas
  `plan.ps1` dans son intégralité au-delà des points d'appel déjà vérifiés en
  Partie A.

### Verdict global (Partie C)

Le dépôt est, de façon vérifiée et corroborée par deux passes indépendantes
produites séparément le même jour, **substantiellement plus robuste** qu'au
07/08 : les cinq points de rupture de l'audit fondateur sont fermés ou
explicitement REJECTED par décision humaine, avec preuve mécanique (tests,
hooks identiques, CI réelle) plutôt que déclarative. Le seul point non déjà
consigné par les Parties A/B est structurel et probablement déjà connu de
l'humain : une CI qui donne un verdict indépendant n'est pas la même chose
qu'une CI qui bloque un atterrissage sur `main`, tant qu'aucune règle de
protection de branche n'existe.

---

## Partie D — Filets mécaniques complémentaires (même session, suite de la Partie C)

Poursuite de la Partie C sur une question distincte posée par l'utilisateur :
au-delà des cinq points de rupture de l'audit fondateur (tous fermés ou
REJECTED), existe-t-il **d'autres catégories** de filets mécaniques absentes
du dépôt et qui mériteraient d'être ajoutées ? Boucle de 3 passes de
vérification directe (pas de supposition) avant de formuler des
recommandations. Aucune modification effectuée — audit seul.

### Passe 1 — hygiène du dépôt et fichiers versionnés

- **Aucun `.gitignore` à la racine du dépôt.** Le seul existant,
  `Implementation/.gitignore`, ne couvre que `__pycache__/`, `*.py[cod]`,
  `research_packages/`.
- Le venv Nautilus (`Implementation/adapters/nautilus_env/venv/`, **2,6 Go**,
  contient `numpy`/`pandas`/`nautilus_trader`) n'est pas suivi par git — mais
  uniquement grâce à son propre `.gitignore` auto-généré par l'outil `venv`
  lui-même (`venv/.gitignore` contenant `*`), pas grâce à une protection du
  dépôt. Un `git add -f` explicite ou un venv recréé par un outil qui ne
  génère pas ce fichier n'est protégé par rien au niveau du dépôt.
- `pyproject.toml` existe à la racine (config `[tool.pyrefly]` uniquement,
  pas de section `build-system`/`dependencies`) — nuance mineure sur
  l'affirmation de `CLAUDE.md` (« no requirements.txt/pyproject.toml »), sans
  impact sur la robustesse.
- Aucun secret grossier trouvé dans les fichiers versionnés (grep motifs
  `api_key=`, `password=`, clés privées). Aucun `TODO`/`FIXME` orphelin dans
  `Implementation/ebta_engine` hors tests.

### Passe 2 — filets natifs GitHub, interrogés via API (pas supposés)

Le dépôt est **public** (`gh api repos/.../` → `"visibility":"public"`), et :

```
"secret_scanning": {"status": "disabled"}
"secret_scanning_push_protection": {"status": "disabled"}
"dependabot_security_updates": {"status": "disabled"}
```

Aucun `.github/dependabot.yml`. `Implementation/adapters/nautilus_env/requirements.txt`
épingle `nautilus_trader==1.230.0`, mais `.github/workflows/ebta-runtime-suite.yml`
installe `numpy`/`pandas` **sans version fixée** (`pip install numpy pandas`)
— une montée de version majeure amont pourrait changer un comportement
numérique silencieusement, sans qu'aucun test existant ne le détecte
nécessairement.

### Passe 3 — recoupement positif (filet déjà présent, à ne pas dupliquer)

`Implementation/ebta_engine/tests/test_protocol_manifest_hashes.py::test_frozen_protocol_hashes_still_match`
recalcule le SHA-256 de chaque fichier listé dans
`Protocole/MANIFESTE DE GEL EBTA.md` et fait échouer la suite si un seul
octet a changé — filet anti-altération silencieuse du `Protocole/` déjà en
place, déjà couvert par la CI (le lot 6 l'a même cassé volontairement une
fois pour prouver que la CI le détecte réellement, puis reverté — voir
commits `97ad264`/`038f315`). Ne pas recréer ce mécanisme, il existe déjà et
fonctionne.

### Recommandations consolidées à trier par l'humain (Parties C + D)

Priorisées par rapport coût/bénéfice, avec référence précise pour
implémentation directe par une autre IA :

1. **Activer le secret scanning + push protection GitHub** (paramètres du
   dépôt, gratuit sur un dépôt public, zéro dépendance ajoutée). Actuellement
   `disabled` alors que le dépôt est public — bloque un `push` contenant un
   token/clé avant qu'il n'atterrisse sur `main`. Aucune modification de
   fichier requise, juste une action dans les Settings GitHub du dépôt
   (Settings → Code security → Secret scanning / Push protection).
2. **Ajouter un `.gitignore` à la racine du dépôt**, couvrant explicitement
   `venv/`, `.venv/`, `__pycache__/`, `*.py[cod]`, et les résidus OS/IDE
   courants (`.DS_Store`, `Thumbs.db`, `.vscode/`, `.idea/`). Ferme le risque
   qu'un `git add -A` futur aspire les 2,6 Go du venv Nautilus dans
   l'historique git — protection aujourd'hui accidentelle (dépend du
   `.gitignore` interne du venv), pas voulue par le dépôt.
3. **Activer Dependabot** (alerts au minimum, éventuellement security
   updates) pour les dépendances `numpy`/`pandas`/`nautilus_trader` — gratuit,
   natif GitHub, cohérent avec le fait que le dépôt est public et que ces
   dépendances sont déjà présentes dans `Implementation/adapters/`.
4. **Épingler les versions `numpy`/`pandas` dans `.github/workflows/ebta-runtime-suite.yml`**
   (aujourd'hui `pip install numpy pandas` sans version), pour la
   reproductibilité de la CI et pour éviter qu'une release amont ne change un
   résultat numérique sans qu'aucun test ne le signale comme une régression
   d'environnement plutôt que de logique.
5. **Clarifier/configurer la protection de branche sur `main`** (déjà
   identifié en Partie C, recommandation 1) : décision à prendre en premier
   (passer par des PR changerait le mode de travail actuel du dépôt solo), à
   ne pas configurer sans validation humaine explicite.
6. **Ajouter Pyrefly comme étape déterministe de la CI** (`ebta-runtime-suite.yml`),
   en plus de la suite `unittest` déjà présente — bloque si le compte
   d'erreurs Pyrefly sur `Implementation/ebta_engine/` n'est pas zéro,
   indépendamment de toute preuve `bug_hunter` écrite par un agent. Ne ferme
   pas le triage sémantique faux-positif/vrai-bug (jugement humain/IA), mais
   retire la possibilité de fabriquer un rapport « 0 erreur » sans avoir
   réellement fait tourner l'outil.
7. **Envisager un linter (`ruff` recommandé, rapide et standard)** comme
   outillage CI/dev — même précédent de gouvernance que Pyrefly/`jsonschema`
   (`EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE.md` section 10 : autorisé comme
   outillage CI, jamais comme dépendance runtime du moteur). Couvre une
   catégorie de défauts que ni le type-checker ni les tests ne détectent
   (imports inutilisés, `except Exception` trop large, argument par défaut
   mutable, complexité excessive) — motifs aujourd'hui traqués seulement à la
   main pendant les audits ou les passages `adversarial-tester`.

Aucune de ces recommandations n'a été implémentée par cet audit — toutes
restent à trier, prioriser et autoriser explicitement par l'humain avant
tout `/start`, conformément à `.ai/governance/AI_MODIFICATION_CHECKLIST.md`
et au principe « aucune décision d'implémentation prise par le skill
lui-même ».

### Niveau de confiance (Partie D)

- **Sur ce qui a été vérifié directement** : haute — état réel interrogé via
  `gh api` (visibility, security_and_analysis, vulnerability-alerts,
  protection, rulesets), fichiers `.gitignore` et `pyproject.toml` lus
  intégralement, taille du venv mesurée sur disque, contenu de
  `ebta-runtime-suite.yml` relu pour confirmer l'absence de pin de version.
- **Sur l'exhaustivité de la couverture** : modérée à l'issue de cette
  section — voir la Partie E ci-dessous, qui reprend explicitement les
  catégories non explorées ici (couverture de tests, chaîne
  d'approvisionnement CI, SAST, encodage, intégrité des références internes)
  plutôt que de les laisser comme un aveu non suivi d'effet.

---

## Partie E — Élargissement de la couverture (même session, sur demande explicite de l'utilisateur)

L'utilisateur a explicitement refusé que « couverture modérée » reste un
aveu sans suite : demande de creuser réellement les catégories non
explorées en Partie D plutôt que de les lister comme limite acceptée.
Nouvelle passe de vérification directe sur cinq catégories supplémentaires.

### 1. Chaîne d'approvisionnement de la CI elle-même

`.github/workflows/ebta-runtime-suite.yml` référence `actions/checkout@v4`
et `actions/setup-python@v5` — des **tags mutables**, pas des SHA de commit
épinglés. Un tag `@v4` peut techniquement être redirigé en amont (scénario
déjà survenu dans l'écosystème GitHub Actions, ex. l'incident
`tj-actions/changed-files` de 2025) ; épingler sur SHA
(`actions/checkout@<sha>  # v4.x.x`) est la pratique de durcissement
standard. Risque faible en pratique (actions officielles GitHub,
probabilité de compromission basse) mais réel et aujourd'hui non mitigé.

Aucun bloc `permissions:` n'est déclaré dans le workflow — le `GITHUB_TOKEN`
hérite donc des permissions par défaut du dépôt au lieu du principe de
moindre privilège (`permissions: contents: read` suffirait, ce job ne
publie rien). Vérifié par lecture intégrale du fichier, pas supposé.

### 2. Mesure de couverture de tests

Aucun outil de couverture (`coverage.py` non installé, aucun `.coveragerc`)
n'existe dans ce dépôt. Conséquence concrète : « 242 tests, OK » ne dit rien
sur la **proportion réelle** du code exercée. Un chemin d'erreur non testé
peut coexister indéfiniment avec une suite entièrement verte, sans qu'aucun
signal ne le révèle. C'est une catégorie de filet mécanique entièrement
absente aujourd'hui, distincte de tout ce qui a été recommandé jusqu'ici.

### 3. Motifs de sécurité dangereux (SAST minimal)

Grep ciblé sur `eval(`, `exec(`, `pickle.load`, `yaml.load(` (sans
`safe_load`), `os.system(`, `subprocess.*shell=True` dans
`Implementation/ebta_engine`, `.ai/tools`, `.agents`, `Implementation/Active`
(hors tests, hors venv) : **zéro occurrence**. Constat positif vérifié, pas
supposé — ce dépôt n'a pas ce genre de défaut classique.

### 4. Encodage

Les 27 fichiers Markdown de `Protocole/` ont été vérifiés individuellement
pour un BOM UTF-8 en tête de fichier (risque classique sur un dépôt à
contributions Windows/éditeurs multiples, pouvant faire échouer une lecture
stricte en amont) : **zéro fichier avec BOM**. Constat positif vérifié.

### 5. Intégrité des références internes de `checkpoint.json`

Vérification mécanique de tous les champs `source_path`,
`original_draft_path`, `active_runtime_path` des 40+ workstreams de
`checkpoint.json` contre le système de fichiers réel : **2 références ne
résolvent pas**.

- `EPIC_ARCHITECTURE_IA_RAG.source_path` → `.ai/backlog/annexes/EPIC_Proposition_Architecture_IA_RAG.md`
  (absent). **Attendu** : le `closure_reason` du workstream documente
  explicitement « Fichier source supprimé manuellement par l'humain le
  2026-07-01 ; plan rejeté avant exécution » — cohérent, pas un défaut.
- `PLAN_IMPLEMENTATION_GOUVERNANCE_BIAIS_EBTA.source_path` →
  `.ai/backlog/annexes/PLAN_IMPLEMENTATION_GOUVERNANCE_BIAIS_EBTA.md`
  (absent). **Non expliqué et non attendu** : le fichier a en réalité été
  archivé vers `.ai/archive/20260701_PLAN_IMPLEMENTATION_GOUVERNANCE_BIAIS_EBTA.md`
  (confirmé present sur disque), mais `checkpoint.json` n'a jamais été mis à
  jour pour pointer vers ce nouveau chemin. **C'est un vrai défaut de
  données, trouvé mécaniquement, pas hypothétique** : `checkpoint.json` se
  déclare lui-même comme source de vérité unique
  (`relay_contract.only_files`), et cette référence brisée le contredit.
  Impact limité (workstream `DONE`, personne ne dépend activement de ce
  lien), mais c'est la preuve concrète qu'aucun mécanisme ne vérifie
  aujourd'hui que les références de `checkpoint.json` pointent vers des
  fichiers réels — un script de moins de 20 lignes en CI le ferait.

### Recommandations supplémentaires (Partie E)

8. **Épingler `actions/checkout` et `actions/setup-python` sur un SHA de
   commit** dans `ebta-runtime-suite.yml`, plutôt que sur un tag mutable
   (`@v4`/`@v5`). Durcissement standard contre un scénario de compromission
   de la chaîne d'approvisionnement CI.
9. **Ajouter `permissions: contents: read`** en tête de
   `ebta-runtime-suite.yml` — principe de moindre privilège pour le
   `GITHUB_TOKEN`, ce job n'a besoin d'écrire nulle part.
10. **Ajouter une mesure de couverture de tests** (`coverage.py` en CI,
    seuil à définir avec l'humain) — catégorie de filet aujourd'hui
    entièrement absente, distincte de « la suite passe » (`242 tests, OK`
    ne garantit aucune proportion de code exercé).
11. **Corriger `checkpoint.json::workstreams[PLAN_IMPLEMENTATION_GOUVERNANCE_BIAIS_EBTA].source_path`**
    vers `.ai/archive/20260701_PLAN_IMPLEMENTATION_GOUVERNANCE_BIAIS_EBTA.md`
    (correctif de données trouvé par cette passe, pas une recommandation
    d'architecture) — et envisager un script de vérification mécanique de
    toutes les références `*_path` de `checkpoint.json`, réutilisable en CI,
    pour éviter la récurrence de ce type de dérive.

### Niveau de confiance (Partie E)

- **Sur ce qui a été vérifié directement** : haute — grep exhaustif sur les
  motifs SAST listés (hors venv/tests), vérification BOM sur l'intégralité
  des 27 fichiers `Protocole/*.md` (pas un échantillon), vérification
  mécanique des 40+ références `*_path` de `checkpoint.json` contre le
  système de fichiers réel (pas un sondage), lecture intégrale du workflow
  CI pour les tags d'action et l'absence de bloc `permissions`.
- **Sur l'exhaustivité de la couverture** : toujours pas totale — des
  catégories restent non explorées même après cette passe élargie (détection
  de code mort, imports circulaires, complexité cyclomatique par fonction,
  liens Markdown internes cassés entre documents `Protocole/`/`.ai/`,
  licences des dépendances tierces). La différence avec la Partie D n'est
  pas que la couverture est devenue exhaustive — aucun audit ne peut
  honnêtement le prétendre — c'est que chaque catégorie nommée a maintenant
  été **vérifiée mécaniquement avec un résultat concret** (0, 2, ou une
  liste précise), au lieu d'être citée comme angle mort non creusé.

---

## Partie F — Arbitrage par Conseil des 5 : que retenir des Parties D/E + du prompt externe ~35 familles ?

Demande explicite de l'utilisateur : les Parties D et E, plus un prompt externe
proposant ~35 familles d'outils supplémentaires (ruff, mypy/pyright, pydantic,
hypothesis, mutation testing, fuzzing, semgrep/bandit/codeql, SBOM,
observabilité, feature flags…), produisaient trop de candidats pour arbitrer
seul sans sur-engineering. Conseil des 5 convoqué en mode `decision`
(Contrarian, First Principles, Expansionist, Outsider, Executor), cinq
délibérations indépendantes en parallèle sur le même paquet de preuves, chaque
allégation factuelle forte re-vérifiée directement (code lu, commandes
ré-exécutées) avant d'être retenue dans la synthèse.

### Convergence unanime (5/5)

**Rejeter en bloc les ~35 familles du prompt externe.** Elles sont calibrées
pour un service en production avec des utilisateurs, un runtime long et des
appelants externes (observabilité OTel/Sentry/Prometheus, feature flags,
circuit breakers, SBOM/sigstore/SLSA, Docker/devcontainers, chaos testing,
canary, CODEOWNERS, contract tests) — rien de tout cela n'a d'objet dans un
dépôt de recherche quantitative solo, sans serveur, sans DB, sans déploiement.
Rejeter aussi Dependabot (créerait des PR dans un dépôt à 0 PR sur 160
commits), la mesure de couverture de tests (`coverage.py`), la migration vers
`pytest`, et la branch protection **avec revue obligatoire** (un solo ne peut
pas s'auto-approuver ; avec 0 approbation requise c'est un bouton
cérémoniel).

### Le diagnostic qui change la priorisation

Quatre des cinq membres, indépendamment, sont arrivés au même critère de tri,
dérivé de la taxonomie réelle des ~12 incidents documentés dans l'historique
du dépôt (booléens codés en dur, WRC masqué, `wrc_pass` figé,
`invariant_evidence` fabriqué) : **aucun outil de type/lint/sécurité/coverage
ne peut faire échouer un artefact dont chaque valeur est individuellement
bien typée, conforme au schéma et syntaxiquement légale.** `True` et `"PASS"`
sont des valeurs canoniques et parfaitement propres pour Pyrefly, ruff,
pydantic ou bandit. Le mode de défaillance qui coûte réellement de l'argent —
un `PASS` alors que la vérité est `FAIL` — est structurellement invisible
pour la quasi-totalité des 46 candidats évalués (11 + ~35).

**Preuves concrètes trouvées et vérifiées pendant la délibération** (pas
hypothétiques) :
- `Implementation/examples/minimal_pilot_pipeline/build_research_package.py:614` :
  `"live_approval": True` en dur, encadré par trois attestations correctement
  dérivées (`live_version_id`, `kill_switch`, `lifecycle_archive`). Le gate
  G13 (déploiement live) peut donc atteindre PASS sur une approbation que
  rien ne vérifie. Second cas similaire lignes 657-660 (`gate_reports` en
  littéraux) alors que la fonction sœur ligne 922 du même fichier dérive
  correctement la même valeur.
- `Implementation/ebta_engine/tests/test_protocol_manifest_hashes.py` lit les
  hashes attendus **dans le fichier même** qu'il protège
  (`Protocole/MANIFESTE DE GEL EBTA.md`), lequel ne figure pas dans sa propre
  table de 26 hashes. Modifier un fichier du `Protocole/` puis mettre à jour
  sa ligne de hash donne une suite verte, une CI verte, un `pre-push` vert.
- `test_gate_discrimination_experiment.py:65` : le seul test qui prouve
  qu'un candidat perdant est rejeté tourne avec
  `segment_runner=_fake_segment_runner` — jamais sur le vrai pipeline.
- Zéro test de calibration statistique du WRC (grep
  `false_positive|null_distribution|white_noise|random_walk` → aucune
  occurrence). Exécution réelle du WRC sur bruit gaussien pur (40 essais,
  100 réplications, 0,26 s) : taux de PASS = 2,5 %, cohérent avec α = 5 % —
  bon signe aujourd'hui, mais rien ne détecterait sa dégradation.
- Aucune assertion sur le nombre de tests (242) nulle part : un agent qui
  supprime un fichier de test rend la CI verte.
- Ratio de commits sur 30 jours : 133 sur `.ai/` contre 3 sur
  `Implementation/ebta_engine/procedures/` et 1 sur `Protocole/` — mesuré,
  pas estimé.
- Ruff (ruleset ciblé bugs `F,E9,B,PLE,RUF`, pas `--select ALL`) : **26
  findings**, 0,15 s, pas un chantier de nettoyage. Pyrefly **sans** le venv
  Nautilus (31 Mo, pas 2,6 Go) : 0,53 s, et trouve un vrai `TypeError` dans
  `Implementation/notebooks/03_candidate_matrix_build.ipynb` (appel de
  `build_nautilus_inputs()` sans son paramètre requis `package_dir`) que les
  242 tests ne détectent pas.
- Un **troisième** chemin cassé trouvé pendant la délibération, en plus des
  deux `source_path` de la Partie E :
  `Implementation/Active/tracking.json::active_scope[1]` pointe vers
  `.ai/backlog/mainline/PLAN_IMPLEMENTATION_MOTEUR_BACKTEST_EBTA_NAUTILUS.md`,
  inexistant (les trois dossiers `.ai/backlog/{mainline,annexes,fixes}/` ne
  contiennent que leur `README.md`).

### Recommandation retenue : 3 lots, dans cet ordre

**Lot 0 — ce soir, ~5 min, zéro fichier versionné touché, zéro cycle de
gouvernance `/start`.** Réglages GitHub uniquement :
- Activer le secret scanning + la push protection (dépôt public,
  actuellement `disabled`).
- Un ruleset sur `main` bloquant le force-push et la suppression de
  branche — **sans** exiger de revue/PR. Seule protection du dossier qu'un
  agent de codage ne peut pas contourner localement, et qui ne change rien
  au rythme de travail actuel (commit direct sur `main`).

**Lot 1 — le sujet prioritaire : rendre le faux succès mécaniquement
détectable.** Quatre tests `unittest` stdlib, zéro dépendance nouvelle, zéro
décision de gouvernance requise (héritent gratuitement de la CI et du hook
`pre-push` déjà existants) :
1. **Contrôle négatif du WRC** : du bruit gaussien pur ne doit jamais
   produire un PASS, taux de faux PASS borné (seeds fixés et versionnés,
   seuil large type « ≤ 3 PASS sur 40 » pour éviter le flaky).
2. **Tests métamorphiques sur le WRC** : la pénalité de multiplicité doit
   être monotone croissante avec la taille de la famille de candidats
   (vérifié faisable : p passe de 0,479 à 0,818 entre 4 et 44 candidats) ;
   le verdict doit être invariant au renommage des candidats.
3. **Cliquet d'inventaire de tests** (*test ratchet*) : un fichier versionné
   listant les identifiants de tests actuels (242 au 08/08), et un test qui
   échoue si l'un disparaît sans mise à jour explicite du fichier dans le
   même commit — rend toute suppression de test visible dans un diff.
4. **Inventaire des littéraux de verdict** : script stdlib (AST, ~150
   lignes) qui échoue en CI sur tout nouveau littéral `"PASS"`/`True` affecté
   à une clé de gate/attestation/évidence d'invariant, hors allowlist
   annotée. Corrige au passage `live_approval` ligne 614 (trouvaille de
   cette délibération, pas une recommandation abstraite).

**Lot 2 — durcissement groupé en un seul chantier `fix`** (regroupe les
items 2, 4, 8, 9, 11 des Parties D/E pour ne payer qu'un seul cycle de
gouvernance) :
- `.gitignore` racine, épingler `numpy`/`pandas` en CI, actions GitHub sur
  SHA, bloc `permissions: contents: read`.
- Corriger les 3 références cassées (`checkpoint.json` ×2 + le
  `tracking.json::active_scope[1]` trouvé pendant cette délibération) et
  ajouter un script de vérification des `*_path`/`active_scope` dans le
  hook `pre-commit` existant (budget disponible : le hook tourne en 0,18 s
  aujourd'hui).
- Pyrefly en CI (config : `--replace-imports-with-any "nautilus_trader.*"`,
  ne pas simuler le venv Nautilus de 2,6 Go — piège d'implémentation
  identifié : le `pyproject.toml` racine contient un
  `python-interpreter-path` Windows en dur, à neutraliser explicitement en
  CI) et ruff avec le ruleset ciblé `F,E9,B,PLE,RUF` uniquement (pas
  `--select ALL`, qui produirait ~3700 findings sans rapport avec le mode de
  défaillance visé).

**Explicitement écarté** : les ~35 familles du prompt externe, Dependabot,
`coverage.py`, migration `pytest`, branch protection avec revue obligatoire.

### Dissidence matérielle (conservée, pas résolue)

L'Outsider maintient que le vrai problème n'est pas un déficit de garde-fous
mais l'**hypertrophie de la couche de contrôle elle-même** : l'échafaudage IA
(`.ai/` + `0 - HUMAN START HERE/` + `.agents/`, 47 698 lignes mesurées) pèse
3,3× la science normative (`Protocole/`, 14 542 lignes). Sur cette lecture,
la mesure la plus rentable serait un *gel* de la gouvernance, pas un ajout,
et seul le test de calibration statistique (Lot 1, point 1) compte vraiment.

Cette dissidence ne contredit pas la recommandation ci-dessus, elle la
**contraint** : le Lot 1 est délibérément du garde-fou exécutable (un test
qui s'exécute) plutôt que narratif (un document qui décrit), et le Lot 2 est
compressé en un seul cycle au lieu de 5. **Condition qui rendrait la
dissidence décisive, à observer après implémentation** : si les Lots 1 et 2
génèrent plus de commits dans `.ai/` (plans, audits, preuves, mises à jour
de `checkpoint.json`) que de lignes de test réellement ajoutées dans
`Implementation/ebta_engine/tests/`, l'Outsider avait raison — il faut
arrêter d'ajouter et geler la gouvernance à la place.

**Risque signalé sans être tranché, hors périmètre technique de ce
Conseil** : personne n'a vérifié que `D:\Livre\Trading\Trading algorithmic\EBTA - David Aronson`
est sauvegardé ailleurs que sur ce disque et sur le remote GitHub public.
C'est le seul risque irréversible identifié dans toute la délibération, et
aucun des 46 candidats évalués ne le couvre.

### Prochaine action concrète

Lot 0 ce soir (5 minutes, réversible en une commande `gh api`), puis `/start`
sur le Lot 1 routé comme **un seul chantier** à quatre tests (pas quatre
chantiers séparés) pour respecter la logique de regroupement de coût de
gouvernance identifiée par l'Executor (11 items traités séparément = 11
cycles `/start`→`/close` pour ~4 h de travail technique réel). Seuil de
décision pour la suite : si l'inventaire des littéraux (Lot 1, point 4)
remonte plus de ~20 occurrences au premier passage, le problème n'est plus
la surveillance mais l'architecture d'assemblage elle-même, et il faut
reposer la question à l'humain avant de continuer à ajouter des tests.

### Niveau de confiance (Partie F)

- **Sur ce qui a été vérifié directement** : haute — les neuf allégations
  factuelles décisives des cinq délibérations (littéral `live_approval`,
  manifeste auto-référentiel, absence de test de calibration,
  `_fake_segment_runner`, ratio de commits 133:3, bug réel du notebook,
  26 findings ruff, Pyrefly sans venv, 3 références cassées) ont été
  re-vérifiées indépendamment par lecture de code ou ré-exécution de
  commande, pas acceptées sur la seule foi du rapport d'un membre.
- **Sur l'exhaustivité de la couverture** : modérée — le Conseil a délibéré
  sur le paquet de preuves des Parties C/D/E et le prompt externe, pas sur
  une nouvelle exploration indépendante du dépôt ; la revue croisée en
  aveugle a été menée par le président (moi) plutôt que par des agents
  relecteurs séparés (procédure compressée, déclarée conformément au mode
  `decision` du skill Council of Five).

---

## Partie G — Plan de chantier consolidé (prêt pour `/start`)

Ce plan fusionne, sans doublon, toutes les recommandations retenues des
Parties D, E et F. Chaque item n'apparaît qu'une seule fois, dans le lot où
le Conseil (Partie F) l'a arbitré. Rien n'est implémenté par cette section —
c'est un brouillon de plan à auditer/router, pas une action.

| Champ | Valeur |
| --- | --- |
| Track | mainline (chantier mère) / fix (les 3 lots) |
| Lifecycle | INTAKE — non routé |
| Scope | Durcir mécaniquement le dépôt contre l'erreur silencieuse d'un agent de codage, sur le périmètre arbitré par le Conseil des 5 (Partie F) : réglages GitHub, tests de calibration/contraste statistique, durcissement CI groupé. Exclut explicitement tout ce qui a été écarté par la délibération. |
| Non-goals | Aucune des ~35 familles du prompt externe (ruff `--select ALL`, mypy/pyright, pydantic, hypothesis, mutation testing, fuzzing, bandit/semgrep/codeql, pip-audit/OSV, SBOM/sigstore/SLSA, Docker/devcontainers, CODEOWNERS, observabilité, feature flags, circuit breakers, chaos testing, policy-as-code, etc.). Pas de Dependabot. Pas de `coverage.py`. Pas de migration vers `pytest`. Pas de branch protection avec revue/PR obligatoire. Aucune modification de `Protocole/`. Aucune dépendance nouvelle au cœur statistique/gouvernance (`procedures/`, `governance/`, `validators/`, `schemas/`, `manifests/`, `persistence.py`, `constants.py`) — seuls `ruff`/`pyrefly` en outillage CI/dev sont concernés, même précédent que `jsonschema` (`EPIC_ROBUSTESSE_GARDE_FOUS_AGENT_CODAGE.md` section 10). |
| Source | Ce document (`AUDIT_ROBUSTESSE_ARCHITECTURE_FACE_ERREURS_IA_2026-08-08.md`), Parties D/E/F. Prompt externe fourni par l'utilisateur (~35 familles), arbitré et très majoritairement rejeté en Partie F. |
| Exit criteria | Les trois lots ci-dessous sont `DONE` dans `.ai/checkpoint.json` ; suite `unittest` complète toujours `OK` après chaque lot ; `bug-hunter` + `adversarial-tester` + `plan-conformance-audit` PASS avant chaque clôture, conformément au workflow `core-engine` existant. |

### Lot 0 — Réglages GitHub (aucun fichier versionné, aucun cycle `/start`)

Ne nécessite pas de chantier au sens de ce dépôt (ne touche aucun fichier
suivi par git) — action directe hors workflow, mentionnée ici pour mémoire
et complétude du plan :
- Activer le secret scanning + la push protection GitHub (dépôt public,
  actuellement `disabled`).
- Ruleset sur `main` : bloquer force-push + suppression de branche, sans
  exiger de revue/PR.

### Lot 1 — Détection mécanique du faux succès statistique (chantier `core-engine`, prioritaire)

Quatre tests `unittest` stdlib dans `Implementation/ebta_engine/tests/`,
zéro nouvelle dépendance :
1. Contrôle négatif du WRC sur bruit gaussien pur (seeds fixés et
   versionnés, seuil borné type « ≤ 3 PASS sur 40 »).
2. Tests métamorphiques sur le WRC : monotonie de la pénalité de
   multiplicité selon la taille de la famille de candidats ; invariance du
   verdict au renommage des candidats.
3. Cliquet d'inventaire de tests : fichier versionné des identifiants de
   tests actuels + test qui échoue si l'un disparaît sans mise à jour
   explicite du fichier dans le même commit.
4. Inventaire des littéraux de verdict (scan AST stdlib, ~150 lignes) :
   échoue en CI sur tout nouveau littéral `"PASS"`/`True` affecté à une clé
   de gate/attestation/évidence d'invariant, hors allowlist annotée. Inclut
   la correction de `"live_approval": True`
   (`Implementation/examples/minimal_pilot_pipeline/build_research_package.py:614`)
   et du littéral `gate_reports` équivalent (mêmes lignes 657-660).

### Lot 2 — Durcissement CI et hygiène du dépôt (chantier `fix`, groupé en un seul cycle)

- `.gitignore` à la racine du dépôt.
- Épingler les versions `numpy`/`pandas` dans
  `.github/workflows/ebta-runtime-suite.yml`.
- Épingler `actions/checkout` et `actions/setup-python` sur un SHA de
  commit (au lieu des tags `@v4`/`@v5`).
- Ajouter `permissions: contents: read` au workflow CI.
- Corriger les 3 références de chemin cassées :
  `checkpoint.json::workstreams[EPIC_ARCHITECTURE_IA_RAG].source_path` (déjà
  expliquée par son `closure_reason`, à documenter comme telle plutôt qu'à
  "corriger"),
  `checkpoint.json::workstreams[PLAN_IMPLEMENTATION_GOUVERNANCE_BIAIS_EBTA].source_path`
  (à pointer vers `.ai/archive/20260701_PLAN_IMPLEMENTATION_GOUVERNANCE_BIAIS_EBTA.md`),
  `Implementation/Active/tracking.json::active_scope[1]` (référence un
  fichier absent de `.ai/backlog/mainline/`) — plus un script de
  vérification mécanique des `*_path`/`active_scope`, intégré au hook
  `pre-commit` existant.
- Pyrefly en CI, sans simuler le venv Nautilus
  (`--replace-imports-with-any "nautilus_trader.*"`), avec neutralisation
  explicite du `python-interpreter-path` Windows en dur dans le
  `pyproject.toml` racine pour l'environnement CI. Inclut la correction du
  bug réel trouvé (`Implementation/notebooks/03_candidate_matrix_build.ipynb`,
  appel de `build_nautilus_inputs()` sans son paramètre requis
  `package_dir`).
- Ruff en CI avec le ruleset ciblé bugs `F,E9,B,PLE,RUF` uniquement (pas
  `--select ALL`), config minimale ajoutée au `[tool.ruff]` du
  `pyproject.toml` racine existant. Corrige les 26 findings identifiés par
  l'Executor (Partie F), dont les faux positifs `E402` déjà expliqués
  (shims `sys.path` dans `Implementation/examples/`, à exclure via
  `per-file-ignores`).

### Ce que ce plan ne contient pas

Volontairement absent, conformément à l'arbitrage du Conseil (Partie F) et
au principe de non-doublon de cette section : toute recommandation déjà
explicitement écartée en Partie F, et tout retour aux items de détail des
Parties D/E qui ont été absorbés sans reformulation supplémentaire dans les
trois lots ci-dessus.
