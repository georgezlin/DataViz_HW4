import altair as alt
import pandas as pd

def base_theme():
    return {
        "config": {
            "view": {"stroke": None},
            "axis": {"labelFontSize": 12, "titleFontSize": 14},
            "legend": {"labelFontSize": 12, "titleFontSize": 14},
        }
    }

def chart_points_by_season(standings: pd.DataFrame) -> alt.Chart:
    team_click = alt.selection_point(fields=['Team'])
    return alt.Chart(standings).mark_circle().encode(
        y='Team:N',
        x='Pts:Q',
        color='Season:N',
        opacity=alt.condition(team_click, alt.value(1), alt.value(0.15)),
        tooltip=[
            alt.Tooltip('Team:N'),
            alt.Tooltip('Season:N'),
            alt.Tooltip('Position:Q', title='League Position'),
            alt.Tooltip('Pts:Q', title='Points'),
            alt.Tooltip('W:Q', title='Wins'),
            alt.Tooltip('D:Q', title='Draws'),
            alt.Tooltip('L:Q', title='Losses'),
            alt.Tooltip('GD:Q', title='Goal Diff')
        ]
    ).add_params(
        team_click
    ).properties(
        title='Team Points by Season'
    )

def chart_cumulative_points_race(team_matches: pd.DataFrame) -> alt.Chart:
    top_teams = (
        team_matches.groupby(["Team", "Season"])["Pts"]
        .sum()
        .reset_index()
        .sort_values("Pts", ascending=False)
        .groupby("Season")
        .head(6)["Team"]
        .unique()
        .tolist()
    )
    df = team_matches[team_matches["Team"].isin(top_teams)].copy()
    highlight = alt.selection_point(fields=["Team"], bind="legend")
    return (
        alt.Chart(df)
        .mark_line(strokeWidth=2.5)
        .encode(
            x='Matchweek:Q',
            y='CumPts:Q',
            color='Team:N',
            opacity=alt.condition(highlight, alt.value(1), alt.value(0.15)),
            tooltip=[
                alt.Tooltip('Team:N'),
                alt.Tooltip('Season:N'),
                alt.Tooltip('Matchweek:Q'),
                alt.Tooltip('CumPts:Q', title='Cumulative Pts'),
            ],
        )
        .add_params(highlight)
        .properties(height=350)
        .facet(column=alt.Column("Season:N", title=None))
    )

def chart_season_shift(standings: pd.DataFrame) -> alt.Chart:
    both = standings.groupby("Team").filter(lambda g: len(g) == 2)
    lines = (
        alt.Chart(both)
        .mark_line(opacity=0.5)
        .encode(
            x='Season:N',
            y=alt.Y('Position:Q', scale=alt.Scale(reverse=True)),
            detail='Team:N',
        )
    )
    points = (
        alt.Chart(both)
        .mark_circle(size=70)
        .encode(
            x='Season:N',
            y=alt.Y('Position:Q', scale=alt.Scale(reverse=True)),
            color=alt.Color('Team:N', legend=None),
            tooltip=[
                alt.Tooltip('Team:N'),
                alt.Tooltip('Season:N'),
                alt.Tooltip('Position:Q'),
                alt.Tooltip('Pts:Q'),
            ],
        )
    )
    labels = (
        alt.Chart(both[both["Season"] == "2024-25"])
        .mark_text(align="left", dx=8, fontSize=11)
        .encode(
            x='Season:N',
            y=alt.Y('Position:Q', scale=alt.Scale(reverse=True)),
            text='Team:N',
        )
    )
    return (lines + points + labels).properties(
        height=500, width=350, title='Position Change: Teams in Both Seasons'
    )

def chart_home_away_combined(standings: pd.DataFrame) -> alt.HConcatChart:
    team_click = alt.selection_point(fields=['Team'])
    scatter = alt.Chart(standings).mark_circle().encode(
        x='HomePts:Q',
        y='AwayPts:Q',
        color='Season:N',
        opacity=alt.condition(team_click, alt.value(1), alt.value(0.15)),
        tooltip=[
            alt.Tooltip('Team:N'),
            alt.Tooltip('Season:N'),
            alt.Tooltip('HomePts:Q'),
            alt.Tooltip('AwayPts:Q'),
            alt.Tooltip('HomeGD:Q', title='Home GD'),
            alt.Tooltip('AwayGD:Q', title='Away GD')
        ]
    ).add_params(
        team_click
    )

    diag = alt.Chart(
        pd.DataFrame({'HomePts': [0, 50], 'AwayPts': [0, 50]})
    ).mark_line().encode(x='HomePts:Q', y='AwayPts:Q')

    scatter_with_diag = (diag + scatter).properties(
        title='Home vs Away Points'
    )

    bar = alt.Chart(standings).transform_filter(
        team_click
    ).transform_fold(
        ['HomePts', 'AwayPts'],
        as_=['Venue', 'Points']
    ).mark_bar().encode(
        x='Venue:N',
        y='mean(Points):Q',
        color='Venue:N'
    ).properties(
        title='Avg Pts (selected)'
    )
    return alt.hconcat(scatter_with_diag, bar)

def chart_home_away_goals(team_matches: pd.DataFrame) -> alt.Chart:
    return alt.Chart(team_matches).mark_bar().encode(
        x='Season:N',
        y='mean(GF):Q',
        color='Venue:N',
        xOffset='Venue:N',
        tooltip=[
            alt.Tooltip('Season:N'),
            alt.Tooltip('Venue:N'),
            alt.Tooltip('mean(GF):Q', title='Avg Goals', format='.2f'),
        ],
    ).properties(
        title='Average Goals Scored: Home vs Away'
    )

