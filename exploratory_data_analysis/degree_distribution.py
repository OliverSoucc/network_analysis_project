import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

'''
 -> Graph nodes vs edges
'''

# Define a function to create an unweighted degree distribution plot
def degree_distribution_plot_unweighted(team_file, title):
    # Load the passing dataset
    team_df = pd.read_csv(team_file)

    # Filter only rows where Type is 'PASS' and drop rows with missing values
    pass_df = team_df[(team_df['Type'] == 'PASS') & team_df['From'].notna() & team_df['To'].notna()]

    # Get the unique teams
    teams = pass_df['Team'].unique()

    for team in teams:
        team_passes = pass_df[pass_df['Team'] == team]

        # Create a directed graph (without weights)
        G = nx.DiGraph()

        # Add edges (passes) to the graph
        for _, row in team_passes.iterrows():
            from_player = row['From']
            to_player = row['To']
            G.add_edge(from_player, to_player)  # No weights added

        # Get degrees (unweighted)
        degrees = [degree for _, degree in G.degree()]
        max_degree = max(degrees)

        # Degree distribution plot
        plt.figure(figsize=(10, 6))
        plt.hist(degrees, bins=np.arange(0, max_degree + 2) - 0.5, alpha=0.75, color='blue', edgecolor='black')
        plt.title(f"Unweighted Degree Distribution - {title} - {team}")
        plt.xlabel("Degree")
        plt.ylabel("Number of Nodes (Players)")
        plt.grid()
        plt.show()

# Array of file paths and corresponding titles
team_files_titles = [
    ('../data/filtered_data/teams/Sample_Game_1_Home_filtered.csv', "Game 1 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_1_Away_filtered.csv', "Game 1 - Away Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Home_filtered.csv', "Game 2 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Away_filtered.csv', "Game 2 - Away Team")
]

# Create degree distribution plots for each team
for team_file, title in team_files_titles:
    degree_distribution_plot_unweighted(team_file, title)


