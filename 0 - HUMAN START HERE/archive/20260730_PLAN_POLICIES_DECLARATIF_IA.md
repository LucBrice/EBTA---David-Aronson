# Brouillon — index déclaratif des autorisations IA

## Objectif

Créer `POLICIES.md` à la racine comme index compact des autorisations déjà
existantes. Chaque ligne utilise les colonnes :

```text
Action | Autorisée ? | Conditions | Validation requise | Source propriétaire
```

Le fichier ne remplace pas ses sources et ne crée aucune autorisation.

La colonne `Autorisée ?` utilise uniquement `OUI`, `CONDITIONNELLE` ou `NON`.
En cas de divergence, la source propriétaire citée prime et l'index doit être
corrigé ; il ne peut jamais servir à contourner une règle plus précise.

## Actions minimales à indexer

- exécuter un brouillon humain ;
- promouvoir `/start`, reprendre `/continue`, fermer `/close` ;
- modifier `.ai/governance/`, `Implementation/` ou `Protocole/` ;
- mettre à jour `.ai/checkpoint.json` ;
- modifier BACKTRADER ;
- créer une dépendance, un agent autonome, du RAG ou une base vectorielle ;
- créer les commits de baseline/clôture ;
- pousser vers un remote ;
- appliquer les skills spécialisés.

## Portée

- créer `POLICIES.md`;
- ajouter une ligne courte dans `AGENTS.md` qui le route après les workflows.

Hors portée : réécrire les règles sources, mécaniser un Policy Engine, modifier
`.ai/governance/`, `Protocole/` ou `Implementation/`.

## Vérification

- chaque ligne cite un chemin existant et son propriétaire ;
- aucune phrase ne prétend que `POLICIES.md` est normative ou exécutable ;
- les conditions restent des résumés courts ; les procédures détaillées sont
  uniquement pointées, jamais copiées ;
- aucun détail procédural long ne revient dans `AGENTS.md`;
- `git diff --check`.

## Journal `/evaluate`

| Passe | Résultat |
| --- | --- |
| 1 | Vocabulaire fermé et règle de priorité des sources ajoutés ; l'index ne peut pas s'auto-autoriser. |
| 2 | Convergence : actions minimales confrontées au bootstrap, workflows et checklist ; conditions bornées à des résumés avec pointeurs, aucun nouvel angle mort majeur. |
