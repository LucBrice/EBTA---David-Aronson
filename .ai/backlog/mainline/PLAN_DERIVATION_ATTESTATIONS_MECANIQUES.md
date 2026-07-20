# Plan - Derivation des attestations mecaniques

> Sous-chantier 2/3 de `PLAN_HORODATAGE_TRANSVERSAL_ET_ATTESTATIONS`.

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Chantier actif concurrent ? | Non. Enfant 1 est `DONE`, cockpit libre. |
| Verrou de gouvernance ? | Aucun pour les preuves mecaniques. Les approbations humaines restent hors scope. |
| Decision humaine necessaire ? | Non. L'absence de preuve produit `INCONCLUSIVE`. |
| Remplacement ? | Non; correction du producer `gates.json` existant. |

## Audit IA de promotion

- [x] Bootstrap, checkpoint, hook, tracking, Protocole et checklist lus.
- [x] Guardian, epic-orchestrator et evaluator appliques.
- [x] Cinq constantes mecaniques confirmees dans `_write_reports()`.
- [x] Deux passes intake convergentes; faux objectif global PASS retire.
- [x] Perimetre ferme et approbations humaines explicitement exclues.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `mainline` |
| Lifecycle | `TRIAGED` |
| Type de chantier | `SINGLE` |
| Scope | Deriver `live_version_id`, `kill_switch` et les trois exigences G14 depuis les rapports/artefacts effectivement presents, sans constante favorable. |
| Non-goals | Aucun `Protocole/`, schema, reviewer, approval, procedure lifecycle, artefact G14 invente, code Nautilus, R5/R6 ou changement de gate validator. |
| Source | Enfant 2/3 du Lot 3; brouillon `0 - HUMAN START HERE/PLAN_DERIVATION_ATTESTATIONS_MECANIQUES.md`. |
| Exit criteria | Cinq sorties sans constante; missing/false perd le PASS; mapping G14 declare et sur produit PASS; package courant G14 INCONCLUSIVE sans autre erreur technique; 182+ tests et Pyrefly verts. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `NON_DEMARRE` |
| Date de creation | 2026-07-20 |
| Date d'activation | - |
| Autorite normative | SOP 11, SOP 12, Paquet d'execution G13/G14 |
| Autorite executable | builder pilote et gate validator existant |
| Changement normatif | Aucun |
| Dependances externes | Aucune |

## Carte d'execution IA

| Champ | Contenu |
| --- | --- |
| Objectif | Remplacer cinq facades par derivations contrastables. |
| Lecture minimale | Bootstrap, SOP 11/12, Paquet, ce plan, builder pilote, gate validator. |
| Perimetre | Builder pilote, package shape fixture, test pilote, historique. |
| Interdits | Approbations/reviewers, schemas, validator, Protocole, Nautilus. |
| Phase de reprise | Phase 1 helpers G13. |
| Preuve | Tests contraste + suite + Pyrefly + build complet G14 INCONCLUSIVE. |
| Escalade | Toute necessite de definir un nom d'artefact normatif ou une approbation. |

## 1. Role et non-objectifs

Le Protocole definit les exigences; le producer ne fait que transformer des
preuves presentes en valeurs de gate. Ce plan ne cree ni preuve lifecycle, ni
incident, ni retention, ni approbation. Il rend leur absence visible.

## 2. Contexte obligatoire

1. `AGENTS.md`, cockpit et checklist.
2. Entree Protocole, SOP 11, SOP 12, Paquet sections G13/G14.
3. Plan mere Lot 3 et ce plan.
4. `build_research_package.py`, `inputs/package_shape.json`,
   `validators/gate_validator.py`, tests pilote.

Hierarchie : Protocole > SOP/Paquet > gate validator > producer pilote.

## 3. Table des gates

| Ordre | Preuve | Derivation | Absence |
| --- | --- | --- | --- |
| 1 | `live_deployment_report.live_version_id` | identifiant non vide | INCONCLUSIVE |
| 2 | `live_deployment_report.kill_switch_tested` | True PASS, False FAIL | INCONCLUSIVE |
| 3 | mapping G14 + artifact path declare/present | PASS | INCONCLUSIVE |

Les champs humains G2/G7/G13 ne sont pas modifies.

## 4. Etat des lieux

| Existant | Role | Decision |
| --- | --- | --- |
| `gate_report()` | PASS seulement si toutes exigences satisfaites. | Conserver. |
| `live_deployment_report` | Porte deja version et kill-switch fixture. | Lire, ne pas recopier une constante. |
| `package_shape.artifact_paths` | Liste fermee des artefacts du package. | Autorite de presence. |
| `lifecycle_archive.schema.json` | Contrat d'un futur archive lifecycle. | Ne pas modifier ni imposer un chemin. |

Manque reel : un mapping optionnel `gate_evidence_paths` dans la forme du
package pour associer `lifecycle_archive`, `incident_log`, `retention_policy` a
des chemins sans convention inventee. Le mapping courant est absent, donc G14
doit etre INCONCLUSIVE.

## 5. Decision d'architecture

Helpers purs :

- `_identifier_gate(value) -> str` : identifiant ou `INCONCLUSIVE` ;
- `_boolean_evidence_gate(value) -> str` : `PASS`/`FAIL`/`INCONCLUSIVE` ;
- `_artifact_evidence_gate(package_dir, package_shape, name) -> str` : PASS
  seulement si mapping string relatif, chemin inclus dans `artifact_paths`,
  resolution contenue sous `package_dir` et fichier present.

`_write_reports()` recoit la forme du package et appelle ces helpers. Aucun
fallback favorable, aucune recherche heuristique par nom.

### Perimetre explicite

Autorises :

