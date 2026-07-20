# Brouillon - R7 reproductibilite operationnelle

## Objectif

Rendre le build Nautilus reproductible sur une autre machine sans modifier la
norme EBTA : resolution explicite du data root, empreinte deterministe de la
configuration effective et procedure unique de recreation/verification du venv.

## Constats verifies le 2026-07-20

- `Implementation/ebta_engine/data/local_ohlcv.py` fixe
  `DEFAULT_DATA_ROOT` a un chemin Windows absolu propre a cette machine.
- `build_nautilus_inputs()` accepte deja `data_root`, mais le point d'entree
  `main()` depend du defaut importe et aucun resolver explicite ne permet une
  variable d'environnement.
- `nautilus_research_package.py` ecrit
  `NAUTILUS_MVP_CONFIG_HASH_PLACEHOLDER` dans `document_hash`.
- `setup_env.ps1` sait creer une venv depuis `requirements.txt`, mais son
  defaut (`Implementation/.venv-nautilus`) differe du venv historique utilise
  par les commandes du repo (`Implementation/adapters/nautilus_env/venv`).

## Source normative et classification

- Autorite : SOP 12, notamment reproductibilite des donnees, du code, de
  l'environnement et de la configuration.
- Classification : `IMPLEMENTATION_DETAIL` / encodage executable d'une exigence
  deja normative.
- Aucun changement de `Protocole/`, schema JSON ou API Nautilus.

## Architecture cible

1. Ajouter dans `local_ohlcv.py` un resolver pur du data root avec precedence
   explicite : argument fourni par l'appelant, puis variable d'environnement
   `EBTA_DATA_ROOT`, puis defaut local historique pour compatibilite. Le resolver
   accepte un mapping d'environnement injecte en test ; il ne capture pas
   `os.environ` dans un argument par defaut.
2. Conserver les fonctions de lecture existantes avec un `Path` explicite ; ne
   pas leur faire relire implicitement l'environnement a chaque appel.
3. Remplacer les signatures `data_root: Path = DEFAULT_DATA_ROOT` des deux
   points de build par `data_root: Path | None = None`. Une valeur par defaut
   liee a l'import empecherait `EBTA_DATA_ROOT` d'agir. Resoudre une seule fois
   au debut de `build_nautilus_inputs()` et propager le `Path` effectif.
4. Dans `nautilus_research_package.py`, calculer un SHA-256 deterministe sur un
   document canonique de configuration preenregistree, sans inclure le champ
   `document_hash` lui-meme ni les resultats de simulation. Le payload ferme
   inclut : version du format d'empreinte ; identifiants immuables hors hash ;
   assets et fenetre demandee ; calendrier Walk-Forward ; espace candidat ;
   regle de selection ; plan statistique ; modele d'execution ; grille de
   robustesse declaree ; gate OOS ; plan d'incubation ; manifeste de
   reproductibilite. Le chemin absolu local et les sorties calculees sont exclus.
   Le checksum du snapshot demeure la preuve distincte du contenu des donnees.
   La serialisation est explicite (`sort_keys=True`, separateurs compacts,
   UTF-8, prefixe de version) pour ne pas dependre de l'indentation ou de
   l'ordre d'insertion des dictionnaires.
5. Calculer l'empreinte apres assemblage des choix preenregistres (dont le
   calendrier) mais avant utilisation comme identifiant dans les registres ; ne
   jamais hasher l'objet `inputs` entier, qui contient ensuite des resultats OOS.
6. Ajouter un guide court et executable dans `nautilus_env/` qui documente la
   creation depuis zero, la recreation, la verification de version et le build,
   sans committer le venv. Aligner `setup_env.ps1` et son wrapper sur le chemin
   canonique deja utilise par les commandes du repo
   (`Implementation/adapters/nautilus_env/venv`) afin d'eviter deux venv lourdes.

## Perimetre ferme

Fichiers autorises :

- `Implementation/ebta_engine/data/local_ohlcv.py`
- `Implementation/ebta_engine/package_builder/nautilus_research_package.py`
- `Implementation/ebta_engine/tests/test_nautilus_research_package.py`
- `Implementation/ebta_engine/tests/test_local_ohlcv.py` (creer)
- `Implementation/adapters/nautilus_env/setup_env.ps1`
- `Implementation/adapters/nautilus_env/setup_nautilus_env.ps1`
- `Implementation/adapters/nautilus_env/README.md`
- `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md`

Fichiers interdits : `Protocole/`, schemas, contrats de strategie, mapping API
Nautilus, research packages persistants (regeneration reservee a la preuve
globale du chantier mere).

## Phases

1. Tests rouges : precedence du resolver, absence de placeholder, stabilite et
   sensibilite du hash (meme config = meme hash ; changement d'un parametre de
   recherche = hash different ; changement du chemin local seul = meme hash).
   Verifier aussi que `build_nautilus_inputs(data_root=None)` utilise le resolver,
   pas seulement que le helper isole fonctionne.
2. Implementer le resolver et le hash canonique, sans nouvelle dependance.
3. Documenter la recreation du venv et journaliser le changement runtime.
4. Executer tests cibles, suite complete, Pyrefly/bug-hunter puis audit de
   conformite avant cloture.

## Exit criteria

- `EBTA_DATA_ROOT` est pris en compte lorsqu'aucun argument explicite n'est
  donne ; un argument explicite garde la priorite ; le defaut historique reste
  disponible pour compatibilite locale.
- Le chemin de production n'emet plus le placeholder et produit un SHA-256
  deterministe de 64 caracteres sur la configuration effective.
- Le test prouve stabilite et sensibilite du hash, et son independance au chemin
  absolu local ; le checksum de donnees reste la preuve du contenu source.
- Les deux scripts partagent le meme chemin canonique par defaut ; une commande
  documentee recree et verifie la venv depuis `requirements.txt` et le smoke
  `-SkipInstall` passe sur l'environnement existant.
- Tests cibles et suite runtime complete PASS ; aucun changement normatif.

## Non-objectifs / NO GO

- Ne pas calibrer couts, slippage, latence ou stress R5/R6.
- Ne pas modifier les valeurs, gates ou schemas du protocole.
- Ne pas hasher les resultats produits apres simulation ni creer une boucle
  auto-referentielle sur `document_hash`.
- Ne pas committer une venv ou introduire une dependance.
- Ne pas modifier les APIs Nautilus ni leur mapping.

## Decision humaine deja actee

Le 2026-07-20, l'humain a demande l'execution du chantier mere multi-lot et a
delegue l'ordre R7 -> R5/R6 -> horodatage -> R4-long. Ce brouillon est le Lot
1/4 `PLAN_REPRODUCTIBILITE_OPERATIONNELLE_R7`.

## Journal des passes `/evaluate`

- 2026-07-20 - Passe 1 : plan juge pertinent mais incomplet. Corrections :
  signatures de build rendues nullable pour ne pas figer le defaut a l'import ;
  payload d'empreinte ferme et moment de calcul explicites ; test d'integration
  du resolver ajoute ; scripts `setup_env.ps1` inclus au perimetre pour resoudre
  la divergence de chemins plutot que la documenter seulement.
- 2026-07-20 - Passe 2 : aucun nouvel angle mort majeur. Precision ajoutee sur
  la canonicalisation JSON et le versionnement du payload d'empreinte. Le plan
  converge : aucune migration de schema/donnee, aucune API externe modifiee,
  compatibilite ascendante conservee par le fallback historique et preuves
  ciblees definies pour chaque frontiere.
