---
name: nautilus-docs-research
description: >
  Recherche ciblée et vérification empirique de l'API NautilusTrader
  (nautilus_trader) pour ce repo EBTA. À invoquer avant d'écrire ou de
  documenter tout appel réel à nautilus_trader (BacktestEngine, Strategy,
  StrategyConfig, FillModel, add_venue, OrderFactory, Instrument,
  MarginModel, indicateurs, etc.), avant de modifier ou d'étendre
  adapters/nautilus_mapping.py ou adapters/nautilus_strategy_bridge.py, ou
  dès qu'une signature/classe/comportement Nautilus est sur le point d'être
  cité dans un plan, une revue ou du code — même si ça a l'air d'un détail
  mineur ou d'une signature "évidente". Ne jamais deviner ni recopier de
  mémoire une API Nautilus sans passer par ce skill d'abord. Non pertinent
  pour la gouvernance du pivot (faut-il utiliser Nautilus, statut D1-D6,
  arbitrage stratégique, lecture du Protocole EBTA) — ces sujets ne
  nécessitent aucune vérification technique.
---

# Recherche documentaire et vérification empirique NautilusTrader

> Ce skill vit dans `.agents/skills/` (outillage cross-AI de ce repo, cf.
> `.agents/AGENTS.md` §"Rôle résiduel de `.agents/`"), pas dans `.claude/`
> — il doit rester lisible et applicable par n'importe quelle IA qui
> travaille dans ce repo, pas seulement par Claude Code. Un pointeur existe
> dans `.claude/skills/nautilus-docs-research/SKILL.md` pour que Claude Code
> le déclenche automatiquement ; ce fichier-ci reste l'unique source de
> vérité de son contenu — ne pas dupliquer les instructions ailleurs.

## Pourquoi ce skill existe

Ce repo (EBTA) confine `nautilus_trader` à
`Implementation/ebta_engine/adapters/nautilus_mapping.py` et
`adapters/nautilus_strategy_bridge.py` (exception `stdlib-only` tracée dans
`CLAUDE.md`). Toute affirmation sur l'API Nautilus qui finit dans un plan ou
du code doit être vérifiable — jamais une supposition. Le plan
`0 - HUMAN START HERE/Implementation_plan_Nautilus.md` contient un encart
"Fondations empiriques vérifiées" produit en interrogeant directement un
environnement avec `nautilus_trader` installé (signatures, construction
d'objets réels) plutôt qu'en résumant la documentation de mémoire — c'est
cette méthode que ce skill reproduit systématiquement, pour que n'importe
quelle IA travaillant dans ce repo obtienne la même rigueur sans avoir à la
réinventer.

La documentation web peut dater par rapport à la version installée. Le
package installé peut différer de ce que dit la doc. Ce skill traite les deux
sources comme complémentaires, jamais interchangeables, et l'exige dans la
réponse finale (voir "Règle de citation" ci-dessous).

## Workflow

### Étape 0 — Consulter le cache avant toute recherche

Lire `Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md` s'il
existe. S'il contient déjà une entrée pour le symbole/comportement recherché
**et que la version `nautilus_trader` qui y est notée correspond à celle
installée dans l'environnement courant** (revérifier avec
`scripts/introspect_nautilus.py`, qui affiche toujours la version en
premier), répondre directement depuis le cache, en le citant comme source,
sans refaire de recherche web ni de nouvelle introspection.

Si le cache a une entrée mais que la version installée a changé : re-vérifier
(étapes 1-2 ci-dessous) et **mettre à jour l'entrée existante en place**
(nouvelle date, nouvelle version, nouveau résultat) — ne pas dupliquer une
nouvelle entrée à côté de l'ancienne.

Si le fichier n'existe pas encore, ne pas le créer à vide par anticipation :
il sera créé à l'étape 3, la première fois qu'un fait réel doit y être
consigné.

### Étape 1 — Recherche documentaire ciblée (jamais une recherche web générale)

