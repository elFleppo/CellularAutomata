from Grid import Grid
from Cell import Cell, SpawnCell, BorderCell, ObstacleCell, Agent, TargetCell

rows = 10
cols = 10
timesteps = 10
spawn_cells = [(6, 6),(2, 2)]
obstacle_cells = [(4, 2),(7, 1)]
target_cells = [(4, 1), (8, 1)]
grid = Grid(rows, cols, spawn_cells=spawn_cells, obstacle_cells=obstacle_cells,target_cells=target_cells)
grid.place_agent(1, 5)
grid.place_agent(2, 5)
for i in range(timesteps):
    print(grid.display())
    print(f"\n{i} Zeitschritt")
    grid.update(target_list=target_cells)

