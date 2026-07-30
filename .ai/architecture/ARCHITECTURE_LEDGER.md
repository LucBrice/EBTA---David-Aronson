# Architecture Ledger — pratiques agentiques

Ce fichier est une memoire de veille et de decision architecturale. Il ne
porte aucun etat de chantier et ne remplace ni `.ai/checkpoint.json`, ni
`Implementation/Active/tracking.json`. Si un besoin d'etat d'execution
apparait ici, il doit etre route vers le cockpit existant conformement a
`.ai/checkpoint.json::relay_contract.do_not_create`.

Ethique append-only : ajouter une veille ou une revision datee ; ne pas
reecrire silencieusement une conclusion passee. Ce Markdown n'a pas le
validateur mecanique de
`Implementation/ebta_engine/validators/registry_append_only_validator.py` :
le controle anti-scellement de
`.agents/skills/agent-architecte/SKILL.md` est donc obligatoire.

Source du remplissage initial :
`0 - HUMAN START HERE/archive/20260729_PROPOSITION_FORMALISATION_WORKFLOWS_IA_ADVERSARIAL_EXPERT_PANEL.md`,
section « Audit chronologique — 13 documents de veille IA vs etat reel du
repo ». Les formulations de palier et timing ci-dessous sont citees depuis
les fichiers sous `D:\Livre\Veille\IA`.

## Registre des veilles ingerees

| ID | Date | Sujet | Fichier sous `D:\Livre\Veille\IA` | Pratiques rattachees | Ingestion |
| --- | --- | --- | --- | --- | --- |
| V01 | 2026-07-17 | Assistant vers travailleur autonome | `veille-ia-1-assistant-vers-travailleur-autonome-2026-07-17-progression-capacitaire.md` | missions bornees ; specialisation ; supervision | 2026-07-29 |
| V02 | 2026-07-19 | Orchestration programmable et preuves | `veille-ia-2-orchestration-programmable-et-preuves-2026-07-19-progression-capacitaire.md` | gates deterministes ; registre de preuves | 2026-07-29 |
| V03 | 2026-07-20 | Superviser une equipe d'agents | `veille-ia-3-superviser-une-equipe-agents-2026-07-20-progression-capacitaire.md` | skills ; roles complementaires ; supervisor pattern | 2026-07-29 |
| V04 | 2026-07-21 | Contexte d'execution | `veille-ia-4-contexte-execution-2026-07-21-progression-capacitaire.md` | contrat de mission ; contexte minimal ; reproductibilite | 2026-07-29 |
| V05 | 2026-07-22 | Gouvernance et securite par capacites | `veille-ia-5-gouvernance-et-securite-par-capacites-2026-07-22-progression-capacitaire.md` | permissions minimales ; Policy Engine | 2026-07-29 |
| V06 | 2026-07-23 | Memoire operationnelle et amelioration continue | `veille-ia-6-memoire-operationnelle-et-amelioration-continue-2026-07-23-progression-capacitaire.md` | incidents ; regressions ; protection executable | 2026-07-29 |
| V07 | 2026-07-24 | Observabilite des agents | `veille-ia-7-observabilite-agents-2026-07-24-progression-capacitaire.md` | traces ; provenance | 2026-07-29 |
| V08 | 2026-07-25 | Evaluation continue des agents | `veille-ia-8-evaluation-continue-des-agents-2026-07-25-progression-capacitaire.md` | cas critiques ; baseline ; graders | 2026-07-29 |
| V09 | 2026-07-26 | Replay causal des incidents | `veille-ia-9-replay-causal-des-incidents-2026-07-26-progression-capacitaire.md` | incident package ; record/replay | 2026-07-29 |
| V10 | 2026-07-27 | SLO pour systemes d'agents | `veille-ia-10-slo-systemes-agents-2026-07-27-progression-capacitaire.md` | SLI ; SLO ; budgets d'erreur | 2026-07-29 |
| V11 | 2026-07-28 | Derive et canaris agentiques | `veille-ia-11-derive-canaris-agents-2026-07-28-progression-capacitaire.md` | shadow ; canari ; promotion | 2026-07-29 |
| V12 | 2026-07-29 | Sagas et compensation | `veille-ia-12-sagas-compensation-agents-2026-07-29-progression-capacitaire.md` | classes d'effet ; idempotence ; compensation | 2026-07-29 |
| V13 | 2026-07-29 | Agent minimal bout-en-bout | `veille-ia-13-agent-minimal-bout-en-bout-2026-07-29.md` | contrat de mission ; boucle agentique | 2026-07-29 |

## Registre des pratiques

