# Workflow `interface`

**PLANNED — non demarre.**

Ce fichier est un emplacement reserve, pas une procedure executable. Il ne
contient aucun gate, verdict, budget ou sequence de travail actif.
`WORKFLOW.json` encode cet etat avec un unique stage terminal `PLANNED` et
aucune transition. `.ai/tools/plan.ps1 start -Workflow interface` le refuse
mecaniquement tant que le contrat n'est pas explicitement active par un
chantier gouverne.

Deux brouillons `INTAKE` se recoupent et devront etre audites puis arbitres
ensemble avant toute formalisation :

- `0 - HUMAN START HERE/PROPOSITION_INTERFACE_PILOTAGE_VISUEL_RECHERCHE_EBTA.md`
  (decisions D1-D15 non tranchees) ;
- `0 - HUMAN START HERE/PROPOSITION_WORKFLOW_VALIDATION_UX_EBTA.md`
  (proposition de workflow de validation UX non auditee).

## Contradiction rendue visible, non resolue

Le second brouillon decrit cinq roles d'agents, tandis que la gouvernance
actuelle repose sur une seule IA executante supervisee. Il s'agit d'un
`STRUCTURAL_CONFLICT` au sens de
`.ai/governance/CONFLICT_RESOLUTION_POLICY.md`. Documenter cette tension ne
la resout pas ; l'arbitrage est differe au demarrage reel du workflow.

## Frontiere adversariale a arbitrer

Le pattern D4/G0 de verrouillage serveur pourra relever d'un futur gate
adversarial UX. `adversarial-tester` couvre aujourd'hui le code moteur et le
pattern de succes fabrique/repli silencieux ; il ne faut ni lui attribuer
automatiquement la validation frontend, ni creer un second gate concurrent
avant l'audit des deux brouillons.

Toute activation future passe par le cycle universel `/start` de
`AGENTS.md`. Ne recopier aucune regle des brouillons dans ce fichier avant
leur promotion gouvernee.
