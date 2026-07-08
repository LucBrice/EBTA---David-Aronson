# 📚 Code Architecture Evaluator - Complete Index

## 📂 Structure de la Skill

```
code-architecture-evaluator/
├── SKILL.md ............... [Cœur] Spécification complète & workflow
├── README.md .............. [Guide] Utilisation rapide & exemples
├── EXAMPLE_REPORT.md ....... [Exemple] Rapport d'audit complet (fictif)
├── WARP.md ................ [Optimisation] Performance & triggering
├── LICENSE ................ [Légal]
└── INDEX.md (ce fichier) ... [Navigation]
```

---

## 🚀 Démarrage Rapide

**Je veux auditer mon plan de refonte maintenant :**
1. Lire : `README.md` (5 min)
2. Préparer : Votre codebase (repomix recommandé)
3. Taper : `/evaluate`
4. Attendre : 5-15 minutes
5. Utiliser : Le rapport pour améliorer votre plan

---

## 📖 Guides par Besoin

### "Je comprends pas comment utiliser cette skill"
→ Lire : **README.md**
- Section : "Utilisation Rapide"
- Exemples concrets
- Cas d'usage

### "Je veux voir à quoi ressemble un rapport complet"
→ Lire : **EXAMPLE_REPORT.md**
- Rapport fictif : Refonte JWT + OAuth2
- 6 sections : Points forts → angles morts → plan phased
- Réaliste (150+ lignes de contenu)

### "Je veux comprendre en détail comment la skill fonctionne"
→ Lire : **SKILL.md**
- Phase 1 : Ingestion silencieuse
- Phase 2 : Extraction plan
- Phase 3 : Audit critique (6 sections)
- Règles absolues : zéro hallucination
- Triggers & commandes

### "Je veux optimiser les résultats et la performance"
→ Lire : **WARP.md**
- Trigger optimization
- Token budget guidance
- Templates (réduisent hallucination)
- Metrics & quality gates

---

## 🎯 Flux de Travail Complet

### Étape 1 : Préparer votre codebase

**Option A : Repomix (recommandé)**
```bash
npm install -g repomix
repomix --include "src/**" --ignore "node_modules,dist"
# → crée : repomix-output.xml ou .txt
```

**Option B : Fichiers directs**
Copiez les 5-10 fichiers les plus importants.

**Option C : URL GitHub**
```
https://github.com/user/repo
```

### Étape 2 : Préparer votre plan

Décrivez votre plan en texte libre :
```
Plan : Migration MongoDB → PostgreSQL

Contexte : Réduire dépendances NoSQL, améliorer querys complexes

Scope :
- UserRepository refactorisé
- Migrations DB v1-10
- Tests intégration updated

Timeline : 4 semaines
```

### Étape 3 : Déclencher l'audit

```
/evaluate

[Votre codebase repomix ou fichiers]

Plan de refonte :
[Votre plan textuel]
```

### Étape 4 : Lire le rapport

La skill génère 6 sections :
1. **Résumé exécutif** : Verdict rapide
2. **Points forts** : Alignements positifs
3. **Points faibles** : Problèmes identifiés
4. **Angles morts** : Checklist 8 points
5. **Standards** : Violations SOLID
6. **Plan rectifié** : Phases + risques + métriques

### Étape 5 : Affiner et ré-auditer (optionnel)

Après lecture du rapport :
```
Voici mes corrections :
[Décrire améliorations du plan]

/evaluate (Round 2)
```

---

## 🔧 Commandes Principales

| Commande | Usage | Durée |
|----------|-------|-------|
| `/evaluate` | Audit complet 6 sections | 10-15 min |
| `/eval-quick` | Rapide, principaux risques | 5 min |
| `/eval-deep` | Analyse exhaustive | 15-20 min |
| `/eval-risks` | Focus risques + angles morts | 7 min |
| `/eval-timeline` | Focus planning + phases | 8 min |

---

## 🎓 Concepts Clés à Comprendre

### Les 6 Sections du Rapport

#### 1. RÉSUMÉ EXÉCUTIF (1-3 lignes)
- Verdict : ✓ VALIDE / ⚠️ PROBLÉMATIQUE / ❌ NON-VIABLE
- Risk Level : MINIMAL / MODÉRÉ / ÉLEVÉ / CRITIQUE
- Cohérence % : 0-100%

#### 2. POINTS FORTS (3-5 items)
- Alignements positifs avec la structure existante
- Facilite la refonte
- Exemple : "Repository pattern existe → swap de driver facile"

#### 3. POINTS FAIBLES (3-7 items)
- Incohérences, over-engineering
- Risques de régression
- Exemple : "Sessions hardcodées → 50k users kickés"

#### 4. ANGLES MORTS (CHECKLIST 8 POINTS)
Souvent oubliés dans les plans :
- Migration de données
- Ruptures API
- Couverture tests
- Déploiement progressif
- Phase transitoire
- Monitoring
- Dépendances inversées
- Documentation

#### 5. ÉCARTS AUX STANDARDS
Violations SOLID :
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

#### 6. PLAN RECTIFIÉ
Version améliorée du plan :
- Phases 0-3 détaillées
- Tasks concrètes + livrables
- Risques identifiés
- Métriques de succès
- Plan de rollback

---

## 📚 Références

