# Plan - Lot F : preuves d'invariants derivees et scellement horodate

> Sous-chantier 3/3 de `EPIC_ATTESTATIONS_RESIDUELLES_R3`. Ce plan est
> `SINGLE` : il corrige un seul flux coherent, la production de
> `invariant_evidence.json`, et ne coordonne aucun sous-lot independant.

---

## 0. Bandeau de statut (a verifier avant toute promotion)

| Question | Reponse |
| --- | --- |
| Un chantier actif couvre-t-il deja ce perimetre (`DONE`, `ACTIVE`, ou `SUPERSEDED`) ? | Non. `.ai/checkpoint.json::active_workstream_id` est `null`; aucun workstream `PLAN_CORRECTION_INVARIANT_EVIDENCE_LOT_F` n'existe. |
| Un verrou de gouvernance actif bloque-t-il ce chantier ? | Non. La decision humaine du 2026-07-20, journalisee dans l'epic parent, autorise la capture UTC automatique du scellement et l'horloge injectee de fixture. |
| Ce plan a-t-il besoin d'une decision humaine explicite pour lever ce verrou avant d'etre routable via `/start` ? | Non. La decision necessaire est actee et son perimetre est ferme en sections 5, 8 et 10. |
| Ce plan remplace-t-il un document ou chantier existant ? | Non. Il materialise le Lot F prevu par l'epic parent. |

### Test de detection multi-lot

Verdict : `SINGLE`. Les quatre derivations corrigees alimentent le meme
artefact et partagent un Exit criterion global : fermer ce lot exige que le
rapport de scellement, les sources WRC/ML/PIT, l'artefact final et leurs tests
soient coherents ensemble. Leur ordre n'est pas interchangeable et un blocage
sur la source de scellement empeche la preuve finale.

---

## Audit IA de promotion

- [x] Plan relu dans le contexte du cockpit actif : `AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json`; aucun hook/tracking actif n'est declare.
- [x] Bandeau de statut verifie contre l'etat machine reel.
- [x] Plan ecrit comme nouveau fichier dans `.ai/backlog/fixes/`; le brouillon original reste intact jusqu'a `plan.ps1 start`.
- [x] Chantier classe `fix`, car il remplace quatre preuves fabriquees par des derivations executables.
- [x] Autorite normative identifiee : `PAQUET D'EXECUTION EBTA.md` section 6, SOP 09A, SOP 10 et SOP 12.
- [x] Perimetre ferme explicite en section 5.
- [x] Decision humaine de source temporelle tracee le 2026-07-20.
- [x] Etat reel verifie : quatre literals subsistent dans `_write_reports()` et `validate_pre_oos_seal()` ne produit pas de timestamp.
- [x] Boucle `/evaluate` du brouillon executee deux fois et convergee.

## Triage

| Champ | Valeur |
| --- | --- |
| Track | `fix` |
| Lifecycle | `TRIAGED` |
| Type de chantier | `SINGLE` |
| Scope | Horodater automatiquement un scellement `PASS`, injecter une horloge de fixture deterministe dans le pilote, puis deriver les quatre valeurs residuelles de `invariant_evidence.json` depuis les rapports et inputs reels. |
| Non-goals | Ne pas modifier `Protocole/`; ne pas modifier les validateurs; ne pas generaliser l'horodatage a tous les jalons; ne pas regenerer `nautilus_mvp`; ne pas inventer de WRC local multi-fold; ne pas changer de gate, seuil ou verdict. |
| Source | Sous-chantier Lot F de `EPIC_ATTESTATIONS_RESIDUELLES_R3`; decision humaine du 2026-07-20 sur l'horodatage automatique. |
| Exit criteria | `sealing.json` porte un timestamp UTC trace a la source; les quatre valeurs de l'artefact sont derivees; les contrastes FAIL/multi-fold bloquent les faux succes; tests cibles, suite runtime, build pilote, bug-hunter et conformance audit passent. |

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | `NON_DEMARRE - plan converge, pret au routage` |
| Date de creation | 2026-07-20 |
| Date d'activation | - |
| Autorite normative | `Protocole/PAQUET D'EXECUTION EBTA.md` section 6 ; SOP 09A ; SOP 10 ; SOP 12 |
| Autorite executable | `Implementation/ebta_engine/procedures/sealing.py` et builder pilote minimal |
| Changement normatif attendu | Aucun - `IMPLEMENTATION_DETAIL` et `TEST_FIXTURE` |
| Dependances externes | Aucune nouvelle |

