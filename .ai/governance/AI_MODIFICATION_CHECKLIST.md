# AI Modification Checklist

## Avant toute modification

- [ ] Lire `AGENTS.md`.
- [ ] Lire `.ai/README.md`.
- [ ] Lire `.ai/checkpoint.json`.
- [ ] Lire le hook actif et le tracking actif declares dans `.ai/checkpoint.json`
      si la tache touche le runtime ou l'etat projet.
- [ ] Lire `Protocole/0-README - Comprendre et maintenir le protocole EBTA.md`
      si la tache touche le protocole, la methode, les SOP ou une decision
      scientifique.
- [ ] Identifier si la tache touche `.ai/`, `Protocole/`, `Implementation/`,
      `.agents/`, `.codex/` ou un autre dossier.
- [ ] Identifier l'autorite normative applicable.
- [ ] Verifier si le changement est documentaire, organisationnel, normatif ou
      executable.
- [ ] Verifier si un SOP fige est concerne.
- [ ] Verifier si une decision humaine est necessaire.
- [ ] Verifier si une trace doit etre ajoutee dans
      `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md`.
- [ ] Verifier si une trace doit etre ajoutee dans
      `Protocole/MATRICE DE COHERENCE DES SOP EBTA.md` ou
      `Implementation/TRACEABILITY_MATRIX.md`.
- [ ] Verifier si `.ai/checkpoint.json` doit etre mis a jour.
- [ ] Verifier si un backlog item doit etre cree, promu, ferme ou archive.
- [ ] Lire `.ai/workflows/README.md`,
      `.ai/workflows/common/WORKFLOW.json` et `WORKFLOW.md`, puis le contrat
      JSON et le Markdown specialises applicables avant toute action
      substantielle. Le `.mmd` est une vue generee, pas une autorite.

## Apres modification

- [ ] Resumer les fichiers modifies.
- [ ] Expliquer pourquoi chaque fichier a ete modifie.
- [ ] Lister les fichiers volontairement non modifies.
- [ ] Lister les conflits detectes mais non resolus.
- [ ] Lister les decisions humaines encore necessaires.
- [ ] Verifier que `.agents/` et `.codex/` ne sont pas devenus normatifs.
- [ ] Verifier que `.ai/governance/` ne contient pas de verite EBTA
      concurrente.
- [ ] Executer les validations pertinentes selon le type de changement.
- [ ] Verifier que le stage `checkpoint.workstreams[].workflow` correspond a
      l'action accomplie et que chaque reference d'evidence est honnete.
- [ ] Regenerer les Mermaid si un `WORKFLOW.json` a change et verifier
      l'idempotence.
- [ ] Si le diff touche un verdict, une ecriture persistee/append-only, une
      frontiere externe, `config.json`/G0 ou une logique derivee de
      parametres, appliquer `.agents/skills/adversarial-tester/SKILL.md` avant
      `/close` et traiter tout faux succes ou repli silencieux confirme.

## Skills de controle et de conseil

- `bug-hunter` chasse les bugs de correction et de typage du runtime selon le
  workflow `core-engine`.
- `adversarial-tester` est un gate procedural du workflow `core-engine` sur
  le pattern « succes fabrique / repli silencieux ». `plan.ps1` impose son ID
  de preuve avant `ready`, mais ne peut pas verifier le contenu du rapport.
- `plan-conformance-audit` compare les Exit criteria a la livraison avant
  toute fermeture.
- `agent-architecte` est recommande, non bloquant, lorsqu'une nouvelle veille
  IA arrive ou lorsqu'une pratique differee doit etre reevaluee. Il produit
  uniquement un brouillon `INTAKE` et ne declenche jamais `/start`.

## Modifications autorisees sans decision normative

- Ajouter ou corriger une regle de gouvernance dans `.ai/governance/`.
- Mettre a jour `.ai/README.md` pour mentionner `.ai/governance/`.
- Mettre a jour `.ai/README.md` pour referencer les registres
  `.ai/workflows/` et `.ai/architecture/` sans leur donner d'autorite
  scientifique ni d'etat projet.
- Mettre a jour `AGENTS.md` avec une regle courte de lecture de
  `.ai/governance/` avant toute modification normative ou structurante.
- Mettre a jour `.ai/checkpoint.json` si le schema existant le permet
  proprement.
- Ajouter un point de checkpoint ou de backlog indiquant que la gouvernance IA a
  ete mise en place, si cela respecte les conventions existantes.

## Modifications interdites sans decision explicite

- Reecrire le protocole EBTA.
- Reecrire les SOP.
- Changer la hierarchie scientifique du protocole.
- Deplacer `.agents/`, `.codex/`, `Protocole/` ou `Implementation/`.
- Introduire un outil RAG, des embeddings, une base vectorielle ou des agents
  autonomes.
- Ajouter des dependances techniques.
- Modifier du code d'implementation sauf si strictement necessaire pour mettre
  a jour une trace documentaire.
