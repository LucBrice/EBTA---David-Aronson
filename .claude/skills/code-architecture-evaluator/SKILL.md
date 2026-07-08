---
name: code-architecture-evaluator
description: >
  Expert en audit d'architecture et ingénierie logicielle. S'active IMMÉDIATEMENT avec "/evaluate"
  pour analyser et critiquer des plans de refonte technique. Confronte le plan aux réalités 
  structurelles du codebase existant via repomix, fichiers directs ou URL GitHub. Délivre un audit 
  précis sans hallucinations : points forts/faibles, angles morts, standards SOLID, et plan 
  d'implémentation rectifié avec phases et livrables concrets. Trigger : "/evaluate", "audite ce plan", 
  "critique ma refonte", ou demandes d'audit technique d'architecture.
---

# Pointeur — instructions complètes ailleurs

Ce fichier existe uniquement pour que Claude Code découvre et déclenche ce
skill automatiquement (mécanisme propre à `.claude/skills/`). **Il ne
contient aucune instruction propre.**

Les instructions complètes (workflow, structure de rapport, règles absolues,
exemple de rapport) vivent dans
`.agents/skills/code-architecture-evaluator/SKILL.md` — c'est l'emplacement
cross-AI de ce repo (cf. `.agents/AGENTS.md`, même précédent que
`.agents/skills/EBTA_Protocol_Guardian/` et
`.agents/skills/nautilus-docs-research/`), lisible par n'importe quelle IA
qui travaille ici, pas seulement par Claude Code.

**Dès que ce skill se déclenche : lire immédiatement
`.agents/skills/code-architecture-evaluator/SKILL.md` et suivre son contenu
à la lettre.** Voir aussi `.agents/skills/code-architecture-evaluator/README.md`
et `EXAMPLE_REPORT.md` pour un exemple complet de rapport attendu. Ne pas
dupliquer ou paraphraser ces instructions ici — ce fichier ne doit jamais
devenir une deuxième source de vérité.
