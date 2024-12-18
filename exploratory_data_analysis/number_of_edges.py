def calculate_team_edges(filepath: str):
    import networkx as nx
    from helper_functions import get_passes_df

    pass_df = get_passes_df(filepath)

    if isinstance(pass_df, int) and pass_df == -1:
        raise Exception("Error")

    teams = pass_df['Team'].unique()

    # Initialize a dictionary to store the number of edges for each team
    team_edges = {}

    # Calculate the number of edges for each team
    for team in teams:
        team_passes = pass_df[pass_df['Team'] == team]

        # Create a directed graph
        G = nx.DiGraph()

        # Add edges (passes) to the graph
        for _, row in team_passes.iterrows():
            from_player = row['From']
            to_player = row['To']
            G.add_edge(from_player, to_player)

        # Store the number of edges for the team
        team_edges = G.number_of_edges()

    return team_edges


# TODO: Return the values in dictionary {"team": no edges}
def display_no_edges() -> None:
    from constants import TEAMS
    # Loop through each file and calculate edges
    for file_path, team in TEAMS:
        team_edges = calculate_team_edges(file_path)
        print(f"{team}: {team_edges} edges")


