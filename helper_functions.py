import pandas as pd
import networkx as nx
import math
from typing import Literal


def calculate_pass_distance(row):
    return math.sqrt((row['End X'] - row['Start X'])**2 + (row['End Y'] - row['Start Y'])**2)


# c - custom; p - pass
MODE = Literal['c', 'p']
# Return value for negative if checks
ERROR = Literal[-1]

def build_graph(df: pd.DataFrame, mode: MODE, graph):
    if mode == 'c':
        for _, row in df.iterrows():
            graph.add_edge(row['From'], row['To'], weight=row['Custom Weight'])
    elif mode == 'p':
        # Build the graph from passes
        for _, row in df.iterrows():
            from_player = row["From"]
            to_player = row["To"]

            # Add or update the edge weight for each pass
            if graph.has_edge(from_player, to_player):
                graph[from_player][to_player]["weight"] += 1
            else:
                graph.add_edge(from_player, to_player, weight=1)

    return graph




def get_passes_df(filepath: str) -> pd.DataFrame | ERROR:
    team_df = pd.read_csv(filepath)
    pass_df = team_df[(team_df['Type'] == 'PASS') & team_df['From'].notna() & team_df['To'].notna()]

    if not isinstance(pass_df, pd.DataFrame):
        return -1

    return pass_df
