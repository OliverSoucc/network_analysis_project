import pandas as pd
import networkx as nx

'''
    -> Average CC (weighted)
        -> average over all nodes, how likely they create triangles with their neighbours
        -> weights are NOT from cost_function
'''

# Define a function to calculate clustering coefficients for each team
def calculate_weighted_clustering_coefficients(team_file, title):
    # Load the passing dataset
    team_df = pd.read_csv(team_file)

    # Filter only rows where Type is 'PASS' and drop rows with missing values
    pass_df = team_df[(team_df['Type'] == 'PASS') & team_df['From'].notna() & team_df['To'].notna()]

    # Get the unique teams
    teams = pass_df['Team'].unique()

    # Calculate clustering coefficients for each team
    for team in teams:
        team_passes = pass_df[pass_df['Team'] == team]

        # Create an undirected graph with weights
        G = nx.Graph()

        # Add weighted edges (passes) to the graph
        for _, row in team_passes.iterrows():
            from_player = row['From']
            to_player = row['To']
            if G.has_edge(from_player, to_player):
                G[from_player][to_player]['weight'] += 1
            else:
                G.add_edge(from_player, to_player, weight=1)

        # Calculate local clustering coefficients (weighted)
        local_clustering = nx.clustering(G, weight="weight")

        # Calculate average clustering coefficient (weighted)
        avg_clustering = sum(local_clustering.values()) / len(local_clustering) if local_clustering else 0

        # Display the results
        print(f"Results for {title} - {team}:")
        print(f"  Average Clustering Coefficient: {avg_clustering:.4f}")
        print("  Local Clustering Coefficients:")
        for player, clustering in local_clustering.items():
            print(f"    {player}: {clustering:.4f}")
        print()

# Array of file paths and corresponding titles
team_files_titles = [
    ('../data/filtered_data/teams/Sample_Game_1_Home_filtered.csv', "Game 1 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_1_Away_filtered.csv', "Game 1 - Away Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Home_filtered.csv', "Game 2 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Away_filtered.csv', "Game 2 - Away Team")
]

# Calculate weighted clustering coefficients for each team in each file
for team_file, title in team_files_titles:
    calculate_weighted_clustering_coefficients(team_file, title)
