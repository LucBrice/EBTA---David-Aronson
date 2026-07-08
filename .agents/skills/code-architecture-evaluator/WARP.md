# WARP - Skill Optimization Guide

This document helps optimize the skill's triggering and performance.

## 🎯 Trigger Optimization

### Primary Triggers (High Priority)
```
/evaluate
/eval-quick
/eval-deep
/eval-risks
```

When user says any of these → activate skill immediately.

### Secondary Triggers (Contextual)
```
"audite ce plan"
"critique ma refonte"
"audit d'architecture"
"review ma refonte technique"
"revue d'architecture"
```

### Semantic Variations
- User provides: codebase + refactoring plan → evaluate needed
- User asks: "Is this architecture good ?" + code → evaluate
- User provides: GitHub repo + proposed changes → evaluate

## ⚡ Performance Optimization

### Context Window Usage
- **Phase 1 (Ingestion)** : Heavy read (codebase), silent processing
  - Cost: High tokens consumed reading code
  - Mitigation: Ask user to provide repomix (compressed format)
  
- **Phase 2 (Audit)** : Moderate write (report generation)
  - Cost: Lower token usage (structured output)
  - Strategy: Provide templates to reduce generation

- **Phase 3 (Plan)** : Heavy write (implementation plan)
  - Cost: Highest token usage (detailed steps)
  - Mitigation: Use templates, avoid hallucination (use [INCERTITUDE])

### Token Budget Guidance
- Small repo (< 10 files) : ~5K-10K tokens
- Medium repo (50 files) : ~20K-30K tokens
- Large repo (200+ files) : ~50K+ tokens (suggest repomix compression)

### Suggested Skill Invocation Pattern
```
User: /evaluate
  ↓
Skill: Request codebase (prefer repomix)
  ↓
User: [provides repomix or files]
  ↓
Skill: Request plan description
  ↓
User: [describes plan]
  ↓
Skill: Generate 6-section audit (40-50min)
```

## 🎨 Template-Based Generation

To reduce hallucination and token usage, use templates for:

### Report Template
```markdown
# AUDIT : [PROJECT_NAME]

## 1️⃣ RÉSUMÉ EXÉCUTIF
[Fill in: verdict, risk level, cohesion %]

## 2️⃣ POINTS FORTS
[List 3-5 with files + reasoning]

## 3️⃣ POINTS FAIBLES
[List 3-7 with severity]

## 4️⃣ ANGLES MORTS
[Run through 8-point checklist]

## 5️⃣ ÉCARTS AUX STANDARDS
[Check SOLID violations]

## 6️⃣ PLAN RECTIFIÉ
[Use phased template below]
```

### Implementation Plan Template
```markdown
# PLAN D'IMPLÉMENTATION : [FEATURE_NAME]

## PHASE 0 : PRÉPARATION
- [ ] Task 0.1 : [What, why, deliverables, validation]
- [ ] Task 0.2 : ...

## PHASE 1 : IMPLÉMENTATION
- [ ] Task 1.1 : ...

## PHASE 2 : MIGRATION
- [ ] Task 2.1 : ...

## PHASE 3 : CLEANUP
- [ ] Task 3.1 : ...

## Risques & Métriques
[Table + bullets]

## Plan de Rollback
[Specific scenarios + actions]
```

Using templates reduces token overhead by ~30%.

## 📊 Metrics & Quality Gates

### When to Use Shortcodes
- `/eval-quick` : User in hurry, wants 30-min review
  - Skip deep SOLID analysis
  - Focus: top 3 points forts + 3 faibles + angles morts
  
- `/eval-deep` : Full analysis (60+ min)
  - All 6 sections complete
  - Extended examples
  
- `/eval-risks` : Security/risk focus only
  - Skip standards (SOLID)
  - Heavy on angles morts + rollback
  
- `/eval-timeline` : Project planning focus
  - Detailed Phase 0-3 tasks
  - Risk matrix
  - Metrics & rollback

## 🎯 Quality Checklist

Before returning audit, verify:

- [ ] No hallucinations (files/functions mentioned actually exist)
- [ ] No [INCERTITUDE] used unless truly ambiguous
- [ ] All code citations have line numbers
- [ ] Angles morts section complete (8/8 points)
- [ ] Plan is phased & actionable (not abstract)
- [ ] Metrics are measurable (not "improve performance")

Audit quality = Customer trust.

## 🚀 Usage Analytics

Suggested metrics to track:

```
- Audits completed (count)
- Average duration (min)
- User satisfaction (feedback)
- Most common issues found (top 3)
- Most common angles morts missed (which category)
```

This helps improve the skill over time.

---

**Last Updated:** May 2025
**Version:** 1.0.0
