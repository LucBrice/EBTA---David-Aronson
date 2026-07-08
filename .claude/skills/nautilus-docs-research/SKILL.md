---
name: nautilus-docs-research
description: >
  Recherche ciblée et vérification empirique de l'API NautilusTrader
  (nautilus_trader) pour ce repo EBTA. TRIGGER — invoque CE skill avant
  d'écrire ou de documenter tout appel réel à nautilus_trader (BacktestEngine,
  Strategy, StrategyConfig, FillModel, add_venue, OrderFactory, Instrument,
  MarginModel, indicateurs, etc.), avant de modifier ou d'étendre
  adapters/nautilus_mapping.py ou adapters/nautilus_strategy_bridge.py, ou dès
  qu'une signature/classe/comportement Nautilus est sur le point d'être cité
  dans un plan, une revue ou du code — même si ça a l'air d'un détail mineur
  ou d'une signature "évidente". Ne jamais deviner ni recopier de mémoire une
  API Nautilus sans passer par ce skill d'abord. SKIP quand la discussion
  porte sur la gouvernance du pivot (faut-il utiliser Nautilus, statut D1-D6,
  arbitrage stratégique, lecture du Protocole EBTA) sans référence à une API
  concrète — ces sujets ne nécessitent aucune vérification technique et ce
  skill n'y ajoute rien.
---

# Pointeur — instructions complètes ailleurs

Ce fichier existe uniquement pour que Claude Code découvre et déclenche ce
skill automatiquement (mécanisme propre à `.claude/skills/`). **Il ne
contient aucune instruction propre.**

Les instructions complètes, l'index de documentation et le script de
vérification empirique vivent dans
`.agents/skills/nautilus-docs-research/SKILL.md` — c'est l'emplacement
cross-AI de ce repo (cf. `.agents/AGENTS.md`, même précédent que
`.agents/skills/EBTA_Protocol_Guardian/`), lisible par n'importe quelle IA
qui travaille ici, pas seulement par Claude Code.

**Dès que ce skill se déclenche : lire immédiatement
`.agents/skills/nautilus-docs-research/SKILL.md` et suivre son contenu à la
lettre.** Ne pas dupliquer ou paraphraser ses instructions ici — ce fichier
ne doit jamais devenir une deuxième source de vérité.
