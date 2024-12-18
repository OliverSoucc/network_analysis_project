
def plot_graph(filepath: str) -> None:
    """
    Displays plot of passes for specific dataframe.
    """
    import matplotlib.pyplot as plt
    from mplsoccer import Pitch
    import pandas as pd

    df = pd.read_csv(filepath)

    pass_df = df[(df['Type'] == 'PASS') & df['From'].notna() & df['To'].notna()]

    pitch = Pitch(pitch_type='metricasports', pitch_color='grass', goal_type='line', pitch_width=68, pitch_length=105)
    _, ax = pitch.draw(figsize=(16, 10.4))

    pitch.arrows(pass_df['Start X'], pass_df['Start Y'], pass_df['End X'], pass_df['End Y'], color='white', ax=ax, width=1, zorder=1)
    plt.show()


def display_passing_graph():
    from constants import TEAMS
    for team_file, _ in TEAMS:
        plot_graph(team_file)
