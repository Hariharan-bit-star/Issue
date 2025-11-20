import random
import time

def create_grid(rows, cols):
    """Creates a grid of random 0s and 1s."""
    return [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

def print_grid(grid):
    """Prints the grid to the console."""
    for row in grid:
        print(" ".join(["■" if cell else "□" for cell in row]))

def get_neighbors(grid, row, col):
    """Gets the number of live neighbors for a cell."""
    rows, cols = len(grid), len(grid[0])
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r, c = row + i, col + j
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
                count += 1
    return count

def update_grid(grid):
    """Updates the grid based on the rules of Conway's Game of Life."""
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            neighbors = get_neighbors(grid, r, c)
            if grid[r][c] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[r][c] = 0
                else:
                    new_grid[r][c] = 1
            else:
                if neighbors == 3:
                    new_grid[r][c] = 1
    return new_grid

def main():
    """Main function to run the Game of Life simulation."""
    rows, cols = 20, 40
    grid = create_grid(rows, cols)
    generations = 50

    for gen in range(generations):
        print(f"Generation {gen + 1}")
        print_grid(grid)
        grid = update_grid(grid)
        time.sleep(0.2)
        # Clear the screen (works on most terminals)
        print("\033[H\033[J", end="")


if __name__ == "__main__":
    main()
