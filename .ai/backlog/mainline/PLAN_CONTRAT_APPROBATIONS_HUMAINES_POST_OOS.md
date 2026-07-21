# Plan d'implementation — Contrat des approbations humaines pre-OOS

## 0. Bandeau de statut (a verifier avant toute promotion)

| Champ | Valeur |
|---|---|
| Track | mainline |
| Lifecycle | PENDING |
| Type de chantier | SINGLE |
| Scope | Remplacer les reviewers/approbations pre-OOS fabriques par un contrat d'inputs explicites optionnels, propage vers scellement, autorisation OOS, gates et manifeste. |
| Non-goals | Post-OOS/live, G-BIAS, schemas, validateurs, Protocole, BACKTRADER, identites humaines inventees. |
| Source | `0 - HUMAN START HERE/archive/20260721_PLAN_CONTRAT_APPROBATIONS_HUMAINES_POST_OOS.md` |
| Exit criteria | Absence non-PASS et OOS DENIED ; preuves externes exactes propagees ; fixtures test-only refusees par defaut ; aucun litteral de preuve ; zero changement interdit ; audits finaux PASS. |

- [x] Decision humaine `3A` journalisee dans la mere.
- [x] Test multi-lot `SINGLE`.
- [x] Brouillon `/evaluate` deux passes convergentes.
- [ ] `/start`, deux audits du plan route, baseline puis `/continue`.

## Audit IA de promotion

Le defect est confirme dans le code : deux gates valent litteralement `True`,
le scellement et la requete OOS consomment une valeur fixture, et le manifeste
fabrique deux chaines d'identite. Corriger seulement le rapport final serait
une facade ; le contrat doit gouverner avant l'autorisation OOS.

## Triage

| Question | Reponse |
|---|---|
| Plusieurs lots independants ? | Non, contrat et propagation forment une chaine unique. |
| Decision bloquante ? | Levee par `3A`. |
| Autorite normative | SOP 03/10/12, inchangees. |
| Classification | GOVERNANCE / IMPLEMENTATION_DETAIL. |

## Sous-chantiers

Sans objet (`SINGLE`).

## Statut

`PENDING / TRIAGED` apres routage ; aucune modification code avant baseline.

## Carte d'execution IA (lecture prioritaire pour `/continue`)

| Element | Contrat |
|---|---|
| Premier geste | Relire checkpoint, plan et diff depuis baseline. |
| Chemin critique | Contrat -> scellement/OOS -> gates -> manifeste -> tests. |
| Arret | Toute preuve absente/invalide laisse OOS refuse ; aucune identite n'est deduite. |
| Cloture | bug-hunter + plan-conformance, puis `/close`. |

## 1. Role de ce document et non-objectifs

Ce plan livre l'enfant 3 du Lot 3. Il ne produit aucune approbation humaine :
il encode le transport et le refus honnete en son absence. Les champs live
exclus le 2026-07-17 restent intouches.

## 2. Contexte obligatoire a lire avant de coder

1. Bootstrap EBTA complet et checklist de modification.
2. SOP 03, SOP 10, SOP 12 et entree Protocole.
3. Plan mere `PLAN_HORODATAGE_TRANSVERSAL_ET_ATTESTATIONS`.
4. Enfants clos chronologie et attestations mecaniques.
5. Builder pilote, `procedures/sealing.py`, `procedures/oos_access.py`,
   `manifests/manifest_builder.py` et tests correspondants.

## 3. Table des gates (points de decision sequentiels)

| Gate | PASS | Sinon |
|---|---|---|
| C1 contrat | Champs obligatoires, UTC, scope autorise | preuve invalide/non-PASS |
| C2 fixture | `TEST_FIXTURE` + option d'appel explicite | refusee |
| C3 scellement | approbation externe ou fixture test autorisee | scellement non PASS |
| C4 OOS | tous gates + preuve valide | DENIED, zero runner OOS |
| C5 manifeste | identites/IDs derives de preuves acceptees | tableaux vides |

## 4. Etat des lieux (avant/apres) — reutiliser avant de recreer

### Ce qui existe deja

- `validate_pre_oos_seal()` et `authorize_oos_access()` derivent correctement.
- G2/G7 et le manifeste acceptent deja une valeur derivee/array.
- Le builder Nautilus s'arrete deja avant OOS si la decision est `DENIED`.
- Les schemas du manifeste acceptent des tableaux vides.

### Ce qui manque reellement

- Un validateur SSoT des preuves humaines.
- Une option test-only non serialisee.
- La propagation de ce SSoT vers les quatre consommateurs.
- Les tests de contraste et le retrait des valeurs fabriquees.

## 5. Decision d'architecture

