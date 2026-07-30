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
   des pratiques, des revisions et du compteur global.
2. Deriver le shard du mois courant par la convention
   `.ai/architecture/ledger_veilles/YYYY-MM.md`, puis :
   - s'il existe, lire uniquement ce shard pour calculer le delta du mois ;
   - s'il n'existe pas, inspecter la derniere ligne `OPEN` de
     `.ai/architecture/ledger_veilles/MANIFEST.md`, cloturer le shard
     precedent en passant son en-tete a `CLOSED`, calculer son SHA-256
     canonique sur ce contenu final, cloturer sa ligne de manifeste, creer
     le nouveau shard et ajouter sa ligne `OPEN` ;
   - pour chaque fichier de veille fourni par l'humain, rechercher son nom
     entoure de ses delimitateurs Markdown (forme `` `nom.md` ``) avec
     `rg -F --` dans `.ai/architecture/ledger_veilles/*.md` ; un match
     existant prouve qu'il est deja ingere et interdit un doublon ;
   - lire integralement uniquement les documents sans match.
   Le mois du shard est le mois d'ingestion, pas necessairement le mois de
   la date portee par la veille : une veille ancienne soumise tardivement
   entre dans le shard `OPEN` courant.
   Le SHA-256 canonique est calcule sur le Markdown decode en UTF-8, BOM
   retire, fins de ligne normalisees en LF et une unique fin de ligne
   terminale.
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
9. Ajouter chaque nouvelle veille au shard `OPEN`, mettre a jour sa ligne de
   manifeste et le compteur global du ledger, puis ajouter les revisions de
   pratiques au ledger.

Une ingestion est une transaction au niveau du diff : la ligne du shard,
la ligne du manifeste, le compteur global et les revisions eventuelles sont
prepares ensemble, valides, puis commites ensemble. Avant tout commit,
rejouer le controle anti-scellement ci-dessous. En cas d'echec, bloquer la
sortie et corriger le patch non commite ; ne jamais publier un etat partiel
ni produire un plan `INTAKE` qui suppose l'ingestion reussie.

# Controle anti-scellement

A chaque invocation :

- re-deriver depuis sa veille source le palier et la condition d'au moins une
  pratique non touchee par le delta, par rotation ;
- relire a la source toute pratique non reevaluee depuis trois invocations ;
- consigner l'accord ou le desaccord comme revision, jamais en reecrivant
  silencieusement l'historique ;
- verifier que la somme des compteurs du manifeste egale le compteur global,
  qu'une seule ligne est `OPEN` et que le SHA-256 canonique de chaque shard
  `CLOSED` correspond a son contenu.

Un doublon, un compteur divergent, zero ou plusieurs lignes `OPEN`, ou un
hash manquant/invalide sur un shard `CLOSED` est bloquant : ne rien ajouter,
ne pas declarer l'ingestion reussie et rendre l'incoherence visible.

Ne jamais purger, tronquer, resumer ou remplacer une veille ancienne. Lire
le manifeste complet ou un shard clos uniquement pour une recherche
historique, une reevaluation qui l'exige ou le controle d'integrite ; ne pas
les charger sur le chemin courant d'une invocation.

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
