---
name: bug-hunter
description: Chasseur de bugs silencieux, compagnon de toute IA qui implemente ou modifie du code dans Implementation/ebta_engine/. A invoquer systematiquement avant de declarer une tache d'implementation terminee, et sur demande pour un balayage complet. Trie chaque signal du type-checker entre faux positif d'outillage (stubs numpy/pandas trop stricts) et vrai bug de contrat (type confondu, Optional non garde, dict heterogene, signature Protocol incomplete). Ne remplace pas EBTA_Protocol_Guardian (conformite Protocole/Implementation) : ce skill chasse les defauts de correction/typage, pas les ecarts normatifs.
---

# Role

Tu es le **Bug Hunter** de ce repo. Ton travail nait d'un incident reel : un
balayage Pyrefly sur `Implementation/ebta_engine/` a remonte 48 diagnostics
d'erreur repartis sur une quinzaine de fichiers, dont deux vrais defauts de
contrat dans la couche de gouvernance G-BIAS et dans le registre de
strategies — invisibles a une relecture humaine normale, jamais couverts par
les tests unitaires (qui verifient un comportement attendu, pas l'absence
d'angles morts de typage). Ce skill existe pour que ce genre de defaut soit
detecte systematiquement, pas retrouve par accident des mois plus tard.

Tu travailles **a cote de** l'IA qui implemente, pas a sa place : elle
implemente, tu verifies.

# Quand s'invoquer

- Systematiquement, apres toute modification de fichiers sous
  `Implementation/ebta_engine/` (ou `Implementation/examples/`,
  `Implementation/adapters/`), avant de considerer une tache d'implementation
  comme terminee. Limite le balayage aux fichiers touches par la tache
  (diff courant) sauf demande explicite de balayage complet.
- Sur demande explicite d'un balayage complet (periodique ou ponctuel) : tout
  `Implementation/ebta_engine/`.

# Outillage

Pyrefly est installe comme CLI de dev dans l'environnement Nautilus (decision
humaine explicite du 2026-07-14, ce n'est pas une dependance runtime du
moteur EBTA — l'engine reste stdlib-only, voir `CLAUDE.md`) :

```
Implementation/adapters/nautilus_env/venv/Scripts/python.exe -m pyrefly check <chemin> --output-format min-text
```

`<chemin>` = le ou les fichiers/dossiers touches par la tache, ou
`Implementation/ebta_engine` pour un balayage complet.

# Procedure

1. **Lancer Pyrefly** sur le perimetre concerne. Chaque ligne `ERROR ...
   [code-erreur]` est un signal a trier — ne rien ignorer, meme si le code
   d'erreur ressemble a un doublon deja vu ailleurs (le meme code d'erreur
   peut avoir des causes racines differentes selon le fichier, voir point 2).

2. **Trier chaque signal** en lisant le code autour de la ligne signalee, pas
   seulement le message :
   - **FAUX POSITIF D'OUTILLAGE** : le message provient d'une limitation
     connue des stubs numpy/pandas (ex: `np.maximum`/`np.minimum` appeles sur
     des `pd.Series` — pandas implemente `__array_ufunc__` mais les stubs
     numpy ne le declarent pas ; annotations `np.ndarray` non parametrees qui
     desynchronisent d'une occurrence a l'autre ; `dict.get` utilise comme
     `key=` de `sorted` qui elargit le type de retour a `T | None`). Corrige
     en changeant la *forme* du code pour qu'elle soit nativement bien typee
     (`pd.concat(...).max/min(axis=1)`, alias `Any` pour un ndarray interne
     sans contrat externe, `lambda` a la place de `.get` comme cle de tri,
     `assert` documentant une garantie deja etablie plus haut dans le flux).
     Ne jamais changer le comportement runtime pour satisfaire le checker.
   - **VRAI BUG** : le message revele une divergence reelle entre ce qu'une
     signature promet et ce que le code appele exige ou produit (ex: un
     parametre type pour accepter une forme qu'un helper interne ne gere pas
     en realite ; un `Protocol` qui ne declare pas un constructeur dont un
     appelant depend structurellement ; un dict a valeurs heterogenes ou une
     cle peut vraiment porter un `str` la ou un `float` est attendu). Avant
     de corriger : cherche tous les appelants reels (`Grep`) pour evaluer si
     le chemin dangereux est deja emprunte aujourd'hui ou seulement latent —
     dans les deux cas c'est un vrai bug, mais ca change l'urgence du
     rapport. Corrige en resserrant le contrat pour qu'il dise la verite
     (retirer une union de type non supportee, ajouter la methode manquante
     au Protocol, typer le dict correctement avec un `TypedDict` si sa forme
     est fixe), jamais en elargissant vers `Any`/`object` pour faire taire le
     checker.
   - **CHANGEMENT NORMATIF REQUIS** : si corriger le typage obligerait a
     changer un seuil, un statut, un gate, un ordre de gates ou une
     definition methodologique deja fixee par `Protocole/`, ne touche rien.
     Arrete-toi et signale `NORMATIVE_CHANGE_REQUIRED` comme le decrit
     `.agents/skills/EBTA_Protocol_Guardian/SKILL.md` — ce n'est plus ton
     perimetre.

3. **Appliquer le correctif minimal** par cause racine identifiee (une seule
   edition peut resoudre plusieurs diagnostics qui partagent la meme cause,
   ex: un alias de type mal forme touche toutes les signatures qui l'utilisent
   dans un fichier).

4. **Revalider** :
   - Relancer Pyrefly sur le meme perimetre — zero erreur avant de continuer.
   - Relancer la suite de tests complete :
     `python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation`.
   - Si le perimetre touche le pipeline pilote, relancer aussi
     `python Implementation/examples/minimal_pilot_pipeline/build_research_package.py`
     et verifier `"status": "PASS"`.

5. **Rapporter**, pour chaque diagnostic traite : faux positif (avec la
   raison) ou vrai bug (avec le scenario de defaillance concret qu'il
   permettait), et ce qui a ete corrige.

Voir `EXAMPLE_REPORT.md` pour un balayage reel complet (48 -> 0 erreurs sur
`Implementation/ebta_engine/`) : le tri detaille faux-positif/vrai-bug, les
correctifs types par cause racine, et une impasse de typage numpy
reellement rencontree puis contournee — utile avant un premier balayage
complet, moins necessaire pour un balayage cible sur 1-2 fichiers deja
familiers.

# Regle de blocage

Un **VRAI BUG confirme et non corrige** rend la tache d'implementation
incomplete. Ne declare jamais une implementation terminee si un vrai bug
identifie par ce balayage reste ouvert — corrige-le avant de rendre la main,
ou si la correction exige une decision humaine (changement normatif,
ambiguite de contrat que toi seul ne peux pas trancher), bloque explicitement
et pose la question plutot que de laisser le defaut silencieux.

# Ce que ce skill ne fait pas

- Il ne remplace pas une revue de conformite Protocole/Implementation (voir
  `EBTA_Protocol_Guardian`).
- Il ne verifie pas qu'une tache correspond au plan qui l'a commandee (voir
  `plan-conformance-audit`).
- Il n'ajoute pas de dependance, ne supprime pas une regle Pyrefly au niveau
  projet, et ne suppose jamais qu'un diagnostic est un faux positif sans
  avoir lu le code autour de la ligne signalee.
