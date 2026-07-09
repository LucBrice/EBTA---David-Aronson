# EBTA Engine Core

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - RUNTIME_CONTRACT_0.1.0 |
| Runtime | EBTA-ENGINE-0.1.0 |
| Autorite normative | `Protocole/` gele en `EBTA-DOC-1.0` |
| Source operationnelle | `Protocole/PAQUET D'EXECUTION EBTA.md` |
| Historique runtime | `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |

## Frontiere d'autorite

`Implementation/` encode des contrats executables. Il ne cree aucune norme EBTA.

Ordre d'autorite:

1. `Protocole/MANIFESTE DE GEL EBTA.md`
2. `Protocole/PROTOCOLE EBTA.md`
3. `Protocole/REGISTRE DES DECISIONS NORMATIVES EBTA.md`
4. SOP proprietaires
5. `Protocole/PAQUET D'EXECUTION EBTA.md`
6. `Implementation/`
7. adaptateurs externes

Si le runtime contredit `Protocole/`, le runtime est faux. Si une regle manque,
le runtime bloque ou marque le controle comme `INCONCLUSIVE` /
`DEFERRED_REQUIRES_PIPELINE_DATA`.

## Choix d'implementation

- Langage: Python 3, standard library first.
- Tests: `unittest`.
- Schémas: JSON Schema minimal documente, valide par un validateur interne
  restreint aux mots-cles utilises.
- Persistance: fichiers explicites dans un paquet EBTA, sans base de donnees
  normative.

## Etat courant

`EBTA-ENGINE-0.1.x` est un banc de controle local pour paquets EBTA minimaux et
un runtime de simulation pilote via NautilusTrader. Il inclut schemas, fixtures,
validateurs de paquet, manifestes, gates, invariants, persistance fichier,
decomposition E-I, loader CSV local, frontiere d'adapter Nautilus et frontiere
d'adaptateur BACKTRADER historique.

BACKTRADER est reference historique en lecture seule, pas dependance runtime.
Le chemin actif est la production d'un `research_package/` par l'adapter
Nautilus puis la validation par `validate_package_dir()`.

## Versions et compatibilite

| EBTA-DOC | EBTA-ENGINE | Schemas | Stades supportes |
| --- | --- | --- | --- |
| EBTA-DOC-1.0 | EBTA-ENGINE-0.1.0 | 1.0.0 | `PRE_OOS_SEALED`, `VALIDATION_READY`, `DEPLOYMENT_CERTIFIED`, `LIFECYCLE_ARCHIVED` |

Regles:

- `EBTA-DOC-*` reste la version normative.
- `EBTA-ENGINE-*` versionne uniquement le runtime.
- Tout artefact persistant porte `schema_version` quand il est produit par le
  runtime.
- Une evolution compatible incremente la version mineure du schema.
- Une evolution cassante exige une version majeure ou une migration explicite.
- Un paquet d'une version non supportee est rejete explicitement.

## Migrations

Les migrations vivent dans `Implementation/ebta_engine/migrations/`.

Regles:

- deterministes et testees;
- sans changement de signification normative;
- sans perte d'information sauf decision explicite;
- journalisees dans l'historique runtime.

## Quality gate

Commande de validation transversale:

```powershell
python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation
```

Cette gate couvre:

- validation des schemas et fixtures;
- generation et verification de manifestes SHA-256;
- invariants executables;
- rapports de gates;
- hashes du protocole gele;
- matrice de tracabilite;
- adapter Nautilus E-I ;
- frontiere d'adaptateur BACKTRADER future.

## Modele de paquet EBTA minimal

```text
research_package/
  config.json
  registry.jsonl
  oos_access_log.jsonl
  reports/
  series/
  manifests/
```

Les journaux critiques sont append-only au niveau contractuel. Le runtime lit les
artefacts comme donnees non fiables et produit des erreurs contractuelles
explicites.

## Frontiere de confiance

L'adapter Nautilus produit les series de simulation et laisse le noyau EBTA
valider le contrat. Tout moteur externe reste traite comme une source non
fiable : ses sorties sont mappees vers les artefacts EBTA, puis le noyau EBTA
valide. Il ne corrigera pas silencieusement les erreurs de mapping et n'importera
pas les conventions du pipeline externe dans la norme EBTA.