Une fonction stdlib dans le builder pilote normalise une seule fois
`pre_oos_human_evidence` avant `config.json`. La version acceptee fait partie
de la config scellee ; l'autorisation de fixture est un argument d'appel
distinct, jamais ecrit dans la config. Scellement, gates et OOS lisent la meme
version normalisee ; le manifeste lit uniquement la config, ce qui evite une
seconde source de verite. Dans ses tableaux de chaines, une fixture acceptee
en test est prefixee `TEST_FIXTURE:` afin que son scope reste visible sans
modifier le schema.

### Frontieres explicites (ce que chaque couche fait / ne fait pas)

| Couche | Fait | Ne fait pas |
|---|---|---|
| Validateur evidence | Verifie forme, scope, statut, UTC, reference | N'approuve personne |
| Builder pre-OOS | Derive scellement/gates/OOS | N'ouvre pas OOS sans decision AUTHORIZED |
| Manifeste | Extrait reviewers/approvals acceptes | Ne fabrique pas de placeholder |
| Tests | Autorisent explicitement TEST_FIXTURE | Ne changent pas le defaut production |

### Contrat d'interface entre les couches

Chaque entree `registry_review` / `pre_oos_approval` contient :
`evidence_id`, `reviewer_id`, `status`, `evidence_scope`, `approved_at`,
`source_reference`, `subject_id` et `independence_attested=true`. Le
`subject_id` doit correspondre a la famille de recherche pour la revue du
registre et au `manifest_hash` scelle pour l'approbation pre-OOS. Seul
`APPROVED` est PASS. `EXTERNAL` est autorise par defaut ; `TEST_FIXTURE` exige
`allow_test_fixture_human_evidence=True`.

### Decisions deja actees

- `3A`, 2026-07-21 : inputs optionnels ; absence `INCONCLUSIVE`/DENIED.
- Fixtures reservees aux tests.
- Post-OOS/live hors perimetre.

### Structure cible

```text
pilot_inputs.pre_oos_human_evidence
  -> validate once
  -> seal + OOS request + G2/G7
  -> config
  -> manifest reviewers/approvals
```

### Perimetre de fichiers explicite (autorises / interdits)

Autorises : builder pilote, manifest builder, tests pilote/manifeste/Nautilus,
input fixture si retrait de champ mort, README/historique runtime si necessaire,
plan et checkpoint. Interdits : `Protocole/**`, schemas, validateurs, champs
live/post-OOS, BACKTRADER.

## 6. Decoupage en phases

### Phase 0 - Contrat de preuve

Ajouter normalisation/validation et tests unitaires absent, incomplet, UTC
naif, scope inconnu, EXTERNAL valide, TEST_FIXTURE refuse/accepte.

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_human_approval_evidence.py
```

### Phase 1 - Scellement et autorisation OOS

Remplacer la valeur fixture par le verdict du contrat dans le seal et la
requete OOS. Test espion : aucun seed/run OOS sans preuve.

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_nautilus_research_package.py
```

### Phase 2 - Gates et manifeste

