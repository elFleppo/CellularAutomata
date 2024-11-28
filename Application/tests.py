import random
from Grid import Grid
from Cell import Cell, SpawnCell, ObstacleCell, TargetCell, Agent

def room_square():
    rows = 50
    cols = 50
    timesteps = 55
    # aktuell noch fix auf eine Zelle gesetzt / Anpassung an Zellgrössen-Änderung
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


def ChickenTest():
    rows = 20
    cols = 20
    timesteps = 55
    # aktuell noch fix auf eine Zelle gesetzt / Anpassung an Zellgrössen-Änderung
    spawn_cells = []
    obstacle_cells = [] # muss noch ergänzt werden
    target_cells = []

    grid = Grid(rows, cols, spawn_cells=spawn_cells, obstacle_cells=obstacle_cells,target_cells=target_cells)
    grid.place_agent(1, 1)


    for i in range(timesteps):
        print(grid.display())
        print(f"\n{i} Zeitschritt")
        grid.update(target_list=target_cells)


def RiMEA9(Doors):
    rows = 20
    cols = 30
    timesteps = 120
    # aktuell noch fix auf eine Zelle gesetzt / Anpassung an Zellgrössen-Änderung
    spawn_cells = []
    obstacle_cells = []
    possible_targets = [(0, 4), (19, 25), (0, 25), (19, 4)]
    target_cells = []
    for k in range(0,Doors):
        target_cells.append(possible_targets[k])
    print(target_cells)

    grid = Grid(rows, cols, spawn_cells=spawn_cells, obstacle_cells=obstacle_cells,target_cells=target_cells)
    for i in range(0, rows - 4):
        for j in range(0, cols - 4):
            grid.place_agent(i + 2, j + 2)


    for i in range(timesteps):
        print(grid.display())
        print(f"\n{i} Zeitschritt")
        grid.update(target_list=target_cells)
        # Abbruch des Updates, wenn alle Agenten vom Gitter weg sind? (Ersatz von festgelegten timesteps)


def RiMEA4():
    rows = 10
    cols = 150
    timesteps = 200
    # aktuell werden in jedem Zeitschritt aus allen Spawn-Cells Agenten platziert - wird noch angepasst
    # noch fix auf eine Zelle gesetzt / Anpassung an Zellgrössen-Änderung
    spawn_cells = []
    for i in range(0, rows):
            spawn_cells.append((i, 0))
    obstacle_cells = [(4, 24), (5, 24), (4, 25), (5, 25), (4, 74), (5, 74), (6, 74), (7, 74), (4, 75), (5, 75), (6, 75), (7, 75)] 
    target_cells = [(0, 149), (1, 149), (2, 149), (3, 149), (4, 149), (5, 149), (6, 149), (7, 149), (8, 149), (9, 149)]
    print(target_cells)

    grid = Grid(rows, cols, spawn_cells=spawn_cells, obstacle_cells=obstacle_cells,target_cells=target_cells)
    #grid.place_agent(i + 2, j + 2)


    for i in range(timesteps):
        print(grid.display())
        print(f"\n{i} Zeitschritt")
        grid.update(target_list=target_cells)