---
name: capture-coding-session-learnings
description: Extraire d'une session de travail EBTA les reussites verifiees, pratiques reutilisables, erreurs et frictions, puis proposer leur promotion vers les proprietaires existants. TRIGGER automatiquement apres tout `/close` aboutissant a une sortie terminale (`DONE`, `BLOCKED`, `REJECTED` ou `SUPERSEDED`), sur `/learn-session`, ou sur demande humaine explicite de retrospective, de capitalisation, de bonnes et mauvaises pratiques ou d'amelioration durable des agents. SKIP pour un simple statut, `/continue`, ou toute tentative de memoriser automatiquement une conversation hors du cycle terminal `/close`.
---

# Capitaliser une session EBTA

Transformer des preuves de session en ameliorations durables sans fabriquer de
succes, dupliquer une source de verite ni memoriser du bruit.

## Autorite et non-role

- Lire d'abord `AGENTS.md`, `.ai/README.md`, `.ai/checkpoint.json` et les
  chemins actifs qu'il declare.
- Respecter `Protocole/` comme autorite scientifique, `Implementation/` comme
  traduction executable et `.ai/` comme cockpit projet.
- Traiter ce skill comme une procedure cross-IA. Ne jamais en faire un etat
  projet, une autorite EBTA, une preuve de performance ou un registre de
  sessions.
- Preserver litteralement les verdicts `FAIL`, `DENIED`, `INCONCLUSIVE`, les
  timeouts et les absences de sortie. Aucun resultat technique ne les convertit
  en `PASS`.

## Procedure

1. Delimiter la session.
   - Identifier la demande initiale, les decisions humaines, le resultat
     attendu et les operations externes autorisees.
   - Borner toute analyse Git par des SHA explicites. Ne pas utiliser `HEAD`
     mobile comme seule borne historique.
   - Dans un worktree mixte, distinguer le scope de la session des changements
     humains ou paralleles.

2. Recueillir les preuves compactes.
   - Examiner les fichiers d'etat live, commits bornes, diffs cibles, tests,
     rapports d'audit et sorties finales utiles.
   - Preferer une verification live peu couteuse au souvenir de conversation.
   - Distinguer un echec attendu de test negatif d'un vrai echec seulement si
     le harnais global le prouve.

3. Classer chaque signal.
   - `BIEN_FAIT` : action verifiee ayant ameliore correction, tracabilite,
     securite ou efficacite.
   - `A_REUTILISER` : procedure transferable avec trigger et validation.
   - `ERREUR_OU_FRICTION` : signal observable, cause et prevention concrete.
   - `NON_PROMU` : detail ponctuel, deja couvert, instable, non prouve ou hors
     autorisation.
   - Ajouter un tag de portee a chaque signal classe :
     - `Portee: meta` — le signal porte sur le fonctionnement du systeme lui-
       meme : skills (`.agents/skills/`), workflow (`.ai/workflows/`), gates
       CI, gouvernance de cloture, outillage de backlog. Un stock fini de
       defauts : chaque correction reduit la probabilite d'en retrouver un du
       meme genre.
     - `Portee: objet` — le signal porte sur ce que le systeme EBTA fait :
       `Protocole/`, `Implementation/` (moteur, procedures, adapters), capacite
       statistique ou de backtest. Un perimetre etendu deliberement : chaque
       extension produit normalement de nouveaux apprentissages, sans
       obligation de convergence.
     - En cas de doute (ex. un skill qui encode une regle Protocole), classer
       `objet` si le signal touche `Protocole/`/`Implementation/` meme
       indirectement, `meta` sinon.

4. Appliquer le test de promotion.
   Promouvoir seulement si toutes les conditions sont satisfaites :
   - trigger futur identifiable ;
   - procedure ou decision non triviale ;
   - utilite probable au-dela du cas unique ;
   - preuve issue de la session ;
   - proprietaire durable legitime ;
   - autorisation d'ecriture et validation explicites.
   Sinon classer `NON_PROMU`. Ne jamais creer un skill par reflexe.

5. Router vers le proprietaire existant.
   - pratique cross-IA repetable : skill canonique concerne sous
     `.agents/skills/` ;
   - regle de cycle projet : workflow proprietaire sous `.ai/workflows/` ;
   - erreur mecaniquement detectable : test, hook ou validateur proprietaire ;
   - decision ou resultat du chantier courant : plan actif, puis archive par
     son cycle normal ;
   - idee nouvelle non auditee : nouveau brouillon `INTAKE` sous
     `0 - HUMAN START HERE/` ;
   - changement scientifique : procedure normative separee, avec decision
     humaine et gouvernance de version ;
   - preuve de session optionnelle : copie de
     `.ai/governance/TEMPLATE_PREUVE_SESSION_IA.json` seulement si un plan en
     definit le chemin et la validation.

6. Separer les autorisations.
   - `/learn-session` seul autorise l'analyse et la proposition, pas l'ecriture.
   - Persister seulement si la demande humaine autorise explicitement la
     creation ou la modification des fichiers cibles.
   - Une autorisation de persistance n'autorise ni commit, ni push, ni
     publication externe. Obtenir chaque autorisation separement.
   - Ne jamais modifier une memoire personnelle ou un fichier hors depot par
     implication.

7. Valider et rendre compte.
   - Relire les fichiers ecrits, verifier leur proprietaire et l'absence de
     secrets ou de duplication.
   - Executer les validateurs et tests du proprietaire modifie.
   - Rapporter ce qui est promu, seulement propose, classe `NON_PROMU` et
     volontairement laisse intact.

## Cas de calibration

Cas positif : une commande PowerShell fragile a echoue deux fois pour la meme
cause, puis une forme corrigee a ete prouvee par des tests. Si le trigger futur,
la procedure et le proprietaire sont clairs, classer `A_REUTILISER` et proposer
une correction du skill ou du workflow proprietaire.

Cas negatif : une faute de frappe unique sans recurrence, preuve de cout futur
ni procedure nouvelle reste `NON_PROMU`. Ne creer ni skill, ni regle, ni note
durable pour ce seul signal.

## Format de sortie

Produire un rapport concis :

1. `Ce qui a bien fonctionne` ;
2. `Pratiques promues ou proposees`, avec preuve et proprietaire ;
3. `Erreurs a ne pas refaire`, avec signal, cause et prevention ;
4. `Actifs crees ou modifies`, avec validations reelles ;
5. `NON_PROMU et limites`, y compris les actions non autorisees.

Chaque signal du rapport porte explicitement `Portee: meta` ou
`Portee: objet`.
