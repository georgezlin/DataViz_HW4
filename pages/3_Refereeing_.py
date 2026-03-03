import streamlit as st
import altair as alt
from utils.io import load_matches
from charts.charts import (
    base_theme,
    chart_referee_combined,
)

st.set_page_config(page_title="Refereeing", layout="wide")

alt.themes.register("project", base_theme)
alt.themes.enable("project")

matches = load_matches()

st.title("Refereeing")
st.write(
    "Every Premier League match is officiated by a head referee. "
    "This referee will have their own threshold for fouls and cards. "
    "The bar chart ranks referees by the average number of cards they show per match. "
    "Click a referee to cross-filter the scatter plot below."
)
st.altair_chart(chart_referee_combined(matches), use_container_width=True)
st.caption(
    "Takeaway: There is a wide range in referee strictness. "
    "Foul to card rate varies by referee. "
    "Some officials are more systematic, while others are more unpredictable."
)

st.divider()
st.subheader("Conclusion")
st.write(
    "Some officials consistently show more cards than others. The relationship between "
    "fouls and bookings is not uniform. Some referees are strict but predictable. "
    "Others appear to act on their own discretion."
)

st.write(
    "The Explore page contains an interactive dashboard that allows you to investigate these relationships on your own."
)
