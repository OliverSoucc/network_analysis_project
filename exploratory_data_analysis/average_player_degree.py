def calculate_average_degree(filepath: str):
    import networkx as nx
    from helper_functions import get_passes_df

    pass_df = get_passes_df(filepath)

    if isinstance(pass_df, int) and pass_df == -1:
        raise Exception("Error")

    teams = pass_df['Team'].unique()
    team_avg_degrees = {}

    # Calculate the average degree for each team
    for team in teams:
        team_passes = pass_df[pass_df['Team'] == team]

        G = nx.DiGraph()

        # Add edges (passes) to the graph
        for _, row in team_passes.iterrows():
            from_player = row['From']
            to_player = row['To']
            G.add_edge(from_player, to_player)

        # Calculate the average degree (total degree / number of nodes)
        total_degree = sum(dict(G.degree()).values())
        num_nodes = G.number_of_nodes()
        average_degree = total_degree / num_nodes if num_nodes > 0 else 0

        # Store the average degree for the team
        team_avg_degrees = average_degree

    return team_avg_degrees

def display_average_degree():
    from constants import TEAMS
    # Loop through each file and calculate average degree
    for file_path, team in TEAMS:
        team_avg_degrees = calculate_average_degree(file_path)
        print(f"Team {team}: Average Degree = {team_avg_degrees}")
