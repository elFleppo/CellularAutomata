from Grid import Grid
from Cell import Cell, SpawnCell, BorderCell, ObstacleCell, Agent, TargetCell
import matplotlib.pyplot as plt
import numpy as np 
from Grid import Grid, Visualization
from tests import room_square, ChickenTest, RiMEA9, RiMEA4
import tests
grid = RiMEA9(1, "floodfill")
visualization = Visualization(grid)

agent_count_list = []
average_distance = [] 
density_list = []
timesteps = 10

for i in range(timesteps):
    grid.update(target_list=grid.target_cells, timestep=i)
    #visualization.plot_grid_state(i)
    grid.plot_grid_state(i)
    plt.pause(0.2)

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

plt.subplot(1, 3, 1)
plt.plot(agent_count_list)
plt.title('Anzahl Agenten über Zeit')
plt.xlabel('Zeitschritt')
plt.ylabel('Anzahl Agenten') 

plt.subplot(1, 3, 2)
plt.plot(average_distance)
plt.title('Mittlere Distanz Agenten zum Ziel')
plt.xlabel('Zeitschritt')
plt.ylabel('Distanz') 



plt.tight_layout()
plt.show()

visualization.animate_grid_states(timesteps)