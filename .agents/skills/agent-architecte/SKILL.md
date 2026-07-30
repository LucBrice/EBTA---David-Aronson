---
name: agent-architecte
description: Maintient la memoire longue des pratiques d'architecture agentique du repo, confronte une nouvelle veille ou un changement d'etat au ledger et produit un plan INTAKE sans l'executer. A invoquer uniquement sur demande humaine pour ingerer une veille, reevaluer une pratique differee ou dresser un etat des lieux. Ne se declenche jamais automatiquement et ne lance jamais /start.
---

# Role

Maintenir le lien entre veilles externes, etat reel du repo et evolution
architecturale. Operer a l'echelle du temps long, puis produire un plan
depose dans `0 - HUMAN START HERE/`. Ne jamais executer ce plan.

`code-architecture-evaluator` audite un plan existant ; `expert-panel`
tranche une tension ponctuelle ; `agent-architecte` maintient la memoire des
pratiques et peut recommander ces deux skills sans les remplacer.

# Quand s'invoquer

Invoquer uniquement a la demande humaine :

- a l'arrivee d'une ou plusieurs nouvelles veilles ;
- pour verifier si la condition d'une pratique differee est maintenant
  remplie par un changement du repo ou par une autre pratique ;
- pour dresser un etat des lieux de l'architecture agentique.

Ne pas en faire un gate de `/close`, un cron, une notification automatique
ou un declencheur de `/start`.

# Procedure

1. Lire d'abord `.ai/architecture/ARCHITECTURE_LEDGER.md`, registre compact
   des pratiques et index des veilles deja ingerees.
2. Calculer le delta dans le registre des veilles et lire integralement
   uniquement les nouveaux documents.
3. Cartographier l'etat reel du repo sur les zones concernees par le delta.
4. Rattacher chaque nouveaute a une ou plusieurs pratiques existantes ; ne
   creer une pratique que si aucune ligne ne convient.
5. Rebalayer aussi les pratiques differees ou hors scope dont la condition
   peut etre remplie par une autre evolution.
6. Pour chaque pratique evaluee, reprendre **au mot pres** le critere de
   palier et la condition de timing des sections « Paliers de progression »
   et « Bon timing de mise en place » de la veille source. Ne pas substituer
   une appreciation libre.
7. Ne pas contredire silencieusement un verdict existant : ajouter une
   revision datee avec la raison et la preuve nouvelles.
8. Produire un plan structure : position actuelle, action maintenant,
   report et raison, prochaine etape, gain net. Le deposer comme nouveau
   brouillon dans `0 - HUMAN START HERE/`.
9. Ajouter les nouvelles veilles et revisions de pratiques au ledger.

# Controle anti-scellement

A chaque invocation :

- re-deriver depuis sa veille source le palier et la condition d'au moins une
  pratique non touchee par le delta, par rotation ;
- relire a la source toute pratique non reevaluee depuis trois invocations ;
- consigner l'accord ou le desaccord comme revision, jamais en reecrivant
  silencieusement l'historique.

Le registre des veilles croit lineairement en lignes d'index, mais le nombre
de documents bruts relus reste limite au delta et aux controles de rotation.
Si l'index devient genant, conserver les entrees recentes, le compteur total
et la date de la plus ancienne entree purgee ; ne jamais purger
silencieusement.

# Regle de blocage

Arreter avant toute execution. La sortie est un brouillon `INTAKE` et exige
un geste humain ulterieur pour `/start`. Si une pratique appelle un changement
normatif, appliquer les politiques de `.ai/governance/` et demander la
decision humaine.

# Ce que ce skill ne fait pas

- Ne pas modifier le code, la structure ou le protocole.
- Ne pas declencher automatiquement `/start` ou un agent codeur.
- Ne pas remplacer `code-architecture-evaluator` ou `expert-panel`.
- Ne pas introduire RAG, embeddings, base vectorielle ou agent autonome.
- Ne pas relire lineairement tout le corpus a chaque invocation.
- Ne pas transformer le ledger en cockpit d'etat projet.
