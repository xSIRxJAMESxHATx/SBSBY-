import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(
    page_title="SBSBY!",
    page_icon="🏟️",
    layout="wide",
    initial_sidebar_state="expanded",
)

TEAM_DATA = {
    "Cleveland Browns": {
        "accent": "#FF7300",
        "dark": "#4C230A",
        "light": "#F5F1EC",
        "sources": [
            "https://www.nfl.com/teams/cleveland-browns/",
            "https://www.espn.com/nfl/team/_/name/cle/cleveland-browns",
            "https://www.cbssports.com/nfl/teams/CLE/cleveland-browns/",
        ],
        "news": [
            "https://www.nfl.com/teams/cleveland-browns/",
            "https://www.espn.com/nfl/team/_/name/cle/cleveland-browns",
            "https://www.cbssports.com/nfl/teams/CLE/cleveland-browns/",
        ],
        "history": "The Browns are Cleveland's NFL franchise, founded in 1946. Their official club colors are brown, orange, and white.",
    },
    "Cleveland Guardians": {
        "accent": "#FF7300",
        "dark": "#4C230A",
        "light": "#F5F1EC",
        "sources": [
            "https://www.espn.com/mlb/team/_/name/cle/cleveland-guardians",
            "https://www.cbssports.com/mlb/teams/CLE/cleveland-guardians/",
            "https://www.mlb.com/guardians",
        ],
        "news": [
            "https://www.espn.com/mlb/team/_/name/cle/cleveland-guardians",
            "https://www.cbssports.com/mlb/teams/CLE/cleveland-guardians/",
            "https://www.mlb.com/guardians",
        ],
        "history": "The Guardians are Cleveland's MLB franchise, with live scores, standings, roster info, and season news available from major sports sources.",
    },
    "Cleveland Cavaliers": {
        "accent": "#860038",
        "dark": "#FDBB30",
        "light": "#F5F1EC",
        "sources": [
            "https://www.espn.com/nba/team/_/name/cle/cleveland-cavaliers",
            "https://www.cbssports.com/nba/teams/CLE/cleveland-cavaliers/",
            "https://www.nba.com/cavaliers/",
        ],
        "news": [
            "https://www.espn.com/nba/team/_/name/cle/cleveland-cavaliers",
            "https://www.cbssports.com/nba/teams/CLE/cleveland-cavaliers/",
            "https://www.nba.com/cavaliers/",
        ],
        "history": "The Cavaliers are Cleveland's NBA franchise and have extensive public coverage for scores, stats, player trends, and season history.",
    },
    "Ohio State Football": {
        "accent": "#CE202F",
        "dark": "#666666",
        "light": "#F5F1EC",
        "sources": [
            "https://ohiostatebuckeyes.com/sports/football",
            "https://www.espn.com/college-football/team/_/id/194/ohio-state-buckeyes",
            "https://www.cbssports.com/college-football/teams/OHIOST/ohio-state-buckeyes/",
        ],
        "news": [
            "https://ohiostatebuckeyes.com/sports/football",
            "https://www.espn.com/college-football/team/_/id/194/ohio-state-buckeyes",
            "https://www.cbssports.com/college-football/teams/OHIOST/ohio-state-buckeyes/",
        ],
        "history": "Ohio State football uses scarlet and gray and has a deep historical archive of seasons, championships, and program milestones.",
    },
    "Ohio State Men's Basketball": {
        "accent": "#CE202F",
        "dark": "#666666",
        "light": "#F5F1EC",
        "sources": [
            "https://ohiostatebuckeyes.com/sports/mens-basketball",
            "https://www.espn.com/mens-college-basketball/team/_/id/194/ohio-state-buckeyes",
            "https://www.cbssports.com/college-basketball/teams/OHIOST/ohio-state-buckeyes/",
        ],
        "news": [
            "https://ohiostatebuckeyes.com/sports/mens-basketball",
            "https://www.espn.com/mens-college-basketball/team/_/id/194/ohio-state-buckeyes",
            "https://www.cbssports.com/college-basketball/teams/OHIOST/ohio-state-buckeyes/",
        ],
        "history": "Ohio State men's basketball is a major college program with strong season archives, roster history, and game coverage.",
    },
}

