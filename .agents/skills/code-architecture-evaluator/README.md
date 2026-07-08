# 🏗️ Code Architecture Evaluator

**Expert en audit d'architecture et ingénierie logicielle pour plans de refonte technique.**

Une skill Claude pour valider, critiquer et rectifier les plans de refonte en les confrontant aux réalités du codebase existant.

---

## ✨ Qu'est-ce que c'est ?

Vous avez un **plan de refonte technique** et vous voulez savoir :
- ✅ Que c'est solide et réaliste ?
- ❌ Qu'il y a des problèmes cachés ?
- 🔧 Comment l'améliorer ?

**Code Architecture Evaluator** délivre un audit **précis, sans hallucinations**, avec :
- Points forts et points faibles
- Angles morts souvent oubliés (migrations, tests, déploiement...)
- Violations des principes SOLID
- Plan d'implémentation rectifié et phased

---

## 🚀 Utilisation Rapide

### Étape 1 : Préparez votre codebase

**Option A - Repomix (recommandé pour gros repos)**
```bash
# Installer repomix si ce n'est pas fait
npm install -g repomix

# Exporter votre repo
repomix --include "src/**" --ignore "node_modules,dist,.env"

# Cela crée : repomix-output.xml ou .txt
```

**Option B - Fichiers directs**
Copiez vos fichiers clés directement dans le chat.

**Option C - URL GitHub**
```
https://github.com/user/repo
```

### Étape 2 : Décrivez votre plan de refonte

Texte libre ou structuré. Exemple :
```
Plan de refonte : Migration MongoDB → PostgreSQL

- Remplacer la couche data (UserRepository)
- Adapter les modèles (User schema)
- Créer les migrations DB
- Déployer progressivement
```

### Étape 3 : Déclenchez l'audit

```
/evaluate

[Votre codebase]

Plan de refonte :
[Votre plan]
```

**Boom !** Claude vous livre un audit complet en 5-10 minutes.

---

## 📋 Exemple de Rapport (Fictif)

```
# AUDIT : Migration MongoDB → PostgreSQL

## 1️⃣ RÉSUMÉ EXÉCUTIF
✓ Plan cohérent avec l'architecture actuelle
🟡 Risk Level : MODÉRÉ (migration données complexe)
Cohérence : 82% | Timeline : 4-5 semaines réaliste

## 2️⃣ POINTS FORTS
- [src/database/] Repository pattern déjà en place
  → Simplifie le swap de driver
  
- [test/integration/] Bonne couverture des contrats API
  → Permet de valider la régression

## 3️⃣ POINTS FAIBLES
- [src/models/User.ts] Hardcoding MongoDB (_id au lieu d'id)
  Impact : 15+ fichiers dépendants
  Sévérité : 🔴 CRITIQUE
  
- [Plan] Aucun rollback strategy mentionné
  Sévérité : 🔴 CRITIQUE

## 4️⃣ ANGLES MORTS
⚠️ ANGLE MORT : Migration de données
   Aucun script de transformation JSON → SQL fourni
   Impact : Data loss potentielle, downtime
   Suggestion : Écrire migration tool + tests

⚠️ ANGLE MORT : Déploiement progressif
   Pas de canary deploy ou feature flags
   Impact : Risque de downtime sur data massive
   Suggestion : Dual-run + feature flag pour 1-2 semaines

## 5️⃣ ÉCARTS STANDARDS
- SINGLE RESPONSIBILITY
  UserController gère auth + validation + business logic
  Fichier : src/controllers/UserController.ts (400+ lignes)
  Recommandation : Extraire AuthService + ValidationService

## 6️⃣ PLAN RECTIFIÉ
PHASE 0 (Semaine 1) : Préparation
  - Écrire migrations et tests (postgres-migrations/)
  - Feature flag pour UserRepository (POSTGRES_ENABLED)
  - Plan de rollback validé
  
PHASE 1 (Semaines 2-3) : Implémentation
  - Refactorer UserRepository (interface + implémentation PG)
  - Tests d'intégration validés
  - Code review cross-team
  
PHASE 2 (Semaines 4-5) : Migration
  - Canary 5% traffic → 100% progressif
  - Dual-run MongoDB + PostgreSQL en parallèle
  - Monitoring strict (latency, error rate, data consistency)
  
PHASE 3 (Semaine 6) : Cleanup
  - Supprimer ancien code MongoDB
  - Documenter patterns nouveaux
  - Retro équipe

Risques identifiés : [table détaillée]
Métriques de succès : [liste mesurable]
Plan de rollback : [instructions précises]
```

---

## 🔧 Commandes & Triggers

