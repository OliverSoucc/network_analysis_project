import pandas as pd
import numpy as np


'''
    -> parameters we take to consideration:
        -> pass distance
        -> success rate of passing of player
        -> pass frequency, how many times he exchange the ball with every other teammate (this is what where were using previously alone and still using in files where "weights NOT from cost_function")
'''

def calculate_pass_success_rate(team_df):
    # Filter relevant rows (PASS, BALL LOST, BALL OUT)
    filtered_df = team_df[team_df['Type'].isin(['PASS', 'BALL LOST', 'BALL OUT'])]

    # Calculate total passes attempted by each player
    total_passes = filtered_df.groupby('From').size()

    # Calculate successful passes
    successful_passes = filtered_df[filtered_df['Type'] == 'PASS'].groupby('From').size()

    # Calculate success rate
    success_rate = (successful_passes / total_passes).fillna(0)  # Fill NaN for players with no total passes
    return success_rate.to_dict()

# Calculate pass frequency between two players
def calculate_pass_frequency(pass_df):
    # Count frequency of passes between each pair of players
    pass_frequency = pass_df.groupby(['From', 'To']).size()
    return pass_frequency.to_dict()


'''
    -> calculating cost function
    -> cost_function = w_1 x distance + w_2 x 1/Frequency + w_3 x (1 - Success)
        -> note: still need to estimate w_1,2,3 for each team, done in optimize_weights_with_gradient_descent
'''
def calculate_custom_cost(row, max_distance, success_rate, pass_frequency, weights):
    w1, w2, w3 = weights
    normalized_distance = row['Distance'] / max_distance if max_distance > 0 else 0
    normalized_frequency = 1 / pass_frequency.get((row['From'], row['To']), 1)
    normalized_success = 1 - success_rate.get(row['From'], 0)
    return w1 * normalized_distance + w2 * normalized_frequency + w3 * normalized_success

def total_cost(weights, pass_df, max_distance, success_rate, pass_frequency):
    return pass_df.apply(
        calculate_custom_cost,
        axis=1,
        max_distance=max_distance,
        success_rate=success_rate,
        pass_frequency=pass_frequency,
        weights=weights
    ).sum()



'''
    -> estimating w_1,2,3 with gradient descent for each team
'''
def optimize_weights_with_gradient_descent(pass_df, max_distance, success_rate, pass_frequency, learning_rate=0.01, iterations=100):
    weights = np.array([0.33, 0.33, 0.34])
    for _ in range(iterations):
        gradients = np.zeros_like(weights)
        for i in range(len(weights)):
            delta = 1e-5
            weights_plus = weights.copy()
            weights_minus = weights.copy()
            weights_plus[i] += delta
            weights_minus[i] -= delta
            cost_plus = total_cost(weights_plus, pass_df, max_distance, success_rate, pass_frequency)
            cost_minus = total_cost(weights_minus, pass_df, max_distance, success_rate, pass_frequency)
            gradients[i] = (cost_plus - cost_minus) / (2 * delta)
        weights -= learning_rate * gradients
        weights = np.clip(weights, 0, 1)
        if weights.sum() > 0:
            weights /= weights.sum()
    return weights

# Example usage
def optimize_custom_cost(team_path: str):
    from helper_functions import calculate_pass_distance
    # Load the team's passing data
    team_df = pd.read_csv(team_path)

    # Filter only rows where Type is 'PASS'
    pass_df = team_df[team_df['Type'] == 'PASS'].copy()

    # Calculate distance for each pass
    pass_df['Distance'] = pass_df.apply(calculate_pass_distance, axis=1)

    # Calculate success rate for each player
    success_rate = calculate_pass_success_rate(team_df)

    # Calculate frequency of passes between players
    pass_frequency = calculate_pass_frequency(pass_df)

    # Normalize distance feature
    max_distance = pass_df['Distance'].max()

    # Optimize weights
    optimized_weights = optimize_weights_with_gradient_descent(
        pass_df, max_distance, success_rate, pass_frequency, learning_rate=0.0001, iterations=100
    )
    return optimized_weights

