# Brouillon — Recherche des consommateurs contractuels pendant `/evaluate`

> Sous-chantier 1/3 de
> `EPIC_AMELIORATIONS_POST_RETROSPECTIVE_CI_NODE20`. Ce brouillon est un
> intake autonome, non executable avant son propre `/start`, sa double boucle
> `/evaluate` post-route et sa baseline.

## Objectif

Durcir `.agents/skills/code-architecture-evaluator/SKILL.md` pour qu'un audit
de plan qui modifie un workflow, une configuration, un schema, un manifeste
ou un autre contrat persiste recherche explicitement les producteurs,
consommateurs et tests qui figent ses valeurs avant de declarer le plan
coherent.

## Constat revalide dans le depot live

- Le skill contient deja une analyse d'impact generale, une verification des
  dependances cachees et une checklist de couverture de tests.
- Il ne contient aucune gate explicite qui oblige a rechercher par nom de
  fichier, cle, valeur, fonction ou identifiant les consommateurs qui figent
  le contrat vise.
- Cette absence a permis au premier plan CI Node.js 20 de traiter cinq
  substitutions YAML comme une modification `GOVERNANCE/common`, alors que
  `Implementation/ebta_engine/tests/test_ci_supply_chain.py` figeait les SHA
  et imposait un lot `CONTRACT_ENCODING/core-engine`.
- Les consommateurs directs du skill sont proceduraux :
  `.ai/workflows/common/WORKFLOW.md` impose `/evaluate`, et
  `.agents/skills/epic-orchestrator/SKILL.md` l'impose avant et apres routage
  de chaque lot. Ils restent en lecture seule dans ce sous-chantier.
- Le validateur canonique disponible dans l'environnement courant est
  `C:/Users/liant/.codex/skills/.system/skill-creator/scripts/quick_validate.py`;
  il valide deja le skill actuel avec `Skill is valid!`.

## Changement propose

Ajouter une gate concise et generalisable dans le flux de travail du skill :

1. La declencher pour tout plan touchant un workflow, une configuration, un
   schema, un manifeste, un format serialise, une enum ou une valeur de
   contrat.
2. Rechercher les producteurs, appelants, lecteurs, validateurs, tests,
   fixtures, snapshots et CI qui citent ou figent ce contrat.
3. Citer dans le rapport les consommateurs trouves et l'impact attendu; ne pas
   conclure `VALIDE` si la recherche requise n'a pas pu etre executee.
4. Garder la regle courte, generique et compatible avec la structure actuelle
   du skill; ne pas recopier l'incident CI EBTA dans l'instruction durable.
5. Conserver le frontmatter existant, employer la forme imperative et garder
   `SKILL.md` sous la recommandation de 500 lignes du skill `skill-creator`.

## Perimetre

Autorise :

```text
.agents/skills/code-architecture-evaluator/SKILL.md
```

Lecture seule :

```text
.ai/workflows/common/WORKFLOW.md
.agents/skills/epic-orchestrator/SKILL.md
.agents/skills/code-architecture-evaluator/*
.ai/archive/20260809_PLAN_CORRECTION_CI_NODE20_DEPRECATION_ACTIONS.md
.ai/archive/20260809_PLAN_CORRECTION_CI_NODE20_DEPRECATION_CORE_ENGINE.md
Implementation/ebta_engine/tests/test_ci_supply_chain.py
```

## Non-objectifs

- Ne pas creer un nouveau skill, script ou test dans le depot.
- Ne pas modifier les fichiers auxiliaires historiques du dossier du skill.
- Ne pas specialiser la regle pour EBTA, GitHub Actions ou Node.js.
- Ne pas imposer une technologie de recherche precise quand `rg`, une lecture
  directe ou un autre outil adapte suffit.
- Ne pas modifier `Protocole/`, `Implementation/`, `.ai/workflows/` ou le
  schema du checkpoint.
- Ne pas committer ni pousser sans l'autorisation gouvernee correspondante.

## Exit criteria

1. Le skill exige explicitement le scan des consommateurs contractuels pour
   les categories de contrats enumerees dans l'objectif.
2. L'instruction couvre producteurs, lecteurs/appelants, validateurs, tests,
   fixtures, snapshots et CI, et exige une preuve citee dans le rapport.
3. Une recherche impossible ou incomplete interdit une conclusion `VALIDE`
   sans incertitude explicite.
4. Le validateur `skill-creator/scripts/quick_validate.py` retourne
   `Skill is valid!` sur le dossier cible.
5. Un forward-test sur un plan de modification de workflow montre que
   l'evaluateur inspecte le test contractuel correspondant avant de conclure.
6. Le frontmatter reste valide, la nouvelle instruction est a l'imperatif et
   `SKILL.md` reste sous 500 lignes.
7. Aucun fichier hors perimetre n'est modifie.

## Decisions humaines heritees

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-09 | `Je valide tes propositions`, puis `/continue`. | Autorise l'execution gouvernee du Lot 1 dans le cadre du chantier mere. N'autorise aucun push. |

## Journal de convergence de l'intake

| Passe | Constat | Correction | Resultat |
| --- | --- | --- | --- |
| `/evaluate` 1 | `VALIDE`, risque modere. Le manque est confirme dans `SKILL.md` : les mentions actuelles de couverture, dependances cachees et dependances inversees sont des angles d'analyse generaux, pas une gate de recherche des consommateurs avant classification. Le brouillon omettait toutefois les contraintes de forme et de taille du skill `skill-creator`. Migration, deploiement et monitoring sont non applicables; rupture de contrat, tests, dependances inversees et documentation sont couverts. | Ajout de la preservation du frontmatter, de la forme imperative et de la limite recommandee de 500 lignes; Exit criteria etendu en consequence. | Corrections appliquees; seconde passe requise. |
| `/evaluate` 2 | Contre-audit du brouillon corrige contre le skill cible, ses consommateurs proceduraux, l'incident CI source et `skill-creator`. Les sept Exit criteria sont binaires ou preuves par une commande/trace; le plan reste `SINGLE`, car ses etapes sont sequentielles et un seul changement de `SKILL.md` les couvre. Aucun nouveau risque de contrat, de test ou de deploiement n'est ouvert. | Aucune correction supplementaire. | `CONVERGE` en 2 passes; aucun angle mort majeur restant. |
