from Grid import Grid
from Cell import Cell, SpawnCell, ObstacleCell, Agent, TargetCell
import matplotlib.pyplot as plt
import numpy as np 
from Grid import Grid, Visualization
from tests import room_square, ChickenTest, RiMEA9, RiMEA4, Experiment
import matplotlib
#This line is needed for the plots to render in Pychamr Sciplot-View
matplotlib.use("Qt5Agg")
#Abschnitt in dem Die simulations Parameter angegeben werden.
time_input = input("Bitte geben sie die Anzahl Zeitschritte an (ein Zeitschritt ist 1 Sekunde)")
timesteps = int(time_input)
user_input = input("Bitte geben sie an welchen Test (RiMEA4, RiMEA9 oder Experiment) sie durchführen wollen")
if user_input == "RiMEA9":
    door_input = input("Bitte Anzahl (1-4) Türen angeben")
    pathfinding = input("Bitte Algorithmus wählen (dijkstra, floodfill)")
    if pathfinding == "floodfill":
        algo = "floodfill"
    elif pathfinding == "dijkstra":
        algo = "dijkstra"
    else:
        algo = "dijkstra" #Standardwert ist dijkstra
    doors = int(door_input)
    grid, door_cells, roi = RiMEA9(movement_method=algo, Doors=doors)
elif user_input == "RiMEA4":
    pathfinding = input("Bitte Algorithmus wählen (dijkstra, floodfill)")
    if pathfinding == "floodfill":
        algo = "floodfill"
    elif pathfinding == "dijkstra":
        algo = "dijkstra"
    else:
        algo = "dijkstra" #Standardwert ist dijkstra
    spawn_input = input("Bitte spawnrate zwischen 0 und 1 eingeben um Personendichte zu variieren (Wird mit einer Zufallsvariable zwischen 0 und 1 verglichen um spawn zu bestimmen)")
    grid, door_cells, roi = RiMEA4(movement_method=algo,spawn_rate=float(spawn_input))
elif user_input == "Experiment":
    pathfinding = input("Bitte Algorithmus wählen (dijkstra, floodfill)")
    if pathfinding == "floodfill":
        algo = "floodfill"
    elif pathfinding == "dijkstra":
        algo = "dijkstra"
    else:
        algo = "dijkstra"  # Standardwert ist dijkstra
    spawn_input = input("Bitte spawnrate zwischen 0 und 1 eingeben um Personendichte zu variieren (Wird mit einer Zufallsvariable zwischen 0 und 1 verglichen um spawn zu bestimmen)")
    grid, door_cells, roi = Experiment(movement_method=algo, spawn_rate=float(spawn_input))
####################################################
#Visualisierung initialisieren und Variablen für Resultate anlegen
visualization = Visualization(grid)
agent_count_list = []
fundamental_data = []


grid.update_distance_maps()# Befor wir die Simulation starten setzen wir bereits die Distance-Maps für Dijkstra/Floodfill
agents_crossed = {}  # Dictionary to track agents crossing the boundary
for i in range(timesteps):
    grid.update(target_list=grid.target_cells, timestep=i)
    #Print statement trent einzelne Zeitschritte von einander (für einfacheres debugging)
    print("--------------------------------------------------------------------------------------------------")
    #Visualisierung aktueller grid-state
    visualization.plot_grid_state(i)
    #Bereich für Density berechnung von aktuelem Grid state wählen
    area = grid.select_area_by_coordinates(roi[0], roi[1], roi[2], roi[3])
    #grid.plot_grid_state(i)

    #Berechnung fürs Fundamentaldiagram (Aktuelle Agenten dichte, Fluss und durchschnittsgeschwindigkeit)
    fd_results = grid.calculate_fundamental_diagram(door_cells, i, agents_crossed, area)
    fundamental_data.append(fd_results)
#Nachdem die Simulation durchgeführt wurde plotten wir noch die Ergebnisse der Fundamentaldiagram Berechnungen
visualization.plot_fundamental_diagram(fundamental_data)