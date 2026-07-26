# SBSBY! — SUPER BOWL! SUPER BROWNS! YEAH!

**Cleveland Browns · Cleveland Guardians · Cleveland Cavaliers · Ohio State Football · Ohio State Men's Basketball**

Production Streamlit sports hub with **near real-time polling**, multi-source failover, optional betting odds, Plotly trends, and premium team-themed UI (light + dark).

---

## Features (v2)

| Area | Details |
|------|---------|
| **Live scores** | ESPN primary → TheSportsDB fallback; live pulse badge; optional in-card lines |
| **Real-time feel** | Configurable auto-poll (15–90s) via `streamlit-autorefresh` |
| **Betting odds** | Optional [The Odds API](https://the-odds-api.com/) (moneyline, spreads, totals) |
| **News / standings / schedule** | Failover + empty-state UI (never hard-crashes) |
| **Trends** | Recent form table + Plotly scoring chart |
| **Prediction markets** | Deep links: Polymarket, Kalshi, ESPN |
| **UI** | Team colors, light eye-friendly tones, dark mode, Outfit + JetBrains Mono |
| **Resilience** | Retries (`tenacity`), short TTL cache, static fallbacks for missing team data |

---

## Quick start (local)

```bash
cd sbsby
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Optional odds key

1. Free tier: https://the-odds-api.com/ (500 requests/month)
2. Either:
   - Paste key in the **sidebar**, or
   - Set environment variable `ODDS_API_KEY`, or
   - On Streamlit Cloud: **App settings → Secrets**:

```toml
ODDS_API_KEY = "your_key_here"
```

---

## Deploy to Streamlit Community Cloud

1. Push the **`sbsby`** folder contents to a **public** GitHub repo (root of repo = files below).
2. Visit [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Settings:
   - **Main file path:** `app.py`
   - Python 3.11+ recommended
4. (Optional) Add `ODDS_API_KEY` under Secrets.
5. Deploy → `https://<your-app>.streamlit.app`

---

## Project layout

```
sbsby/
├── app.py                 # Main dashboard
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
└── utils/
    ├── __init__.py
    ├── api_client.py      # Multi-source client + odds
    └── theme.py           # Dynamic CSS
```

---

## Data sources

| Priority | Source | Use |
|----------|--------|-----|
| 1 | ESPN site API (no key) | Scores, news, standings, schedule, team info |
| 2 | TheSportsDB | Team meta + events fallback |
| Optional | The Odds API | H2H / spreads / totals |
| Links | Polymarket, Kalshi | Prediction markets |

Missing data is handled with empty states and static team fallbacks so the app stays usable off-season or during outages.

---

## Notes on “WebSocket” / real-time

Browser Streamlit apps cannot hold arbitrary external WebSockets as easily as a custom backend. This build uses **aggressive, configurable HTTP polling** (default 30s) plus cache invalidation for a live experience without a separate server. For true push WebSockets you would pair this UI with a small FastAPI/Node worker — not required for share.streamlit.io.

---

## Disclaimer

Unofficial fan project. Not affiliated with the NFL, MLB, NBA, Cleveland teams, or The Ohio State University. Public endpoints may change; failover keeps the UI resilient. Betting/prediction links are external — follow local laws.

**SBSBY!** · SUPER BOWL! SUPER BROWNS! YEAH!
