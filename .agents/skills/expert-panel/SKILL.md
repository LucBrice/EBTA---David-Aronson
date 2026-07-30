---
name: expert-panel
description: Tranche une tension de conception reelle par un debat de 3 a 5 personas orthogonaux, ancre dans les fichiers et contraintes du repo. A invoquer sur demande explicite ou lorsqu'un choix oppose des valeurs legitimes sans reponse conventionnelle. Ne pas invoquer pour une decision normative reservee a l'humain, une question factuelle simple ou un audit structurel que code-architecture-evaluator suffit a traiter.
---

# Role

Transformer une tension de conception en decision exploitable. Faire
argumenter des personas reellement en desaccord a partir du repo, confronter
leurs objections, puis rendre un verdict tranche. Un catalogue de
pour/contre ou « cela depend » sans decision n'est pas une sortie valide.

# Quand s'invoquer

- Sur demande explicite d'un panel ou d'un conseil d'experts.
- Lorsqu'une tension oppose des valeurs legitimes : simplicite contre
  couverture, centralisation contre specialisation, vitesse contre preuve,
  automatisation contre controle humain.
- Lorsqu'un audit ou l'IA identifie plusieurs choix techniquement viables
  dont le compromis ne se deduit pas d'une convention du repo.

Ne pas invoquer si la reponse est factuelle ou conventionnelle, si
`code-architecture-evaluator` suffit a corriger une tension de structure, ou
si la decision modifie la doctrine EBTA et appartient donc a l'humain.

# Procedure

1. Lire les autorites et fichiers directement concernes.
2. Formuler la tension comme une question fermee avec 2 ou 3 options
   mutuellement exclusives.
3. Choisir 3 a 5 personas orthogonaux pertinents pour ce choix precis ; ne
   pas reutiliser une distribution fixe par ceremonie.
4. Faire produire a chaque persona :
   - sa recommandation ;
   - deux preuves du repo ;
   - le risque principal de sa propre option ;
   - l'objection la plus forte a l'option adverse.
5. Confronter les desaccords sans les lisser. Ecarter tout argument non
   soutenu par le repo ou par une contrainte explicite.
6. Rendre un verdict unique, ses raisons determinantes, les options rejetees
   et un critere de reouverture.
7. Si le verdict exige une decision humaine, formuler la question exacte et
   arreter avant toute mutation.

Voir `EXAMPLE_REPORT.md` pour le debat ayant borne
`adversarial-tester`.

# Regle de blocage

Le panel n'est pas un gate automatique. Il bloque seulement lorsqu'il
revele qu'une option requiert une decision normative ou une autorisation
humaine absente. Dans ce cas, ne pas convertir une recommandation majoritaire
en autorisation.

# Ce que ce skill ne fait pas

- Ne pas remplacer `code-architecture-evaluator`.
- Ne pas simuler un consensus : conserver les objections substantielles.
- Ne pas choisir un seuil, un gate ou une doctrine EBTA a la place de
  l'humain.
- Ne pas etre invoque sur chaque divergence mineure.
- Ne pas produire plusieurs options non tranchees comme resultat final.
