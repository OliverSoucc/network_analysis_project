import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
print("Current Working Directory:", os.getcwd())

"""
-> Degree Centrality
-> Identify and visualize players based on pass involvement (in-degree, out-degree)
"""


# Define a function to calculate degree centrality and visualize the passing network
def calculate_and_plot_degree_centrality(team_file, title):
    # Load the team's passing data
    team_df = pd.read_csv(team_file)

    # Filter only rows where Type is 'PASS' and 'To' is not null
    pass_df = team_df[(team_df["Type"] == "PASS") & team_df["To"].notna()]

    # Initialize a directed graph
    G = nx.DiGraph()

    # Build the graph from passes
    for _, row in pass_df.iterrows():
        from_player = row["From"]
        to_player = row["To"]

        # Add an edge for each pass
        if G.has_edge(from_player, to_player):
            G[from_player][to_player]["weight"] += 1
        else:
            G.add_edge(from_player, to_player, weight=1)

    # Calculate in-degree and out-degree centrality
    in_degree_centrality = nx.in_degree_centrality(G)
    out_degree_centrality = nx.out_degree_centrality(G)

    # Sort players by out-degree centrality (most active passers)
    sorted_out_degree = sorted(out_degree_centrality.items(), key=lambda x: x[1], reverse=True)
    print(f"Top players by out-degree centrality in {title}:")
    for player, centrality in sorted_out_degree[:5]:  # Show top 5 players
        print(f"{player}: {centrality:.4f}")

    print("\n")

    # Sort players by in-degree centrality (most frequent pass receivers)
    sorted_in_degree = sorted(in_degree_centrality.items(), key=lambda x: x[1], reverse=True)
    print(f"Top players by in-degree centrality in {title}:")
    for player, centrality in sorted_in_degree[:5]:  # Show top 5 players
        print(f"{player}: {centrality:.4f}")

    print("\n")

    # Visualize the passing network
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, seed=42)  # Layout for consistent visualization

    # Node sizes based on out-degree centrality
    node_sizes = [out_degree_centrality[player] * 3000 for player in G.nodes]

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="lightblue", alpha=0.7)
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.5, edge_color="gray")
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    plt.title(f"{title} – Passing Network with Degree Centrality")
    plt.show(block=False)  # Show the plot without blocking the script
    plt.pause(5)           # Pause for 5 seconds before proceeding
    plt.close() 


# Paths to team files for each game and titles for each plot
team_files_titles = [
    ("data/filtered_data/teams/Sample_Game_1_Home_filtered.csv", "Game 1 – Home Team"),
    ("data/filtered_data/teams/Sample_Game_1_Away_filtered.csv", "Game 1 – Away Team"),
    ("data/filtered_data/teams/Sample_Game_2_Home_filtered.csv", "Game 2 – Home Team"),
    ("data/filtered_data/teams/Sample_Game_2_Away_filtered.csv", "Game 2 – Away Team"),
]

# Debugging: Check if the file paths exist
for team_file, title in team_files_titles:
    print(f"Checking file path: {team_file}")
    if not os.path.exists(team_file):
        print(f"File not found: {team_file}")


# Calculate and plot degree centrality for each team
for team_file, title in team_files_titles:
    calculate_and_plot_degree_centrality(team_file, title)
