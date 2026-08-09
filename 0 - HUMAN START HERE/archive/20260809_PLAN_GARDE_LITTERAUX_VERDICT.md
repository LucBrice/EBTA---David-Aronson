# Plan d'implementation — Garde AST des litteraux de verdict

## Intention humaine reformulee

Installer, apres fermeture des trois producteurs defectueux 3A a 3C, un
cliquet AST qui rend visible toute reintroduction d'un `PASS` ou `True`
fabrique dans une cle semantiquement protegee.

Classification : `CONTRACT_ENCODING` sous workflow `core-engine`.

Le garde ne doit pas devenir une autorite scientifique, ni classifier le
code par fragments de noms. Les exceptions legitimes doivent etre explicites,
annotees et revues dans le meme diff que toute evolution de l'inventaire.

## Contraintes

- stdlib uniquement ;
- aucun changement de `Protocole/`, schema, producteur de verdict ou CI ;
- cles protegees exactes issues de `GATE_REQUIREMENTS`, des champs de verdict
  persistes et des hurdles economiques ;
- empreintes independantes des numeros de ligne ;
- allowlist structuree : categorie, justification et source de decision ;
- echec sur occurrence nouvelle, exception stale ou annotation invalide ;
- fixture positive de sink persiste et negatives pour calcul derive, attente
  de contrat et attestation technique ;
- suite canonique et inventaire de tests verts.

## Journal de convergence de l'intake

| Passe | Verification | Resultat |
| --- | --- | --- |
| 1 | Audit 3D confronte aux producteurs 3A-3C maintenant `DONE` et au scan vivant. | Le scan par fragment de nom est rejete ; choix d'un registre de cles exactes et d'empreintes AST stables. |
| 2 | Inventaire exact applique aux sources de production hors tests/fixtures/venv/packages. | 31 occurrences legitimes restent a annoter ; aucun des cinq faux succes initiaux ne subsiste. |
| 3 | Fixtures, CI et frontieres relues. | Le test canonique suffit a mecaniser le garde ; `.github/` reste reserve au lot 7. Convergence. |

## Critere de succes

Une nouvelle affectation positive a une cle protegee fait echouer le test ;
les 31 occurrences courantes sont expliquees sans ligne fragile ; retirer une
occurrence rend son exception stale ; les exemples negatifs restent acceptes.
