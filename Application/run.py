from Grid import Grid
from Cell import Cell, SpawnCell, BorderCell, ObstacleCell, Agent, TargetCell
import matplotlib.pyplot as plt
import numpy as np 
from Grid import Grid, Visualization
from tests import room_square, ChickenTest, RiMEA9, RiMEA4, Experiment
import matplotlib
#This line is needed for the plots to render in Pychamr Sciplot-View
matplotlib.use("Qt5Agg")
#Using the Maps from tests build a grid. every map returns a grid, door_cells (used as boundary zones for flow measurements) and roi (region used to calculate agent density)
#grid, door_cells, roi = RiMEA9(2,"dijkstra")
#grid, door_cells, roi = RiMEA9(1, "dijsktra")
#grid, door_cells, roi = RiMEA9(3, "dijkstra")
#grid, door_cells, roi = RiMEA9(4, "dijkstra")
#grid, door_cells, roi = RiMEA4(movement_method="dijkstra", spawn_rate=0.6)
#grid, door_cells, roi = Experiment("dijkstra")
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
#exp_grid, roi = Experiment("dijkstra")
#exp_grid.plot_grid_state(timestep=0)
visualization = Visualization(grid)
agent_count_list = []
fundamental_data = []


grid.update_distance_maps()
agents_crossed = {}  # Dictionary to track agents crossing the boundary
for i in range(timesteps):
    grid.update(target_list=grid.target_cells, timestep=i)
    print("--------------------------------------------------------------------------------------------------")
    #Select current area inside of Hallway or Room to see how many agents are still inside (for FundamentalDiagram)
    area = grid.select_area_by_coordinates(roi[0], roi[1], roi[2], roi[3])
    if i == 0:
        initial_count = len(grid.agents)
        print(f"init{initial_count}")
    visualization.plot_grid_state(i)
    #grid.plot_grid_state(i)
    plt.pause(1)
    #print(f"len_agentscrossed:{len(agents_crossed)}")
    # Calculate density, speed, and flow: Set Boundarys to be doorcells (as defined in Rimea), pass current timestep, already_crossed agents and the area for density calculation
    fd_results = grid.calculate_fundamental_diagram(door_cells, i, agents_crossed, area)
    fundamental_data.append(fd_results)


    # Update previous positions for the next timestep
    agent_count = len(grid.agents)
    agent_count_list.append(agent_count)
    if agent_count == 0:
        print("All agents have reached their targets. Stopping simulation.")
        break


plot = visualization.plot_fundamental_diagram(fundamental_data)














































#plot_fundamental_diagram_with_dual_axis(densities, speeds, flows)
#plt.figure(figsize=(10,5))

#plt.subplot(1, 4, 1)
#plt.plot(agent_count_list)
#plt.title('Anzahl Agenten über Zeit')
#plt.xlabel('Zeitschritt')
#plt.ylabel('Anzahl Agenten')

#plt.subplot(1, 4, 2)
#plt.plot(average_distance_list)
#plt.title('Mittlere Distanz Agenten zum Ziel')
#plt.xlabel('Zeitschritt')
#plt.ylabel('Distanz')

#plt.subplot(1, 4, 3)
#plt.plot(average_speed_list)
#plt.title('Mittlere Geschwindigkeit der Agenten')
#plt.xlabel('Zeitschritt')
#plt.ylabel('Geschwindigkeit')

#plt.subplot(1, 4, 4)
#if len(density_list) > len(average_speed_list):
#    plt.plot(density_list[:-1], average_speed_list)
#else:
#    plt.plot(density_list, average_speed_list[:len(density_list)])
#plt.title('Fundamental Diagram of Traffic Flow')
#plt.xlabel('Dichte')
#plt.ylabel('Mittlere Geschwindigkeit')
#
#plt.tight_layout()
#plt.show()

# visualization.animate_grid_states(timesteps) 