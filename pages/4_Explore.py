import streamlit as st
import altair as alt
from utils.io import load_standings, load_matches
from charts.charts import base_theme, chart_dashboard

st.set_page_config(page_title="Explore", layout="wide")

alt.themes.register("project", base_theme)
alt.themes.enable("project")
standings = load_standings()
matches = load_matches()

st.title("Explore the Data")
st.markdown(
    "How to interact:\n"
    "- Click a team in the dot plot or scatter to highlight it and update the bar chart.\n"
    "- Click a referee in the referee bar chart to filter the fouls vs cards scatter.\n"
    "- Brush on the fouls-vs-cards scatter to filter the referee bars.\n"
)

st.altair_chart(chart_dashboard(standings, matches), use_container_width=True)
st.markdown(
    "Addressable Questions:\n"
    "- Which teams earned a larger share of their points at home?\n"
    "- Is there a referee who stands out as particularly strict or lenient?\n"
    "- Do high-foul matches always produce more cards?"
)
