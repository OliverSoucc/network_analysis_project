import pandas as pd
import os


"""
 -> filter games and keep only passing -> valid_types
"""
# Load the datasets
game1 = pd.read_csv("../data/Sample_Game_1.csv")
game2 = pd.read_csv("../data/Sample_Game_2.csv")

# Define the values to keep in the Type column
valid_types = ["PASS", "BALL LOST", "BALL OUT"]

# Filter both datasets
game1_filtered = game1[game1["Type"].isin(valid_types)]
game2_filtered = game2[game2["Type"].isin(valid_types)]

# Define the directory path
filtered_data_dir = "../data/filtered_data"

# Create the directory if it does not exist
os.makedirs(filtered_data_dir, exist_ok=True)

# Save the filtered datasets
game1_filtered.to_csv(f"{filtered_data_dir}/Sample_Game_1_filtered.csv", index=False)
game2_filtered.to_csv(f"{filtered_data_dir}/Sample_Game_2_filtered.csv", index=False)


"""
    -> device filtered passing data based on team
"""


# Load the filtered datasets for Game_1 and Game_2
game1_filtered = pd.read_csv("../data/filtered_data/Sample_Game_1_filtered.csv")
game2_filtered = pd.read_csv("../data/filtered_data/Sample_Game_2_filtered.csv")

# Define the directory to save team-specific data
team_data_dir = "../data/filtered_data/teams"
os.makedirs(team_data_dir, exist_ok=True)


# Function to filter by team and save the dataset
def save_team_data(game_df, game_name):
    teams = game_df["Team"].unique()
    for team in teams:
        team_df = game_df[game_df["Team"] == team]
        team_filename = f"{team_data_dir}/{game_name}_{team}_filtered.csv"
        team_df.to_csv(team_filename, index=False)


# Apply the function to both games
save_team_data(game1_filtered, "Sample_Game_1")
save_team_data(game2_filtered, "Sample_Game_2")