Deriver G2/G7 et tableaux reviewers/approvals depuis la config scellee.
Supprimer les placeholders.

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_minimal_pilot_pipeline.py
```

### Phase 3 - Non-regression et preuve production

Prouver absence => DENIED/0 OOS et fixture explicite => tests historiques
encore valides. Lancer venv complet et package pilote dans son mode fixture de
test explicite seulement.

```powershell
Push-Location Implementation
.\adapters\nautilus_env\venv\Scripts\python.exe -m unittest discover -s ebta_engine\tests -t .
Pop-Location
```

### Chemin critique (ordre des phases)

`P0 contrat -> P1 seal/OOS -> P2 gates/manifeste -> P3 suite`

## 7. Artefacts produits

- Contrat de preuve humaine optionnelle.
- Gates et manifeste sans placeholder.
- Tests absent/externe/fixture et zero-OOS.
- Historique runtime et plan audite.

## 8. Invariants absolus et NO GO

### Invariants (non negociables dans le code)

- Absence/invalide n'est jamais PASS.
- Un reviewer ID n'est jamais une preuve suffisante sans evidence ID/source/UTC.
- Une fixture n'est jamais acceptee par defaut.
- Une preuve est scellee avant l'OOS.

### NO GO (actions explicitement interdites — a verifier a chaque revue de diff)

- Inventer une identite, preuve ou timestamp.
- Conserver un fallback `True`.
- Mettre l'option fixture dans un fichier de production.
- Modifier schema/validateur/Protocole pour faire passer le package.
- Toucher les champs post-OOS/live exclus.

## 9. Verification a chaque etape

Apres chaque phase : tests cibles, `git diff --check`, recherche des placeholders
et verification qu'aucun fichier interdit n'est touche.

```powershell
rg -n "independent_registry_review.*True|independent_pre_oos_approval.*True|independent_reviewer|runtime_fixture_approval" Implementation -g "*.py"
git diff --check
```

### Execution sans interruption

Traiter les regressions dans le perimetre jusqu'a suite verte ; stopper si un
schema ou une decision normative devient necessaire.

### Autorite decisionnelle accordee

L'IA choisit noms/helpers et adaptation des fixtures de tests. Elle ne fournit
aucune preuve externe reelle et ne reouvre aucun champ live.

### Interdiction des raccourcis (aucun faux succes)

Un test qui passe avec fixture n'est pas preuve production. Le test principal
doit partir de l'absence totale de preuve et constater le refus avant OOS.

## 10. Journal des decisions humaines (autorisations)

| Date | Decision | Effet |
|---|---|---|
| 2026-07-17 | Champs post-OOS/live exclus | Perimetre borne au pre-OOS/recherche |
| 2026-07-21 | `3A` inputs explicites optionnels | Absence non-PASS ; fixtures test-only |

## 11. Risques et blocages connus

| Risque | Mitigation |
|---|---|
| Deux sources de verite | Config scellee unique, manifeste la lit |
| Tests historiques supposent PASS | Helper fixture explicite dans tests, jamais defaut production |
| G-BIAS confondu avec approbation OOS | Contrats et IDs distincts |
| OOS execute trop tot | Test espion sur runner/seed et decision DENIED |

## 12. Definition of Done

- [x] Absence => seal non PASS, gates non PASS, DENIED, 0 OOS, manifeste vide.
- [x] EXTERNAL valide => IDs exacts propages et autorisation conditionnelle.
- [x] TEST_FIXTURE refuse par defaut, accepte seulement avec option explicite.
- [x] Aucun placeholder/litteral de preuve ne subsiste.
- [x] Aucun fichier interdit touche.
- [x] Tests cibles, suite venv, bug-hunter et conformance PASS.

## 13. Cloture

Clore seulement apres bug-hunter et plan-conformance propres, puis valider le
checkpoint et committer uniquement le delta de cloture.

### Resultat d'execution (a dupliquer a chaque session d'execution significative)

| Date | Phase | Validation | Resultat |
|---|---|---|---|
| 2026-07-21 | Preparation | `/evaluate` brouillon x2 | Convergent |
| 2026-07-21 | Phases 0-2 | Contrat SSoT, seal/OOS, G2/G7 et manifeste | 30 tests cibles PASS ; package pilote absent => INCONCLUSIVE/FAIL/DENIED/tableaux vides | PASS |
| 2026-07-21 | Phase 3 | Contraste fixture et non-regression | TEST_FIXTURE refusee par defaut/prefixee si autorisee ; 208 tests venv PASS | PASS |
| 2026-07-21 | bug-hunter | Pyrefly sur tous les Python touches | 1 contrat de dict heterogene corrige ; 0 erreur final | PASS |
| 2026-07-21 | plan-conformance-audit | Six criteres DoD contre diff depuis `f561884` | 6 IMPLEMENTE ; 0 MANQUANT ; 0 non-goal viole | PASS |

## 14. Journal d'audits post-hoc

| Date | Audit | Conclusion |
|---|---|---|
| 2026-07-21 | Plan route passe 1 | Liaison obligatoire de chaque preuve a son `subject_id` et attestation d'independance ajoutees |
| 2026-07-21 | Plan route passe 2 | Normalisation unique avant config scellee et prefixe manifeste `TEST_FIXTURE:` ajoutes ; aucun nouveau blind spot majeur, convergence |

### Plan-conformance-audit final — 2026-07-21

| Critere | Classification | Preuve |
|---|---|---|
| Absence non-PASS, DENIED, 0 OOS, manifeste vide | IMPLEMENTE | Test pilote lit G2/G7, seal, decision et manifeste ; test Nautilus espion prouve aucun seed OOS |
| EXTERNAL valide et IDs exacts | IMPLEMENTE | `test_external_evidence_is_bound_to_exact_subjects` ; normalisation `subject_id`/UTC/independance et extraction manifeste |
| Fixture test-only | IMPLEMENTE | Refus par defaut, option explicite dans wrappers de tests, prefixe `TEST_FIXTURE:` |
| Aucun placeholder/litteral de preuve | IMPLEMENTE | Recherche cible : aucune occurrence des deux `True` ni de `runtime_fixture_approval` dans le perimetre production/manifeste regenere |
| Aucun fichier interdit | IMPLEMENTE | Diff sans `Protocole/`, schema, validateur, BACKTRADER ni champ live/post-OOS |
| Audits finaux | IMPLEMENTE | 208 tests venv PASS ; Pyrefly 0 erreur ; present audit 0 manquant |
