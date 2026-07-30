# Exemple de rapport — audit initial des 13 veilles IA

## Position actuelle

Le repo possede deja un cockpit machine-verifiable, des gates deterministes,
des skills specialises et une execution humaine supervisee. Il ne possede
pas de runtime multi-agents autonome, de traces distribuees ni de volume de
missions justifiant SLO, canaris ou replay causal industrialise.

## Faire maintenant

- Formaliser `adversarial-tester` pour convertir les incidents recurrents de
  faux succes en gate procedural et en regressions executables.
- Formaliser `expert-panel` pour trancher les tensions de valeurs sans
  alourdir chaque audit.
- Creer un registre des workflows et conserver un bootstrap universel mince.
- Amorcer `ARCHITECTURE_LEDGER.md` afin que les prochaines veilles soient
  comparees aux pratiques existantes plutot qu'empilees.

## Differer

| Pratique | Raison actuelle | Signal de reouverture |
| --- | --- | --- |
| Policy Engine mecanise | Les permissions et gates restent portes par la gouvernance supervisee. | Acces en ecriture externe ou action a cout reel automatisee. |
| Observabilite agentique | Aucun workflow autonome multi-outils difficile a reconstruire. | Missions avec retries, artefacts et decisions non reconstructibles. |
| Evaluation continue | Pas de trajectoires agentiques repetees comparables. | Plusieurs versions d'un meme agent a promouvoir. |
| Replay causal | Les incidents restent diagnosticables par tests, git et lecture. | Regression ambigue non reproductible par relance manuelle. |
| SLO et canaris | Aucun service agentique continu ni version candidate deployee. | Volume stable de missions et baseline comparable. |
| Sagas | Un seul processus local, pas de workflow distribue. | Ecritures partielles sur plusieurs services. |
| Runtime agent minimal | Codex/Claude Code fournit deja la boucle supervisee. | Sous-processus EBTA autonome avec choix dynamiques d'outils. |

## Prochaine etape

Executer le plan de formalisation via le cycle humain gouverne. Ne pas lancer
automatiquement `/start` depuis ce rapport.

## Gain net

La memoire devient pratique-centrique : les nouvelles veilles enrichissent ou
reevaluent des lignes existantes sans reconstruire l'audit complet.

Source :
`0 - HUMAN START HERE/archive/20260729_PROPOSITION_FORMALISATION_WORKFLOWS_IA_ADVERSARIAL_EXPERT_PANEL.md`,
section « Audit chronologique — 13 documents de veille IA vs etat reel du
repo ».
