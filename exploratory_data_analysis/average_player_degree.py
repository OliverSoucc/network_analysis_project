import pandas as pd
import networkx as nx


'''
 -> Average player degree for each team 
'''

# Define a function to calculate the average degree for each team
def calculate_average_degree(team_file):
    # Load the passing dataset
    team_df = pd.read_csv(team_file)

    # Filter only rows where Type is 'PASS' and drop rows with missing values
    pass_df = team_df[(team_df['Type'] == 'PASS') & team_df['From'].notna() & team_df['To'].notna()]

    # Get the unique teams
    teams = pass_df['Team'].unique()

    # Initialize a dictionary to store the average degree for each team
    team_avg_degrees = {}

    # Calculate the average degree for each team
    for team in teams:
        team_passes = pass_df[pass_df['Team'] == team]

        # Create a directed graph
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


# Array of file paths
team_files = [
    ('../data/filtered_data/teams/Sample_Game_1_Home_filtered.csv', "Game 1 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_1_Away_filtered.csv', "Game 1 - Away Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Home_filtered.csv', "Game 2 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Away_filtered.csv', "Game 2 - Away Team")
]

# Loop through each file and calculate average degree
for file_path, team in team_files:
    team_avg_degrees = calculate_average_degree(file_path)
    print(f"Team {team}: Average Degree = {team_avg_degrees}")
