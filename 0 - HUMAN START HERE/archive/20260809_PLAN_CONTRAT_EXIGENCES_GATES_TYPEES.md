# Brouillon — Contrat d'exigences G0-G14 type et fail-closed

Statut : `INTAKE`, non executable.

Parent : `EPIC_DURCISSEMENT_POST_AUDIT_ERREURS_IA`.

ID prevu : `PLAN_CONTRAT_EXIGENCES_GATES_TYPEES`.

## Objectif

Remplacer la validation generique par truthiness de
`Implementation/ebta_engine/validators/gate_validator.py` par un contrat
explicite pour chaque exigence G0-G14 :

- `identifier` : chaine non vide ;
- `verdict_pass` : uniquement la valeur exacte `"PASS"` ;
- `boolean_true` : uniquement le singleton `True`.

Le validateur doit refuser sans exception tout statut negatif, bloquant,
local, technique, de monitoring ou inconnu lorsqu'un champ exige un verdict
`PASS`.

## Source et preuve du defaut

- Audit cible :
  `0 - HUMAN START HERE/AUDIT_ROBUSTESSE_ARCHITECTURE_FACE_ERREURS_IA_2026-08-09.md`, finding A1.
- Code : `gate_validator.py::_requirement_satisfied()` accepte aujourd'hui
  toute chaine non vide hors `PASS`/`FAIL`/`INCONCLUSIVE`.
- Test : `test_gates.py::test_gate_report_would_accept_raw_not_validated_oos_gate`
  attend explicitement que `NOT_VALIDATED` satisfasse G9.
- Prototype observe : `REJECTED_ECONOMIC`, `NOT_VALIDATED`, `DENIED` et
  `UNKNOWN` satisfont `G10.economic_report`.

Autorites existantes, sans nouvelle norme :

- `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md` porte les taxonomies ;
- `Protocole/PAQUET D'EXECUTION EBTA.md` porte les exigences G0-G14 ;
- `Implementation/ebta_engine/constants.py` encode deja les familles de
  statuts ;
- un gate n'est satisfait que par sa preuve positive attendue.

Classification Guardian : `CONTRACT_ENCODING`. Aucun nouveau gate, statut,
seuil, ordre ou verdict.

## Test multi-lot

Resultat : `SINGLE_CHANTIER`.

Le contrat type, son evaluation fail-closed et les regressions associees ont
un seul jeu d'Exit criteria. Les tests n'ont pas de sens sans le contrat et le
contrat n'est pas clos sans ses preuves negatives. Les lots approbation live,
coherence des verdicts persistes et garde AST restent dans leurs workstreams
separes.

## Decision d'architecture

Remplacer les listes de noms de `GATE_REQUIREMENTS` par des objets immuables
`GateRequirement(name, kind)`.

Regles :

1. `identifier` accepte uniquement une `str` dont `strip()` n'est pas vide ;
2. `verdict_pass` accepte uniquement `value == "PASS"` ;
3. `boolean_true` accepte uniquement `value is True` ;
4. un type de requirement inconnu leve une erreur explicite, jamais un repli
   truthy ;
5. chaque nom present dans G0-G14 possede exactement une nature explicite ;
6. la sortie publique `GateResult` et la forme de `gate_report()` restent
   inchangees.

Classification initiale :

- identifiants : `config_id`, `project_id`, `research_family_id`,
  `hypothesis_id`, `process_version_id`, `template_hash`,
  `selected_candidate_id`, `live_version_id` ;
- booleen strict : `live_approval` ;
- toutes les autres exigences : `verdict_pass`.

## Perimetre autorise

- `Implementation/ebta_engine/validators/gate_validator.py` ;
- `Implementation/ebta_engine/tests/test_gates.py` ;
- `Implementation/ebta_engine/tests/test_inventory.txt` si de nouveaux IDs de
  tests sont ajoutes ;
- `Implementation/ebta_engine/fixtures/valid_minimal/reports/gates.json` pour
  normaliser les anciens booleens de pseudo-verdict vers `"PASS"` ;
- `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` ;
- plan, checkpoint et rapports de controle propres au cycle gouverne.

## Non-goals

- aucune modification de `Protocole/`, des schemas, du builder, des artefacts
  de package ou de BACKTRADER ;
- aucune correction de `live_approval=True`, d'INV-010 ou des litteraux de
  verdict : workstreams 3B, 3C et 3D ;
- aucune nouvelle taxonomie ;
- aucun assouplissement pour conserver le test qui accepte `NOT_VALIDATED` ;
- aucune modification de la forme de sortie `GateResult`/`gate_report()`.

