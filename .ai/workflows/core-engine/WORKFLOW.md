# Workflow `core-engine`

Ce fichier complete `AGENTS.md` pour les chantiers touchant le moteur EBTA,
ses adaptateurs, exemples, packages, gates ou artefacts executables.
Lire d'abord `.ai/workflows/common/WORKFLOW.md`, qui porte les commandes
universelles `/start`, `/continue`, `/close`, les deux boucles `/evaluate` et
le test `epic-orchestrator`.

## Frontiere BACKTRADER

Ne pas modifier BACKTRADER avant d'avoir lu sa gouvernance locale et recu un
scope explicite. BACKTRADER reste reference-only tant que ce scope n'est pas
ouvert ; ne pas importer ses conventions comme normes EBTA.

## Skills propres au workflow moteur

Apres toute implementation ou modification de code sous
`Implementation/ebta_engine/` ou dans les adaptateurs/exemples adjacents, et
avant de declarer la tache terminee :

1. Appliquer `.agents/skills/bug-hunter/SKILL.md` aux fichiers touches. Tout
   bug reel confirme doit etre corrige ou explicitement escalade.
2. Appliquer `.agents/skills/adversarial-tester/SKILL.md` si le diff touche :
   - un producteur ou consommateur de verdict ;
   - une ecriture persistee ou append-only ;
   - une frontiere externe non fiable ;
   - `config.json`, un artefact G0 ou `package_builder/` ;
   - une logique conditionnelle derivee de parametres.
3. Appliquer `EBTA_Protocol_Guardian` lorsqu'une coherence
   `Protocole/Implementation`, une regle scientifique ou un adaptateur
   subordonne au runtime est en jeu.

`expert-panel` est recommande pendant `/evaluate` lorsqu'une tension de
valeurs oppose plusieurs architectures viables. Il ne remplace pas
`code-architecture-evaluator` et ne constitue pas un gate.

## Gate procedural avant `/close`

Avant tout appel a `.ai/tools/plan.ps1 close` sur un chantier moteur :

1. appliquer `.agents/skills/bug-hunter/SKILL.md` en balayage complet des
   fichiers touches par le workstream, pas seulement du dernier diff ;
2. appliquer `.agents/skills/adversarial-tester/SKILL.md` sur les cinq zones
   de declenchement ci-dessus ;
3. appliquer `.agents/skills/plan-conformance-audit/SKILL.md` contre tous les
   Exit criteria du plan ;
4. ne pas appeler `plan.ps1 close` si un bug confirme, un faux succes, un
   repli silencieux ou un critere manquant reste ouvert.

Ces refus sont proceduraux. Avant la fermeture nominale, enregistrer les trois
IDs exiges par le contrat :

```powershell
.\.ai\tools\plan.ps1 ready -Id <ID> `
  -Evidence "bug_hunter=<rapport ou N/A justifie>", `
            "adversarial_tester=<rapport ou N/A justifie>", `
            "plan_conformance=<rapport>"
```

`plan.ps1` impose leur presence mais ne verifie pas l'execution reelle des
skills ni le contenu des references. Un controle non applicable doit donc
rester visible sous forme de reference `N/A` justifiee ; l'IA executante porte
la veracite de la preuve et le blocage.

Si les controles passent, reprendre la procedure universelle de fermeture
de `common/WORKFLOW.md` : appeler le backend, valider les JSON touches, puis
committer exactement le scope de fermeture sans pousser.

## Sources et frontieres

- `Protocole/` reste l'autorite normative.
- `Implementation/` reste sa traduction executable.
- `.ai/governance/AI_MODIFICATION_CHECKLIST.md` encadre toute modification
  structurante ou impactant `Implementation/`.
- `.agents/skills/bug-hunter/SKILL.md`,
  `.agents/skills/adversarial-tester/SKILL.md` et
  `.agents/skills/plan-conformance-audit/SKILL.md` portent les procedures
  detaillees ; ce workflow ne les remplace pas.
