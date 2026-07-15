# Prompt d'exécution — Plan R4

Exécute intégralement, du début à la fin, sans t'arrêter et sans dérive, le plan suivant dans le dépôt EBTA `D:\Livre\Trading\Trading algorithmic\EBTA - David Aronson` :

**`.ai/backlog/mainline/PLAN_R4_DONNEES_INTRADAY_REELLES_PACKAGE_PRODUCTION.md`**

Lis d'abord `AGENTS.md`, puis `.ai/checkpoint.json`, puis ce plan dans son intégralité (sections 0 à 14) — il est conçu pour être repris à froid et contient tout ce qui est nécessaire : ordre de lecture, phases, gates, commandes de vérification exactes, invariants, périmètre de fichiers autorisés/interdits, décisions humaines déjà tranchées, et la règle explicite de non-interruption (section 9, "Exécution sans interruption").

Exécute les phases dans l'ordre indiqué, vérifie chaque critère de sortie avec les commandes données avant de passer à la phase suivante, et ne t'arrête que pour l'une des causes listées dans cette même section. Si tu constates qu'une information nécessaire manque au plan pour continuer seul, c'est le plan qu'il faut corriger avant de reprendre — pas un contournement ad hoc.

Applique `.agents/skills/bug-hunter/SKILL.md` sur les fichiers touchés avant de considérer le chantier terminé (obligatoire, cf. `AGENTS.md`), puis produis le rapport de clôture prévu par le Definition of Done (section 12) et la section Clôture (section 13) du plan.