## Carte d'execution IA (lecture prioritaire pour `/continue`)

| Champ | Contenu operationnel |
| --- | --- |
| Objectif executable | Produire `sealing.json` et `invariant_evidence.json` sans les quatre valeurs fabriquees identifiees par Lot F. |
| Autorite et lecture minimale | Lire `AGENTS.md`, cockpit actif, epic parent, ce plan, `PAQUET D'EXECUTION EBTA.md`, SOP 09A/10/12, puis les fichiers cites section 2. |
| Perimetre autorise | Procedure de scellement, builder/inputs/package pilote, deux tests cibles, historique runtime, plan Lot F, epic parent et checkpoint via `plan.ps1`. |
| Interdits absolus | Aucun changement `Protocole/`, validateurs ou package `nautilus_mvp`; aucune date libre dans `_write_reports()`; aucune duplication d'un WRC agrege en WRC locaux. |
| Phase de reprise | Phase 1 : ajouter le contrat d'horloge et ses tests. |
| Preuve attendue | Tests cibles, suite runtime, build pilote, comparaison `sealing.sealed_at == invariant_evidence.pre_oos_sealed_at`, Pyrefly, bug-hunter et conformance audit. |
| Arret et escalade | Arreter si un timestamp doit etre fourni manuellement en production, si un rapport WRC local multi-fold devient necessaire, ou si un fichier hors liste fermee doit changer. |

---

## 1. Role de ce document et non-objectifs

| Element | Role |
| --- | --- |
| `PAQUET D'EXECUTION EBTA.md` et SOP 09A/10/12 | Autorite normative des invariants, de l'ordre temporel et du scellement. |
| `procedures/sealing.py` | Producteur executable du rapport de scellement. |
| `build_research_package.py` | Assembleur pilote qui doit propager les preuves sans les fabriquer. |
| `reports/invariant_evidence.json` | Artefact final consomme par `validate_invariants()`. |
| Ce plan | Carte d'implementation subordonnee a la norme. |

Non-objectifs :

- ne pas reecrire une SOP ou le protocole ;
- ne pas ajouter un service transversal de journalisation de tous les jalons ;
- ne pas changer la semantique des invariants ;
- ne pas rendre un package rouge artificiellement vert ;
- ne pas traiter la regeneration persistante reservee a la Phase 4 de l'epic.

---

## 2. Contexte obligatoire a lire avant de coder

1. `AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json`.
2. `.ai/backlog/fixes/EPIC_ATTESTATIONS_RESIDUELLES_R3.md`, notamment Phase 3 et decisions du 2026-07-18/20.
3. Ce plan et son brouillon archive apres `/start`.
4. `Protocole/PAQUET D'EXECUTION EBTA.md` section 6 ; SOP 09A, SOP 10 et SOP 12.
5. `Implementation/ebta_engine/procedures/sealing.py`.
6. `Implementation/ebta_engine/validators/invariant_validator.py` en lecture seule.
7. `Implementation/examples/minimal_pilot_pipeline/build_research_package.py` et `inputs/pilot_inputs.json`.
8. `Implementation/ebta_engine/tests/test_procedure_governance.py` et `test_minimal_pilot_pipeline.py`.

Hierarchie d'autorite :

```text
1. Protocole/MANIFESTE DE GEL EBTA.md
2. Protocole/PROTOCOLE EBTA.md et REGISTRE DES DECISIONS NORMATIVES EBTA.md
3. PAQUET D'EXECUTION EBTA.md et SOP 09A/10/12
4. Implementation/ebta_engine/procedures et validators
5. Builder pilote minimal
```