Identifier le thème de la question, puis consulter directement
`references/doc_index.md` (dans ce même dossier) pour trouver la ou les
pages officielles pertinentes — ce fichier indexe les pages par thème pour
éviter une recherche web à l'aveugle. Récupérer directement l'URL identifiée
(outil de fetch web disponible dans l'agent courant), pas via un moteur de
recherche générique.

**Cet index est un raccourci pour les questions courantes de ce repo, pas un
miroir exhaustif du site.** Si la question ne rentre dans aucune catégorie du
fichier index, ce n'est pas une impasse : `doc_index.md` explique, dans sa
section "Que faire si l'information n'est pas dans la table", l'ordre à
suivre (référence API Python générée, `how_to/`, puis recherche web réelle
scopée au site officiel — jamais une URL devinée par pattern sans la vérifier
par un fetch direct). Ne jamais conclure qu'une information n'existe pas dans
la doc Nautilus simplement parce qu'elle n'est pas dans cette table.

### Étape 2 — Vérification empirique sur le package réellement installé

La documentation web décrit l'intention de l'API ; elle ne garantit pas
qu'une signature précise n'a pas changé dans la version installée. Avant de
figer une signature ou une affirmation de classe dans un document ou du code,
vérifier empiriquement :

```powershell
python .agents\skills\nautilus-docs-research\scripts\introspect_nautilus.py <chemin.pointé.Symbole> [<autre.symbole> ...]
```

(Adapter le chemin de l'interpréteur Python si `nautilus_trader` vit dans un
environnement dédié — voir la décision E6 du plan Nautilus sur l'emplacement
du venv via `subst`, typiquement sous
`Implementation/adapters/nautilus_env/`.)

Le script affiche la version `nautilus_trader` installée, puis pour chaque
symbole demandé : sa signature réelle (`inspect.signature`), s'il s'agit
d'une classe ou d'une fonction/méthode, et ses membres publics s'il s'agit
d'une classe. S'il ne trouve pas `nautilus_trader` du tout dans
l'environnement courant, il le dit explicitement et s'arrête — **ne jamais
continuer en devinant** dans ce cas ; dire à l'utilisateur que
`nautilus_trader` n'est pas installé dans cet environnement et que la réponse
ne peut s'appuyer que sur la doc web (donc non vérifiée empiriquement).

### Étape 3 — Mettre à jour le cache

Ajouter ou mettre à jour une entrée dans
`Implementation/adapters/nautilus_env/NAUTILUS_API_NOTES.md` (créer le
fichier avec l'en-tête du gabarit ci-dessous s'il n'existe pas encore) pour
chaque fait nouvellement vérifié — pas pour une simple lecture de doc non
confirmée empiriquement si une vérification empirique était possible et n'a
pas été faite. Une entrée sans vérification empirique doit être marquée
explicitement `[NON VÉRIFIÉ EMPIRIQUEMENT]`.

Gabarit d'entrée (voir aussi `references/cache_template.md`) :

```markdown
### <Symbole ou question>

- **Fait vérifié** : <description précise, signature exacte si applicable>
- **Version nautilus_trader** : <ex. 1.230.0>
- **Date** : <AAAA-MM-JJ>
- **Source** : <URL doc exacte> et/ou "vérifié par introspection sur package installé (scripts/introspect_nautilus.py)"
```

### Étape 4 — Répondre en distinguant toujours les deux sources

Dans la réponse finale, ne jamais fusionner silencieusement "ce que dit la
doc" et "ce qui a été vérifié sur le package installé". Utiliser explicitement
deux registres :

- **Documenté (site officiel)** : ce que dit `nautilustrader.io/docs/latest/`
  — peut être en retard sur la version installée.
- **Vérifié empiriquement** : ce qui a été confirmé par introspection sur le
  package réellement installé — la source la plus fiable, à préférer chaque
  fois qu'un choix d'implémentation ou une affirmation de plan en dépend.

Si une seule des deux sources a pu être consultée (ex. package non installé),
le dire explicitement plutôt que de laisser croire à une double vérification.

## Fichiers de ce skill

- `references/doc_index.md` — index des pages officielles par thème, pour
  une recherche web ciblée (étape 1).
- `references/cache_template.md` — gabarit détaillé du fichier de cache
  (étape 3), avec un exemple rempli.
- `scripts/introspect_nautilus.py` — script d'introspection réutilisable
  (étape 2) : version installée, signature réelle, membres publics ; échoue
  explicitement si `nautilus_trader` n'est pas installé, ne devine jamais.