| Commande | Effet |
|----------|--------|
| `/evaluate` | Audit complet 6 sections |
| `/eval-quick` | 30min, focus principal |
| `/eval-deep` | Analyse exhaustive 60+ min |
| `/eval-risks` | Focus risques et angles morts |
| `/eval-timeline` | Focus phases et planning |

---

## 📚 Concepts Clés

### Les 6 Sections du Rapport

1. **RÉSUMÉ EXÉCUTIF** : Verdict en 2-3 lignes
2. **POINTS FORTS** : Alignements avec structure cible
3. **POINTS FAIBLES** : Incohérences et over-engineering
4. **ANGLES MORTS** : 8 checkpoints (migration, tests, déploiement, etc.)
5. **ÉCARTS STANDARDS** : Violations SOLID + bonnes pratiques
6. **PLAN RECTIFIÉ** : Phases phased, risques, métriques, rollback

### Règles Absolues

- ✗ JAMAIS suggérer un outil absent du repo
- ✓ TOUJOURS citer le fichier exact et la ligne
- ✓ TOUJOURS évaluer l'impact sur modules non-refondus
- ✗ JAMAIS halluciner (utiliser [INCERTITUDE] sinon)

### Angles Morts (8 points obligatoires)

```
1. Migration de données
2. Ruptures de contrats API
3. Couverture de tests
4. Déploiement progressif
5. Gestion phase transitoire
6. Monitoring & observabilité
7. Dépendances inversées
8. Documentation & onboarding
```

---

## 🎯 Cas d'Usage

### 1. Vous êtes TechLead
Vous avez un plan de refonte de l'équipe. Vous voulez :
- Valider que c'est solide
- Identifier les risques cachés
- Optimiser le timeline

→ `/evaluate` + rapport = 1 heure de travail évité

### 2. Vous faites une refonte seul(e)
Vous voulez une second pair of eyes avant de coder.
→ `/evaluate` te donne le feedback critique

### 3. Vous auditez du code legacy
Vous proposez une migration (tech stack, architecture, DB, etc.)
→ `/evaluate` te valide le plan contre la réalité du code

### 4. Code Review d'un plan de team mate
Au lieu d'écrire un long commentaire, passer par `/evaluate`
→ Rapport structuré, points de risque clairs

---

## 💡 Tips & Tricks

### Repomix Efficace
```bash
# Pour un gros repo, cibler src/
repomix --include "src/**" --style plain

# Exclure les gros fichiers
repomix --ignore "*.lock,dist/**,node_modules/**"

# Format texte (léger)
repomix --style plain > repomix-output.txt
```

### Plan Clair = Meilleur Audit
Un plan vague = rapport avec [INCERTITUDE] partout.

Structurez votre plan :
```
Plan : [Nom court]

Contexte : [Pourquoi cette refonte ? Contraintes métier ?]

Scope :
- Modules affectés : [Liste]
- Modules non-affectés : [Liste]

Architecture :
- Avant : [Schéma ou description]
- Après : [Schéma ou description]

Timeline proposée : [X semaines]

Hypothèses : [Quoi suppose-t-on vrai ?]
```

### Questions avant Audit
Si votre plan a des trous :
```
Avant d'auditer, clarifiez :
1. Comment gérer les données existantes ?
2. Quel déploiement strategy (canary, blue-green, etc.) ?
3. Qui dépend de l'API que je change ?
```

---

## 🚀 Workflow Complet

```
Jour 1 : Générer repomix + écrire plan draft
Jour 2 : /evaluate → obtenir rapport
Jour 3 : Lire rapport + ajuster plan
Jour 4 : /evaluate (round 2) → valider corrections
Jour 5 : Plan final prêt, commencer implémentation
```

---

## 📖 Référence

### Patterns Architecture
MVC, CQRS, Event-Driven, Layered, Hexagonal, Microservices

### Principes SOLID
- **S** : Single Responsibility
- **O** : Open/Closed
- **L** : Liskov Substitution
- **I** : Interface Segregation
- **D** : Dependency Inversion

### Stratégies Déploiement
- **Canary** : Progressif % traffic
- **Blue-Green** : Deux envs parallèles
- **Strangler Fig** : Graduel, wrapping legacy
- **Dual-Run** : Ancien + nouveau côte à côte
- **Feature Flags** : Toggle logiciel

### Observabilité
- **Metrics** : Latency, error rate, throughput
- **Logging** : Logs structurés (JSON)
- **Tracing** : Requête distribuée
- **Alerting** : SLO/SLI/SLA basés

---

## 📝 License

Cette skill fait partie de l'écosystème Claude Skills.

---

## 🤝 Support

Questions ou feedback ?
- GitHub Issues : [Si hébergé]
- Claude Community : [Lien]

Bon audit ! 🚀
