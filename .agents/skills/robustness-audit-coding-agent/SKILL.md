---
name: robustness-audit-coding-agent
description: Audite en boucles convergentes la capacité de l'architecture du repo (gouvernance IA, hooks, workflows, gates) à contenir les erreurs d'un agent de codage qui implémente dans Implementation/. À invoquer sur demande explicite de l'utilisateur ("audit robustesse agent de codage", "revérifie la robustesse face aux erreurs d'IA", "relance l'audit de robustesse"), notamment après un changement d'outillage de gouvernance destiné à corriger un point faible identifié par un audit précédent. Ne remplace pas EBTA_Protocol_Guardian (conformité scientifique Protocole/Implementation) : ce skill audite les garde-fous procéduraux/mécaniques contre l'erreur d'implémentation, pas la justesse méthodologique.
---

# Rôle

Auditer si un agent de codage (IA) qui implémente dans ce repo peut produire
une erreur silencieuse — bug de contrat, faux succès, repli non autorisé,
gate satisfait en forme mais pas en substance — sans qu'aucun mécanisme du
repo ne la détecte avant qu'elle n'atterrisse. Ce skill ne corrige rien : il
produit un diagnostic vérifié, avec un niveau de confiance explicite et
calibré, destiné au triage humain.

Née d'un audit réel (2026-08-07) qui a distingué deux zones de risque très
différentes : les erreurs méthodologiques/statistiques (hors périmètre de ce
skill, relèvent d'`EBTA_Protocol_Guardian`) et les erreurs d'implémentation
d'un agent de codage (périmètre de ce skill). Cet audit a montré qu'une
lecture de documentation seule surestime la robustesse réelle — les gains de
confiance les plus importants sont venus de la lecture directe du code des
mécanismes de contrôle, pas de leur description.

# Quand s'invoquer

- Sur demande explicite de l'utilisateur pour auditer ou ré-auditer la
  robustesse du repo face aux erreurs d'un agent de codage.
- Systématiquement recommandé après toute modification d'un mécanisme de
  gouvernance IA (`.ai/tools/`, `.ai/workflows/`, `.git/hooks/`,
  `.ai/governance/`) destinée à corriger une faiblesse trouvée par un audit
  précédent — pour vérifier que le correctif ferme réellement le gate et
  n'en ouvre pas un nouveau.
- Non pertinent pour un audit de conformité normative (`Protocole/` vs
  `Implementation/`) ou pour la revue d'un diff ponctuel — voir
  `EBTA_Protocol_Guardian`, `bug-hunter`, `adversarial-tester`.

# Principe directeur

**Ne jamais accepter une affirmation de robustesse sur la seule foi de la
documentation ou du nom d'un mécanisme.** Un skill qui s'appelle
`adversarial-tester`, un fichier qui s'appelle `pre-commit`, une clé JSON qui
s'appelle `required_evidence` ne prouvent rien sur ce qu'ils vérifient
réellement. Chaque affirmation de garde-fou doit être vérifiée en lisant le
code qui l'implémente et, si possible, en observant son comportement réel
(exécuter la suite de tests, inspecter le contenu d'un hook installé,
tracer un chemin d'erreur jusqu'à son traitement effectif).

# Procédure — boucle de passes convergentes

Boucle par défaut, plafonnée à **6 passes**. S'arrêter dès que deux passes
consécutives ne révèlent aucun nouveau point de rupture majeur (convergence
genuine), même avant le plafond. Une passe qui ne fait que corroborer un
constat déjà posé, sans le nuancer ni le contredire, compte comme
"sans nouveauté" pour le critère de convergence.

## Passe 1 — relevé documentaire et état de base

1. Lire `AGENTS.md`, `.ai/checkpoint.json`, `.ai/governance/AI_MODIFICATION_CHECKLIST.md`.
2. Lister les skills de contrôle disponibles (`.agents/skills/*/SKILL.md`) et
   noter, pour chacun, s'il est déclaré obligatoire, recommandé, ou
   mécaniquement vérifié (chercher explicitement toute phrase du type
   "n'est pas mécanisé" ou "ne peut pas verifier le contenu").
3. Exécuter la suite de tests complète
   (`python -m unittest discover -s Implementation/ebta_engine/tests -t Implementation`)
   et noter tout échec, même hors-scope apparent.
4. Produire un premier relevé de points de rupture plausibles (table
   zone -> mécanisme de rupture typique), explicitement marqué comme non
   vérifié au-delà de la lecture documentaire.

## Passes 2+ — vérification directe contre le code, pas la doc

Pour chaque passe suivante, choisir 1 à 3 affirmations non encore vérifiées
de la passe précédente et les confronter au code réel. Zones à vérifier en
priorité, dans l'ordre d'impact observé lors de l'audit fondateur :

- **Hooks git réellement actifs** : lister `.git/hooks/` (en excluant les
  `.sample`), lire le contenu de tout hook présent, vérifier
  `git config core.hooksPath` pour confirmer qu'aucune redirection ne
  désactive silencieusement le hook. Ne jamais conclure "pas de hook" sans
  avoir listé le dossier.
- **CI/CD réel** : chercher `.github/workflows/`, tout fichier de pipeline.
  Confirmer l'absence plutôt que la supposer.
- **Mécanique de vérification des preuves de workflow** (`.ai/tools/plan.ps1`,
  `.ai/tools/workflow_state.ps1` ou équivalent) : lire la fonction qui valide
  une preuve (`Add-WorkflowEvidence` ou équivalent) ligne par ligne. Question
  décisive : la preuve est-elle vérifiée par existence d'un artefact
  (`Test-Path` ou équivalent) ou seulement par un test de forme (regex,
  chaîne non vide) ? C'est le point qui a le plus fait varier la confiance
  lors de l'audit fondateur (2026-08-07).
- **Patterns de repli silencieux dans le code, pas seulement leur présence** :
  grep `except Exception`, `.get(...)` avec valeur par défaut positive,
  `or True`/`or "PASS"` dans `governance/`, `validators/`, `adapters/`. Pour
  chaque occurrence trouvée, lire le contexte complet (pas seulement la
  ligne) et déterminer si l'échec dégrade vers la branche la plus prudente
  (`EXPECTED_DEFAULT`, sain) ou vers un verdict positif fabriqué
  (`FALSE_SUCCESS`, à signaler). Mesurer aussi la proportion de fichiers
  concernés (`except Exception` confiné aux `adapters/` est un bon signe ;
  dispersé dans `governance/`/`validators/` est un mauvais signe).
- **Rigueur des schémas JSON** : compter `additionalProperties` dans
  `Implementation/ebta_engine/schemas/` — un schéma permissif laisse passer
  des champs fabriqués sans les valider.
- **Taille de la surface auditée** : mesurer les lignes de code des zones
  sensibles (`wc -l` sur `governance/`, `validators/`) pour calibrer si un
  futur passage `adversarial-tester` outillé sur cette zone est réaliste.
- **Chaîne de gate spécifique à la clôture d'un chantier d'implémentation**
  (ex. `core-engine` `WORKFLOW.json` transition `ready`) : vérifier que les
  IDs de preuve exigés (`bug_hunter`, `adversarial_tester`,
  `plan_conformance` ou équivalents renommés) sont bien exigés au bon
  endroit, puis immédiatement vérifier avec le point précédent si leur
  contenu est substantifié ou seulement syntaxique.

Pour chaque vérification : indiquer si elle **confirme**, **infirme** ou
**affine** un constat de la passe précédente. Une infirmation compte comme
nouveauté majeure et relance le compteur de convergence.

## Passe ciblée (optionnelle, sur demande)

Si l'utilisateur précise une préoccupation prioritaire (ex. "l'agent de
codage" spécifiquement, par opposition aux erreurs méthodologiques), ne pas
refaire un balayage général : chercher directement le mécanisme de gate qui
couvre ce risque précis, lire son code d'application ligne par ligne, et
s'arrêter dès que le point de défaillance exact est localisé (fichier +
ligne) — une seule passe bien ciblée suffit souvent à converger sur une
question précise, même si l'audit général est encore en cours.

