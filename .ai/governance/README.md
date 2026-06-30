# Gouvernance IA EBTA

`.ai/governance/` decrit les regles de transformation, de validation et de
tracabilite appliquees par une IA avant de modifier le repository EBTA.

Ce dossier ne contient pas la verite scientifique EBTA. Il n'ajoute aucune
doctrine, aucun seuil, aucun gate et aucune regle statistique. Il encadre
seulement la maniere dont une connaissance, une note, une contradiction ou une
demande de changement peut etre analysee avant de devenir, eventuellement, une
modification fiable.

## Autorites

- `Protocole/` reste l'autorite normative EBTA.
- `Implementation/` reste la traduction executable derivee du protocole.
- `.ai/checkpoint.json` reste l'etat courant machine-verifiable du cockpit IA.
- `.ai/` orchestre les chantiers et les decisions de routage, sans remplacer le
  protocole.
- `.agents/` et `.codex/` restent des helpers ou adaptateurs non normatifs.

## Role des fichiers

- `KNOWLEDGE_INTAKE_POLICY.md` definit comment classer une connaissance entrante.
- `NORMATIVE_CHANGE_POLICY.md` definit quand et comment `Protocole/` peut etre
  modifie.
- `CONFLICT_RESOLUTION_POLICY.md` definit comment rendre visibles les
  contradictions sans les resoudre silencieusement.
- `AI_MODIFICATION_CHECKLIST.md` fournit la checklist operationnelle avant et
  apres modification par IA.

## Tracabilite attendue

Une decision normative doit etre reliee aux registres actifs du protocole,
notamment `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md`,
`Protocole/MATRICE DE COHERENCE DES SOP EBTA.md`,
`Protocole/HISTORIQUE DES VERSIONS EBTA.md` et
`Protocole/MANIFESTE DE GEL EBTA.md` lorsque le changement l'exige.

Un impact executable doit etre relie a `Implementation/TRACEABILITY_MATRIX.md`
et, si le changement est significatif, a
`Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`.

Si un registre attendu manque dans une future version du repo, l'IA doit le
signaler comme amelioration a creer au lieu d'inventer une source concurrente
dans `.ai/governance/`.

