import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


"""
 -> ZDA SA ZE TOTO SA NEBUDE DAT POUZIT KVOLI SHORTEST PATH
 -> Node Betweenness Centrality
 -> identify and visualize players who act as key playmakers in the passing network
"""


# Define a function to calculate betweenness centrality and visualize the passing network
def calculate_and_plot_betweenness(team_file, title):
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

        # Add or update the edge weight for each pass
        if G.has_edge(from_player, to_player):
            G[from_player][to_player]["weight"] += 1
        else:
            G.add_edge(from_player, to_player, weight=1)

    # Calculate betweenness centrality for all nodes (players)
    betweenness_centrality = nx.betweenness_centrality(
        G, weight="weight", normalized=True
    )

    # Sort players by betweenness centrality to display the top ones
    sorted_betweenness = sorted(
        betweenness_centrality.items(), key=lambda x: x[1], reverse=True
    )
    print(f"Top players by betweenness centrality in {title}:")
    for player, centrality in sorted_betweenness[:5]:  # Show top 5 players
        print(f"{player}: {centrality:.4f}")
    print("\n")

    # Visualize the passing network
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, seed=42)  # Layout for consistent visualization
    node_sizes = [
        betweenness_centrality[player] * 3000 for player in G.nodes
    ]  # Scale size by betweenness

    # Draw nodes with size based on betweenness centrality
    nx.draw_networkx_nodes(
        G, pos, node_size=node_sizes, node_color="skyblue", alpha=0.7
    )
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.5, edge_color="gray")
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    plt.title(f"{title} - Passing Network with Betweenness Centrality")
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

# Calculate and plot betweenness centrality for each team
for team_file, title in team_files_titles:
    calculate_and_plot_betweenness(team_file, title)
