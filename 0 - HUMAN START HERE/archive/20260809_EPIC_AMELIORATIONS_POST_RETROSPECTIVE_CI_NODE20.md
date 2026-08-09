# Brouillon — Chantier mere des ameliorations post-retrospective CI Node.js 20

> Statut : `INTAKE` humain valide en conversation le 2026-08-09. Ce document
> coordonne trois sous-chantiers independants. Il n'est ni audite via
> `/evaluate`, ni route via `/start`, ni executable par sa seule existence.

## 0. Bandeau de statut

| Question | Reponse |
| --- | --- |
| Un chantier actif couvre-t-il ce perimetre ? | Non dans le checkout local : `.ai/checkpoint.json::active_workstream_id` vaut `null`. Le distant `origin/main` porte encore l'etat `ACTIVE` du chantier CI, car le commit local de fermeture `0d70f77` n'est pas publie. |
| Une decision normative EBTA est-elle requise ? | Non. Aucun lot ne touche `Protocole/`, une SOP, un seuil, un gate scientifique ou un verdict EBTA. |
| Une decision humaine a-t-elle ete donnee ? | Oui. Apres la retrospective du correctif CI Node.js 20, l'humain a repondu `Je valide tes propositions`, autorisant leur persistance. Cette autorisation ne vaut ni commit, ni push. |
| Resultat du test multi-lot | `MULTI_LOT` : chacun des trois lots a un Exit criteria autonome, peut etre execute dans un ordre different et peut bloquer sans empecher les autres. Toute implementation groupee est interdite. |

## 1. Role du chantier mere

Conserver un point d'ancrage unique pour trois ameliorations durables issues de
la session bornee par les commits `704af88` (base), `54e00f4`
(implementation CI publiee) et `0d70f77` (fermeture locale).

Le chantier mere coordonne uniquement. Il ne modifie aucun des proprietaires
cibles et ne duplique pas le contenu detaille des futurs plans de lot.

## 2. Lots independants

| Ordre propose | Lot | Nature revalidee | Proprietaire cible | Exit criteria autonome |
| --- | --- | --- | --- | --- |
| 1 | Recherche des consommateurs contractuels pendant `/evaluate` | Amelioration de skill | `.agents/skills/code-architecture-evaluator/SKILL.md` | Un plan qui modifie un workflow, une configuration, un schema ou un manifeste declenche une recherche explicite des tests/consommateurs qui figent ses valeurs; le skill reste valide avec `quick_validate.py`. |
| 2 | Autorisation explicite du cycle de publication a deux pushes | Regle conversationnelle de workflow | `.ai/workflows/common/WORKFLOW.md` | Pour tout gate distant exigeant un premier push avant `/close`, la demande d'autorisation distingue explicitement le push d'implementation et l'eventuel push conditionnel du commit de fermeture; aucune autorisation implicite ni modification de `WORKFLOW.json`. |
| 3 | Diagnostic actionnable des ancres de preuve invalides | Correctif mecanique et tests | `.ai/tools/workflow_state.ps1` et `.ai/tools/tests/test_workflow_state_machine.ps1` | Une ancre absente reste rejetee, mais l'erreur expose le slug recherche et les slugs de titres valides; tests positif et negatif `PASS`, sans affaiblir `Test-EvidenceReferenceSubstance`. |

## 3. Preuves sources

- Le plan initial `GOVERNANCE/common` a produit un `FAIL` canonique 2/292 :
  `Implementation/ebta_engine/tests/test_ci_supply_chain.py` figeait les SHA
  et imposait une reclassification `CONTRACT_ENCODING/core-engine`.
- Deux appels `plan.ps1 ready` ont ete rejetes avant de retrouver l'ancre
  exacte `#14-journal-daudits-post-hoc`.
- G7 a exige le push de `54e00f4`; `/close` a ensuite cree `0d70f77`. Le
  distant porte donc encore le workstream `ACTIVE`, tandis que le checkout
  local le porte `DONE`.

Ces faits sont documentes dans :

- `.ai/archive/20260809_PLAN_CORRECTION_CI_NODE20_DEPRECATION_ACTIONS.md` ;
- `.ai/archive/20260809_PLAN_CORRECTION_CI_NODE20_DEPRECATION_CORE_ENGINE.md` ;
- le run GitHub Actions `31318437757`.

