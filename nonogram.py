import random

def generate_structured_grid(height, width, density=0.5):
    grid = [[0 for _ in range(width)] for _ in range(height)]
    
    # Fill grid with random patterns based on density
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

def validate_nonogram(grid, row_clues, column_clues):
    for i, row in enumerate(grid):
        if calculate_clues(row) != row_clues[i]:
            return False
    for j in range(len(grid[0])):
        column = [grid[i][j] for i in range(len(grid))]
        if calculate_clues(column) != column_clues[j]:
            return False
    return True

def display_nonogram(grid, row_clues, column_clues):
    # Get the maximum length of the clues
    max_row_clue_len = max(len(clue) for clue in row_clues)
    max_col_clue_len = max(len(clue) for clue in column_clues)

    # Determine the padding based on the maximum length of the clues
    max_clue_len = max(max_row_clue_len, max_col_clue_len)

    # Create a format string based on the maximum clue length
    cell_width = 3  # Adjust this width for better alignment
    format_str = f"{{:>{cell_width}}}"

    # Print column clues with appropriate padding
    for i in range(max_col_clue_len):
        # Start with padding for the row clues
        print(" " * (max_clue_len * cell_width), end=" ")
        for clue in column_clues:
            # Print the clue if it exists, else print an empty space
            if len(clue) > i:
                print(f"{format_str.format(clue[i])}", end="")
            else:
                print(" " * cell_width, end="")
        print()

    # Print each row with its clues
    for row_clue, row in zip(row_clues, grid):
        # Pad row clues to align with the grid
        row_clue_str = "".join(format_str.format(clue) for clue in row_clue).rjust(max_clue_len+2 * cell_width)
        # Then print the grid cells
        grid_row_str = "".join(format_str.format("#" if cell else ".") for cell in row)
        print(f"{row_clue_str} | {grid_row_str}")

# Example usage
height, width = 10, 10
grid, row_clues, column_clues = generate_nonogram(height, width, density=0.5)

if validate_nonogram(grid, row_clues, column_clues):
    print("Generated nonogram is valid!")
    display_nonogram(grid, row_clues, column_clues)
else:
    print("Generated nonogram is invalid.")
