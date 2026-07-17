# Exemple reel : EPIC_CLOTURE_ATTESTATIONS_RESIDUELLES_GATES

Cet exemple documente la premiere application reelle de ce skill (avant meme
que le skill lui-meme n'existe sous cette forme — c'est cette session qui en
a motive l'ecriture), y compris deux erreurs commises et corrigees en cours
de route.

## 1. Declencheur

L'observation d'intake `0 - HUMAN START HERE/archive/20260716_OBSERVATION_GATES_ATTESTATIONS_RESIDUELLES.md`
avait deja identifie 4 lots (A1/A2/B/C) de champs `gates.json` codes en dur.
Le Lot A1 avait deja ete traite et clos separement
(`.ai/archive/20260716_PLAN_CORRECTION_GATE_STATISTIQUE_OOS_MASQUE.md`).
Les lots A2/B/C restaient chacun a l'etat de simple mention dans un document
d'observation deja archive — aucun n'avait de chantier propre. L'humain a
signale explicitement perdre la vue d'ensemble sur ces sous-chantiers
disperses et a demande un traitement regroupe jusqu'a cloture generale.

## 2. Chantier mere redige

`.ai/backlog/fixes/EPIC_CLOTURE_ATTESTATIONS_RESIDUELLES_GATES.md` : liste
les 3 lots restants (C, A2, B), fixe l'ordre C -> A2 -> B, journalise les
decisions humaines deja actees, et precise explicitement qu'il ne modifie
lui-meme aucun fichier de `Implementation/`. Route via `plan.ps1 start`
comme un chantier `fix` normal.

## 3. Premiere erreur reelle : classification non revalidee

L'ordre initialement propose par l'observation source placait le Lot A2
(`power_check.status`) en premier, le qualifiant de "le plus urgent... calcul
reel". Avant de rediger son plan, une lecture directe de
`oos_confidence_interval.py` a montre que `validate_power_target(power,
target_power=0.80)` recoit **le meme parametre qu'il est cense valider**
(defaut de signature jamais estime depuis l'echantillon) — ce n'etait pas un
branchement mecanique mais un calcul manquant, contrairement a l'hypothese
heritee. Consequence sur la procedure : l'ordre a ete revise (Lot C
mecanique d'abord, verifie sur 6 fonctions sous-jacentes dont le `status`
est confine a `PASS`/`FAIL`/`INCONCLUSIVE`) et la decision de methode pour
A2 (reutiliser le bootstrap stationnaire par blocs deja normatif plutot
qu'un nouvel estimateur) a ete demandee et actee explicitement avant de
rediger son plan. **Lecon encodee dans ce skill : etape 1 de la boucle par
lot, "revalider dans le code reel avant de rediger".**

## 4. Deuxieme erreur reelle : sur-ingenierie de test detectee en `/evaluate`

Le premier jet du plan Lot C prescrivait un test de rejet unitaire pour
chacun des 12 champs `gates.json` cibles. La passe 1 de
`code-architecture-evaluator` a releve que le patron deja accepte dans ce
depot (`test_gate_report_rejects_non_pass_oos_gate`, sur le Lot A1/G9) ne
teste qu'un seul champ representatif par gate quand plusieurs champs
partagent la meme source — 4 des 5 gates de ce lot etaient dans ce cas,
seul un gate avait 3 sources reellement distinctes. Corrige : 7 tests de
rejet au lieu de 12, sans reduire la couverture reelle. La passe 2 a
confirme la convergence (aucun nouvel angle mort, un seul defaut de
formatage Markdown corrige).

## 5. Forme attendue du chantier mere

- Aucune ligne de code modifiee par le document de suivi lui-meme.
- Un seul id a suivre dans `.ai/checkpoint.json` par famille de lots.
- Chaque lot garde son propre cycle complet, sa propre boucle `/evaluate`,
  son propre commit de baseline, sa propre cloture.
- Le chantier mere se met a jour lui-meme apres chaque cloture de lot
  (section "Suite immediate"), sans jamais recopier le contenu technique des
  plans de lots.

## Piege a surveiller si ce cas est repris comme reference

Le chantier mere lui-meme n'a pas encore ete clos au moment de la redaction
de cet exemple (seul le lot mecanique a une boucle `/evaluate` deja
convergee et une baseline commitee ; son implementation, puis les lots A2 et
B, restent a executer). Ne pas lire cet exemple comme "le cas est termine" —
verifier l'etat reel dans `.ai/checkpoint.json` avant de s'appuyer dessus
comme precedent de cloture complete.
