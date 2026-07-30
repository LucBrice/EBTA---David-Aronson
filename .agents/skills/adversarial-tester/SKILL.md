---
name: adversarial-tester
description: Chasse le pattern de faux succes ou de repli silencieux dans le code EBTA. A invoquer obligatoirement avant /close quand un chantier touche un verdict, un artefact persiste ou append-only, une frontiere externe non fiable, config.json ou un artefact G0, ou une logique conditionnelle derivee de parametres. Recommande ailleurs. Ne remplace ni bug-hunter, ni EBTA_Protocol_Guardian, ni plan-conformance-audit.
---

# Role

Chasser un seul pattern : une erreur, une entree invalide ou une condition
non satisfaite est transformee en valeur plausible, en valeur par defaut ou
en verdict positif, de sorte que le pipeline continue et fabrique un succes.

Verifier deux proprietes separees pour chaque scenario :

1. l'entree invalide est rejetee au point d'entree ;
2. le resultat final est correct.

Un scenario ne tient que si les deux proprietes sont vraies. Un resultat
correct obtenu apres acceptation silencieuse d'une entree invalide reste un
defaut.

# Quand s'invoquer

Invoquer obligatoirement avant `/close` si le diff du chantier touche du code
qui :

- produit ou consomme un verdict (`validators/`, `governance/`,
  `procedures/`, gates) ;
- ecrit un artefact persiste ou append-only (`manifests/`, registres, journaux
  OOS, `reports/*.json`) ;
- franchit une frontiere externe non fiable (`adapters/`) ;
- construit ou scelle `config.json` ou un artefact G0 (`package_builder/`) ;
- derive un comportement conditionnel de parametres (`strategies/`).

L'invocation est recommandee, non bloquante, sur les autres changements.
Le futur workflow `interface` devra arbitrer separement l'application de ce
pattern au verrouillage serveur G0 ; ne pas inventer cette regle ici.

# Procedure

1. Delimiter le diff du chantier et identifier chaque point de decision,
   conversion, valeur par defaut, capture d'exception et construction de
   verdict.
2. Pour chaque point, ecrire le comportement d'echec attendu avant de tester.
3. Provoquer reellement chaque violation avec une entree minimale et observer
   a la fois le point d'entree et le resultat final.
4. Classer le scenario :
   - `PASS_ADVERSARIAL` : rejet explicite au point d'entree et resultat final
     correct ;
   - `FALSE_SUCCESS` : erreur transformee en resultat plausible ou positif ;
   - `SILENT_FALLBACK` : valeur de repli non autorisee sans preuve visible ;
   - `EXPECTED_DEFAULT` : valeur par defaut voulue, justifiee par le contrat et
     sans corruption de verdict ;
   - `NORMATIVE_GAP` : comportement attendu impossible a fixer sans decision
     normative.
5. Pour tout `FALSE_SUCCESS` ou `SILENT_FALLBACK`, corriger la cause minimale
   et ajouter un test de regression qui exige l'echec explicite au point
   d'entree.
6. Relancer le scenario adversarial, les tests cibles puis la suite complete.
7. Rapporter le point teste, l'entree hostile, l'observation, la
   classification, le correctif et la preuve. Utiliser
   `EXAMPLE_REPORT.md` comme exemple de forme.

# Regle de blocage

Refuser **proceduralement** `/close` tant qu'un `FALSE_SUCCESS` ou
`SILENT_FALLBACK` confirme reste non corrige, non couvert par regression ou
non escalade. Ce refus n'est pas mecanise :
`.ai/tools/plan.ps1 close` ne verifie pas ce skill. L'IA executante doit
appliquer elle-meme ce gate et ne jamais annoncer une garantie mecanique
inexistante.

Classer `NORMATIVE_GAP` selon
`.ai/governance/NORMATIVE_CHANGE_POLICY.md` et demander la decision humaine
requise au lieu d'inventer un verdict, un seuil ou un gate.

# Ce que ce skill ne fait pas

- Ne pas lancer un fuzzing generaliste sans rapport avec le diff.
- Ne pas assimiler toute valeur par defaut a un defaut : verifier son contrat
  et ses appelants.
- Ne pas remplacer `bug-hunter` (correction/typage),
  `EBTA_Protocol_Guardian` (conformite normative) ou
  `plan-conformance-audit` (livraison du plan).
- Ne pas modifier `Protocole/` ni trancher une lacune normative.
- Ne pas tenir un journal permanent de trouvailles : les tests de regression
  sont la memoire executable des incidents confirmes.
