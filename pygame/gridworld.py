def get_neighbours(x, y, grid):
    """Returns the number of live neighbours around the cell at position (x, y)."""
    neighbours = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i == x and j == y) or i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]):
                continue
            if grid[i][j] == 1:
                neighbours += 1
    return neighbours

def crop_grid(grid):
    """Crop the grid around the living cells."""
    rows_with_living = [i for i in range(len(grid)) if any(grid[i])]
    cols_with_living = [j for j in range(len(grid[0])) if any(row[j] for row in grid)]

    if not rows_with_living or not cols_with_living:
        return [[]]
    
    min_row, max_row = min(rows_with_living), max(rows_with_living)
    min_col, max_col = min(cols_with_living), max(cols_with_living)
    
    cropped_grid = []
    for i in range(min_row, max_row + 1):
        cropped_grid.append(grid[i][min_col:max_col + 1])
        
    for row in cropped_grid:
        print(row)
    print("\n")
    return cropped_grid

def expand_grid(grid, padding):
    """Expand the grid with a border of zeros."""
    new_rows = len(grid) + 2 * padding
    new_cols = len(grid[0]) + 2 * padding
    new_grid = [[0] * new_cols for _ in range(new_rows)]
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            new_grid[i + padding][j + padding] = grid[i][j]
    
    return new_grid

def game_of_life(initial_state, generations):
    padding = generations + 1  # To ensure we have enough space for any possible growth
    grid = expand_grid(initial_state, padding)

    for _ in range(generations):
        new_grid = [[0] * len(grid[0]) for _ in range(len(grid))]
        
        for x in range(1, len(grid) - 1):
            for y in range(1, len(grid[0]) - 1):
                alive = grid[x][y] == 1
                neighbours = get_neighbours(x, y, grid)
                
                if alive:
                    if neighbours < 2 or neighbours > 3:
                        new_grid[x][y] = 0
                    else:
                        new_grid[x][y] = 1
                else:
                    if neighbours == 3:
                        new_grid[x][y] = 1

        grid = new_grid

    return crop_grid(grid)

# Example usage:
initial_state = [
    [1, 1, 1, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 1, 1, 1]
]

generations = 10
result = game_of_life(initial_state, generations)
for row in result:
    print(row)