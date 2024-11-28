from Grid import Grid
from Cell import Cell, SpawnCell, BorderCell, ObstacleCell, Agent, TargetCell
import matplotlib.pyplot as plt
import numpy as np 

#Einfacher aufbau um erste Visualisierung zu machen
rows = 15
cols = 15
timesteps = 20
spawn_cells = [(8, 6),(2, 7)]
obstacle_cells = [(4, 2),(7, 1)]
target_cells = [(4, 1), (8, 1)]

agent_count_list = []
average_distance = []

grid = Grid(rows, cols, spawn_cells=spawn_cells, obstacle_cells=obstacle_cells,target_cells=target_cells)

plt.ion()

for i in range(timesteps):
    #print(grid.display())
    grid.update(target_list=target_cells, timestep=i)
    
    plt.clf()  # clear current figure
    grid.plot_grid_state(i) 
    plt.pause(0.01)  # pause for a short time to allow the plot to be rendered
    
    agent_count = len(grid.agents)
    agent_count_list.append(agent_count)

    # mittlere distanz von Agenten zu Ziel
    total_distance_to_target = 0
    if len(grid.agents) > 0:
        total_istance_to_target = 0
        for agent in grid.agents:
            potential = abs(agent.potential(grid, target_list=target_cells))
            total_distance_to_target += potential
        
        average_distance.append(total_distance_to_target / len(grid.agents))
    else:
        average_distance.append(np.nan)  

plt.ioff()
plt.figure(figsize=(10,5)) 

plt.subplot(1, 2, 1)
plt.plot(agent_count_list)
plt.title('Anzahl Agenten über Zeit')
plt.xlabel('Zeitschritt')
plt.ylabel('Anzahl Agenten')

plt.subplot(1, 2, 2)
plt.plot(average_distance)
plt.title('Mittlere Distanz Agenten zum Ziel')
plt.xlabel('Zeitschritt')
plt.ylabel('Distanz')

plt.tight_layout()
plt.show()

