# Exemple reel : audit retroactif de PLAN_R1_R2_SIGNAUX_ET_EXTRACTION_NAUTILUS

Cet exemple documente un audit reel (pas invente), execute a la demande de
l'utilisateur sur un plan deja archive, pour valider ce skill avant son
premier usage sur un `/close` en conditions reelles. Il montre la forme
attendue du rapport et deux difficultes reellement rencontrees qui ont fait
evoluer la procedure du skill lui-meme.

## 1. Localisation

`PLAN_ID = PLAN_R1_R2_SIGNAUX_ET_EXTRACTION_NAUTILUS`. Trouve dans
`.ai/checkpoint.json` : `status: DONE`, `lifecycle: DONE`,
`source_path: .ai/archive/20260713_PLAN_R1_R2_SIGNAUX_ET_EXTRACTION_NAUTILUS.md`,
`opened_at: 2026-07-13`, `last_moved_at: 2026-07-13`.

## 2. Contrat extrait de la table `## Triage`

Quatre Exit criteria :

1. Payloads E, F, G/H/I incrementaux : chacun passe son test de parite vert
   contre l'oracle vectorise sur un segment reel.
2. `extract_simulation_result` derive `nav`, `daily_returns`,
   `daily_exposure`, `positions`, `total_costs` du portfolio/analyzer/rapports
   Nautilus, plus de reconstruction manuelle.
3. Suite runtime 110+ tests PASS.
4. `validate_package_dir()` PASS apres R2.

## 3. Fenetre du chantier — premiere difficulte reelle

`opened_at` et `last_moved_at` sont la meme date (2026-07-13) : le chantier
a ete ouvert et cloture le meme jour, avant le debut de la conversation ou
cet audit a ete demande (2026-07-14). Or, **au moment de cet audit, des
fichiers du meme perimetre venaient d'etre modifies par un balayage
`bug-hunter` separe, dans la meme session**. Sans borner la fenetre a
`[2026-07-13, 2026-07-13]` (et non pas "jusqu'a maintenant"), ces
modifications ulterieures auraient ete confondues avec la livraison du plan
— fausse alerte de derive de perimetre, ou fausse impression de couverture
supplementaire. Consequence sur la procedure : toujours determiner la borne
haute depuis le passage a `DONE`/`BLOCKED` dans le checkpoint, jamais
depuis l'instant present.

## 4. Deuxieme difficulte reelle : pas d'historique de commits

`git log -- <chemins du perimetre>` n'a quasiment rien montre — le chantier
n'avait jamais ete commite, seulement stage (visible via `git status`). Un
audit qui se serait arrete a `git log` aurait conclu, a tort, qu'aucune
preuve n'existait. `git diff --cached --stat` sur les memes chemins a
confirme les 16 fichiers du perimetre declare (signals/*.py,
incremental/*.py, registry.py, resample.py, nautilus_mapping.py,
nautilus_strategy_bridge.py, tests). Consequence : toujours verifier l'etat
stage/working-tree en complement de l'historique de commits, surtout dans
un repo qui ne commite pas systematiquement apres chaque chantier.

## 5. Verification critere par critere

| # | Classification | Preuve |
| --- | --- | --- |
| (1) | IMPLEMENTE | `test_incremental_parity_{e,f,ghi}.py` executes directement : 6 tests en `ok`, pas `SKIP` — donc de vraies donnees M1 etaient disponibles et la comparaison oracle/incremental s'est reellement executee, pas seulement "le fichier de test existe" |
| (2) | IMPLEMENTE | Lecture directe de `nautilus_mapping.py` : decomposition SRP confirmee (`_extract_nav_series`, `_extract_costs`, `_extract_positions`) ; le seul `total_costs=0.0` restant est dans `_flat_simulation_result`, la branche NO_MODEL explicitement voulue par le plan (Cas NO_MODEL, section 5) — distinguer ce `0.0`-la de l'ancien bug `total_costs=0.0` en dur inconditionnel demande de lire le code autour, pas seulement de grep la chaine |
| (3) | IMPLEMENTE | 139 tests PASS (> 110 requis) |
| (4) | IMPLEMENTE, avec ambiguite a signaler | Seul `test_minimal_pilot_pipeline.py` appelle reellement `validate_package_dir()`, sur le pipeline pilote **non-Nautilus** — aucun test n'appelle `validate_package_dir()` sur un package construit via Nautilus specifiquement. Verification du Non-goal correspondant ("ne pas brancher dans `nautilus_research_package.py` avant R4") : `_daily_sample` est toujours present dans ce fichier, donc R4 n'est effectivement pas resolu et ce branchement n'a pas eu lieu — c'est *coherent*, pas un manque. Le critere tel que redige pretait a confusion des sa formulation initiale ; le signaler comme defaut de redaction du plan, pas comme un item manquant. |

## 6. Verdict rendu

Zero critere MANQUANT -> le chantier aurait passe le gate `/close`. Point
non-bloquant signale en plus : les champs internes du plan
(`Statut: NON_DEMARRE`, `Date d'activation: -`, section Cloture vide)
n'ont jamais ete mis a jour bien que `checkpoint.json` dise `DONE` —
`checkpoint.json` fait autorite, ce n'est pas un blocage, mais une
incoherence documentaire a faire remonter.

## Forme du rapport attendu

Reprendre la structure ci-dessus : localisation courte, tableau
`critere -> classification -> preuve`, puis toute ambiguite ou
incoherence trouvee en cours de route signalee explicitement (ne pas la
resoudre silencieusement a la place de l'humain), puis le verdict de
blocage.
