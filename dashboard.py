import streamlit as st
import pandas as pd
import plotly.express as px
import os
import base64

# ========================
# App Config (MUST be first!)
# ========================
st.set_page_config(page_title="🏏 ODI Match Dashboard", layout="wide")
st.title("🏏 ODI Match Analytics Dashboard")

# ========================
# Load Data
# ========================
@st.cache_data
def load_data():
    return pd.read_csv("ODI_Match_info.csv")

df = load_data()

# ========================
# Helper: Base64 encode image
# ========================
def get_base64_image(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# ========================
# Sidebar Filters
# ========================
st.sidebar.header("🔎 Filters")

seasons = ["All"] + sorted(df['season'].dropna().unique().tolist())
teams = ["All"] + sorted(pd.concat([df['team1'], df['team2']]).dropna().unique().tolist())

selected_season = st.sidebar.selectbox("Select Season", seasons)
selected_team = st.sidebar.selectbox("Select Team", teams)

# Apply filters
filtered_df = df.copy()
if selected_season != "All":
    filtered_df = filtered_df[filtered_df['season'] == selected_season]
if selected_team != "All":
    filtered_df = filtered_df[
        (filtered_df['team1'] == selected_team) |
        (filtered_df['team2'] == selected_team) |
        (filtered_df['winner'] == selected_team) |
        (filtered_df['toss_winner'] == selected_team)
    ]

st.sidebar.success(f"📊 Showing: Season={selected_season}, Team={selected_team}")

# ========================
# Tabs for Dashboard Sections
# ========================
tab0, tab1, tab2, tab3 = st.tabs(["🏠 Home", "⚡ Toss Insights", "📈 Special Analysis", "🌟 Player Highlights"])

# ========================
# TAB 0: Home Page
# ========================
# ========================
# TAB 0: Home Page
# ========================
with tab0:
    stadium_img = get_base64_image("stadium.jpeg")

    st.markdown(
        f"""
        <style>
        .hero {{
            position: relative;
            background-image: url("data:image/jpeg;base64,{stadium_img}");
            background-size: cover;
            background-position: center;
            height: 500px;
            border-radius: 0px 0px 50% 50% / 0px 0px 20% 20%;  /* curve effect */
            overflow: hidden;
        }}
        .overlay {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.55);
        }}
        .hero h1 {{
            position: relative;
            text-align: center;
            padding-top: 200px;
            font-size: 42px;
            font-weight: bold;
            color: white;
            z-index: 2;
        }}
        </style>

        <div class="hero">
            <div class="overlay"></div>
            <h1>🏏 Welcome to ODI Match Analytics Dashboard</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Quick Stats
    st.subheader("📊 Quick Insights")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Matches", len(df))
    col2.metric("Unique Teams", df['team1'].nunique())
    col3.metric("Unique Venues", df['venue'].nunique())
    col4.metric("Seasons", df['season'].nunique())

    st.markdown("---")


    
    st.info("👉 Use the tabs above to explore Toss Insights, Yearly Trends, and Player Highlights.")

# ========================
# TAB 1: Toss Insights
# ========================
with tab1:
    st.header("⚡ Toss Insights")

    # Tosses per country
    toss_counts = filtered_df['toss_winner'].value_counts().reset_index()
    toss_counts.columns = ['Team', 'Toss Wins']
    fig1 = px.bar(toss_counts, x='Team', y='Toss Wins', title="Tosses Won per Team")
    st.plotly_chart(fig1, use_container_width=True)

    # Toss Win % per country
    toss_percent = (filtered_df['toss_winner'].value_counts(normalize=True) * 100).reset_index()
    toss_percent.columns = ['Team', 'Toss Win %']
    fig2 = px.pie(toss_percent, names='Team', values='Toss Win %', title="Toss Win Percentage")
    st.plotly_chart(fig2, use_container_width=True)

    # Toss Win → Match Win/Loss
    toss_match = pd.crosstab(filtered_df['toss_winner'], filtered_df['winner'])
    fig3 = px.imshow(toss_match, text_auto=True, aspect="auto", title="Toss Winner vs Match Winner")
    st.plotly_chart(fig3, use_container_width=True)

    # Toss Decision Outcomes
    decision_outcomes = pd.crosstab(filtered_df['toss_decision'], filtered_df['winner'])
    fig4 = px.imshow(decision_outcomes, text_auto=True, aspect="auto",
                     title="Toss Decision (Bat/Field) vs Match Winner")
    st.plotly_chart(fig4, use_container_width=True)

# ========================
# TAB 2: Special Analysis
# ========================
with tab2:
    st.header("📈 Special Country & Yearly Analysis")

    # Toss Wins by Season + Team
    toss_by_season = filtered_df.groupby(['season', 'toss_winner']).size().reset_index(name="Toss Wins")
    fig5 = px.line(toss_by_season, x='season', y='Toss Wins', color='toss_winner',
                   markers=True, title="Toss Wins Over Seasons (per Team)")
    st.plotly_chart(fig5, use_container_width=True)

    # Venue Analysis
    venue_df = filtered_df['venue'].value_counts().reset_index().head(10)
    venue_df.columns = ['Venue', 'Matches']
    fig6 = px.bar(venue_df, x='Venue', y='Matches', title="Top 10 Venues by Matches Played")
    st.plotly_chart(fig6, use_container_width=True)

    # Win Type Distribution
    filtered_df['win_type'] = filtered_df.apply(
        lambda x: 'By Runs' if x['win_by_runs'] > 0 else (
                  'By Wickets' if x['win_by_wickets'] > 0 else 'Tie/Other'),
        axis=1
    )
    fig7 = px.histogram(filtered_df, x='win_type', title="Win Types Distribution")
    st.plotly_chart(fig7, use_container_width=True)

# ========================
# TAB 3: Player Highlights
# ========================
with tab3:
    st.header("🌟 Player Highlights")

    # Top Player of the Match Awards
    pom_df = filtered_df['player_of_match'].value_counts().reset_index().head(10)
    pom_df.columns = ['Player', 'Awards']
    fig8 = px.bar(pom_df, x='Player', y='Awards', title="Top 10 Players (Player of the Match Awards)")
    st.plotly_chart(fig8, use_container_width=True)

    # Highlight Best Player
    if not pom_df.empty:
        best_player = pom_df.iloc[0]
        st.success(f"🏆 **Best Performer:** {best_player['Player']} with {best_player['Awards']} awards")

        # Try to show local image if exists
        img_file = f"{best_player['Player']}.jpg"
        img_b64 = get_base64_image(img_file)
        if img_b64:
            st.image(f"data:image/jpeg;base64,{img_b64}", caption=best_player['Player'], width=200)
        else:
            st.warning(f"No image found for {best_player['Player']}")
