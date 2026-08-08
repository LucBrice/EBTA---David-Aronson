# Intake — Cliquet versionne de l'inventaire unittest

Date : 2026-08-08

| Champ | Valeur |
| --- | --- |
| Track | `mainline` |
| Lifecycle | `INTAKE` — non executable |
| Type de chantier | `SINGLE` |
| Scope | Ajouter un inventaire texte versionne des IDs `unittest` et un test qui echoue des qu'un ID est ajoute, retire, duplique ou desordonne sans mise a jour visible de l'inventaire. |
| Non-goals | Ne pas garantir contre la suppression volontaire simultanee du garde et de son inventaire ; ne pas modifier la CI, le chargeur unittest, les tests existants, `Protocole/` ou le code de production. |
| Source | Sous-chantier 2/7 de `EPIC_DURCISSEMENT_POST_AUDIT_ERREURS_IA`. |
| Exit criteria | L'inventaire contient exactement les IDs decouverts, y compris le garde lui-meme ; le test cible et la suite complete passent ; une suppression ou un ajout simule provoque une assertion explicite. |

## Constat verifie

- La suite vivante contient 245 IDs et 245 IDs uniques apres le lot WRC.
- Aucun cliquet ou fichier d'inventaire equivalent n'existe sous
  `Implementation/`, `.github/` ou `.ai/`.
- La commande canonique utilise `unittest discover -s
  Implementation/ebta_engine/tests -t Implementation`.

## Architecture proposee

```text
Implementation/ebta_engine/tests/test_inventory.txt
Implementation/ebta_engine/tests/test_test_inventory.py
```

Le garde decouvre la suite avec le meme `start_dir` et le meme `top_level_dir`
que la commande canonique, aplatit recursivement les `TestSuite`, trie les
`TestCase.id()` et compare la liste exacte au fichier texte. Le snapshot
initial contient egalement l'ID du garde, soit 246 IDs attendus apres ajout.

Contrats :

- une ligne non vide par ID ;
- ordre lexicographique ;
- aucun doublon ;
- egalite exacte attendu/reel ;
- message d'echec distinguant IDs manquants et inattendus.

## Limite honnete

Supprimer volontairement `test_test_inventory.py` et `test_inventory.txt`
retire aussi le mecanisme qui pourrait detecter cette suppression. Ce lot
rend une disparition accidentelle ou une mise a jour non declaree visible ;
il ne pretend pas resister a un agent malveillant qui modifie simultanement
le garde et la CI. Le diff git reste alors la preuve humaine.

## Perimetre

Autorise : les deux fichiers nouveaux ci-dessus uniquement.

Interdit : tous les tests existants, `.github/`, `Protocole/`, les modules de
production, les schemas, exemples, notebooks, adaptateurs et BACKTRADER.

## Verification

```powershell
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation -p test_test_inventory.py
python -m unittest discover -s Implementation\ebta_engine\tests -t Implementation
git diff --check -- Implementation\ebta_engine\tests\test_test_inventory.py Implementation\ebta_engine\tests\test_inventory.txt
```

## Audit intake — convergence

| Passe | Constat | Correction |
| --- | --- | --- |
| 1 | Les 245 IDs courants sont uniques, mais un snapshot pris avant creation du garde l'omettrait et ferait echouer immediatement le lot. | Generer l'inventaire apres creation logique du garde et y inclure explicitement son propre ID : total attendu 246. |
| 2 | Un test interne ne peut pas detecter sa propre suppression simultanee ; pretendre le contraire serait un faux succes de gouvernance. | Limite documentee dans Scope/Non-goals ; aucune modification CI ajoutee a ce lot. Les scenarios adversariaux porteront sur inventaire manquant et ID inattendu tant que le garde est execute. Aucun nouvel angle mort majeur. |

## Definition of Done

- [ ] Deux fichiers nouveaux seulement dans `Implementation/`.
- [ ] Inventaire exact, trie, unique et auto-inclusif.
- [ ] Test cible puis suite complete `OK` avec 246 tests ou davantage.
- [ ] Scenarios adversariaux ajout/suppression rejetes.
- [ ] Audits de fermeture sans finding bloquant.
