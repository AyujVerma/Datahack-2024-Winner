import pandas as pd  # type: ignore
import numpy as np
from collections import defaultdict

BID_COL = "Bid Amount($)"


def simulate_bidding(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Simulate bidding process and return results.
    Takes a DataFrame with the following columns:
    - "Team Name": Name of the datahack team
    - "Submission DataFrame": DataFrame with columns "Name" (player name) and "Bid Amount($)"

    Returns "results" DataFrame with the following columns:
    - "Team Name": Name of the datahack team
    - "Players Won": List of players won by the team

    Returns "bidding" DataFrame with the following columns:
    - "Bid Amount($)": Bid amount of the player
    - "Team Name": Name of the datahack team
    - "Player Name": Name of the player
    - "Rand": Random number used to break ties
    - "Won?": Whether the player was won by the team
    """

    def format(x: pd.Series) -> None:
        submission_df: pd.DataFrame = x["Submission DataFrame"]

        # Add team name
        submission_df["Team Name"] = x["Team Name"]
        submission_df.set_index("Name", inplace=True)
        submission_df["Player Name"] = submission_df.index

        submission_df[BID_COL] = submission_df[BID_COL].astype(float)
        submission_df[BID_COL] *= 200.0 / submission_df[BID_COL].sum()

    df.apply(format, axis=1)

    # Run bids
    bidding_df = pd.concat(list(df["Submission DataFrame"]), ignore_index=True)
    bidding_df["Rand"] = np.random.rand(bidding_df.shape[0])

    # Sort by bid amount then random to break ties
    bidding_df.sort_values([BID_COL, "Rand"], ascending=False, inplace=True)

    bidding_df["Won?"] = False
    taken_players_set: set[str] = set()
    players_won_count: dict[str, int] = defaultdict(int)  # default = 0

    # Start bidding
    for i, row in bidding_df.iterrows():
        player_name = row["Player Name"]
        if player_name in taken_players_set:  # skip if already taken
            continue
        if players_won_count[row["Team Name"]] == 3:  # skip if already won 3 players
            continue

        bidding_df.loc[i, "Won?"] = True
        taken_players_set.add(player_name)
        players_won_count[row["Team Name"]] += 1

    # Convert to list of won players for each team
    won_players_df = (
        bidding_df.loc[bidding_df["Won?"], ["Won?", "Team Name", "Player Name"]]
        .groupby("Team Name")
        .agg(list)
    )
    won_players_df.rename(columns={"Player Name": "Players Won"}, inplace=True)
    won_players_df["Players Won"] = won_players_df["Players Won"].apply(sorted)

    # Join results and return
    final_results = df.join(won_players_df, on="Team Name", how="left", rsuffix="_bids")
    final_results = final_results[["Team Name", "Players Won"]]
    return final_results, bidding_df


if __name__ == "__main__":
    team_1_bids = pd.DataFrame(
        [
            {"Name": "Pedro Severino", "Bid Amount($)": 2.0},
            {"Name": "Ryan Buchter", "Bid Amount($)": 2.0},
            {"Name": "Akeel Morris", "Bid Amount($)": 2.0},
            {"Name": "Lee Gronkiewicz", "Bid Amount($)": 1.0},
            {"Name": "Chris McGuiness", "Bid Amount($)": 1.0},
            {"Name": "Drew Meyer", "Bid Amount($)": 1.0},
        ]
    )
    team_2_bids = pd.DataFrame(
        [
            {"Name": "Pedro Severino", "Bid Amount($)": 1.0},
            {"Name": "Ryan Buchter", "Bid Amount($)": 1.0},
            {"Name": "Akeel Morris", "Bid Amount($)": 1.0},
            {"Name": "Lee Gronkiewicz", "Bid Amount($)": 2.0},
            {"Name": "Chris McGuiness", "Bid Amount($)": 2.0},
            {"Name": "Drew Meyer", "Bid Amount($)": 2.0},
        ]
    )

    df = pd.DataFrame(
        [
            {"Team Name": "Team 1", "Submission DataFrame": team_1_bids},
            {"Team Name": "Team 2", "Submission DataFrame": team_2_bids},
        ]
    )
    results, bidding_df = simulate_bidding(df)
    results.to_csv("results.csv", index=False)
    bidding_df.to_csv("bidding.csv", index=False)
