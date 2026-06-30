# Cockpit IA EBTA

`.ai/` est le cockpit IA unique du repository EBTA.

## Roles

- `checkpoint.json` porte l'etat courant machine-verifiable.
- `checkpoint.schema.json` valide la forme du checkpoint.
- `../0 - HUMAN START HERE/` recoit les idees, brouillons et plans bruts.
- `backlog/` contient les chantiers tries et auditables.
- `governance/` contient les politiques de transformation, de conflit et de
  checklist avant modification par IA.
- `archive/` conserve les chantiers termines, rejetes ou remplaces.
- `tools/plan.ps1` est le backend mecanique appele par l'IA apres audit.

## Regle de source de verite

- `Protocole/` reste l'autorite normative EBTA.
- `Implementation/` reste la traduction executable du protocole.
- `Implementation/Active/` reste le cockpit micro du runtime actif.
- `.ai/` gere seulement l'organisation IA, les chantiers macro et la gouvernance
  de modification. `.ai/governance/` n'est pas une autorite scientifique EBTA.
- `0 - HUMAN START HERE/` reste le point d'entree humain, hors cockpit IA.
- `.agents/` n'est pas une source d'etat projet.

## Gouvernance de modification IA

Avant toute modification normative, structurante ou impactant `Implementation/`,
l'IA doit lire `.ai/governance/AI_MODIFICATION_CHECKLIST.md`, puis appliquer les
politiques specialisees si necessaire :

- `.ai/governance/KNOWLEDGE_INTAKE_POLICY.md` pour classer une connaissance
  entrante ;
- `.ai/governance/NORMATIVE_CHANGE_POLICY.md` pour toute modification de
  `Protocole/` ;
- `.ai/governance/CONFLICT_RESOLUTION_POLICY.md` pour rendre visibles les
  contradictions.

Ces fichiers encadrent le processus. Ils ne remplacent ni `Protocole/` ni
`Implementation/`.

## Cycle de vie des chantiers

Les chantiers passent par les etats suivants :

```text
INTAKE -> TRIAGED -> PLANNED -> ACTIVE -> BLOCKED/DONE/REJECTED/SUPERSEDED -> ARCHIVED
```

Un fichier depose dans `0 - HUMAN START HERE/` est toujours `INTAKE` et non executable.
L'IA doit l'auditer puis le router vers `backlog/mainline/`, `backlog/annexes/`
ou `backlog/fixes/`.

## Backend de gestion des plans

Depuis la racine du repo, l'IA peut appeler :

```powershell
# 1. Promouvoir un plan deja audite et structure.
.\.ai\tools\plan.ps1 start -Path "0 - HUMAN START HERE\MON_PLAN.md" -Track mainline -Id MON_PLAN -Title "Mon plan" -Audited

# 2. Continuer un plan deja route dans le backlog.
.\.ai\tools\plan.ps1 continue -Id MON_PLAN

# 3. Cloturer un plan et archiver son fichier.
.\.ai\tools\plan.ps1 close -Id MON_PLAN -Outcome DONE -Reason "Plan termine"
```

`plan.ps1` n'est pas l'interface humaine principale. Il ne fait pas l'audit
semantique ; il applique le deplacement et met a jour le JSON une fois l'audit
fait par l'IA. `start` exige `-Audited` et refuse un plan sans checklist
Markdown, `Track`, `Lifecycle`, `Scope`, `Non-goals`, `Source` et
`Exit criteria`.

## Commandes conversationnelles

L'humain peut aussi taper ces commandes directement dans l'IA :

```text
/start "0 - HUMAN START HERE/MON_PLAN.md"
/continue MON_PLAN
/close MON_PLAN
```

Contrat d'interpretation par l'IA :

- `/start` signifie : lire le plan brut humain, l'auditer, le structurer si
  besoin, choisir `mainline`, `annexe` ou `fix`, puis appeler
  `.ai/tools/plan.ps1 start -Audited`. Le fichier humain peut etre brouillon ;
  c'est l'IA qui le rend conforme avant promotion.
- `/continue` signifie : retrouver l'id dans `.ai/checkpoint.json`, passer le
  chantier en `ACTIVE`, puis reprendre le fichier de plan associe.
- `/close` signifie : retrouver l'id dans `.ai/checkpoint.json`, verifier les
  criteres de sortie, puis appeler `.ai/tools/plan.ps1 close`.

Si la commande est ambigue, l'IA doit d'abord inspecter `0 - HUMAN START HERE/` et
`.ai/checkpoint.json`. Elle ne demande une precision a l'humain que si plusieurs
choix restent plausibles.

## Fichiers retires du flux actif

- `.ai/archive/current_plan_legacy.md` conserve l'ancien resume humain.
- Le flux actif lit maintenant `.ai/README.md`, puis `.ai/checkpoint.json`.
