# Audit de maturite — Le moteur EBTA est-il pret pour une vraie campagne de recherche quantitative ?

> Note d'intake, pas un plan. Deposee ici pour triage humain futur, suite a un
> audit technique complet du depot demande le 2026-07-13.
> Etat machine au moment de l'audit : branche `main`, HEAD `184b013`.
> Ce fichier reste `INTAKE`, non executable, tant qu'un humain ne l'a pas
> audite et route vers `.ai/backlog/`.

## Avertissement

L'etat machine (`.ai/checkpoint.json`, `Implementation/Active/tracking.json`)
affiche `DONE` / `PASS` / `110 tests PASS` partout. **Ces statuts sont vrais
structurellement mais trompeurs scientifiquement.** L'audit a lu le chemin
critique complet : chargement de donnees -> strategie -> simulation Nautilus ->
extraction -> statistiques -> gates -> validation.

---

## 1. Etat actuel du moteur

**Verdict : ce n'est pas encore un moteur de recherche. C'est un echafaudage
de gouvernance qui produit un `research_package` structurellement valide dont
le contenu scientifique est creux.**

Quatre constats detruisent l'idee d'un vrai backtest aujourd'hui :

### a) La strategie n'a aucune logique de signal
`Implementation/ebta_engine/adapters/nautilus_strategy_bridge.py::on_bar` :
- au **premier bar**, si `rule_id` est non-vide (toujours) -> **ACHETE**
  (toujours `OrderSide.BUY`) ;
- apres `horizon_bars` -> ferme la position.

Aucun calcul de liquidity sweep, engulfing, biais MTF, filtre de session, ni
direction. Les payloads E-I decrivent une strategie riche dans
`strategies/payloads.py`, mais **rien n'est evalue**. Tous les candidats
executent le meme comportement : acheter au bar 1, tenir N bars, vendre, long
uniquement. Le "backtest" est un buy-and-hold deguise.

### b) L'extraction de resultat est une reconstruction naive
`adapters/nautilus_mapping.py::extract_simulation_result` prend le premier fill
comme entree, le dernier comme sortie, puis reconstruit la NAV bar par bar
comme `starting_nav + (close - entry_price) * quantity` **pour tout le segment,
y compris apres la sortie** (bug de correction). De plus `total_costs = 0.0`
est code en dur : les frais Nautilus ne sont jamais extraits. On n'utilise ni
le portfolio, ni l'`analyzer`, ni le PnL reel de Nautilus.

### c) Le volume de donnees est un jouet
L'orchestrateur charge NASDAQ + XAUUSD, puis `_daily_sample` reduit le
1-minute a **un bar par jour** sur une fenetre de **10 jours** (~7 points par
actif), walk-forward `train=2, test=1, oos=1, K=2`. Or il existe **8 actifs en
1-minute sur toute l'annee 2020** sur `D:\TRADING\...\Data`. On dispose de
millions de barres et on en utilise sept.

### d) La robustesse ne stresse rien
Les trois scenarios `CENTRAL/PLAUSIBLE/EXTREME` recoivent **exactement les
memes donnees**, avec un seuil `minimum_mean_return = -1.0` (-100%). Aucun choc
de cout/slippage/latence. Le gate de robustesse ne peut structurellement pas
echouer.

**Peut-on executer un vrai backtest de recherche ? Non.** On peut executer un
prototype de bout-en-bout qui produit un artefact valide. La mecanique de
gouvernance est reelle ; le contenu simule ne l'est pas.

---

## 2. Audit par zones

### Solide et reellement operationnel
- `procedures/wrc.py` : White's Reality Check + SPA + Romano-Wolf + MCPM.
  Excellent, du vrai travail statistique.
- `procedures/oos_confidence_interval.py`, `bootstrap.py`, `zero_centering.py`.
- `procedures/detrending.py` (formule SOP 07 correcte, mais alimentee par des
  donnees canned — voir 3).
- `validators/*`, `schema_validation.py`, `schemas/` : rigoureux, vraies
  verifications de coherence croisee.
