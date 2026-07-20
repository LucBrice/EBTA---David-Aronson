# Brouillon - Chronologie et horodatage des evenements runtime

## Objectif

Garantir que le builder Nautilus n'accede jamais a l'OOS avant les calculs
pre-OOS, le scellement et l'autorisation, puis horodater les transitions
effectivement produites avec UTC runtime ou horloge fixture injectee.

## Classification et test multi-lot

`IMPLEMENTATION_DETAIL`, `SINGLE_CHANTIER`. Le refactor de chronologie et les
timestamps sont interdependants : un timestamp sans ordre reel serait une
facade; l'ordre sans timestamps ne prouverait pas les transitions.

## Defaut confirme

`build_nautilus_inputs()` execute actuellement : Test, selection, puis
`run_multifold_segments(oos_inputs)`. Seulement ensuite
`pilot.build_package()` appelle `_procedure_reports()`, qui calcule WRC,
robustesse, scellement, G-BIAS et `authorize_oos_access()`. L'OOS est donc lu
avant l'autorisation qui pretend le preceder.

Autres preuves : `_write_registry()` fixe le timestamp du registre; le builder
Nautilus conserve le timestamp fixture de l'acces OOS.

## Architecture cible

1. Extraire dans le pilote un helper pur de rapports pre-OOS, reutilise par le
   builder Nautilus avant OOS et par `_procedure_reports()` lors de l'ecriture.
   Il produit au minimum search space, selection, candidate matrix, WRC local et
   global, robustesse, scellement, G-BIAS et decision d'acces.
2. Le builder Nautilus execute Test, remplit les preuves pre-OOS, calcule la
   robustesse et une preuve d'execution limitee aux segments Test, capture le
   scellement, puis appelle ce helper. Cette preuve pre-OOS ne doit pas exiger
   des ordres ou une NAV OOS, sinon l'autorisation devient circulaire.
3. Separer le gabarit de demande/autorisation du journal des acces reellement
   executes. Le G-BIAS pre-OOS recoit un journal vide; une entree
   `oos_access_log` n'est creee qu'au bord de l'acces autorise.
4. Si decision `DENIED`, aucun `oos_inputs` n'est soumis au runner, aucune serie
   OOS ni entree d'acces n'est fabriquee. Le builder retourne une sortie
   controlee `DENIED` avec les preuves pre-OOS et la liste des exigences
   manquantes; il ne tente pas de construire le package VALIDATION_READY dont
   le contrat actuel exige une serie OOS non vide.
5. Si `AUTHORIZED`, capturer le timestamp d'acces immediatement avant la lecture
   OOS, materialiser les entrees d'acces par fold a partir du gabarit autorise,
   et seulement alors executer le runner OOS. La preuve d'execution finale est
   ensuite enrichie avec l'OOS sans modifier la decision pre-OOS.
6. Capturer le timestamp d'enregistrement avant les runs Test et le propager a
   `_write_registry()`; le pilote minimal injecte son timestamp fixe comme
   fixture explicite.
7. Une horloge injectable appartient au bord du builder; les fonctions internes
   recoivent des chaines UTC concretes, pas un acces diffus a `datetime.now()`.
8. Le helper pre-OOS retourne un objet immuable/logiquement scelle, stocke dans
   les inputs sous une cle interne dediee. `_procedure_reports()` doit le
   reutiliser par identite de contenu et ne recalculer apres OOS que les
   rapports dependants de l'OOS (intervalle, economie et preuves aval).

## Perimetre pressenti

- pilote minimal `build_research_package.py` et inputs fixture ;
- builder Nautilus ;
- tests pilote, package Nautilus et gouvernance ;
- historique moteur.

Pas de schema, Protocole, mapping API Nautilus, R5/R6, artefact persistant final
ou changement de statut.

## Tests obligatoires

- runner espion : decision DENIED => zero appel avec seed OOS, zero entree
  d'acces et sortie controlee portant les exigences manquantes;
- decision AUTHORIZED => appels OOS seulement apres trace d'autorisation;
- l'autorisation se fonde sur une preuve d'execution Test-only et n'exige jamais
  une preuve OOS future;
- timestamps registration/access proviennent de l'horloge injectee en fixture;
- production sans horloge utilise UTC aware;
- `_procedure_reports()` reutilise exactement les rapports pre-OOS deja calcules
  au lieu de resceller ou recalculer une decision apres OOS;
- pilote minimal demeure PASS; suite complete PASS.

## Exit criteria

- Aucun chemin n'execute l'OOS avant autorisation.
- Un refus d'acces produit une sortie de recherche honnete et exploitable, sans
  pretendre satisfaire le contrat d'un package VALIDATION_READY complet.
- Les evenements produits portent leurs vrais timestamps de transition.
- Aucun timestamp fixe n'est code dans un writer de production.
- Aucun recalcul post-OOS ne remplace les preuves pre-OOS scellees.

## Journal `/evaluate`

- Passe 1 (2026-07-20) : correction de la dualite dangereuse entre gabarit
  d'autorisation et preuve d'acces; abandon du faux package complet sur refus;
  separation explicite entre calculs pre-OOS scelles et rapports aval.
- Passe 2 (2026-07-20) : suppression de la dependance circulaire
  `execution_pass -> preuve OOS -> autorisation OOS`; ajout d'une preuve
  d'execution Test-only avant autorisation, puis enrichissement aval sans
  mutation de la decision scellee. Aucun nouvel angle mort majeur apres cette
  correction; convergence atteinte en deux passes.
