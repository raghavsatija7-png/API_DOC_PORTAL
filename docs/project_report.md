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

A full-stack developer tool that ingests raw API route definitions — uploaded as OpenAPI/Swagger files, FastAPI/Flask source code, or plain text — and automatically generates professional-grade documentation, realistic sample requests and responses, edge-case test cases, and plain-English error explanations. All output is driven by the **Groq API** using the `llama-3.1-8b-instant` model via an OpenAI-compatible SDK interface.

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

- Turns a sparse route schema into **Swagger / Postman / Stripe-quality documentation** in one click.
- Generates **4–6 runnable pytest snippets** per endpoint covering all common edge cases.
- On any failed live call, returns a **plain-English explanation + concrete suggested fix** so developers know exactly what to change next.

**Real-world impact:** faster onboarding for new developers, fewer support tickets caused by unclear errors, and a CI-ready test suite generated in minutes instead of days.

---

## 3. Dataset / Reference Source

### Starter Dataset — `data/endpoints.json`

Since this project does not require a public dataset, a realistic starter dataset was generated programmatically using `data/generate_dataset.py`. The file is loaded directly into the portal at runtime — no database is used.

| Property | Value |
|---|---|
| **Total endpoint records** | 100 |
| **Resources covered** | 20 |
| **CRUD operations per resource** | 5 (GET list, POST, GET by ID, PUT, DELETE) |
| **Schema format** | JSON — matches the project's normalised endpoint schema |
| **Storage** | Flat file (`data/endpoints.json`) — loaded into memory at runtime |

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
| **requests** | 2.32+ | HTTP calls from Streamlit to the FastAPI backend |

### AI / LLM
| Tool | Detail |
|---|---|
| **OpenAI SDK** | Used as the API client library (`openai` Python package) |
| **Groq API** | Provides the actual API key and inference endpoint — free tier, no credit card required |
| **Model** | `llama-3.1-8b-instant` (Meta Llama 3.1 8B, served by Groq) |
| **Compatibility** | Groq exposes an OpenAI-compatible `/v1/chat/completions` endpoint — the OpenAI SDK works with zero code changes, only `base_url` and `api_key` differ |
| **Fallback** | Built-in deterministic template engine — full feature parity with no API key |

### Parsing
| Tool | Purpose |
|---|---|
| **PyYAML** | OpenAPI YAML parsing |
| **Python `re` module** | FastAPI/Flask decorator extraction, path-param resolution |
| **Python `json` module** | JSON schema parsing and sample payload generation |

### DevOps / Packaging
| Tool | Purpose |
|---|---|
| **venv** | Python virtual environment isolation |
| **pip** | Dependency management |
| **`requirements.txt`** | Reproducible dependency pinning |

---

## 5. Project Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER (Developer / QA)                            │
└─────────────────┬───────────────────────────────────────────────────────┘
                  │  uploads file / pastes text / loads starter dataset
                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│             STREAMLIT FRONTEND  (frontend/app_improved.py)              │
│  • Three input tabs: Upload file | Paste text | Use starter dataset     │
│  • Endpoint explorer dropdown (choose from all loaded routes)           │
│  • Action tabs: AI Docs | AI Tests | Try it live | Explain an error     │
└─────────────────┬───────────────────────────────────────────────────────┘
                  │  HTTP requests to FastAPI  (localhost:8000)
                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                  FASTAPI BACKEND  (backend/main.py)                     │
