# Audit cible — Architecture d'assemblage des verdicts EBTA

Date : 2026-08-09

Statut : audit en quatre passes, converge

Portee prioritaire : assemblage des verdicts, gates et autorisations persistees

Decision d'implementation : aucune ; ce document est un `INTAKE` non executable.

## Journal des passes

| Passe | Verification directe | Resultat |
| --- | --- | --- |
| 1 | Bootstrap, autorites normatives, epic actif, scan AST des affectations positives sensibles, lecture du contexte des 27 candidats et suite canonique. | Le seuil brut est confirme, mais il melange sept calculs derives, sept valeurs attendues de contrat, deux fixtures, deux attestations techniques, deux constantes humaines documentees, deux evenements de registre et cinq faux succes actifs. Suite : 246 tests, `OK`. |
| 2 | Tracage des cinq faux succes vers `gates.json`, `invariant_evidence.json`, `deployment_gate.json` et leurs validateurs ; prototypes en repertoires temporaires. | Trois ruptures majeures distinctes sont reproduites : statuts negatifs/unknown acceptes par le validateur generique, verdict live `FAIL` transforme en G13 `PASS`, rapport economique rejete contredit par un invariant `PASS`. |
| 3 | Relecture des tests, de `constants.py`, du validateur de paquet et des exigences SOP 11/SOP 12/G13/INV-010. | Les ruptures sont confirmees comme ecarts d'implementation, sans nouvelle norme necessaire. Le test existant `test_gate_report_would_accept_raw_not_validated_oos_gate` conserve explicitement l'un des comportements dangereux au lieu de le refuser. Aucun nouveau cluster majeur. |
| 4 | Contre-verification comportementale bout en bout d'un paquet avec verdict live soumis `FAIL`, puis validation isolee d'INV-010 avec trois `PASS` litteraux. | G13 reste `PASS` et INV-010 reste `PASS`. Aucun nouveau cluster majeur : convergence apres deux passes consecutives sans nouvelle famille de rupture. |

## 1. Resume executif

Pertinence : **PROBLEMATIQUE**

Risk Level : **CRITIQUE** — un refus economique, un statut inconnu ou un verdict live `FAIL` peut etre represente comme gate satisfait.

Coherence avec l'existant normatif : **faible sur les trois chemins trouves** ; SOP 11 interdit de transformer un non-`PASS` en autorisation et G13 exige une approbation signee.

Plan rectifie : quatre workstreams atomiques, ordonnes du contrat central vers la prevention de recurrence.

Le depot n'a pas une proliferation generale de 27 faux succes : 22 occurrences ont une justification verifiable. En revanche, les cinq occurrences dangereuses atteignent des artefacts persistants, et le validateur central presente une faiblesse plus large que le scan AST initial.

## 2. Points forts

- [`governance/bias_gate.py:45`] -> le `PASS` est atteint seulement apres elimination explicite des branches `BURNED`, `FAIL` et `INCONCLUSIVE`.
- [`governance/human_evidence.py:61`] -> une approbation humaine pre-OOS est normalisee, rattachee a un sujet attendu et degrade en `INCONCLUSIVE` si la preuve manque.
- [`examples/minimal_pilot_pipeline/build_research_package.py:314`] -> les helpers `_g9_gate_value()` et `_gate_verdict()` degradent les valeurs non reconnues au lieu de fabriquer un succes.
- [`package_validator.py:172`] -> plusieurs coherences transversales sont deja verifiees, notamment le verdict economique et la coherence de la famille WRC.
- [`.ai/archive/20260710_PLAN_CORRECTION_GATE_ECONOMIQUE_CALIBRATION.md:372`] -> les deux constantes `capacity_pass`/`execution_pass` sont une decision humaine explicite et tracee, pas une invention silencieuse de l'implementation courante.

## 3. Points faibles et incoherences

### A1 — Le validateur de gates confond preuve identitaire et verdict

`Implementation/ebta_engine/validators/gate_validator.py:19-53` decrit chaque gate par une simple liste de noms. `_requirement_satisfied()` ne connait pas la nature du champ : seules les chaines `FAIL` et `INCONCLUSIVE` sont refusees ; toute autre chaine non vide est vraie.