def chart_referee_combined(matches: pd.DataFrame) -> alt.LayerChart:
    ref_click = alt.selection_point(fields=['Referee'])
    bar = alt.Chart(matches).mark_bar().encode(
        y='Referee:N',
        x='mean(TotalCards):Q',
        color='mean(TotalFouls):Q',
        opacity=alt.condition(ref_click, alt.value(1), alt.value(0.3)),
        tooltip=[
            alt.Tooltip('Referee:N'),
            alt.Tooltip('count():Q', title='Matches'),
            alt.Tooltip('mean(TotalFouls):Q'),
            alt.Tooltip('mean(TotalYellow):Q'),
            alt.Tooltip('mean(TotalRed):Q')
        ]
    ).add_params(
        ref_click
    ).properties(
        title='Referee Card Rankings'
    )

    scatter = alt.Chart(matches).mark_circle().encode(
        x='TotalFouls:Q',
        y='TotalCards:Q',
        color='FTR:N',
        opacity=alt.condition(ref_click, alt.value(0.7), alt.value(0.1)),
        tooltip=[
            alt.Tooltip('HomeTeam:N'),
            alt.Tooltip('AwayTeam:N'),
            alt.Tooltip('FTHG:Q', title='Home Goals'),
            alt.Tooltip('FTAG:Q', title='Away Goals'),
            alt.Tooltip('Referee:N'),
            alt.Tooltip('TotalFouls:Q'),
            alt.Tooltip('TotalCards:Q')
        ]
    ).properties(
        title='Match Fouls vs Cards'
    )
    return alt.vconcat(bar, scatter)

def chart_dashboard(standings: pd.DataFrame, matches: pd.DataFrame) -> alt.Chart:
    team_click = alt.selection_point(fields=['Team'])
    ref_click = alt.selection_point(fields=['Referee'])
    match_brush = alt.selection_interval()

    q1_dots = alt.Chart(standings).mark_circle().encode(
        y='Team:N',
        x='Pts:Q',
        color='Season:N',
        opacity=alt.condition(team_click, alt.value(1), alt.value(0.15)),
        tooltip=[
            alt.Tooltip('Team:N'),
            alt.Tooltip('Season:N'),
            alt.Tooltip('Position:Q', title='League Position'),
            alt.Tooltip('Pts:Q', title='Points'),
            alt.Tooltip('W:Q', title='Wins'),
            alt.Tooltip('D:Q', title='Draws'),
            alt.Tooltip('L:Q', title='Losses'),
            alt.Tooltip('GD:Q', title='Goal Diff')
        ]
    ).add_params(
        team_click
    ).properties(
        title='Team Points by Season'
    )

    q3_scatter = alt.Chart(standings).mark_circle().encode(
        x='HomePts:Q',
        y='AwayPts:Q',
        color='Season:N',
        opacity=alt.condition(team_click, alt.value(1), alt.value(0.15)),
        tooltip=[
            alt.Tooltip('Team:N'),
            alt.Tooltip('Season:N'),
            alt.Tooltip('HomePts:Q'),
            alt.Tooltip('AwayPts:Q'),
            alt.Tooltip('HomeGD:Q', title='Home GD'),
            alt.Tooltip('AwayGD:Q', title='Away GD')
        ]
    ).add_params(
        team_click
    )

    diag = alt.Chart(
        pd.DataFrame({'HomePts': [0, 50], 'AwayPts': [0, 50]})
    ).mark_line().encode(x='HomePts:Q', y='AwayPts:Q')

    q3_left = (diag + q3_scatter).properties(
        title='Home vs Away Points'
    )

    q3_bar = alt.Chart(standings).transform_filter(
        team_click
    ).transform_fold(
        ['HomePts', 'AwayPts'],
        as_=['Venue', 'Points']
    ).mark_bar().encode(
        x='Venue:N',
        y='mean(Points):Q',
        color='Venue:N'
    ).properties(
        title='Avg Pts (selected)'
    )

    q5_ref_bar = alt.Chart(matches).mark_bar().encode(
        y='Referee:N',
        x='mean(TotalCards):Q',
        color='mean(TotalFouls):Q',
        opacity=alt.condition(ref_click, alt.value(1), alt.value(0.3)),
        tooltip=[
            alt.Tooltip('Referee:N'),
            alt.Tooltip('count():Q', title='Matches'),
            alt.Tooltip('mean(TotalFouls):Q'),
            alt.Tooltip('mean(TotalYellow):Q'),
            alt.Tooltip('mean(TotalRed):Q')
        ]
    ).add_params(
        ref_click
    ).transform_filter(
        match_brush
    ).properties(
        title='Referee Card Rankings'
    )

    q5_match = alt.Chart(matches).mark_circle().encode(
        x='TotalFouls:Q',
        y='TotalCards:Q',
        color='FTR:N',
        opacity=alt.condition(match_brush, alt.value(0.7), alt.value(0.15)),
        tooltip=[
            alt.Tooltip('HomeTeam:N'),
            alt.Tooltip('AwayTeam:N'),
            alt.Tooltip('FTHG:Q', title='Home Goals'),
            alt.Tooltip('FTAG:Q', title='Away Goals'),
            alt.Tooltip('Referee:N'),
            alt.Tooltip('TotalFouls:Q'),
            alt.Tooltip('TotalCards:Q')
        ]
    ).add_params(
        match_brush
    ).transform_filter(
        ref_click
    ).properties(
        title='Match Fouls vs Cards'
    )

    return alt.vconcat(
        q1_dots,
        alt.hconcat(q3_left, q3_bar),
        alt.hconcat(q5_ref_bar, q5_match),
        spacing=50
    ).properties(
        title='English Premier League Interactive Dashboard'
    )