│  POST /upload         POST /parse-text       POST /load-sample          │
│  POST /generate-docs  POST /generate-tests   POST /try-it               │
│  POST /explain-error                                                     │
└──────────┬──────────────────────────┬──────────────────────────┬────────┘
           │                          │                          │
           ▼                          ▼                          ▼
  ┌─────────────────┐   ┌────────────────────────┐   ┌──────────────────┐
  │  PARSER         │   │  AI ENGINE             │   │  DATA STORE      │
  │  parser.py      │   │  UPDATED2_ai_engine.py │   │                  │
  │                 │   │                        │   │  endpoints.json  │
  │  • OpenAPI JSON │──▶│  generate_             │   │  (100 records,   │
  │  • OpenAPI YAML │   │  documentation()       │   │  in-memory       │
  │  • FastAPI .py  │   │                        │   │  session store)  │
  │  • Flask .py    │   │  generate_             │   │                  │
  │  • Freeform txt │   │  test_cases()          │   └──────────────────┘
  └─────────────────┘   │                        │
                        │  explain_error()       │
                        └──────────┬─────────────┘
                                   │  API call
                                   ▼
                        ┌──────────────────────┐
                        │  GROQ API            │
                        │  llama-3.1-8b-instant│
                        │  (OpenAI-compatible  │
                        │   /v1/chat/completions│
                        └──────────────────────┘
```

### Step-by-step flow

```
Step 1  ─  User opens the portal in the browser (Streamlit, port 8501)
Step 2  ─  User uploads a file / pastes text / clicks "Load starter dataset"
Step 3  ─  Parser normalises input → list of endpoint dicts (held in memory)
Step 4  ─  All routes appear in the endpoint dropdown
Step 5  ─  User picks an endpoint; raw JSON definition shown side-by-side
Step 6  ─  "AI Documentation" tab → FastAPI → AI Engine → Groq API
           → rich docs (summary, params, sample request, cURL, error examples)
Step 7  ─  "AI Test Cases" tab → FastAPI → AI Engine → Groq API
           → 4–6 test cases with runnable pytest snippets
Step 8  ─  "Try it live" tab → user enters base URL → FastAPI fires real HTTP call
           → on failure → AI Engine explains error in plain English
Step 9  ─  "Explain an error" tab → paste any status code + body → AI explanation
```

---

## 6. AI / ML / Agent / Software Component

The AI layer lives entirely in `backend/UPDATED2_ai_engine.py` and contains **three AI-driven functions**.

### AI Provider Setup

```
SDK:      openai  (Python package — used as the HTTP client only)
API Key:  Groq free-tier key  →  https://console.groq.com
Endpoint: https://api.groq.com/openai/v1
Model:    llama-3.1-8b-instant
```

Groq exposes the exact same `/v1/chat/completions` contract as OpenAI, so the standard `openai` Python SDK works without any modification — only `base_url` and `api_key` are changed via environment variables.

### Where AI is used

#### 6.1 — `generate_documentation(endpoint)`

**What it does:** Converts a sparse route schema into Stripe-quality developer documentation including:

- Plain-English summary and detailed description
- Parameter explanations (why each field exists, accepted values, constraints)
- **Rich sample request** — method-aware: GET/DELETE get no body; POST/PUT/PATCH get a realistic JSON body; includes full URL with resolved path parameters, headers, and an executable cURL command
- **Rich success response** — `{ status, headers, body }` envelope
- **Error response examples** — realistic `401`, `404`, `409`, `422`, `500` response bodies with plain-English explanations per status code
- Usage notes: auth requirements, rate limits, idempotency, pagination behaviour

**Why AI is useful here:** Hand-writing docs for every route is the first thing teams skip under pressure. The LLM reasons about *why* a field exists — not just its type — producing context-aware explanations that a pure template engine cannot.

#### 6.2 — `generate_test_cases(endpoint)`

**What it does:** Produces 4–6 concrete test cases per endpoint:

| Test Case | Description | Expected Status |
|---|---|---|
| `happy_path_success` | Valid request, correct credentials | 200 / 201 |
| `missing_auth_rejected` | No Authorization header | 401 |
| `validation_error_on_missing_required_field` | Empty request body | 422 |
| `not_found_for_invalid_id` | Non-existent path ID | 404 |
| `double_delete_conflict_or_idempotent` | Repeat DELETE call | 404 |

Each test case includes a name, description, full request object, expected status, expected response shape, and a **runnable pytest snippet** ready to copy into a test suite.

**Why AI is useful here:** The LLM infers which edge cases a schema implies — e.g. a required `email` field implies a malformed-email test case — going beyond what a template engine alone would generate.

#### 6.3 — `explain_error(endpoint, status_code, response_payload)`

**What it does:** Given a real failed HTTP response from the "Try it live" feature, returns:

- `likely_cause` — concise root-cause label
- `plain_english_explanation` — developer-friendly explanation of what went wrong
- `suggested_fix` — the exact next action the caller should take
- `severity` — `low` / `medium` / `high`

**Why AI is useful here:** This is the *"actionable output"* requirement from the brief. A raw `422 Unprocessable Entity` tells nobody anything. The AI reads both the endpoint definition and the actual failed response body together to tell the developer precisely what to fix.

### Deterministic fallback engine

Every AI function has a built-in template fallback that activates when `AI_API_KEY` is not set:

- Portal runs fully offline with zero API key — useful for demos without internet access
- Fallback produces high-quality structured output (rich request/response/error shapes)
- Only prose fields (summaries, parameter explanations) differ from the live LLM path
- Switching from Groq to any other OpenAI-compatible provider requires changing two environment variables and zero lines of Python

---

## 7. How to Run the Project

### Prerequisites

- Python 3.10+
- A free Groq API key — sign up at [console.groq.com](https://console.groq.com) (no credit card required)

### Step 1 — Clone the repository

```bash
git clone https://github.com/raghavsatija7-png/API_DOC_PORTAL.git
cd API_DOC_PORTAL
```

### Step 2 — Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set environment variables

```bash
export AI_API_KEY="your_groq_key"
export AI_BASE_URL="https://api.groq.com/openai/v1"
export AI_MODEL="llama-3.1-8b-instant"
```

> **Note:** Skip this step to run in template-fallback mode — all features still work, prose is generated by the built-in engine instead of the LLM.

### Step 5 — Start the FastAPI backend

```bash
venv/bin/uvicorn backend.main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### Step 6 — Start the Streamlit frontend (new terminal)

```bash
venv/bin/streamlit run frontend/app_improved.py
```

Open the URL printed in the terminal — usually **http://localhost:8501**.

### Step 7 — Quick demo walkthrough

```
1.  "Use starter dataset" tab  →  click "Load starter dataset"
2.  Choose an endpoint from the dropdown  (e.g. POST /api/v1/users)
3.  "AI Documentation" tab     →  click "Generate documentation"
4.  "AI Test Cases" tab        →  click "Generate test cases"
5.  "Try it live" tab          →  enter a base URL, click "Send request"
6.  "Explain an error" tab     →  paste any status code + response body
```

---

## 8. Demo Screenshots

### Screen 1 — Home: Load API Definitions

The portal opens with three input methods. The "Use starter dataset" tab loads 100 pre-built endpoints instantly — no file upload or database setup required.

![Home screen — load API definitions](demo_home.png)

---

### Screen 2 — Endpoint Explorer Dropdown

After loading the starter dataset, the dropdown lists every route across all 20 resources. The user can browse all 5 CRUD operations per resource — users, orders, invoices, payments, and more.

![Endpoint explorer dropdown showing all loaded routes](demo_endpoints.png)

---

### Screen 3 — Raw Definition and At-a-Glance Panel

Selecting an endpoint shows two panels side-by-side:
- **Left:** the raw normalised JSON definition as parsed from `endpoints.json`
- **Right:** a quick-read summary — method, path, auth requirement, known error codes

![Raw definition and at-a-glance panel](demo_raw_definition.png)

---

### Screen 4 — AI Documentation Output

The AI Documentation tab generates a full Swagger/Postman-style reference — including a rich sample request with URL, resolved path parameters, headers, request body, and sample response. Powered by `llama-3.1-8b-instant` via the Groq API.

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
| Supported input formats | 5 (OpenAPI JSON, OpenAPI YAML, FastAPI .py, Flask .py, freeform text) |
| AI model | `llama-3.1-8b-instant` via Groq API |
| Average doc generation time (LLM) | ~800–1 500 ms |
| Average doc generation time (fallback) | < 50 ms |
| API keys required | 1 (free Groq key, no credit card) |

### Qualitative insights

**1. Method-aware request generation fixes a critical UX bug.**
The biggest pre-fix pain point was DELETE endpoints displaying an `ERROR` object as their sample request body. After enforcing `_NO_BODY_METHODS = {"GET", "DELETE"}`, GET and DELETE routes consistently show no body, no Content-Type header, and a correct cURL command — exactly matching Postman and Swagger behaviour.

**2. Groq + `llama-3.1-8b-instant` is fast enough for interactive use.**
Average latency of ~1 second per generation keeps the portal responsive. The free tier handles the demo workload comfortably without hitting rate limits.

**3. OpenAI SDK + Groq = zero code changes.**
Because Groq's endpoint is OpenAI-compatible, the entire AI engine required only two environment variable changes to switch providers — not a single line of Python was modified.

**4. Deterministic + LLM hybrid is more reliable than LLM-only.**
Structured fields (sample bodies, cURL commands, error status codes) are always generated by the deterministic engine — guaranteed to be correct. LLM output is used only for prose fields where variation is acceptable and adds value.

**5. The parser covers the real-world 80% case.**
OpenAPI JSON/YAML, FastAPI decorator extraction, and freeform text together cover the vast majority of how developers describe APIs in practice. The parser correctly infers path parameters from `{param}` tokens and detects auth requirements from `Depends(require_auth)` patterns.

---

## 10. Limitations

### Technical limitations

| Limitation | Detail |
|---|---|
| **In-memory session storage** | Loaded endpoints live in a Python dict keyed by session ID. Restarting the backend clears all data. Intentional for a lightweight demo scope. |
| **No persistent database** | The project uses `endpoints.json` as its data source and in-memory storage. Documentation generated in one session is not available in another. |
| **Heuristic Python parser** | Regex-based FastAPI/Flask route extraction does not handle dynamic route registration, class-based views, APIRouter prefix chaining, or multi-line decorators. |
| **AI can be wrong** | LLM-generated summaries and parameter explanations are a strong first draft — not a substitute for human review before publishing to end users. |
| **Rate limits on Groq free tier** | The free tier allows ~30 requests/minute on `llama-3.1-8b-instant`. Generating docs for all 100 endpoints in rapid succession may hit this limit. |

### Responsible use

| Practice | Implementation |
|---|---|
| **No secrets stored** | Auth tokens entered in "Try it live" are used only for that single HTTP call and never written to disk. |
| **Live calls are user-initiated only** | The portal never contacts a real API unless the user explicitly enters a base URL and clicks "Send request". |
| **Provenance labelling** | All generated output is tagged with `_generated_by: ai/llama-3.1-8b-instant` or `_generated_by: template-fallback` so consumers always know the source. |
| **Review before production** | Generated pytest snippets are illustrative stubs — they are not wired to a live test runner and will not break CI if copied as-is. |

---

## 11. Future Improvements

### Near-term

| # | Improvement | Rationale |
|---|---|---|
| 1 | **Persistent storage** | Add SQLite or PostgreSQL so generated docs and test cases survive backend restarts and can be shared across team members. |
| 2 | **Auto-run generated tests** | Execute the generated pytest suite against a staging API using `httpx.Client` and show live pass/fail badges in the UI. |
| 3 | **AI provider fallback chain** | On Groq failure, automatically retry with the template engine instead of returning an error. |
| 4 | **Batch documentation** | Generate docs for all loaded endpoints in one click with a progress bar. |

### Medium-term

| # | Improvement | Rationale |
|---|---|---|
| 5 | **OpenAPI export** | Generate a valid `openapi.yaml` from the parsed endpoints and AI descriptions — turning the portal into a round-trip documentation editor. |
| 6 | **CI/CD integration** | Export the generated test suite directly into a GitHub Actions workflow YAML. |
| 7 | **Multi-user collaboration** | Add user accounts so teams can share projects and view each other's generated documentation. |
| 8 | **Versioned doc history** | Track how an endpoint's documentation changes over time with a diff view. |

### Long-term

| # | Improvement | Rationale |
|---|---|---|
| 9 | **Natural-language endpoint search** | "Which endpoint cancels a subscription?" → semantic search → matching endpoint with docs. |
| 10 | **Agentic regression watch** | A background agent periodically re-tests live endpoints and alerts the team on breaking changes. |
| 11 | **SDK generation** | Auto-generate a typed Python/JavaScript client SDK from stored endpoint schema and examples. |
| 12 | **More input formats** | Postman Collection v2, HAR files, gRPC proto files. |

---

## 12. Team Members

**Team Name: Agentic Mandi Testers**

| Name | Roll Number |
|---|---|
| **Raghav Satija** | 311 |
| **Jnanesha V** | 383 |
| **Thanush M** | 315 |

---

## Appendix — Project File Structure

```
API_DOC_PORTAL/
├── backend/
│   ├── main.py                      # FastAPI app — all API routes
│   ├── parser.py                    # Multi-format route extractor
│   └── UPDATED2_ai_engine.py        # AI layer — docs, tests, error explanations
├── data/
│   ├── endpoints.json               # 100-endpoint starter dataset
│   └── generate_dataset.py          # Script that generated endpoints.json
├── docs/
│   ├── presentation.pdf             # Project presentation slides
│   └── project_report.md            # This document
├── frontend/
│   └── app_improved.py              # Streamlit UI
├── sample_uploads/
│   └── sample_fastapi_routes.py     # Demo FastAPI file for parser testing
├── venv/                            # Python virtual environment (not committed)
├── README.md
└── requirements.txt
```

---