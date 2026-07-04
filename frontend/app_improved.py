"""
app_improved.py — Streamlit frontend for the AI-Powered API Documentation & Testing Portal.

Run alongside the FastAPI backend:
    uvicorn backend.main:app --reload --port 8000
    streamlit run frontend/app_improved.py
"""
import json
import os
import uuid
from collections import Counter

import requests
import streamlit as st

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
AI_REQUEST_TIMEOUT = int(os.environ.get("AI_REQUEST_TIMEOUT", "60"))

st.set_page_config(
    page_title="AI API Doc & Testing Portal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS — light modern theme with alive animations
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg:        #f4f6fb;
    --surface:   #ffffff;
    --surface2:  #f0f2f8;
    --border:    #d8dde8;
    --text:      #1a1d2e;
    --muted:     #6b7194;
    --accent:    #5046e5;
    --accent2:   #0ea5e9;
    --green:     #16a34a;
    --blue:      #2563eb;
    --amber:     #d97706;
    --purple:    #7c3aed;
    --red:       #dc2626;
    --pink:      #db2777;
    --cyan:      #0891b2;
    --glow:      rgba(80,70,229,0.20);
}

.stApp {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #eef1fa 0%, #e4e8f5 100%);
    border-right: 1px solid var(--border);
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* =========================  ANIMATIONS  ========================= */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 8px var(--glow); }
    50%      { box-shadow: 0 0 22px var(--glow), 0 0 44px rgba(80,70,229,0.08); }
}
@keyframes pulse-dot {
    0%, 100% { transform: scale(1); opacity: 1; }
    50%      { transform: scale(1.6); opacity: 0.5; }
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-4px); }
}
@keyframes scaleIn {
    from { transform: scale(0.92); opacity: 0; }
    to   { transform: scale(1);    opacity: 1; }
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.animate-in      { animation: fadeInUp 0.45s ease-out both; }
.animate-in-slow { animation: fadeInUp 0.65s ease-out both; }
.animate-fade    { animation: fadeIn 0.5s ease-out both; }
.animate-scale   { animation: scaleIn 0.35s ease-out both; }

/* =========================  HERO  ========================= */
.hero {
    background: linear-gradient(135deg, #5046e5 0%, #0ea5e9 50%, #8b5cf6 100%);
    background-size: 300% 300%;
    animation: gradientShift 6s ease infinite;
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 20% 50%, rgba(255,255,255,0.15) 0%, transparent 60%);
}
.hero h1 {
    color: #fff;
    font-size: 1.9rem;
    font-weight: 800;
    margin: 0 0 6px 0;
    position: relative;
    text-shadow: 0 2px 12px rgba(0,0,0,0.2);
}
.hero p {
    color: rgba(255,255,255,0.88);
    font-size: 0.95rem;
    margin: 0;
    position: relative;
}

/* =========================  METHOD BADGES  ========================= */
.method-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #fff;
    text-transform: uppercase;
    transition: all 0.25s ease;
    cursor: default;
}
.method-badge:hover {
    transform: translateY(-1px) scale(1.05);
    filter: brightness(1.12);
}
.method-GET    { background: linear-gradient(135deg, #16a34a, #15803d); box-shadow: 0 2px 8px rgba(22,163,74,0.30); }
.method-POST   { background: linear-gradient(135deg, #2563eb, #1d4ed8); box-shadow: 0 2px 8px rgba(37,99,235,0.30); }
.method-PUT    { background: linear-gradient(135deg, #d97706, #b45309); box-shadow: 0 2px 8px rgba(217,119,6,0.30); }
.method-PATCH  { background: linear-gradient(135deg, #7c3aed, #6d28d9); box-shadow: 0 2px 8px rgba(124,58,237,0.30); }
.method-DELETE { background: linear-gradient(135deg, #dc2626, #b91c1c); box-shadow: 0 2px 8px rgba(220,38,38,0.30); }

.method-badge:hover.method-GET    { box-shadow: 0 4px 18px rgba(22,163,74,0.50); }
.method-badge:hover.method-POST   { box-shadow: 0 4px 18px rgba(37,99,235,0.50); }
.method-badge:hover.method-PUT    { box-shadow: 0 4px 18px rgba(217,119,6,0.50); }
.method-badge:hover.method-PATCH  { box-shadow: 0 4px 18px rgba(124,58,237,0.50); }
.method-badge:hover.method-DELETE { box-shadow: 0 4px 18px rgba(220,38,38,0.50); }

/* =========================  GLOW CARD  ========================= */
.glow-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 10px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.glow-card:hover {
    border-color: var(--accent);
    box-shadow: 0 0 0 1px var(--accent),
                0 8px 32px rgba(80,70,229,0.10),
                0 2px 8px rgba(0,0,0,0.06);
    transform: translateY(-2px);
}

/* =========================  STAT CARD  ========================= */
.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: 0;
    transition: opacity 0.3s;
}
.stat-card:hover {
    border-color: var(--accent);
    box-shadow: 0 0 20px rgba(80,70,229,0.08), 0 8px 24px rgba(0,0,0,0.06);
    transform: translateY(-3px);
}
.stat-card:hover::before { opacity: 1; }
.stat-icon {
    font-size: 1.6rem;
    margin-bottom: 6px;
    display: block;
    animation: float 3s ease-in-out infinite;
}
.stat-value {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label {
    font-size: 0.78rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 2px;
}

/* =========================  BOXES  ========================= */
.info-box {
    background: rgba(37,99,235,0.06);
    border-left: 4px solid var(--blue);
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 10px 0;
    animation: fadeInUp 0.4s ease-out;
}
.warning-box {
    background: rgba(217,119,6,0.06);
    border-left: 4px solid var(--amber);
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 10px 0;
    animation: fadeInUp 0.4s ease-out;
}
.success-box {
    background: rgba(22,163,74,0.06);
    border-left: 4px solid var(--green);
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 10px 0;
    animation: fadeInUp 0.4s ease-out;
}

/* =========================  PULSE DOT  ========================= */
.pulse-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse-dot 2s ease-in-out infinite;
}
.pulse-green { background: var(--green); box-shadow: 0 0 8px rgba(22,163,74,0.5); }
.pulse-amber { background: var(--amber); box-shadow: 0 0 8px rgba(217,119,6,0.5); }
.pulse-red   { background: var(--red);   box-shadow: 0 0 8px rgba(220,38,38,0.5); }

/* =========================  SEVERITY  ========================= */
.severity {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    transition: all 0.25s ease;
}
.severity:hover { transform: scale(1.08); filter: brightness(1.15); }
.severity-low    { background: linear-gradient(135deg, #16a34a, #15803d); box-shadow: 0 2px 8px rgba(22,163,74,0.3); }
.severity-medium { background: linear-gradient(135deg, #d97706, #b45309); box-shadow: 0 2px 8px rgba(217,119,6,0.3); }
.severity-high   { background: linear-gradient(135deg, #dc2626, #b91c1c); box-shadow: 0 2px 8px rgba(220,38,38,0.3); }

/* =========================  STATUS BADGE  ========================= */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 20px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 1.05rem;
    color: #fff;
    transition: all 0.3s ease;
}
.status-badge:hover { transform: scale(1.04); filter: brightness(1.1); }
.status-success {
    background: linear-gradient(135deg, #16a34a, #15803d);
    box-shadow: 0 4px 16px rgba(22,163,74,0.30);
}
.status-error {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    box-shadow: 0 4px 16px rgba(220,38,38,0.30);
}

/* =========================  SECTION HEADER  ========================= */
.section-header {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-header .icon {
    font-size: 1.3rem;
    animation: float 3s ease-in-out infinite;
}

/* =========================  TABS  ========================= */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: var(--surface2);
    border-radius: 10px;
    padding: 4px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    padding: 10px 22px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.88rem;
    color: var(--muted);
    transition: all 0.25s ease;
    border: 1px solid transparent;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text);
    background: var(--surface);
    border-color: var(--border);
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #fff;
    background: linear-gradient(135deg, var(--accent), #4f46e5);
    border-color: var(--accent);
    box-shadow: 0 2px 12px rgba(80,70,229,0.25);
}

/* =========================  BUTTONS  ========================= */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.88rem;
    padding: 8px 24px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid transparent;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(80,70,229,0.25);
}
.stButton > button:active {
    transform: translateY(0) scale(0.97);
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent), #4f46e5) !important;
    border: none !important;
    color: #fff !important;
    animation: pulse-glow 3s ease-in-out infinite;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 28px rgba(80,70,229,0.45), 0 0 60px rgba(80,70,229,0.10) !important;
    animation: none;
}

/* =========================  EXPANDER  ========================= */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    transition: all 0.25s ease !important;
}
.streamlit-expanderHeader:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 4px 16px rgba(80,70,229,0.08) !important;
}

/* =========================  SHIMMER  ========================= */
.shimmer {
    background: linear-gradient(90deg, var(--surface2) 25%, var(--border) 50%, var(--surface2) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.8s ease-in-out infinite;
    border-radius: 8px;
    min-height: 60px;
}

/* =========================  SIDEBAR ICON  ========================= */
.sidebar-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: var(--surface);
    border: 1px solid var(--border);
    font-size: 1.1rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: default;
}
.sidebar-icon:hover {
    background: var(--accent);
    border-color: var(--accent);
    box-shadow: 0 4px 16px rgba(80,70,229,0.35);
    transform: translateY(-2px) scale(1.1);
}

.small-text { font-size: 0.82rem; color: var(--muted); }

.footer-line {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 16px 0;
    font-size: 0.8rem;
    color: var(--muted);
}
.footer-line .dot {
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: var(--border);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "endpoints" not in st.session_state:
    st.session_state.endpoints = []
if "method_filter" not in st.session_state:
    st.session_state.method_filter = "ALL"
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

SID = st.session_state.session_id


# ---------------------------------------------------------------------------
# Helpers — all icons are plain emoji/text characters for reliable rendering
# ---------------------------------------------------------------------------
def post_ai(path, payload):
    try:
        return requests.post(f"{BACKEND_URL}{path}", json=payload, timeout=AI_REQUEST_TIMEOUT), None
    except requests.exceptions.Timeout:
        return None, f"AI request timed out ({AI_REQUEST_TIMEOUT}s)."
    except requests.exceptions.RequestException as exc:
        return None, f"Could not reach backend: {exc}"


METHOD_ICONS = {
    "GET": "🟢",
    "POST": "🔵",
    "PUT": "🟠",
    "PATCH": "🟣",
    "DELETE": "🔴",
}

def method_badge(method: str) -> str:
    m = method.upper()
    icon = METHOD_ICONS.get(m, "⚪")
    return f'<span class="method-badge method-{m}">{icon} {m}</span>'


SEVERITY_ICONS = {"low": "✅", "medium": "⚠️", "high": "❌"}

def severity_badge(sev: str) -> str:
    icon = SEVERITY_ICONS.get(sev, "•")
    return f'<span class="severity severity-{sev}">{icon} {sev.upper()}</span>'


def status_badge(code: int, ok: bool) -> str:
    cls = "status-success" if ok else "status-error"
    icon = "✔" if ok else "✖"
    return f'<span class="status-badge {cls}">{icon} HTTP {code}</span>'


def pulse_dot(color: str = "green") -> str:
    return f'<span class="pulse-dot pulse-{color}"></span>'


def endpoint_matches(ep, query: str, method_filter: str) -> bool:
    if method_filter != "ALL" and ep.get("method", "").upper() != method_filter:
        return False
    if query:
        q = query.lower()
        searchable = f"{ep.get('method', '')} {ep.get('path', '')} {ep.get('description', '')}".lower()
        return q in searchable
    return True


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div style="text-align:center; padding:8px 0 4px 0;">'
        '<span style="font-size:2.2rem; animation: float 3s ease-in-out infinite; display:inline-block;">⚡</span>'
        '<div style="font-size:1.15rem; font-weight:800; margin-top:2px; '
        'background:linear-gradient(135deg,#5046e5,#0ea5e9); '
        '-webkit-background-clip:text; -webkit-text-fill-color:transparent; '
        'background-clip:text;">API Portal</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border:1px solid var(--border); margin:8px 0;'>", unsafe_allow_html=True)

    # Backend status
    try:
        health = requests.get(f"{BACKEND_URL}/health", timeout=3).json()
        ai_on = health.get("ai_enabled")
        ai = health.get("ai") or {}
        if ai_on:
            st.markdown(
                f'<div class="success-box">{pulse_dot("green")} <b>Connected</b> — AI Live<br>'
                f'<span style="font-size:0.78rem; color:var(--muted);">{ai.get("model", "?")}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="warning-box">{pulse_dot("amber")} <b>Connected</b> — Template Fallback<br>'
                f'<span style="font-size:0.78rem; color:var(--muted);">Set AI_API_KEY for live AI</span></div>',
                unsafe_allow_html=True,
            )
    except Exception:
        st.markdown(
            f'<div class="warning-box">{pulse_dot("red")} <b>Offline</b><br>'
            f'<span style="font-size:0.78rem; color:var(--muted);">{BACKEND_URL}</span></div>',
            unsafe_allow_html=True,
        )
        st.stop()

    st.markdown("<hr style='border:1px solid var(--border); margin:8px 0;'>", unsafe_allow_html=True)

    endpoints = st.session_state.endpoints
    if endpoints:
        st.markdown(
            '<div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">'
            '<span class="sidebar-icon">🔍</span>'
            '<span style="font-weight:700; font-size:0.92rem;">Search & Filter</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        search_q = st.text_input("Search", value=st.session_state.search_query, placeholder="e.g. /users, POST", key="sidebar_search", label_visibility="collapsed")
        st.session_state.search_query = search_q

        methods = ["ALL"] + sorted(set(e.get("method", "").upper() for e in endpoints))
        sel_method = st.selectbox("Method", methods, index=methods.index(st.session_state.method_filter) if st.session_state.method_filter in methods else 0, key="sidebar_method", label_visibility="collapsed")
        st.session_state.method_filter = sel_method

        filtered = [e for e in endpoints if endpoint_matches(e, search_q, sel_method)]
        st.markdown(
            f'<div style="text-align:center; padding:6px; border-radius:8px; background:var(--surface); '
            f'border:1px solid var(--border); font-size:0.82rem;">'
            f'{pulse_dot("green")} Showing <b>{len(filtered)}</b> of <b>{len(endpoints)}</b></div>',
            unsafe_allow_html=True,
        )

        st.markdown("<hr style='border:1px solid var(--border); margin:12px 0;'>", unsafe_allow_html=True)

        st.markdown(
            '<div style="display:flex; align-items:center; gap:8px; margin-bottom:10px;">'
            '<span class="sidebar-icon" style="background:linear-gradient(135deg,var(--accent),var(--accent2)); '
            'border-color:transparent; color:#fff;">📊</span>'
            '<span style="font-weight:700; font-size:0.92rem;">Quick Stats</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        auth_count = sum(1 for e in endpoints if e.get("auth_required"))
        error_count = sum(1 for e in endpoints if e.get("error_codes"))

        st.markdown(
            f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px;">'
            f'<div class="stat-card"><span class="stat-icon">📡</span><div class="stat-value">{len(endpoints)}</div><div class="stat-label">Endpoints</div></div>'
            f'<div class="stat-card"><span class="stat-icon">🔐</span><div class="stat-value">{auth_count}</div><div class="stat-label">Auth</div></div>'
            f'<div class="stat-card"><span class="stat-icon">⚠️</span><div class="stat-value">{error_count}</div><div class="stat-label">Errors</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='border:1px solid var(--border); margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="text-align:center; font-size:0.72rem; color:var(--muted);">'
        f'Session <code style="background:var(--surface); padding:2px 6px; border-radius:4px; '
        f'border:1px solid var(--border);">{SID[:8]}</code></div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="hero animate-in">'
    '<h1>⚡ AI-Powered API Documentation & Testing Portal</h1>'
    '<p>Upload route definitions or paste endpoints → get AI-generated docs, sample requests/responses, test cases, and plain-English error explanations.</p>'
    '</div>',
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Step 1 — Load data
# ------------------------------------------------------------------
st.markdown(
    '<div class="section-header animate-in-slow" style="animation-delay:0.1s;">'
    '<span class="icon">📥</span> Load your API definitions'
    '</div>',
    unsafe_allow_html=True,
)

tab_upload, tab_paste, tab_sample = st.tabs(["📁 Upload", "✏️ Paste", "📦 Demo"])

with tab_upload:
    st.markdown("Supports **OpenAPI/Swagger** (`.json` / `.yaml`), the portal's own `endpoints.json` schema, or a **FastAPI / Flask** `.py` source file.")
    uploaded = st.file_uploader("Choose a file", type=["json", "yaml", "yml", "py"], label_visibility="collapsed")
    if uploaded and st.button("Parse uploaded file", key="btn_parse_upload", type="primary"):
        with st.spinner("Parsing..."):
            files = {"file": (uploaded.name, uploaded.getvalue())}
            r = requests.post(f"{BACKEND_URL}/upload", params={"session_id": SID}, files=files)
        if r.ok:
            st.session_state.endpoints = r.json()["endpoints"]
            st.rerun()
        else:
            st.error(r.json().get("detail", "Failed to parse file."))

with tab_paste:
    st.markdown("Paste raw JSON (`{\"endpoints\": [...]}`) **or** freeform lines like `GET /users - list users`.")
    pasted = st.text_area(
        "Paste here",
        height=140,
        placeholder="GET /api/v1/orders - list all orders\nPOST /api/v1/orders - create an order\nDELETE /api/v1/orders/{id} - delete an order",
        label_visibility="collapsed",
    )
    if st.button("Parse pasted text", key="btn_parse_text", type="primary"):
        with st.spinner("Parsing..."):
            r = requests.post(f"{BACKEND_URL}/parse-text", json={"session_id": SID, "text": pasted})
        if r.ok:
            st.session_state.endpoints = r.json()["endpoints"]
            st.rerun()
        else:
            st.error(r.json().get("detail", "Failed to parse text."))

with tab_sample:
    st.markdown("Load a **100-endpoint demo dataset** (20 resources, full CRUD) to explore the portal instantly.")
    if st.button("Load demo dataset", key="btn_load_sample", type="primary"):
        with st.spinner("Loading..."):
            r = requests.post(f"{BACKEND_URL}/load-sample", params={"session_id": SID})
        if r.ok:
            st.session_state.endpoints = r.json()["endpoints"]
            st.rerun()
        else:
            st.error(r.text)

# ------------------------------------------------------------------
# Step 2 — Explore
# ------------------------------------------------------------------
endpoints = st.session_state.endpoints
if not endpoints:
    st.markdown(
        '<div class="glow-card animate-in-slow" style="text-align:center; padding:40px 20px;">'
        '<div style="font-size:3rem; margin-bottom:8px; animation: float 3s ease-in-out infinite;">🚀</div>'
        '<div style="font-size:1.1rem; font-weight:600;">Load some endpoints above to get started</div>'
        '<div style="font-size:0.85rem; color:var(--muted); margin-top:4px;">Upload a file, paste text, or try the demo dataset</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.stop()

st.markdown(
    '<div class="section-header animate-in-slow" style="animation-delay:0.15s;">'
    '<span class="icon">🔎</span> Explore an endpoint'
    '</div>',
    unsafe_allow_html=True,
)

filtered_endpoints = [e for e in endpoints if endpoint_matches(e, st.session_state.search_query, st.session_state.method_filter)]

if not filtered_endpoints:
    st.markdown(
        '<div class="glow-card" style="text-align:center; padding:32px 20px;">'
        '<div style="font-size:2.5rem; margin-bottom:6px;">🤔</div>'
        '<div style="font-weight:600;">No endpoints match your search</div>'
        '<div style="font-size:0.85rem; color:var(--muted);">Try adjusting the sidebar filters</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.stop()

labels = [f"{e['method'].upper()}  {e['path']}" for e in filtered_endpoints]
idx = st.selectbox("Select endpoint", range(len(labels)), format_func=lambda i: labels[i], label_visibility="collapsed")
endpoint = filtered_endpoints[idx]
real_index = endpoints.index(endpoint)

# ---- Endpoint card ----
auth_html = (
    f'{pulse_dot("green")} <span style="color:var(--green); font-weight:600;">Yes</span>'
    if endpoint.get("auth_required")
    else '<span style="color:var(--muted);">No</span>'
)
codes = endpoint.get("error_codes", [])
codes_html = (
    " ".join(f'<code style="background:var(--surface2); padding:2px 6px; border-radius:4px; font-size:0.78rem; border:1px solid var(--border);">{c}</code>' for c in codes)
    if codes
    else '<span style="color:var(--muted);">None</span>'
)

params = []
for k in (endpoint.get("query_params") or {}):
    params.append(f'<code style="color:var(--cyan);">{k}</code>')
for k in (endpoint.get("request_body") or {}) if isinstance(endpoint.get("request_body"), dict) else {}:
    params.append(f'<code style="color:var(--purple);">{k}</code> <span style="font-size:0.72rem; color:var(--muted);">(body)</span>')
params_html = ", ".join(params) if params else '<span style="color:var(--muted);">None</span>'

desc_text = endpoint.get("description", "")[:60] or "No description"

st.markdown(
    f'<div class="glow-card animate-scale" style="animation-delay:0.1s;">'
    f'<div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">'
    f'{method_badge(endpoint["method"])}'
    f'<code style="font-size:0.95rem; font-weight:600;">{endpoint["path"]}</code>'
    f'<span style="margin-left:auto; display:flex; align-items:center; gap:12px; font-size:0.82rem;">'
    f'<span>{auth_html}</span>'
    f'<span>🔒 {desc_text}</span>'
    f'</span>'
    f'</div>'
    f'<div style="margin-top:10px; padding-top:10px; border-top:1px solid var(--border); '
    f'display:flex; align-items:center; gap:16px; flex-wrap:wrap; font-size:0.82rem;">'
    f'<span><b>Params:</b> {params_html}</span>'
    f'<span><b>Errors:</b> {codes_html}</span>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)

with st.expander("Raw definition", expanded=False):
    st.json(endpoint)

st.markdown("<hr style='border:1px solid var(--border);'>", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Step 3 — Action tabs
# ------------------------------------------------------------------
st.markdown(
    '<div class="section-header animate-in-slow" style="animation-delay:0.2s;">'
    '<span class="icon">🚀</span> Take action'
    '</div>',
    unsafe_allow_html=True,
)

tab_docs, tab_tests, tab_try, tab_error = st.tabs([
    "📄 Documentation",
    "🧪 Test Cases",
    "🚀 Try It Live",
    "❓ Explain Error",
])

# ======================== DOCUMENTATION ========================
with tab_docs:
    st.markdown('<div class="section-header"><span class="icon">📄</span> AI-Generated Documentation</div>', unsafe_allow_html=True)
    st.caption("Get a full documentation page for this endpoint: summary, parameters, samples, usage notes.")

    if st.button("Generate documentation", key="gen_docs", type="primary"):
        with st.spinner("Generating..."):
            r, err = post_ai("/generate-docs", {"session_id": SID, "endpoint_index": real_index})
        if err:
            st.error(err)
        elif r.ok:
            doc = r.json()["documentation"]

            st.markdown(
                f'<div class="glow-card animate-scale" style="border-left:4px solid var(--accent);">'
                f'<div style="font-size:1.15rem; font-weight:700; margin-bottom:6px;">{doc.get("summary", "")}</div>'
                f'<div style="color:var(--muted); font-size:0.9rem;">{doc.get("detailed_description", "")}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            params_exp = doc.get("parameters_explained") or {}
            if params_exp:
                st.markdown("**Parameters explained:**")
                for k, v in params_exp.items():
                    st.markdown(f"- `{k}` — {v}")

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Sample request**")
                req_val = doc.get("sample_request")
                if isinstance(req_val, (dict, list)):
                    st.json(req_val)
                elif isinstance(req_val, str):
                    req_stripped = req_val.strip()
                    if (req_stripped.startswith("{") and req_stripped.endswith("}")) or (req_stripped.startswith("[") and req_stripped.endswith("]")):
                        try:
                            st.json(json.loads(req_stripped))
                        except Exception:
                            st.code(req_val)
                    elif req_stripped.lower().startswith("curl"):
                        st.code(req_val, language="bash")
                    else:
                        st.code(req_val)
                elif req_val is not None:
                    st.code(str(req_val))
                else:
                    st.caption("None")
            with c2:
                st.markdown("**Sample response**")
                resp_val = doc.get("sample_response")
                if isinstance(resp_val, (dict, list)):
                    st.json(resp_val)
                elif isinstance(resp_val, str):
                    resp_stripped = resp_val.strip()
                    if (resp_stripped.startswith("{") and resp_stripped.endswith("}")) or (resp_stripped.startswith("[") and resp_stripped.endswith("]")):
                        try:
                            st.json(json.loads(resp_stripped))
                        except Exception:
                            st.code(resp_val)
                    else:
                        st.code(resp_val)
                elif resp_val is not None:
                    st.code(str(resp_val))
                else:
                    st.caption("None")

            if doc.get("usage_notes"):
                st.markdown("**Usage notes / gotchas:**")
                for n in doc["usage_notes"]:
                    st.markdown(f"- {n}")

            if doc.get("_generated_by"):
                st.markdown(f'<p class="small-text">Generated by: {doc["_generated_by"]}</p>', unsafe_allow_html=True)
        else:
            st.error(r.text)

# ======================== TEST CASES ========================
with tab_tests:
    st.markdown('<div class="section-header"><span class="icon">🧪</span> AI-Generated Test Cases</div>', unsafe_allow_html=True)
    st.caption("Copy-paste pytest snippets for happy path, auth failures, validation errors, and not-found cases.")

    if st.button("Generate test cases", key="gen_tests", type="primary"):
        with st.spinner("Generating..."):
            r, err = post_ai("/generate-tests", {"session_id": SID, "endpoint_index": real_index})
        if err:
            st.error(err)
        elif r.ok:
            tests = r.json()["test_cases"]
            st.markdown(
                f'<div class="success-box animate-scale">'
                f'Generated <b>{len(tests)}</b> test case(s) — copy these into your test suite.'
                f'</div>',
                unsafe_allow_html=True,
            )

            for i, t in enumerate(tests):
                status = t.get("expected_status", "?")
                with st.expander(f"{t['name']}  —  expects {status}", expanded=(i == 0)):
                    st.write(t.get("description", ""))
                    st.markdown("**Request:**")
                    st.json(t.get("request"))
                    st.markdown("**Expected response shape:**")
                    st.write(t.get("expected_response_shape"))
                    st.markdown("**Pytest snippet:**")
                    st.code(t.get("pytest_snippet", ""), language="python")
                    if t.get("_generated_by"):
                        st.markdown(f'<p class="small-text">Generated by: {t["_generated_by"]}</p>', unsafe_allow_html=True)
        else:
            st.error(r.text)

# ======================== TRY IT LIVE ========================
with tab_try:
    st.markdown('<div class="section-header"><span class="icon">🚀</span> Live Endpoint Tester</div>', unsafe_allow_html=True)
    st.caption("Point at a real, running API. Failed calls are auto-explained by the AI.")

    c_url, c_path = st.columns([2, 3])
    with c_url:
        base_url = st.text_input("Base URL", placeholder="https://api.yourservice.com")
    with c_path:
        path_to_call = st.text_input("Path", value=endpoint["path"])

    c_hdr, c_body = st.columns(2)
    with c_hdr:
        headers_raw = st.text_area(
            "Headers (JSON)",
            value=json.dumps({"Authorization": "Bearer YOUR_TOKEN"} if endpoint.get("auth_required") else {}, indent=2),
            height=120,
        )
    with c_body:
        body_raw = st.text_area(
            "Body (JSON)",
            value=json.dumps(endpoint.get("request_body") or {}, indent=2),
            height=120,
            disabled=endpoint["method"].upper() in ("GET", "DELETE"),
        )

    if st.button("Send request", key="send_req", type="primary"):
        try:
            headers = json.loads(headers_raw) if headers_raw.strip() else {}
            body = json.loads(body_raw) if body_raw.strip() and endpoint["method"].upper() in ("POST", "PUT", "PATCH") else None
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON in headers/body: {e}")
            headers, body = None, None

        if base_url and headers is not None:
            with st.spinner("Calling endpoint..."):
                r = requests.post(f"{BACKEND_URL}/try-it", json={
                    "base_url": base_url,
                    "method": endpoint["method"],
                    "path": path_to_call,
                    "headers": headers,
                    "body": body,
                    "endpoint": endpoint,
                })
            if r.ok:
                result = r.json()
                code = result.get("status_code", 0)
                ok = result.get("ok", False)

                st.markdown(
                    f'<div class="glow-card animate-scale" style="text-align:center; padding:16px;">'
                    f'{status_badge(code, ok)}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                st.markdown("**Response body:**")
                st.json(result.get("response_body") or result.get("network_error"))

                resp_headers = result.get("headers", {})
                if resp_headers:
                    with st.expander("Response headers"):
                        st.json(resp_headers)

                if "ai_explanation" in result:
                    exp = result["ai_explanation"]
                    sev = exp.get("severity", "low")
                    st.markdown(
                        f'<div class="glow-card animate-scale" style="border-left:4px solid var(--purple);">'
                        f'<div class="section-header" style="margin-bottom:8px;">'
                        f'<span class="icon">🤖</span> AI Error Analysis'
                        f'</div>'
                        f'<div style="margin-bottom:6px;"><b>Likely cause:</b> {exp.get("likely_cause", "")} &nbsp; {severity_badge(sev)}</div>'
                        f'<div style="color:var(--muted); margin-bottom:6px;">{exp.get("plain_english_explanation", "")}</div>'
                        f'<div><b>Suggested fix:</b> {exp.get("suggested_fix", "")}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.error(r.text)
        elif not base_url:
            st.warning("Enter a base URL to test against.")

# ======================== EXPLAIN ERROR ========================
with tab_error:
    st.markdown('<div class="section-header"><span class="icon">❓</span> Error Explainer</div>', unsafe_allow_html=True)
    st.caption("Paste any status code + response body (from Postman, logs, etc.) and get a plain-English explanation + fix.")

    c_code, c_sev = st.columns([1, 2])
    with c_code:
        status_code = st.number_input("HTTP status code", min_value=100, max_value=599, value=422)
    with c_sev:
        payload_raw = st.text_area(
            "Response payload (JSON or text)",
            value='{"error": "validation_error", "details": {"email": "is required"}}',
            height=80,
        )

    if st.button("Explain this error", key="explain_err", type="primary"):
        try:
            payload = json.loads(payload_raw)
        except json.JSONDecodeError:
            payload = payload_raw

        with st.spinner("Analyzing..."):
            r, err = post_ai("/explain-error", {
                "endpoint": endpoint,
                "status_code": int(status_code),
                "response_payload": payload,
            })
        if err:
            st.error(err)
        elif r.ok:
            exp = r.json()["explanation"]
            sev = exp.get("severity", "low")
            st.markdown(
                f'<div class="glow-card animate-scale" style="border-left:4px solid var(--amber);">'
                f'<div style="margin-bottom:6px;"><b>Likely cause:</b> {exp.get("likely_cause", "")} &nbsp; {severity_badge(sev)}</div>'
                f'<div style="color:var(--muted); margin-bottom:6px;">{exp.get("plain_english_explanation", "")}</div>'
                f'<div><b>Suggested fix:</b> {exp.get("suggested_fix", "")}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.error(r.text)

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    f'<div class="footer-line animate-fade" style="animation-delay:0.4s;">'
    f'<span style="font-size:1.1rem;">⚡</span>'
    f'<span class="dot"></span>'
    f'<span>Session <code style="background:var(--surface); padding:2px 8px; border-radius:4px; '
    f'border:1px solid var(--border);">{SID[:8]}</code></span>'
    f'<span class="dot"></span>'
    f'<span>Data resets on backend restart</span>'
    f'<span class="dot"></span>'
    f'<span style="color:var(--accent);">🚀 Powered by AI</span>'
    f'</div>',
    unsafe_allow_html=True,
)
