import streamlit as st
import altair as alt
from utils.io import load_standings, load_team_matches
from charts.charts import (
    base_theme,
    chart_home_away_combined,
    chart_home_away_goals,
)

st.set_page_config(page_title="Home Field Advantage", layout="wide")

alt.themes.register("project", base_theme)
alt.themes.enable("project")

standings = load_standings()
team_matches = load_team_matches()
st.title("Home Field Advantage")
st.write(
    "Does home field advantage exist in the English Premier League? "
    "The scatter plot below shows each team's home points against their away points. "
    "Teams below the diagonal earn more points at home; teams above it are better away."
)
st.write("Click on a team to see its home/away split in the bar chart on the right.")
st.altair_chart(chart_home_away_combined(standings), use_container_width=True)

st.caption(
    "Takeaway: Most teams fall below the diagonal. This suggests a home advantage. "
    "The size of that advantage varies from team to team."
)

st.header("The Gap")
st.write(
    "On average, teams score more goals at home than away in both seasons. "
    "The grouped bar chart below illustrates this gap across both seasons."
)
st.altair_chart(chart_home_away_goals(team_matches), use_container_width=True)
st.caption(
    "Takeaway: Home teams score on average more goals per game. "
)
st.divider()
st.write(
    "Next, look at how referees influence the outcome of the game. "
)
