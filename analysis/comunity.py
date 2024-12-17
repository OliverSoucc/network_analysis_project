

def detect_communities_with_modularity(filepath: str, title):
    """
     - Community Detection (Identifying Subgroups in Teams)
     - Modularity (evaluation of Community detection)
     - we used Louvain algorithm
    """
    import matplotlib
    import networkx as nx
    import community.community_louvain as community_louvain
    import matplotlib.pyplot as plt
    from helper_functions import build_graph, get_passes_df

    pass_df = get_passes_df(filepath)
    assert pass_df != -1
    G = build_graph(pass_df, mode='p', graph=nx.Graph())

    # Apply Louvain community detection algorithm
    partition = community_louvain.best_partition(G, weight="weight")

    # Calculate modularity
    modularity = community_louvain.modularity(partition, G, weight="weight")
    print(f"Modularity for {title}: {modularity:.4f}")

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


def display_comunity():
    from constants import TEAMS
    # Detect and display communities and modularity for each team
    for team_file, title in TEAMS:
        detect_communities_with_modularity(team_file, title)

