import random
import json
import numpy as np

def generate_structured_grid(height, width, density=0.5):
    grid = [[0 for _ in range(width)] for _ in range(height)]
    for i in range(height):
        for j in range(width):
            grid[i][j] = 1 if random.random() < density else 0
    return grid

def calculate_clues(line):
    clues = []
    count = 0
    for cell in line:
        if cell == 1:
            count += 1
        else:
            if count > 0:
                clues.append(count)
                count = 0
    if count > 0:
        clues.append(count)
    return clues or [0]

def generate_nonogram(height, width, density=0.5):
    grid = generate_structured_grid(height, width, density)
    row_clues = [calculate_clues(row) for row in grid]
    column_clues = [calculate_clues([grid[r][c] for r in range(height)]) for c in range(width)]
    return grid, row_clues, column_clues

def generate_dataset(num_samples, height, width, density=0.5, filename="nonogram_dataset.json"):
    dataset = []
    for _ in range(num_samples):
        grid, row_clues, column_clues = generate_nonogram(height, width, density)
        dataset.append({
            "grid": grid,
            "row_clues": row_clues,
            "column_clues": column_clues
        })
    with open(filename, "w") as f:
        json.dump(dataset, f)
    print(f"Dataset of {num_samples} nonograms saved to {filename}.")

# Example usage: Generate a dataset of 1000 nonograms
generate_dataset(num_samples=1000, height=10, width=10)
