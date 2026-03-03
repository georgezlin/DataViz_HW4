import streamlit as st
import pandas as pd

@st.cache_data
def load_matches() -> pd.DataFrame:
    s1 = pd.read_csv("data/HW3 Season 23-24.csv")
    s2 = pd.read_csv("data/HW3 Season 24-25.csv")
    s1["Season"] = "2023-24"
    s2["Season"] = "2024-25"

    matches = pd.concat([s1, s2], ignore_index=True)
    matches["Date"] = pd.to_datetime(matches["Date"], format="%d/%m/%y")
    matches["TotalFouls"] = matches["HF"] + matches["AF"]
    matches["TotalYellow"] = matches["HY"] + matches["AY"]
    matches["TotalRed"] = matches["HR"] + matches["AR"]
    matches["TotalCards"] = matches["TotalYellow"] + matches["TotalRed"]
    matches["TotalGoals"] = matches["FTHG"] + matches["FTAG"]
    return matches


@st.cache_data
def load_team_matches() -> pd.DataFrame:
    matches = load_matches()

    home = matches[["Date", "Season", "HomeTeam", "FTHG", "FTAG", "FTR"]].copy()
    home.columns = ["Date", "Season", "Team", "GF", "GA", "FTR"]
    home["Venue"] = "Home"
    home["Result"] = home["FTR"].map({"H": "W", "D": "D", "A": "L"})
    home["Pts"] = home["FTR"].map({"H": 3, "D": 1, "A": 0})

    away = matches[["Date", "Season", "AwayTeam", "FTAG", "FTHG", "FTR"]].copy()
    away.columns = ["Date", "Season", "Team", "GF", "GA", "FTR"]
    away["Venue"] = "Away"
    away["Result"] = away["FTR"].map({"H": "L", "D": "D", "A": "W"})
    away["Pts"] = away["FTR"].map({"H": 0, "D": 1, "A": 3})

    team_matches = pd.concat([home, away], ignore_index=True)
    team_matches = team_matches.sort_values(["Season", "Team", "Date"]).reset_index(drop=True)

    team_matches["CumPts"] = team_matches.groupby(["Team", "Season"])["Pts"].cumsum()
    team_matches["Matchweek"] = team_matches.groupby(["Team", "Season"]).cumcount() + 1

    return team_matches


@st.cache_data
def load_standings() -> pd.DataFrame:
    team_matches = load_team_matches()
    standings = team_matches.groupby(["Team", "Season"]).agg(
        P=("Pts", "count"),
        W=("Result", lambda x: (x == "W").sum()),
        D=("Result", lambda x: (x == "D").sum()),
        L=("Result", lambda x: (x == "L").sum()),
        GF=("GF", "sum"),
        GA=("GA", "sum"),
        Pts=("Pts", "sum"),
    ).reset_index()
    standings["GD"] = standings["GF"] - standings["GA"]
    standings = standings.sort_values(
        ["Season", "Pts", "GD", "GF"], ascending=[True, False, False, False]
    )
    standings["Position"] = standings.groupby("Season").cumcount() + 1

    ha = team_matches.groupby(["Team", "Season", "Venue"]).agg(
        W=("Result", lambda x: (x == "W").sum()),
        D=("Result", lambda x: (x == "D").sum()),
        L=("Result", lambda x: (x == "L").sum()),
        GF=("GF", "sum"),
        GA=("GA", "sum"),
        Pts=("Pts", "sum"),
    ).reset_index()

    h = ha[ha.Venue == "Home"].rename(columns={
        "W": "HomeW", "D": "HomeD", "L": "HomeL",
        "GF": "HomeGF", "GA": "HomeGA", "Pts": "HomePts",
    }).drop(columns="Venue")
    a = ha[ha.Venue == "Away"].rename(columns={
        "W": "AwayW", "D": "AwayD", "L": "AwayL",
        "GF": "AwayGF", "GA": "AwayGA", "Pts": "AwayPts",
    }).drop(columns="Venue")

    standings = standings.merge(h, on=["Team", "Season"]).merge(a, on=["Team", "Season"])
    standings["HomeGD"] = standings["HomeGF"] - standings["HomeGA"]
    standings["AwayGD"] = standings["AwayGF"] - standings["AwayGA"]
    return standings
