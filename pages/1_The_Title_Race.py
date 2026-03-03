import streamlit as st
import altair as alt
from utils.io import load_standings, load_team_matches
from charts.charts import (
    base_theme,
    chart_points_by_season,
    chart_cumulative_points_race,
)

st.set_page_config(page_title="The Title Race", layout="wide")

standings = load_standings()
team_matches = load_team_matches()

st.title("The Title Race")
st.header("Final Standings")
st.write(
    "Cumulative points dictate who wins the title for that season. "
    "Manchester City won the title with 91 points in 2023-24 and Liverpool won the title in 2024-25 with 84 points. "
    "A dot plot of every team reveals how competitive the middle "
    "of the table was and how different teams performed over two seasons."
)
st.write("Click on a team to highlight it across both seasons.")
st.altair_chart(chart_points_by_season(standings), use_container_width=True)
st.caption(
    "Takeaway: Manchester City won the title with 91 points in 2023-24 and Liverpool won the title in 2024-25 with 84 points. "
    "Additionaly, there is a significant gap between the top 6 and mid-table."
)

st.header("Week by Week Title Race Analysis")
st.write(
    "Final standings don't tell the full picture. "
    "Standings can't show momentum. "
    "By tracking cumulative points across matchweeks for the top contenders, you can see when the "
    "title was seemingly decided."
)
st.write("Click a team in the legend to highlight its trajectory.")
st.altair_chart(chart_cumulative_points_race(team_matches), use_container_width=True)
st.caption(
    "Takeaway: In 2023-24, Man City and Arsenal were the two clear contenders for the title. "
    "The cumulative curve illustrates how late-season performance led to the title for Manchester City."
)

st.divider()
st.write(
    "Next, examine how playing at home provides a measurable advantage. "
)
