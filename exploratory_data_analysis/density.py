def calculate_graph_density(filepath: str, title: str):
    """
        Density
        Team Passing Cohesion
    """
    import networkx as nx
    from helper_functions import get_passes_df

    pass_df = get_passes_df(filepath)
    G = nx.DiGraph()

    # Build the graph from passes, without weights
    for _, row in pass_df.iterrows():
        from_player = row["From"]
        to_player = row["To"]

        # Add an edge between players if it doesn't already exist
        G.add_edge(from_player, to_player)

    # Calculate graph density
    density = nx.density(G)

    # Display graph density
    print(f"Graph Density (Team Passing Cohesion) for {title}: {density:.4f}\n")

def display_density():
    from constants import TEAMS
    # Calculate and display graph density for each team
    for team_file, title in TEAMS:
        calculate_graph_density(team_file, title)
