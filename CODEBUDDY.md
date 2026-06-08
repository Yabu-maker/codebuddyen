---
description: CloudBase AI Development Rules Guide - Provides scenario-based best practices to ensure development quality
globs: *
alwaysApply: true
inclusion: always
---

# CloudBase AI Development Rules Guide

## Activation Contract

This file is a compatibility projection of the CloudBase routing contract. Keep its semantics aligned with the CloudBase source guideline, and express routing with stable skill identifiers rather than repo-specific file paths.

## Table of Contents

1. [Existing Implementation First](#existing-implementation-first)
2. [Rule File Path Resolution](#rule-file-path-resolution)
3. [Engineering Constitution](#engineering-constitution)
4. [High-Priority Routing Table](#high-priority-routing-table)
5. [Scenario-Based Quick Reference](#scenario-based-quick-reference)
6. [Core Capabilities](#core-capabilities)
7. [Development Workflow](#development-workflow)
8. [Deployment Workflow](#deployment-workflow)
9. [Rule File Reference](#rule-file-reference)
10. [Quality Checklist](#quality-checklist)
11. [Console Entry Points](#console-entry-points)

---

## Existing Implementation First

When the workspace already contains an existing application with explicit TODO markers, fixed routes, or pre-created pages and services:

- Do **not** start with `ui-design`, design specs, or visual exploration unless the user explicitly asks for UI redesign.
- Do **not** broad-read unrelated skills first.
- First inspect the existing implementation surfaces that already own the flow, such as `src/lib/backend.*`, `src/lib/auth.*`, `src/lib/*service.*`, route guards, and the actual page or form handlers wired to submit buttons.
- Prefer implementing TODOs and fixing the real broken flow in-place over creating parallel helpers, extra demo pages, or detached example code.
- For login + CRUD applications, use the shortest path: inspect existing code -> verify provider readiness if required -> patch the active handlers -> validate the changed flow.

### Global Must-Read Rules

- Identify the scenario first. Do not start implementation before reading the matching rule file.
- Login or registration request -> read `{auth-tool}` first, then the platform auth rule.
- Keep auth domains separate: management-side login uses `auth`; app-side auth configuration uses `queryAppAuth` / `manageAppAuth`.
- When writing MCP or tool results to a local file with a generic file-writing tool, pass text rather than raw objects. For JSON files, serialize first with `JSON.stringify(result, null, 2)` and write that string.
- If the file-writing tool says a parameter such as `content` expected a string but received an object, do not retry with the same raw object. Serialize the object first, then retry once with the serialized text.
- UI request -> read `rules/ui-design/rule.md` first and output the design specification before code.
- Native App / Flutter / React Native request -> route to `{http-api}`, not Web SDK rules.
- Cloud Function request -> route to `{cloud-functions}`, not `cloudrun-development`, unless the task explicitly needs container service behavior.
- Generated, mirrored, or IDE-specific artifacts are compatibility outputs, not the primary semantic source.

---

## Rule File Path Resolution

**CRITICAL: All rule file paths in this document follow a smart resolution strategy to support multiple AI editors.**

When this document references a rule file (e.g., `{auth-web}`), try locations in this order:

1. **CodeBuddy Path**: `.codebuddy/rules/tcb/rules/{rule-name}/rule.md`
2. **Universal Path**: `rules/{rule-name}/rule.md`
3. **Fallback Search**: Use `search_file` with pattern `*{rule-name}*rule.md`

> **Note**: Files already using `rules/` prefix (like `rules/ui-design/rule.md`) work universally across all editors and don't need path resolution.

### Rule Name Mapping

| Shorthand | Full Name |
|-----------|-----------|
| `auth-tool` | Authentication Tool Configuration |
| `auth-web` | Web Authentication |
| `auth-wechat` | WeChat Mini Program Authentication |
| `auth-nodejs` | Node.js Authentication |
| `web-development` | Web Platform Development |
| `miniprogram-development` | Mini Program Platform Development |
| `cloudrun-development` | CloudRun Backend Development |
| `cloud-functions` | Cloud Functions Development |
| `http-api` | HTTP API Usage |
| `relational-database-tool` | MySQL Database Tool Operations |
| `relational-database-web` | MySQL Web SDK |
| `no-sql-web-sdk` | NoSQL Web SDK |
| `no-sql-wx-mp-sdk` | NoSQL WeChat Mini Program SDK |
| `cloudbase-platform` | CloudBase Platform Knowledge |
| `cloud-storage-web` | Cloud Storage Web SDK |
| `ui-design` | UI Design Guidelines |
| `spec-workflow` | Software Engineering Workflow |
| `data-model-creation` | Data Model Creation |
| `ai-model-web` | AI Model Calling (Web SDK) |
| `ai-model-nodejs` | AI Model Calling (Node SDK) |
| `ai-model-wechat` | AI Model Calling (WeChat Mini Program) |

---

## Engineering Constitution

These rules override convenience. They are a gate before saying "done". Applies to **every scenario**.

- **Do NOT use `any` to bypass type errors.** Not `: any`, not `as any`, not `@ts-ignore`, not `@ts-nocheck`. Use `unknown` + type guard, precise `interface`, or `declare module` augmentation instead.
- **Self-verify before claiming done.** Static layer (`tsc --noEmit` / lint / build / tests) **and** runtime layer (use agent-browser for user-visible flows). "It should work" without evidence is not acceptable.
- **Do not paper over failures.** No empty `try/catch` to silence bugs, no skipping/deleting failing tests, "it compiles" is not "it works".
- **`ai.createModel(...)` argument is a GroupName, not a vendor/model id.** Only: `"cloudbase"` (default), `"hunyuan-exp"` (Mini Program Growth Plan), or `"custom-<name>"`. The concrete model id goes into the **`model` field** of `generateText`/`streamText`, never into `createModel(...)`.

---

## High-Priority Routing Table

| Scenario | Read First | Then Read | Avoid | Pre-Action Check |
|----------|------------|-----------|-------|------------------|
| Web login/register | `{auth-tool}` | `{auth-web}`, `{web-dev}` | `{cloud-func}`, `{http-api}` | Provider status & publishable key |
| Mini program + CB | `{miniprogram-dev}` | `{auth-wechat}`, `{no-sql-wx-mp}` | `{auth-web}`, `{web-dev}` | Uses `wx.cloud`? |
| Native App / HTTP | `{http-api}` | `{auth-tool}`, `{relational-db-tool}` | `{auth-web}`, `{no-sql-web}` | SDK boundary, OpenAPI |
| Cloud Functions | `{cloud-functions}` | domain rule | `{cloudrun-dev}` | Event vs HTTP, runtime |
| CloudRun backend | `{cloudrun-dev}` | domain rule | `{cloud-functions}` | Container, Dockerfile, CORS |
| UI generation | `rules/ui-design/rule.md` | platform rule | backend-only rules | Design spec first |

---

## Scenario-Based Quick Reference

> Step 0 for ALL scenarios: Call `envQuery(action=info)` first to get environment ID.

### Web Project (React/Vue/JS)

1. **Environment**: `envQuery(action=info)` — auto-use returned envId
2. **Existing code?** Inspect & patch active handlers first; don't recreate structure
3. **UI work only if needed**: Read `rules/ui-design/rule.md` → output design spec → then code. Skip if just completing functionality on existing app.
4. **Auth (if needed)**: MUST read `{auth-tool}` FIRST → check/enable providers → THEN implement frontend. Use Web SDK built-in auth (`{auth-web}`). Route users to custom `/login` page, NOT hosted login page.
5. **Platform rules**: `{web-development}`
6. **Database**:
   - NoSQL: `{no-sql-web-sdk}`
   - MySQL: `{relational-database-web}` (app code) + `{relational-database-tool}` (management)
7. **AI models**: `{ai-model-web}`

### Mini Program Project

1. **Environment**: `envQuery(action=info)`
2. **UI (MANDATORY)**: MUST read `rules/ui-design/rule.md` FIRST → output design spec → then code. No exceptions.
3. **Platform rules**: `{miniprogram-development}`
4. **Auth**: Naturally login-free, get `wxContext.OPENID` in cloud functions (`{auth-wechat}`)
5. **Database**:
   - NoSQL: `{no-sql-wx-mp-sdk}`
   - MySQL: `{relational-database-tool}` (via tools only)
6. **AI models**: `{ai-model-wechat}`
7. **TabBar icons**: Download via `downloadRemoteFile`, must be **png** format (Unsplash/wikimedia/Pexels/Apple UI)

### Native App (iOS/Android/Flutter/RN/etc.)

1. **Environment**: `envQuery(action=info)`
2. **⚠️ SDK NOT supported** — MUST use HTTP API for everything
3. **UI (MANDATORY)**: MUST read `rules/ui-design/rule.md` FIRST → output design spec → then code
4. **Required rules (MANDATORY)**:
   - `{http-api}` — all CloudBase operations
   - `{relational-database-tool}` — MySQL operations
   - `{auth-tool}` — auth configuration
5. **⚠️ Database limitation**: Only MySQL supported. If user needs MySQL, **MUST prompt enable in console first**: [Enable MySQL](https://tcb.cloud.tencent.com/dev?envId=${envId}#/db/mysql/table/default/)
6. **Optional**: `{cloudbase-platform}`, `{ui-design}`, `{ai-model-nodejs}`

### CloudRun Backend (Java/Go/Python/Node.js/PHP)

1. **Environment**: `envQuery(action=info)`
2. **Rules**: `{cloudrun-development}`
3. **Requirements**: Dockerfile, CORS support, container boundary awareness

### Cloud Functions (Event/HTTP)

1. **Environment**: `envQuery(action=info)`
2. **Rules**: `{cloud-functions}`
3. **Deployment**: `queryFunctions` → `manageFunctions(action="createFunction")` / `manageFunctions(action="updateFunctionCode")`. Runtime CANNOT change after creation.
4. **Event vs HTTP**:
   - Event: `exports.main = async (event, context) => {}`
   - HTTP: listen port `9000`, include `scf_bootstrap`, use native `http.createServer`

---

## Core Capabilities

### 0. Configuration-First Principle (HIGHEST PRIORITY)

**🚨 Always check and configure CloudBase services BEFORE implementing code.**

**Authentication trigger words** — when user mentions ANY of these, read `{auth-tool}` FIRST:
Phone/SMS/Mobile login, Email, WeChat, Username/password, Anonymous/Guest, Login/Register/Auth/Sign in/up

**Auth execution sequence**: Read `{auth-tool}` → `callCloudApi` check config → `queryAppAuth`/`manageAppAuth` enable methods → verify effective → implement frontend code

### 1. UI Design (CRITICAL)

**🚨 MANDATORY for ALL tasks involving pages, interfaces, components, styles, or any frontend visuals:**
1. **MUST FIRST read** `rules/ui-design/rule.md` via file reading tool — NO skipping
2. **MUST output design spec** before code:
   - Purpose Statement
   - Aesthetic Direction (specific options, NOT generic terms)
   - Color Palette (hex codes, avoid forbidden colors)
   - Typography (specific font names, avoid forbidden fonts)
   - Layout Strategy (asymmetric/creative, avoid centered templates)
3. **MUST ensure** distinctive aesthetic quality; avoid generic AI aesthetics

**Exception**: Existing app with prebuilt pages + TODOs where user wants functional completion, not redesign → patch directly.

**Violation detection**: If you catch yourself writing UI code without having read `rules/ui-design/rule.md`, STOP and read it first.

### 2. Database + Authentication

| Platform | Auth Method | NoSQL | MySQL |
|----------|-------------|-------|-------|
| **Web** | Web SDK built-in (`{auth-web}`) | `{no-sql-web-sdk}` | `{relational-database-web}` + `{relational-database-tool}` |
| **Mini Program** | Login-free, OPENID in cloud func (`{auth-wechat}`) | `{no-sql-wx-mp-sdk}` | `{relational-database-tool}` |
| **Native App** | HTTP API (`{http-api}`) | Not supported | `{relational-database-tool}` (MySQL ONLY) |
| **Node.js Backend** | Server-side (`{auth-nodejs}`) | N/A | Via SDK or tools |

### 3. Web App Deployment (CloudApp / Static Hosting)

**Primary path — CloudApp (independent subdomain):**
- `manageApps(action="deployApp")` with `framework="static"`, `installCmd=""`, `buildCmd=""` — deploys pre-built dist/
- Domain: `<serviceName>-<envId>.webapps.tcloudbase.com`
- Custom domain: `manageGateway(action="bindCustomDomain")`
- Poll status: `queryApps(action="getAppVersion", buildId)`; on failure: `queryApps(action="getBuildLog", buildId)`

**Compatibility warning**: Don't switch deploy methods on existing projects — old URLs will break. Check with `queryHosting` first.

**Fallback — Static Hosting (shared domain):**
- `manageHosting(action="upload")` with `cloudPath="/<serviceName>"`
- Domain: `<envId>-<appId>.tcloudbaseapp.com/<cloudPath>`
- CDN has ~few minutes cache after deployment; use random queryString for links

### 4. Backend Deployment (Cloud Functions or CloudRun)

- **Cloud Functions**: Refer to `{cloud-functions}`. Use `queryFunctions` → `manageFunctions(...)`. Runtime locked at creation. Point `functionRootPath` to parent dir (e.g., `cloudfunctions/`).
- **CloudRun**: Refer to `{cloudrun-development}`. Use `manageCloudRun`. Ensure CORS, prepare Dockerfile. Set MinNum >= 1 to reduce cold starts.

---

## Development Workflow

### Pre-Work Checklist

1. **[ ] Environment Check**: `envQuery(action=info)` — get envId, use it everywhere
2. **[ ] Scenario Identification**: Web / Mini Program / Native / CloudRun / Cloud Function / DB-only / UI / AI
3. **[ ] Existing Implementation**: If workspace has target pages/services, patch don't recreate
4. **[ ] Auth Triggered?** If yes → `{auth-tool}` FIRST → configure → then code
5. **[ ] UI Work?** If yes → read `rules/ui-design/rule.md` FIRST → design spec → then code

### Core Behavior Rules

1. **Tool Priority**: CloudBase operations must use CloudBase tools
2. **Project Understanding**: Read README.md first, follow project instructions
3. **Directory Awareness**: Check current directory before outputting code
4. **Dev Order**: Frontend first, then backend
5. **Backend Strategy**: Prefer SDK direct DB calls over cloud functions unless complex logic/third-party APIs/server-side computation needed
6. **Deploy Order**: Deploy backend before previewing frontend
7. **Interactive Confirmation**: Clarify ambiguous requirements; confirm before high-risk operations
8. **Real-time Comm**: Use CloudBase real-time database watch capability when applicable

### Mini Program Specifics

- Suggest WeChat Developer Tools for preview/debug/publish
- Confirm `project.config.json` has `appid` configured
- Open via CLI:
  - Windows: `"C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat" open --project "<root>"`
  - macOS: `/Applications/wechatwebdevtools.app/Contents/MacOS/cli open --project "<root>"`

### Documentation Generation

- Generate `README.md` after project creation: name, description, architecture, CloudBase resources used
- After deployment: write access URLs to documentation
- Optionally generate `cloudbaserc.json` for resource visibility

### Tool Interface Rules

- Understand data types of all interface parameters and return values before calling
- Check docs/tool descriptions first when unsure
- Example pitfall: many interfaces require boolean `confirm` param; omitting or wrong type causes errors

### Environment ID Auto-Configuration

- Auto-use envId from `envQuery` in config files (`cloudbaserc.json`, `project.config.json`)
- Resolve aliases via `envQuery(action=list, alias=..., aliasExact=true)`; never pass aliases into SDK init/console URLs/config files
- In code examples, auto-fill current envId — no manual replacement needed

---

## Deployment Workflow

When user requests deployment to CloudBase:

### Step 0: Check Existing Deployment

- Read `README.md` for prior deployment info
- Identify previously deployed services and URLs
- Determine: new deployment or update?

### Step 1: Backend Deployment (if applicable)

**Cloud Functions (Node.js only)**:
- Use `queryFunctions` to inspect → `manageFunctions(action="createFunction")` or `manageFunctions(action="updateFunctionCode")`
- Decide Event vs HTTP before creating (runtime locked):
  - **Event**: `exports.main = async (event, context) => {}`
  - **HTTP**: listen port `9000`, include `scf_bootstrap`, native `http.createServer`, manual req.body parsing, explicit response headers

**CloudRun (all other languages + Node.js containers)**:
- Ensure CORS support, prepare Dockerfile
- `manageCloudRun` for deployment
- Set MinNum >= 1

### Step 2: Frontend Deployment (if applicable)

- Update API endpoints with deployed backend addresses
- Build frontend application
- Deploy via `manageApps(action="deployApp")` (preferred) or `manageHosting(action="upload")` (fallback)

### Step 3: Display URLs

- Backend URL (if applicable)
- Frontend URL with trailing `/` + random query string (CDN cache bust)

### Step 4: Update Documentation

- Write deployment info + service details to `README.md`
- Include API endpoints, access URLs, CloudBase resources used

---

## Rule File Reference

### Platform Skills
| Skill | Description |
|-------|-------------|
| `{web-development}` | SDK integration, static hosting, build config |
| `{miniprogram-development}` | Project structure, WeChat DevTools, wx.cloud |
| `{cloud-functions}` | Dev, deploy, logging, HTTP access |
| `{cloudrun-development}` | Backend deployment (functions/containers) |
| `{cloudbase-platform}` | Environment, services console |

### Authentication Skills
| Skill | Description |
|-------|-------------|
| `{auth-web}` | **MUST use** Web SDK built-in authentication |
| `{auth-wechat}` | Naturally login-free, OPENID in cloud functions |
| `{auth-nodejs}` | Server-side identity, user lookup |
| `{auth-tool}` | Configure/manage auth providers via MCP tools |

### Database Skills
| Skill | Description |
|-------|-------------|
| `{no-sql-web-sdk}` | NoSQL for Web apps |
| `{no-sql-wx-mp-sdk}` | NoSQL for Mini Programs |
| `{relational-database-web}` | MySQL for Web apps |
| `{relational-database-tool}` | MySQL management via tools |

### Storage / AI / Workflow Skills
| Skill | Description |
|-------|-------------|
| `{cloud-storage-web}` | Upload, download, temp URLs, file mgmt |
| `{ai-model-web}` | AI in browser (@cloudbase/js-sdk), text + streaming |
| `{ai-model-nodejs}` | AI in backend (>=3.16.0), text + streaming + image |
| `{ai-model-wechat}` | AI in Mini Program (wx.cloud.extend.AI), callbacks |
| `{spec-workflow}` | Requirements → design → tasks workflow |

### 🎨 UI Design Skill (CRITICAL — Read FIRST for ANY UI work)

**`rules/ui-design/rule.md`** — MANDATORY, HIGHEST PRIORITY, NO EXCEPTIONS

---

## Quality Checklist

### Before Starting Any Task

- [ ] **Environment checked** via `envQuery`
- [ ] **Scenario identified** and confirmed with user
- [ ] **Existing implementation inspected** (don't recreate what exists)
- [ ] **UI Design doc read** (`rules/ui-design/rule.md`) if task involves UI
- [ ] **Design spec outputted** before writing any UI code
- [ ] **Auth configured** via `{auth-tool}` if auth is involved
- [ ] **Correct DB/auth method selected** for target platform

### Common Pitfalls to Avoid

- ❌ Skipping UI design document read before generating UI
- ❌ Mixing APIs/auth methods across platforms
- ❌ Using `any` to bypass TypeScript errors
- ❌ Empty try/catch to silence bugs
- ❌ Putting model id into `createModel()` instead of `model` field
- ❌ Ignoring Native App limitations (SDK unsupported, MySQL only)
- ❌ Switching deploy methods on existing projects (URLs break)

---

## Console Entry Points

All console URLs follow: `https://tcb.cloud.tencent.com/dev?envId=${envId}#{path}`

| Resource | Path |
|----------|------|
| Overview | `#/overview` |
| Template Center | `#/cloud-template/market` |
| Document Database (NoSQL) | `#/db/doc` · Collections: `#/db/doc/collection/${name}` · Models: `#/db/doc/model/${name}` |
| MySQL Database | `#/db/mysql` · Tables: `#/db/mysql/table/default/` |
| Cloud Functions | `#/scf` · Detail: `#/scf/detail?id=${func}&NameSpace=${envId}` |
| CloudRun | `#/platform-run` |
| Cloud Storage | `#/storage` |
| AI+ | `#/ai` |
| Static Hosting | `#/static-hosting` |
| Identity Auth | `#/identity` · Login: `#/identity/login-manage` · Tokens: `#/identity/token-management` |
| Low-Code (Weida) | `#/lowcode/apps` |
| Logs & Monitoring | `#/devops/log` |
| Extensions | `#/apis` |
| Environment Settings | `#/env` |