| Pratique | Palier atteint, citation source | Veilles | Disposition | Condition de declenchement, citation source | Reevaluation | Historique bref |
| --- | --- | --- | --- | --- | --- | --- |
| Missions bornees et supervision | « une mission peut être décrite avec un objectif, des entrées, un livrable et des limites. » | V01, V04 | integree | « Quand une mission est répétitive, documentable, mesurable et suffisamment stable pour être confiée à un exécutant supervisé. » | 2026-07-29 | Initial : plans structures et validation humaine. |
| Orchestration et preuves deterministes | « aucun verdict critique ne dépend uniquement d’un texte généré. » | V02 | integree | « Quand les mêmes appels d’outils, calculs ou validations se répètent et consomment inutilement des tokens ou du temps humain. » | 2026-07-29 | Initial : gates, schemas, tests et artefacts EBTA. |
| Skills et roles complementaires | « la procédure possède des entrées, des étapes, une sortie et une checklist. » | V03 | reconsideree | « Quand un seul agent supervisé suffit encore ou que les procédures n’ont jamais été stabilisées. » | 2026-07-29 | Skills specialises retenus ; flotte multi-agents differee. |
| Contexte d'execution versionne | « deux personnes peuvent comprendre la mission sans explication orale supplémentaire. » | V04 | integree | « Quand les erreurs proviennent de fichiers manquants, de règles oubliées, d’outils mal choisis ou de permissions trop larges. » | 2026-07-29 | Bootstrap et cockpit presents ; workflows formalises par le lot courant. |
| Securite par capacites et Policy Engine | « chaque action sensible est identifiée et classée. » | V05 | differee | « Avant de donner un accès en écriture, de connecter des outils externes ou d’automatiser une action ayant un coût réel. » | 2026-07-29 | Gouvernance en prose presente ; moteur de policy non justifie. |
| Memoire operationnelle et protection executable | « une erreur connue déclenche automatiquement une détection ou un blocage. » | V06 | integree | « Quand plusieurs incidents révèlent des causes répétitives et que les règles existantes peuvent être versionnées. » | 2026-07-29 | Tests, bug-hunter et adversarial-tester portent les incidents confirmes. |
| Observabilite agentique | « une mission peut être reconstruite manuellement à partir de ses événements. » | V07 | differee | « Quand les workflows comportent plusieurs outils, agents, retries, artefacts ou décisions difficiles à reconstruire. » | 2026-07-29 | Sessions supervisees encore reconstructibles sans trace distribuee. |
| Evaluation continue | « chaque cas possède une mission, des résultats attendus et des interdictions. » | V08 | differee | « Dès qu’un comportement doit être conservé malgré des changements de modèle, prompt, Skill, outil ou politique. » | 2026-07-29 | Couche deterministe presente ; trajectoires agentiques repetees absentes. |
| Replay causal | « Une personne peut expliquer la chronologie d’un incident et identifier les éléments nécessaires à une relance. » | V09 | differee | « une régression est détectée mais sa cause reste ambiguë » | 2026-07-29 | Incidents actuels diagnosticables par git, tests et lecture. |
| SLO agentiques | « chaque mission critique peut être reliée à son résultat, ses preuves et ses versions. » | V10 | hors scope actuel | « Le sujet devient utile lorsqu’une même classe de mission revient régulièrement, que plusieurs versions doivent être comparées, ou que les erreurs imposent déjà des revues manuelles. » | 2026-07-29 | Aucun service agentique continu mesurable. |
| Derive, shadow et canaris | « une mission peut être rejouée et attribuée à une version exacte. » | V11 | hors scope actuel | « Les régressions connues sont couvertes, les missions sont classées, les SLO existent, les effets externes peuvent être neutralisés et une version stable peut servir de contrôle. » | 2026-07-29 | Pas de versions d'agent deployee controle/candidate. |
| Sagas et compensation | « chaque outil d’écriture possède une classe d’effet explicite. » | V12 | differee | « Le workflow traverse plusieurs services ou artefacts, certaines étapes peuvent réussir avant qu’une autre échoue, et les traces permettent déjà de savoir ce qui s’est passé. » | 2026-07-29 | Processus local sequentiel ; classification future possible si ecritures externes. |
| Runtime d'agent minimal | « trois missions représentatives peuvent être exécutées et expliquées étape par étape. » | V13 | hors scope actuel | « La mission exige parfois de choisir entre plusieurs opérations autorisées, de vérifier un résultat intermédiaire ou de s’arrêter selon une observation du monde. » | 2026-07-29 | Codex ou Claude Code fournit deja la boucle supervisee. |

## Revisions et controles anti-scellement

| Date | Pratique | Motif | Source relue | Conclusion |
| --- | --- | --- | --- | --- |
| 2026-07-29 | Memoire operationnelle et protection executable | Initialisation et controle de rotation n°1 | `D:\Livre\Veille\IA\veille-ia-6-memoire-operationnelle-et-amelioration-continue-2026-07-23-progression-capacitaire.md` | Accord : le palier et le timing cites correspondent a la source. |

Compteur total de veilles ingerees : **13**. Aucune entree purgee. Seuil de
relecture forcee : **3 invocations** sans reevaluation d'une pratique.
