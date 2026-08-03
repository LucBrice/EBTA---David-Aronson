# Architecture Ledger — pratiques agentiques

Ce fichier est une memoire de veille et de decision architecturale. Il ne
porte aucun etat de chantier et ne remplace ni `.ai/checkpoint.json`, ni
`Implementation/Active/tracking.json`. Si un besoin d'etat d'execution
apparait ici, il doit etre route vers le cockpit existant conformement a
`.ai/checkpoint.json::relay_contract.do_not_create`.

Ethique append-only : ajouter une veille au shard `OPEN` ou une revision
datee dans ce ledger ; ne pas reecrire silencieusement une conclusion
passee. Ces Markdown n'ont pas le validateur mecanique de
`Implementation/ebta_engine/validators/registry_append_only_validator.py` :
le controle anti-scellement de
`.agents/skills/agent-architecte/SKILL.md` est donc obligatoire.

Source du remplissage initial :
`0 - HUMAN START HERE/archive/20260729_PROPOSITION_FORMALISATION_WORKFLOWS_IA_ADVERSARIAL_EXPERT_PANEL.md`,
section « Audit chronologique — 13 documents de veille IA vs etat reel du
repo ». Les echelles de palier sont reprises telles quelles depuis la
section « Paliers de progression » de chaque veille sous
`D:\Livre\Veille\IA`, une echelle par veille/pratique.

## Comment lire ce ledger

Chaque veille source definit sa propre echelle de paliers (Palier 0 a Palier
3 ou 4 selon la veille), avec pour chaque palier un titre et un critere de
passage cite mot pour mot. Le repo occupe **un seul palier par pratique** :
celui dont le critere de passage correspond exactement au constat deja
verifie. Rien n'est reevalue ici ; ce fichier ne fait que reprojeter une
position deja etablie dans le registre precedent.

- **Table A — Vue synthetique** : une ligne par pratique, pour un scan
  rapide. Ne contient aucune citation — seulement des nombres et des titres.
  En cas de doute sur une valeur, la source unique de verite est Table B.
- **Table B — Echelle complete (source unique des citations)** : une ligne
  par (pratique, palier), du Palier 0 au dernier palier de la veille source,
  chacune avec son critere de passage cite mot pour mot et un statut
  `ATTEINT` / `ACTUEL` / `A_VENIR`. C'est la seule table a modifier si un
  palier est reevalue ; Table A doit alors etre resynchronisee.

`id` identifie une pratique par son theme (`missions_bornees`,
`observabilite`, ...), pas par un palier global — il n'y a plus de
hierarchie de paliers commune a toutes les pratiques depuis que chaque
veille porte sa propre echelle.

Une reevaluation (changement de statut) ne se fait qu'en reprenant le
critere **au mot pres** dans la veille source, comme l'exige
`.agents/skills/agent-architecte/SKILL.md` (etape 6, controle
anti-substitution).

## Index des veilles ingerees

Le detail individuel des veilles est conserve integralement dans des shards
mensuels sous `.ai/architecture/ledger_veilles/`. Leur inventaire et leurs
controles d'integrite sont portes par
[`ledger_veilles/MANIFEST.md`](ledger_veilles/MANIFEST.md).

Le chemin de lecture courant d'`agent-architecte` derive directement le
shard actif `ledger_veilles/YYYY-MM.md`. Les shards clos et le manifeste
complet ne sont relus qu'en cas de recherche historique, de reevaluation qui
l'exige ou de controle d'integrite.

## Table A — Vue synthetique (aucune citation, voir Table B pour le detail)