## 4. Ordre et coordination

Ordre propose : Lot 1, puis Lot 2, puis Lot 3.

Justification :

1. prevenir une mauvaise classification en amont avant d'optimiser les
   transitions de fin de cycle ;
2. clarifier ensuite la frontiere d'autorisation qui conditionne la
   publication et la cloture ;
3. terminer par l'ergonomie du validateur, independante des deux decisions
   procedurales.

Cet ordre n'est pas une dependance technique. Chaque lot suit son propre cycle
`/start -> /evaluate x2 -> baseline -> /continue -> audits -> /close` et son
propre commit. Deux lots ne doivent jamais etre fusionnes dans un commit ou une
cloture.

## 5. Collision et precedences a respecter

Le brouillon humain non suivi
`0 - HUMAN START HERE/PLAN_INTEGRATION_LEARN_SESSION_POST_CLOSE.md` envisage
egalement une modification de `.ai/workflows/common/WORKFLOW.md`, sur une autre
section et pour un autre objectif. Il reste intact et n'est pas absorbe par ce
chantier.

Avant d'executer le Lot 2 :

- re-lire ce brouillon et le checkpoint live ;
- verifier si son propre chantier a ete route ou implemente entre-temps ;
- rebaseliner le plan du Lot 2 sur le contenu courant de `WORKFLOW.md` ;
- ne jamais melanger l'automatisation de `/learn-session` avec le contrat des
  deux pushes dans un meme lot ou commit.

## 6. Invariants et non-objectifs

- Aucun changement de `Protocole/`, `Implementation/`, BACKTRADER ou schema du
  checkpoint.
- Aucun nouveau skill : le Lot 1 ameliore un proprietaire existant.
- Aucun changement de `.ai/workflows/common/WORKFLOW.json` ou Mermaid pour le
  Lot 2.
- Le Lot 3 ne relache jamais le rejet d'une preuve absente, hors depot ou a
  ancre invalide.
- Aucune persistance dans une memoire personnelle ou un registre de sessions.
- Aucune modification des autres fichiers humains non suivis ou supprimes du
  worktree mixte.
- La validation humaine des propositions n'autorise ni commit, ni push, ni
  publication externe.

## 7. Risques

| Risque | Mitigation |
| --- | --- |
| Une amelioration retrospective devient une implementation groupee hors workflow | Le chantier mere est non executable; chaque lot possede un brouillon, un workstream et une cloture distincts. |
| Le Lot 1 rend `code-architecture-evaluator` trop verbeux ou trop specialise EBTA | Ajouter une regle concise et generalisable de recherche des consommateurs, sans recopier l'incident CI. |
| Le Lot 2 elargit implicitement une autorisation de push | Exiger une portee textuelle explicite pour chacun des deux pushes possibles; le choix par defaut reste le premier push seulement. |
| Le Lot 3 divulgue trop de contenu dans un message d'erreur | Afficher uniquement des slugs de titres, jamais le contenu des preuves. |
| Le brouillon `/learn-session` et le Lot 2 se modifient en parallele | Execution sequentielle et relecture live avant baseline du Lot 2. |

## 8. Decisions humaines

| Date | Decision | Portee |
| --- | --- | --- |
| 2026-08-09 | `Je valide tes propositions`. | Autorise la persistance de ce chantier mere et confirme les trois orientations. Ne vaut pas autorisation de commit ou de push. |

## 9. Suite immediate

1. Lancer `/start` sur ce chantier mere si l'humain veut ouvrir le cycle
   gouverne.
2. Apres promotion et baseline du chantier mere, creer uniquement le brouillon
   du Lot 1 et appliquer sa boucle complete.
3. Mettre a jour ce chantier mere apres chaque fermeture de lot, sans y coder
   le contenu du lot suivant.

## 10. Critere de cloture du chantier mere

- Les trois lots sont `DONE` ou explicitement differes par decision humaine.
- Leurs diffs et commits restent distincts.
- L'audit final couvre l'union des fichiers touches depuis la baseline du
  chantier mere.
- Aucun fichier humain parallele n'a ete absorbe ou modifie.
