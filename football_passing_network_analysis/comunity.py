import matplotlib
import pandas as pd
import networkx as nx
import community.community_louvain as community_louvain  # Correct import for Louvain
import matplotlib.pyplot as plt
import random
import numpy as np

"""
 -> Community Detection (Identifying Subgroups in Teams)
 -> we used Louvain algorithm
"""

# Set a fixed seed for reproducibility
random.seed(42)
np.random.seed(42)


# Define a function to detect communities within the passing network
def detect_communities(team_file, title):
    # Load the team's passing data
    team_df = pd.read_csv(team_file)

    # Filter only rows where Type is 'PASS' and 'To' is not null
    pass_df = team_df[(team_df["Type"] == "PASS") & team_df["To"].notna()]

    # Initialize an undirected graph (community detection works well with undirected graphs)
    G = nx.Graph()

    # Build the graph from passes
    for _, row in pass_df.iterrows():
        from_player = row["From"]
        to_player = row["To"]

        # Add or update the edge weight for each pass
        if G.has_edge(from_player, to_player):
            G[from_player][to_player]["weight"] += 1
        else:
            G.add_edge(from_player, to_player, weight=1)

    # Apply Louvain community detection algorithm
    partition = community_louvain.best_partition(G, weight="weight")

    # Extract the unique communities detected
    communities = {}
    for player, community in partition.items():
        if community not in communities:
            communities[community] = []
        communities[community].append(player)

    # Display the communities
    print(f"Communities detected in {title}:")
    for community, players in communities.items():
        print(f"Community {community + 1}: {', '.join(players)}")
    print("\n")

    # Visualize the communities on the passing network
    pos = nx.spring_layout(G, seed=42)  # Use a fixed layout for consistency
    plt.figure(figsize=(10, 7))

    # Prepare color mapping for each community as hex colors
    cmap = plt.get_cmap("viridis", max(partition.values()) + 1)
    node_colors = [cmap(partition[player])[:3] for player in G.nodes]  # Get RGB values
    node_colors = [
        matplotlib.colors.to_hex(color) for color in node_colors
    ]  # Convert to hex

    # Draw nodes with colors based on community membership
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color=node_colors, alpha=0.8)
    nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color="gray")
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    plt.title(f"{title} - Community Detection in Passing Network")
    plt.show()


# Paths to team files for each game and titles for each plot
team_files_titles = [
    (
        "../data/filtered_data/teams/Sample_Game_1_Home_filtered.csv",
        "Game 1 - Home Team",
    ),
    (
        "../data/filtered_data/teams/Sample_Game_1_Away_filtered.csv",
        "Game 1 - Away Team",
    ),
    (
        "../data/filtered_data/teams/Sample_Game_2_Home_filtered.csv",
        "Game 2 - Home Team",
    ),
    (
        "../data/filtered_data/teams/Sample_Game_2_Away_filtered.csv",
        "Game 2 - Away Team",
    ),
]

# Detect and display communities for each team
for team_file, title in team_files_titles:
    detect_communities(team_file, title)
