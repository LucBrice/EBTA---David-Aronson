# Exemple de rapport — portee d'`adversarial-tester`

## Question fermee

Faut-il construire un adversarial tester generaliste couvrant toutes les
classes de bugs, ou un skill etroit cible sur le pattern deja observe
« succes fabrique / repli silencieux » ?

## Panel

| Persona | Position | Preuve du repo | Risque reconnu |
| --- | --- | --- | --- |
| Pragmatique maintenance | Skill etroit | Les incidents confirmes partagent le meme pattern : gates a `True`, stub buy-and-hold, auto-attestation, conversion d'erreur en `0.0`. | Peut manquer une nouvelle classe de defauts. |
| Ingenieur qualite | Skill large | Une taxonomie large donne une couverture theorique superieure. | Produit du bruit et chevauche `bug-hunter`. |
| Gardien gouvernance | Skill etroit | Les responsabilites doivent rester separees entre correction, norme, conformite au plan et adversarial. | Exige une reouverture explicite si le risque evolue. |
| Architecte simplicite | Skill etroit | Aucun precedent de race condition ou corruption de schema ne justifie un framework general. | Risque de sous-generaliser trop longtemps. |

## Confrontation

L'option large promet une couverture sans preuve locale et duplique des
responsabilites deja attribuees. L'option etroite explique tous les incidents
observes et permet des scenarios deterministes. Son risque est controlable :
reouvrir la portee lorsqu'une classe de defauts confirmee echappe au pattern.

## Verdict

**Choisir le skill etroit.** Il chasse uniquement le succes fabrique et le
repli silencieux, avec cinq zones de declenchement observables. Ne pas creer
de fuzzing generique ni de journal de trouvailles.

Critere de reouverture : au moins deux incidents confirmes d'une meme nouvelle
classe, non couverte par `bug-hunter`, `EBTA_Protocol_Guardian` ou
`plan-conformance-audit`.

Source narrative :
`0 - HUMAN START HERE/archive/20260729_PROPOSITION_FORMALISATION_WORKFLOWS_IA_ADVERSARIAL_EXPERT_PANEL.md`,
etapes 8 a 13.