## Phases

### Phase 1 — Contrat type

- introduire la representation immuable des exigences ;
- classifier tous les champs G0-G14 ;
- remplacer `_requirement_satisfied(value)` par une evaluation qui recoit la
  nature attendue et echoue explicitement sur une nature inconnue.

### Phase 2 — Preuves negatives et compatibilite

- inverser le test `NOT_VALIDATED` ;
- couvrir sur un champ `verdict_pass` : `REJECTED_ECONOMIC`, `NOT_VALIDATED`,
  `INVALID_TECHNICAL`, `DENIED`, `BURNED`, `WATCH`, `NO_MODEL`,
  `STOP_PROCESS`, `UNKNOWN`, chaine vide, `None`, `False`, `True` et `1` ;
- prouver qu'un identifiant non vide est accepte et qu'un identifiant vide ou
  non-string est refuse ;
- prouver que `boolean_true` refuse `1`, `"PASS"`, les valeurs fausses et les
  chaines non vides ;
- prouver qu'une nature inconnue echoue explicitement ;
- prouver que l'ensemble des noms et leur classification sont exhaustifs et
  sans doublon ;
- conserver les sorties `present`/`missing` et l'ordre G0-G14.

### Phase 3 — Validation et trace

- migrer la fixture `valid_minimal` des anciens `true` de pseudo-verdict vers
  les valeurs `"PASS"` emises par le producteur vivant, en conservant les huit
  identifiants et `live_approval` boolean ;
- verifier les manifestes reconstruits en repertoire temporaire par les tests
  existants ; aucun manifeste n'est persiste dans cette fixture ;
- executer `test_gates.py`, puis la suite canonique complete ;
- mettre a jour l'inventaire de tests si necessaire ;
- journaliser le changement runtime sans modifier l'autorite normative.

## Exit criteria

- [ ] Chaque exigence G0-G14 a une nature explicite et unique.
- [ ] Seul `"PASS"` satisfait un champ `verdict_pass`.
- [ ] Une valeur inconnue ou d'un mauvais type ne peut jamais passer par
      truthiness.
- [ ] Les identifiants et le booleen strict conservent leur semantique.
- [ ] La fixture `valid_minimal` est alignee sur les types du producteur vivant
      et son manifeste reste verifiable.
- [ ] Le test qui acceptait `NOT_VALIDATED` est inverse.
- [ ] Les taxonomies negatives et une valeur inconnue sont couvertes par des
      tests deterministes.
- [ ] La forme de `GateResult` et `gate_report()` reste compatible.
- [ ] La suite canonique complete passe et l'inventaire de tests est a jour.
- [ ] L'historique runtime cite le finding A1 et l'absence de changement
      normatif.
- [ ] Aucun fichier hors perimetre n'est modifie par ce workstream.

## Risques et rollback

- Risque : un appelant utilisait une chaine arbitraire comme pseudo-verdict.
  Mitigation : les identifiants sont classes explicitement ; tout autre champ
  est contractuellement un verdict positif et doit etre `PASS`.
- Risque : `True == 1` en Python. Mitigation : `boolean_true` utilise
  `value is True`, et les tests couvrent `1`.
- Risque : omission d'un nouveau champ lors d'une future evolution.
  Mitigation : le champ doit etre ajoute avec un `kind`; aucune branche par
  defaut permissive.
- Rollback : revert du commit d'implementation ; aucune migration de donnees
  ni de schema.

## Journal d'audit intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Relecture de `gate_validator.py`, de tous ses consommateurs internes, du producteur minimal et des fixtures `gates.json`. | Finding majeur : `valid_minimal` utilise encore des booleens `true` pour les pseudo-verdicts, alors que le producteur vivant emet `"PASS"`. Perimetre corrige pour migrer cette fixture et verifier les manifestes reconstruits par les tests ; ajout d'une preuve d'exhaustivite des classifications. |
| 2 | Verification des fichiers reels de `valid_minimal` et des tests `test_package_validator.py`/`test_manifest_hashes.py`. | Hypothese infirmee : aucun manifeste n'est versionne dans la fixture ; il est construit en temporaire par les tests. Le faux chemin a ete retire et la validation reformulee sans artefact invente. |
| 3 | Relecture du perimetre corrige contre le producteur, les deux fixtures de gates, les consommateurs et les Exit criteria. | Aucun nouvel angle mort majeur. Le chantier reste `SINGLE_CHANTIER`, sans schema ni decision normative ; convergence intake. |
