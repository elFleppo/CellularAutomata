from Grid import Grid
from Cell import Cell, SpawnCell, BorderCell, ObstacleCell, Agent, TargetCell
import matplotlib.pyplot as plt
import numpy as np 
from Grid import Grid, Visualization
from tests import room_square, ChickenTest, RiMEA9, RiMEA4
def plot_fundamental_diagram(densities, speeds, flows):
    """
    Plot density vs. speed and flow for ROI-based analysis.
    """
    import matplotlib.pyplot as plt

    fig, ax1 = plt.subplots()

    ax1.set_xlabel("Density (agents/m²)")
    ax1.set_ylabel("Speed (m/s)", color="blue")
    ax1.plot(densities, speeds, label="Speed", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    ax2 = ax1.twinx()  # instantiate a second y-axis that shares the same x-axis
    ax2.set_ylabel("Flow (agents/s)", color="red")
    ax2.plot(densities, flows, label="Flow", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    fig.tight_layout()  # ensure everything fits without overlap
    plt.title("Fundamental Diagram at Exit")
    plt.show()
grid = RiMEA9(2, "dijkstra")
visualization = Visualization(grid)

agent_count_list = []
average_distance_list = [] 
average_speed_list = [] 
density_list = []
densities = []
speeds = []
flows = []
timesteps = 10000
grid.update_distance_maps()
for i in range(800):
    grid.update(target_list=grid.target_cells, timestep=i)
    #visualization.plot_grid_state(i)
    grid.plot_grid_state(i)
    plt.pause(0.01)
   # density, speed, flow = grid.calculate_density_speed_flow_in_rectangular_roi(10, 8, 12, 8)
    #densities.append(density)
    #speeds.append(speed)
    #flows.append(flow)
    agent_count = len(grid.agents)
    agent_count_list.append(agent_count)

    # berechne dichte
    total_area = grid.length * grid.height  
    density = agent_count / total_area
    density_list.append(density)

    if agent_count == 0:
        print("All agents have reached their targets. Stopping simulation.")
        break

    # berechne mittlere Geschwindigkeit
    total_speed = sum(agent.velocity for agent in grid.agents)
    if agent_count > 0:
        average_speed = total_speed / agent_count
    else:
        average_speed = 0  # Avoid division by zero
    average_speed_list.append(average_speed)

    # mittlere distanz von Agenten zu Ziel
    total_distance_to_target = 0
    if len(grid.agents) > 0:
        for agent in grid.agents:
            target = agent.find_target(grid.target_cells)
            total_distance_to_target += agent.euclidean_distance_to(grid.grid[target[0]][target[1]])
        
        average_distance_list.append(total_distance_to_target / len(grid.agents))
    else:
        average_distance_list.append(np.nan)  
plot_fundamental_diagram(densities, speeds, flows)
plt.figure(figsize=(10,5)) 

plt.subplot(1, 4, 1)
plt.plot(agent_count_list)
plt.title('Anzahl Agenten über Zeit')
plt.xlabel('Zeitschritt')
plt.ylabel('Anzahl Agenten') 

plt.subplot(1, 4, 2)
plt.plot(average_distance_list)
plt.title('Mittlere Distanz Agenten zum Ziel')
plt.xlabel('Zeitschritt')
plt.ylabel('Distanz') 

plt.subplot(1, 4, 3)
plt.plot(average_speed_list)
plt.title('Mittlere Geschwindigkeit der Agenten')
plt.xlabel('Zeitschritt')
plt.ylabel('Geschwindigkeit') 

plt.subplot(1, 4, 4)
if len(density_list) > len(average_speed_list):
    plt.plot(density_list[:-1], average_speed_list)
else:
    plt.plot(density_list, average_speed_list[:len(density_list)])
plt.title('Fundamental Diagram of Traffic Flow')
plt.xlabel('Dichte')
plt.ylabel('Mittlere Geschwindigkeit')

plt.tight_layout()
plt.show()

# visualization.animate_grid_states(timesteps) 