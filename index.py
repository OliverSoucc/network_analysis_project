import networkx as nx
import pandas as pd
import community.community_louvain as community_louvain  # Correct import for Louvain
from analysis.cost_function_weight import (
    optimize_custom_cost,
    calculate_pass_distance,
    calculate_pass_success_rate,
    calculate_pass_frequency,
    calculate_custom_cost,
)

data = []

def prepare_data():
    optimized_weights = optimize_custom_cost("hh", "title")
    team_df = pd.read_csv("hh")

    # Filter only rows where Type is 'PASS'
    pass_df = team_df[team_df['Type'] == 'PASS'].copy()

    # Calculate distance for each pass
    pass_df['Distance'] = pass_df.apply(calculate_pass_distance, axis=1)

    # Calculate success rate for each player
    success_rate = calculate_pass_success_rate(team_df)

    # Calculate frequency of passes between players
    pass_frequency = calculate_pass_frequency(pass_df)

    # Normalize distance feature
    max_distance = pass_df['Distance'].max()

    pass_df['Custom Weight'] = pass_df.apply(
        calculate_custom_cost,
        axis=1,
        max_distance=max_distance,
        success_rate=success_rate,
        pass_frequency=pass_frequency,
        weights=optimized_weights
    )

    return pass_df


class FootballGraph():
    def __init__(self) -> None:
        self.df = prepare_data()
        self.G = nx.DiGraph()



    # done
    def get_betweenness_centrality(self):
        for _, row in self.df.iterrows():
            self.G.add_edge(row['From'], row['To'], weight=row['Custom Weight'])

        return nx.betweenness_centrality(self.G, weight='weight', normalized=True)

    # done
    def get_closeness_centrality(self):
        for _, row in self.df.iterrows():
            self.G.add_edge(row['From'], row['To'], weight=row['Custom Weight'])

        if not nx.is_weakly_connected(self.G):
            print(f"Warning: The graph for {title} is not fully connected. Results may be inaccurate.")

        # Calculate closeness centrality
        closeness_centrality = nx.closeness_centrality(self.G, distance='weight')
        return closeness_centrality

    # done
    def get_degree_centrality(self):
        # Add edges (passes) to the graph with weights
        teams = self.df['Team'].unique() # type: ignore

        for team in teams:
            team_passes = self.df[self.df['Team'] == team]
            for _, row in team_passes.iterrows():
                from_player = row['From']
                to_player = row['To']
                if self.G.has_edge(from_player, to_player):
                    self.G[from_player][to_player]['weight'] += 1  # Pass frequency as weight
                else:
                    self.G.add_edge(from_player, to_player, weight=1)

            weighted_in_degree = {node: sum(edge["weight"] for _, _, edge in self.G.in_edges(node, data=True)) for node in self.G.nodes()}
            weighted_out_degree = {node: sum(edge["weight"] for _, _, edge in self.G.out_edges(node, data=True)) for node in self.G.nodes()}
            weighted_total_degree = {node: weighted_in_degree[node] + weighted_out_degree[node] for node in self.G.nodes()}

    # done
    def get_clustering_coefficient(self):
        # Get the unique teams
        teams = self.df['Team'].unique()

        # Calculate clustering coefficients for each team
        for team in teams:
            team_passes = self.df[self.df['Team'] == team]

            # Create an undirected graph with weights
            G = nx.Graph()

            # Add weighted edges (passes) to the graph
            for _, row in team_passes.iterrows():
                from_player = row['From']
                to_player = row['To']
                if G.has_edge(from_player, to_player):
                    G[from_player][to_player]['weight'] += 1
                else:
                    G.add_edge(from_player, to_player, weight=1)

            # Calculate local clustering coefficients (weighted)
            local_clustering = nx.clustering(G, weight="weight")

            # Calculate average clustering coefficient (weighted)
            avg_clustering = sum(local_clustering.values()) / len(local_clustering) if local_clustering else 0

            return avg_clustering

    def display_communities(self):
        # Initialize an undirected graph (community detection works well with undirected graphs)
        G = nx.Graph()

        # Build the graph from passes
        for _, row in self.df.iterrows():
            from_player = row["From"]
            to_player = row["To"]

            # Add or update the edge weight for each pass
            if G.has_edge(from_player, to_player):
                G[from_player][to_player]["weight"] += 1
            else:
                G.add_edge(from_player, to_player, weight=1)

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







