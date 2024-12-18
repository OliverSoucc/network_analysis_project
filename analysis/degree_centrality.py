def calculate_weighted_degree_centrality(filepath: str, title: str):
    '''
     Degree centrality
     - Basically density for each individual node
     - (in-degree, out-degree, total degree)
     - weights are NOT from cost_function
    '''
    import networkx as nx
    from helper_functions import build_graph, get_passes_df

    pass_df = get_passes_df(filepath)

    if isinstance(pass_df, int) and pass_df == -1:
        raise Exception("Error")

    teams = pass_df['Team'].unique()

    G = build_graph(pass_df, mode='p', graph=nx.DiGraph())

    for team in teams:
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

def display_degree_centrality():
    from constants import TEAMS
    # Calculate weighted degree centrality for each team
    for team_file, title in TEAMS:
        calculate_weighted_degree_centrality(team_file, title)


