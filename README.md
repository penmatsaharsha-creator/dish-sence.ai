# 🍽️ Restaurant Review Analyser
### Google Places + Grok AI · Built with Streamlit

Search any restaurant → fetch live Google reviews → get a full AI-powered business report analysing positives, negatives, pain points, category scores, dish mentions, and actionable suggestions.

---

## Features

| Feature | Detail |
|---------|--------|
| 🔍 Live search | Find any restaurant via Google Places API |
| 📋 Real reviews | Fetch actual Google Maps customer reviews |
| 🤖 AI analysis | Grok (xAI) analyses every review |
| 📊 Category scores | Food, Service, Value, Ambience rated /10 |
| ✅ Positives & ❌ Negatives | With frequency indicators |
| 😟 Pain points | What customers complain about most |
| 💡 Business suggestions | Actionable fixes with priority labels |
| 🍛 Best dishes | Specific dishes mentioned positively |
| ⚠️ Worst complaints | Specific recurring issues |
| 📥 JSON export | Download the full report |
| 🌐 Multi-language | English / Telugu / Tenglish output |

---

## Project Structure

```
zomato_review_analyser/
├── app.py                   ← Main Streamlit app
├── requirements.txt         ← Python dependencies
├── .gitignore               ← Keeps secrets out of GitHub
├── README.md                ← This file
└── .streamlit/
    └── secrets.toml         ← LOCAL ONLY — your API keys (never commit)
```

---

## Setup — Two API Keys Needed

### 1. Grok API Key (xAI)
1. Go to https://console.x.ai
2. Sign up / log in
3. Create an API key
4. Copy it — starts with `xai-...`

### 2. Google Places API Key
1. Go to https://console.cloud.google.com
2. Create a new project (or use existing)
3. Go to **APIs & Services → Library**
4. Enable **Places API** (search for "Places API")
5. Go to **APIs & Services → Credentials**
6. Click **Create Credentials → API Key**
7. Copy the key — starts with `AIza...`
8. (Optional but recommended) Restrict key to Places API only

> **Free tier:** Google gives $200/month credit. Each Places Details call (fetching reviews) costs ~$0.017. That's ~11,700 free lookups/month.

---

## Local Development

### Install dependencies
```bash
pip install -r requirements.txt
```

### Add your keys
Edit `.streamlit/secrets.toml`:
```toml
XAI_API_KEY = "xai-your-actual-key"
GOOGLE_PLACES_API_KEY = "AIza-your-actual-key"
```

### Run
```bash
streamlit run app.py
```
Open http://localhost:8501

---

## Deploy to Streamlit Community Cloud (Free)

### Step 1 — Push to GitHub
```bash
# Make sure secrets.toml is NOT included
git add app.py requirements.txt .gitignore README.md
git commit -m "Initial deploy"
git push origin main
```

### Step 2 — Deploy
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click **New app**
4. Select your repo, branch `main`, file `app.py`
5. Click **Deploy**

### Step 3 — Add secrets in Streamlit Cloud
After deploy → **App menu (⋮) → Settings → Secrets**

Paste this and click **Save**:
```toml
XAI_API_KEY = "xai-your-actual-key"
GOOGLE_PLACES_API_KEY = "AIza-your-actual-key"
```

App restarts automatically. Your keys are hidden — users never see them.

---

## How to Use

1. **Search** — type a restaurant name + city (e.g. "Paradise Biryani Hyderabad")
2. **Pick** — select the correct restaurant from results
3. **Fetch** — click "Fetch reviews & analyse"
4. **Read** — view the full AI report with scores, positives, negatives, suggestions
5. **Download** — export the full JSON report

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | UI framework |
| [Google Places API](https://developers.google.com/maps/documentation/places/web-service) | Live restaurant search + reviews |
| [Grok / xAI](https://x.ai) | AI analysis engine |
| [OpenAI Python SDK](https://github.com/openai/openai-python) | API client (xAI-compatible) |

---

## Grok Models

| Model | Speed | Best for |
|-------|-------|----------|
| `grok-3-mini` | ⚡ Fast | Daily use, stable output |
| `grok-3` | 🔄 Balanced | Richer analysis |
| `grok-2-1212` | 🔍 Thorough | Deep detailed reports |
