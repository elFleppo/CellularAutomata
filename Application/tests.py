import random
from Grid import Grid
from Cell import Cell, SpawnCell, ObstacleCell, TargetCell, Agent

rows = 10
cols = 10
timesteps = 10
spawn_cells = [(3, 2)]
#obstacle_cells = [(4, 0), (4, 1), (4, 2),(4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9)] #X-Tunnel
#obstacle_cells = [(0, 4), (1, 4), (2, 4),(3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4)] #Y-Tunnel
obstacle_cells = [(0, 0), (1, 1), (2, 2), (3, 3),(4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)] #Diagonal-Tunnel
target_cells = [(2, 9), (9, 2)] #Ein Target ist immer erreichbar, das andere dient sozusagen als Beweis das der Agent nicht durch das Hindernis kann

grid = Grid(rows, cols, spawn_cells=spawn_cells, obstacle_cells=obstacle_cells,target_cells=target_cells)
grid.place_agent(4, 2) #Hier muss man je nach Hindernis anpassen
for i in range(timesteps):
    print(grid.display())
    print(f"\n{i} Zeitschritt")
    grid.update(target_list=target_cells)