Prototype observe sur `G10.economic_report` :

| Valeur injectee | Statut G10 observe |
| --- | --- |
| `FAIL` | `INCONCLUSIVE` |
| `INCONCLUSIVE` | `INCONCLUSIVE` |
| `REJECTED_ECONOMIC` | `PASS` |
| `NOT_VALIDATED` | `PASS` |
| `DENIED` | `PASS` |
| `UNKNOWN` | `PASS` |

Impact : la taxonomie normative de `Implementation/ebta_engine/constants.py:7-15` existe, mais n'est pas consommee par le validateur central. Un statut negatif reconnu ou inconnu peut donc satisfaire un gate par simple truthiness.

Severite : **CRITIQUE**.

### A2 — Le verdict live soumis n'est pas valide et l'approbation est fabriquee

`Implementation/ebta_engine/procedures/incubation_report.py:130-215` declare `_VALID_LIFECYCLE_VERDICTS`, mais `validate_live_deployment_report()` ne refuse ni `FAIL`, ni `INCONCLUSIVE`, ni une valeur inconnue : il retourne `PASS` si les champs structurels passent. Ensuite, `build_research_package.py:1087-1093` injecte `live_approval=True`, et `build_research_package.py:611-614` persiste une seconde fois ce `True` dans G13.

Prototype bout en bout observe avec `live_deployment_report.verdict = "FAIL"` :

```text
submitted_verdict = FAIL
live_deployment.status = PASS
deployment_gate.status = PASS
G13 = PASS
```