Si le code contredit l'autorite normative, le code doit etre corrige. Une
preuve absente ou non locale doit rester non passante plutot qu'etre inventee.

---

## 3. Table des invariants traverses

| Ordre | Invariant | Question | Sortie si preuve insuffisante/echec |
| --- | --- | --- | --- |
| INV-002 | Scellement avant acces OOS | Le timestamp de scellement reussi precede-t-il chaque acces OOS ? | `INCONCLUSIVE` si absent, `FAIL` si acces anterieur. |
| INV-003 | WRC local avant ouverture OOS | Chaque ouverture possede-t-elle un WRC local `PASS` ? | `FAIL` pour tout statut non `PASS`. |
| INV-006 | Fit Train-only | Les transformations proviennent-elles du manifest ML et restent-elles `Train_k` ? | `FAIL` si un fit sort de Train. |
| INV-007 | Disponibilite PIT | Chaque donnee etait-elle disponible avant la decision ? | `FAIL` si disponibilite posterieure. |

---

## 4. Etat des lieux (avant/apres) - reutiliser avant de recreer

### Ce qui existe deja

| Module actuel | Chemin | Role reel verifie | Suffisant ? |
| --- | --- | --- | --- |
| `validate_pre_oos_seal()` | `Implementation/ebta_engine/procedures/sealing.py` | Verifie stage, hash et approbation ; retourne PASS/FAIL sans date. | A etendre. |
| `_procedure_reports()` | Builder pilote | Produit deja `sealing`, `wrc`, `ml_manifest` et disponibilite des donnees. | Oui comme sources, a propager. |
| `_write_reports()` | Builder pilote | Assemble l'artefact mais fabrique quatre valeurs. | A corriger. |
| `validate_invariants()` | `validators/invariant_validator.py` | Consomme les quatre preuves et retourne PASS/FAIL/INCONCLUSIVE. | Suffisant, lecture seule. |
| Inputs pilote | `inputs/pilot_inputs.json` | Contiennent acces OOS, transformations et disponibilites ; pas d'horloge de fixture nommee. | A completer. |

### Ce qui manque reellement

| Brique manquante | Module | Source | Reutilisation |
| --- | --- | --- | --- |
| Horloge de scellement | `procedures/sealing.py` | Decision humaine 2026-07-20, SOP 10/12 | Etendre la procedure existante. |
| Adaptateur d'horloge fixture | Builder pilote | Besoin de reproductibilite | Lire `fixture_sealed_at`, construire un callable ; ne pas passer un `sealed_at` libre. |
| Derivations d'invariant | Builder pilote | PAQUET section 6 | Lire les rapports deja produits. |
| Contrastes de non-fabrication | Tests existants | Exit criteria Lot F | Etendre les suites cibles. |

---

## 5. Decision d'architecture

Principe directeur : l'evenement source produit la preuve temporelle ;
l'assembleur ne choisit jamais la date. La procedure de scellement capture
l'heure apres validation reussie et le builder ne fait que la propager.

Le contrat d'horloge utilise une dependance injectable pour separer les deux
contextes legitimes : temps reel en production et temps fixe dans une fixture.
La provenance `RUNTIME_UTC` ou `INJECTED_FIXTURE_CLOCK` rend cette distinction
auditable.

Pour WRC, le pilote courant est mono-fold. Sans rapports WRC locaux distincts,
un calendrier multi-fold produit `INCONCLUSIVE` pour chaque ouverture. Cette
sortie fait echouer `INV-003` et empeche un faux succes ; elle n'invente pas une
nouvelle regle et reutilise un statut deja admis dans le runtime.

### Frontieres explicites

| Couche | Elle fait | Elle ne fait pas |
| --- | --- | --- |
| `sealing.py` | Valide le scellement puis capture/normalise l'instant UTC. | Ne lit pas les inputs pilote et ne choisit pas une date historique. |
| Builder pilote | Injecte l'horloge de fixture et derive l'artefact des rapports. | Ne genere pas directement `datetime.now()` dans `_write_reports()`. |
| Validateur | Juge les preuves produites. | Ne repare pas une preuve absente ou fabriquee. |
| Tests | Prouvent production, fixture, FAIL et multi-fold. | Ne remplacent pas une source par un literal de complaisance. |

