import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

'''
    -> Heat map
    -> based on start of pass
    -> both half times for each team on one graph
'''

# Define a function to create a heatmap of pass origins using seaborn
def passing_heatmap_seaborn(team_file, title):
    # Load the team's passing data
    team_df = pd.read_csv(team_file)

    # Filter only rows where Type is 'PASS'
    pass_df = team_df[team_df['Type'] == 'PASS'].copy()  # Use .copy() to avoid warnings

    # Define pitch dimensions
    pitch_length = 105  # in meters
    pitch_width = 68  # in meters

    # Ensure 'Start X' and 'Start Y' are numeric
    pass_df.loc[:, 'Start X'] = pd.to_numeric(pass_df['Start X'], errors='coerce')
    pass_df.loc[:, 'Start Y'] = pd.to_numeric(pass_df['Start Y'], errors='coerce')

    # Drop rows with missing values in 'Start X' and 'Start Y'
    pass_df = pass_df.dropna(subset=['Start X', 'Start Y'])

    # Convert normalized values to pitch dimensions
    pass_df.loc[:, 'Start X'] *= pitch_length
    pass_df.loc[:, 'Start Y'] *= pitch_width

    # Create a higher-resolution grid for the heatmap
    grid_resolution_x, grid_resolution_y = 50, 50  # Higher grid resolution
    heatmap, xedges, yedges = np.histogram2d(
        pass_df['Start X'],
        pass_df['Start Y'],
        bins=[grid_resolution_x, grid_resolution_y],
        range=[[0, pitch_length], [0, pitch_width]]
    )

    # Convert the heatmap data to a DataFrame for Seaborn
    heatmap_df = pd.DataFrame(
        heatmap.T,  # Transpose to align with the plot
        index=np.linspace(0, pitch_width, grid_resolution_y),
        columns=np.linspace(0, pitch_length, grid_resolution_x)
    )

    # Create the heatmap using seaborn
    plt.figure(figsize=(12, 8))
    sns.heatmap(
        heatmap_df, cmap="Reds", linewidths=0.5, linecolor='black',
         xticklabels=False, yticklabels=False,cbar_kws={'label': 'Number of Passes'}
    )
    plt.title(f"Passing Heatmap (Origins) - {title}")
    plt.xlabel("Pitch Length (meters)")
    plt.ylabel("Pitch Width (meters)")
    plt.show()

# Paths to team files for each game and titles for each result
team_files_titles = [
    ('../data/filtered_data/teams/Sample_Game_1_Home_filtered.csv', "Game 1 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_1_Away_filtered.csv', "Game 1 - Away Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Home_filtered.csv', "Game 2 - Home Team"),
    ('../data/filtered_data/teams/Sample_Game_2_Away_filtered.csv', "Game 2 - Away Team")
]

for team_file, title in team_files_titles:
    passing_heatmap_seaborn(team_file, title)





