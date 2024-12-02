import pandas as pd
import networkx as nx
from cost_function_weight import (
    optimize_custom_cost,
    calculate_pass_distance,
    calculate_pass_success_rate,
    calculate_pass_frequency,
    calculate_custom_cost,
)

'''
    -> tu by mali byt values pre kazdeho hraca medzi [0, 1] (normalizovane), a nie som si uplne isty preco nie su
    -> dat tomu 10 minut, ak sa nepodari fixnut, vymazat -> mame toho dost
'''

def calculate_closeness_centrality(team_file, title, optimized_weights):
    # Load the team's passing data
    team_df = pd.read_csv(team_file)

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

    # Build a directed graph with custom weights
    G = nx.DiGraph()
    for _, row in pass_df.iterrows():
        if row['From'] != row['To']:  # Exclude self-loops
            G.add_edge(row['From'], row['To'], weight=row['Custom Weight'])

    # Check connectivity
    if not nx.is_weakly_connected(G):
        print(f"Warning: The graph for {title} is not fully connected. Results may be inaccurate.")

    # Calculate closeness centrality
    closeness_centrality = nx.closeness_centrality(G, distance='weight')

    # Display results
    print(f"Closeness Centrality for {title}:")
    for player, centrality in sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True):
        print(f"  {player}: {centrality:.4f}")

    return closeness_centrality


# Paths to team files and corresponding titles
team_files_titles = [
    ('../data/filtered_data/teams/Sample_Game_1_Home_filtered.csv', "Game 1 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_1_Away_filtered.csv', "Game 1 - Away Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Home_filtered.csv', "Game 2 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Away_filtered.csv', "Game 2 - Away Team")
]

# Perform closeness centrality analysis for each team

for team_file, title in team_files_titles:
    optimized_weights = optimize_custom_cost(team_file, title)
    calculate_closeness_centrality(team_file, title, optimized_weights)
