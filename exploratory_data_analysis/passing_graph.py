import pandas as pd

def plot_passes(df: pd.DataFrame) -> None:
    """
    Displays plot of passes for specific dataframe.
    """
    import matplotlib.pyplot as plt
    from mplsoccer import Pitch

    pass_df = df[(df['Type'] == 'PASS') & df['From'].notna() & df['To'].notna()]

    pitch = Pitch(pitch_type='metricasports', pitch_color='grass', goal_type='line', pitch_width=68, pitch_length=105)
    _, ax = pitch.draw(figsize=(16, 10.4))

    pitch.arrows(pass_df['Start X'], pass_df['Start Y'], pass_df['End X'], pass_df['End Y'], color='white', ax=ax, width=1, zorder=1)
    plt.show()

