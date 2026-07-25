import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="SBSBY!",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded",
)

TEAM_CONFIG = {
    "Cleveland Browns": {
        "score_url": "https://www.nfl.com/teams/cleveland-browns/",
        "news_url": "https://www.nfl.com/teams/cleveland-browns/",
        "history_url": "https://www.nfl.com/teams/cleveland-browns/",
        "type": "nfl",
        "theme": {
            "primary": "#FF7300",
            "secondary": "#4C230A",
            "accent": "#FFFFFF",
        },
    },
    "Cleveland Guardians": {
        "score_url": "https://www.espn.com/mlb/team/_/name/cle/cleveland-guardians",
        "news_url": "https://www.espn.com/mlb/team/_/name/cle/cleveland-guardians",
        "history_url": "https://www.espn.com/mlb/team/_/name/cle/cleveland-guardians",
        "type": "mlb",
        "theme": {
            "primary": "#FF7300",
            "secondary": "#4C230A",
            "accent": "#FFFFFF",
        },
    },
    "Cleveland Cavaliers": {
        "score_url": "https://www.espn.com/nba/team/_/name/cle/cleveland-cavaliers",
        "news_url": "https://www.espn.com/nba/team/_/name/cle/cleveland-cavaliers",
        "history_url": "https://www.espn.com/nba/team/_/name/cle/cleveland-cavaliers",
        "type": "nba",
        "theme": {
            "primary": "#FF7300",
            "secondary": "#4C230A",
            "accent": "#FFFFFF",
        },
    },
    "Ohio State Football": {
        "score_url": "https://ohiostatebuckeyes.com/sports/football",
        "news_url": "https://ohiostatebuckeyes.com/sports/football",
        "history_url": "https://ohiostatebuckeyes.com/sports/football",
        "type": "ncaaf",
        "theme": {
            "primary": "#CE202F",
            "secondary": "#666666",
            "accent": "#FFFFFF",
        },
    },
    "Ohio State Men's Basketball": {
        "score_url": "https://ohiostatebuckeyes.com/sports/mens-basketball",
        "news_url": "https://ohiostatebuckeyes.com/sports/mens-basketball",
        "history_url": "https://ohiostatebuckeyes.com/sports/mens-basketball",
        "type": "ncaab",
        "theme": {
            "primary": "#CE202F",
            "secondary": "#666666",
            "accent": "#FFFFFF",
        },
    },
}

MARKET_LINKS = [
    ("Polymarket", "https://polymarket.com/"),
    ("Kalshi", "https://kalshi.com/"),
    ("Manifold", "https://manifold.markets/"),
]