Impact : contradiction directe avec `Protocole/SOP 11 - Incubation passage live et monitoring sequentiel.md:44` et avec l'approbation signee exigee par `Protocole/PAQUET D'EXECUTION EBTA.md:179-185`.

Severite : **CRITIQUE**.

### A3 — INV-010 verifie la forme, pas la coherence des verdicts publies

`Implementation/ebta_engine/validators/invariant_validator.py:149-158` verifie seulement la presence des gates statistique/economique et la mention du composant statistique. Il ne compare pas `gate_reports` aux rapports WRC/economique reels. `build_research_package.py:657-660` peut donc persister trois `PASS` litteraux.

Prototype observe avec un gate economique `REJECTED_ECONOMIC` :

```text
reports/economic.json::global_status = REJECTED_ECONOMIC
reports/gates.json::economic_report = INCONCLUSIVE
reports/invariant_evidence.json::gate_reports.economic = PASS
reports/invariant_evidence.json::gate_reports.final = PASS
INV-010 = PASS
```

Le paquet global reste actuellement `FAIL` grace a d'autres controles, mais aucune erreur ne nomme cette contradiction. Un futur changement de surface peut donc rendre le faux invariant decisif.

Severite : **ELEVEE**.

### A4 — Le test canonique preserve explicitement un faux succes

`Implementation/ebta_engine/tests/test_gates.py:71-78` attend que `NOT_VALIDATED` fasse passer G9. Ce test n'est pas une absence de couverture : c'est un cliquet actif sur le comportement dangereux.

Impact : toute correction fail-closed du validateur central devra remplacer cette attente par une preuve negative couvrant la taxonomie complete et les valeurs inconnues.

Severite : **ELEVEE**.

## 4. Triage des 27 litteraux

| Classe | Nombre | Exemples | Decision d'audit |
| --- | ---: | --- | --- |
| Calcul derive | 7 | `bias_gate.py:65`, `economic_gate.py:32`, `robustness.py:56` | Legitimes : le positif est la sortie d'une branche explicite. |
| Valeur attendue de contrat | 7 | `lifecycle.py:14-35` | Legitimes : ce sont des attentes comparees aux preuves, pas des sorties fabriquees. |
| Fixture controlee | 2 | `gate_discrimination_experiment.py:43,155` | Legitimes si l'allowlist exige l'annotation de fixture. |
| Attestation technique non-verdict | 2 | `long_data.py:145`, `nautilus_research_package.py:387` | Hors cible du garde de verdict. |
| Constante humaine documentee | 2 | `economic_calibration.py:51,53` | Dette calibree et autorisee le 2026-07-10 ; garder visible dans une allowlist motivee. |
| Evenement de registre structurel | 2 | `build_research_package.py:300,1197` | A conserver seulement avec justification semantique explicite ; ce n'est pas un gate final. |
| Faux succes actif | 5 | `live_approval` x2 ; `gate_reports` x3 | A supprimer par derivation et validation avant d'installer le garde AST. |

Total : **27**. Le seuil d'escalade etait donc utile, mais une allowlist immediate de 22 lignes aurait masque les defauts de contrat centraux A1 a A3.

## 5. Angles morts et standards

- **Rupture de contrat d'artefact** : `GATE_REQUIREMENTS` ne porte ni type, ni semantique d'acceptation par champ. Mitigation : exigences typees (`identifier`, `verdict_pass`, `boolean_true`, `signed_approval`) avec refus explicite des valeurs inconnues.
- **Couverture de tests** : la suite verte de 246 tests ne prouve pas le fail-closed ; un test attend meme le faux succes `NOT_VALIDATED`. Mitigation : table de tests sur toute la taxonomie et valeurs hors taxonomie.
- **Dependances inversees** : le builder fabrique une approbation au lieu de consommer une preuve validee. Mitigation : faire dependre G13 d'un resultat de validation de preuve humaine, pas d'un literal local.
- **Encapsulation** : INV-010 recoit une copie manuelle des verdicts sans acces aux rapports proprietaires. Mitigation : assembler l'evidence depuis les rapports derives et ajouter une coherence transversale dans `package_validator.py`.
- **Single Responsibility** : `gate_validator.py` essaie de valider avec une unique fonction des identifiants, booleens et verdicts de vocabulaires differents. Mitigation : contrat explicite par exigence, sans heuristique fondee sur la valeur recue.
- **Migration/rollback** : aucun schema persiste n'a besoin d'etre modifie si les cles restent identiques ; les changements peuvent etre livres par petits workstreams reversibles. Toute extension de la preuve live doit conserver les fixtures historiques ou fournir une migration explicite.
- **Monitoring/deploiement progressif** : non applicable a cet audit de code local ; le risque est bloque avant production par les gates, pas par un rollout applicatif.

## 6. Plan d'implementation rectifie

Le test multi-lot de `epic-orchestrator` est positif : les trois corrections ont des Exit criteria independants et le garde de recurrence depend de leur classification finale. Le lot unique `PLAN_GARDE_LITTERAUX_VERDICT` doit etre remplace par quatre workstreams.

### Workstream 3A — `PLAN_CONTRAT_EXIGENCES_GATES_TYPEES`

Objectif : remplacer la truthiness generique par un contrat type par champ, reutiliser la taxonomie runtime et refuser tout verdict autre que `PASS`, y compris inconnu.

Preuves minimales :

- `REJECTED_ECONOMIC`, `NOT_VALIDATED`, `INVALID_TECHNICAL`, `DENIED`, `BURNED`, `WATCH`, `UNKNOWN`, `None`, `False` ne satisfont jamais une exigence `verdict_pass` ;
- les identifiants non vides restent acceptes uniquement sur les champs declares `identifier` ;
- suppression/inversion du test qui attend aujourd'hui le faux succes `NOT_VALIDATED`.

### Workstream 3B — `PLAN_APPROBATION_LIVE_DERIVEE`

Objectif : valider le verdict soumis du rapport live, consommer une approbation de deploiement signee et derivee, puis supprimer les deux `live_approval=True`.

Preuves minimales :

- verdict live `FAIL`, `INCONCLUSIVE`, `WATCH`, `SUSPENDED` ou inconnu interdit `deployment_gate PASS` ;
- preuve absente, mal signee, hors sujet ou fixture non autorisee degrade sans `PASS` ;
- G13 consomme le resultat valide, jamais un booleen fabrique dans le builder.

### Workstream 3C — `PLAN_COHERENCE_VERDICTS_PERSISTES`

Objectif : deriver `invariant_evidence.gate_reports` depuis les rapports proprietaires et verifier leur coherence transversale.

Preuves minimales :

- un economique `REJECTED_ECONOMIC` ne peut produire `gate_reports.economic/final = PASS` ;
- une divergence entre `economic.json`, `gates.json` et `invariant_evidence.json` est nommee et fait echouer le paquet ;
- les trois litteraux `PASS` de `build_research_package.py:657-660` disparaissent.

### Workstream 3D — `PLAN_GARDE_LITTERAUX_VERDICT`

Objectif : seulement apres 3A-3C, installer le garde AST de non-regression avec categories/allowlist annotees.

Preuves minimales :

- fixture positive qui detecte un verdict fabrique dans un sink persiste ;
- fixtures negatives pour calcul derive, valeur attendue de contrat et attestation technique ;
- chaque exception restante porte classe, justification et source de decision ;
- aucun scanner fonde uniquement sur un fragment de nom ne peut devenir une autorite semantique.

Ordre recommande : **3A -> 3B -> 3C -> 3D**. Les trois premiers restent des workstreams fermables independamment ; l'ordre reduit les conflits de fichiers et stabilise l'allowlist finale.

## Points de rupture synthetiques

| Zone | Mecanisme de rupture | Detection actuelle |
| --- | --- | --- |
| `gate_validator.py` | Toute chaine non vide hors vocabulaire minimal devient preuve satisfaite. | Un test documente le comportement au lieu de le bloquer. |
| `incubation_report.py` + builder | Verdict live soumis ignore ; approbation injectee a `True`. | Aucune preuve negative bout en bout avant cet audit. |
| `invariant_validator.py` + builder | Trois verdicts recopies en literals et controles seulement sur leur separation. | Le paquet peut echouer ailleurs, mais la contradiction elle-meme reste invisible. |
| Futurs producteurs | Nouveau literal positif ajoute dans un sink sensible. | Aucun garde AST aujourd'hui. |

## Mecanise et verifie vs procedural

Mecanise et verifie directement :

- la suite canonique execute 246 tests et retourne `OK` ;
- `package_validator.py` bloque deja certains statuts economiques par une verification semantique separee ;
- les preuves humaines pre-OOS manquantes degradent en `INCONCLUSIVE` ;
- les trois prototypes de faux succes ci-dessus sont reproductibles sans modifier le depot.

Reste procedural ou incomplet :

- aucune semantique typee n'attache aujourd'hui chaque exigence G0-G14 a son mode de validation ;
- aucune preuve signee n'alimente `live_approval` dans le pipeline minimal ;
- aucune coherence mecanique ne relie les verdicts recopies dans `invariant_evidence.json` aux rapports proprietaires ;
- aucun garde AST n'empeche la recurrence apres correction.

## Recommandations prioritaires

1. Corriger d'abord le contrat central de gate (3A), car sa surface depasse les cinq literals trouves.
2. Fermer ensuite le faux passage live (3B), risque financier le plus direct et contradiction normative explicite.
3. Fermer la divergence des rapports persistants (3C).
4. Installer enfin le garde AST (3D) sur la classification stabilisee, sans allowlist de confort.

## Non-goals

- aucune modification de `Protocole/` ou `Implementation/`, ni correction executable sous `.ai/` ; seul le journal narratif de l'epic est redimensionne conformement a la decision humaine ;
- aucune nouvelle taxonomie, aucun nouveau gate, seuil ou verdict ;
- aucune modification de BACKTRADER, de GitHub ou des schemas sans plan enfant dedie ;
- aucune interpretation d'un paquet actuellement `FAIL` comme scientifiquement `PASS`.

## Niveau de confiance

- Sur les mecanismes verifies directement : **haute** — code producteur et consommateur lu, exigences normatives recoupees, suite complete executee, trois prototypes comportementaux reproduits, artefacts persistes inspectes.
- Sur l'exhaustivite de la couverture : **moderee a haute pour l'assemblage G0-G14 du pipeline minimal**, moderee pour tout `Implementation/` ; l'audit n'a pas prouve l'absence de tout autre faux succes hors des sinks et vocabulaires explores.