MARKETS = [
    ("Polymarket", "https://polymarket.com/"),
    ("Kalshi", "https://kalshi.com/"),
    ("Manifold", "https://manifold.markets/"),
]

st.markdown(
    """
    <style>
    :root { color-scheme: dark; }
    .stApp {
        background: #111214;
        color: #F4F4F5;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #17181B 0%, #101114 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    .hero {
        border-radius: 22px;
        padding: 1.25rem 1.4rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1rem;
    }
    .panel {
        border-radius: 18px;
        padding: 1rem;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1rem;
    }
    .muted {
        color: #A1A1AA;
        font-size: 0.93rem;
    }
    .team-chip {
        display: inline-block;
        padding: 0.35rem 0.65rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    a { text-decoration: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "selected_team" not in st.session_state:
    st.session_state.selected_team = "Cleveland Browns"

with st.sidebar:
    st.markdown("## SBSBY!")
    st.caption("Cleveland sports hub")
    st.session_state.selected_team = st.selectbox(
        "Select a team",
        list(TEAM_DATA.keys()),
        index=list(TEAM_DATA.keys()).index(st.session_state.selected_team),
    )
    page = st.radio(
        "Section",
        ["Overview", "Live Scores", "News", "Stats", "History", "Markets"],
        index=0,
    )
    st.divider()
    st.link_button("Streamlit Cloud", "https://share.streamlit.io/")
    st.link_button("GitHub", "https://github.com/")

team = st.session_state.selected_team
cfg = TEAM_DATA[team]

def source_button(label, url):
    st.link_button(label, url)

def fetch_text(url):
    try:
        r = requests.get(url, timeout=12, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200 and r.text:
            return r.text
        return ""
    except Exception:
        return ""

def first_working_source(urls):
    for url in urls:
        text = fetch_text(url)
        if text:
            return url, text
    return None, ""

def link_table(urls, limit=12):
    rows = []
    for idx, url in enumerate(urls, start=1):
        rows.append({"Priority": idx, "Source": url})
    return pd.DataFrame(rows)

def static_stats(team_name):
    if team_name == "Cleveland Browns":
        data = [
            ("League", "NFL"),
            ("Theme", "Brown, orange, white"),
            ("Focus", "Roster, schedule, trends"),
            ("History", "Founded in 1946"),
        ]
    elif team_name == "Cleveland Guardians":
        data = [
            ("League", "MLB"),
            ("Theme", "Neutral site, orange accents"),
            ("Focus", "Scores, batting, pitching"),
            ("History", "Cleveland baseball franchise"),
        ]
    elif team_name == "Cleveland Cavaliers":
        data = [
            ("League", "NBA"),
            ("Theme", "Wine and gold accents"),
            ("Focus", "Game flow, player trends"),
            ("History", "Cleveland basketball franchise"),
        ]
    elif team_name == "Ohio State Football":
        data = [
            ("League", "NCAA Football"),
            ("Theme", "Scarlet and gray"),
            ("Focus", "Rankings, schedules, game previews"),
            ("History", "Power program"),
        ]
    else:
        data = [
            ("League", "NCAA Basketball"),
            ("Theme", "Scarlet and gray"),
            ("Focus", "Season results, roster info"),
            ("History", "Major college basketball program"),
        ]
    return pd.DataFrame(data, columns=["Stat", "Value"])

def render_links(title, urls):
    st.subheader(title)
    cols = st.columns(len(urls))
    for i, url in enumerate(urls):
        with cols[i]:
            st.link_button(f"Source {i+1}", url)

@st.fragment(run_every=60)
def live_score_panel():
    st.subheader("Live score feed")
    url, text = first_working_source(cfg["sources"])
    if url and text:
        preview = " ".join(text.split())[:6000]
        st.success(f"Showing latest accessible source: {url}")
        st.write(preview)
        st.caption("This panel refreshes automatically every 60 seconds.")
    else:
        st.warning("No live source responded right now. Try a different source or reload in a moment.")
    st.markdown("### Source priority")
    st.dataframe(link_table(cfg["sources"]), use_container_width=True, hide_index=True)

if page == "Overview":
    st.markdown(
        f"""
        <div class="hero">
            <div class="team-chip" style="background:{cfg['accent']}; color:{cfg['light']};">
                {team}
            </div>
            <h1 style="margin:0 0 0.25rem 0;">SBSBY!</h1>
            <p style="margin:0;">
                Clean Cleveland sports dashboard with live sources, stats, history, and market links.
            </p>
            <p class="muted" style="margin:0.35rem 0 0 0;">
                Neutral overall design, team-specific color accents, and a polished layout optimized for quick browsing.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    a, b, c = st.columns([1.2, 1, 1])
    with a:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### Quick actions")
        source_button("Open primary source", cfg["sources"][0])
        source_button("Open news source", cfg["news"][0])
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### Theme")
        st.write(f"Accent color: {cfg['accent']}")
        st.write(f"Secondary color: {cfg['dark']}")
        st.write("Neutral site-wide styling")
        st.markdown("</div>", unsafe_allow_html=True)
    with c:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### Market links")
        for name, url in MARKETS:
            st.link_button(name, url)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### Summary stats")
    st.dataframe(static_stats(team), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Live Scores":
    st.markdown(
        f"""
        <div class="hero">
            <div class="team-chip" style="background:{cfg['accent']}; color:{cfg['light']};">
                {team}
            </div>
            <h2 style="margin:0;">Live scores and schedules</h2>
            <p class="muted" style="margin:0.35rem 0 0 0;">The app checks multiple sources in order and refreshes automatically.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    live_score_panel()

elif page == "News":
    st.markdown(
        f"""
        <div class="hero">
            <div class="team-chip" style="background:{cfg['accent']}; color:{cfg['light']};">
                {team}
            </div>
            <h2 style="margin:0;">News and articles</h2>
            <p class="muted" style="margin:0.35rem 0 0 0;">Source links are arranged by priority so the page still works when one source is unavailable.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_links("Open news sources", cfg["news"])

elif page == "Stats":
    st.markdown(
        f"""
        <div class="hero">
            <div class="team-chip" style="background:{cfg['accent']}; color:{cfg['light']};">
                {team}
            </div>
            <h2 style="margin:0;">Stats and trends</h2>
            <p class="muted" style="margin:0.35rem 0 0 0;">Use this section for standings, player trends, and historical performance links.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(static_stats(team), use_container_width=True, hide_index=True)
    st.subheader("Source options")
    st.dataframe(link_table(cfg["sources"]), use_container_width=True, hide_index=True)

elif page == "History":
    st.markdown(
        f"""
        <div class="hero">
            <div class="team-chip" style="background:{cfg['accent']}; color:{cfg['light']};">
                {team}
            </div>
            <h2 style="margin:0;">Historical information</h2>
            <p class="muted" style="margin:0.35rem 0 0 0;">Concise team history with clean presentation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="panel"><p>{cfg["history"]}</p></div>', unsafe_allow_html=True)

elif page == "Markets":
    st.markdown(
        f"""
        <div class="hero">
            <div class="team-chip" style="background:{cfg['accent']}; color:{cfg['light']};">
                {team}
            </div>
            <h2 style="margin:0;">Prediction markets</h2>
            <p class="muted" style="margin:0.35rem 0 0 0;">General market destinations for current and future games.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    for i, (name, url) in enumerate(MARKETS):
        with cols[i]:
            st.link_button(name, url)
    st.caption("Swap these links for specific event pages as you build out the app.")

st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
