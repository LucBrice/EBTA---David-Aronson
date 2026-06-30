# Knowledge Intake Policy

## Objectif

Cette politique definit comment une nouvelle connaissance entre dans le systeme
EBTA avant toute promotion vers le protocole, le runtime ou le backlog.

Une connaissance brute ne peut jamais modifier directement un SOP. Une source
externe ne devient pas automatiquement une regle EBTA. Une note utilisateur peut
declencher une analyse, mais pas une modification normative automatique.

## Taxonomie minimale

- `RAW_NOTE` : note brute, idee non validee, extrait de lecture, intuition
  utilisateur.
- `SOURCE_SUMMARY` : resume fidele d'une source, sans decision normative.
- `CANDIDATE_RULE` : regle candidate, non encore validee.
- `NORMATIVE_CHANGE_REQUEST` : demande explicite de changement du protocole.
- `IMPLEMENTATION_CHANGE_REQUEST` : demande de modification du code ou de
  l'architecture technique.
- `CONFLICT_REPORT` : contradiction detectee entre sources, SOP, protocole ou
  code.
- `ANNEX_ONLY` : connaissance utile mais non normative.

## Pipeline

```text
Intake -> Classification -> Scope detection -> Authority check -> Conflict check -> Human decision if normative -> Implementation impact check -> Traceability update -> Archive or backlog
```

## Regles de traitement

1. Classer l'entree avant toute modification.
2. Identifier si elle concerne `.ai/`, `Protocole/`, `Implementation/`,
   `.agents/`, `.codex/` ou un autre dossier.
3. Identifier les fichiers probablement impactes.
4. Si la connaissance concerne plusieurs SOP, l'IA doit identifier les SOP
   impactes avant modification.
5. Verifier l'autorite applicable dans `Protocole/0-README - Comprendre et
   maintenir le protocole EBTA.md`, puis dans les registres et SOP concernes.
6. Si un SOP n'est pas encore fige, il ne peut pas servir d'autorite contre un
   SOP deja fige.
7. Si la connaissance contredit un element fige, creer un conflit ou une demande
   de decision humaine.
8. Si l'entree implique `Implementation/`, verifier l'impact dans
   `Implementation/TRACEABILITY_MATRIX.md` quand la matrice existe.
9. Router l'entree vers l'archive ou le backlog selon les conventions de
   `.ai/README.md`.

## Decision humaine

Une decision humaine est requise quand l'entree :

- modifie une regle EBTA ;
- change l'ordre, le sens ou l'autorite d'un gate ;
- contredit un element fige ;
- transforme une source externe en doctrine EBTA ;
- necessite d'ouvrir une nouvelle version documentaire.

## Template d'intake

```md
# Knowledge Intake

## Source
## Type
## Resume neutre
## Fichiers probablement impactes
## SOP concernes
## Statut normatif actuel
## Conflits possibles
## Decision humaine requise ?
## Action recommandee
```

