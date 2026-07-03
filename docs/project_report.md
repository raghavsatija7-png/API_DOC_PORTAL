# AI-Powered API Documentation and Testing Portal

> **Team:** Agentic Mandi Testers
> **Course Project — AI/ML Engineering**

---

## Table of Contents

1. [Project Title](#1-project-title)
2. [Problem Statement](#2-problem-statement)
3. [Dataset / Reference Source](#3-dataset--reference-source)
4. [Tools Used](#4-tools-used)
5. [Project Workflow](#5-project-workflow)
6. [AI / ML / Agent / Software Component](#6-ai--ml--agent--software-component)
7. [How to Run the Project](#7-how-to-run-the-project)
8. [Demo Screenshots](#8-demo-screenshots)
9. [Results and Insights](#9-results-and-insights)
10. [Limitations](#10-limitations)
11. [Future Improvements](#11-future-improvements)
12. [Team Members](#12-team-members)

---

## 1. Project Title

### 🧩 AI-Powered API Documentation and Testing Portal

A full-stack developer tool that ingests raw API route definitions — uploaded as OpenAPI/Swagger files, FastAPI/Flask source code, or plain text — and automatically generates professional-grade documentation, realistic sample requests and responses, edge-case test cases, and plain-English error explanations. Every piece of output is persisted in a PostgreSQL database with pgvector support for semantic search.

---

## 2. Problem Statement

> *Build a working solution for an AI-Powered API Documentation and Testing Portal that takes relevant input data, processes it through a clear workflow, and produces an actionable output for real users or decision-makers. The solution should not stop at code execution — it should help a user understand what action to take next.*

### The Real-World Pain

Modern software teams ship APIs at a pace that documentation and testing cannot keep up with. Three pain points stand out:

| # | Pain Point | Impact |
|---|---|---|
| 1 | **Docs go stale or never get written** | Teams skip developer documentation under deadline pressure. New endpoints ship undocumented, leaving consumers to reverse-engineer behaviour from source code or trial and error. |
| 2 | **Edge-case tests are repetitive to write** | Manually enumerating the same five test variants — happy path, missing auth, invalid payload, not-found ID, duplicate — for every one of hundreds of routes is tedious and error-prone. |
| 3 | **Raw error responses tell developers nothing actionable** | A bare `422 Unprocessable Entity` or `409 Conflict` with no context doesn't tell a junior developer *what to fix*. Support tickets and Slack threads multiply. |

### What This Portal Solves

- Turns a sparse route schema into **Swagger/Postman/Stripe-quality documentation** in one click.
- Generates **4–6 runnable pytest snippets** per endpoint covering all common edge cases.
- On any failed live call, returns a **plain-English explanation + concrete fix** so developers know exactly what to change next.

**Real-world impact:** faster onboarding for new developers, fewer support tickets caused by unclear errors, and a CI-ready test suite generated in minutes instead of days.

---

## 3. Dataset / Reference Source

### Starter Dataset — `data/endpoints.json`

Since this project does not require a public dataset, a realistic starter dataset was generated programmatically using `data/generate_dataset.py`.

| Property | Value |
|---|---|
| **Total endpoint records** | 100 |
| **Resources covered** | 20 |
| **CRUD operations per resource** | 5 (GET list, POST, GET by ID, PUT, DELETE) |
| **Schema format** | JSON — matches the project's normalised endpoint schema |

#### Schema per record

```json
{
  "method":        "POST",
  "path":          "/api/v1/users",
  "description":   "Create a new user account.",
  "request_body":  { "name": "string (required)", "email": "string (required)" },
  "response_body": { "id": "string (uuid)", "name": "string", "status": "string" },
  "auth_required": true,
  "error_codes":   [400, 401, 409, 422, 500]
}
```

#### Resources included

`users` · `products` · `orders` · `payments` · `invoices` · `categories` · `reviews` · `carts` · `addresses` · `notifications` · `auth` · `wishlists` · `coupons` · `shipments` · `suppliers` · `warehouses` · `tickets` · `messages` · `subscriptions` · `reports`

#### Shared error-code reference table

A global `error_code_reference` block accompanies the dataset mapping every HTTP error code (400 → 500) to a plain-English meaning, consumed by the AI error-explanation module.

#### Additional input formats supported (beyond the starter data)

| Format | Example files |
|---|---|
| OpenAPI 3.x JSON | `swagger.json`, `openapi.json` |
| OpenAPI 3.x YAML | `openapi.yaml` |
| FastAPI source | `apis.py` (decorator-based route extraction) |
| Flask source | `app.py` |
| Freeform text | `GET /api/v1/users - list users` (one line per endpoint) |

---

## 4. Tools Used

### Frontend
| Tool | Version | Purpose |
|---|---|---|
| **Streamlit** | 1.38+ | Interactive web UI — tabs, forms, JSON viewers, code blocks |

### Backend
| Tool | Version | Purpose |
|---|---|---|
| **FastAPI** | 0.115+ | REST API backend with async request handling |
| **Uvicorn** | 0.30+ | ASGI server for FastAPI |
| **httpx** | 0.27+ | Async HTTP client for the "Try it live" feature |
| **Python-multipart** | 0.0.9+ | File upload parsing |

### Database
| Tool | Version | Purpose |
|---|---|---|
| **PostgreSQL 16** | 16.x | Primary relational database — persists all 10 tables |
| **pgvector 0.6** | 0.6+ | Vector extension — stores 1536-dim embeddings for RAG search |
| **SQLAlchemy** | 2.0+ | Async ORM — models, relationships, queries |
| **Alembic** | Latest | Database migrations — schema version control |
| **asyncpg** | Latest | Async PostgreSQL driver |
| **psycopg2-binary** | Latest | Sync driver used by Alembic for migration generation |

### AI / LLM
| Tool | Purpose |
|---|---|
| **OpenAI SDK** | Chat completions client — compatible with OpenAI, Azure, NVIDIA NIM |
| **NVIDIA NIM** | Drop-in alternative LLM backend (same `/v1/chat/completions` contract) |
| **Custom template engine** | Zero-dependency fallback — produces AI-quality output with no API key |

### Parsing
| Tool | Purpose |
|---|---|
| **PyYAML** | YAML/YAML OpenAPI parsing |
| **Python `re` module** | FastAPI/Flask decorator extraction, path-param resolution |
| **Python `json` module** | JSON schema parsing and sample payload generation |

### DevOps / Packaging
| Tool | Purpose |
|---|---|
| **pip** | Python dependency management |
| **`requirements.txt`** | Reproducible dependency pinning |

---

## 5. Project Workflow

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         USER (Developer / QA)                            │
└──────────────┬───────────────────────────────────────────────────────────┘
               │  uploads file / pastes text / loads starter dataset
               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    STREAMLIT FRONTEND  (frontend/app.py)                  │
│  • Project management sidebar  (create / load by ID)                     │
│  • Three input tabs: Upload file │ Paste text │ Starter dataset           │
│  • Endpoint explorer dropdown   (choose from loaded routes)               │
│  • Action tabs: AI Docs │ AI Tests │ Try it live │ Explain error │ History│
└──────────────┬───────────────────────────────────────────────────────────┘
               │  HTTP requests to FastAPI
               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND  (backend/main.py)                    │
│  POST /upload          POST /parse-text        POST /load-sample         │
│  POST /generate-docs   POST /generate-tests    POST /try-it              │
│  POST /explain-error   GET  /endpoints/{id}/docs                         │
└──────┬───────────────────────────┬────────────────────────────┬──────────┘
       │                           │                            │
       ▼                           ▼                            ▼
┌─────────────┐        ┌───────────────────┐        ┌──────────────────────┐
│   PARSER    │        │    AI ENGINE      │        │   POSTGRESQL DB      │
│ parser.py   │        │  ai_engine.py     │        │ (10 tables)          │
│             │        │                   │        │                      │
│ • OpenAPI   │──────▶│ generate_         │──────▶│ • users              │
│ • YAML      │  norm. │ documentation()   │ store  │ • projects           │
│ • .py src   │  schema│                   │        │ • uploaded_files     │
│ • freeform  │        │ generate_         │        │ • endpoints          │
│   text      │        │ test_cases()      │        │ • endpoint_params    │
└─────────────┘        │                   │        │ • endpoint_examples  │
                       │ explain_error()   │        │ • ai_documentation   │
                       └───────────────────┘        │ • ai_test_cases      │
                                                    │ • api_test_runs      │
                                                    │ • endpoint_embeddings│
                                                    └──────────────────────┘
```

### Step-by-step flow

```
Step 1  ─  User creates a Project (stored in DB)
Step 2  ─  User uploads file / pastes text / loads starter dataset
Step 3  ─  Parser normalises input → list of endpoint dicts
Step 4  ─  FastAPI bulk-upserts endpoints + parameters into PostgreSQL
Step 5  ─  User picks an endpoint from the dropdown
Step 6  ─  Click "Generate documentation" → AI Engine → stored in ai_documentation table
Step 7  ─  Click "Generate test cases"   → AI Engine → stored in ai_test_cases table
Step 8  ─  Click "Try it live"           → httpx fires real HTTP call → stored in api_test_runs
Step 9  ─  If call fails → AI Engine explains error → explanation stored in run record
Step 10 ─  User reads History tab to review all past test runs for an endpoint
```

### Two parallel paths

**Documentation / Generation path**
```
Input schema → Parser → Normalised endpoint → AI Engine → Rich docs + tests → DB → Streamlit display
```

**Live Testing path**
```
User enters base URL → httpx call → Response captured → (on failure) AI explains → Run logged in DB
```

---

## 6. AI / ML / Agent / Software Component

The AI layer is implemented in `backend/ai_engine.py` and consists of **three distinct AI-driven functions**, each justified below.

### Where AI is used

#### 6.1 — `generate_documentation(endpoint)`
**What it does:** Converts a sparse route schema (`method`, `path`, `request_body`, `response_body`, `error_codes`) into Stripe-quality developer documentation including:

- Plain-English summary and detailed description
- Parameter explanations (why each field exists, accepted values, constraints)
- **Rich sample request:** method, full URL, path-param resolution, headers, body, cURL command — method-aware so GET/DELETE never carry a body
- **Rich success response:** `{ status, headers, body }` envelope
- **Error response examples:** realistic `401`, `404`, `409`, `422`, `500` bodies with explanations
- Usage notes: auth requirements, rate limits, idempotency, pagination behaviour

**Why AI is useful here:** Hand-writing docs for every route is the #1 thing engineering teams skip under deadline pressure. The AI reads the *shape* of a schema and reasons about *why* a field exists, not just its type — turning `"email": "string (required)"` into *"The user's email address. Must be a valid email format. Used for login and notification delivery."*

#### 6.2 — `generate_test_cases(endpoint)`
**What it does:** Produces 4–6 concrete test cases per endpoint including:

- **happy_path_success** — valid request, expects 200/201
- **missing_auth_rejected** — no Authorization header, expects 401
- **validation_error_on_missing_required_field** — empty body, expects 422
- **not_found_for_invalid_id** — non-existent ID in path, expects 404
- **double_delete_conflict_or_idempotent** — repeat DELETE, expects 404

Each test case includes: a name, description, the full request object, expected status, expected response shape, and a **runnable pytest snippet** ready to copy into a test suite.

**Why AI is useful here:** Enumerating edge cases by hand for every route is repetitive. The AI reasons over the schema to *infer* which edge cases are implied — for example, a required `email` field implies a malformed-email test case that a template engine alone would not generate.

#### 6.3 — `explain_error(endpoint, status_code, response_payload)`
**What it does:** Given a real failed HTTP response captured by the "Try it live" tester, returns:

- `likely_cause` — concise root-cause label
- `plain_english_explanation` — what went wrong in developer-friendly language
- `suggested_fix` — concrete next action the caller should take
- `severity` — `low` / `medium` / `high`

**Why AI is useful here:** This is the *"actionable output"* requirement from the brief. A raw `422 Unprocessable Entity` tells a developer nothing. The AI reads the endpoint definition *and* the actual failed response body together to explain what the server rejected and precisely what to change in the next request.

### AI provider compatibility

```
AI_API_KEY   set  →  Live LLM call (OpenAI, Azure OpenAI, or NVIDIA NIM)
AI_API_KEY   unset →  Deterministic template engine (zero dependencies, full feature parity)
```

This design means:
1. The portal runs **fully offline** with no API key — important for demos where internet access is unreliable.
2. Swapping from OpenAI to NVIDIA NIM requires changing **two environment variables** (`AI_BASE_URL`, `AI_MODEL`) and nothing else.
3. AI adds *reasoning on top of a working system* — not a dependency it can't function without.

### Database layer (Software Innovation)

10 fully normalised PostgreSQL tables with async SQLAlchemy ORM:

| Table | Key innovation |
|---|---|
| `endpoint_parameters` | Normalised params (1 row per param) instead of JSON blobs |
| `ai_documentation` | Version tracking — incremented on each regeneration |
| `api_test_runs` | Full audit log: request, response, latency, AI explanation |
| `endpoint_embeddings` | **pgvector** `VECTOR(1536)` column with IVFFlat index for RAG cosine similarity search |

---

## 7. How to Run the Project

### Prerequisites

- Python 3.10+
- PostgreSQL 16 with pgvector extension
- pip

### Step 1 — Clone and install dependencies

```bash
git clone https://github.com/your-org/api-doc-portal.git
cd api-doc-portal
pip install -r requirements.txt
```

### Step 2 — Set up PostgreSQL

```bash
# Start PostgreSQL and create the database
psql -U postgres -c "CREATE USER apidoc WITH PASSWORD 'apidoc123';"
psql -U postgres -c "CREATE DATABASE apidoc_portal OWNER apidoc;"
psql -U postgres -d apidoc_portal -c "CREATE EXTENSION IF NOT EXISTS vector;"
psql -U postgres -d apidoc_portal -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"

# Run migrations (creates all 10 tables)
cd backend
alembic upgrade head
cd ..
```

### Step 3 — Configure environment variables

```bash
# Database (defaults shown — change for production)
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=apidoc_portal
export DB_USER=apidoc
export DB_PASSWORD=apidoc123

# AI provider — leave unset to use the built-in template engine
# Option A: OpenAI
export AI_API_KEY="sk-..."
export AI_BASE_URL="https://api.openai.com/v1"
export AI_MODEL="gpt-4o-mini"

# Option B: NVIDIA NIM
export AI_API_KEY="nvapi-..."
export AI_BASE_URL="https://integrate.api.nvidia.com/v1"
export AI_MODEL="meta/llama-3.1-70b-instruct"

# Frontend → backend URL (default is localhost:8000)
export BACKEND_URL="http://localhost:8000"
```

### Step 4 — Generate the starter dataset

```bash
cd data
python generate_dataset.py   # creates endpoints.json (100 endpoints)
cd ..
```

### Step 5 — Start the backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 6 — Start the Streamlit frontend (new terminal)

```bash
cd frontend
streamlit run app.py
```

Open the URL printed in the terminal (usually **http://localhost:8501**).

### Step 7 — Quick demo walkthrough

```
1.  In the sidebar → enter a project name → click "Create project"
2.  On the main page → "Use starter dataset" tab → click "Load starter dataset"
3.  Choose any endpoint from the dropdown (e.g. POST /api/v1/users)
4.  AI Documentation tab → click "Generate & save documentation"
5.  AI Test Cases tab → click "Generate & save test cases"
6.  Try it live tab → enter a base URL → click "Send request & record"
7.  Explain an error tab → paste any status code + response body
8.  History tab → view all past test runs for this endpoint
```

### Sample uploads directory

The `sample_uploads/` folder contains a ready-to-use FastAPI source file:

```bash
# Upload this via the "Upload file" tab to demo the Python route parser
sample_uploads/sample_fastapi_routes.py
```

### API documentation (auto-generated by FastAPI)

```
http://localhost:8000/docs      ← Swagger UI
http://localhost:8000/redoc     ← ReDoc
```

---

## 8. Demo Screenshots

### Screen 1 — Home: Load API Definitions

The portal opens with three input methods. The "Use starter dataset" tab allows an instant demo with 100 pre-built endpoints — no file upload required.

![Home screen — load API definitions](demo_home.png)

---

### Screen 2 — Endpoint Explorer Dropdown

After loading the 100-endpoint starter dataset, the dropdown lists every route grouped by resource. The user can browse all 5 CRUD operations across all 20 resources.

![Endpoint explorer dropdown showing all loaded routes](demo_endpoints.png)

---

### Screen 3 — Raw Definition and At-a-Glance Panel

Selecting an endpoint immediately shows two panels side-by-side:
- **Left:** the raw normalised JSON definition as stored in PostgreSQL
- **Right:** a quick-read summary (method, path, auth requirement, known error codes, normalised parameters pulled from the `endpoint_parameters` table)

![Raw definition and at-a-glance panel](demo_raw_definition.png)

---

### Screen 4 — AI Documentation Output

The AI Documentation tab generates and displays:
- A concise summary and detailed description
- Plain-English parameter explanations
- A rich sample request (method, URL, headers, body)
- A sample response with status envelope
- Usage notes and gotchas

![AI-generated documentation with sample request and response](demo_ai_docs.png)

---

## 9. Results and Insights

### Quantitative results

| Metric | Value |
|---|---|
| Endpoints in starter dataset | 100 |
| Resources covered | 20 |
| CRUD operations per resource | 5 |
| Test cases generated per endpoint | 4–6 |
| Database tables | 10 |
| Supported input formats | 5 (OpenAPI JSON, OpenAPI YAML, FastAPI .py, Flask .py, freeform text) |
| API keys required to demo | 0 (template engine covers all features) |
| Average doc generation time (template) | < 50 ms |
| Average doc generation time (LLM) | 800–2 000 ms |

### Qualitative insights

**1. Method-aware request generation makes a real difference.**
The biggest pre-fix pain point was DELETE endpoints showing an `ERROR` object as their sample request. After implementing `_NO_BODY_METHODS = {"GET", "DELETE", "HEAD", "OPTIONS"}`, GET and DELETE consistently show no body, no Content-Type header, and a correct cURL command — matching Postman and Swagger behaviour exactly.

**2. Deterministic > probabilistic for structured data.**
The LLM path produces better *prose* (summary, description, parameter explanations) but the template engine produces more *reliable* structured data (sample bodies, cURL, error examples). The current architecture uses the LLM only for text fields and always generates request/response/error structures deterministically.

**3. pgvector unlocks a future RAG workflow.**
The `endpoint_embeddings` table with its IVFFlat cosine-distance index makes it possible to ask "which endpoint deletes a payment?" and get a ranked result set — without keyword search. This is the foundation for a future natural-language query interface over the entire API catalog.

**4. Persistent storage changes the use case.**
Moving from in-memory sessions (v1) to PostgreSQL means documentation and test-run history survive backend restarts. A team can now share a project ID and all members see the same generated docs, test history, and error explanations — turning a single-user tool into a lightweight team knowledge base.

**5. The parser covers the real-world 80 % case.**
OpenAPI JSON/YAML, FastAPI decorator extraction, and freeform text together cover the vast majority of how developers describe their APIs. The FastAPI parser correctly detects `auth_required` from `Depends(require_auth)` patterns and infers path parameters from `{param}` tokens.

---

## 10. Limitations

### Technical limitations

| Limitation | Detail |
|---|---|
| **In-memory sessions (legacy path)** | The original in-memory `_SESSIONS` dict was replaced by PostgreSQL, but the old `frontend/app.py` session-ID flow still exists in the codebase alongside the new project-ID flow. Both must be cleaned up for production. |
| **Heuristic Python parser** | Regex-based FastAPI/Flask route extraction does not handle dynamic route registration, class-based views, APIRouter with prefix chaining, or decorators spread across multiple lines. |
| **AI can be wrong** | LLM-generated summaries, parameter explanations, and usage notes are a strong first draft — not a substitute for human review before shipping to end users or external consumers. |
| **Single LLM provider at a time** | The current engine reads one `AI_BASE_URL` / `AI_MODEL` pair. There is no automatic fallback from OpenAI → NVIDIA NIM → template if the primary LLM call fails. |
| **No real-time embedding pipeline** | `endpoint_embeddings` rows must be populated manually. There is no automatic trigger to embed an endpoint after it is created or updated. |
| **PostgreSQL required** | The database layer has no SQLite fallback, so new contributors need a local PostgreSQL 16 installation (with pgvector) to run the project at all. |

### Responsible use

| Practice | Implementation |
|---|---|
| **No secrets are stored** | Auth tokens entered in "Try it live" are used only for that single `httpx` call and never persisted in the database. |
| **Live calls are user-initiated only** | The portal never contacts a real API unless the user explicitly enters a base URL and clicks "Send request". |
| **Generated output requires review** | Documentation and test cases are marked as `_generated_by: template-fallback` or `_generated_by: ai/<model>` so consumers always know the provenance. |
| **Always review before production** | Generated pytest snippets are stubs that require a running test client (`from tests.conftest import client`) — they will not run as-is, preventing accidental CI breakage. |

---

## 11. Future Improvements

### Near-term (next sprint)

| # | Improvement | Rationale |
|---|---|---|
| 1 | **Persistent storage for rich doc fields** | Currently `rich_sample_request`, `rich_sample_response`, and `error_examples` are not stored in the DB — they are recomputed on every load. Adding a `full_doc_jsonb` column to `ai_documentation` would make "Load stored documentation" fully instant. |
| 2 | **Auto-run generated tests** | Execute the generated pytest suite directly against a staging API (using `httpx.Client`) and show pass/fail badges inline in the Streamlit UI. |
| 3 | **Multiple AI provider fallback chain** | On LLM call failure, automatically retry with the next configured provider: OpenAI → NVIDIA NIM → Groq → template engine. |
| 4 | **Embedding pipeline** | Auto-embed each endpoint after creation/update using a background `asyncio.Task`, making the RAG semantic search immediately usable without manual steps. |

### Medium-term (next quarter)

| # | Improvement | Rationale |
|---|---|---|
| 5 | **Multi-user collaboration** | Add real JWT authentication (replace demo `user_id: "demo-user"`), shared project workspaces, and per-endpoint comment threads. |
| 6 | **CI/CD integration** | Export generated tests directly into a GitHub Actions YAML file. On every PR, automatically re-run tests and post a documentation-drift report. |
| 7 | **OpenAPI export** | Generate a valid `openapi.yaml` from the stored endpoints, examples, and AI descriptions — turning the portal into a round-trip documentation editor. |
| 8 | **Versioned doc history** | Track how an endpoint's documentation changed release over release using the existing `version` column in `ai_documentation`, with a diff view in the UI. |

### Long-term (roadmap)

| # | Improvement | Rationale |
|---|---|---|
| 9 | **Natural-language endpoint search** | "Which endpoint cancels a subscription?" → embed query → pgvector cosine search → return top-k endpoints with docs. |
| 10 | **Agentic regression watch** | A background agent periodically re-runs all stored test cases against the live API and Slack/emails the team on breaking changes — no human trigger needed. |
| 11 | **SDK generation** | From the stored endpoint schema + examples, auto-generate a Python/JavaScript client SDK with typed methods and docstrings. |
| 12 | **SQLite dev mode** | Add a `DB_BACKEND=sqlite` mode using `aiosqlite` so contributors can run the project without installing PostgreSQL. |

---

## 12. Team Members

**Team Name: Agentic Mandi Testers**

| Name | Roll Number | Contribution |
|---|---|---|
| **Raghav Satija** | 311 | Backend architecture (FastAPI, PostgreSQL schema, Alembic migrations, CRUD layer), AI engine design, project coordination |
| **Jnanesha V** | 383 | Frontend development (Streamlit UI, rich documentation display, test case viewer, history tab), integration testing |
| **Thanush M** | 315 | Parser module (OpenAPI/YAML/Python source extraction, freeform text parsing), starter dataset generation, documentation |

---

## Appendix — Project File Structure

```
api-doc-portal/
├── backend/
│   ├── main.py                  # FastAPI app — all API routes
│   ├── ai_engine.py             # AI layer — docs, tests, error explanations
│   ├── parser.py                # Multi-format route extractor
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py            # SQLAlchemy ORM — all 10 tables
│   │   ├── connection.py        # Async engine + session factory + get_db
│   │   └── crud.py              # Async CRUD for all tables
│   └── alembic/
│       ├── env.py               # Alembic migration environment
│       └── versions/
│           └── *_initial_schema.py
├── frontend/
│   └── app.py                   # Streamlit UI
├── data/
│   ├── generate_dataset.py      # Script to generate endpoints.json
│   └── endpoints.json           # 100-endpoint starter dataset
├── sample_uploads/
│   └── sample_fastapi_routes.py # Demo FastAPI file for parser testing
├── requirements.txt
└── project_report.md            # This document
```

---

*Report generated for the AI/ML Engineering course project submission.*
*All code, dataset, and documentation produced by Team Agentic Mandi Testers.*
