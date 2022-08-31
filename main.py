from pybaseball import batting_stats_range, pitching_stats_range, schedule_and_record
import pandas as pd


def get_team_record(year, team, month):
    bal = schedule_and_record(year, team)
    bal = bal[bal["Date"].str.contains(month)]

    wins = bal["W/L"].str.count("W").sum()
    loss = bal["W/L"].str.count("L").sum()

    return {"W/L": format(round(wins / loss, 3), '.3f')}


def get_batting_stats(start_date, end_date):  # YYYY-MM-DD
    batting_df = batting_stats_range(start_date, end_date)
    batting_df = batting_df.loc[batting_df["Tm"] == "Baltimore"]

    players = batting_df["Name"].unique()
    d = {}

    for p in players:
        stats = batting_df[batting_df["Name"] == p]
        stats = stats.reset_index(drop=True)

        name = stats["Name"].item()
        g = stats["G"].item()
        ba = format(round(stats["BA"].item(), 3), '.3f')
        obp = format(round(stats["OBP"].item(), 3), '.3f')
        slg = format(round(stats["SLG"].item(), 3), '.3f')
        ops = format(round(stats["OPS"].item(), 3), '.3f')

        d[name] = f"G: {g} - {ba}/ {obp}/ {slg}/ {ops}"

    return d


def get_pitching_stats(start_date, end_date):  # YYYY-MM-DD
    pitching_df = pitching_stats_range(start_date, end_date)
    pitching_df = pitching_df.loc[pitching_df["Tm"] == "Baltimore"]

    pd.set_option('display.max_columns', None)

    players = pitching_df["Name"].unique()
    d = {}

    for p in players:
        stats = pitching_df[pitching_df["Name"] == p]
        stats = stats.reset_index(drop=True)

        name = stats["Name"].item()
        ip = stats["IP"].item()
        era = format(round(stats["ERA"].item(), 3), '.3f')
        whip = format(round(stats["WHIP"].item(), 3), '.3f')
        so = stats["SO"].item()
        bb = stats["BB"].item()

        d[name] = f"{ip} IP/ {era} ERA/ {whip} WHIP/ {so}:{bb} SO:BB"

    return d


if __name__ == "__main__":
    batting = get_batting_stats("2022-08-01", "2022-08-31")
    pitching = get_pitching_stats("2022-08-01", "2022-08-31")
    wl = get_team_record(2022, "BAL", "Aug")

    wl_df = pd.DataFrame.from_dict(wl, orient="index")
    batting_df = pd.DataFrame.from_dict(batting, orient="index")
    pitching_df = pd.DataFrame.from_dict(pitching, orient="index")
    result_df = pd.concat([wl_df, batting_df, pitching_df])

    result_df.to_csv("baltimore.csv")