| id | pratique | veille | palier_actuel / palier_max | prochain_palier_titre | reevaluation |
| --- | --- | --- | --- | --- | --- |
| missions_bornees | Missions bornees et supervision | V01 | 0 / 3 | Un agent specialise et supervise | 2026-07-29 |
| orchestration_preuves | Orchestration et preuves deterministes | V02 | 2 / 3 | Orchestration multi-agents gouvernee | 2026-07-29 |
| contexte_execution | Contexte d'execution versionne | V04 | 0 / 3 | Contexte d'execution minimal | 2026-07-29 |
| memoire_operationnelle | Memoire operationnelle et protection executable | V06 | 2 / 4 | Boucle d'amelioration gouvernee | 2026-07-29 |
| skills_roles | Skills et roles complementaires | V03 | 0 / 3 | Skill unique versionne | 2026-07-29 |
| securite_capacites | Securite par capacites et Policy Engine | V05 | 0 / 3 | Permissions statiques minimales | 2026-07-29 |
| observabilite | Observabilite agentique | V07 | 0 / 3 | Instrumentation d'un workflow critique | 2026-07-29 |
| evaluation_continue | Evaluation continue | V08 | 0 / 4 | Suite rejouable locale | 2026-07-29 |
| replay_causal | Replay causal | V09 | 0 / 4 | Incident Package manuel | 2026-07-29 |
| sagas_compensation | Sagas et compensation | V12 | 0 / 4 | Version minimale utile | 2026-07-29 |
| slo | SLO agentiques | V10 | 0 / 4 | Version minimale utile | 2026-07-29 |
| derive_canaris | Derive, shadow et canaris | V11 | 0 / 4 | Shadow minimal | 2026-07-29 |
| runtime_minimal | Runtime d'agent minimal | V13 | 0 / 4 | Version minimale utile | 2026-07-29 |
| workflow_graphe | Workflow engineering et graphe d'execution | V14 | 0 / 4 | Graphe minimal verifiable | 2026-08-03 |
| etat_durable | State management et execution durable | V15 | 0 / 4 | Checkpoint et reprise | 2026-08-03 |
| controle_humain | Human-in-the-loop comme architecture de controle | V16 | 0 / 3 | Une interruption durable | 2026-08-03 |
| agents_longue_duree | Long-running agents | V17 | 0 / 4 | Lease et heartbeat locaux | 2026-08-03 |
| event_driven | Event-driven AI | V18 | 0 / 4 | Routeur local fiable | 2026-08-03 |

### Dependances inter-pratiques citees explicitement

| id | prereq_ids | citation source (V11, section « Bon moment ») |
| --- | --- | --- |
| derive_canaris | memoire_operationnelle, missions_bornees, slo, sagas_compensation | « Les régressions connues sont couvertes, les missions sont classées, les SLO existent, les effets externes peuvent être neutralisés et une version stable peut servir de contrôle. » |

Aucune autre pratique n'a de `prereq_ids` : toutes les autres conditions de
declenchement (Table B) attendent un evenement du repo, pas un autre noeud
de ce ledger.

## Table B — Echelle complete par pratique (source unique des citations)

Statut : `ATTEINT` = en dessous ou egal au palier courant ; `ACTUEL` = palier
courant (repris dans Table A) ; `A_VENIR` = au-dessus du palier courant.

