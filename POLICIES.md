# Index déclaratif des autorisations IA

Ce fichier facilite la consultation des règles existantes. Il n'est ni une
autorité scientifique EBTA, ni un Policy Engine, ni une source d'état projet.
Il ne crée aucune autorisation et ne garantit aucun blocage mécanique.

Valeurs fermées de la colonne `Autorisée ?` :

- `OUI` : l'action est autorisée sans décision supplémentaire, sous les
  conditions citées ;
- `CONDITIONNELLE` : l'action exige les conditions et validations indiquées ;
- `NON` : l'action décrite est interdite dans ce mode.

En cas de divergence, la source propriétaire citée prime toujours. L'index doit
alors être corrigé ; il ne peut jamais servir à contourner une règle plus
précise.

| Action | Autorisée ? | Conditions | Validation requise | Source propriétaire |
| --- | --- | --- | --- | --- |
| Exécuter directement un brouillon de `0 - HUMAN START HERE/` | NON | Un brouillon est `INTAKE` et non exécutable. | Le promouvoir par `/start` avant toute implémentation. | `AGENTS.md`; `.ai/workflows/common/WORKFLOW.md` |
| Promouvoir un brouillon avec `/start` | CONDITIONNELLE | Demande humaine, double boucle `/evaluate`, plan réécrit dans le backlog et audit `-Audited`. | Sections du gabarit, checkpoint/schema puis baseline pré-implémentation. | `.ai/workflows/common/WORKFLOW.md` |
| Reprendre un plan avec `/continue` | CONDITIONNELLE | Workstream route, baseline présente et test `epic-orchestrator` rejoué. | Respect de la carte d'exécution et du workflow spécialisé. | `.ai/workflows/common/WORKFLOW.md` |
| Fermer un plan avec `/close` | CONDITIONNELLE | Tous les gates du workflow spécialisé et les Exit criteria sont satisfaits, ou outcome bloqué explicitement justifié. | JSON d'état validés puis commit limité à la clôture ; jamais de push automatique. | `.ai/workflows/common/WORKFLOW.md`; workflow spécialisé applicable |
| Modifier `.ai/governance/` | CONDITIONNELLE | Changement procédural non scientifique, checklist lue et aucune autorité EBTA concurrente créée. | Checklist post-modification et validations pertinentes. | `.ai/governance/AI_MODIFICATION_CHECKLIST.md`; `.ai/governance/README.md` |
| Modifier `Implementation/` | CONDITIONNELLE | Scope d'un plan audité, gouvernance lue, contrat `Protocole/Implementation` préservé. | Tests, workflow `core-engine`, skills déclenchés et trace runtime si nécessaire. | `AGENTS.md`; `.ai/workflows/core-engine/WORKFLOW.md`; `.agents/skills/EBTA_Protocol_Guardian/SKILL.md` |
| Modifier `Protocole/` | CONDITIONNELLE | Tâche explicitement normative, décision humaine lorsqu'elle change doctrine, gate, statut, seuil ou définition, et procédure de nouvelle version respectée. | Registre, matrice, historique et manifeste selon l'impact. | `.ai/governance/NORMATIVE_CHANGE_POLICY.md`; `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md` |
| Mettre à jour `.ai/checkpoint.json` | CONDITIONNELLE | Utiliser `plan.ps1` pour le cycle des plans ; autre mise à jour seulement si le schéma existant le permet proprement. | Syntaxe JSON et validation contre `.ai/checkpoint.schema.json`. | `.ai/README.md`; `.ai/governance/AI_MODIFICATION_CHECKLIST.md`; `.ai/workflows/common/WORKFLOW.md` |
| Modifier BACKTRADER | CONDITIONNELLE | Gouvernance locale lue et périmètre explicite reçu ; sinon référence uniquement. | Vérifier que ses conventions ne deviennent pas des normes EBTA. | `.ai/workflows/core-engine/WORKFLOW.md` |
| Ajouter une dépendance, un outil RAG, des embeddings, une base vectorielle ou des agents autonomes | CONDITIONNELLE | Décision humaine explicite et chantier gouverné distinct obligatoires. | Vérifier dépendances, autorité, non-concurrence et périmètre approuvé avant toute écriture. | `.ai/governance/AI_MODIFICATION_CHECKLIST.md` |
| Créer la baseline pré-implémentation | CONDITIONNELLE | Plan normalisé convergé après au moins deux passes post-`/start`; fichiers machine valides. | Forme détaillée du commit et scope intentionnel. | `.ai/workflows/common/WORKFLOW.md` |
| Créer le commit automatique de clôture | CONDITIONNELLE | `plan.ps1 close` réussi et tous les JSON touchés valides. | Commit limité exactement aux fichiers de clôture. | `.ai/workflows/common/WORKFLOW.md` |
| Pousser automatiquement vers un remote | NON | Le cycle des plans n'autorise jamais un push automatique. | Une demande humaine distincte est nécessaire pour tout workflow de publication. | `.ai/workflows/common/WORKFLOW.md` |
| Appliquer un skill spécialisé | CONDITIONNELLE | Le déclencheur documenté dans son `SKILL.md` correspond à la tâche. | Suivre intégralement la procédure et son éventuelle règle de blocage. | `AGENTS.md`; `.agents/skills/*/SKILL.md` |

Cet index doit rester compact. Toute procédure détaillée appartient à sa source
propriétaire et ne doit pas être recopiée ici.