```text
Implementation/examples/minimal_pilot_pipeline/build_research_package.py
Implementation/examples/minimal_pilot_pipeline/inputs/package_shape.json
Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py
Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md
```

Interdits :

```text
Protocole/
Implementation/ebta_engine/schemas/
Implementation/ebta_engine/validators/gate_validator.py
Implementation/ebta_engine/manifests/manifest_builder.py
Implementation/ebta_engine/package_builder/nautilus_research_package.py
reviewers, approvals, R5/R6, BACKTRADER
.ai/checkpoint.json [sauf plan.ps1]
```

## 6. Decoupage en phases

### Phase 1 - Deriver les preuves G13 mecaniques

Objectif : retirer les constantes live version et kill-switch.

Actions :

- Ajouter helpers identifiant/booleen.
- Alimenter les gates depuis `live_deployment_report`.
- Tester valeur, false et absence.

Livrables :

- Deux gates derives et contrastes.

Critere de sortie :

- Aucune valeur favorable ne survit quand la source est retiree ou false.

### Phase 2 - Deriver G14 depuis un mapping explicite

Objectif : rendre l'absence d'artefacts lifecycle visible sans inventer de chemin.

Actions :

- Passer `package_shape` a `_write_reports()`.
- Ajouter le helper de presence securise.
- Tester mapping absent, path absent/hors racine et trois artefacts presents.

Livrables :

- Trois gates G14 derives.

Critere de sortie :

- Package courant donne trois INCONCLUSIVE; fixture temporaire declaree donne trois PASS.

### Phase 3 - Recalibrer les attentes du pilote

Objectif : accepter le rouge G14 honnete sans masquer une erreur technique.

Actions :

- Adapter le test end-to-end : status global FAIL, G14 seul inconclusif.
- Verifier absence de schema, manifest, invariant et semantic errors.
- Journaliser le changement.

Livrables :

- Test de non-regression et historique.

Critere de sortie :

- Le build est complet; la seule cause de gate failure introduite est G14.

### Phase 4 - Audits finaux

Objectif : prouver correction, conformite et scope.

Actions :

- Suite complete, Pyrefly, bug-hunter, plan conformance.

Livrables :

- Preuves de cloture.

Critere de sortie :

- Zero bug confirme et aucun Exit criterion manquant.

## 7. Artefacts produits

| Sortie | Format |
| --- | --- |
| `reports/gates.json` | cinq valeurs derivees |
| tests contraste | unittest |
| historique | Markdown |

## 8. Invariants et NO GO

1. Absence de preuve = jamais PASS.
2. False explicite du kill-switch = FAIL, pas INCONCLUSIVE.
3. Aucun chemin G14 devine ou autorise hors package.
4. Aucun champ humain modifie.
5. Le rouge honnete n'est pas corrige par exemption implicite de stage.

NO GO : modifier validator/schema/SOP, creer un faux artefact, coder une valeur
fixture dans le producer, ou faire passer G14 sur le seul nom du stage.

## 9. Verification a chaque etape

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_minimal_pilot_pipeline.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m pyrefly check Implementation\examples\minimal_pilot_pipeline\build_research_package.py Implementation\ebta_engine\tests\test_minimal_pilot_pipeline.py --output-format min-text
```

Le script pilote est execute pour constater le build complet et G14
INCONCLUSIVE; son exit code non nul attendu n'est pas transforme en PASS.

### Execution sans interruption

Executable sans humain. Escalade seulement si un chemin normatif, schema,
validator ou approbation devient necessaire.

### Autorite decisionnelle

Details techniques permis dans la liste fermee; aucun elargissement doctrinal.

### Interdiction des raccourcis

Il est interdit de retablir le PASS global par `True`, exemption de stage,
mock de preuve ou relachement du validator.

## 10. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-20 | `/continue` de l'EPIC et avancement anti-stagnation. | Autorise cet enfant mecanique, pas les approbations. |

## 11. Risques

| Risque | Mitigation |
| --- | --- |
| Pilot historiquement PASS devient FAIL | Teste comme G14 seul inconclusif; resultat honnete. |
| Path traversal mapping | Resolution sous package obligatoire. |
| Confusion preuve humaine/mecanique | Liste d'interdits et enfant 3 distinct. |

## 12. Definition of Done

- [ ] Cinq constantes mecaniques supprimees.
- [ ] Contrastes missing/false/present verts.
- [ ] G14 courant INCONCLUSIVE sans erreur technique.
- [ ] Aucun champ humain ou fichier interdit touche.
- [ ] Suite, Pyrefly, bug-hunter et conformance verts.

## 13. Cloture

| Champ | Valeur |
| --- | --- |
| Resultat | A remplir |
| Ecarts | A remplir |
| Suite | Enfant 3 approbations humaines. |

## 14. Journal d'audits

| Date | Correction | Pourquoi |
| --- | --- | --- |
| 2026-07-20 | Passe intake 1 : package PASS retire; mapping declaratif introduit. | G14 sans artefacts doit etre INCONCLUSIVE et les chemins ne sont pas specifies. |
| 2026-07-20 | Passe intake 2 : path traversal bloque, false kill-switch distingue de missing; convergence. | Securiser la derivation et conserver le sens des preuves. |
| 2026-07-20 | Passe plan route 1 : le helper G14 est limite a la reconnaissance; il ne cree, copie ni preserve aucun artefact lifecycle. | Un mapping futur ne suffit pas a produire une preuve et le reset du builder demeure inchangé. |
| 2026-07-20 | Passe plan route 2 : aucun nouvel angle mort majeur; convergence. | Les branches present/missing/false sont binaires, les preuves humaines et la production lifecycle restent hors scope. |
