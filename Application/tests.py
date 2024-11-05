import random
from Grid import Grid
from Cell import Cell, SpawnCell, ObstacleCell, TargetCell, Agent

rows = 50
cols = 50
timesteps = 55
spawn_cells = [(0, 1), (0, 2), (0, 3), (0, 4)]
obstacle_cells = [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), (5, 19), (5, 20), (5, 21), (5, 22), (5, 23), (5, 24), (5, 25), (5, 26), (5, 27), (5, 28), (5, 29), (5, 30), (5, 31), (5, 32), (5, 33), (5, 34), (5, 35), (5, 36), (5, 37), (5, 38), (5, 39), (5, 40), (5, 41), (5, 42), (5, 43), (5, 44), (5, 45), (5, 46), (5, 47), (5, 48), (5, 49), (2, 4), (3, 25)]
target_cells = [(0, 49), (1, 49), (2, 49), (3, 49), (4, 49)] 

grid = Grid(rows, cols, spawn_cells=spawn_cells, obstacle_cells=obstacle_cells,target_cells=target_cells)
grid.place_agent(4, 1) 
grid.place_agent(3, 1) 
grid.place_agent(2, 1) 
grid.place_agent(1, 1) 


for i in range(timesteps):
    print(grid.display())
    print(f"\n{i} Zeitschritt")
    grid.update(target_list=target_cells)


