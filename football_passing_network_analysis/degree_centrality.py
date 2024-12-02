import pandas as pd
import networkx as nx

'''
 -> Degree centrality
    -> Basically density for each individual node 
    -> (in-degree, out-degree, total degree)
    -> weights are NOT from cost_function
'''


# Define a function to calculate weighted degree centrality for each team
def calculate_weighted_degree_centrality(team_file, title):
    # Load the passing dataset
    team_df = pd.read_csv(team_file)

    # Filter only rows where Type is 'PASS' and drop rows with missing values
    pass_df = team_df[(team_df['Type'] == 'PASS') & team_df['From'].notna() & team_df['To'].notna()]

    # Get the unique teams
    teams = pass_df['Team'].unique()

    for team in teams:
        team_passes = pass_df[pass_df['Team'] == team]

        # Create a directed graph with weights
        G = nx.DiGraph()

        # Add edges (passes) to the graph with weights
        for _, row in team_passes.iterrows():
            from_player = row['From']
            to_player = row['To']
            if G.has_edge(from_player, to_player):
                G[from_player][to_player]['weight'] += 1  # Pass frequency as weight
            else:
                G.add_edge(from_player, to_player, weight=1)

        # Calculate weighted degree centrality
        weighted_in_degree = {node: sum(edge["weight"] for _, _, edge in G.in_edges(node, data=True)) for node in G.nodes()}
        weighted_out_degree = {node: sum(edge["weight"] for _, _, edge in G.out_edges(node, data=True)) for node in G.nodes()}
        weighted_total_degree = {node: weighted_in_degree[node] + weighted_out_degree[node] for node in G.nodes()}

        # Display results
        print(f"Weighted Degree Centrality for {title} - {team}:")
        print("  Weighted In-Degree:")
        for player, centrality in sorted(weighted_in_degree.items(), key=lambda x: x[1], reverse=True):
            print(f"    {player}: {centrality:.4f}")

        print("  Weighted Out-Degree:")
        for player, centrality in sorted(weighted_out_degree.items(), key=lambda x: x[1], reverse=True):
            print(f"    {player}: {centrality:.4f}")

        print("  Weighted Total Degree:")
        for player, centrality in sorted(weighted_total_degree.items(), key=lambda x: x[1], reverse=True):
            print(f"    {player}: {centrality:.4f}")
        print()

# Array of file paths and corresponding titles
team_files_titles = [
    ('../data/filtered_data/teams/Sample_Game_1_Home_filtered.csv', "Game 1 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_1_Away_filtered.csv', "Game 1 - Away Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Home_filtered.csv', "Game 2 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Away_filtered.csv', "Game 2 - Away Team")
]

# Calculate weighted degree centrality for each team
for team_file, title in team_files_titles:
    calculate_weighted_degree_centrality(team_file, title)


