import random
from Grid import Grid
from Cell import Cell, SpawnCell, ObstacleCell, TargetCell, Agent

def room_square():
    height = 50
    length = 50

    spawn_cells = [(0, 1), (0, 2), (0, 3), (0, 4)]
    obstacle_cells = [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), (5, 19), (5, 20), (5, 21), (5, 22), (5, 23), (5, 24), (5, 25), (5, 26), (5, 27), (5, 28), (5, 29), (5, 30), (5, 31), (5, 32), (5, 33), (5, 34), (5, 35), (5, 36), (5, 37), (5, 38), (5, 39), (5, 40), (5, 41), (5, 42), (5, 43), (5, 44), (5, 45), (5, 46), (5, 47), (5, 48), (5, 49), (2, 4), (3, 25)]
    target_cells = [(0, 49), (1, 49), (2, 49), (3, 49), (4, 49)] 

    grid = Grid(height=height, length=length, spawn_cells=spawn_cells, obstacle_cells=obstacle_cells, target_cells=target_cells, cell_size=0.5)

    return grid


def ChickenTest():
    rows = 20
    cols = 20


def RiMEA9(Doors):
    height = 20
    length = 30

    possible_targets = [(0, 4), (19, 25), (0, 25), (19, 4)]

    grid = Grid(height=height, length=length, spawn_cells=[], obstacle_cells=[], target_cells=[], cell_size=0.5)

    for k in range(0,Doors):
        grid.place_target(possible_targets[k][0], possible_targets[k][1])

    for i in range(0, 1000):
        for cell in grid.grid:
            if  isinstance(cell, Cell) and cell.row(2/grid.cell_size, (grid.height-1/grid.cell_size)-2/grid.cell_size) and cell.col(2/grid.cell_size, (grid.length-1/grid.cell_size)-2/grid.cell_size):
                grid.place_agent(cell[0], cell[1])

    return grid
    
def RiMEA4():
    height = 10
    length = 150

    obstacle_cells = [(4, 24), (5, 24), (4, 25), (5, 25), (4, 74), (5, 74), (6, 74), (7, 74), (4, 75), (5, 75), (6, 75), (7, 75)] 

    grid = Grid(height=height, length=length, spawn_cells=[], obstacle_cells=[], target_cells=[], cell_size=0.5)

    for i in range(0, height):
        grid.place_spawn_cell(i, 0)
        grid.place_target(i, length-1)

    for j in range(0, len(obstacle_cells)-1):
        grid.place_obstacle(obstacle_cells[j][0], obstacle_cells[j][1])

    grid = Grid(rows, cols, spawn_cells, obstacle_cells, target_cells)

    return grid