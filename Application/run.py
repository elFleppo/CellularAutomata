from Grid import Grid
from Cell import Cell, SpawnCell, BorderCell, ObstacleCell, Agent, TargetCell

#Einfacher aufbau um erste Visualisierung zu machen
rows = 15
cols = 15
timesteps = 10
spawn_cells = [(8, 6),(2, 7)]
obstacle_cells = [(4, 2),(7, 1)]
target_cells = [(4, 1), (8, 1)]
grid = Grid(rows, cols, spawn_cells=spawn_cells, obstacle_cells=obstacle_cells,target_cells=target_cells)

for i in range(timesteps):
    print(grid.display())
    print(f"\n{i} Zeitschritt")
    grid.update(target_list=target_cells)