| id | palier | titre_palier | critere_passage_citation | statut |
| --- | --- | --- | --- | --- |
| missions_bornees | 0 | Clarifier le travail a deleguer | « une mission peut être décrite avec un objectif, des entrées, un livrable et des limites. » | ACTUEL |
| missions_bornees | 1 | Un agent specialise et supervise | « la mission est répétée avec une qualité suffisamment stable. » | A_VENIR |
| missions_bornees | 2 | Petite equipe d'agents | « les erreurs de coordination sont mesurées et les responsabilités restent compréhensibles. » | A_VENIR |
| missions_bornees | 3 | Organisation agentique gouvernee | « chaque décision importante est reconstructible et chaque action irréversible est contrôlée. » | A_VENIR |
| orchestration_preuves | 0 | Identifier les operations deterministes | « chaque calcul, filtre ou gate possède une spécification testable. » | ATTEINT |
| orchestration_preuves | 1 | Script d'orchestration local | « le script reproduit le workflow sans intervention manuelle sur plusieurs cas. » | ATTEINT |
| orchestration_preuves | 2 | Registre de preuves et gates | « aucun verdict critique ne dépend uniquement d'un texte généré. » | ACTUEL |
| orchestration_preuves | 3 | Orchestration multi-agents gouvernee | « les agents peuvent se contredire, mais seuls les gates autorisent l'avancement. » | A_VENIR |
| contexte_execution | 0 | Contrat de mission | « deux personnes peuvent comprendre la mission sans explication orale supplémentaire. » | ACTUEL |
| contexte_execution | 1 | Contexte d'execution minimal | « l'agent réussit sans charger un contexte massif ou contradictoire. » | A_VENIR |
| contexte_execution | 2 | Contexte versionne et observable | « une exécution peut être reproduite et comparée. » | A_VENIR |
| contexte_execution | 3 | Plateforme de contexte gouvernee | « le système fournit le minimum de contexte utile tout en conservant une preuve complète. » | A_VENIR |
| memoire_operationnelle | 0 | Capturer les incidents | « les incidents importants sont décrits de manière comparable. » | ATTEINT |
| memoire_operationnelle | 1 | Lessons learned manuelles | « les leçons sont consultées lors des missions suivantes. » | ATTEINT |
| memoire_operationnelle | 2 | Protection executable | « une erreur connue déclenche automatiquement une détection ou un blocage. » | ACTUEL |
| memoire_operationnelle | 3 | Boucle d'amelioration gouvernee | « les modifications peuvent être évaluées contre une baseline. » | A_VENIR |
| memoire_operationnelle | 4 | Boucle semi-autonome | « aucune auto-amélioration ne peut contourner les politiques ni dégrader les suites de régression. » | A_VENIR |
| skills_roles | 0 | Procedure explicite | « la procédure possède des entrées, des étapes, une sortie et une checklist. » | ACTUEL |
| skills_roles | 1 | Skill unique versionne | « le Skill produit des résultats cohérents sur plusieurs missions. » | A_VENIR |
| skills_roles | 2 | Deux roles complementaires | « les désaccords sont exploitables et ne créent pas une boucle infinie. » | A_VENIR |
| skills_roles | 3 | Supervisor Pattern | « chaque agent a une responsabilité distincte et une performance mesurable. » | A_VENIR |
| securite_capacites | 0 | Inventaire des actions | « chaque action sensible est identifiée et classée. » | ACTUEL |
| securite_capacites | 1 | Permissions statiques minimales | « les missions courantes fonctionnent sans permissions générales. » | A_VENIR |
| securite_capacites | 2 | Policy Engine centralise | « aucune action critique ne dépend d'une règle cachée dans un prompt. » | A_VENIR |
| securite_capacites | 3 | Defense en profondeur | « une compromission locale ne permet pas une escalade globale. » | A_VENIR |
| observabilite | 0 | Identifiants et taxonomie | « une mission peut être reconstruite manuellement à partir de ses événements. » | ACTUEL |
| observabilite | 1 | Instrumentation d'un workflow critique | « le premier point d'échec peut être localisé sans relire tous les logs. » | A_VENIR |
| observabilite | 2 | Collecte et visualisation centralisees | « les métriques produisent des alertes réellement actionnables. » | A_VENIR |
| observabilite | 3 | Provenance et boucle fermee | « un échec peut être localisé, expliqué, reproduit et transformé en test. » | A_VENIR |
| evaluation_continue | 0 | Cas critiques definis | « chaque cas possède une mission, des résultats attendus et des interdictions. » | ACTUEL |
| evaluation_continue | 1 | Suite rejouable locale | « deux versions peuvent être comparées dans le même environnement. » | A_VENIR |
| evaluation_continue | 2 | Graders multiples et CI | « une régression critique bloque automatiquement une version candidate. » | A_VENIR |
| evaluation_continue | 3 | Jeux geles, vivant et canari | « le système apprend des incidents sans déplacer constamment la baseline. » | A_VENIR |
| evaluation_continue | 4 | Evaluation continue de l'organisation | « toute modification de modèle, Skill, outil ou Policy produit un verdict comparatif auditable. » | A_VENIR |
| replay_causal | 0 | Preconditions | « Une personne peut expliquer la chronologie d'un incident et identifier les éléments nécessaires à une relance. » | ACTUEL |
| replay_causal | 1 | Incident Package manuel | « L'échec est reproduit de manière suffisamment fréquente ou l'absence de reproduction est quantifiée. » | A_VENIR |
| replay_causal | 2 | Replay automatise | « Le replay s'exécute automatiquement dans la CI et produit un verdict reproductible. » | A_VENIR |
| replay_causal | 3 | Replay contrefactuel cible | « Une intervention ciblée réduit significativement le taux d'échec et explique mieux les observations que les hypothèses concurrentes. » | A_VENIR |
| replay_causal | 4 | Boucle d'incident semi-autonome | « Le système peut proposer une protection, démontrer qu'elle corrige l'incident sans créer de régression, puis attendre l'autorisation appropriée. » [†] | A_VENIR |
| sagas_compensation | 0 | Preconditions | « chaque outil d'écriture possède une classe d'effet explicite. » | ACTUEL |
| sagas_compensation | 1 | Version minimale utile | « une interruption après chaque étape peut être reprise sans duplication. » | A_VENIR |
| sagas_compensation | 2 | Industrialisation | « les compensations échouées sont détectées, prouvées et escaladées. » | A_VENIR |
| sagas_compensation | 3 | Architecture avancee | « les scénarios de panne partielle respectent les invariants sur plusieurs services. » | A_VENIR |
| sagas_compensation | 4 | Boucle autonome | « les décisions automatiques reproduisent les décisions validées sur un jeu d'incidents gelé. » | A_VENIR |
| slo | 0 | Preconditions | « chaque mission critique peut être reliée à son résultat, ses preuves et ses versions. » | ACTUEL |
| slo | 1 | Version minimale utile | « une baseline couvre assez de missions pour observer les taux d'échec, délais et coûts réels. » | A_VENIR |
| slo | 2 | Industrialisation | « les alertes déclenchent des décisions reproductibles et les écarts sont investigables via traces et artefacts. » | A_VENIR |
| slo | 3 | Architecture avancee | « toute modification de modèle, prompt, Skill ou Policy a une politique de promotion et de repli mesurée. » | A_VENIR |
| slo | 4 | Boucle autonome sous controle | « les incidents et changements passés sont convertis en tests, politiques et cas d'évaluation vivants. » | A_VENIR |
| derive_canaris | 0 | Preconditions | « une mission peut être rejouée et attribuée à une version exacte. » | ACTUEL |
| derive_canaris | 1 | Shadow minimal | « zéro effet externe et chaque divergence importante possède une trace consultable. » | A_VENIR |
| derive_canaris | 2 | Industrialisation | « plusieurs changements ont été acceptés ou refusés par le même contrat. » | A_VENIR |
| derive_canaris | 3 | Canari agentique | « les paliers 5 %, 20 % et 50 % respectent les gates sans violation critique. » | A_VENIR |
| derive_canaris | 4 | Gouvernance adaptative | « les décisions automatiques reproduisent les décisions validées sur plusieurs changements. » | A_VENIR |
| runtime_minimal | 0 | Preconditions | « trois missions représentatives peuvent être exécutées et expliquées étape par étape. » | ACTUEL |
| runtime_minimal | 1 | Version minimale utile | « un succès, un refus et une exhaustion de budget produisent chacun un état et une preuve cohérents. » | A_VENIR |
| runtime_minimal | 2 | Industrialisation | « une régression est détectée avant promotion et une interruption reprend sans duplication. » | A_VENIR |
| runtime_minimal | 3 | Architecture avancee | « le système explique quel nœud a produit quel effet et comment récupérer après un échec. » | A_VENIR |
| runtime_minimal | 4 | Boucle autonome supervisee | « l'autonomie augmente ou diminue par des règles préenregistrées et auditables. » | A_VENIR |
| workflow_graphe | 0 | Mission et chemin nominal | « chaque étape possède une entrée, une sortie et un propriétaire. » | ACTUEL |
| workflow_graphe | 1 | Graphe minimal verifiable | « les chemins succès, correction, blocage et budget épuisé sont simulables. » | A_VENIR |
| workflow_graphe | 2 | Contrats executables | « une suite de tests vérifie chaque transition et interdit les chemins illégaux. » | A_VENIR |
| workflow_graphe | 3 | Composition de sous-graphes | « chaque sous-graphe peut être testé seul et remplacé sans modifier les invariants du parent. » | A_VENIR |
| workflow_graphe | 4 | Workflow durable | « une interruption à chaque frontière reprend sans perte ni duplication. » | A_VENIR |
| etat_durable | 0 | Etat explicite | « l'état courant d'un run peut être expliqué sans relire la conversation. » | ACTUEL |
| etat_durable | 1 | Checkpoint et reprise | « arrêter le worker à trois frontières puis obtenir le même terminal et les mêmes preuves. » | A_VENIR |
| etat_durable | 2 | Journal et replay | « supprimer la vue d'état dérivée puis la reconstruire à l'identique. » | A_VENIR |
| etat_durable | 3 | Versioning et migration | « un run V1 reprend sous la politique prévue après déploiement V2. » | A_VENIR |
| etat_durable | 4 | Execution durable industrialisee | « les scénarios crash, réseau coupé, worker remplacé et déploiement de version respectent les invariants. » | A_VENIR |
| controle_humain | 0 | Pivots explicites | « chaque pivot possède un propriétaire et un terminal de refus. » | ACTUEL |
| controle_humain | 1 | Une interruption durable | « approbation, refus, révision et expiration sont simulés sans double effet. » | A_VENIR |
| controle_humain | 2 | Supervision operable | « une demande oubliée est détectée et atteint un terminal prévu. » | A_VENIR |
| controle_humain | 3 | Autorite distribuee | « aucune approbation ne dépasse le périmètre du décideur. » | A_VENIR |
| agents_longue_duree | 0 | Mission decoupee et etat durable | « une interruption entre deux nœuds reprend sans réinterprétation. » | ACTUEL |
| agents_longue_duree | 1 | Lease et heartbeat locaux | « deux workers concurrents ne peuvent pas faire avancer simultanément le même run. » | A_VENIR |
| agents_longue_duree | 2 | Recuperation et budgets | « un crash pendant une activité est simulé, puis le terminal et les preuves restent cohérents. » | A_VENIR |
| agents_longue_duree | 3 | Operation longue supervisee | « les runs bloqués, expirés et coûteux sont visibles avant de devenir des incidents. » | A_VENIR |
| agents_longue_duree | 4 | Agents de longue duree sous gouvernance | « chaque changement d'autorité, de budget ou de plan est traçable et réversible. » | A_VENIR |
| event_driven | 0 | Contrats et taxonomie | « chaque message réel peut être classé et validé sans lire un prompt. » | ACTUEL |
| event_driven | 1 | Routeur local fiable | « doublon, redémarrage et événement invalide produisent les verdicts attendus. » | A_VENIR |
| event_driven | 2 | Pression et observabilite | « un test de surcharge respecte coûts, priorités et latence maximale. » | A_VENIR |
| event_driven | 3 | Bus multi-producteurs | « un producteur évolue sans casser ses consommateurs compatibles. » | A_VENIR |
| event_driven | 4 | Organisation reactive supervisee | « la mission collective reste attribuable et terminable malgré doublons, retard et panne partielle. » | A_VENIR |

