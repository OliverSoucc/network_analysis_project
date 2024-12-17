import matplotlib.pyplot as plt
import pandas as pd
from exploratory_data_analysis.number_of_edges import display_no_edges
from helper_functions import get_passes_df

if __name__ == "__main__":
    df = pd.read_csv("data/game1_home.csv")
    display_no_edges()