st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
    }
    .stApp {
        background: linear-gradient(180deg, #1C1208 0%, #0F0A06 100%);
        color: #F8F1E7;
    }
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }
    [data-testid="stSidebar"] {
        background: #24160D;
    }
    .hero {
        background: linear-gradient(135deg, rgba(255,115,0,0.18), rgba(76,35,10,0.92));
        border: 1px solid rgba(255,115,0,0.35);
        border-radius: 18px;
        padding: 1.2rem 1.2rem 0.9rem 1.2rem;
        margin-bottom: 1rem;
    }
    .card {
        background: rgba(42, 27, 16, 0.92);
        border: 1px solid rgba(255,115,0,0.28);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .small-muted {
        color: #C9B8A6;
        font-size: 0.92rem;
    }
    a {
        color: #FFB366 !important;
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1 style="margin-bottom: 0.25rem;">SBSBY!</h1>
        <p style="margin-top: 0; margin-bottom: 0.2rem;">
            Cleveland sports hub for scores, news, stats, trends, history, and prediction-market links.
        </p>
        <p class="small-muted" style="margin-top: 0;">
            Browns-inspired theme. Built for fast switching between teams and sections.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Controls")
    selected_team = st.selectbox("Choose a team", list(TEAM_CONFIG.keys()))
    view = st.radio(
        "View",
        ["Overview", "Scores", "News", "Stats", "History", "Markets"],
        index=0,
    )
    st.divider()
    st.caption("Theme")
    st.write(f"Primary: {TEAM_CONFIG[selected_team]['theme']['primary']}")
    st.write(f"Secondary: {TEAM_CONFIG[selected_team]['theme']['secondary']}")
    st.divider()
    st.link_button("Streamlit Cloud", "https://share.streamlit.io/")
    st.link_button("GitHub", "https://github.com/")

cfg = TEAM_CONFIG[selected_team]


@st.cache_data(ttl=300)
def fetch_html(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        return requests.get(url, headers=headers, timeout=15).text
    except Exception:
        return ""


@st.cache_data(ttl=300)
def extract_links(url: str, max_links: int = 15) -> pd.DataFrame:
    html = fetch_html(url)
    if not html:
        return pd.DataFrame(columns=["Title", "URL"])
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for a in soup.select("a"):
        title = " ".join(a.get_text(" ", strip=True).split())
        href = a.get("href")
        if not title or not href:
            continue
        if href.startswith("/"):
            href = requests.compat.urljoin(url, href)
        if len(title) >= 18:
            rows.append({"Title": title, "URL": href})
    df = pd.DataFrame(rows).drop_duplicates().head(max_links)
    if df.empty:
        return pd.DataFrame(columns=["Title", "URL"])
    return df


@st.cache_data(ttl=300)
def quick_stats(team: str) -> pd.DataFrame:
    if team == "Cleveland Browns":
        data = [
            ("Club colors", "Brown, orange, white"),
            ("League", "NFL"),
            ("Focus", "Roster, schedule, depth, trends"),
            ("History", "Founded in 1946"),
        ]
    elif team == "Cleveland Guardians":
        data = [
            ("League", "MLB"),
            ("Focus", "Standings, batting, pitching, lineup trends"),
            ("History", "Cleveland MLB franchise"),
            ("Use case", "Scores, articles, seasonal stats"),
        ]
    elif team == "Cleveland Cavaliers":
        data = [
            ("League", "NBA"),
            ("Focus", "Efficiency, scoring, playoff form"),
            ("History", "Cleveland NBA franchise"),
            ("Use case", "Scores, player trends, team momentum"),
        ]
    elif team == "Ohio State Football":
        data = [
            ("Colors", "Scarlet and gray"),
            ("League", "NCAA Football"),
            ("Focus", "Rankings, recruits, game previews"),
            ("History", "Long-running powerhouse program"),
        ]
    else:
        data = [
            ("Colors", "Scarlet and gray"),
            ("League", "NCAA Basketball"),
            ("Focus", "Rosters, results, season trends"),
            ("History", "Major college basketball program"),
        ]
    return pd.DataFrame(data, columns=["Stat", "Value"])


def render_links(df: pd.DataFrame):
    if df.empty:
        st.info("No links could be extracted from the source page.")
        return
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_markets():
    st.subheader("Prediction markets")
    st.write("These are general public links now; you can swap in team-specific event pages later.")
    cols = st.columns(3)
    for i, (name, url) in enumerate(MARKET_LINKS):
        with cols[i % 3]:
            st.link_button(name, url)


if view == "Overview":
    left, right = st.columns([1.4, 1])
    with left:
        st.markdown(
            f"""
            <div class="card">
                <h3>{selected_team}</h3>
                <p>Central hub for live scores, news articles, stats, historical information, and market links.</p>
                <p class="small-muted">Use the sidebar to jump between sections and switch teams instantly.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button("Open team source page", cfg["score_url"])
        st.link_button("Open news source page", cfg["news_url"])
    with right:
        st.markdown(
            """
            <div class="card">
                <h4>Dynamic features</h4>
                <ul>
                    <li>Source-linked scores and news pages</li>
                    <li>Clickable article extraction</li>
                    <li>Stats snapshots</li>
                    <li>Prediction-market links</li>
                    <li>Historical team context</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.subheader("Trending links")
    render_links(extract_links(cfg["news_url"]))

elif view == "Scores":
    st.subheader("Scores and schedules")
    html = fetch_html(cfg["score_url"])
    if html:
        text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
        st.write(text[:8000])
    else:
        st.warning("Unable to retrieve the source page right now.")
    st.link_button("Open live source", cfg["score_url"])

elif view == "News":
    st.subheader("News articles")
    st.caption("This section extracts link text from the source page. You can later replace it with dedicated news APIs.")
    render_links(extract_links(cfg["news_url"]))

elif view == "Stats":
    st.subheader("Stats snapshot")
    st.dataframe(quick_stats(selected_team), use_container_width=True, hide_index=True)
    st.subheader("More source links")
    render_links(extract_links(cfg["score_url"]))

elif view == "History":
    st.subheader("Historical information")
    history_text = {
        "Cleveland Browns": "The Browns are a Cleveland NFL franchise founded in 1946. Their official club colors are brown, orange, and white.",
        "Cleveland Guardians": "The Guardians are Cleveland's MLB franchise, with public team pages for scores, highlights, standings, and season context.",
        "Cleveland Cavaliers": "The Cavaliers are Cleveland's NBA franchise, with playoff history and strong player-trend coverage on public sports pages.",
        "Ohio State Football": "Ohio State football uses scarlet and gray and has one of the most recognized historical archives in college football.",
        "Ohio State Men's Basketball": "Ohio State men's basketball also uses scarlet and gray and has a large historical footprint in college sports.",
    }
    st.write(history_text[selected_team])
    st.caption("You can add richer year-by-year history later if you want a deeper archive.")

elif view == "Markets":
    render_markets()

st.divider()
st.caption(f"Last rendered: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
