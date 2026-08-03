# INTAKE — Ingestion des veilles #14 à #18 (agent unitaire durable) et rebalayage des pratiques différées

**Statut : `INTAKE`.** Ce document est un brouillon produit par `agent-architecte`. Il n'exécute rien et n'autorise aucun `/start` automatique. Un geste humain explicite reste nécessaire pour transformer une des lignes ci-dessous en workstream.

## Position actuelle

Les veilles #1 à #13 (ledger `2026-07.md`, désormais `CLOSED`, hash `ca1afd7a5e84a0fa878b80f5639c8052988da4f23cbdda5fb4b4d31e30075be7`) couvraient missions bornées, orchestration, contexte, mémoire, skills, sécurité, observabilité, évaluation, replay, SLO, dérive/canaris, sagas et runtime minimal. Cinq nouvelles veilles (#14-#18, shard `2026-08.md`, `OPEN`) prolongent directement la #13 sous le même jalon (« Jalon 3B — Agent unitaire durable ») : graphe d'exécution, état durable, contrôle humain, agents de longue durée, événementiel. Elles créent 5 nouvelles pratiques dans le ledger (`workflow_graphe`, `etat_durable`, `controle_humain`, `agents_longue_duree`, `event_driven`), toutes au palier 0 (ACTUEL) — aucune ne dépasse ses propres préconditions.

Le rebalayage des 13 pratiques déjà suivies n'a promu aucune ligne : les commits récents (`f4500bb`, `88a1613`, `a4ce82d`, `0ccc131`, `00764ec`) sont documentaires/gouvernance (conformité FREEZE, sharding du registre), pas des artefacts exécutables. Un contrôle anti-scellement de rotation sur `securite_capacites` (palier 0, citation « chaque action sensible est identifiée et classée. ») confirme l'accord avec la source, sans reréévaluation.

## Faire maintenant

Rien n'est requis en implémentation. Les 5 veilles se classent elles-mêmes `COMPRENDRE_MAINTENANT_APPLIQUER_PLUS_TARD` (#14, #15, #16) ou `CONSERVER_POUR_PLUS_TARD` (#17, #18) — verdict sur la consommation de l'édition, pas un ordre d'implémentation. Si une action à faible coût est souhaitée, chaque veille propose un unique fichier déclaratif non exécutable (`workflow_graph.yaml`, `state.yaml`, `approval.yaml`, `run.yaml`, `EBTA_EVENT_CONTRACT.yaml` sous `.ai/workflows/` ou `.ai/events/`) décrivant le workflow UX existant sans coder de moteur. Ceci reste un choix humain, pas une recommandation d'exécution immédiate de ce rapport.

## Différer

| Pratique | Raison actuelle | Signal de réouverture |
| --- | --- | --- |
| `workflow_graphe` (P1 : graphe minimal vérifiable) | Le workflow UX est normatif et documentaire, pas encore un contrat machine simulable. | Une mission EBTA réellement répétée dont les chemins succès/correction/blocage/budget doivent être simulés. |
| `etat_durable` (P1 : checkpoint et reprise) | Aucun run agentique EBTA ne dépasse aujourd'hui la durée d'un processus. | Un workflow long nécessitant réellement une reprise après interruption. |
| `controle_humain` (P1 : interruption durable) | Le contrôle humain est déjà normatif (arbitrage documenté) ; son encodage runtime n'est pas encore requis. | Un pivot à effet irréversible ou conflit d'autorité géré par un agent, pas par lecture humaine directe. |
| `agents_longue_duree` (P1 : lease et heartbeat) | Aucun agent EBTA de longue durée en production. Explicitement `CONSERVER_POUR_PLUS_TARD` par la veille source. | Un worker concurrent ou une mission dépassant plusieurs heures avec risque de double exécution. |
| `event_driven` (P1 : routeur local fiable) | Aucun flux asynchrone multi-producteurs. Explicitement `CONSERVER_POUR_PLUS_TARD` par la veille source. | Plusieurs producteurs capables de réveiller le même run, ou un besoin de découplage mesuré (débit, rétention, doublons). |

## Prochaine étape

Aucune exécution automatique. Si l'humain choisit d'avancer, la voie normale reste `/start` sur un brouillon audité désignant explicitement l'un des cinq fichiers déclaratifs proposés par les veilles — jamais ce rapport lui-même.

## Gain net

Le ledger reste pratique-centrique après le doublement de son volume (13 → 18 veilles) : chaque nouvelle veille a été rattachée à une pratique propre plutôt qu'empilée dans un audit générique, et le rebalayage confirme qu'aucune pratique existante n'a silencieusement changé de statut.

Source : `D:\Livre\Veille\IA\veille-ia-14-workflow-engineering-graphe-execution-2026-07-30-orientation-v1.md` à `veille-ia-18-event-driven-ai-2026-08-03-orientation-v1.md`, sections « Paliers de progression », « Bon timing de mise en place » et « Décision de consommation » de chacune.
