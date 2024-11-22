import pandas as pd
import networkx as nx
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

def calculate_and_classify_roles(team_file, title):
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
        if G.has_edge(from_player, to_player):
            G[from_player][to_player]["weight"] += 1
        else:
            G.add_edge(from_player, to_player, weight=1)
    
    # Calculate centralities
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G, weight="weight", normalized=True)
    closeness_centrality = nx.closeness_centrality(G)
    
    # Create a DataFrame for classification
    centrality_data = pd.DataFrame({
        "Player": list(G.nodes),
        "Degree Centrality": [degree_centrality[node] for node in G.nodes],
        "Betweenness Centrality": [betweenness_centrality[node] for node in G.nodes],
        "Closeness Centrality": [closeness_centrality[node] for node in G.nodes],
    })
    
    # Normalize the centrality values
    scaler = MinMaxScaler()
    centrality_data.iloc[:, 1:] = scaler.fit_transform(centrality_data.iloc[:, 1:])
    
    # Define player roles
    def classify(row):
        if row["Degree Centrality"] > 0.8 and row["Closeness Centrality"] > 0.7:
            return "Playmaker"
        elif row["Betweenness Centrality"] > 0.7:
            return "Linker"
        elif row["Degree Centrality"] > 0.6 and row["Closeness Centrality"] > 0.6:
            return "Hub"
        elif row["Degree Centrality"] < 0.3 and row["Closeness Centrality"] < 0.3:
            return "Peripheral Player"
        elif row["Closeness Centrality"] > 0.5 and row["Degree Centrality"] < 0.4:
            return "Target Player"
        else:
            return "General Player"
    
    centrality_data["Role"] = centrality_data.apply(classify, axis=1)
    
    # Visualize the roles in the passing network
    visualize_roles(G, centrality_data, title)
    
    # Return the classification results
    return centrality_data

def visualize_roles(graph, roles_df, title):
    pos = nx.spring_layout(graph, seed=42)
    role_colors = {
        "Playmaker": "green",
        "Linker": "blue",
        "Hub": "orange",
        "Target Player": "red",
        "Peripheral Player": "purple",
        "General Player": "gray"
    }
    node_colors = [role_colors[roles_df.loc[roles_df['Player'] == node, 'Role'].values[0]] for node in graph.nodes]
    
    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=500, alpha=0.8)
    nx.draw_networkx_edges(graph, pos, edge_color="gray", alpha=0.5)
    nx.draw_networkx_labels(graph, pos, font_size=10, font_color="black")
    plt.title(f"{title} - Player Roles in Passing Network")
    plt.show()

# Paths to team files for each game
team_files_titles = [
    ("data/filtered_data/teams/Sample_Game_1_Home_filtered.csv", "Game 1 – Home Team"),
    ("data/filtered_data/teams/Sample_Game_1_Away_filtered.csv", "Game 1 – Away Team"),
    ("data/filtered_data/teams/Sample_Game_2_Home_filtered.csv", "Game 2 – Home Team"),
    ("data/filtered_data/teams/Sample_Game_2_Away_filtered.csv", "Game 2 – Away Team"),
]

# Perform role identification for each team
for team_file, title in team_files_titles:
    roles = calculate_and_classify_roles(team_file, title)
    print(f"\nPlayer Roles in {title}:\n", roles)
