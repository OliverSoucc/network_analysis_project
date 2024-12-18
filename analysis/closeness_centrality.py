import pandas as pd
import networkx as nx
from analysis.cost_function_weight import (
    optimize_custom_cost,
    calculate_pass_success_rate,
    calculate_pass_frequency,
    calculate_custom_cost,
)
from helper_functions import build_graph, calculate_pass_distance, get_passes_df


def calculate_closeness_centrality(path: str, title: str, optimized_weights):
    '''
        tu by mali byt values pre kazdeho hraca medzi [0, 1] (normalizovane), a nie som si uplne isty preco nie su
        dat tomu 10 minut, ak sa nepodari fixnut, vymazat -> mame toho dost
    '''
    pass_df = get_passes_df(path)

    if isinstance(pass_df, int) and pass_df == -1:
        raise Exception("Error")

    pass_df['Distance'] = pass_df.apply(calculate_pass_distance, axis=1)

    success_rate = calculate_pass_success_rate(pd.read_csv(path))
    pass_frequency = calculate_pass_frequency(pass_df)

    # Normalize distance feature
    max_distance = pass_df['Distance'].max()

    # Calculate custom weights for each pass
    pass_df['Custom Weight'] = pass_df.apply(
        calculate_custom_cost,
        axis=1,
        max_distance=max_distance,
        success_rate=success_rate,
        pass_frequency=pass_frequency,
        weights=optimized_weights
    )

    # Normalize custom weights
    min_weight = pass_df['Custom Weight'].min()
    max_weight = pass_df['Custom Weight'].max()
    pass_df['Custom Weight'] = (pass_df['Custom Weight'] - min_weight) / (max_weight - min_weight) if max_weight > min_weight else pass_df['Custom Weight']

    G = build_graph(pass_df, mode='c', graph=nx.DiGraph())

    if not nx.is_weakly_connected(G):
        print(f"Warning: The graph for {title} is not fully connected. Results may be inaccurate.")

    closeness_centrality = nx.closeness_centrality(G, distance='weight')

    print(f"Closeness Centrality for {title}:")
    for player, centrality in sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True):
        print(f"  {player}: {centrality:.4f}")

    return closeness_centrality


def display_closeness_centrality():
    from constants import TEAMS
    # Perform closeness centrality analysis for each team
    for team_file, title in TEAMS:
        optimized_weights = optimize_custom_cost(team_file)
        calculate_closeness_centrality(team_file, title, optimized_weights)