### Contrat d'interface

```python
def validate_pre_oos_seal(
    package_stage: str,
    *,
    manifest_hash: str,
    independent_approval: bool,
    clock: Callable[[], datetime] | None = None,
) -> dict:
    """Capture sealed_at seulement lorsque les controles passent."""
```

Sortie `PASS` : `artifact_type`, `status`, `violations`, `sealed_at`,
`sealed_at_source`. Sortie `FAIL` : ni `sealed_at` ni `sealed_at_source`.

Le builder copie `pilot_inputs["pre_oos_seal"]`, retire
`fixture_sealed_at` de cette copie, construit le callable d'horloge puis passe
seulement les trois arguments metier et `clock` a `validate_pre_oos_seal()`.
La procedure generique ne connait donc jamais la cle de configuration propre
au pilote et ne peut pas la confondre avec une preuve de production.

### Decisions deja actees

| Decision | Justification |
| --- | --- |
| Heure runtime UTC automatique | Evite la saisie humaine fragile et la date choisie par IA. |
| Horloge injectable uniquement pour fixture/test | Rend le pilote reproductible sans transformer la fixture en preuve reelle. |
| `INCONCLUSIVE` sur multi-fold sans WRC locaux | Evite de dupliquer un verdict agrege et de produire un faux PASS. |
| Validateurs inchanges | Ils expriment deja les invariants attendus. |

### Perimetre de fichiers explicite

Autorises :

```text
Implementation/ebta_engine/procedures/sealing.py                                MODIFIER
Implementation/examples/minimal_pilot_pipeline/build_research_package.py        MODIFIER
Implementation/examples/minimal_pilot_pipeline/inputs/pilot_inputs.json         MODIFIER
Implementation/examples/minimal_pilot_pipeline/research_package/                REGENERER
Implementation/ebta_engine/tests/test_procedure_governance.py                   MODIFIER
Implementation/ebta_engine/tests/test_minimal_pilot_pipeline.py                 MODIFIER
Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md                           MODIFIER
.ai/backlog/fixes/PLAN_CORRECTION_INVARIANT_EVIDENCE_LOT_F.md                   MODIFIER
.ai/backlog/fixes/EPIC_ATTESTATIONS_RESIDUELLES_R3.md                            MODIFIER apres cloture
.ai/checkpoint.json                                                              MODIFIER via plan.ps1
```

Interdits :

```text
Protocole/                                                                       NORME INTOUCHABLE
Implementation/ebta_engine/validators/invariant_validator.py                    CONTRAT SUFFISANT
Implementation/ebta_engine/validators/gate_validator.py                         HORS SCOPE
Implementation/research_packages/nautilus_mvp/                                  PHASE 4 EPIC UNIQUEMENT
.ai/checkpoint.schema.json                                                       PAS D'EXTENSION
Tout module transversal d'horodatage des autres jalons                          CHANTIER SEPARE
```

---

## 6. Decoupage en phases

### Phase 1 - Contrat de scellement automatique

Objectif : faire produire `sealed_at` par l'evenement de scellement reussi.

Classification : IMPLEMENTATION_DETAIL

Actions :

- Ajouter la dependance `clock` optionnelle et l'horloge UTC runtime par defaut.
- Normaliser la date timezone-aware en ISO-8601 suffixe `Z`.
- Retourner `sealed_at_source = RUNTIME_UTC` ou `INJECTED_FIXTURE_CLOCK`.
- Ne pas produire `sealed_at` si une violation rend le scellement `FAIL`.
- Ajouter les tests runtime, fixture, FAIL et datetime naive.

Livrables :

- Rapport de scellement horodate et tests unitaires.

Critere de sortie :

- `test_procedure_governance.py` prouve les quatre comportements sans echec.

### Phase 2 - Deriver invariant_evidence depuis ses sources