- `manifests/` : notarisation SHA-256 reelle et testee.
- `governance/` (G-BIAS, SOP 13) : checkers reels.
- `data/local_ohlcv.py`, `data/walk_forward.py` : reels et corrects.
- `adapters/nautilus_mapping.py` (mapping instrument/couts/barres) : reel,
  verifie contre l'API 1.230.0. C'est l'extraction (2b) qui est faible.

### Present mais trompeur / incomplet
- `adapters/nautilus_strategy_bridge.py` : stub de signal (1a). Trou noir du
  projet.
- `adapters/nautilus_mapping.py::extract_simulation_result` : NAV naive, couts
  a 0, ignore la compta Nautilus (1b).
- `risk/robustness.py` + grille orchestrateur : calcul reel mais aucun stress
  applique (1d).
- `package_builder/nautilus_research_package.py` : selection sur la moyenne des
  returns du stub ; downsampling ~7 barres ; detrending non recable.
- `examples/minimal_pilot_pipeline/build_research_package.py::_write_reports` :
  **le point le plus grave.** Le dict `gates` code en dur ~50 booleens a
  `True` et `invariant_evidence` fixe `gate_reports: {statistical: PASS,
  economic: PASS, final: PASS}`, tous les `package_stages` (jusqu'a
  `LIVE_LIMITED_STARTED`), `manifest_hash_failures: []`. Le validateur valide
  une auto-attestation, pas une preuve derivee.
- `procedures/incubation_report.py`, `monitoring.py`, `lifecycle.py`,
  `reproduction_report.py` : valident des rapports fournis en entree statique.
  Tout le cycle post-OOS (incubation -> paper trading -> deploiement -> live ->
  kill switch -> monitoring) est fictif.

### Dette structurelle / incoherences
- **Le venv Nautilus (~milliers de fichiers tiers) est commite dans le depot**
  (`Implementation/adapters/nautilus_env/venv/`). A sortir immediatement.
- `DEFAULT_DATA_ROOT` = chemin absolu Windows en dur (`local_ohlcv.py`). Non
  reproductible ailleurs.
- `document_hash: "NAUTILUS_MVP_CONFIG_HASH_PLACEHOLDER"` : le hash d'integrite
  de config est un placeholder litteral.
- Doublons de vocabulaire : `procedures/robustness.py` vs `risk/robustness.py`,
  `procedures/walk_forward.py` (validation) vs `data/walk_forward.py`
  (splitter).
- `CLAUDE.md` affirme "stdlib-only, no pyproject.toml" — desormais faux :
  pyproject.toml + numpy/pandas/nautilus_trader. La doc d'autorite a diverge.

---

## 3. Reel vs. impression de fonctionner

**Reellement execute :** WRC et secondaires, IC OOS, bootstrap, detrending (sur
ses entrees), selection de complexite, matrice de candidats, validation
schemas/manifests/invariants, checkers G-BIAS, mapping Nautilus, walk-forward
splitter, execution effective de `BacktestEngine`.

**Facade :**
- Le `status: PASS` du research_package (attestation, pas decouverte).
- La strategie (buy-and-hold quel que soit le payload).
- L'economie (NAV/couts) : reconstruction naive, couts nuls.
- La robustesse : 3 scenarios identiques, jamais bloquants.
- Le detrending du paquet Nautilus : alimente par les entrees canned du pilote,
  deconnecte de la simulation.
- L'experience "gagnant vs perdant" : prouve que le gate rejette une serie a
  return negatif (arithmetique correcte), via des fixtures concues pour que
  NASDAQ monte et XAUUSD baisse sous le stub. Ne demontre aucune discrimination
  de strategie.

**Prevu par l'architecture mais inexistant :** moteur de features/signaux,
extraction de la compta reelle Nautilus, realisme des couts, stress reel,
boucle d'incubation/monitoring/deploiement live.

---

## 4. Ecart avec un vrai moteur de recherche quantitative

Composants manquants, par gravite decroissante :
1. Moteur de signaux / features (coeur absent) — bloquant absolu.
2. Extraction fidele de la performance depuis Nautilus — bloquant.
3. Realisme des couts (frais/slippage calibres).
4. Volume de donnees (vrai 1-minute multi-mois/multi-actifs).
5. Stress de robustesse effectif.
6. Boucle de recherche reelle (candidats distincts par leur logique,
   calibration Train-only, selection OOS-safe).
