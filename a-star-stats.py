import os
import subprocess
import csv

# Constants
NUM_SEEDS = 100
HEURISTICS = [0, 1, 2, 3]  # 0: Uniform Cost, 1: Misplaced Tiles, 2: Manhattan, 3: Custom
SEEDS = range(NUM_SEEDS)  # Generate seeds from 0 to 99
SEARCH_OUTPUT_DIR = 'search_outputs'  # Directory to save individual search outputs
HEURISTIC_DATA_DIR = 'heuristic_data'  # Directory to save V, N, d, b for each heuristic

# Ensure the output directories exist
os.makedirs(SEARCH_OUTPUT_DIR, exist_ok=True)
os.makedirs(HEURISTIC_DATA_DIR, exist_ok=True)

# Function to run the A* search
def run_a_star(seed, heuristic):
    try:
        # Generate the random board
        random_board_cmd = f"python random-board.py {seed} 100 < OLA1-input.txt > random-board-output.txt"
        os.system(random_board_cmd)
        
        # Run the A* search
        a_star_cmd = f"python a-star.py {heuristic} < random-board-output.txt"
        result = subprocess.run(a_star_cmd, shell=True, capture_output=True, text=True)
        
        # Save the full output to a file for reference
        search_output_filename = os.path.join(SEARCH_OUTPUT_DIR, f"search_seed_{seed}_heuristic_{heuristic}.txt")
        with open(search_output_filename, 'w') as f:
            f.write(result.stdout)
        
        # Capture the output and parse the relevant lines
        output = result.stdout.strip().split('\n')
        
        # Initialize variables
        V, N, d, b = None, None, None, None
        
        # Parse the output to find V, N, d, b
        for line in output:
            if line.startswith('V='):
                V = int(line.split('=')[1])
            elif line.startswith('N='):
                N = int(line.split('=')[1])
            elif line.startswith('d='):
                d = int(line.split('=')[1])
            elif line.startswith('b='):
                b = float(line.split('=')[1])
        
        # Check if all values were found
        if None in (V, N, d, b):
            print(f"Error: Could not parse output for seed {seed}, heuristic {heuristic}")
            return None, None, None, None
        
        return V, N, d, b

    except Exception as e:
        print(f"Error during processing seed {seed} with heuristic {heuristic}: {e}")
        return None, None, None, None

# Initialize data storage for each heuristic
heuristic_data = {h: [] for h in HEURISTICS}

# Run the experiments
for seed in SEEDS:
    for heuristic in HEURISTICS:
        V, N, d, b = run_a_star(seed, heuristic)
        if V is not None:  # Only add results if parsing was successful
            heuristic_data[heuristic].append((V, N, d, b))

# Save results for each heuristic
for heuristic in HEURISTICS:
    data_file = os.path.join(HEURISTIC_DATA_DIR, f"heuristic_{heuristic}_data.csv")
    with open(data_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['V', 'N', 'd', 'b'])
        writer.writerows(heuristic_data[heuristic])

print(f"Data for all heuristics saved in the {HEURISTIC_DATA_DIR} directory.")
