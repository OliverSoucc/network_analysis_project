import networkx as nx

# Define a function to calculate clustering coefficients for each team
def calculate_weighted_clustering_coefficients(path: str, title: str):
    '''
        -> Average CC (weighted)
            -> average over all nodes, how likely they create triangles with their neighbours
            -> weights are NOT from cost_function
    '''
    from helper_functions import build_graph, get_passes_df

    pass_df = get_passes_df(path)
    assert pass_df != -1

    # Get the unique teams
    teams = pass_df['Team'].unique()

    # Calculate clustering coefficients for each team
    for team in teams:
        G = build_graph(pass_df, mode='p', graph=nx.Graph())

        # Calculate local clustering coefficients (weighted)
        local_clustering = nx.clustering(G, weight="weight")

        # Calculate average clustering coefficient (weighted)
        avg_clustering = sum(local_clustering.values()) / len(local_clustering) if local_clustering else 0

        # Display the results
        print(f"Results for {title} - {team}:")
        print(f"  Average Clustering Coefficient: {avg_clustering:.4f}")
        print("  Local Clustering Coefficients:")
        for player, clustering in local_clustering.items():
            print(f"    {player}: {clustering:.4f}")

def display_clustering_coefficient():
    from constants import TEAMS
    # Calculate weighted clustering coefficients for each team in each file
    for team_file, title in TEAMS:
        calculate_weighted_clustering_coefficients(team_file, title)
