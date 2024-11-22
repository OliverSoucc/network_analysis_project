import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

"""
-> Closeness Centrality
-> Identify players with quick access to others in the passing network
"""

def calculate_and_plot_closeness_centrality(team_file, title):
    # Load the team's passing data
    team_df = pd.read_csv(team_file)
    
    # Filter rows where Type is 'PASS' and 'To' is not null
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
    
    # Calculate closeness centrality
    closeness_centrality = nx.closeness_centrality(G)
    
    # Sort players by closeness centrality to display the top ones
    sorted_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)
    print(f"Top players by closeness centrality in {title}:")
    for player, centrality in sorted_closeness[:5]:  # Show top 5 players
        print(f"{player}: {centrality:.4f}")
    print("\n")
    
    # Visualize the passing network
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, seed=42)  # Layout for consistent visualization
    node_sizes = [closeness_centrality[player] * 3000 for player in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="lightgreen", alpha=0.7)
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.5, edge_color="gray")
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")
    plt.title(f"{title} – Passing Network with Closeness Centrality")
    
    # Show or save the plot
    plt.show(block=False)  # Non-blocking visualization
    plt.pause(5)
    plt.close()
    

# Paths to team files for each game and titles for each plot
team_files_titles = [
    ("data/filtered_data/teams/Sample_Game_1_Home_filtered.csv", "Game 1 – Home Team"),
    ("data/filtered_data/teams/Sample_Game_1_Away_filtered.csv", "Game 1 – Away Team"),
    ("data/filtered_data/teams/Sample_Game_2_Home_filtered.csv", "Game 2 – Home Team"),
    ("data/filtered_data/teams/Sample_Game_2_Away_filtered.csv", "Game 2 – Away Team"),
]

# Calculate and plot closeness centrality for each team
for team_file, title in team_files_titles:
    calculate_and_plot_closeness_centrality(team_file, title)