Objectif : supprimer les quatre literals residuels de `_write_reports()`.

Classification : IMPLEMENTATION_DETAIL

Actions :

- Ajouter `fixture_sealed_at` aux inputs et construire une horloge injectee dans le builder.
- Propager `sealing.get("sealed_at")` vers `pre_oos_sealed_at`.
- Deriver `transformation_fits` du manifest ML.
- Deriver `decision_events` de `data_availability_checks` avec renommage de cle.
- Mapper le WRC reel pour le mono-fold ; produire `INCONCLUSIVE` pour chaque fold si le calendrier est multi-fold sans preuves locales.
- Ajouter des tests de contraste qui modifient les sources et observent les sorties.

Livrables :

- Builder sans literals residuels et tests de non-fabrication.

Critere de sortie :

- Les tests prouvent l'egalite source/sortie et le non-PASS multi-fold.

### Phase 3 - Regeneration pilote, audits et cloture

Objectif : regenerer la fixture, prouver la non-regression et clore Lot F.

Classification : GOVERNANCE

Actions :

- Regenerer le package pilote minimal.
- Verifier `sealing.sealed_at == invariant_evidence.pre_oos_sealed_at`.
- Executer tests cibles et suite runtime complete.
- Mettre a jour l'historique runtime.
- Executer bug-hunter puis plan-conformance-audit.
- Clore Lot F via `plan.ps1 close` et valider le checkpoint.
- Mettre a jour l'epic parent vers sa Phase 4.

Livrables :

- Package pilote regenere, workstream Lot F `DONE`, epic parent synchronise.

Critere de sortie :

- Tous les Exit criteria section 12 sont coches et le checkpoint valide Lot F `DONE`.

### Chemin critique

```mermaid
flowchart LR
    P1[Phase 1 - scellement date] --> P2[Phase 2 - derivations]
    P2 --> P3[Phase 3 - audits et cloture]
```

---

## 7. Artefacts produits

| Etape | Fichier/sortie | Regle source |
| --- | --- | --- |
| Scellement | `reports/sealing.json` | SOP 10/12 |
| Preuves | `reports/invariant_evidence.json` | PAQUET section 6 |
| Fixture | `inputs/pilot_inputs.json` | Reproductibilite test |
| Tests | deux fichiers unittest cibles | Exit criteria Lot F |
| Historique | `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` | Gouvernance runtime |

---

## 8. Invariants absolus et NO GO

### Invariants

1. Un timestamp de scellement n'existe qu'apres un resultat `PASS`.
2. En production, la source est l'horloge UTC runtime au moment de l'evenement.
3. En fixture, la date fixe est explicitement etiquetee et injectee.
4. `pre_oos_sealed_at` est une propagation exacte, jamais un nouvel appel d'horloge.
5. Un WRC agrege ne devient jamais plusieurs WRC locaux `PASS`.
6. Les transformations et disponibilites conservent exactement leurs valeurs sources.

### NO GO

- Appeler `datetime.now()` dans `_write_reports()`.
- Ajouter un argument public `sealed_at` choisi librement pour la production.
- Horodater un scellement `FAIL`.
- Emettre une liste `oos_openings` vide pour contourner INV-003.
- Modifier un validateur, une SOP, un gate ou un seuil.
- Generaliser tous les jalons dans Lot F.

---

## 9. Verification a chaque etape

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_procedure_governance.py
```

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_minimal_pilot_pipeline.py
```

