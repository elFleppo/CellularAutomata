from Grid import Grid
from Cell import Cell, SpawnCell, BorderCell, ObstacleCell, Agent

rows = 10
cols = 10
grid = Grid(rows, cols)



# Place an agent and a target
grid.place_agent(2, 2)
grid.place_obstacle(8,8)
grid.place_target(7, 7)
grid.place_target(1, 5)
grid.place_target(6, 6)

print("Grid State:")
grid.display()

# Check line of sight from agent to target
agent = grid.grid[2][2]
if isinstance(agent, Agent):
    print(agent.find_nearest_target(grid))
    print(agent.line_of_sight(grid))
    print(agent.potential(grid))
