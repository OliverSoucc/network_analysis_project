def degree_distribution_plot_unweighted(filepath: str, title: str):
    '''
    Graph nodes vs edges
    '''
    import networkx as nx
    import matplotlib.pyplot as plt
    import numpy as np
    from helper_functions import get_passes_df

    pass_df = get_passes_df(filepath)

    if isinstance(pass_df, int) and pass_df == -1:
        raise Exception("Error")

    teams = pass_df['Team'].unique()

    for team in teams:
        team_passes = pass_df[pass_df['Team'] == team]

        G = nx.DiGraph()

        for _, row in team_passes.iterrows():
            from_player = row['From']
            to_player = row['To']
            G.add_edge(from_player, to_player)  # No weights added

        # Get degrees (unweighted)
        degrees = [degree for _, degree in G.degree()]
        max_degree = max(degrees)

        # Degree distribution plot
        plt.figure(figsize=(10, 6))
        plt.hist(degrees, bins=np.arange(0, max_degree + 2) - 0.5, alpha=0.75, color='blue', edgecolor='black')
        plt.title(f"Unweighted Degree Distribution - {title} - {team}")
        plt.xlabel("Degree")
        plt.ylabel("Number of Nodes (Players)")
        plt.grid()
        plt.show()

def display_degree_distribution():
    from constants import TEAMS

    for team_file, title in TEAMS:
        degree_distribution_plot_unweighted(team_file, title)