# Format de sortie

Écrire ou mettre à jour un document dans `0 - HUMAN START HERE/` nommé
`AUDIT_ROBUSTESSE_ARCHITECTURE_FACE_ERREURS_IA_<date>.md` (INTAKE par
défaut, jamais exécutable directement — voir `AGENTS.md`), avec :

1. **En-tête** : date, statut (`audit en N passes, convergé`), aucune
   décision d'implémentation prise par le skill lui-même.
2. **Journal des passes** : une ligne par passe, ce qu'elle a vérifié, ce
   qu'elle a confirmé/infirmé/affiné.
3. **Points de rupture** (table zone -> mécanisme de rupture).
4. **Ce qui est mécanisé et vérifié** vs **ce qui reste procédural** —
   séparation stricte, avec référence fichier:ligne pour chaque affirmation.
5. **Section dédiée si une préoccupation prioritaire a été précisée** (ex.
   agent de codage), avec le point de défaillance exact localisé.
6. **Recommandations** priorisées, la première étant toujours celle qui
   corrige le risque prioritaire explicitement énoncé par l'utilisateur si
   une telle priorité a été donnée.
7. **Non-goals** : aucune modification de `Protocole/`, `Implementation/`
   ou `.ai/` n'est faite par ce skill — audit seul, jamais de correctif
   appliqué directement, sauf demande explicite distincte de l'utilisateur.
8. **Niveau de confiance explicite**, séparé en deux : confiance sur ce qui
   a été vérifié directement (peut être haute) vs confiance sur
   l'exhaustivité de la couverture (rester honnête sur ce qui n'a pas été
   lu). Ne jamais fusionner les deux dans un seul chiffre.

# Règle de blocage

Ne jamais déclarer une confiance "haute" sur un mécanisme non lu dans son
code source. Une affirmation appuyée uniquement sur un nom de fichier, un
titre de skill, ou une phrase de documentation reste au mieux
"confiance modérée, à vérifier" tant que le code n'a pas été lu.

# Ce que ce skill ne fait pas

- Ne corrige aucun code ni configuration — audit seul. Une correction
  proposée par ce skill doit être implémentée dans une tâche séparée, avec
  son propre cycle `bug-hunter`/tests/`adversarial-tester`.
- Ne remplace pas `EBTA_Protocol_Guardian` sur la conformité
  scientifique/normative, ni `adversarial-tester` sur un diff ponctuel déjà
  identifié, ni `plan-conformance-audit` sur la clôture d'un chantier
  précis.
- Ne fabrique pas de conclusion "converged" par lassitude : si la 6e passe
  plafond est atteinte alors que des points de rupture majeurs continuent
  d'apparaître, le rapporter explicitement comme non convergé et escalader
  vers une décision humaine plutôt que de déclarer une confiance qui
  n'existe pas.
