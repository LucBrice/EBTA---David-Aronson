# Inventaire d'archivage - 2026-06-26

## Statut

| Champ | Valeur |
| --- | --- |
| Etape | STEP_0_ARCHIVE_OBSOLETE |
| Statut | COMPLETE |
| Type | GOVERNANCE |
| Impact protocole | NONE |
| Hook | `Implementation/HOOK - Plan actif stabilisation archive et pipeline pilote.md` |
| Suivi JSON | `Implementation/task_tracking.json` |

## Regles appliquees

- Archive-over-delete.
- Ne pas archiver une source active.
- Verifier les references avant deplacement.
- Separations maintenues : `Protocole/Archives/` reste reserve aux archives du
  protocole, `Archives/` conserve les sources historiques hors protocole.

## Classification

| Element | Classification | Action | Preuve / justification |
| --- | --- | --- | --- |
| `Applications/` | ARCHIVE_CANDIDATE | Deplace vers `Archives/Applications_2026-06-26/` | Dossier ignore par Git, 69 notebooks/fichiers exploratoires, aucune reference active trouvee dans `Protocole/`, `Implementation/`, `.agents`, `.codex` ou `.gitignore` hors entree ignore. |
| `Notes/` | ACTIF | Conserve a sa place | Plusieurs SOP actives citent explicitement des notes comme sources de support. |
| `Protocole/Archives/` | ACTIF | Conserve a sa place | Archive documentaire officielle deja referencee par le protocole, le manifeste et la matrice. |
| `Implementation/` | ACTIF | Conserve a sa place | Runtime EBTA actif et banc de controle du lot courant. |
| `Implementation/HOOK - Reprise EBTA Engine Core autonome.md` | ARCHIVE_CANDIDATE | Deplace vers `Implementation/Archives/completed_2026-06-26/HOOK - Reprise EBTA Engine Core autonome.md` | Hook de reprise initial termine. Les pointeurs actifs ont ete corriges vers le hook actif ou vers l'archive selon le besoin. |
| `Implementation/PLAN - Procedures de calcul EBTA et optimisation ML.md` | ARCHIVE_CANDIDATE | Deplace vers `Implementation/Archives/completed_2026-06-26/PLAN - Procedures de calcul EBTA et optimisation ML.md` | Plan execute et termine. Les pointeurs de tracabilite et tests ont ete corriges vers l'archive. |
| `Implementation/implementation_context.json` | ARCHIVE_CANDIDATE | Deplace vers `Implementation/Archives/completed_2026-06-26/implementation_context.json` | Ancien contexte du lot procedures termine. Le suivi actif est `Implementation/task_tracking.json`. |
| `Implementation/HOOK - Plan actif stabilisation archive et pipeline pilote.md` | ACTIF | Conserve a sa place | Hook actif du lot archivage/checkpoint/pipeline pilote. |
| `Implementation/task_tracking.json` | ACTIF | Conserve a sa place | Suivi machine-readable actif du lot courant. |
| `Implementation/**/__pycache__/` | GENERATED_CACHE | Non archive | Cache Python recreable, sans valeur historique EBTA. A exclure des decisions d'archive documentaire. |

## References verifiees

Commandes utilisees :

```powershell
rg -n "Applications/|Applications\\|`Applications|\bApplications\b" -S Protocole Implementation .agents .codex .gitignore
rg -n "Notes/|Notes\\|`Notes|\bNotes\b" -S Protocole Implementation .agents .codex .gitignore
rg -n "HOOK - Reprise EBTA Engine Core autonome|PLAN - Procedures de calcul EBTA|implementation_context.json|HOOK - Plan actif stabilisation|task_tracking.json" -S Protocole Implementation .agents .codex
git ls-files Applications
git ls-files Notes
```

Resultat :

- `Applications/` n'etait pas suivi par Git et n'avait pas de reference active
  hors `.gitignore`.
- `Notes/` n'est pas suivi par Git mais reste cite par les SOP actives.
- Les hooks/plans/contextes termines ont ete archives apres correction des
  pointeurs actifs.

## Deplacement effectue

```text
Applications/ -> Archives/Applications_2026-06-26/
Implementation/HOOK - Reprise EBTA Engine Core autonome.md -> Implementation/Archives/completed_2026-06-26/HOOK - Reprise EBTA Engine Core autonome.md
Implementation/PLAN - Procedures de calcul EBTA et optimisation ML.md -> Implementation/Archives/completed_2026-06-26/PLAN - Procedures de calcul EBTA et optimisation ML.md
Implementation/implementation_context.json -> Implementation/Archives/completed_2026-06-26/implementation_context.json
```

Le chemin source et le chemin cible ont ete resolus et verifies comme inclus
dans le workspace avant `Move-Item`.

## Decision

`STEP_0_ARCHIVE_OBSOLETE` est complete pour ce lot. Aucun fichier normatif du
dossier `Protocole/` n'a ete deplace. Aucun element actif cite n'a ete archive.
Les hooks/plans/json termines ont ete archives et les pointeurs actifs ont ete
corriges.
