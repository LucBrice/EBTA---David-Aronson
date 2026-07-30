# Brouillon — formalisation exécutable des workflows

## Objectif

Faire des workflows une machine à états réellement contrôlée :

- `WORKFLOW.json` autoritatif par workflow ;
- schéma commun des contrats ;
- état workflow obligatoire dans chaque workstream du checkpoint ;
- transitions `start -> baseline -> continue -> ready -> close` vérifiées par
  `plan.ps1` ;
- preuves de gates référencées dans l'état ;
- tests négatifs des transitions interdites ;
- Mermaid généré depuis les contrats, jamais édité comme autorité.

## Décision d'architecture issue du panel

Adopter un enforcement strict pour tous les workstreams. Les historiques sont
migrés vers leur état terminal avec une preuve `legacy_import` qui dit
explicitement qu'aucune gate historique n'est ré-attestée. Le chantier courant
est migré vers son état réel. Après migration, le schéma exige `workflow` sur
chaque workstream et `plan.ps1 start` le crée toujours.

Forme d'état :

```json
{
  "id": "common",
  "contract_version": "1.0.0",
  "stage": "ACTIVE",
  "evidence": [
    {
      "id": "baseline_commit",
      "reference": "<commit>",
      "recorded_at": "2026-07-30"
    }
  ]
}
```

`plan.ps1 ready` reçoit les preuves sous la forme `id=reference`. Il vérifie
les IDs exigés par la transition du contrat ; il ne prétend pas juger la
véracité sémantique de la référence.

## États

```text
TRIAGED -> BASELINED -> ACTIVE -> READY_TO_CLOSE -> DONE
                    \-> BLOCKED/REJECTED/SUPERSEDED
```

- `start` exige au moins deux passes d'audit intake et une référence de preuve ;
- `baseline` exige au moins deux passes sur le plan et un commit existant ; il
  est appelé après le commit de baseline et sa mutation d'état est commitée
  séparément avant `/continue`;
- `continue` refuse tout état autre que `BASELINED` ;
- `ready` exige les preuves définies par le contrat ;
- `close DONE` refuse tout état autre que `READY_TO_CLOSE`.

## Contrats

- `common` actif : preuve `plan_conformance` avant `READY_TO_CLOSE`;
- `core-engine` actif : preuves `bug_hunter`, `adversarial_tester` et
  `plan_conformance` (une non-applicabilité doit être explicitement référencée) ;
- `interface` reste `PLANNED` et ne peut pas être sélectionné par `/start`.

## Périmètre fonctionnel

- ajouter contrats, schéma, module d'état, générateur Mermaid et tests ;
- étendre `plan.ps1` avec `baseline`, `ready`, `migrate-workflows`;
- migrer le checkpoint via le backend ;
- synchroniser les documents et l'index `POLICIES.md`.

Hors portée : changer `Protocole/` ou `Implementation/`, construire le workflow
interface, prouver sémantiquement qu'un audit IA a été bien conduit, ajouter une
dépendance, du RAG ou des agents autonomes.

## Vérification

- validation JSON Schema de tous les contrats et du checkpoint ;
- génération Mermaid reproductible sans diff ;
- tests positifs et négatifs du module d'état ;
- scénarios d'intégration `plan.ps1` sur un repo Git temporaire : migration
  legacy, refus de `continue` avant baseline, refus de `ready` sans preuve,
  refus de `close DONE` avant `READY_TO_CLOSE`, puis chemin nominal complet ;
- `git diff --check`.

## Journal `/evaluate`

| Passe | Résultat |
| --- | --- |
| 1 | Forme d'état et preuve fixée ; test d'intégration temporaire ajouté pour couvrir les refus réels du backend, pas seulement les helpers. |
| 2 | Convergence : séquence du commit de baseline rendue non circulaire ; migration strictement via backend ; Mermaid déclaré généré et contrôlé contre le contrat ; aucun nouvel angle mort majeur. |
