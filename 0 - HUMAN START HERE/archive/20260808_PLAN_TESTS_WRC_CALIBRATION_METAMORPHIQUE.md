# Intake — Tests WRC de regression nulle et metamorphique

Date : 2026-08-08

| Champ | Valeur |
| --- | --- |
| Track | `mainline` |
| Lifecycle | `INTAKE` — non executable |
| Type de chantier | `SINGLE` |
| Scope | Ajouter des tests `unittest` deterministes qui rendent visible une derive grossiere du WRC sous bruit gaussien et des ruptures de deux proprietes controlees : invariance au renommage et penalite sur une extension de famille construite. |
| Non-goals | Aucun changement de `wrc.py`, du bootstrap, des SOP, d'alpha ou du nombre normatif de repetitions ; aucune certification universelle de calibration ; aucun test stochastique non reproductible ; aucun acces OOS. |
| Source | Sous-chantier 1/7 de `EPIC_DURCISSEMENT_POST_AUDIT_ERREURS_IA`, issu de l'audit du 2026-08-08. |
| Exit criteria | Un nouveau module de tests passe seul et dans la suite complete ; il echoue si le comportement WRC courant est remplace par un faux `PASS` systematique, si les IDs changent le resultat, ou si l'extension controlee de famille rend artificiellement le verdict plus favorable. |

## Question technique

Le runtime implemente deja le WRC dans
`Implementation/ebta_engine/procedures/wrc.py`, avec bootstrap stationnaire
conjoint, zero-centering, correction `(1 + exceedances)/(B + 1)` et seuil
strict `p < alpha`. Les tests existants prouvent la reproductibilite d'un cas
positif et le refus d'une famille reduite a la gagnante, mais pas le
comportement d'ensemble sous une nulle synthetique ni l'effet d'une famille
plus large construite a donnees constantes.

## Autorite et classification

- Autorite normative : SOP 02, notamment sections 6 a 9, 13 a 15 et 18 ;
  DN-008, DN-009 et DN-018.
- Classification : `TEST_FIXTURE`.
- Le seuil `alpha=0,05` vient de la norme. Les tailles de matrices, seeds et
  repetitions reduites ci-dessous sont uniquement des parametres de fixture
  versionnes pour une regression rapide ; elles ne changent aucun parametre
  d'une recherche EBTA reelle.

## Perimetre ferme

Autorise :

```text
Implementation/ebta_engine/tests/test_wrc_calibration_metamorphic.py  [CREER]
```

Interdit :

```text
Protocole/
Implementation/ebta_engine/procedures/
Implementation/ebta_engine/schemas/
Implementation/ebta_engine/governance/
Implementation/ebta_engine/validators/
Implementation/ebta_engine/manifests/
Implementation/examples/
Implementation/notebooks/
BACKTRADER/
```

## Cas de test proposes

### 1. Controle nul deterministe

- Generateur stdlib `random.Random` uniquement.
- 40 essais exterieurs, chacun avec 4 candidates independantes de 252
  observations gaussiennes de moyenne nulle.
- Seeds de donnees `0..39`, seeds bootstrap `10000..10039`.
- `replications=499`, `mean_block_length=5`, `alpha=0.05`,
  `run_secondary=False`.
- Assertion de regression : au plus 3 verdicts `PASS` sur les 40 fixtures.
- Cette assertion est un cliquet deterministe sur un jeu versionne, pas une
  estimation generale du taux de faux positifs ni un nouveau seuil EBTA.

### 2. Invariance au renommage

- Construire une matrice fixe, puis renommer uniquement les IDs des colonnes.
- Exiger l'identite de `observed_statistic`, `bootstrap_distribution`,
  `exceedance_count`, `wrc_pvalue` et `verdict`.
- Ne pas exiger l'identite de `candidate_ids` ni de `family_catalogue_hash`,
  qui doivent justement refléter les nouveaux IDs.

### 3. Extension controlee de famille

- Construire avec `random.Random(0)` une famille de base de deux candidates,
  dont une a un drift synthetique de `0.22`, puis ajouter huit candidates
  nulles independantes sans modifier les deux colonnes initiales.
- Utiliser les memes indices bootstrap via `seed=77`, `replications=499`,
  `mean_block_length=5`, `alpha=0.05`, `run_secondary=False`.
- Exiger que la p-value de la famille etendue soit superieure ou egale a
  celle de la famille de base et que le verdict ne devienne pas plus
  favorable (`FAIL` vers `PASS` interdit).
- L'assertion porte sur cette construction versionnee, pas sur un theoreme
  universel pour toute candidate ajoutee.

## Verification

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_wrc_calibration_metamorphic.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
git diff --check -- Implementation\ebta_engine\tests\test_wrc_calibration_metamorphic.py
```

## Audit intake — convergence

| Passe | Constat | Correction |
| --- | --- | --- |
| 1 | Une premiere fixture de 128 observations et bloc moyen 5 produisait 9 `PASS` sur 40 et ne pouvait soutenir le cliquet `<=3`. La premiere commande cible proposee ne respectait pas le `top-level` de la suite canonique. | Taille portee a 252 observations ; mesure directe avec 499 repetitions : 3 `PASS` sur 40, runtime inferieur a quelques secondes. La limite est documentee comme regression de fixture. La commande cible utilise desormais `unittest discover -t Implementation`. |
| 2 | Une extension arbitraire de famille n'a pas necessairement une penalite strictement croissante ; une assertion universelle serait scientifiquement trop forte. | Construction controlee figee : famille 2 candidates `p=0.046/PASS`, famille 10 candidates `p=0.174/FAIL` avec les memes deux colonnes et indices. Assertion non stricte `p_extended >= p_base`, sans nouvelle doctrine. Aucun nouvel angle mort majeur. |

## Definition of Done

- [ ] Le fichier de test nouveau est le seul fichier runtime modifie.
- [ ] Les trois controles ci-dessus sont implementes sans dependance nouvelle.
- [ ] Le test cible et la suite complete passent.
- [ ] `bug-hunter`, `adversarial-tester` et `plan-conformance-audit` ne laissent aucun finding bloquant.
- [ ] Les resultats restent presentes comme regressions deterministes, jamais comme certification scientifique generale.
