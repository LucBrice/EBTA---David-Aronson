# EXEMPLE COMPLET : Audit d'Architecture - Refonte API Authentification

**Cet exemple illustre la structure complète d'un rapport généré par la skill.**

---

## 📋 CONTEXTE FICTIF

**Codebase :** API Node.js / Express (5 ans, 150+ fichiers)
**Plan :** Migrer du système d'auth custom vers JWT + OAuth2
**Équipe :** 2 backend devs, 1 DevOps
**Timeline cible :** 4 semaines

---

## 1️⃣ RÉSUMÉ EXÉCUTIF

```
✓ Plan VALIDE et cohérent avec l'architecture actuelle
🟡 Risk Level : MODÉRÉ (migration d'authentification = critique métier)
Cohérence avec existant : 76%
Timeline réaliste : 4-5 semaines (plan de 4 sem est tight mais possible)
Score risque : 6.5/10 (acceptable avec mitigations)
```

**Verdict :** Le plan va dans la bonne direction (réduire dette tech d'auth), mais nécessite clarifications sur déploiement progressif et rollback.

---

## 2️⃣ POINTS FORTS

### ✅ Couche d'abstraction auth déjà en place
**Source :** `src/middleware/auth.ts` (lignes 1-50)

La logique d'authentification est isolée dans un middleware centralisé. Cela signifie qu'on peut :
- Substituer le driver d'auth sans toucher aux 40+ contrôleurs
- Implémenter JWT en parallèle de l'ancien système
- Tester indépendamment

**Impact positif :** Réduit le scope de refonte de 60% → 40%

---

### ✅ Tests d'authentification existants
**Source :** `test/unit/auth.test.ts` (400+ lignes), `test/integration/auth.integration.ts` (200+ lignes)

Bonne couverture des cas nominaux et edge cases. Permet de :
- Valider que le nouveau JWT respecte les mêmes contrats
- Réduire le risque de régression
- Avoir un filet de sécurité pendant la migration

**Impact positif :** Économise 2-3 jours de test écriture

---

### ✅ Architecture de déploiement existante
**Source :** `docker-compose.yml`, `kubernetes/*.yaml`

L'app est déjà containerisée et orchestrée. Infrastructure mûre permet :
- Feature flags sans refonte DevOps
- Canary deployment avec Helm
- Monitoring des deux versions en parallèle

**Impact positif :** Déploiement peut être progressif sans friction

---

### ✅ Services externalisés
**Source :** `src/services/oauth.ts` (stub only, non intégré), `config/external.json`

Structure de conf existe déjà pour services tiers. Ajouter OAuth2 nécessite juste :
- Implémenter les vrais appels OAuth
- Configurer credentials (secrets management existe)

**Impact positif :** Pas de refonte config/secrets needed

---

## 3️⃣ POINTS FAIBLES & INCOHÉRENCES

### ❌ Sessions en mémoire non documentées
**Source :** `src/middleware/auth.ts::checkSession()` (lignes 28-35)

```javascript
// ⚠️ Problème : Sessions stockées en variable module-level
const activeSessions = new Map(); // ← personne ailleurs dans le code ?
```

**Problème :** Comment migrer les sessions existantes vers JWT ? Aucune doc. Si vous supprimez l'ancien auth, vous perdez les sessions actives.

**Impact :** 🟡 Utilisateurs kickés lors du déploiement (potentiellement des milliers)

**Sévérité :** CRITIQUE

**Recommandation :** 
1. Documenter toutes les sessions actuelles
2. Plan de conversion sessions → JWT tokens
3. Période de double-read (accepter old + new tokens) pendant X jours

---

### ❌ Token expiration hardcoded
**Source :** `src/config/auth.js` (ligne 12)

```javascript
const TOKEN_EXPIRY = 24 * 60 * 60 * 1000; // 24h fixe, pas configurable
```

**Problème :** Pas d'env variable. Difficile d'ajuster en production sans rebuild. Plan ne mentionne pas comment gérer l'expiration JWT.

**Impact :** 🟡 Incompatibilité possible avec OAuth2 issuers (temps sync)

**Sévérité :** MOYEN

**Recommandation :** 
```javascript
const TOKEN_EXPIRY = parseInt(process.env.JWT_EXPIRY || '86400000');
// .env : JWT_EXPIRY=86400000 (24h), JWT_EXPIRY_OAUTH=3600000 (1h)?
```

---

### ❌ Gestion des refresh tokens absente du plan
**Source :** Plan mention "JWT tokens" mais aucune mention de refresh logic

**Problème :** JWT standards incluent refresh tokens. Plan prévoit juste access tokens. Aucune méthode pour :
- Réémettre tokens expirants sans re-login
- Révoquer tokens en cas de sécurité

**Impact :** 🔴 Régression UX (utilisateurs logués doivent se ré-authentifier toutes les 24h)

**Sévérité :** CRITIQUE

**Recommandation :** 
- Implémenter refresh token flow (voir RFC 6749)
- Storage : Redis ou DB ? (plan doit spécifier)

---

### ⚠️ OAuth2 scope & permissions non clarifiés
**Source :** Plan mentionne "OAuth2" mais aucun détail sur providers ni scopes

**Problème :** 
- Quels providers OAuth2 ? (Google, GitHub, Azure, custom ?)
- Quels scopes demander ? (email, profile, etc.)
- Mapping OAuth2 scopes → permissions système existant (admin, user, viewer) ?

**Impact :** 🟡 Implémentation peut diverger d'une personne à l'autre

**Sévérité :** MOYEN

**Recommandation :**
```
Clarifier avant coding :
□ OAuth2 Providers (Google login? GitHub?)
□ Scopes requis par provider
□ Mapping OAuth2 scopes → local roles (user, admin, etc.)
□ Exemples de requête OAuth2 authorize/token
```

---

## 4️⃣ ANGLES MORTS (CHECKLIST CRITIQUE)

### ⚠️ ANGLE MORT #1 : Migration des Sessions Existantes

**Décrit :** Convertir 50k sessions utilisateur en mémoire → JWT tokens

**Problème identifié :** 
- Aucun plan de convertion sessions → JWT
- Ancien système : sessions en Map (durée : 24h)
- Nouveau système : JWT (durée : variable)
- Risque : Tous les utilisateurs logged-in sont kickés au déploiement

**Impact si non adressé :** 
- Downtime utilisateur massive
- Problème de confiance (reconnexion fréquente)
- Support overload

**Mitigation suggérée :**
```
PHASE 1.5 (Semaine 3.5) : Migration Sessions
□ Dump all activeSessions to Redis (backup)
□ Script : sessions.ts → JWT tokens
□ Feature flag : HYBRID_AUTH=true (accepter old + new tokens)
□ Dual-run 48h : Ancien auth + JWT coexistent
□ Après 48h : Basculer 100% JWT
□ Garder Redis session dump 7 jours (rollback)
```

**Risque résiduel :** MOYEN (mitigable)

---

### ⚠️ ANGLE MORT #2 : Déploiement sans Downtime

**Décrit :** Comment garantir 0 downtime pendant la migration auth (critique) ?

**Problème identifié :** 
- Plan dit "déployer progressif" mais pas de détails
- Auth = middleware central, change = risqué
- Aucun mention de feature flags

**Impact si non adressé :** 
- 1-2h de downtime possible
- Utilisateurs disconnectés
- SLA breachées (99.99% → 99.9%)

**Mitigation suggérée :**
```
Feature Flag Pattern :
□ ENABLE_JWT_AUTH (defaut: false)
□ Deploy new code (JWT logic derrière le flag)
□ 5% users → ENABLE_JWT_AUTH=true + monitoring strict
□ 25% → 50% → 100% progressif
□ Fallback : ENABLE_JWT_AUTH=false = ancien système

Timeline :
Hour 1 : Deploy code, flag=off, monitoring
Hour 2-4 : 5% canary, check error rates, latency
Hour 5-8 : 25% if no issues
Hour 9-12 : 100% if 25% stable
Hour 13+ : Cleanup ancien code
```

**Risque résiduel :** MINIMAL (bien documenté)

---

### ⚠️ ANGLE MORT #3 : Tests de Sécurité Absent

**Décrit :** Comment valider que le nouveau JWT est aussi sécurisé que l'ancien système ?

**Problème identifié :** 
- Tests d'intégration existent (nominal cases)
- Aucune mention de :
  - Token forgery tests (signer des tokens invalides)
  - Token expiration edge cases
  - Secret key rotation strategy
  - HMAC vs RSA ? (plan dit JWT mais pas signature algo)

**Impact si non adressé :** 
- Vulnérabilité potentielle si implémentation JWT naive
- Tokens non-validés acceptés
- Secret key compromise sans rotation

**Mitigation suggérée :**
```
Ajouter tests sécurité :
□ test/security/jwt.test.ts
  - Token forgery attempts (signer avec secret fake)
  - Expiration validation (token + 1h)
  - Signature algorithms validation
  - Key rotation simulation
□ OWASP JWT best practices checklist
□ Code review sécu (cryptography expert?)
```

**Risque résiduel :** MOYEN (critère d'acceptation à définir)

---

### ⚠️ ANGLE MORT #4 : Gestion des Token Revocation

**Décrit :** Comment révoquer des tokens en cas de sécurité breach ?

**Problème identifié :** 
- JWT = stateless (pas de "revocation list" native)
- Plan ne mentionne pas :
  - Token blacklist (Redis?)
  - Logout strategy (invalider tokens côté client?)
  - Compromised key scenario (redéployer app?)

**Impact si non adressé :** 
- Ancien token reste valide même après logout
- Breach : tokens compromis restent valides 24h
- No way to force-logout utilisateurs

**Mitigation suggérée :**
```
Implémenter revocation :
□ Redis token blacklist (pattern: "revoked:jti:{id}")
□ Logout endpoint : Add token JTI to blacklist
□ Middleware check : Si token JTI in blacklist → reject
□ TTL Redis entry = token expiration time
□ Emergency plan : Rouler nouveau secret (tous les tokens invalides)

Exemple :
POST /logout
  token: "eyJhbGci..."
→ Extract JTI from token
→ SETEX redis revoked:jti:{jti} 86400 true
→ Client delete token
→ Requests avec ce token rejected
```

**Risque résiduel :** FAIBLE (pattern standard)

---

### ⚠️ ANGLE MORT #5 : Monitoring & Debugging Transition

**Décrit :** Comment détecter et debugger les problèmes pendant la migration ?

**Problème identifié :** 
- Plan dit "monitoring" mais aucun métrique spécifique
- Ancienne auth : logs custom (src/middleware/auth.ts)
- Nouvelle auth : logs JWT (à écrire)
- Pas de corrélation user ID / JWT token / session

**Impact si non adressé :** 
- Bug en production = impossible à tracer
- Utilisateurs dans "old session" vs "JWT token" = debug hell
- SLA breachées, cause unknown

**Mitigation suggérée :**
```
Ajouter observabilité :
□ Structured logs (JSON format)
  {
    "timestamp": "2024...",
    "auth_type": "JWT" | "SESSION",
    "user_id": "123",
    "token_jti": "abc...",
    "action": "login" | "logout" | "refresh",
    "status": "success" | "error",
    "error_reason": "expired" | "invalid_signature"
  }
□ Prometheus metrics
  - auth_attempts_total (by type: jwt vs session)
  - auth_errors_total (by error_type)
  - token_refresh_duration_seconds
□ Grafana dashboard : Auth transition metrics
□ Alerting rules
  - Error rate spike > 5% → alert
  - JWT validation failures > 100/min → alert
  - Token refresh latency p95 > 500ms → alert
```

**Risque résiduel :** FAIBLE (standard observability)

---

### ⚠️ ANGLE MORT #6 : Backward Compatibility API

**Décrit :** Clients APIs existants (mobile app, SPA, tiers) vont-ils continuer de marcher ?

**Problème identifié :** 
- Ancien auth : POST /login → returns session cookie
- Nouveau auth : POST /login → returns JWT token?
- Ancien client : envoie cookie automatiquement
- Nouveau client : envoie Authorization header

**Impact si non adressé :** 
- Mobile app v1.0 (en production) = broken après déploiement
- Impossible forcer upgrade (old versions still used)
- 30% utilisateurs sur old client = stuck

**Mitigation suggérée :**
```
API versioning strategy :
□ POST /auth/v1/login → OLD BEHAVIOR (session cookie) [deprecated]
□ POST /auth/v2/login → NEW BEHAVIOR (JWT token)
□ Middleware détecte client version, route approprié
□ Support dual : accepter cookie AND Authorization header

Timeline :
Week 1 : Déployer /v2, garder /v1
Week 2-4 : 90% users migrent vers /v2
Week 5+ : Deprecation warning pour /v1 users
Month 2 : /v1 endpoint shutdown

Fallback :
□ Old client send cookie : Accepter via middleware
□ New client send JWT : Accepter aussi
□ Pendant X mois : Support both
```

**Risque résiduel :** MINIMAL (standard versioning)

---

### ⚠️ ANGLE MORT #7 : Secrets Management

**Décrit :** Où et comment stocker JWT signing secret ?

**Problème identifié :** 
- Plan mentionne JWT mais pas secret key management
- .env file ? (visible en git ?)
- Vault ? AWS Secrets Manager ? (plan doit spécifier)
- Key rotation ? (redeployer app à chaque rotation ?)

**Impact si non adressé :** 
- Secret hardcoded → Git leak → Compromised tokens
- No key rotation → Impact majeur si breach

**Mitigation suggérée :**
```
Secrets setup :
□ USE : Vault (ou AWS Secrets Manager)
□ NOT : .env files, hardcoded, git-tracked
□ Key structure :
  - signing-secret-v1 (current)
  - signing-secret-v0 (previous, for rotation grace period)
□ Rotation : Every 3 months
  - Generate new key
  - Add to Vault as signing-secret-v2
  - Update app to accept v1 or v2 (backward compat)
  - After 30 days : Remove v1, upgrade v2→v1
□ Emergency : If secret leaked
  - Invalidate all tokens (or set revocation)
  - Roll new secret
  - Force re-login
```

**Risque résiduel :** FAIBLE (défini dans plan)

---

### ⚠️ ANGLE MORT #8 : Compliance & Audit Trails

**Décrit :** Comment logger et auditer les authentifications pour compliance (GDPR, SOC2, etc.) ?

**Problème identifié :** 
- Ancien système : logs de sessions (fichier local)
- Nouveau système : JWT (stateless, comment auditer ?)
- Plan ne mentionne pas : GDPR retention, audit trails, compliance requirements

**Impact si non adressé :** 
- Audit manquante → Compliance risk
- Legal issue si données perdue
- SOC2 certification impact

**Mitigation suggérée :**
```
Audit trail implementation :
□ Log all auth events (login, logout, token refresh, failure)
□ Format : user_id, timestamp, event, ip, user_agent, result
□ Store : Immutable log (PostgreSQL APPEND ONLY, ou S3)
□ Retention : 7 years (GDPR minimum for business logs)
□ Query : "Show all logins for user X in past 90 days"

Compliance :
□ Document auth flow (OIDC/JWT specs)
□ Document secret key management
□ Document revocation mechanism
□ Document retention policy
□ Regular security audits
```

**Risque résiduel :** MOYEN (définir requirements métier)

---

## 5️⃣ ÉCARTS AUX STANDARDS (SOLID + Bonnes Pratiques)

### 🔴 Single Responsibility Principle (SRP) Violation

**Principe :** Chaque classe/module doit avoir une et une seule raison de changer.

**Violation identifiée :**
```
Fichier : src/middleware/auth.ts (280 lignes)

Responsabilités actuelles :
1. Session validation (checkSession)
2. JWT token validation (checkJWT) ← Nouvelle
3. Request enrichment (attachUser)
4. Logging (logAuth)
5. Error handling (handleAuthError)

Problème : Tout mixé ensemble
→ Difficile à tester individuellement
→ Ajouter OAuth2 = 50 lignes de plus → même fichier
→ Reuse token validation ailleurs = copy/paste du code
```

**Recommandation :**
```typescript
// Refactorer en :
src/services/
  ├── auth/
  │   ├── SessionValidator.ts (check old sessions)
  │   ├── JWTValidator.ts (check JWT tokens)
  │   ├── OAuthValidator.ts (check OAuth2 tokens) ← NEW
  │   └── TokenService.ts (issue, refresh tokens)
  │
src/middleware/
  └── auth.ts (utilise les validators, simple orchestration)
```

**Impact :** Réduit couplage, facilite tests unitaires, extensible pour OAuth2

---

### 🟡 Open/Closed Principle (OCP) Violation

**Principe :** Code doit être ouvert à l'extension, fermé à la modification.

**Violation identifiée :**
```
Fichier : src/middleware/auth.ts::attachUser() (lignes 150-200)

Logique conditionnelle hardcodée :
if (hasSession) {
  // Session logic
} else if (hasJWT) {
  // JWT logic
}
// Ajouter OAuth2 = ajouter else if → modifie le fichier existant

Au lieu : Extension fermée (pas de modification)
```

**Recommandation :**
```typescript
// Utiliser Strategy pattern :
interface AuthStrategy {
  validate(request): Promise<User>;
}

class SessionAuthStrategy implements AuthStrategy { ... }
class JWTAuthStrategy implements AuthStrategy { ... }
class OAuthAuthStrategy implements AuthStrategy { ... }

// Middleware :
const strategies: AuthStrategy[] = [
  new JWTAuthStrategy(),
  new SessionAuthStrategy(),
  new OAuthAuthStrategy(),
];

for (const strategy of strategies) {
  try {
    user = await strategy.validate(request);
    if (user) break; // Found
  } catch { /* try next */ }
}
```

**Impact :** Ajouter OAuth2 = nouveau fichier, pas de modification existant

---

### 🔴 Dependency Inversion Principle (DIP) Violation

**Principe :** Dépendre d'abstractions, pas de concrétions.

**Violation identifiée :**
```
Fichier : src/middleware/auth.ts::checkJWT() (lignes 80-120)

Direct dépendance à librairie :
import * as jwt from 'jsonwebtoken';

jwt.verify(token, process.env.SECRET); ← Couplé à jsonwebtoken

Problème :
- Difficile à tester (mock jwt ?)
- Difficile à changer de librairie (jose, etc.)
- Pas de abstraction
```

**Recommandation :**
```typescript
// Créer interface :
interface JWTProvider {
  verify(token: string): Promise<JWTPayload>;
  sign(payload: JWTPayload): Promise<string>;
}

class JsonWebTokenProvider implements JWTProvider {
  constructor(private jwt = require('jsonwebtoken')) {}
  verify(token) { return this.jwt.verify(token, secret); }
  sign(payload) { return this.jwt.sign(payload, secret); }
}

// Mock pour tests :
class MockJWTProvider implements JWTProvider {
  verify(token) { return { sub: '123' }; } // Dummy
}

// Usage :
class AuthMiddleware {
  constructor(private jwtProvider: JWTProvider) {}
  checkJWT(token) { return this.jwtProvider.verify(token); }
}

// Test : new AuthMiddleware(new MockJWTProvider())
```

**Impact :** Testable, flexible, easy to swap implementations

---

### 🟡 Encapsulation Issue

**Problème identifié :**
```
Fichier : src/middleware/auth.ts (module scope)

Export public :
export const activeSessions = new Map();

Utilisé directement dans :
- src/services/UserService.ts
- src/controllers/UserController.ts

Problème : Couplage direct, pas d'interface

Recommandation :
export function getActiveSessions() { return activeSessions; }
export function addSession(userId, session) { ... }
export function removeSession(userId) { ... }

Au lieu :
import { activeSessions } from '...'; // direct Map manipulation
```

---

## 6️⃣ PLAN D'IMPLÉMENTATION RECTIFIÉ

# PLAN OPTIMISÉ : Migration JWT + OAuth2 Auth System

**Durée totale estimée :** 5 semaines (1 semaine de plus que proposé pour mitigations)

**Risk Level :** MODÉRÉ → MINIMAL (avec mitigations)

---

### 📅 SEMAINE 0 : PRÉPARATION (Important !)

#### Objectif
Établir les fondations, définir non-ambiguïtés, configurer infrastructure.

#### Tasks

**Task 0.1 : Clarifications & Décisions** [2 jours]
- [ ] Décider OAuth2 providers (Google, GitHub, ou custom ?)
- [ ] Définir scopes OAuth2 requis + mapping to local roles
- [ ] Décider storage refresh tokens (Redis, DB ?) → Créer tickets pour DevOps
- [ ] Décider strategy revocation (Redis blacklist ? Vault ?)
- [ ] Slack thread : Décisions documentées, alignement équipe

**Livrables :** `AUTH_MIGRATION_DECISIONS.md`

**Validation :**
- [ ] Decision doc reviewed et approuvé par TL + DevOps
- [ ] Pas de "TBD" dans le doc

---

**Task 0.2 : Infra & Tools Setup** [2 jours]
- [ ] Vault / AWS Secrets Manager : Setup JWT signing secret storage
- [ ] Redis : Setup pour token blacklist (5GB reservation)
- [ ] Feature flags system : Test que `ENABLE_JWT_AUTH` toggle fonctionne
- [ ] Monitoring : Prometheus exporters, Grafana dashboard template

**Livrables :**
- [ ] Vault secret created : `auth/jwt-signing-secret`
- [ ] Redis cluster connected + tested
- [ ] Feature flag toggle verified in staging
- [ ] Grafana dashboard deployed (empty, will fill Week 2+)

**Validation :**
- [ ] Load test : Feature flag toggle takes < 1s
- [ ] Monitoring : Can query feature flag states

---

**Task 0.3 : Test Infrastructure & Security Audit** [1.5 jour]
- [ ] Create `test/security/jwt.test.ts` skeleton
- [ ] Security code review scheduled (OWASP JWT best practices)
- [ ] Prepare API versioning (/auth/v1 legacy, /auth/v2 new)

**Livrables :**
- [ ] Test file with first 10 test cases (token forge, expiry, etc.)
- [ ] Security review calendar blocked

**Validation :**
- [ ] Test suite runs, 10 tests failing (expected)
- [ ] Security review scheduled with external expert

---

**Task 0.4 : Documentation & Compliance** [1 jour]
- [ ] Draft auth flow documentation (OIDC, JWT specs, OAuth2 flow)
- [ ] Draft audit trail logging spec
- [ ] Compliance requirements checklist (GDPR, SOC2, etc.)

**Livrables :**
- [ ] `AUTH_FLOW.md` (flow diagrams, endpoints, request/response)
- [ ] `AUDIT_TRAIL_SPEC.md` (what to log, retention, query patterns)
- [ ] `COMPLIANCE_CHECKLIST.md` (requirements → implementation)

**Validation :**
- [ ] Docs reviewed by legal/compliance team
- [ ] No blockers identified

---

**Risques cette phase :** 
- DevOps busy → request early
- Compliance requirements unclear → meet with legal NOW

**Critères de succès :**
- [ ] All decisions documented
- [ ] Infrastructure ready for code
- [ ] No "unknowns" left
- [ ] Team aligned on scope

---

### 📅 SEMAINE 1 : REFACTORING & ABSTRACTION

#### Objectif
Préparer le code existant pour coexister multiple auth strategies (session + JWT + OAuth).

#### Tasks

**Task 1.1 : Refactor src/middleware/auth.ts** [2 jours]
- [ ] Extract `SessionValidator` class → `src/services/auth/SessionValidator.ts`
- [ ] Create `AuthStrategyInterface` → `src/services/auth/types.ts`
- [ ] Create `JWTValidator` class (stub, no real implementation yet)
- [ ] Create `OAuthValidator` class (stub, no real implementation yet)
- [ ] Update `src/middleware/auth.ts` to use strategies (dispatch pattern)

**Code Changes :**

```typescript
// src/services/auth/types.ts
export interface AuthStrategy {
  name: string;
  canHandle(request): boolean;
  validate(request): Promise<AuthResult>;
}

export interface AuthResult {
  success: boolean;
  user?: User;
  error?: Error;
}

// src/services/auth/SessionValidator.ts
export class SessionValidator implements AuthStrategy {
  name = 'SESSION';
  
  canHandle(request) {
    return !!request.cookies?.session_id;
  }
  
  async validate(request) {
    try {
      const session = activeSessions.get(request.cookies.session_id);
      if (!session || isExpired(session)) {
        return { success: false, error: new Error('Session expired') };
      }
      return { success: true, user: session.user };
    } catch (e) {
      return { success: false, error: e };
    }
  }
}

// src/middleware/auth.ts (simplified)
export const authMiddleware = (strategies: AuthStrategy[]) => {
  return async (req, res, next) => {
    for (const strategy of strategies) {
      if (!strategy.canHandle(req)) continue;
      
      const result = await strategy.validate(req);
      if (result.success) {
        req.user = result.user;
        return next();
      }
    }
    res.status(401).json({ error: 'Unauthorized' });
  };
};
```

**Livrables :**
- [ ] `src/services/auth/types.ts`
- [ ] `src/services/auth/SessionValidator.ts`
- [ ] `src/services/auth/JWTValidator.ts` (stub)
- [ ] `src/services/auth/OAuthValidator.ts` (stub)
- [ ] Updated `src/middleware/auth.ts`

**Tests :**
- [ ] Unit tests for SessionValidator : 8 cases (valid, expired, missing, etc.)
- [ ] Unit tests for dispatch logic : 3 cases (session works, JWT stub, no auth)
- [ ] Integration tests : existing session flow still works

**Validation (CRITICAL) :**
- [ ] All existing tests still pass (regression check)
- [ ] Sessions work exactly as before (no behavior change)
- [ ] Code review : architecture looks clean

---

**Task 1.2 : Implement JWT Token Service (no validation yet)** [1.5 jours]

- [ ] Create `TokenService` → `src/services/auth/TokenService.ts`
- [ ] Implement JWT signing (using secret from Vault)
- [ ] Implement token refresh logic (issue new JWT)
- [ ] NO validation logic yet (that's Week 2)

**Code :**

```typescript
// src/services/auth/TokenService.ts
export interface JWTPayload {
  sub: string; // user ID
  email: string;
  roles: string[];
  iat: number;
  exp: number;
  jti: string; // unique token ID for revocation
}

export class TokenService {
  constructor(
    private secretProvider: SecretProvider, // from Vault
    private jtiGenerator = () => crypto.randomUUID(),
  ) {}
  
  async issueAccessToken(user: User, expiresIn = 3600): Promise<string> {
    const secret = await this.secretProvider.getSecret('auth/jwt-signing-secret');
    const payload: JWTPayload = {
      sub: user.id,
      email: user.email,
      roles: user.roles,
      iat: Math.floor(Date.now() / 1000),
      exp: Math.floor(Date.now() / 1000) + expiresIn,
      jti: this.jtiGenerator(),
    };
    return jwt.sign(payload, secret, { algorithm: 'HS256' });
  }
  
  async issueRefreshToken(user: User): Promise<string> {
    // Refresh tokens : longer expiry (7 days), stored in Redis
    const secret = await this.secretProvider.getSecret('auth/jwt-refresh-secret');
    const payload = { sub: user.id, type: 'refresh' };
    return jwt.sign(payload, secret, { expiresIn: '7d' });
  }
}
```

**Livrables :**
- [ ] `src/services/auth/TokenService.ts`
- [ ] `src/services/auth/SecretProvider.ts` (interface)
- [ ] `src/providers/VaultSecretProvider.ts` (Vault integration)

**Tests :**
- [ ] Unit tests : issueAccessToken, issueRefreshToken (mocked secret)
- [ ] Integration test : Real Vault secret fetch (staging only)

**Validation :**
- [ ] Tokens are valid JWTs (can decode with jwt.decode)
- [ ] JTI is unique per token
- [ ] Vault integration works in staging

---

**Task 1.3 : Audit Trail Logging** [1 jour]

- [ ] Create structured logging utility → `src/utils/auditLog.ts`
- [ ] Integrate into all auth flows (session, JWT, OAuth stubs)
- [ ] Store audit logs to immutable store (PostgreSQL APPEND table)

**Code :**

```typescript
// src/utils/auditLog.ts
export function logAuthEvent(event: {
  event_type: 'LOGIN' | 'LOGOUT' | 'TOKEN_REFRESH' | 'VALIDATION_FAIL';
  user_id?: string;
  auth_type: 'SESSION' | 'JWT' | 'OAUTH2';
  ip_address: string;
  user_agent: string;
  status: 'SUCCESS' | 'FAILURE';
  reason?: string;
  jti?: string;
}) {
  // Insert to PostgreSQL (immutable log table)
  // Also output structured JSON log
  console.log(JSON.stringify(event));
}
```

**Livrables :**
- [ ] Logging utility
- [ ] DB migration for audit_logs table
- [ ] Integrated into SessionValidator

**Tests :**
- [ ] Audit log created on successful auth
- [ ] Audit log created on failed auth
- [ ] Log contains user_id, ip, auth_type, etc.

---

**Risques :**
- Refactoring = risk of regression → Extra integration tests
- Vault access = DevOps dependency → Coordinate early

**Critères succès :**
- [ ] All existing auth tests pass (no regression)
- [ ] SessionValidator detachable from auth.ts
- [ ] Code review approval

---

### 📅 SEMAINE 2 : JWT VALIDATOR & REFRESH TOKEN IMPLEMENTATION

#### Objectif
Implement JWT token validation & refresh flow. Prepare feature flag controlled dual-auth.

#### Tasks

**Task 2.1 : JWT Validator Implementation** [1.5 jours]

- [ ] Implement `JWTValidator.ts` with full validation logic
- [ ] Token signature verification (using secret from Vault)
- [ ] Expiration checking
- [ ] Revocation check (Redis blacklist)
- [ ] JTI validation (unique token ID)

**Code :**

```typescript
// src/services/auth/JWTValidator.ts
export class JWTValidator implements AuthStrategy {
  name = 'JWT';
  
  constructor(
    private tokenService: TokenService,
    private revocationService: RevocationService,
    private metricsService: MetricsService,
  ) {}
  
  canHandle(request) {
    return !!request.headers.authorization?.startsWith('Bearer ');
  }
  
  async validate(request) {
    const token = request.headers.authorization.split(' ')[1];
    
    try {
      // 1. Verify signature & expiration
      const payload = await this.tokenService.verifyToken(token);
      
      // 2. Check revocation blacklist
      const isRevoked = await this.revocationService.isRevoked(payload.jti);
      if (isRevoked) {
        return { success: false, error: new Error('Token revoked') };
      }
      
      // 3. Fetch user
      const user = await User.findById(payload.sub);
      if (!user) {
        return { success: false, error: new Error('User not found') };
      }
      
      this.metricsService.recordJWTSuccess();
      return { success: true, user };
    } catch (error) {
      this.metricsService.recordJWTFailure(error.message);
      return { success: false, error };
    }
  }
}
```

**Listrables :**
- [ ] `src/services/auth/JWTValidator.ts` (complete)
- [ ] `src/services/auth/RevocationService.ts` (Redis blacklist)
- [ ] Metrics integration

**Tests :**
- [ ] Valid JWT accepted
- [ ] Expired JWT rejected
- [ ] Forged JWT rejected (wrong signature)
- [ ] Revoked JWT rejected
- [ ] Missing user → rejected
- [ ] Metrics recorded correctly

**Validation :**
- [ ] 100% test coverage for validator
- [ ] Security code review passes
- [ ] Vault + Redis integration works

---

**Task 2.2 : Refresh Token Endpoint** [1 jour]

- [ ] Implement `POST /auth/v2/refresh` endpoint
- [ ] Takes refresh token, returns new access token
- [ ] Store refresh tokens in Redis (with expiry & rotation)

**Code :**

```typescript
// src/routes/auth.ts
router.post('/auth/v2/refresh', async (req, res) => {
  const { refresh_token } = req.body;
  
  try {
    // Verify refresh token
    const payload = await tokenService.verifyRefreshToken(refresh_token);
    
    // Check if already rotated (prevent replay)
    const isUsed = await redis.get(`refresh_used:${payload.jti}`);
    if (isUsed) {
      // Suspicious: refresh token reused → force re-login
      res.status(401).json({ error: 'Token reuse detected' });
      return;
    }
    
    // Mark as used
    await redis.setex(`refresh_used:${payload.jti}`, 3600, 'used');
    
    // Issue new access token
    const user = await User.findById(payload.sub);
    const newAccessToken = await tokenService.issueAccessToken(user);
    
    auditLog({
      event_type: 'TOKEN_REFRESH',
      user_id: user.id,
      auth_type: 'JWT',
      status: 'SUCCESS',
    });
    
    res.json({ access_token: newAccessToken });
  } catch (error) {
    res.status(401).json({ error: error.message });
  }
});
```

**Livrables :**
- [ ] `POST /auth/v2/refresh` endpoint
- [ ] Refresh token rotation logic
- [ ] Replay attack prevention

**Tests :**
- [ ] Valid refresh → new access token
- [ ] Expired refresh → rejected
- [ ] Replay attack (reuse token) → rejected + security alert

---

**Task 2.3 : Feature Flag & Dual-Auth Mode** [1 jour]

- [ ] Add feature flag `ENABLE_JWT_AUTH` (default: false)
- [ ] When OFF : Use old SessionValidator only
- [ ] When ON : Try JWT first, fallback to Session (backward compat)
- [ ] Metrics : Track auth type used per request

**Code :**

```typescript
// src/middleware/auth.ts
export const authMiddleware = () => {
  const enableJWT = featureFlags.isEnabled('ENABLE_JWT_AUTH');
  
  let strategies = [];
  
  if (enableJWT) {
    strategies = [
      new JWTValidator(...),      // Try JWT first (new)
      new SessionValidator(...),  // Fallback to session (old)
    ];
  } else {
    strategies = [new SessionValidator(...)]; // Only session
  }
  
  return async (req, res, next) => {
    for (const strategy of strategies) {
      if (!strategy.canHandle(req)) continue;
      
      const result = await strategy.validate(req);
      if (result.success) {
        req.user = result.user;
        req.auth_type = strategy.name; // For metrics
        return next();
      }
    }
    res.status(401).json({ error: 'Unauthorized' });
  };
};
```

**Livrables :**
- [ ] Feature flag integration
- [ ] Strategy ordering logic
- [ ] Metrics tracking

**Tests :**
- [ ] Flag OFF : Only session works, JWT ignored
- [ ] Flag ON : JWT works, session fallback works
- [ ] Metrics : Track "auth_type_used"

---

**Risques :**
- Redis revocation performance → load test
- Token expiration edge cases → test thoroughly

**Critères succès :**
- [ ] JWT validation = bulletproof (security review)
- [ ] Refresh flow prevents replay attacks
- [ ] Feature flag working (tested in staging)

---

### 📅 SEMAINE 3 : OAuth2 INTEGRATION & MIGRATION PREP

#### Objectif
Implement OAuth2 validator. Prepare session-to-JWT migration strategy.

#### Tasks

**Task 3.1 : OAuth2 Validator** [2 jours]

- [ ] Implement `OAuthValidator.ts`
- [ ] Support multiple OAuth2 providers (Google, GitHub configurable)
- [ ] Scope mapping to local roles
- [ ] User creation on first-time OAuth login
- [ ] Token exchange (authorization code → access token)

**Code outline :**

```typescript
export class OAuthValidator implements AuthStrategy {
  name = 'OAUTH2';
  
  canHandle(request) {
    return !!request.query.code && !!request.query.state;
  }
  
  async validate(request) {
    const { code, state } = request.query;
    
    // Exchange auth code for access token (POST to OAuth2 provider)
    const providerToken = await this.exchangeCode(code, state);
    
    // Get user info from provider
    const oauthUser = await this.getUserInfo(providerToken);
    
    // Create or fetch local user
    let user = await User.findByEmail(oauthUser.email);
    if (!user) {
      user = await User.create({
        email: oauthUser.email,
        name: oauthUser.name,
        roles: this.scopesToRoles(oauthUser.scopes),
        auth_provider: 'google', // or github, etc.
      });
    }
    
    // Issue JWT token
    const token = await this.tokenService.issueAccessToken(user);
    
    return { success: true, user, token };
  }
}
```

**Livrables :**
- [ ] `src/services/auth/OAuthValidator.ts`
- [ ] `src/providers/GoogleOAuthProvider.ts`, `GitHubOAuthProvider.ts`
- [ ] Scope mapping config
- [ ] User creation flow

**Tests :**
- [ ] OAuth2 code exchange works
- [ ] User creation on first login
- [ ] Scope mapping to roles correct
- [ ] Existing user matched by email

---

**Task 3.2 : Session-to-JWT Migration Strategy** [1.5 jours]

- [ ] Implement session dump & migration script
- [ ] Sessions → Redis with TTL = original session expiry
- [ ] Script to convert Redis sessions → JWT tokens
- [ ] Validation : Migrated JWT contains same user_id + roles

**Code :**

```typescript
// scripts/migrate-sessions-to-jwt.ts
async function migrateSessionsToJWT() {
  // 1. Dump all activeSessions from memory
  const sessions = Array.from(activeSessions.entries());
  console.log(`Migrating ${sessions.length} sessions...`);
  
  // 2. For each session, create JWT
  for (const [sessionId, sessionData] of sessions) {
    const user = sessionData.user;
    
    // Create JWT with same expiration as session
    const jwtToken = await tokenService.issueAccessToken(
      user,
      sessionData.expiry - now, // remaining time
    );
    
    // Store mapping : sessionId → jwtToken (for during transition)
    await redis.setex(
      `session_migration:${sessionId}`,
      sessionData.expiry - now,
      jwtToken,
    );
    
    // Also send to client (next request, they'll use JWT)
    // This happens via cookie or client-side storage
  }
}

// During transition, middleware accepts both :
// Old cookie session_id → lookup mapping → convert to JWT
// New Authorization header with JWT → use directly
```

**Livrables :**
- [ ] Migration script
- [ ] Redis session storage
- [ ] Mapping session → JWT

**Tests :**
- [ ] All sessions migrated
- [ ] JWT token valid (can be verified)
- [ ] User ID + roles preserved
- [ ] TTL correct

---

**Task 3.3 : Monitoring & Alert Setup** [1 jour]

- [ ] Prometheus exporters for auth metrics
- [ ] Grafana dashboard (auth success/fail rates, by type)
- [ ] Alert rules (error rate spike, token validation failures)
- [ ] Structured logging output

**Metrics to track :**

```
auth_attempts_total{type="jwt|session|oauth",status="success|failure"}
auth_errors_total{type="jwt|session|oauth",reason="expired|invalid_sig|..."}
token_refresh_duration_seconds{quantile="p50|p95|p99"}
revocation_check_duration_seconds{quantile="p50|p95|p99"}
auth_strategy_dispatch_duration_seconds{quantile="p50|p95|p99"}
```

**Livrables :**
- [ ] Prometheus metrics
- [ ] Grafana dashboard JSON
- [ ] Alert rules (Prometheus AlertManager config)

---

**Risques :**
- Session dump might be large (millions of sessions?)
- Migration script needs load testing

**Critères succès :**
- [ ] OAuth2 implemented & tested
- [ ] Session migration script validated
- [ ] Monitoring dashboard visible & accurate

---

### 📅 SEMAINE 4 : HYBRID MODE & PRODUCTION PREP

#### Objectif
Enable dual-auth in staging. Load test. Prepare production canary deployment.

#### Tasks

**Task 4.1 : Enable Hybrid Auth in Staging** [2 jours]

- [ ] Enable feature flag `ENABLE_JWT_AUTH=true` in **staging only**
- [ ] Run session simulation : 1000 concurrent users with sessions
- [ ] Run JWT simulation : 1000 concurrent users with JWT tokens
- [ ] Monitor : metrics, errors, latency (p50, p95, p99)
- [ ] Load test refresh tokens : 100 refresh requests/sec

**Test scenarios :**

```
Scenario 1: Old client (session cookies)
  - Login via /auth/v1/login (old endpoint)
  - Use session cookie (no Authorization header)
  - Verify still works

Scenario 2: New client (JWT)
  - Login via /auth/v2/login (new endpoint)
  - Use Authorization header with JWT
  - Verify works

Scenario 3: Hybrid (both present)
  - Client has both session cookie AND Authorization header
  - Middleware tries JWT first, then session
  - Verify JWT is preferred, session used as fallback

Scenario 4: Token refresh under load
  - 100 concurrent refresh requests
  - Measure latency, error rate, Redis load
  - Verify no replay attacks
```

**Livrables :**
- [ ] Load test results (latency, error rate, CPU/memory)
- [ ] Screenshots of Grafana dashboard (before/during/after)
- [ ] Issues found + resolutions

**Validation (CRITICAL) :**
- [ ] Error rate < 0.1% (SLA requirement)
- [ ] Latency p99 < 500ms (requirement)
- [ ] No data corruption, no security issues
- [ ] Refresh token replay prevention works

---

**Task 4.2 : Production Deployment Plan** [1 jour]

- [ ] Document exact steps for production deployment
- [ ] Canary plan : 5% → 25% → 50% → 100%
- [ ] Rollback plan : If error rate > 2%, auto-rollback
- [ ] Communication plan : Notify support, ops, customers if needed
- [ ] Post-deployment checklist

**Deployment steps :**

```
1. Code deployment (flag OFF)
   - Deploy new auth code (JWT, OAuth strategies)
   - Feature flag ENABLE_JWT_AUTH = false (old behavior)
   - Verify no errors, metrics normal

2. Day 1 : 5% canary
   - ENABLE_JWT_AUTH = true for 5% users
   - Monitor error rate, latency, revocation/validation failures
   - Alert: If error rate > 2%, page on-call
   - Duration: 2 hours

3. Day 2 : 25% rollout
   - Increase to 25% if 5% stable
   - Same monitoring
   - Duration: 4 hours

4. Day 3 : 50% rollout
   - Increase to 50%
   - Prepare for cleanup (remove old auth code)
   - Duration: 4 hours

5. Day 4 : 100% rollout
   - Ramp to 100%
   - Run session migration script (background job)
   - Session → JWT mapping in Redis (keep for 7 days)
   - Duration: 2 hours

6. Day 5+ : Monitor & Cleanup
   - Keep session support 7 days (old clients might still use)
   - After 7 days: Remove SessionValidator from code
   - Update docs: JWT is now standard
```

**Livrables :**
- [ ] `DEPLOYMENT_RUNBOOK.md` (step-by-step)
- [ ] Rollback procedures
- [ ] Monitoring checklist

---

**Task 4.3 : Compliance & Security Finalization** [1 jour]

- [ ] Complete security code review (OWASP JWT best practices)
- [ ] Finalize audit trail logging (GDPR compliance)
- [ ] Document secret key rotation procedure
- [ ] Prepare SOC2 compliance documentation

**Checklist :**

```
Security :
☐ Token signature verified
☐ Token expiration enforced
☐ Refresh token rotation implemented
☐ Revocation list working
☐ Secret key from Vault (not hardcoded)
☐ No token in logs
☐ Rate limiting on /auth/v2/login (prevent brute force)
☐ Rate limiting on /auth/v2/refresh

Compliance :
☐ Audit trail logging all auth events
☐ Retention policy: 7 years
☐ Query: "Show all logins for user X"
☐ Data privacy: No PII in tokens
☐ SOC2 compliance: Documented key rotation, incidents, etc.
```

**Livrables :**
- [ ] Security review sign-off
- [ ] Compliance documentation
- [ ] Incident response plan

---

**Risques :**
- Production issues during canary → well-prepared rollback needed
- Performance regression → load test thoroughly before

**Critères succès :**
- [ ] Staging load test passes all scenarios
- [ ] Deployment plan documented & reviewed
- [ ] Security review passed
- [ ] Team trained on new auth flows

---

### 📅 SEMAINE 5 : PRODUCTION EXECUTION & CLEANUP

#### Objectif
Execute canary deployment. Monitor closely. Cleanup legacy auth code post-migration.

#### Tasks

**Task 5.1 : Canary Deployment (Production)** [Spanning Days 1-4]

- Execute deployment runbook
- Monitor metrics continuously
- If alert triggered : Execute rollback (< 2 min downtime target)
- Document incidents, timeline, resolution

**Monitoring checklist :**

```
Every 30 min during canary:
☐ Error rate (target < 0.1%)
☐ Latency p99 (target < 500ms)
☐ JWT validation failures (track reason : expired, invalid_sig, revoked)
☐ Token refresh latency
☐ Redis revocation check latency
☐ Vault secret fetch latency
☐ CPU / memory on auth service
☐ Database connection pool
☐ Customer complaints / support tickets

Auto-rollback if :
☐ Error rate > 2% for > 5 min
☐ Latency p99 > 2s for > 5 min
☐ Vault connectivity lost
☐ Redis unavailable
```

**Livrables :**
- [ ] Deployment log (dates, times, % ramp)
- [ ] Metrics snapshots (before/during/after each stage)
- [ ] Incident timeline (if any issues)
- [ ] Rollback procedures (if executed)

---

**Task 5.2 : Session Migration & Legacy Support** [Days 4-5]

- [ ] Run session migration script (background, non-blocking)
- [ ] Dump all activeSessions → Redis (mapping: sessionId → jwtToken)
- [ ] Old clients still use session cookie → convert on-the-fly to JWT
- [ ] Monitor : Are old clients still active ? (logs will show)
- [ ] Keep session support for 7 days (then remove)

**Code :**

```typescript
// During hybrid period, middleware:
if (ENABLE_JWT_AUTH) {
  // Try JWT first
  const jwtResult = await jwtValidator.validate(req);
  if (jwtResult.success) {
    req.user = jwtResult.user;
    req.auth_type = 'JWT';
    return next();
  }
  
  // Fallback to session
  const sessionResult = await sessionValidator.validate(req);
  if (sessionResult.success) {
    req.user = sessionResult.user;
    req.auth_type = 'SESSION'; // Track for metrics
    
    // Optionally : Issue JWT token to client (so next request uses JWT)
    const token = await tokenService.issueAccessToken(req.user);
    res.setHeader('X-New-Auth-Token', token);
    // Client can read this header and use JWT next time
  }
}
```

**Livrables :**
- [ ] Migration script output (how many sessions migrated)
- [ ] Metrics : Are old clients still using sessions ? (tail off timeline)
- [ ] After 7 days : Confirm <1% using session → OK to remove

---

**Task 5.3 : Cleanup & Documentation** [Day 5+]

- [ ] After 7 days of dual-support : Remove SessionValidator from code
- [ ] Update README / docs : "Auth is now JWT-based"
- [ ] Update client libraries / SDKs (use JWT pattern)
- [ ] Blog post / internal announcement (explain why we migrated)
- [ ] Lessons learned retro

**Cleanup steps :**

```
After 7 days confirmed < 1% session usage :
1. Remove SessionValidator.ts
2. Remove auth.ts legacy session handling
3. Remove activeSessions Map
4. Remove /auth/v1 endpoints (legacy)
5. Update docs/guides to use JWT only
6. Update client SDKs with JWT example
7. Update OpenAPI spec
8. Internal wiki update
```

**Livrables :**
- [ ] Cleanup PR merged
- [ ] Documentation updated
- [ ] Blog post published
- [ ] Retro notes (what went well, what we'd do different)

---

**Risques (Ongoing):**
- Support tickets from users (new auth system)
- Performance regressions post-cleanup

**Critères succès :**
- [ ] Zero downtime achieved
- [ ] Metrics improved (latency same or better)
- [ ] Transition smooth (support calls minimal)
- [ ] All old sessions migrated
- [ ] Clean code post-cleanup

---

## 📌 POINTS DE RISQUE IDENTIFIÉS

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|-----------|
| Session dump massive (millions) | Moyenne | Élevé | Pre-load test dump script, async execution |
| Vault secret unavailable | Basse | Critique | Fallback secret in .env (staging only), circuit breaker |
| Redis revocation overload | Moyenne | Élevé | Cache revocation checks, preload common tokens |
| Token forgery (bad implementation) | Moyenne | Critique | Security code review by expert, OWASP checklist |
| OAuth2 provider rate limits | Basse | Moyen | Implement backoff, queue, rate limit our own calls |
| Feature flag bug (stuck ON/OFF) | Basse | Critique | Test feature flag toggle 10+ times, manual override |
| Client confusion (cookie vs header) | Haute | Moyen | Documentation, /auth/v1 vs /auth/v2 clarity |
| Monitoring not working | Basse | Élevé | Test monitoring in staging under load |

---

## ✅ MÉTRIQUES DE SUCCÈS

- [ ] **Latency** : p50 < 100ms, p99 < 500ms (same as before, no regression)
- [ ] **Availability** : 99.99% SLA maintained (zero downtime)
- [ ] **Error rate** : < 0.1% (same as before)
- [ ] **Security** : Zero token forgeries, zero unauthorized access
- [ ] **Coverage** : 100% of users on JWT after 7 days (old sessions fully migrated)
- [ ] **Code quality** : Zero tech debt introduced (refactored cleanly)
- [ ] **Documentation** : Full audit trail logging in place, compliance ready
- [ ] **Team satisfaction** : Retro score 8+/10 (went smoothly)

---

## 🔄 PLAN DE ROLLBACK

### Scenario 1 : Error rate spike during canary (< 2h)

**Trigger :** Error rate > 2% for 5+ min

**Action :**
1. Page on-call engineer immediately
2. Feature flag `ENABLE_JWT_AUTH` → false
3. Traffic automatically reverts to SessionValidator
4. Downtime target : < 30 seconds
5. Investigate issue post-incident

**Post-rollback :**
1. Root cause analysis (logs, metrics)
2. Fix code issue
3. Load test fix in staging
4. Re-attempt canary next day

---

### Scenario 2 : Vault secret compromise (any time)

**Trigger :** Security incident, key leaked

**Action :**
1. Immediately rotate JWT signing secret in Vault
2. All new tokens use new secret
3. Old secret kept in Vault as "signing-secret-v0-revoked"
4. Middleware : Accept tokens signed with old OR new secret (grace period)
5. After 24h : Only new secret accepted, old tokens invalid
6. Logs show tokens invalid, users see "Please re-login"

**Post-incident :**
1. Security audit
2. Policy change (e.g., weekly key rotation instead of quarterly)

---

### Scenario 3 : OAuth2 provider unavailable

**Trigger :** OAuth2 provider down (e.g., Google auth down)

**Action :**
1. Fallback : Accept old JWT tokens without provider check
2. Disable OAuth2 validator (circuit breaker)
3. Users can login with existing JWT tokens
4. New OAuth logins fail → fallback to session login
5. When provider recovers : Re-enable OAuth2

**Post-incident :**
1. Implement provider health checks
2. Add circuit breaker pattern
3. Fallback auth method documented

---

### Scenario 4 : Full rollback to old auth system (catastrophic)

**Trigger :** Unforeseen architectural incompatibility discovered

**Action :**
1. Feature flag `ENABLE_JWT_AUTH` → false (< 1 min)
2. All traffic back to SessionValidator
3. Investigate root cause
4. Decision : Fix or abandon JWT migration
5. If fix : Restart Week 1, re-architect

**Duration :** < 2 minutes downtime

---

## 🚀 NEXT STEPS

1. **Approval :** Share this plan with team lead, DevOps, security
2. **Questions :** Are there any clarifications needed before starting ?
3. **Week 0 starts :** Immediately after approval
4. **Weekly syncs :** Every Monday, review progress & adjust if needed

---

## 📞 POINTS DE CONTACT

- **Tech Lead :** [Name] (decision-making, blockers)
- **DevOps :** [Name] (infrastructure, Vault, Redis, feature flags)
- **Security :** [Name] (JWT implementation review, secrets, compliance)
- **PM :** [Name] (timeline, business impact, communication)

---

# FIN DU PLAN D'IMPLÉMENTATION RECTIFIÉ
