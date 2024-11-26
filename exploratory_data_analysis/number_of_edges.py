import pandas as pd
import networkx as nx

# Define a function to calculate the number of edges for each team
def calculate_team_edges(team_file):
    # Load the passing dataset
    team_df = pd.read_csv(team_file)

    # Filter only rows where Type is 'PASS' and drop rows with missing values
    pass_df = team_df[(team_df['Type'] == 'PASS') & team_df['From'].notna() & team_df['To'].notna()]

    # Get the unique teams
    teams = pass_df['Team'].unique()

    # Initialize a dictionary to store the number of edges for each team
    team_edges = {}

    # Calculate the number of edges for each team
    for team in teams:
        team_passes = pass_df[pass_df['Team'] == team]

        # Create a directed graph
        G = nx.DiGraph()

        # Add edges (passes) to the graph
        for _, row in team_passes.iterrows():
            from_player = row['From']
            to_player = row['To']
            G.add_edge(from_player, to_player)

        # Store the number of edges for the team
        team_edges = G.number_of_edges()

    return team_edges


team_files = [
    ('../data/filtered_data/teams/Sample_Game_1_Home_filtered.csv', "Game 1 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_1_Away_filtered.csv', "Game 1 - Away Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Home_filtered.csv', "Game 2 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Away_filtered.csv', "Game 2 - Away Team")
]

# Loop through each file and calculate edges
for file_path, team in team_files:
    team_edges = calculate_team_edges(file_path)
    print(f"{team}: {team_edges} edges")


