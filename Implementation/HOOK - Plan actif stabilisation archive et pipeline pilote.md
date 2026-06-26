# HOOK - Plan actif stabilisation archive et pipeline pilote

## Statut

| Champ | Valeur |
| --- | --- |
| Statut | ACTIF - PLAN_DE_TRAVAIL_RUNTIME |
| Date de creation | 2026-06-26 |
| Version runtime cible | EBTA-ENGINE-0.1.0 |
| Autorite normative | `Protocole/` gele en `EBTA-DOC-1.0` |
| Source operationnelle | `Implementation/ebta_engine/` |
| Fichier de suivi | `Implementation/task_tracking.json` |
| Historique runtime | `Implementation/HISTORIQUE DES VERSIONS EBTA ENGINE.md` |

## Objectif

Stabiliser le lot runtime EBTA deja produit, archiver les elements obsoletes
avant le checkpoint, puis preparer un pipeline pilote local capable de produire
un vrai `research_package/` valide par le banc de controle EBTA.

Ce hook ne modifie pas le protocole EBTA. Il organise la suite du travail autour
de `Implementation/` comme traduction executable subordonnee au dossier
`Protocole/`.

## Ordre de travail

```text
Etape 0 - Archivage controle des obsoletes
        |
        v
Etape 1 - Checkpoint du lot actuel
        |
        v
Etape 2 - Pipeline pilote EBTA reel local
        |
        v
Etape 3 - Integration BACKTRADER apres lecture de sa gouvernance locale
```

## Etape 0 - Archivage controle des obsoletes

Objectif : nettoyer la surface de reprise sans perdre l'historique utile.

Actions :

- inventorier les dossiers et fichiers candidats a l'archive ;
- classer chaque element en `ACTIF`, `ARCHIVE_CANDIDATE`,
  `OBSOLETE_BUT_REFERENCED` ou `DELETE_NEVER` ;
- rechercher les references avant tout deplacement ;
- archiver au lieu de supprimer ;
- separer les archives protocole et runtime ;
- journaliser tout archivage significatif.

Regles :

- ne pas archiver une source active ;
- ne pas casser les liens depuis les documents actifs ;
- ne pas supprimer l'historique qui explique une decision EBTA ;
- ne pas deplacer un fichier gele de `Protocole/` sans procedure documentaire
  explicite.

Sortie attendue :

- liste des elements archives ou conserves ;
- justification courte par element ;
- liens actifs verifies ou corriges ;
- validation `git diff --check`.

### Hooks et plans termines

Les hooks, plans et contextes termines doivent etre classes pendant l'etape 0
avant tout deplacement.

Regle :

- un hook ou plan termine peut etre archive physiquement si tous les pointeurs
  actifs sont corriges dans le meme lot ;
- les references historiques peuvent rester dans l'historique runtime quand
  elles decrivent le chemin utilise au moment de l'ancien changement ;
- le plan actif courant est ce fichier avec `Implementation/task_tracking.json`.

Classification courante :

| Artefact | Statut courant | Action |
| --- | --- | --- |
| `Implementation/Archives/completed_2026-06-26/HOOK - Reprise EBTA Engine Core autonome.md` | ARCHIVED_REFERENCED | Ancien hook termine, archive; le skill Gardien et le protocole pointent maintenant vers le hook actif. |
| `Implementation/Archives/completed_2026-06-26/PLAN - Procedures de calcul EBTA et optimisation ML.md` | ARCHIVED_REFERENCED | Ancien plan termine, archive; la matrice, la carte et les tests pointent vers l'archive. |
| `Implementation/Archives/completed_2026-06-26/implementation_context.json` | ARCHIVED_REFERENCED | Ancien contexte IA du lot procedures, archive; le suivi actif est `task_tracking.json`. |
| `Implementation/HOOK - Plan actif stabilisation archive et pipeline pilote.md` | ACTIVE | Hook de travail courant. |
| `Implementation/task_tracking.json` | ACTIVE | Suivi machine-readable courant. |

## Etape 1 - Checkpoint du lot actuel

Objectif : confirmer que le runtime existant est stable avant tout nouveau
developpement.

Actions :

- auditer le diff courant ;
- verifier que `Implementation/` ne cree aucune norme concurrente ;
- rejouer les tests runtime ;
- reconstruire le paquet pilote minimal ;
- verifier la proprete du diff ;
- identifier les risques residuels.

Definition de fini :

- `python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation`
  passe ;
- `python Implementation\examples\minimal_pilot_pipeline\build_research_package.py`
  produit un paquet `PASS` ;
- `git diff --check -- Implementation Protocole` passe ;
- les risques sont classes en `GO`, `LOCAL_FIX_REQUIRED` ou
  `NORMATIVE_CLARIFICATION_REQUIRED`.

## Etape 2 - Pipeline pilote EBTA reel local

Objectif : passer d'une fixture controlee a un pipeline local minimal qui
genere un `research_package/` depuis des entrees concretes.

Actions :

- definir les inputs pilotes ;
- produire les artefacts EBTA attendus par `validate_package_dir()` ;
- connecter les modules de procedure existants ;
- maintenir les statuts `DEFERRED_REQUIRES_PIPELINE_DATA` quand la preuve
  manque ;
- ajouter des tests limites au comportement pilote.

Non-objectifs :

- pas de donnees live ;
- pas d'ouverture OOS opportuniste ;
- pas de regle alpha nouvelle dans le protocole ;
- pas d'integration BACKTRADER tant que l'etape 2 n'est pas stabilisee ou que
  la gouvernance BACKTRADER n'est pas lue.

## Etape 3 - Integration BACKTRADER

Objectif : brancher BACKTRADER seulement apres stabilisation locale et lecture
de sa gouvernance.

Preconditions :

- le checkpoint runtime est `GO` ;
- le mapping local existe dans `Implementation/EXTERNAL_ENGINE_PROCEDURE_MAPPING.md` ;
- la gouvernance locale BACKTRADER a ete lue ;
- aucune dette BACKTRADER n'est importee comme norme EBTA.

Sortie attendue :

- BACKTRADER produit ou consomme des artefacts EBTA conformes ;
- les erreurs de contrat sont explicites ;
- l'historique runtime documente le mapping effectif.

## Politique de blocage

Bloquer et classer `NORMATIVE_CLARIFICATION_REQUIRED` si une action exige :

- un nouveau gate EBTA ;
- un nouveau statut normatif ;
- un changement d'ordre des gates ;
- un seuil methodologique absent du protocole ;
- une definition nouvelle de candidate, OOS, robustesse, WRC ou verdict.

Dans ce cas, ne pas coder la regle dans `Implementation/`. Ouvrir d'abord une
clarification documentaire controlee.

## Commandes de validation

```powershell
python -m json.tool Implementation\task_tracking.json
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
python Implementation\examples\minimal_pilot_pipeline\build_research_package.py
git diff --check -- Implementation Protocole
```

## Reprise rapide

1. Lire ce hook.
2. Lire `Implementation/task_tracking.json`.
3. Si `current_step` vaut `STEP_0_ARCHIVE_OBSOLETE`, commencer par l'inventaire
   et ne pas creer de pipeline.
4. Apres chaque deplacement ou modification significative, relancer les
   validations pertinentes.
5. Mettre a jour le JSON de suivi et l'historique runtime.
