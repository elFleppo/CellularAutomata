from Grid import Grid
from Cell import Cell, SpawnCell, BorderCell

rows = 10
cols = 10
grid = Grid(rows, cols)

# Place some impassable cells (represented by 'B')
grid.grid[4][4] = Cell(state=1)  # Impassable cell
grid.grid[5][5] = Cell(state=1)  # Impassable cell

# Place an agent and a target
grid.place_agent(2, 2)
grid.place_target(7, 7)

print("Grid State:")
grid.display()

# Check line of sight from agent to target
agent = grid.grid[2][2]
has_los = agent.line_of_sight(grid.grid, 2, 2, 7, 7)
print(f"Line of Sight: {has_los}")