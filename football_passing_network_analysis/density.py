import pandas as pd
import networkx as nx

'''
    -> Density
    -> Team Passing Cohesion
'''

# Define a function to calculate and display graph density for a team
def calculate_graph_density(team_file, title):
    # Load the team's passing data
    team_df = pd.read_csv(team_file)

    # Filter only rows where Type is 'PASS' and 'To' is not null
    pass_df = team_df[(team_df['Type'] == 'PASS') & team_df['To'].notna()]

    # Initialize a directed graph
    G = nx.DiGraph()

    # Build the graph from passes, without weights
    for _, row in pass_df.iterrows():
        from_player = row['From']
        to_player = row['To']

        # Add an edge between players if it doesn't already exist
        G.add_edge(from_player, to_player)

    # Calculate graph density
    density = nx.density(G)

    # Display graph density
    print(f"Graph Density (Team Passing Cohesion) for {title}: {density:.4f}\n")


# Paths to team files for each game and titles for each result
team_files_titles = [
    ('../data/filtered_data/teams/Sample_Game_1_Home_filtered.csv', "Game 1 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_1_Away_filtered.csv', "Game 1 - Away Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Home_filtered.csv', "Game 2 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Away_filtered.csv', "Game 2 - Away Team")
]

# Calculate and display graph density for each team
for team_file, title in team_files_titles:
    calculate_graph_density(team_file, title)