7. Separation preuve/attestation (les gates doivent deriver leurs booleens).
8. Reproductibilite operationnelle (data root parametrable, hash reel, venv
   hors depot).
9. Performance/scalabilite (aujourd'hui un `subprocess` Python relance par
   segment).

---

## 5. Roadmap priorisee

### CRITIQUE
- **R1 — Vrai moteur de signaux dans la strategie.** Sans lui tout teste du
  vide. Aucune dependance ; debloque tout.
- **R2 — Extraire la performance reelle depuis Nautilus.** Depend de R1.
  Rend `economic_gate` et `detrending` valides.
- **R3 — Decoupler preuve et attestation dans `_write_reports`.** Depend de
  R1/R2. Le `PASS` redevient une decouverte auditable.

### IMPORTANT
- **R4 — Vrai volume de donnees** (retirer `_daily_sample`). Depend de R2 pour
  la perf.
- **R5 — Realisme des couts** (frais/slippage/latence calibres, sources).
- **R6 — Robustesse reellement stressee** (chocs appliques). Depend de R5.
- **R7 — Sortir le venv du depot + requirements.txt + data root parametrable +
  hash de config reel.** Independant, rapide, gros gain.

### AMELIORATION
- **R8 — Remplacer le subprocess-par-segment** par un runner in-process.
- **R9 — Consolider les doublons + realigner `CLAUDE.md`.**
- **R10 — Rendre la boucle post-OOS reelle** (seulement quand une strategie
  survit reellement a l'OOS).

---

## 6. Vision globale

- Echafaudage gouvernance/stats/validation : **~70-75%** (reellement construit,
  teste, serieux — la vraie valeur du depot).
- Capacite de moteur de recherche quantitative : **~15-20%** (coeur absent).
- Global vers "campagne robuste et reproductible" : **~20-25%**.

### Risques techniques principaux
1. **Illusion de completude** (risque n1) : tout est `DONE`/`PASS`, d'ou le
   danger d'ouvrir une vraie campagne sur un moteur creux et de "valider" du
   bruit. Le checkpoint a deja connu ce faux-positif (RISK_007).
2. **Attestation != calcul** : l'architecture laisse le pipeline ecrire ses
   propres verdicts.
3. **Reproductibilite** : chemin data en dur, hash placeholder, venv commite.
4. **Scalabilite** : subprocess-par-segment.
5. **Fidelite de simulation** : rejeter la compta Nautilus annule le benefice
   du choix de Nautilus.

### Points bloquants avant une campagne complete
1. Aucune logique de signal (R1).
2. Performance/couts non extraits de Nautilus (R2).
3. Gates auto-attestes au lieu de derives (R3).
4. Donnees jouet (R4).

Tant que R1->R4 ne sont pas levies, lancer une campagne produirait un
research_package PASS sur du bruit — le pire resultat pour un cadre dont toute
la valeur est l'honnetete statistique.

---

## Remise en question de l'architecture

La decision la plus risquee a long terme n'est pas Nautilus, c'est la
**porosite entre la couche qui calcule les preuves et celle qui les declare**.
Le pilote ecrit `gates.json` / `invariant_evidence.json` comme des documents
"tout est vrai", et le validateur les relit. C'est inverse : les gates
devraient etre des **sorties** produites par les procedures a partir des
artefacts de simulation, jamais des **entrees** redigees par le constructeur du
paquet. A renverser avant meme d'ecrire le premier vrai signal.

Second point : avoir choisi Nautilus (moteur event-driven lourd) puis
contourner sa comptabilite revient a payer le cout sans le benefice. Soit on
utilise reellement le portfolio/analyzer de Nautilus (recommande), soit un
moteur vectoriel leger suffirait a ce stade.

---

## Suite proposee

Un plan d'implementation detaille pour R1 (moteur de signaux) + R2 (extraction
reelle Nautilus), avec points d'API concrets, est depose separement :
`0 - HUMAN START HERE/PLAN_R1_R2_SIGNAUX_ET_EXTRACTION_NAUTILUS_2026-07-13.md`.
Il reste `INTAKE` jusqu'a `/start`.
