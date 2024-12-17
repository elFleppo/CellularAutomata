from Grid import Grid
from Cell import Cell, SpawnCell, BorderCell, ObstacleCell, Agent, TargetCell
import matplotlib.pyplot as plt
import numpy as np 
from Grid import Grid, Visualization
from tests import room_square, ChickenTest, RiMEA9, RiMEA4
'''''''''
rows = 20
cols = 20
timesteps = 50
spawn_cells = [(15, 2),(15, 12)]
obstacle_cells = [(6, 0),(6, 1),(6, 2),(6, 3),(6, 4),(6, 5),(6, 6),(6, 7),(6, 8),(6, 9),(6, 10),(6, 11),(6, 12),(6, 13),(6, 14),(6, 15),(6, 16),(6, 17),(6, 19),
                  (9, 0),(9, 1),(9, 2),(9, 4),(9, 5),(9, 6),(9, 7),(9, 8),(9, 9),(9, 10),(9, 11),(9, 12),(9, 13),(9, 14),(9, 15),(9, 16),(9, 17),(9, 18), (9, 19)]
target_cells = [(2, 2)]

grid = Grid(rows, cols, spawn_cells, target_cells, obstacle_cells)
'''''''''
grid = RiMEA4()
visualization = Visualization(grid)

agent_count_list = []
average_distance = [] 
timesteps = 10

for i in range(timesteps):
    grid.update(target_list=grid.target_cells, timestep=i)
    grid.plot_grid_state(timestep=i)
    #visualization.plot_grid_state(i)
    #plt.pause(0.1)

    agent_count = len(grid.agents)
    agent_count_list.append(agent_count)

    # mittlere distanz von Agenten zu Ziel
    total_distance_to_target = 0
    if len(grid.agents) > 0:
        total_istance_to_target = 0
        for agent in grid.agents:
            target = agent.find_target(grid.target_cells)
            total_distance_to_target += agent.euclidean_distance_to(grid.grid[target[0]][target[1]])
        
        average_distance.append(total_distance_to_target / len(grid.agents))
    else:
        average_distance.append(np.nan)  

   

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

visualization.animate_grid_states(timesteps)