import json
import re
import requests
import streamlit as st
from openai import OpenAI
from fpdf import FPDF
import io
import streamlit.components.v1 as components

st.set_page_config(
    page_title="DishSense AI — Restaurant Intelligence",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,.stApp{font-family:'Inter',sans-serif;background:#f2f2f7;color:#1c1c1e;}
.block-container{max-width:1100px!important;padding:0 1.5rem 4rem!important;}
.main>div{padding-top:0!important;}

/* ── Topbar ── */
.topbar{background:#fff;border-bottom:1px solid #e8e8e8;padding:0 4px;display:flex;align-items:center;justify-content:space-between;height:52px;margin-bottom:18px;}
.tb-logo{display:flex;align-items:center;gap:8px;}
.tb-icon{width:32px;height:32px;border-radius:9px;background:#FC8019;display:flex;align-items:center;justify-content:center;font-size:16px;}
.tb-name{font-size:16px;font-weight:800;color:#1c1c1e;letter-spacing:-0.02em;}
.tb-name span{color:#FC8019;}
.tb-loc{font-size:11px;color:#555;border:1px solid #e8e8e8;border-radius:6px;padding:4px 10px;background:#fafafa;}

/* ── Sidebar ── */
[data-testid="stSidebar"]{background:#fff;border-right:1px solid #ebebeb;}
[data-testid="stSidebar"]>div{padding-top:0!important;}
[data-testid="stSidebar"] *{color:#444!important;}
[data-testid="stSidebar"] label{font-size:10px!important;font-weight:700!important;color:#bbb!important;text-transform:uppercase!important;letter-spacing:0.1em!important;}
[data-testid="stSidebar"] .stSelectbox>div>div{background:#fafafa!important;border:1px solid #e8e8e8!important;border-radius:8px!important;font-size:12px!important;color:#444!important;}
[data-testid="stSidebar"] .stSlider [data-testid="stSliderThumb"]{background:#FC8019!important;}
[data-testid="stSidebar"] .stSlider [data-testid="stSliderTrackFill"]{background:#FC8019!important;}
[data-testid="stSidebar"] .stButton>button{background:#fff!important;color:#888!important;border:1px solid #e8e8e8!important;border-radius:8px!important;font-size:12px!important;font-weight:500!important;padding:0.4rem 1rem!important;width:100%!important;box-shadow:none!important;}
[data-testid="stSidebar"] .stButton>button:hover{background:#f5f5f5!important;color:#333!important;transform:none!important;box-shadow:none!important;}

.sb-brand{padding:18px 14px 14px;border-bottom:1px solid #ebebeb;margin-bottom:16px;}
.sb-icon{width:32px;height:32px;border-radius:9px;background:#FC8019;display:inline-flex;align-items:center;justify-content:center;font-size:16px;vertical-align:middle;}
.sb-name{display:inline-block;vertical-align:middle;margin-left:8px;font-size:14px;font-weight:800;color:#1c1c1e!important;letter-spacing:-0.02em;}
.sb-tag{font-size:9px;color:#bbb!important;text-transform:uppercase;letter-spacing:0.08em;margin-top:3px;}

/* ── Role selector ── */
.role-wrap{background:#fff;border:1px solid #e8e8e8;border-radius:14px;padding:18px;margin-bottom:14px;}
.role-title{font-size:14px;font-weight:700;color:#1c1c1e;margin-bottom:3px;}
.role-sub{font-size:11px;color:#aaa;margin-bottom:14px;}
.role-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.role-card{border:2px solid #e8e8e8;border-radius:12px;padding:14px;cursor:pointer;position:relative;transition:all .15s;}
.role-card.sel-owner{border-color:#FC8019;background:#fffaf6;}
.role-card.sel-user{border-color:#3b82f6;background:#f0f6ff;}
.role-icon{font-size:26px;margin-bottom:7px;}
.role-name{font-size:13px;font-weight:700;color:#1c1c1e;margin-bottom:3px;}
.role-desc{font-size:11px;color:#888;line-height:1.5;}
.role-feats{margin-top:9px;display:flex;flex-direction:column;gap:4px;}
.rf{font-size:10px;color:#666;display:flex;align-items:center;gap:5px;}
.rf-o{color:#FC8019;}
.rf-u{color:#3b82f6;}
.role-badge{position:absolute;top:10px;right:10px;font-size:9px;font-weight:700;padding:2px 7px;border-radius:4px;}
.rb-o{background:#fff5ee;color:#FC8019;border:1px solid #ffd9b8;}
.rb-u{background:#eff6ff;color:#3b82f6;border:1px solid #bfdbfe;}
.rb-idle{background:#f5f5f5;color:#aaa;border:1px solid #e8e8e8;}

/* ── Steps ── */
.steps{display:flex;align-items:center;gap:0;background:#fff;border:1px solid #e8e8e8;border-radius:10px;overflow:hidden;margin-bottom:14px;}
.st{flex:1;padding:9px 6px;font-size:10px;font-weight:600;color:#ccc;border-right:1px solid #f0f0f0;text-align:center;display:flex;align-items:center;justify-content:center;gap:4px;}
.st:last-child{border-right:none;}
.st.on{background:#fff5ee;color:#FC8019;}
.sn{width:16px;height:16px;border-radius:50%;background:#eee;font-size:9px;font-weight:700;line-height:16px;text-align:center;color:#bbb;flex-shrink:0;}
.st.on .sn{background:#FC8019;color:#fff;}

/* ── Search ── */
.stTextInput>div>div>input{background:#fff!important;border:1.5px solid #e8e8e8!important;border-radius:10px!important;font-size:14px!important;color:#1c1c1e!important;padding:11px 14px!important;font-family:'Inter',sans-serif!important;}
.stTextInput>div>div>input:focus{border-color:#FC8019!important;box-shadow:0 0 0 3px rgba(252,128,25,0.1)!important;}
.stTextInput>div>div>input::placeholder{color:#ccc!important;}

/* ── Main buttons ── */
.stButton>button{background:#FC8019!important;color:#fff!important;border:none!important;border-radius:10px!important;font-size:13px!important;font-weight:700!important;padding:0.65rem 1.4rem!important;box-shadow:0 2px 10px rgba(252,128,25,0.25)!important;transition:all .15s!important;}
.stButton>button:hover{background:#e8700a!important;box-shadow:0 4px 16px rgba(252,128,25,0.35)!important;transform:translateY(-1px)!important;}

/* ── Restaurant cards ── */
.rc{background:#fff;border:1px solid #e8e8e8;border-radius:12px;padding:13px 14px;margin-bottom:8px;display:flex;align-items:center;gap:11px;transition:border-color .15s,box-shadow .15s;}
.rc:hover{border-color:#FC8019;box-shadow:0 2px 12px rgba(252,128,25,0.1);}
.rc-img{width:46px;height:46px;border-radius:9px;background:#fff5ee;border:1px solid #ffd9b8;display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0;}
.rc-body{flex:1;}
.rc-name{font-size:13px;font-weight:700;color:#1c1c1e;margin-bottom:2px;}
.rc-addr{font-size:11px;color:#aaa;line-height:1.4;}
.rc-meta{display:flex;align-items:center;gap:7px;margin-top:5px;}
.rat{display:inline-flex;align-items:center;gap:3px;font-size:10px;font-weight:700;padding:2px 6px;border-radius:4px;color:#fff;}
.rat-hi{background:#48c479;}.rat-mid{background:#f59e0b;}.rat-lo{background:#ef4444;}
.rcount{font-size:11px;color:#bbb;}
.rbadge{font-size:10px;color:#FC8019;background:#fff5ee;border:1px solid #ffd9b8;padding:2px 7px;border-radius:4px;font-weight:600;}

/* ── Selected pill ── */
.sel-pill{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid #ffd9b8;border-radius:10px;padding:11px 14px;margin-bottom:14px;}
.sp-icon{width:36px;height:36px;border-radius:8px;background:#fff5ee;border:1px solid #ffd9b8;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;}
.sp-name{font-size:13px;font-weight:700;color:#1c1c1e;}
.sp-meta{font-size:11px;color:#aaa;margin-top:1px;}

/* ── Fetch section ── */
.fetch-section{background:#fff;border:1px solid #e8e8e8;border-radius:14px;padding:18px;margin-bottom:14px;}
.fetch-title{font-size:13px;font-weight:700;color:#1c1c1e;margin-bottom:4px;}
.fetch-sub{font-size:11px;color:#aaa;margin-bottom:14px;}
.fetch-role-label{font-size:11px;font-weight:600;color:#555;margin-bottom:10px;display:flex;align-items:center;gap:6px;}
.frl-badge{font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;}
.frl-o{background:#fff5ee;color:#FC8019;border:1px solid #ffd9b8;}
.frl-u{background:#eff6ff;color:#3b82f6;border:1px solid #bfdbfe;}

/* ── Verdict ── */
.verdict{background:#fff;border:1px solid #e8e8e8;border-radius:13px;padding:16px 18px;margin-bottom:12px;display:flex;gap:14px;align-items:stretch;}
.v-sc{background:#f8f8f8;border-radius:10px;padding:13px 17px;text-align:center;border:1px solid #ebebeb;flex-shrink:0;}
.vsn{font-size:36px;font-weight:900;color:#FC8019;letter-spacing:-0.04em;line-height:1;}
.vsd{font-size:12px;color:#ccc;}
.vst{font-size:12px;color:#FC8019;margin-top:2px;}
.v-sep{width:1px;background:#f0f0f0;flex-shrink:0;}
.v-mid{flex:1;padding:0 6px;}
.vsent{display:inline-flex;align-items:center;gap:3px;font-size:10px;font-weight:700;padding:3px 8px;border-radius:4px;margin-bottom:6px;}
.sp{background:#f0fbf4;color:#166534;}.sn2{background:#fef2f2;color:#991b1b;}.sm{background:#fff7ed;color:#c2410c;}.sn3{background:#f3f4f6;color:#374151;}
.vline{font-size:14px;font-weight:600;color:#1c1c1e;line-height:1.5;margin-bottom:3px;}
.vloc{font-size:11px;color:#bbb;}
.v-rt{display:flex;flex-direction:column;gap:6px;flex-shrink:0;justify-content:center;}
.vstat{background:#f8f8f8;border-radius:8px;padding:8px 12px;text-align:center;border:1px solid #ebebeb;}
.vsnum{font-size:17px;font-weight:800;color:#1c1c1e;}
.vslbl{font-size:9px;color:#bbb;text-transform:uppercase;letter-spacing:0.07em;}

/* ── Score cards ── */
.score-row{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:12px;}
.sc{background:#fff;border:1px solid #ebebeb;border-radius:10px;padding:11px 13px;}
.sc-icon{font-size:18px;margin-bottom:4px;}
.sc-lbl{font-size:9px;font-weight:600;color:#bbb;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:5px;}
.sc-val{font-size:18px;font-weight:800;color:#1c1c1e;}
.sc-den{font-size:10px;color:#ccc;}
.sc-bar{background:#f0f0f0;border-radius:999px;height:4px;margin-top:6px;overflow:hidden;}
.sc-fill{height:4px;border-radius:999px;}

/* ── Summary cards ── */
.owner-sum{background:#fff;border:1px solid #ffd9b8;border-left:3px solid #FC8019;border-radius:0 10px 10px 0;padding:13px 15px;margin-bottom:8px;}
.user-sum{background:#fff;border:1px solid #bfdbfe;border-left:3px solid #3b82f6;border-radius:0 10px 10px 0;padding:13px 15px;margin-bottom:8px;}
.sum-label{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:5px;}
.sum-text{font-size:12px;color:#555;line-height:1.75;}

/* ── List cards ── */
.two{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;}
.lc{background:#fff;border:1px solid #ebebeb;border-radius:10px;padding:12px;}
.lc-head{font-size:11px;font-weight:700;color:#333;margin-bottom:8px;padding-bottom:7px;border-bottom:1px solid #f5f5f5;display:flex;align-items:center;gap:5px;flex-wrap:wrap;}
.lc-badge{font-size:9px;padding:2px 6px;border-radius:4px;font-weight:600;}
.ob{background:#fff5ee;color:#FC8019;border:1px solid #ffd9b8;}
.ub{background:#eff6ff;color:#3b82f6;border:1px solid #bfdbfe;}
.li{display:flex;align-items:flex-start;gap:7px;padding:5px 8px;border-radius:7px;margin-bottom:3px;font-size:11px;line-height:1.55;}
.lg{background:#f0fbf4;color:#166534;border:1px solid #bbf7d0;}
.lr{background:#fef2f2;color:#991b1b;border:1px solid #fecaca;}
.ly{background:#fff7ed;color:#c2410c;border:1px solid #fed7aa;}
.lb{background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;}
.dot{width:5px;height:5px;border-radius:50%;margin-top:4px;flex-shrink:0;}
.dg{background:#22c55e;}.dr{background:#ef4444;}.dy{background:#f97316;}.db{background:#3b82f6;}
.trow{display:flex;flex-wrap:wrap;gap:5px;margin-top:5px;}
.tag{background:#f5f5f5;border:1px solid #e8e8e8;color:#555;font-size:11px;padding:3px 9px;border-radius:4px;font-weight:500;}
.tag-o{background:#fff5ee;border-color:#ffd9b8;color:#c2410c;}
.tag-r{background:#fef2f2;border-color:#fecaca;color:#b91c1c;}
.tag-g{background:#f0fbf4;border-color:#bbf7d0;color:#166534;}
.tag-b{background:#eff6ff;border-color:#bfdbfe;color:#1d4ed8;}

/* report tabs */
.rtabs{display:flex;gap:0;background:#fff;border:1px solid #e8e8e8;border-radius:10px;overflow:hidden;margin-bottom:12px;}
.rtab{flex:1;padding:9px 6px;font-size:11px;font-weight:600;color:#aaa;text-align:center;border-right:1px solid #f0f0f0;}
.rtab:last-child{border-right:none;}
.rtab.ton{background:#fff5ee;color:#FC8019;}

.div{height:1px;background:#ebebeb;margin:14px 0;}
.sec-head{font-size:14px;font-weight:700;color:#1c1c1e;margin-bottom:12px;display:flex;align-items:center;gap:8px;}
.sh-badge{font-size:11px;font-weight:500;color:#48c479;background:#f0fbf4;border:1px solid #c8efd8;padding:3px 9px;border-radius:999px;}
.stSpinner>div{border-top-color:#FC8019!important;}
.stDownloadButton button{background:#fff!important;border:1.5px solid #FC8019!important;border-radius:8px!important;font-size:12px!important;font-weight:600!important;color:#FC8019!important;padding:7px 16px!important;width:auto!important;box-shadow:none!important;}
.stDownloadButton button:hover{background:#fff5ee!important;}
</style>

<script>
function scrollToFetch() {
    setTimeout(function() {
        var el = document.getElementById('fetch-anchor');
        if (el) el.scrollIntoView({behavior: 'smooth', block: 'center'});
    }, 300);
}
</script>
""", unsafe_allow_html=True)


# ── Secrets ───────────────────────────────────────────────────────────────────
GROQ_KEY   = st.secrets["GROQ_API_KEY"]
PLACES_KEY = st.secrets["GOOGLE_PLACES_API_KEY"]
PLACES_BASE = "https://maps.googleapis.com/maps/api/place"


# ── Google Places ─────────────────────────────────────────────────────────────
def search_places(query):
    r = requests.get(f"{PLACES_BASE}/textsearch/json",
        params={"query": query + " restaurant", "type": "restaurant", "key": PLACES_KEY},
        timeout=10)
    r.raise_for_status()
    return r.json().get("results", [])[:8]

def get_place_details(place_id):
    r = requests.get(f"{PLACES_BASE}/details/json",
        params={"place_id": place_id,
                "fields": "name,rating,user_ratings_total,formatted_address,reviews,url",
                "key": PLACES_KEY, "reviews_sort": "newest"},
        timeout=10)
    r.raise_for_status()
    return r.json().get("result", {})


# ── Groq AI ───────────────────────────────────────────────────────────────────
def analyse_reviews(reviews, place_name, role, language, model, temp):
    client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")
    reviews_text = "\n\n".join([
        f"Reviewer: {r.get('author_name','?')}\nRating: {r.get('rating','?')}/5\nReview: {r.get('text','').strip()}"
        for r in reviews
    ])
    owner_fields = """
  "executive_summary": "2-3 sentence business summary for the owner",
  "owner_action_plan": "3 specific numbered steps the owner must take to improve ratings",
  "customer_pain_points": ["pain 1", "pain 2", "pain 3"],
  "business_suggestions": [
    {"suggestion": "specific fix", "priority": "High"},
    {"suggestion": "...", "priority": "Medium"},
    {"suggestion": "...", "priority": "Low"}
  ],
  "competitor_edge": "one sharp line on competitive position","""

    user_fields = """
  "visit_recommendation": "Should You Visit? Yes/No/Maybe — with one reason",
  "best_dishes_mentioned": ["dish 1", "dish 2", "dish 3"],
  "best_time_to_visit": ["weekday lunch", "early dinner"],
  "avoid_when": ["weekend rush", "rainy days"],
  "value_verdict": "one line on whether price is worth it","""

    prompt = f"""
Analyse these Google Maps reviews for: "{place_name}"
Role: {"Restaurant Owner — focus on business improvement" if role == "owner" else "Customer / Food Lover — focus on visit decision"}

REVIEWS:
{reviews_text}

Return ONLY this exact JSON:
{{
  "overall_sentiment": "Positive / Neutral / Negative / Mixed",
  "estimated_rating_out_of_5": 4.2,
  "one_line_verdict": "punchy one-liner",
  "food_quality_score": 8.2,
  "service_score": 7.1,
  "value_for_money_score": 6.5,
  "ambience_score": 7.8,
  "top_positives": [
    {{"point": "specific positive", "frequency": "X of Y reviewers"}},
    {{"point": "...", "frequency": "..."}},
    {{"point": "...", "frequency": "..."}}
  ],
  "top_negatives": [
    {{"point": "specific issue", "frequency": "X of Y reviewers"}},
    {{"point": "...", "frequency": "..."}},
    {{"point": "...", "frequency": "..."}}
  ],
  "keywords": ["word1", "word2", "word3", "word4", "word5"],
  "best_for": ["occasion 1", "occasion 2"],
  {owner_fields if role == "owner" else user_fields}
  "worst_complaints": ["complaint 1", "complaint 2"]
}}

Output language: {language}
Be specific — mention actual dishes, patterns, names from the reviews.
"""
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an elite restaurant analyst. Return ONLY valid JSON. No markdown."},
            {"role": "user", "content": prompt}
        ],
        temperature=temp,
    )
    text = resp.choices[0].message.content
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            return json.loads(m.group())
        raise ValueError("Could not parse JSON.")


# ── PDF generator ─────────────────────────────────────────────────────────────
def generate_pdf(place, analysis, role, reviews):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(252, 128, 25)
    pdf.cell(0, 10, "DishSense AI Report", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Role: {'Restaurant Owner' if role == 'owner' else 'Customer'}", ln=True)
    pdf.ln(4)

    # Restaurant info
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(28, 28, 30)
    pdf.cell(0, 8, place.get("name", ""), ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, place.get("formatted_address", ""), ln=True)
    pdf.cell(0, 5, f"Google Rating: {place.get('rating', '-')}/5  |  {place.get('user_ratings_total', 0):,} total reviews", ln=True)
    pdf.ln(4)

    # Divider
    pdf.set_draw_color(232, 232, 232)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    def section(title, color=(252, 128, 25)):
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*color)
        pdf.cell(0, 7, title, ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(60, 60, 60)

    def body(text):
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 5, str(text))
        pdf.ln(2)

    def bullet_list(items):
        for item in items:
            if isinstance(item, dict):
                text = item.get("point") or item.get("suggestion") or str(item)
                sub  = item.get("frequency") or item.get("priority") or ""
                pdf.cell(6, 5, chr(149), ln=False)
                pdf.multi_cell(0, 5, f"{text}" + (f" [{sub}]" if sub else ""))
            else:
                pdf.cell(6, 5, chr(149), ln=False)
                pdf.multi_cell(0, 5, str(item))
        pdf.ln(2)

    # Verdict
    section("AI Verdict")
    body(f"Overall Sentiment: {analysis.get('overall_sentiment','')}")
    body(f"AI Rating: {analysis.get('estimated_rating_out_of_5','')}/5")
    body(analysis.get("one_line_verdict", ""))

    # Scores
    section("Category Scores")
    body(f"Food Quality: {analysis.get('food_quality_score','-')}/10")
    body(f"Service: {analysis.get('service_score','-')}/10")
    body(f"Value for Money: {analysis.get('value_for_money_score','-')}/10")
    body(f"Ambience: {analysis.get('ambience_score','-')}/10")

    # Positives & Negatives
    section("Top Positives", (22, 163, 74))
    bullet_list(analysis.get("top_positives", []))
    section("Top Negatives", (220, 38, 38))
    bullet_list(analysis.get("top_negatives", []))

    if role == "owner":
        section("Executive Summary")
        body(analysis.get("executive_summary", ""))
        section("Owner Action Plan", (22, 163, 74))
        body(analysis.get("owner_action_plan", ""))
        section("Customer Pain Points", (249, 115, 22))
        bullet_list(analysis.get("customer_pain_points", []))
        section("Business Suggestions")
        bullet_list(analysis.get("business_suggestions", []))
        section("Competitive Edge")
        body(analysis.get("competitor_edge", ""))
    else:
        section("Visit Recommendation", (59, 130, 246))
        body(analysis.get("visit_recommendation", ""))
        section("Must-Try Dishes", (22, 163, 74))
        body(", ".join(analysis.get("best_dishes_mentioned", [])))
        section("Best Time to Visit", (59, 130, 246))
        body(", ".join(analysis.get("best_time_to_visit", [])))
        section("Avoid When", (220, 38, 38))
        body(", ".join(analysis.get("avoid_when", [])))
        section("Value Verdict")
        body(analysis.get("value_verdict", ""))

    section("Worst Complaints", (220, 38, 38))
    bullet_list(analysis.get("worst_complaints", []))
    section("Keywords")
    body(", ".join(analysis.get("keywords", [])))
    section("Best For")
    body(", ".join(analysis.get("best_for", [])))

    # Reviews
    pdf.add_page()
    section("Raw Reviews Analysed")
    for rev in reviews:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(28, 28, 30)
        pdf.cell(0, 5, f"{rev.get('author_name','?')} — {'★' * rev.get('rating',0)}", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 5, rev.get("text", "").strip()[:300])
        pdf.ln(2)

    return pdf.output(dest="S").encode("latin-1")


# ── Helpers ───────────────────────────────────────────────────────────────────
def star_str(r, n=5):
    try: f=round(float(r)); return "★"*f+"☆"*(n-f)
    except: return "★★★★☆"

def render_items(items, li_cls, dot_cls):
    h = ""
    for item in items:
        if isinstance(item, dict):
            text = item.get("point") or item.get("suggestion") or str(item)
            sub  = item.get("frequency") or item.get("priority") or ""
            h += f'<div class="li {li_cls}"><div class="dot {dot_cls}"></div><span>{text}'
            if sub: h += f' <span style="font-size:10px;opacity:0.6;margin-left:3px">· {sub}</span>'
            h += '</span></div>'
        else:
            h += f'<div class="li {li_cls}"><div class="dot {dot_cls}"></div><span>{item}</span></div>'
    return h

def rat_class(r):
    try:
        v = float(r)
        if v >= 4.2: return "rat-hi"
        if v >= 3.5: return "rat-mid"
        return "rat-lo"
    except: return "rat-mid"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div><span class="sb-icon">🍽️</span><span class="sb-name">DishSense AI</span></div>
        <div class="sb-tag">Restaurant Intelligence Platform</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("**AI Model**")
    model = st.selectbox("Model", ["llama-3.3-70b-versatile","llama-3.1-8b-instant","gemma2-9b-it"], index=0, label_visibility="collapsed")
    st.markdown("**Language**")
    language = st.selectbox("Language", ["English","Telugu","Tenglish","Hindi"], index=0, label_visibility="collapsed")
    st.markdown("**Temperature**")
    temperature = st.slider("Temp", 0.0, 1.0, 0.3, 0.1, label_visibility="collapsed")
    st.markdown("---")
    if st.button("🗑️ Clear & restart"):
        for k in ["results","selected","details","analysis","role"]:
            st.session_state.pop(k, None)
        st.rerun()
    st.markdown("""
    <div style="margin-top:16px;padding:12px;background:#fafafa;border:1px solid #ebebeb;border-radius:10px;">
        <div style="font-size:9px;font-weight:700;color:#bbb;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">How it works</div>
        <div style="font-size:11px;color:#aaa;line-height:2.1;">
        🔍 Search restaurant<br>👤 Choose your role<br>📍 Pick from results<br>📋 Fetch reviews<br>🤖 Groq AI analysis<br>📄 Download PDF
        </div>
    </div>
    <div style="margin-top:24px;padding:12px 14px;border-top:1px solid #ebebeb;text-align:center;">
        <div style="font-size:9px;color:#ccc;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:4px;">Designed by</div>
        <div style="font-size:13px;font-weight:700;color:#FC8019;letter-spacing:-0.01em;">Harsha Penmatsa</div>
    </div>""", unsafe_allow_html=True)


# ── Topbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="tb-logo">
        <div class="tb-icon">🍽️</div>
        <div class="tb-name">Dish<span>Sense</span> AI</div>
    </div>
    <div class="tb-loc">📍 Hyderabad, IN</div>
</div>""", unsafe_allow_html=True)


# ── Role selector ─────────────────────────────────────────────────────────────
role = st.session_state.get("role", None)

owner_sel = "sel-owner" if role == "owner" else ""
user_sel  = "sel-user"  if role == "user"  else ""
owner_badge = '<span class="role-badge rb-o">✓ Selected</span>' if role == "owner" else '<span class="role-badge rb-idle">Tap to select</span>'
user_badge  = '<span class="role-badge rb-u">✓ Selected</span>' if role == "user"  else '<span class="role-badge rb-idle">Tap to select</span>'

st.markdown(f"""
<div class="role-wrap">
    <div class="role-title">Who is using DishSense AI today?</div>
    <div class="role-sub">Select your role to get a personalised analysis report</div>
    <div class="role-grid">
        <div class="role-card {owner_sel}">
            {owner_badge}
            <div class="role-icon">🏪</div>
            <div class="role-name">Restaurant Owner</div>
            <div class="role-desc">Deep business intelligence to improve ratings and operations</div>
            <div class="role-feats">
                <div class="rf rf-o">✓ Owner action plan</div>
                <div class="rf rf-o">✓ Business suggestions + priority</div>
                <div class="rf rf-o">✓ Pain point analysis</div>
                <div class="rf rf-o">✓ Competitive edge report</div>
                <div class="rf rf-o">✓ Download as PDF</div>
            </div>
        </div>
        <div class="role-card {user_sel}">
            {user_badge}
            <div class="role-icon">👤</div>
            <div class="role-name">Customer / Food Lover</div>
            <div class="role-desc">Find out if this restaurant is worth visiting based on real reviews</div>
            <div class="role-feats">
                <div class="rf rf-u">✓ Should I visit? verdict</div>
                <div class="rf rf-u">✓ Must-try dishes</div>
                <div class="rf rf-u">✓ Best time to visit</div>
                <div class="rf rf-u">✓ Value for money verdict</div>
                <div class="rf rf-u">✓ Download as PDF</div>
            </div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

col_o, col_u = st.columns(2)
with col_o:
    if st.button("🏪  I'm a Restaurant Owner", use_container_width=True):
        st.session_state["role"] = "owner"
        st.rerun()
with col_u:
    if st.button("👤  I'm a Customer / Food Lover", use_container_width=True):
        st.session_state["role"] = "user"
        st.rerun()

if not role:
    st.info("👆 Please select your role above to continue.")
    st.stop()


# ── Step indicator ────────────────────────────────────────────────────────────
step = 1
if "results"  in st.session_state: step = 2
if "selected" in st.session_state: step = 3
if "analysis" in st.session_state: step = 4

st.markdown(f"""
<div class="steps">
    <div class="st {'on' if step>=1 else ''}"><div class="sn">1</div> Search</div>
    <div class="st {'on' if step>=2 else ''}"><div class="sn">2</div> Pick Restaurant</div>
    <div class="st {'on' if step>=3 else ''}"><div class="sn">3</div> Fetch Reviews</div>
    <div class="st {'on' if step>=4 else ''}"><div class="sn">4</div> View Report</div>
</div>""", unsafe_allow_html=True)


# ══ STEP 1 — Search ══════════════════════════════════════════════════════════
st.markdown('<div style="font-size:10px;font-weight:700;color:#bbb;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:7px;">Search Restaurant</div>', unsafe_allow_html=True)
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
                    st.error("No results found. Try adding the city name.")
                else:
                    st.session_state["results"] = res
                    for k in ["selected","details","analysis"]:
                        st.session_state.pop(k, None)
                    st.rerun()
            except Exception as e:
                st.error(f"Search error: {e}")


# ══ STEP 2 — Pick ═════════════════════════════════════════════════════════════
if "results" in st.session_state:
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
    results = st.session_state["results"]
    st.markdown(f'<div style="font-size:10px;font-weight:700;color:#bbb;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">{len(results)} restaurants found — click a name to select</div>', unsafe_allow_html=True)

    for i, p in enumerate(results):
        rc = rat_class(p.get("rating"))
        col_card, col_btn = st.columns([6,1], gap="small")
        with col_card:
            st.markdown(f"""
            <div class="rc">
                <div class="rc-img">🍛</div>
                <div class="rc-body">
                    <div class="rc-name">{p.get('name','')}</div>
                    <div class="rc-addr">{p.get('formatted_address','')}</div>
                    <div class="rc-meta">
                        <div class="rat {rc}">★ {p.get('rating','–')}</div>
                        <div class="rcount">{p.get('user_ratings_total',0):,} reviews</div>
                        <div class="rbadge">Dine-in · Delivery</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
        with col_btn:
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            if st.button("Select ›", key=f"sel_{i}"):
                st.session_state["selected"] = p
                for k in ["details","analysis"]:
                    st.session_state.pop(k, None)
                st.session_state["do_scroll"] = True
                st.rerun()


# ══ STEP 3 — Fetch ════════════════════════════════════════════════════════════
if "selected" in st.session_state:
    p = st.session_state["selected"]
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    # Anchor + auto-scroll
    st.markdown('<div id="fetch-anchor"></div>', unsafe_allow_html=True)
    if st.session_state.pop("do_scroll", False):
        components.html("""
        <script>
            window.parent.document.getElementById('fetch-anchor').scrollIntoView({behavior:'smooth',block:'center'});
        </script>
        """, height=0)

    # Selected restaurant pill
    st.markdown(f"""
    <div class="sel-pill">
        <div class="sp-icon">🍛</div>
        <div>
            <div class="sp-name">{p.get('name','')}</div>
            <div class="sp-meta">★ {p.get('rating','–')} · {p.get('user_ratings_total',0):,} reviews · {p.get('formatted_address','')[:55]}…</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Fetch section
    role_label = "Restaurant Owner" if role == "owner" else "Customer / Food Lover"
    role_badge_cls = "frl-o" if role == "owner" else "frl-u"
    role_icon = "🏪" if role == "owner" else "👤"

    st.markdown(f"""
    <div class="fetch-section">
        <div class="fetch-title">Ready to analyse "{p.get('name','')}"</div>
        <div class="fetch-sub">Live Google reviews will be fetched and analysed by Groq AI — takes about 10 seconds</div>
        <div class="fetch-role-label">
            {role_icon} Viewing as: <strong>{role_label}</strong>
            <span class="frl-badge {role_badge_cls}">{role_label}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # Fetch buttons
    if role == "owner":
        col1, col2 = st.columns(2, gap="small")
        with col1:
            fetch_full = st.button("📊  Full Business Report", use_container_width=True)
        with col2:
            fetch_quick = st.button("⚡  Quick Pain Points Scan", use_container_width=True)
        fetch_any = fetch_full or fetch_quick
    else:
        col1, col2 = st.columns(2, gap="small")
        with col1:
            fetch_full = st.button("🍽️  Should I Visit? Full Report", use_container_width=True)
        with col2:
            fetch_quick = st.button("🍛  Best Dishes & Quick Tips", use_container_width=True)
        fetch_any = fetch_full or fetch_quick

    if fetch_any:
        with st.spinner("Fetching live reviews from Google…"):
            try:
                details = get_place_details(p["place_id"])
                st.session_state["details"] = details
                reviews = details.get("reviews", [])
                if not reviews:
                    st.error("No reviews found for this restaurant on Google Maps.")
                    st.stop()
            except Exception as e:
                st.error(f"Could not fetch reviews: {e}")
                st.stop()

        with st.spinner(f"Groq AI is generating your {'business' if role == 'owner' else 'customer'} report…"):
            try:
                analysis = analyse_reviews(reviews, p.get("name",""), role, language, model, temperature)
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
    role     = st.session_state.get("role", "owner")

    st.markdown('<div class="div"></div>', unsafe_allow_html=True)

    sentiment = analysis.get("overall_sentiment","N/A")
    s_map = {"positive":"sp","negative":"sn2","mixed":"sm","neutral":"sn3"}
    s_cls = s_map.get(sentiment.lower(), "sn3")
    rating   = analysis.get("estimated_rating_out_of_5","–")
    verdict  = analysis.get("one_line_verdict","")
    g_rating = place.get("rating","–")
    g_total  = place.get("user_ratings_total",0)

    # Report header
    role_color = "#FC8019" if role == "owner" else "#3b82f6"
    role_label = "Owner Business Report" if role == "owner" else "Customer Visit Report"
    st.markdown(f"""
    <div class="sec-head">
        AI {role_label}
        <span class="sh-badge">✓ {len(reviews)} reviews analysed</span>
    </div>""", unsafe_allow_html=True)

    # Verdict
    st.markdown(f"""
    <div class="verdict">
        <div class="v-sc">
            <div class="vsn">{rating}</div>
            <div class="vsd">/5</div>
            <div class="vst">{star_str(rating)}</div>
            <div style="font-size:9px;color:#bbb;text-transform:uppercase;letter-spacing:0.07em;margin-top:3px;">AI Score</div>
        </div>
        <div class="v-sep"></div>
        <div class="v-mid">
            <div class="vsent {s_cls}">{sentiment}</div>
            <div class="vline">{verdict}</div>
            <div class="vloc">{place.get('name','')} · {place.get('formatted_address','')[:60]}</div>
        </div>
        <div class="v-sep"></div>
        <div class="v-rt">
            <div class="vstat"><div class="vsnum" style="color:#FC8019;">{g_rating}</div><div class="vslbl">Google avg</div></div>
            <div class="vstat"><div class="vsnum" style="font-size:14px;">{g_total:,}</div><div class="vslbl">Reviews</div></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # Scores
    food_s = analysis.get("food_quality_score",0)
    svc_s  = analysis.get("service_score",0)
    val_s  = analysis.get("value_for_money_score",0)
    amb_s  = analysis.get("ambience_score",0)

    st.markdown(f"""
    <div class="score-row">
        <div class="sc"><div class="sc-icon">🍛</div><div class="sc-lbl">Food Quality</div><div><span class="sc-val">{food_s}</span><span class="sc-den">/10</span></div><div class="sc-bar"><div class="sc-fill" style="width:{float(food_s)*10:.0f}%;background:#FC8019;"></div></div></div>
        <div class="sc"><div class="sc-icon">🤝</div><div class="sc-lbl">Service</div><div><span class="sc-val">{svc_s}</span><span class="sc-den">/10</span></div><div class="sc-bar"><div class="sc-fill" style="width:{float(svc_s)*10:.0f}%;background:#3b82f6;"></div></div></div>
        <div class="sc"><div class="sc-icon">💰</div><div class="sc-lbl">Value</div><div><span class="sc-val">{val_s}</span><span class="sc-den">/10</span></div><div class="sc-bar"><div class="sc-fill" style="width:{float(val_s)*10:.0f}%;background:#22c55e;"></div></div></div>
        <div class="sc"><div class="sc-icon">✨</div><div class="sc-lbl">Ambience</div><div><span class="sc-val">{amb_s}</span><span class="sc-den">/10</span></div><div class="sc-bar"><div class="sc-fill" style="width:{float(amb_s)*10:.0f}%;background:#a855f7;"></div></div></div>
    </div>""", unsafe_allow_html=True)

    # Role-specific summaries
    if role == "owner":
        st.markdown(f"""
        <div class="owner-sum">
            <div class="sum-label" style="color:#FC8019;">🏪 Executive Summary</div>
            <div class="sum-text">{analysis.get("executive_summary","–")}</div>
        </div>
        <div class="owner-sum" style="border-left-color:#22c55e;">
            <div class="sum-label" style="color:#16a34a;">🎯 Owner Action Plan</div>
            <div class="sum-text">{analysis.get("owner_action_plan","–")}</div>
        </div>
        <div class="owner-sum" style="border-left-color:#6366f1;">
            <div class="sum-label" style="color:#4f46e5;">⚡ Competitive Edge</div>
            <div class="sum-text">{analysis.get("competitor_edge","–")}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="user-sum">
            <div class="sum-label" style="color:#3b82f6;">👤 Should You Visit?</div>
            <div class="sum-text">{analysis.get("visit_recommendation","–")}</div>
        </div>
        <div class="user-sum" style="border-left-color:#22c55e;">
            <div class="sum-label" style="color:#16a34a;">💰 Value Verdict</div>
            <div class="sum-text">{analysis.get("value_verdict","–")}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Positives & Negatives
    c1, c2 = st.columns(2, gap="small")
    with c1:
        st.markdown(f"""<div class="lc"><div class="lc-head">✅ Top Positives <span class="lc-badge ob">Owner</span><span class="lc-badge ub" style="margin-left:2px">User</span></div>{render_items(analysis.get('top_positives',[]),'lg','dg')}</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="lc"><div class="lc-head">❌ Top Negatives <span class="lc-badge ob">Owner</span><span class="lc-badge ub" style="margin-left:2px">User</span></div>{render_items(analysis.get('top_negatives',[]),'lr','dr')}</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if role == "owner":
        c3, c4 = st.columns(2, gap="small")
        with c3:
            st.markdown(f"""<div class="lc"><div class="lc-head">😟 Pain Points <span class="lc-badge ob">Owner</span></div>{render_items(analysis.get('customer_pain_points',[]),'ly','dy')}</div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="lc"><div class="lc-head">💡 Suggestions <span class="lc-badge ob">Owner</span></div>{render_items(analysis.get('business_suggestions',[]),'lb','db')}</div>""", unsafe_allow_html=True)
    else:
        c3, c4 = st.columns(2, gap="small")
        with c3:
            dishes = "".join(f'<span class="tag tag-o">{d}</span>' for d in analysis.get("best_dishes_mentioned",[]))
            st.markdown(f"""<div class="lc"><div class="lc-head">🍛 Must-Try Dishes <span class="lc-badge ub">User</span></div><div class="trow">{dishes}</div></div>""", unsafe_allow_html=True)
        with c4:
            best = "".join(f'<span class="tag tag-g">{t}</span>' for t in analysis.get("best_time_to_visit",[]))
            avoid = "".join(f'<span class="tag tag-r">{t}</span>' for t in analysis.get("avoid_when",[]))
            st.markdown(f"""<div class="lc"><div class="lc-head">📅 When to Go <span class="lc-badge ub">User</span></div><div class="trow">{best}{avoid}</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    c5, c6 = st.columns(2, gap="small")
    with c5:
        compl = "".join(f'<span class="tag tag-r">{c}</span>' for c in analysis.get("worst_complaints",[]))
        st.markdown(f"""<div class="lc"><div class="lc-head">⚠️ Worst Complaints <span class="lc-badge ob">Owner</span><span class="lc-badge ub" style="margin-left:2px">User</span></div><div class="trow">{compl}</div></div>""", unsafe_allow_html=True)
    with c6:
        kw = "".join(f'<span class="tag">{k}</span>' for k in analysis.get("keywords",[]))
        bf = "".join(f'<span class="tag tag-g">{b}</span>' for b in analysis.get("best_for",[]))
        st.markdown(f"""<div class="lc"><div class="lc-head">🔑 Keywords · 👥 Best For</div><div class="trow">{kw}{bf}</div></div>""", unsafe_allow_html=True)

    # Raw reviews expander
    with st.expander(f"📋  View {len(reviews)} raw Google reviews"):
        for rev in reviews:
            stars = "★"*rev.get("rating",0)+"☆"*(5-rev.get("rating",0))
            st.markdown(f"""
            <div style="background:#fafafa;border:1px solid #ebebeb;border-radius:10px;padding:12px 14px;margin-bottom:8px;">
                <div style="font-size:12px;font-weight:700;color:#1c1c1e;margin-bottom:2px;">{rev.get('author_name','Anonymous')}</div>
                <div style="font-size:12px;color:#FC8019;margin-bottom:5px;">{stars}</div>
                <div style="font-size:12px;color:#555;line-height:1.65;">{rev.get('text','').strip()}</div>
                <div style="font-size:10px;color:#bbb;margin-top:5px;">{rev.get('relative_time_description','')}</div>
            </div>""", unsafe_allow_html=True)

    # ── Downloads ──
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:10px;font-weight:700;color:#bbb;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Download Report</div>', unsafe_allow_html=True)

    dl1, dl2 = st.columns(2, gap="small")

    with dl1:
        try:
            pdf_bytes = generate_pdf(place, analysis, role, reviews)
            fname = f"{place.get('name','report').replace(' ','_')}_dishsense.pdf"
            st.download_button(
                f"📄  Download {'Owner Business' if role == 'owner' else 'Customer Visit'} Report (PDF)",
                data=pdf_bytes,
                file_name=fname,
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"PDF error: {e}")

    with dl2:
        report_json = {
            "restaurant": place.get("name"),
            "address": place.get("formatted_address"),
            "google_rating": g_rating,
            "total_google_reviews": g_total,
            "role": role,
            "ai_analysis": analysis,
            "fetched_reviews": reviews,
        }
        st.download_button(
            "📦  Download Raw Data (JSON)",
            data=json.dumps(report_json, indent=2, ensure_ascii=False),
            file_name=f"{place.get('name','report').replace(' ','_')}_data.json",
            mime="application/json",
            use_container_width=True,
        )
