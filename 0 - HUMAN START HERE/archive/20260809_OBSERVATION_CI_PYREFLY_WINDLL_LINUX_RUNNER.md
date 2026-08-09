# Observation brute — CI `ebta-runtime-suite.yml` rouge : `ctypes.WinDLL` absent sous Linux

> Statut : `INTAKE` — brouillon humain/IA non executable.
> Ce fichier ne constitue ni un `/start`, ni une autorisation d'implementation,
> ni une source normative EBTA.

## 1. Constat

Le dernier run GitHub Actions du workflow `ebta-runtime-suite.yml` sur `main`
(run `31305469412`, commit `64a086f`) echoue a l'etape **"Run portable
Pyrefly checks"**. Les etapes suivantes (Ruff, suite `unittest`, validation
des schemas JSON) ne se sont pas executees — cascade d'annulation apres
l'echec de la premiere etape bloquante, pas une regression du moteur.

`gh run view 31305469412 --log-failed` montre 3 erreurs Pyrefly identiques
dans leur nature :

```text
ERROR No attribute `WinDLL` in module `ctypes` [missing-attribute]
  --> Implementation/ebta_engine/benchmarks/long_data.py:407:16
  --> Implementation/ebta_engine/benchmarks/long_data.py:448:16
  --> Implementation/ebta_engine/benchmarks/long_data.py:449:13
```

## 2. Diagnostic (deja verifie en local, lecture seule)

- Le code en cause (`_windows_process_parent_map` et
  `_windows_working_set_bytes` dans `long_data.py`) est du code Windows-only,
  deja garde a l'execution par `if os.name == "nt": ...` (ligne 383 du
  fichier). Pyrefly type-verifie neanmoins le corps de ces fonctions
  inconditionnellement.
- Le runner CI est `ubuntu-latest`. Reproduit en local avec
  `python -m pyrefly check --python-interpreter-path python --python-platform
  linux --replace-imports-with-any "nautilus_trader.*" Implementation/ebta_engine
  Implementation/notebooks` : les 3 memes erreurs apparaissent a l'identique.
  Sans forcer `--python-platform linux`, l'execution locale (Windows) ne les
  voit pas — differentiel de plateforme des stubs typeshed
  (`ctypes.WinDLL` n'existe que sous les stubs `win32`), pas une regression
  de code.
- Teste isolement sur un fichier de reproduction minimal : le commentaire
  inline `# pyrefly: ignore` supprime bien l'erreur (`INFO 0 errors`).
- Les 3 erreurs sont independantes entre elles (memes 2 fonctions, 3 lignes) —
  aucune n'est une consequence d'une autre.
- Le warning de depreciation Node.js 20 (annotation separee sur
  `actions/checkout` et `actions/setup-python`) n'a aucun rapport avec cet
  echec et est hors scope de cette correction.
- `Implementation/ebta_engine/benchmarks/` est du tooling de benchmark, pas
  le coeur statistique/gouvernance stdlib-only du moteur (`procedures/`,
  `governance/`, `validators/`, `schemas/`, `manifests/`, `persistence.py`,
  `constants.py`) : cette correction est technique et locale, pas normative.

## 3. Track

`fix` — correction ciblee d'un gate CI en echec, meme nature que les
precedents `PLAN_PYREFLY_CI_NOTEBOOK` et `PLAN_RUFF_CI_BUGS_CIBLES`
(`.ai/archive/20260809_PLAN_PYREFLY_CI_NOTEBOOK.md`,
`.ai/archive/20260809_PLAN_RUFF_CI_BUGS_CIBLES.md`), issus du meme
`EPIC_DURCISSEMENT_POST_AUDIT_ERREURS_IA` deja clos.

## 4. Lifecycle

`INTAKE` — ce fichier doit etre audite et route via `/start` avant toute
modification de `Implementation/ebta_engine/benchmarks/long_data.py`.

## 5. Scope

Supprimer les 3 faux positifs Pyrefly sur `ctypes.WinDLL` dans
`Implementation/ebta_engine/benchmarks/long_data.py` par un ignore cible
(`# pyrefly: ignore`) sur les 3 lignes concernees, documente par un
commentaire court expliquant pourquoi (code Windows-only deja garde a
l'execution, faux positif de plateforme du type-checker), et faire repasser
le workflow `ebta-runtime-suite.yml` au vert sur `main`.

## 6. Non-goals

- Ne pas passer `--python-platform windows` (ou win32) au check Pyrefly
  global du workflow — masquerait silencieusement de vraies erreurs de
  portabilite POSIX ailleurs dans `Implementation/ebta_engine` et
  `Implementation/notebooks`.
- Ne pas desactiver, contourner ni assouplir Pyrefly, Ruff, la suite
  `unittest` ou les validations de schema JSON pour faire passer la CI.
- Ne pas toucher `Protocole/`, le coeur stdlib-only du moteur
  (`procedures/`, `governance/`, `validators/`, `schemas/`, `manifests/`,
  `persistence.py`, `constants.py`), `Implementation/Active/`, ni
  `.github/workflows/ebta-runtime-suite.yml`.
- Ne pas traiter le warning de depreciation Node.js 20 (hors scope, sans
  lien avec cet echec).

## 7. Source

Demande humaine explicite : "Inspecte immediatement le dernier echec GitHub
Actions du workflow `ebta-runtime-suite.yml` sur la branche `main` (run #8,
commit `64a006f`)... Corrige la cause dans le repository." Correction
demandee le 2026-08-09.

## 8. Exit criteria

- `python -m pyrefly check --python-interpreter-path python --python-platform
  linux --replace-imports-with-any "nautilus_trader.*" Implementation/ebta_engine
  Implementation/notebooks` retourne `0 errors` (equivalent local du runner
  CI Linux).
- `python -m ruff check Implementation/ebta_engine` retourne
  `All checks passed!` (aucune regression introduite).
- `python -m unittest discover -s Implementation/ebta_engine/tests -t
  Implementation` passe integralement (aucune regression).
- Le nouveau run GitHub Actions `ebta-runtime-suite.yml` declenche par le
  commit de correction est `success` (`gh run list --workflow=ebta-runtime-suite.yml
  --branch main --limit 3`).

## Journal de convergence de l'intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Plan reecrit confronte au code reel (`long_data.py:370-471`) via `code-architecture-evaluator` : garde runtime cite, dependances inversees verifiees par grep, sequencement des commandes de verification. | 2 corrections appliquees : garde `os.name == "nt"` incomplet (un seul des deux points d'entree cite), risque de faux succes local si `--python-platform linux` omis lors de la Phase 1. |
| 2 | Relecture du plan corrige confrontee a `.ai/checkpoint.json` (workstreams `PLAN_PYREFLY_CI_NOTEBOOK`, `PLAN_RUFF_CI_BUGS_CIBLES`) pour verifier la justification du `track: fix`. | 1 correction appliquee : les deux precedents sont en realite `track: mainline` (sous-chantiers d'un epic actif), pas `fix` — la justification du `track: fix` de ce chantier a ete reecrite pour refleter l'absence d'epic parent actif, plutot que citer a tort un alignement avec les precedents. |
| 3 (confirmation) | Relecture structurelle complete du plan reecrit (`.ai/backlog/fixes/PLAN_CORRECTION_PYREFLY_CI_WINDLL_LINUX.md`) : toutes les sections obligatoires du gabarit presentes et correctement numerotees, aucun nouvel angle mort majeur detecte. | Convergence confirmee : aucune correction supplementaire necessaire. |

