import pandas as pd
import matplotlib.pyplot as plt

# Load the filtered datasets for each team
team_data_dir = '../data/filtered_data/teams'
game1_home = pd.read_csv(f'{team_data_dir}/Sample_Game_1_Home_filtered.csv')
game1_away = pd.read_csv(f'{team_data_dir}/Sample_Game_1_Away_filtered.csv')
game2_home = pd.read_csv(f'{team_data_dir}/Sample_Game_2_Home_filtered.csv')
game2_away = pd.read_csv(f'{team_data_dir}/Sample_Game_2_Away_filtered.csv')

# Define colors for each pass type
type_colors = {
    'PASS': 'green',
    'BALL OUT': 'orange',
    'BALL LOST': 'red'
}


# Function to plot passes for each team
def plot_team_passes(team_df, title):
    plt.figure(figsize=(10, 7))
    for _, row in team_df.iterrows():
        start_x, start_y = row['Start X'] * 105, row['Start Y'] * 68
        end_x, end_y = row['End X'] * 105, row['End Y'] * 68
        color = type_colors.get(row['Type'], 'blue')
        plt.arrow(start_x, start_y, end_x - start_x, end_y - start_y,
                  head_width=1, head_length=1, fc=color, ec=color, alpha=0.6)

    plt.title(title)
    plt.xlabel("Pitch X-coordinate (meters)")
    plt.ylabel("Pitch Y-coordinate (meters)")
    plt.xlim(0, 105)
    plt.ylim(0, 68)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(False)
    plt.show()


# Plot each team
plot_team_passes(game1_home, "Game 1 - Home Team Passes")
plot_team_passes(game1_away, "Game 1 - Away Team Passes")
plot_team_passes(game2_home, "Game 2 - Home Team Passes")
plot_team_passes(game2_away, "Game 2 - Away Team Passes")