### Patterns Architecturaux
- MVC, CQRS, Event-Driven, Layered, Hexagonal, Microservices

### Principes
- SOLID (5 principes d'ingénierie)
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- YAGNI (You Aren't Gonna Need It)

### Stratégies Déploiement
- **Canary** : Progressif % traffic
- **Blue-Green** : Deux envs parallèles
- **Feature Flags** : Toggle logiciel
- **Dual-Run** : Ancien + nouveau côte à côte
- **Strangler Fig** : Wrapping graduel du legacy

### Sécurité
- JWT (tokens stateless)
- OAuth2 (délégation auth)
- OWASP (10 vulnérabilités principales)
- Secrets management (Vault, AWS Secrets)

---

## ❓ Questions Fréquentes

### Q: Combien de temps prend un audit ?
**A:** Dépend du scope:
- Petit plan + repo simple : 5-10 min
- Plan moyen + repo moyen : 10-15 min
- Plan complexe + gros repo : 15-30 min

Utilisez `/eval-quick` si vous êtes pressé.

### Q: Dois-je vraiment fournir le codebase complet ?
**A:** Pas nécessairement. Plus vous en fournissez, plus précis l'audit:
- Juste plan textuel : Audit rapide, très général
- 5-10 fichiers clés : Audit de qualité normale
- Repomix complet : Audit précis et détaillé

### Q: Et si mon plan est très floue ?
**A:** La skill utilisera [INCERTITUDE] pour signaler les parties floues.
Elle vous demandera des clarifications avant de continuer.

### Q: Peux-je ré-auditer après corrections ?
**A:** Oui ! Décrivez les corrections, `/evaluate` à nouveau.
La skill comparera avec le rapport précédent.

### Q: Quelle est la précision de la skill ?
**A:** La skill ne hallucine JAMAIS de fichiers ou patterns inexistants.
Elle pointe toujours vers des artefacts réels (fichiers, lignes).

Exceptions documentées avec [INCERTITUDE].

### Q: La skill me dit ma refonte est "non-viable". Que faire ?
**A:** Le rapport explique pourquoi. Souvent, des solutions sont proposées.
- Lisez la section "PLAN RECTIFIÉ"
- Utilisez les corrections
- `/evaluate` à nouveau après ajustements

---

## 🎯 Cas d'Usage Réels

### Cas 1: TechLead vérifiant un plan de refonte
```
→ Fournir : Codebase complet + plan écrit
→ Utiliser : `/evaluate`
→ Lire : Points faibles + angles morts
→ Livrable : Rapport à partager avec équipe
```

### Cas 2: Senior Dev auditing plan du junior
```
→ Fournir : Repomix du repo + plan du junior
→ Utiliser : `/eval-risks` (focus risques)
→ Lire : Angles morts et sécurité
→ Livrable : Feedback constructif pour junior
```

### Cas 3: Équipe migrant une tech majeure (DB, framework, etc)
```
→ Fournir : Codebase complet + plan détaillé
→ Utiliser : `/eval-deep` (60+ min)
→ Lire : Toutes sections, surtout plan rectifié
→ Livrable : Phases d'implémentation optimisées
```

### Cas 4: Code review rapide avant sprint
```
→ Fournir : Plan textuel court (5 fichiers clés)
→ Utiliser : `/eval-quick` (5 min)
→ Lire : Résumé exécutif + points faibles
→ Livrable : Oui/non, go/no-go decision
```

---

## 📞 Support & Questions

**Besoin d'aide ?**
1. Relire **README.md** (section pertinente)
2. Consulter **EXAMPLE_REPORT.md** (exemple similaire à votre cas)
3. Vérifier **SKILL.md** (détails techniques)

**Feedback / Bug report ?**
- Utilisez le thumbs-down button dans Claude
- Décrivez ce qui n'a pas fonctionné
- Suggestion : Ce qu'on aurait pu faire mieux

---

## 🚀 Prochaines Étapes

### Pour votre première utilisation :
1. Lire : `README.md` (quick start)
2. Consulter : `EXAMPLE_REPORT.md` (expected output)
3. Préparer : Votre codebase (repomix)
4. Taper : `/evaluate`
5. Profit ! 📈

### Pour maîtriser la skill :
1. Faire : 3-5 audits réels
2. Lire : Les rapports complètement
3. Appliquer : Les recommandations
4. Observer : Les résultats (plan plus solide)
5. Raffiner : Votre approche (angles morts?)

---

## 📊 Cheat Sheet

### Commandes Rapides
```
/evaluate        → Audit complet
/eval-quick      → 5 min (risques principaux)
/eval-deep       → 60 min (tout)
/eval-risks      → Focus sécurité/risques
/eval-timeline   → Focus phases/planning
```

### Formats d'Entrée
```
Repomix (XML/TXT)  → Recommandé pour gros repos
Fichiers directs   → Pour petits repos (< 50 files)
URL GitHub         → Suggérer repomix pour efficacité
```

### Structure Rapport
```
1. Résumé (1-3 lignes)
2. Points forts (3-5)
3. Points faibles (3-7)
4. Angles morts (checklist 8)
5. Standards (SOLID violations)
6. Plan rectifié (phases 0-3)
```

---

**Créé :** Mai 2025
**Version :** 1.0.0
**Statut :** Production-ready ✅
