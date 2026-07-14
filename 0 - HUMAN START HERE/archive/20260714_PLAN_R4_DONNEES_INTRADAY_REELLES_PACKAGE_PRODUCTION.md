# Brouillon — R4 : donnees intraday reelles et reconciliation du candidate space de production

> Brouillon humain brut, pas encore audite ni structure. A router via
> `/start` (l'IA auditera, structurera selon
> `.ai/backlog/TEMPLATE_PLAN_IMPLEMENTATION.md`, puis appellera
> `.ai/tools/plan.ps1 start -Audited`).

## Pourquoi ce brouillon

`PLAN_R1_R2_SIGNAUX_ET_EXTRACTION_NAUTILUS.md` (desormais
`.ai/archive/20260713_...`, cloture `DONE`) nommait explicitement R4 comme
suite necessaire (section 13, Cloture, "Suites a prevoir") : "retrait
`_daily_sample`, vraies donnees intraday". R1/R2 a construit tout le
moteur de signaux incremental (`strategies/registry.py`,
`strategies/incremental/payload_{e,f,ghi}.py`, oracle vectorise dans
`strategies/signals/`) et a delibere laisse `nautilus_research_package.py`
(le chemin de production du package MVP) hors perimetre — Non-goal
explicite du plan R1/R2 : "Ne pas brancher dans
`nautilus_research_package.py` (chemin de production) tant que R4 n'est
pas resolu".

Resultat actuel : le moteur de signaux qu'on vient de construire et de
corriger n'est utilise par **aucun** package de production. Ca vaut la
peine d'etre resolu maintenant, tant que le contexte de R1/R2 est frais.

## Constat concret (verifie dans le code, pas suppose)

1. `package_builder/nautilus_research_package.py:411-417`,
   `_daily_sample()` : reduit chaque jour de barres M1 a une seule barre
   (la premiere de la journee) avant de construire les folds walk-forward.
   Consequence directe : aucune donnee intraday n'atteint jamais le
   pipeline de production — incompatible avec les signaux R1/R2, qui
   dependent tous de la granularite M1 (sweeps de liquidite, patterns
   engulfing, fenetres de session).

2. `package_builder/nautilus_research_package.py:85-93`, l'espace de
   candidats de production est parametre par
   `{"bias_filter": ["none", "directional_mtf_bias"], "session": ["all",
   "asia", "london", "us"]}`, associe a des `StrategyPayload` via
   `(asset, bias_filter, session)` — un schema de parametrage entierement
   distinct des codes de payload E/F/G/H/I du nouveau registry
   (`strategies/registry.py`). Il n'est pas etabli si ce candidate space
   route reellement, au bout de la chaine, vers le nouveau moteur
   incremental ou vers un mecanisme anterieur a R1/R2 — a verifier
   pendant l'audit `/start` avant de figer le perimetre du plan.

## Ce que ce brouillon NE fait PAS

- Il ne propose pas de solution technique arretee (comment reechantillonner,
  quelle taille de fold, quel candidate space final) — c'est le travail du
  plan une fois audite et structure, pas de ce brouillon.
- Il ne dit pas si le candidate space de production doit migrer
  integralement vers les codes E/F/G/H/I du registry ou coexister avec le
  schema `bias_filter`/`session` actuel — question a trancher a l'audit.
- Il ne touche a aucun fichier — brouillon en lecture seule sur l'etat du
  code.

## Question ouverte pour l'humain (a trancher avant ou pendant `/start`)

Le schema de candidats de production (`bias_filter`/`session`) doit-il
etre remplace par les codes de payload du registry R1/R2 (E/F/G/H/I), ou
les deux schemas doivent-ils coexister le temps d'une transition ? C'est
une decision de perimetre, pas un detail d'implementation — elle change
la taille du plan.

## Reference

- Plan source : `.ai/archive/20260713_PLAN_R1_R2_SIGNAUX_ET_EXTRACTION_NAUTILUS.md`,
  section 13 (Cloture) et section 1 (Non-objectifs, "brancher dans
  `nautilus_research_package.py`... tant que R4 n'est pas resolu").
- Code concerne : `Implementation/ebta_engine/package_builder/nautilus_research_package.py`.