```powershell
python Implementation\examples\minimal_pilot_pipeline\build_research_package.py
```

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
```

```powershell
Implementation\adapters\nautilus_env\venv\Scripts\python.exe -m pyrefly check Implementation\ebta_engine\procedures\sealing.py Implementation\examples\minimal_pilot_pipeline\build_research_package.py Implementation\ebta_engine\tests\test_procedure_governance.py Implementation\ebta_engine\tests\test_minimal_pilot_pipeline.py --output-format min-text
```

Regle bloquante : ne pas clore si une validation echoue, si un literal
historique subsiste, ou si le test multi-fold produit INV-003 `PASS`.

### Execution sans interruption

Le plan peut etre execute integralement sans retour humain. La decision de
source temporelle et le perimetre sont actees. Arreter uniquement aux
conditions d'escalade de la carte d'execution.

### Autorite decisionnelle accordee

L'IA peut choisir des helpers locaux et assertions de test dans les fichiers
autorises, sans modifier le contrat normatif ni etendre le chantier.

### Interdiction des raccourcis

Ne jamais remplacer un literal par un autre literal de complaisance, appeler
deux horloges pour la meme preuve, ou masquer un FAIL/INCONCLUSIVE legitime.

---

## 10. Journal des decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-07-17 | Lot F est un sous-chantier distinct de l'epic R3. | Implique un cycle `/start` a `/close` autonome. |
| 2026-07-20 | Les dates des jalons ne doivent etre saisies manuellement ni choisies par une IA. Pour Lot F, le runtime capture automatiquement l'heure UTC du scellement reussi ; tests et pilote utilisent une horloge injectee identifiee comme fixture. | Leve le blocage de `pre_oos_sealed_at` sans modifier `Protocole/`. |
| 2026-07-20 | La generalisation a tous les jalons est un chantier transversal distinct. | Interdit l'elargissement silencieux de Lot F. |

---

## 11. Risques et blocages connus

| Risque | Impact | Mitigation |
| --- | --- | --- |
| Horloge naive ou non UTC | Comparaisons temporelles ambiguës | Rejeter les datetime sans timezone et normaliser UTC. |
| Scellement FAIL sans date | INV-002 devient non concluant | Comportement attendu : aucune fausse preuve. |
| Plusieurs folds mais un WRC agrege | Faux PASS local possible | Emettre `INCONCLUSIVE` pour chaque fold et tester INV-003 non passant. |
| Fixture confondue avec preuve reelle | Historique trompeur | Champ `fixture_sealed_at` et provenance `INJECTED_FIXTURE_CLOCK`. |
| G4/WRC pilote peut legitimement changer | Package rouge apres derivation | Documenter le verdict reel, ne pas le masquer. |

---

## 12. Definition of Done

- [ ] `sealing.json` contient `sealed_at` UTC et sa provenance sur PASS.
- [ ] Un scellement FAIL ne contient pas `sealed_at`.
- [ ] Une horloge naive est rejetee.
- [ ] `pre_oos_sealed_at` est egal a `sealing.sealed_at`.
- [ ] `oos_openings`, `transformation_fits` et `decision_events` derivent de leurs sources reelles.
- [ ] Un calendrier multi-fold sans WRC locaux ne produit aucun WRC local `PASS` et INV-003 n'est pas PASS.
- [ ] Les quatre literals historiques ont disparu de `_write_reports()`.
- [ ] Tests cibles et suite runtime `PASS`.
- [ ] Build pilote minimal `PASS` et artefacts regeneres.
- [ ] Pyrefly/bug-hunter `PASS`.
- [ ] Plan-conformance-audit `PASS`.
- [ ] Lot F clos via `plan.ps1 close`, checkpoint valide et epic parent synchronise.

---

## 13. Cloture

A remplir apres les audits pre-cloture.

---

## 14. Journal d'audits

| Date | Passe | Resultat |
| --- | --- | --- |
| 2026-07-20 | Brouillon `/evaluate` 1 | Signature d'horloge, normalisation UTC, echec sans date, cle fixture et comportement multi-fold fermes. |
| 2026-07-20 | Brouillon `/evaluate` 2 | Convergence ; appelants, schemas et frontieres verifies ; aucun nouveau blind spot majeur. |
| 2026-07-20 | Plan route `/evaluate` 1 | Contrat builder/procedure precise : `fixture_sealed_at` est retire avant `**kwargs`; FAIL ne contient ni date ni provenance. Aucun changement de perimetre. |
| 2026-07-20 | Plan route `/evaluate` 2 | Convergence ; perimetre, tests de contraste, comportement temporel et fallback multi-fold couvrent les risques identifies sans nouveau blind spot majeur. |
