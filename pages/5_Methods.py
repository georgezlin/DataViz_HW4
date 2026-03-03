import streamlit as st

st.set_page_config(page_title="Methods", layout="wide")
st.title("Methods")
st.header("Data Source")
st.write(
    "All match data came from 2 CSVs that compiled "
    "official English Premier League results from the past two seasons."
)

st.header("Key Variables")
st.write("- Variables used: `FTHG`, `FTAG`, `FTR`, `HF`, `AF`, `HY`, `AY`, `HR`, `AR`, `Referee`")
st.header("Derived Metrics")
st.markdown(
    "- TotalFouls = HF + AF\n"
    "- TotalCards = (HY + AY) + (HR + AR)\n"
    "- Points: 3 for a win, 1 for a draw, 0 for a loss\n"
    "- CumPts: Cumulative points per team per season (ordered by date)\n"
    "- Matchweek: Game number (1-38) for each team within a season\n"
    "- Position: League rank based on Pts"
)

st.header("Limitations")
st.markdown(
    "- Only two seasons: patterns may not generalize to the league's longer history.\n"
    "- Promotion/relegation: three teams differ between seasons."
    "- Referee assignment is not random: based on experience, rest, and potential conflicts of interest."
)
