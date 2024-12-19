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


def ChickenTest(movement_method):
    height = 20
    length = 20

    grid = Grid(height=height, length=length, spawn_cells=[], obstacle_cells=[], target_cells=[], cell_size=0.5, movement_method=movement_method)

    # place obstacles
    obstacles = grid.select_area_by_coordinates(6, 6, 14, 6)
    obstacles += grid.select_area_by_coordinates(6, 6, 6, 10)
    obstacles += grid.select_area_by_coordinates(14, 6, 14, 10)

    for cell in obstacles:
        grid.place_obstacle(cell.row, cell.col)

    # place target
    target = grid.select_area_by_coordinates(10, 0, 11, 0)
    
    for cell in target:
        grid.place_target(cell.row, cell.col)
    
    # place agent
    agent_cell = grid.select_area_by_coordinates(10, 7, 11, 7)

    for cell in agent_cell:
        grid.place_agent(cell.row, cell.col)


    return grid


def RiMEA9(Doors, movement_method):
    room_height = 20
    room_length = 30
    frameSize = 5
    height = room_height+2*frameSize
    length = room_length+2*frameSize

    grid = Grid(height=height, length=length, spawn_cells=[], obstacle_cells=[], target_cells=[], cell_size=0.5, movement_method=movement_method)

    # place obstacles and targets
    vertical_placement = grid.select_area_by_coordinates(frameSize, frameSize, frameSize, height-frameSize) # Obstacle-Zellen links
    vertical_placement += grid.select_area_by_coordinates(length-frameSize, frameSize, length-frameSize, height-frameSize) # Obstacle-Zellen rechts
    horizontal_placement = grid.select_area_by_coordinates(frameSize, frameSize, length-frameSize, frameSize) # Obstacle-Zellen oben
    horizontal_placement += grid.select_area_by_coordinates(frameSize, height-frameSize, length-frameSize, height-frameSize) # Obstacle-Zellen unten

    obstacles = vertical_placement+horizontal_placement

    for cell in obstacles:
        grid.place_obstacle(cell.row, cell.col)

    if Doors == 1:
        door_cells = grid.select_area_by_coordinates(frameSize+4, frameSize, frameSize+5, frameSize)
        print(len(door_cells))
        target_placement = grid.select_area_by_coordinates(frameSize+4, 0, frameSize+5, 0)
    elif Doors == 2:
        door_cells = grid.select_area_by_coordinates(frameSize+4, frameSize, frameSize+5, frameSize)
        door_cells += grid.select_area_by_coordinates(length-frameSize-5, height-frameSize, length-frameSize-4, height-frameSize)
        target_placement = grid.select_area_by_coordinates(frameSize+4, 0, frameSize+5, 0)
        target_placement += grid.select_area_by_coordinates(length-frameSize-5, height, length-frameSize-4, height)
    elif Doors == 3:
        door_cells = grid.select_area_by_coordinates(frameSize+4, frameSize, frameSize+5, frameSize)
        door_cells += grid.select_area_by_coordinates(length-frameSize-5, height-frameSize, length-frameSize-4, height-frameSize)
        door_cells += grid.select_area_by_coordinates(length-frameSize-5, frameSize, length-frameSize-4, frameSize)
        target_placement = grid.select_area_by_coordinates(frameSize+4, 0, frameSize+5, 0)
        target_placement += grid.select_area_by_coordinates(length-frameSize-5, height, length-frameSize-4, height)
        target_placement += grid.select_area_by_coordinates(length-frameSize-5, 0, length-frameSize-4, 0)
    else:
        # hiermit wird abgefangen, falls Zahlen ausserhalb der Menge 1-3 eingegeben werden - dann default 4
        door_cells = grid.select_area_by_coordinates(frameSize+4, frameSize, frameSize+5, frameSize)
        door_cells += grid.select_area_by_coordinates(length-frameSize-5, height-frameSize, length-frameSize-4, height-frameSize)
        door_cells += grid.select_area_by_coordinates(length-frameSize-5, frameSize, length-frameSize-4, frameSize)
        door_cells += grid.select_area_by_coordinates(frameSize+4, height-frameSize, frameSize+5, height-frameSize)
        target_placement = grid.select_area_by_coordinates(frameSize+4, 0, frameSize+5, 0)
        target_placement += grid.select_area_by_coordinates(length-frameSize-5, height, length-frameSize-4, height)
        target_placement += grid.select_area_by_coordinates(length-frameSize-5, 0, length-frameSize-4, 0)
        target_placement += grid.select_area_by_coordinates(frameSize+4, height, frameSize+5, height)

    for cell in target_placement:
        grid.place_target(cell.row, cell.col)

    # place doors
    for cell in door_cells:
        grid.place_empty_cell(cell.row, cell.col)

    # place agents
    potential_agent_cells = grid.select_area_by_coordinates(frameSize+2, frameSize+2, length-frameSize-2, height-frameSize-2)

    for cell in potential_agent_cells:
        chance = random.randint(0, 10)
        if chance <= 5 and len(grid.agents)<=1000:
            grid.place_agent(cell.row, cell.col)


    return grid


# Anpassungen aus den anderen Maps müssen für RiMEA4 noch übernommen werden
def RiMEA4():
    height = 10
    length = 150

    obstacle_cells = [(4, 24), (5, 24), (4, 25), (5, 25), (4, 74), (5, 74), (6, 74), (7, 74), (4, 75), (5, 75), (6, 75), (7, 75)] 

    grid = Grid(height=height, length=length, spawn_cells=[], obstacle_cells=[], target_cells=[], cell_size=0.5)

    for i in range(0, grid.rows-1):
        grid.place_spawn_cell(i, 0)
        grid.place_target(i, grid.cols-1)

    for j in range(0, len(obstacle_cells)-1):
        grid.place_obstacle(obstacle_cells[j][0], obstacle_cells[j][1])

    return grid