import json
import re
import requests
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="DishSense AI — Restaurant Intelligence",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background: #060A08;
    color: #B8C4B0;
}
.block-container { max-width: 1100px !important; padding: 0 2rem 4rem !important; }
.main > div { padding-top: 0 !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #070C09;
    border-right: 1px solid #141F17;
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: #8A9E88 !important; }

.sb-brand {
    padding: 28px 20px 22px;
    border-bottom: 1px solid #141F17;
    margin-bottom: 24px;
}
.sb-brand-logo {
    display: flex; align-items: center; gap: 12px; margin-bottom: 4px;
}
.sb-brand-icon {
    width: 38px; height: 38px; border-radius: 12px;
    background: linear-gradient(135deg, #3DFF8A, #00C957);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
}
.sb-brand-name { font-size: 17px; font-weight: 800; color: #EAF2E8 !important; letter-spacing: -0.03em; }
.sb-brand-tag  { font-size: 11px; color: #3A5040 !important; letter-spacing: 0.05em; margin-top: 2px; }

[data-testid="stSidebar"] label {
    font-size: 10px !important; font-weight: 700 !important;
    color: #2E4535 !important; text-transform: uppercase !important; letter-spacing: 0.1em !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: #0D1610 !important; border: 1px solid #1A2E20 !important;
    border-radius: 8px !important; font-size: 13px !important; color: #8A9E88 !important;
}
[data-testid="stSidebar"] .stSlider [data-testid="stSliderThumb"] { background: #3DFF8A !important; }
[data-testid="stSidebar"] .stSlider [data-testid="stSliderTrackFill"] { background: #3DFF8A !important; }
[data-testid="stSidebar"] .stButton > button {
    background: #0D1610 !important; color: #4A6A50 !important;
    border: 1px solid #1A2E20 !important; border-radius: 8px !important;
    font-size: 12px !important; font-weight: 500 !important;
    padding: 0.4rem 1rem !important; width: 100% !important; box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #141F17 !important; color: #8A9E88 !important; transform: none !important;
}

/* ── Hero banner ── */
.hero {
    background: #060A08;
    padding: 40px 0 32px;
    border-bottom: 1px solid #0F1A12;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; top: -60px; right: -80px;
    width: 320px; height: 320px; border-radius: 50%;
    background: radial-gradient(circle, rgba(61,255,138,0.04) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(61,255,138,0.08); border: 1px solid rgba(61,255,138,0.18);
    color: #3DFF8A; font-size: 11px; font-weight: 700;
    padding: 4px 12px; border-radius: 999px;
    letter-spacing: 0.08em; text-transform: uppercase;
    margin-bottom: 16px;
}
.hero-title {
    font-size: 38px; font-weight: 900; color: #EAF2E8;
    letter-spacing: -0.04em; line-height: 1.1; margin-bottom: 10px;
}
.hero-title span { color: #3DFF8A; }
.hero-sub {
    font-size: 16px; color: #4A6A50; font-weight: 400; line-height: 1.6;
    max-width: 560px;
}

/* ── Step pills ── */
.steps-row {
    display: flex; align-items: center; gap: 6px;
    margin-bottom: 28px; flex-wrap: wrap;
}
.step-pill {
    display: flex; align-items: center; gap: 6px;
    background: #0D1610; border: 1px solid #1A2E20;
    border-radius: 999px; padding: 6px 14px;
    font-size: 12px; font-weight: 500; color: #3A5040;
    transition: all 0.2s;
}
.step-pill.active {
    background: rgba(61,255,138,0.1); border-color: rgba(61,255,138,0.3);
    color: #3DFF8A;
}
.step-pill-num {
    width: 18px; height: 18px; border-radius: 50%;
    background: #141F17; display: flex; align-items: center;
    justify-content: center; font-size: 10px; font-weight: 700; color: #3A5040;
}
.step-pill.active .step-pill-num {
    background: rgba(61,255,138,0.2); color: #3DFF8A;
}
.step-arrow { color: #1A2E20; font-size: 16px; }

/* ── Search box ── */
.search-section {
    background: #0A0F0B;
    border: 1px solid #141F17;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 20px;
}
.section-label {
    font-size: 10px; font-weight: 700; color: #2E4535;
    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 10px;
}
.stTextInput > div > div > input {
    background: #0D1610 !important; border: 1px solid #1A2E20 !important;
    border-radius: 12px !important; font-size: 15px !important; color: #C8D4C0 !important;
    padding: 14px 16px !important; font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #3DFF8A !important;
    box-shadow: 0 0 0 3px rgba(61,255,138,0.08) !important;
}
.stTextInput > div > div > input::placeholder { color: #2A3E30 !important; }

/* ── Buttons ── */
.stButton > button {
    background: #3DFF8A !important; color: #050C07 !important; border: none !important;
    border-radius: 12px !important; font-size: 14px !important; font-weight: 800 !important;
    padding: 0.72rem 1.6rem !important; letter-spacing: -0.02em;
    box-shadow: 0 0 24px rgba(61,255,138,0.15) !important; transition: all 0.15s !important;
}
.stButton > button:hover {
    background: #00E87A !important;
    box-shadow: 0 0 36px rgba(61,255,138,0.25) !important;
    transform: translateY(-1px) !important;
}

/* ── Place cards ── */
.place-card {
    background: #0A0F0B; border: 1px solid #141F17;
    border-radius: 14px; padding: 16px 18px; margin-bottom: 10px;
    transition: border-color 0.2s, background 0.2s;
}
.place-card:hover { border-color: #1E3524; background: #0C1410; }
.place-name { font-size: 15px; font-weight: 700; color: #D4E8D0; margin-bottom: 3px; }
.place-addr { font-size: 12px; color: #3A5040; line-height: 1.5; }
.place-meta { display: flex; gap: 12px; margin-top: 6px; }
.place-rating { font-size: 12px; color: #3DFF8A; font-weight: 600; }
.place-reviews { font-size: 12px; color: #2A3E30; }

/* ── Review cards ── */
.review-card {
    background: #0A0F0B; border: 1px solid #141F17;
    border-radius: 12px; padding: 14px 16px; margin-bottom: 8px;
}
.rev-author { font-size: 13px; font-weight: 600; color: #C8D4C0; margin-bottom: 3px; }
.rev-stars { font-size: 12px; color: #3DFF8A; margin-bottom: 6px; }
.rev-text { font-size: 13px; color: #5A7060; line-height: 1.65; }
.rev-time { font-size: 11px; color: #2A3E30; margin-top: 6px; }

/* ── Verdict banner ── */
.verdict {
    background: #080D09;
    border: 1px solid #1A2E20;
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 20px;
    display: grid;
    grid-template-columns: auto 1px auto 1px 1fr;
    align-items: center;
    gap: 28px;
    position: relative;
    overflow: hidden;
}
.verdict::after {
    content: '';
    position: absolute; bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #3DFF8A, transparent);
}
.verdict-score { text-align: center; }
.verdict-score-num {
    font-size: 52px; font-weight: 900; color: #3DFF8A;
    letter-spacing: -0.05em; line-height: 1;
}
.verdict-score-denom { font-size: 18px; color: #2A3E30; font-weight: 400; }
.verdict-score-stars { font-size: 16px; color: #3DFF8A; margin-top: 4px; }
.verdict-sep { width: 1px; height: 60px; background: #141F17; flex-shrink: 0; }
.verdict-sentiment {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 11px; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; padding: 4px 12px;
    border-radius: 999px; margin-bottom: 8px;
}
.sent-positive { background: rgba(61,255,138,0.1); color: #3DFF8A; border: 1px solid rgba(61,255,138,0.2); }
.sent-negative { background: rgba(255,80,80,0.1); color: #FF8080; border: 1px solid rgba(255,80,80,0.2); }
.sent-neutral  { background: rgba(148,163,184,0.1); color: #94a3b8; border: 1px solid rgba(148,163,184,0.2); }
.sent-mixed    { background: rgba(255,191,36,0.1); color: #FFD166; border: 1px solid rgba(255,191,36,0.2); }
.verdict-line { font-size: 17px; color: #C8D4C0; line-height: 1.5; font-weight: 500; }
.verdict-meta { font-size: 12px; color: #3A5040; margin-top: 4px; }

/* ── Score grid ── */
.score-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }
.score-card {
    background: #080D09; border: 1px solid #141F17;
    border-radius: 14px; padding: 16px;
    position: relative; overflow: hidden;
}
.score-card::before {
    content: '';
    position: absolute; bottom: 0; left: 0;
    height: 3px; background: var(--accent);
    width: var(--pct); border-radius: 0 0 14px 14px;
    transition: width 0.8s ease;
}
.score-label { font-size: 10px; font-weight: 700; color: #2A3E30; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }
.score-icon { font-size: 22px; margin-bottom: 6px; }
.score-value { font-size: 26px; font-weight: 900; color: #EAF2E8; letter-spacing: -0.03em; }
.score-denom { font-size: 13px; color: #2A3E30; font-weight: 400; }
.score-bar-bg { background: #141F17; border-radius: 999px; height: 4px; margin-top: 8px; overflow: hidden; }
.score-bar-fill { height: 100%; border-radius: 999px; background: var(--accent); transition: width 0.8s ease; }

/* ── Summary card ── */
.summary-card {
    background: #080D09; border: 1px solid #1A2E20;
    border-left: 2px solid #3DFF8A;
    border-radius: 14px; padding: 20px 22px; margin-bottom: 14px;
}
.summary-label { font-size: 10px; font-weight: 700; color: #2A3E30; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; }
.summary-text { font-size: 14px; color: #7A9A78; line-height: 1.8; }

/* ── List cards ── */
.list-card {
    background: #080D09; border: 1px solid #141F17;
    border-radius: 14px; padding: 18px; height: 100%;
}
.list-card-head {
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 12px; padding-bottom: 10px;
    border-bottom: 1px solid #0F1A12;
}
.list-card-icon { font-size: 16px; }
.list-card-title { font-size: 13px; font-weight: 700; color: #B8C4B0; letter-spacing: -0.01em; }
.list-item {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 8px 10px; border-radius: 10px; margin-bottom: 5px;
    font-size: 13px; line-height: 1.55;
}
.li-pos  { background: rgba(61,255,138,0.05);  color: #7AE89A; border: 1px solid rgba(61,255,138,0.12); }
.li-neg  { background: rgba(255,100,100,0.05); color: #FF9999; border: 1px solid rgba(255,100,100,0.12); }
.li-warn { background: rgba(255,210,50,0.05);  color: #FFDA6A; border: 1px solid rgba(255,210,50,0.12); }
.li-info { background: rgba(100,180,255,0.05); color: #90C8FF; border: 1px solid rgba(100,180,255,0.12); }
.li-dot { width: 6px; height: 6px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.d-pos  { background: #3DFF8A; }
.d-neg  { background: #FF6464; }
.d-warn { background: #FFD132; }
.d-info { background: #64B4FF; }

/* ── Tag rows ── */
.tag-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
.tag { background: #0D1610; border: 1px solid #1A2E20; color: #4A6A50; font-size: 12px; font-weight: 500; padding: 4px 12px; border-radius: 999px; }
.tag-green { background: rgba(61,255,138,0.07); border: 1px solid rgba(61,255,138,0.18); color: #3DFF8A; }
.tag-red   { background: rgba(255,100,100,0.07); border: 1px solid rgba(255,100,100,0.18); color: #FF8888; }

/* ── Info pills ── */
.pill-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: #0A0F0B; border: 1px solid #141F17;
    border-radius: 999px; padding: 5px 12px;
    font-size: 12px; color: #3A5040; font-weight: 500;
}
.pill-green { background: rgba(61,255,138,0.07); border-color: rgba(61,255,138,0.2); color: #3DFF8A; }
.pill-dot { width: 6px; height: 6px; border-radius: 50%; background: #3DFF8A; }

/* ── Divider ── */
.div { height: 1px; background: #0F1A12; margin: 24px 0; }

/* ── Report header ── */
.report-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 20px; flex-wrap: wrap; gap: 12px;
}
.report-title { font-size: 22px; font-weight: 900; color: #EAF2E8; letter-spacing: -0.03em; }
.report-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(61,255,138,0.08); border: 1px solid rgba(61,255,138,0.2);
    color: #3DFF8A; font-size: 11px; font-weight: 700;
    padding: 5px 14px; border-radius: 999px; letter-spacing: 0.05em;
}

/* ── Competitor edge ── */
.edge-card {
    background: #080D09; border: 1px solid #1A2E20;
    border-radius: 14px; padding: 18px 20px;
    display: flex; align-items: flex-start; gap: 14px;
}
.edge-icon-wrap {
    width: 38px; height: 38px; border-radius: 10px;
    background: rgba(61,255,138,0.1); border: 1px solid rgba(61,255,138,0.2);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}
.edge-label { font-size: 10px; font-weight: 700; color: #2A3E30; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 5px; }
.edge-text { font-size: 14px; color: #7A9A78; line-height: 1.6; }

/* ── Download ── */
.stDownloadButton button {
    background: #0D1610 !important; color: #4A6A50 !important;
    border: 1px solid #1A2E20 !important; border-radius: 10px !important;
    font-size: 13px !important; font-weight: 600 !important;
    padding: 9px 20px !important; width: auto !important; box-shadow: none !important;
}
.stDownloadButton button:hover {
    background: #141F17 !important; color: #8A9E88 !important;
    transform: none !important; box-shadow: none !important;
}

/* spinner */
.stSpinner > div { border-top-color: #3DFF8A !important; }

/* expander */
.streamlit-expanderHeader { color: #4A6A50 !important; font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)


# ── Secrets ───────────────────────────────────────────────────────────────────
GROQ_KEY   = st.secrets["GROQ_API_KEY"]
PLACES_KEY = st.secrets["GOOGLE_PLACES_API_KEY"]

PLACES_BASE = "https://maps.googleapis.com/maps/api/place"


# ── Google Places ─────────────────────────────────────────────────────────────
def search_places(query: str) -> list:
    params = {"query": query + " restaurant", "type": "restaurant", "key": PLACES_KEY}
    r = requests.get(f"{PLACES_BASE}/textsearch/json", params=params, timeout=10)
    r.raise_for_status()
    return r.json().get("results", [])[:8]


def get_place_details(place_id: str) -> dict:
    params = {
        "place_id": place_id,
        "fields": "name,rating,user_ratings_total,formatted_address,reviews,price_level,url",
        "key": PLACES_KEY,
        "reviews_sort": "newest",
    }
    r = requests.get(f"{PLACES_BASE}/details/json", params=params, timeout=10)
    r.raise_for_status()
    return r.json().get("result", {})


# ── Groq AI analysis ──────────────────────────────────────────────────────────
def analyse_reviews(reviews: list, place_name: str, language: str, model: str, temp: float) -> dict:
    client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")
    reviews_text = "\n\n".join([
        f"Reviewer: {r.get('author_name','Unknown')}\nRating: {r.get('rating','?')}/5\nReview: {r.get('text','').strip()}"
        for r in reviews
    ])
    system = "You are an elite restaurant business intelligence analyst. Return ONLY valid JSON. No markdown. No explanation."
    prompt = f"""
Deeply analyse these Google Maps reviews for: "{place_name}"

REVIEWS:
{reviews_text}

Return ONLY this exact JSON:
{{
  "overall_sentiment": "Positive / Neutral / Negative / Mixed",
  "estimated_rating_out_of_5": 4.2,
  "one_line_verdict": "one punchy verdict",
  "executive_summary": "2-3 sentence executive summary for the owner",
  "top_positives": [
    {{"point": "specific positive", "frequency": "X of Y reviewers mention this"}},
    {{"point": "...", "frequency": "..."}},
    {{"point": "...", "frequency": "..."}}
  ],
  "top_negatives": [
    {{"point": "specific complaint", "frequency": "X of Y reviewers mention this"}},
    {{"point": "...", "frequency": "..."}},
    {{"point": "...", "frequency": "..."}}
  ],
  "customer_pain_points": ["pain 1", "pain 2", "pain 3"],
  "business_suggestions": [
    {{"suggestion": "specific actionable fix", "priority": "High"}},
    {{"suggestion": "...", "priority": "Medium"}},
    {{"suggestion": "...", "priority": "Low"}}
  ],
  "food_quality_score": 8.2,
  "service_score": 7.1,
  "value_for_money_score": 6.5,
  "ambience_score": 7.8,
  "best_dishes_mentioned": ["dish 1", "dish 2", "dish 3"],
  "worst_complaints": ["complaint 1", "complaint 2"],
  "best_for": ["families", "dates", "quick lunch"],
  "keywords": ["word1", "word2", "word3", "word4", "word5"],
  "competitor_edge": "one powerful line on what sets this place apart or holds it back",
  "owner_action_plan": "3 sentence personalised action plan for the restaurant owner to improve ratings"
}}

Output language: {language}
Be hyper-specific — quote actual dishes, names, patterns from the reviews.
"""
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        temperature=temp,
    )
    text = resp.choices[0].message.content
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            return json.loads(m.group())
        raise ValueError("Could not parse JSON from Groq response.")


# ── Helpers ───────────────────────────────────────────────────────────────────
def star_str(rating, out_of=5):
    try:
        f = round(float(rating))
        return "★" * f + "☆" * (out_of - f)
    except Exception:
        return "★★★★☆"

def score_bar_html(score, label, icon, color):
    try: pct = min(100, max(0, float(score) * 10))
    except: pct = 0
    return f"""
<div class="score-card" style="--accent:{color}; --pct:{pct:.0f}%">
    <div class="score-label">{label}</div>
    <div class="score-icon">{icon}</div>
    <div><span class="score-value">{score}</span><span class="score-denom">/10</span></div>
    <div class="score-bar-bg"><div class="score-bar-fill" style="width:{pct:.0f}%; background:{color};"></div></div>
</div>"""

def render_items(items, li_cls, dot_cls):
    html = ""
    for item in items:
        if isinstance(item, dict):
            text = item.get("point") or item.get("suggestion") or str(item)
            sub  = item.get("frequency") or item.get("priority") or ""
            html += f'<div class="list-item {li_cls}"><div class="li-dot {dot_cls}"></div><span>{text}'
            if sub: html += f' <span style="font-size:11px;opacity:0.55;margin-left:4px">· {sub}</span>'
            html += '</span></div>'
        else:
            html += f'<div class="list-item {li_cls}"><div class="li-dot {dot_cls}"></div><span>{item}</span></div>'
    return html


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-brand-logo">
            <div class="sb-brand-icon">🍽️</div>
            <div>
                <div class="sb-brand-name">DishSense AI</div>
            </div>
        </div>
        <div class="sb-brand-tag">RESTAURANT INTELLIGENCE PLATFORM</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("**AI Engine**")
    model = st.selectbox("Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"], index=0, label_visibility="collapsed")
    st.markdown("**Output Language**")
    language = st.selectbox("Language", ["English", "Telugu", "Tenglish", "Hindi"], index=0, label_visibility="collapsed")
    st.markdown("**Creativity**")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1, label_visibility="collapsed")

    st.markdown("---")
    if st.button("🗑️  Clear & restart"):
        for k in ["results","selected","details","analysis"]:
            st.session_state.pop(k, None)
        st.rerun()

    st.markdown("""
    <div style="margin-top:20px; padding:16px; background:#0A0F0B; border:1px solid #141F17; border-radius:12px;">
        <div style="font-size:10px;color:#2A3E30;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;font-weight:700;">How it works</div>
        <div style="font-size:12px;color:#3A5040;line-height:2;">
            🔍 Search any restaurant<br>
            📍 Pick from live results<br>
            📋 Fetch real Google reviews<br>
            🤖 Groq AI deep analysis<br>
            📊 Get full business report
        </div>
    </div>""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🌟 AI-Powered Restaurant Intelligence</div>
    <div class="hero-title">Know exactly what<br>customers <span>really think</span></div>
    <div class="hero-sub">Search any restaurant · fetch live Google reviews · get a deep AI analysis that tells you exactly what's working, what's broken, and how to fix it.</div>
</div>""", unsafe_allow_html=True)

# Step indicator
step = 1
if "results"  in st.session_state: step = 2
if "selected" in st.session_state: step = 3
if "analysis" in st.session_state: step = 4

st.markdown(f"""
<div class="steps-row">
    <div class="step-pill {'active' if step>=1 else ''}"><div class="step-pill-num">1</div>Search</div>
    <div class="step-arrow">›</div>
    <div class="step-pill {'active' if step>=2 else ''}"><div class="step-pill-num">2</div>Pick restaurant</div>
    <div class="step-arrow">›</div>
    <div class="step-pill {'active' if step>=3 else ''}"><div class="step-pill-num">3</div>Fetch reviews</div>
    <div class="step-arrow">›</div>
    <div class="step-pill {'active' if step>=4 else ''}"><div class="step-pill-num">4</div>AI report</div>
</div>""", unsafe_allow_html=True)


# ══ STEP 1 — Search ══════════════════════════════════════════════════════════
st.markdown('<div class="section-label">Search Restaurant</div>', unsafe_allow_html=True)
c1, c2 = st.columns([5,1], gap="small")
with c1:
    query = st.text_input("", placeholder="e.g.  Paradise Biryani Hyderabad", label_visibility="collapsed", key="q")
with c2:
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    go = st.button("Search →", use_container_width=True)

if go:
    if not query.strip():
        st.warning("Enter a restaurant name.")
    else:
        with st.spinner("Searching Google Places…"):
            try:
                res = search_places(query.strip())
                if not res:
                    st.error("No results. Try adding the city name.")
                else:
                    st.session_state["results"] = res
                    for k in ["selected","details","analysis"]: st.session_state.pop(k, None)
                    st.rerun()
            except Exception as e:
                st.error(f"Search error: {e}")


# ══ STEP 2 — Pick ═════════════════════════════════════════════════════════════
if "results" in st.session_state:
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    results = st.session_state["results"]
    st.markdown(f'<div class="section-label">{len(results)} restaurants found</div>', unsafe_allow_html=True)

    for i, p in enumerate(results):
        cc, cb = st.columns([6,1], gap="small")
        with cc:
            st.markdown(f"""
            <div class="place-card">
                <div class="place-name">{p.get('name','')}</div>
                <div class="place-addr">{p.get('formatted_address','')}</div>
                <div class="place-meta">
                    <div class="place-rating">★ {p.get('rating','–')}</div>
                    <div class="place-reviews">{p.get('user_ratings_total',0):,} Google reviews</div>
                </div>
            </div>""", unsafe_allow_html=True)
        with cb:
            st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
            if st.button("Select", key=f"sel_{i}"):
                st.session_state["selected"] = p
                for k in ["details","analysis"]: st.session_state.pop(k, None)
                st.rerun()


# ══ STEP 3 — Fetch ════════════════════════════════════════════════════════════
if "selected" in st.session_state and "details" not in st.session_state:
    p = st.session_state["selected"]
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="pill-row">
        <div class="pill pill-green"><div class="pill-dot"></div>{p.get('name','')}</div>
        <div class="pill">★ {p.get('rating','–')} · {p.get('user_ratings_total',0):,} total reviews</div>
    </div>""", unsafe_allow_html=True)

    if st.button("📥  Fetch reviews & run AI analysis →", use_container_width=True):
        with st.spinner("Fetching live reviews from Google…"):
            try:
                details = get_place_details(p["place_id"])
                st.session_state["details"] = details
                reviews = details.get("reviews", [])
                if not reviews:
                    st.error("No reviews found for this restaurant.")
                    st.stop()
            except Exception as e:
                st.error(f"Could not fetch reviews: {e}")
                st.stop()

        with st.spinner("Groq AI is analysing every review…"):
            try:
                analysis = analyse_reviews(reviews, p.get("name",""), language, model, temperature)
                st.session_state["analysis"] = analysis
                st.rerun()
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.stop()


# ══ STEP 4 — Report ═══════════════════════════════════════════════════════════
if "analysis" in st.session_state and "details" in st.session_state:
    details  = st.session_state["details"]
    analysis = st.session_state["analysis"]
    reviews  = details.get("reviews", [])
    place    = st.session_state["selected"]

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    # Raw reviews expander
    with st.expander(f"📋  View {len(reviews)} fetched Google reviews", expanded=False):
        for rev in reviews:
            stars = "★"*rev.get("rating",0) + "☆"*(5-rev.get("rating",0))
            st.markdown(f"""
            <div class="review-card">
                <div class="rev-author">{rev.get('author_name','Anonymous')}</div>
                <div class="rev-stars">{stars}</div>
                <div class="rev-text">{rev.get('text','').strip()}</div>
                <div class="rev-time">{rev.get('relative_time_description','')}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    # Report header
    sentiment = analysis.get("overall_sentiment","N/A")
    s_cls = sentiment.lower() if sentiment.lower() in ["positive","negative","neutral","mixed"] else "neutral"
    rating  = analysis.get("estimated_rating_out_of_5","–")
    verdict = analysis.get("one_line_verdict","")
    g_rating = place.get("rating","–")
    g_total  = place.get("user_ratings_total",0)

    st.markdown(f"""
    <div class="report-header">
        <div class="report-title">AI Intelligence Report</div>
        <div class="report-badge">✓ Analysis complete · {len(reviews)} reviews</div>
    </div>""", unsafe_allow_html=True)

    # Verdict banner
    st.markdown(f"""
    <div class="verdict">
        <div class="verdict-score">
            <div class="verdict-score-num">{rating}</div>
            <div class="verdict-score-denom">/5</div>
            <div class="verdict-score-stars">{star_str(rating)}</div>
        </div>
        <div class="verdict-sep"></div>
        <div>
            <div class="verdict-score-num" style="font-size:22px;color:#4A6A50;">{g_rating}</div>
            <div style="font-size:10px;color:#2A3E30;text-transform:uppercase;letter-spacing:0.08em;margin-top:2px;">Google avg</div>
            <div style="font-size:11px;color:#2A3E30;margin-top:4px;">{g_total:,} reviews</div>
        </div>
        <div class="verdict-sep"></div>
        <div class="verdict-text-wrap">
            <div class="verdict-sentiment sent-{s_cls}">{sentiment}</div>
            <div class="verdict-line">{verdict}</div>
            <div class="verdict-meta">{place.get('name','')} · {place.get('formatted_address','')[:60]}…</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Score cards
    food_s    = analysis.get("food_quality_score", 0)
    service_s = analysis.get("service_score", 0)
    value_s   = analysis.get("value_for_money_score", 0)
    ambience_s= analysis.get("ambience_score", 0)

    st.markdown(
        '<div class="score-grid">'
        + score_bar_html(food_s,     "Food Quality",    "🍛", "#3DFF8A")
        + score_bar_html(service_s,  "Service",         "🤝", "#64B4FF")
        + score_bar_html(value_s,    "Value for Money", "💰", "#FFD132")
        + score_bar_html(ambience_s, "Ambience",        "✨", "#C084FC")
        + '</div>',
        unsafe_allow_html=True
    )

    # Summary + edge
    col_sum, col_edge = st.columns([3,2], gap="medium")
    with col_sum:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-label">Executive Summary</div>
            <div class="summary-text">{analysis.get('executive_summary','–')}</div>
        </div>""", unsafe_allow_html=True)
    with col_edge:
        st.markdown(f"""
        <div class="edge-card">
            <div class="edge-icon-wrap">⚡</div>
            <div>
                <div class="edge-label">Competitive Edge</div>
                <div class="edge-text">{analysis.get('competitor_edge','–')}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Owner action plan
    st.markdown(f"""
    <div class="summary-card" style="border-left-color:#64B4FF;margin-top:14px;">
        <div class="summary-label" style="color:#2A4060;">🎯 Owner Action Plan</div>
        <div class="summary-text">{analysis.get('owner_action_plan','–')}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Positives & Negatives
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown(f"""
        <div class="list-card">
            <div class="list-card-head"><div class="list-card-icon">✅</div><div class="list-card-title">Top Positives</div></div>
            {render_items(analysis.get('top_positives',[]), 'li-pos', 'd-pos')}
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="list-card">
            <div class="list-card-head"><div class="list-card-icon">❌</div><div class="list-card-title">Top Negatives</div></div>
            {render_items(analysis.get('top_negatives',[]), 'li-neg', 'd-neg')}
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2, gap="medium")
    with c3:
        st.markdown(f"""
        <div class="list-card">
            <div class="list-card-head"><div class="list-card-icon">😟</div><div class="list-card-title">Customer Pain Points</div></div>
            {render_items(analysis.get('customer_pain_points',[]), 'li-warn', 'd-warn')}
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="list-card">
            <div class="list-card-head"><div class="list-card-icon">💡</div><div class="list-card-title">Business Suggestions</div></div>
            {render_items(analysis.get('business_suggestions',[]), 'li-info', 'd-info')}
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Dishes + Complaints + Tags
    c5, c6 = st.columns(2, gap="medium")
    with c5:
        dishes = "".join(f'<span class="tag tag-green">{d}</span>' for d in analysis.get("best_dishes_mentioned",[]))
        st.markdown(f"""
        <div class="list-card">
            <div class="list-card-head"><div class="list-card-icon">🍛</div><div class="list-card-title">Best Dishes Mentioned</div></div>
            <div class="tag-row">{dishes or '<span style="color:#2A3E30;font-size:13px;">None mentioned</span>'}</div>
        </div>""", unsafe_allow_html=True)
    with c6:
        compl = "".join(f'<span class="tag tag-red">{c}</span>' for c in analysis.get("worst_complaints",[]))
        st.markdown(f"""
        <div class="list-card">
            <div class="list-card-head"><div class="list-card-icon">⚠️</div><div class="list-card-title">Worst Complaints</div></div>
            <div class="tag-row">{compl or '<span style="color:#2A3E30;font-size:13px;">None found</span>'}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    c7, c8 = st.columns(2, gap="medium")
    with c7:
        kw = "".join(f'<span class="tag">{k}</span>' for k in analysis.get("keywords",[]))
        st.markdown(f"""
        <div class="list-card">
            <div class="list-card-head"><div class="list-card-icon">🔑</div><div class="list-card-title">Keywords</div></div>
            <div class="tag-row">{kw}</div>
        </div>""", unsafe_allow_html=True)
    with c8:
        bf = "".join(f'<span class="tag tag-green">{b}</span>' for b in analysis.get("best_for",[]))
        st.markdown(f"""
        <div class="list-card">
            <div class="list-card-head"><div class="list-card-icon">👥</div><div class="list-card-title">Best For</div></div>
            <div class="tag-row">{bf}</div>
        </div>""", unsafe_allow_html=True)

    # Download
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    report = {
        "restaurant": place.get("name"),
        "address": place.get("formatted_address"),
        "google_rating": g_rating,
        "total_google_reviews": g_total,
        "fetched_reviews": reviews,
        "ai_analysis": analysis,
    }
    st.download_button(
        "⬇  Download full intelligence report as JSON",
        data=json.dumps(report, indent=2, ensure_ascii=False),
        file_name=f"{place.get('name','report').replace(' ','_')}_dishsense.json",
        mime="application/json",
    )
