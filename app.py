"""
SBSBY! — SUPER BOWL! SUPER BROWNS! YEAH!
Cleveland + Ohio State Sports Hub v2
Real-time polling, multi-source failover, optional odds API,
robust missing-data handling, Plotly trends, premium UI.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone

import pandas as pd
import plotly.express as px
import streamlit as st

try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None

from utils.api_client import TEAMS, get_client
from utils.theme import inject_css

st.set_page_config(
    page_title="SBSBY! | Cleveland & Ohio State Hub",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded",
)

defaults = {
    "team_key": "browns",
    "dark_mode": False,
    "auto_refresh": True,
    "refresh_sec": 30,
    "odds_key_input": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

with st.sidebar:
    st.markdown("## ⚡ SBSBY!")
    st.caption("Cleveland · Ohio State Hub · v2")

    team_options = {v["short"]: k for k, v in TEAMS.items()}
    labels = list(team_options.keys())
    try:
        idx = list(team_options.values()).index(st.session_state.team_key)
    except ValueError:
        idx = 0
    selected_label = st.selectbox("Select Team", options=labels, index=idx)
    st.session_state.team_key = team_options[selected_label]

    st.session_state.dark_mode = st.toggle(
        "🌙 Dark Mode", value=st.session_state.dark_mode
    )
    st.session_state.auto_refresh = st.toggle(
        "🔄 Live polling",
        value=st.session_state.auto_refresh,
        help="Auto-refresh scores & odds (near real-time)",
    )
    st.session_state.refresh_sec = st.slider(
        "Poll interval (sec)", 15, 90, st.session_state.refresh_sec, 5
    )

    st.divider()
    st.markdown("### 🎲 Odds API (optional)")
    st.caption(
        "Free key at [the-odds-api.com](https://the-odds-api.com/) (500 req/mo). "
        "Or set ODDS_API_KEY in Streamlit secrets."
    )
    key_in = st.text_input(
        "The Odds API key",
        value=st.session_state.odds_key_input,
        type="password",
        placeholder="xxxxxxxxxxxxxxxxxxxxxxxx",
    )
    st.session_state.odds_key_input = key_in

    st.divider()
    st.markdown("### Quick Links")
    team = TEAMS[st.session_state.team_key]
    q = team["name"].replace(" ", "+")
    st.markdown(
        f"""
        - [Google · Official](https://www.google.com/search?q={q}+official)
        - [ESPN search](https://www.espn.com/search/_/q/{q})
        """
    )
    st.caption("Failover: ESPN → TheSportsDB · Odds: The Odds API (optional)")

team_key = st.session_state.team_key
inject_css(team_key, st.session_state.dark_mode)

if st.session_state.auto_refresh and st_autorefresh is not None:
    st_autorefresh(
        interval=int(st.session_state.refresh_sec) * 1000,
        key="sbsby_live_poll",
    )

client = get_client()

odds_key = (
    st.session_state.odds_key_input
    or st.secrets.get("ODDS_API_KEY", "")
    or os.environ.get("ODDS_API_KEY", "")
    or os.environ.get("THE_ODDS_API_KEY", "")
)
if odds_key:
    client.set_odds_key(odds_key)

team = TEAMS[team_key]

live = False
try:
    live = client.any_live_games(team_key)
except Exception:
    live = False

live_html = (
    '<span class="live-dot"></span>LIVE GAMES'
    if live
    else "Scores · News · Odds · Markets"
)
st.markdown(
    f"""
    <div class="sbsby-banner">
        <h1>SUPER BOWL! SUPER BROWNS! YEAH!</h1>
        <p class="subtitle">SBSBY! · {team['name']} · {live_html}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns([2.2, 1, 1])
with c1:
    st.markdown(f"### {team['name']}")
with c2:
    if st.button("↻ Force Refresh", use_container_width=True):
        client.clear_cache()
        st.rerun()
with c3:
    st.caption(f"UTC {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")

try:
    info, info_src = client.get_team_info(team_key)
except Exception:
    info, info_src = {
        "name": team["name"],
        "record": "—",
        "logo": None,
    }, "error"

record = info.get("record") or "—"
logo = info.get("logo")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(
        f'<div class="metric-pill"><div class="label">Record</div>'
        f'<div class="value">{record}</div></div>',
        unsafe_allow_html=True,
    )
with m2:
    st.markdown(
        f'<div class="metric-pill"><div class="label">League</div>'
        f'<div class="value">{team["league"].replace("-", " ").upper()}</div></div>',
        unsafe_allow_html=True,
    )
with m3:
    st.markdown(
        f'<div class="metric-pill"><div class="label">Data Source</div>'
        f'<div class="value" style="font-size:0.9rem">{info_src}</div></div>',
        unsafe_allow_html=True,
    )
with m4:
    if logo:
        try:
            st.image(logo, width=56)
        except Exception:
            st.markdown(
                f'<div class="metric-pill"><div class="label">Team</div>'
                f'<div class="value">{team["short"]}</div></div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            f'<div class="metric-pill"><div class="label">Team</div>'
            f'<div class="value">{team["short"]}</div></div>',
            unsafe_allow_html=True,
        )

(
    tab_scores,
    tab_odds,
    tab_news,
    tab_standings,
    tab_schedule,
    tab_trends,
    tab_markets,
) = st.tabs(
    [
        "🏈 Live Scores",
        "💰 Odds",
        "📰 News",
        "📊 Standings",
        "📅 Schedule",
        "📈 Trends",
        "🎯 Prediction Markets",
    ]
)

with tab_scores:
    st.markdown(
        '<div class="section-title">Current & Recent Scores</div>',
        unsafe_allow_html=True,
    )
    try:
        games, src = client.get_scoreboard(team_key)
        if not games:
            st.markdown(
                '<div class="sbsby-card empty-state">'
                "No games in the current window. Check Schedule or try another team."
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            for g in games:
                state = (g.get("status_state") or "").lower()
                is_live = state == "in"
                badge_cls = "status-badge live" if is_live else "status-badge"
                status_txt = g.get("detail") or g.get("status") or "Scheduled"
                odds_line = g.get("odds") or {}
                odds_html = ""
                if odds_line:
                    bits = []
                    if odds_line.get("spread"):
                        bits.append(f"Line: {odds_line['spread']}")
                    if odds_line.get("over_under") is not None:
                        bits.append(f"O/U: {odds_line['over_under']}")
                    if bits:
                        odds_html = (
                            f'<div class="source-badge">{" · ".join(bits)}'
                            f' ({odds_line.get("provider") or "odds"})</div>'
                        )
                st.markdown(
                    f"""
                    <div class="sbsby-card">
                        <div class="score-card">
                            <div class="team-block">
                                <div class="score">{g.get('away_score', '–')}</div>
                                <div class="name">{g.get('away_team', 'Away')}</div>
                            </div>
                            <div style="text-align:center;">
                                <div class="vs-pill">VS</div>
                                <div class="{badge_cls}">{status_txt}</div>
                            </div>
                            <div class="team-block">
                                <div class="score">{g.get('home_score', '–')}</div>
                                <div class="name">{g.get('home_team', 'Home')}</div>
                            </div>
                        </div>
                        <div class="source-badge">
                            {(g.get('venue') or '')} · {(g.get('broadcast') or '')} · via {g.get('source', src)}
                        </div>
                        {odds_html}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.caption(f"Scores source: **{src}** · Failover: ESPN → TheSportsDB")
    except Exception as e:
        st.error("Scores unavailable after all sources.")
        st.caption(str(e))

with tab_odds:
    st.markdown(
        '<div class="section-title">Consensus & Book Odds</div>',
        unsafe_allow_html=True,
    )
    if not odds_key:
        st.info(
            "Add a free **The Odds API** key in the sidebar (or Streamlit secrets "
            "`ODDS_API_KEY`) to load moneyline, spread, and totals."
        )
        st.markdown(
            "[Get free API key → the-odds-api.com](https://the-odds-api.com/)"
        )
    else:
        try:
            odds_games, osrc = client.get_odds(team_key)
            if not odds_games:
                st.markdown(
                    '<div class="sbsby-card empty-state">'
                    "No odds returned (off-season, rate limit, or no matching games)."
                    "</div>",
                    unsafe_allow_html=True,
                )
            else:
                for og in odds_games:
                    rel = "⭐ " if og.get("relevant") else ""
                    st.markdown(
                        f"""
                        <div class="sbsby-card">
                            <strong>{rel}{og.get('away_team')} @ {og.get('home_team')}</strong>
                            <div class="news-meta">{(og.get('commence_time') or '')[:16].replace('T',' ')} UTC · {og.get('sport') or ''}</div>
                        """,
                        unsafe_allow_html=True,
                    )
                    for bm in og.get("bookmakers") or []:
                        chips = []
                        for mkey, outcomes in (bm.get("markets") or {}).items():
                            for o in outcomes:
                                label = o.get("name") or ""
                                price = o.get("price")
                                pt = o.get("point")
                                pt_s = f" ({pt})" if pt is not None else ""
                                chips.append(
                                    f'<span class="odds-chip">{mkey}: {label}{pt_s} {price}</span>'
                                )
                        if chips:
                            st.markdown(
                                f'<div class="odds-book"><strong>{bm.get("book")}</strong><br>'
                                + "".join(chips)
                                + "</div>",
                                unsafe_allow_html=True,
                            )
                    st.markdown("</div>", unsafe_allow_html=True)
                st.caption(f"Odds source: **{osrc}** · American odds · US books")
        except Exception as e:
            st.warning(f"Odds request failed: {e}")

with tab_news:
    st.markdown(
        '<div class="section-title">Latest Headlines</div>', unsafe_allow_html=True
    )
    try:
        articles, src = client.get_news(team_key, limit=14)
        if not articles:
            st.markdown(
                '<div class="sbsby-card empty-state">No articles right now.</div>',
                unsafe_allow_html=True,
            )
        else:
            for a in articles:
                url = a.get("url") or "#"
                headline = a.get("headline") or "Untitled"
                desc = (a.get("description") or "")[:200]
                published = (a.get("published") or "")[:16].replace("T", " ")
                st.markdown(
                    f"""
                    <div class="sbsby-card">
                        <div class="news-item" style="border:none;padding:0;">
                            <div>
                                <a href="{url}" target="_blank" rel="noopener">{headline}</a>
                                <div class="news-meta">{published} · {a.get('source', src)}</div>
                                <p style="margin:0.4rem 0 0;font-size:0.88rem;opacity:0.85;">{desc}</p>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.caption(f"News source: **{src}**")
    except Exception as e:
        st.warning(f"News unavailable ({e}).")

with tab_standings:
    st.markdown(
        '<div class="section-title">Standings Snapshot</div>', unsafe_allow_html=True
    )
    try:
        rows, src = client.get_standings(team_key)
        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Standings source: **{src}**")
        else:
            st.markdown(
                '<div class="sbsby-card empty-state">'
                "Standings not available (season inactive or source gap)."
                "</div>",
                unsafe_allow_html=True,
            )
    except Exception as e:
        st.warning(f"Standings unavailable ({e}).")

with tab_schedule:
    st.markdown(
        '<div class="section-title">Recent & Upcoming</div>', unsafe_allow_html=True
    )
    try:
        games, src = client.get_schedule(team_key)
        if not games:
            st.markdown(
                '<div class="sbsby-card empty-state">No schedule entries.</div>',
                unsafe_allow_html=True,
            )
        else:
            for g in games:
                st.markdown(
                    f"""
                    <div class="sbsby-card" style="padding:0.85rem 1.1rem;">
                        <strong>{g.get('name') or (str(g.get('away_team','')) + ' @ ' + str(g.get('home_team','')))}</strong>
                        <div class="news-meta">
                            {(g.get('date') or '')[:16]} · {g.get('status', '')} ·
                            {g.get('away_score','–')} – {g.get('home_score','–')}
                            {(' · ' + g['venue']) if g.get('venue') else ''}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.caption(f"Schedule source: **{src}**")
    except Exception as e:
        st.warning(f"Schedule unavailable ({e}).")

with tab_trends:
    st.markdown(
        '<div class="section-title">Recent Form & Scoring Trend</div>',
        unsafe_allow_html=True,
    )
    try:
        form, src = client.get_recent_form(team_key)
        if form:
            rows = []
            for g in form:
                try:
                    hs = int(float(g.get("home_score") or 0))
                    as_ = int(float(g.get("away_score") or 0))
                except (TypeError, ValueError):
                    hs, as_ = 0, 0
                rows.append(
                    {
                        "Matchup": g.get("name")
                        or f"{g.get('away_team')} @ {g.get('home_team')}",
                        "Away": as_,
                        "Home": hs,
                        "Total": as_ + hs,
                        "Date": (g.get("date") or "")[:10],
                        "Status": g.get("status"),
                    }
                )
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True, hide_index=True)
            if len(df) >= 2 and df["Total"].sum() > 0:
                fig = px.bar(
                    df,
                    x="Date",
                    y="Total",
                    color="Total",
                    title="Combined score by game (recent)",
                    labels={"Total": "Points"},
                )
                fig.update_layout(
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=320,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)
            st.caption(f"Form source: **{src}**")
        else:
            st.markdown(
                '<div class="sbsby-card empty-state">'
                "Not enough completed games for form analysis."
                "</div>",
                unsafe_allow_html=True,
            )
    except Exception as e:
        st.warning(f"Trends unavailable ({e}).")

    st.markdown("#### Historical resources")
    st.markdown(
        """
        - [Pro Football Reference](https://www.pro-football-reference.com/)
        - [Basketball Reference](https://www.basketball-reference.com/)
        - [Baseball Reference](https://www.baseball-reference.com/)
        - [Sports-Reference CFB / CBB](https://www.sports-reference.com/)
        """
    )

with tab_markets:
    st.markdown(
        '<div class="section-title">Prediction Markets</div>', unsafe_allow_html=True
    )
    st.markdown(
        "External platforms for current & future outcomes. Comply with local laws."
    )
    links = client.prediction_links(team_key)
    cards = "".join(
        f"""
        <a class="pred-card" href="{l['url']}" target="_blank" rel="noopener">
            <strong>{l['name']}</strong>
            <span>{l['desc']}</span>
        </a>
        """
        for l in links
    )
    st.markdown(f'<div class="pred-grid">{cards}</div>', unsafe_allow_html=True)

st.divider()
st.markdown(
    """
    <div style="text-align:center;opacity:0.7;font-size:0.82rem;">
        <strong>SBSBY!</strong> · SUPER BOWL! SUPER BROWNS! YEAH!<br>
        Live poll · ESPN → TheSportsDB failover · Optional The Odds API ·
        Not affiliated with NFL, MLB, NBA, or Ohio State
    </div>
    """,
    unsafe_allow_html=True,
)
