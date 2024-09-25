import pandas as pd
import os

# Directory where the heuristic data is stored
HEURISTIC_DATA_DIR = 'heuristic_data'

# Function to load data for a specific heuristic
def load_heuristic_data(heuristic):
    file_path = os.path.join(HEURISTIC_DATA_DIR, f"heuristic_{heuristic}_data.csv")
    return pd.read_csv(file_path)

# Function to calculate detailed statistics
def calculate_statistics(data):
    stats = {
        'Min': data.min(),
        'Median': data.median(),
        'Mean': data.mean(),
        'Max': data.max(),
        'StdDev': data.std()
    }
    return stats

# Process and display statistics for each heuristic
for heuristic in range(4):
    data = load_heuristic_data(heuristic)
    stats = calculate_statistics(data)
    print(f"Statistics for Heuristic {heuristic}:\n")
    for metric, values in stats.items():
        print(f"{metric}:\n{values}\n")
    print("\n" + "="*50 + "\n")
