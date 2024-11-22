import pandas as pd
import os

# Paths to all team files
team_files = [
    ("data/filtered_data/teams/Sample_Game_1_Home_filtered.csv", "Game_1_Home"),
    ("data/filtered_data/teams/Sample_Game_1_Away_filtered.csv", "Game_1_Away"),
    ("data/filtered_data/teams/Sample_Game_2_Home_filtered.csv", "Game_2_Home"),
    ("data/filtered_data/teams/Sample_Game_2_Away_filtered.csv", "Game_2_Away"),
]

# Function to prepare data for Gephi
def prepare_data_for_gephi(team_file, team_title):
    # Load the passing data for the team
    team_data = pd.read_csv(team_file)

    # Filter only rows where the type is 'PASS'
    pass_data = team_data[team_data["Type"] == "PASS"]

    # Group by 'From' and 'To' to calculate weights
    edge_data = pass_data.groupby(["From", "To"]).size().reset_index(name="Weight")

    # Rename columns to match Gephi's expected format
    edge_data.rename(columns={"From": "Source", "To": "Target"}, inplace=True)

    # Save the edge file for this team
    os.makedirs("data_for_gephi", exist_ok=True)
    edge_data.to_csv(f"data_for_gephi/edges_{team_title}.csv", index=False)

    # Create nodes for this team (unique players)
    nodes = set(edge_data["Source"]).union(set(edge_data["Target"]))
    node_data = pd.DataFrame({"ID": list(nodes), "Label": list(nodes)})

    # Save the node file for this team
    node_data.to_csv(f"data_for_gephi/nodes_{team_title}.csv", index=False)

# Loop through each team file
for team_file, team_title in team_files:
    prepare_data_for_gephi(team_file, team_title)

print("Separate files for each team and game have been created.")