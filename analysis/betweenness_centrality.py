def calculate_betweenness_centrality(path: str, title: str, optimized_weights):
    """
     Identify and visualize players who act as key playmakers in the passing network.
    """
    from helper_functions import build_graph, calculate_pass_distance, get_passes_df
    import pandas as pd
    import networkx as nx
    from analysis.cost_function_weight import (
        calculate_pass_success_rate,
        calculate_pass_frequency,
        calculate_custom_cost,
    )

    pass_df = get_passes_df(path)
    assert pass_df != -1

    # Calculate distance for each pass
    pass_df["Distance"] = pass_df.apply(calculate_pass_distance, axis=1)

    # Calculate success rate for each player
    success_rate = calculate_pass_success_rate(pd.read_csv(path))

    # Calculate frequency of passes between players
    pass_frequency = calculate_pass_frequency(pass_df)

    # Normalize distance feature
    max_distance = pass_df["Distance"].max()

    # Calculate custom weights for each pass
    pass_df["Custom Weight"] = pass_df.apply(
        calculate_custom_cost,
        axis=1,
        max_distance=max_distance,
        success_rate=success_rate,
        pass_frequency=pass_frequency,
        weights=optimized_weights,
    )

    # Build a directed graph with custom weights
    G = build_graph(pass_df, mode='c', graph=nx.DiGraph())

    # Calculate betweenness centrality
    betweenness_centrality = nx.betweenness_centrality(
        G, weight="weight", normalized=True
    )

    # Display results
    print(f"Betweenness Centrality for {title}:")
    for player, centrality in sorted(
        betweenness_centrality.items(), key=lambda x: x[1], reverse=True
    ):
        print(f"  {player}: {centrality:.4f}")

    return betweenness_centrality


def display_betweenness():
    from constants import TEAMS
    from analysis.cost_function_weight import optimize_custom_cost

    for team_file, title in TEAMS:
        optimized_weights = optimize_custom_cost(team_file)
        calculate_betweenness_centrality(team_file, title, optimized_weights)
