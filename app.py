import streamlit as st

st.set_page_config(page_title="Deep Dive Into the Performances of the English Premier League", layout="wide")
st.title("Deep Dive Into the Performances of the English Premier League")
st.markdown(
    "**Central question:** *In the English Premier League, how much of the game "
    "is decided before the ball is kicked? How does where you play and who is refereeing the game affect the outcome?*"
)

st.write(
    "This project conducts a deep dive into the performances of football clubs participating in the last two seasons of English top flight football. Use the sidebar to navigate:"
)

st.markdown(
    "- **The Title Race** — Who won the title and who moved up or down?\n"
    "- **Home Field Advantage** — Does playing at home help a team win?\n"
    "- **Refereeing** — Which referees are stricter than others?\n"
    "- **Explore** — An Interactive Dashboard.\n"
    "- **Methods** — Details on data, variables, and limitations."
)