[†] `replay_causal` palier 4 : la veille V09 nomme ce texte « critere de
maturite », pas « critere de passage » — c'est le dernier palier de son
echelle, il n'y a rien au-dessus a franchir.

## Contexte global (derive de Table A, non autoritatif)

18 pratiques suivies. Palier actuel = 0 pour 16 pratiques, = 2 pour 2
pratiques (`orchestration_preuves`, `memoire_operationnelle` — les deux
seules a avoir depasse leurs propres preconditions). Aucune pratique n'a
atteint son dernier palier.

## Revisions et controles anti-scellement

| Date | Pratique | Motif | Source relue | Conclusion |
| --- | --- | --- | --- | --- |
| 2026-07-29 | memoire_operationnelle | Initialisation et controle de rotation n°1 | `D:\Livre\Veille\IA\veille-ia-6-memoire-operationnelle-et-amelioration-continue-2026-07-23-progression-capacitaire.md` | Accord : le palier et le timing cites correspondent a la source. |
| 2026-07-30 | (format) | Passage d'un tableau plat (`disposition` globale) a l'echelle de paliers propre a chaque veille source (Table A + Table B), sur demande humaine. | `D:\Livre\Veille\IA\veille-ia-{1..13}` sections « Paliers de progression » | Aucune pratique reevaluee par ce changement de forme ; compteur de rotation non affecte. |
| 2026-07-30 | (format) | Autocritique de lisibilite (demande humaine) : suppression de la duplication des citations entre Table A et Table B (Table A n'a plus que des nombres/titres, Table B reste l'unique source des citations) ; retrait des prefixes `P00_`/`P01_`/`P02_`/`P03_` dans les `id` car ils referaient a l'ancien schema de paliers globaux, remplace par une echelle propre a chaque veille ; deplacement de la note « critere de maturite vs passage » (`replay_causal` palier 4) d'une parenthese inline vers une note de bas de tableau `[†]`. Aucune citation, palier ou condition n'a change de fond. | — | Aucune pratique reevaluee par ce changement de forme ; compteur de rotation non affecte. |
| 2026-07-30 | (format) | Extraction du registre individuel des veilles vers `ledger_veilles/2026-07.md` et ajout du manifeste de shards. | `PLAN_SHARDING_ARCHITECTURE_LEDGER` ; comparaison canonique des 13 lignes | Migration de forme uniquement : 13/13 lignes conservees, aucune pratique, citation, palier ou condition reevaluee. |
| 2026-08-03 | securite_capacites | Controle anti-scellement n°2 (rotation), avant ingestion des veilles #14-#18. | `D:\Livre\Veille\IA\veille-ia-5-gouvernance-et-securite-par-capacites-2026-07-22-progression-capacitaire-orientation-v1.md`, section « Paliers de progression » | Accord : le palier 0 et sa citation (« chaque action sensible est identifiée et classée. ») correspondent mot pour mot a la ligne du ledger. Aucun changement de statut. |
| 2026-08-03 | (toutes, rebalayage) | Rebalayage des pratiques differees a l'ingestion des veilles #14-#18 : verification si une condition de palier A_VENIR est remplie par les 5 nouvelles veilles ou par les commits recents (`f4500bb`, `88a1613`, `a4ce82d`, `0ccc131`, `00764ec`, tous documentaires/gouvernance FREEZE et sharding, aucun n'introduit d'artefact executable). | Table B de ce ledger ; `git log` recent ; contenu integral des veilles #14-#18 | Desaccord avec aucune ligne existante : aucune condition A_VENIR n'est remplie. Les veilles #14-#18 sont explicitement `COMPRENDRE_MAINTENANT_APPLIQUER_PLUS_TARD` (#14, #15, #16) ou `CONSERVER_POUR_PLUS_TARD` (#17, #18) selon leur propre section « Décision de consommation » ; aucune ne revendique une implementation deja faite dans EBTA. |
| 2026-08-03 | workflow_graphe, etat_durable, controle_humain, agents_longue_duree, event_driven | Ingestion initiale des veilles #14 a #18 (shard `2026-08.md`), 5 nouvelles pratiques creees faute de ligne existante couvrant leur echelle de paliers propre. | `veille-ia-14` a `veille-ia-18-...-orientation-v1.md`, sections « Paliers de progression » | Palier actuel = 0 (ACTUEL) pour les 5, aucune ne depasse ses propres preconditions : les veilles elles-memes constatent qu'aucun artefact machine (`workflow_graph.yaml`, `state.yaml`, `approval.yaml`, `run.yaml`, `EBTA_EVENT_CONTRACT.yaml`) n'est present sur `main` a la date de lecture. |

Compteur total de veilles ingerees : **18**. Aucune entree purgee. Seuil de
relecture forcee : **3 invocations** sans reevaluation d'une pratique.
