from Grid import Grid
from Cell import Cell, SpawnCell, BorderCell, ObstacleCell, Agent, TargetCell
import matplotlib.pyplot as plt
import numpy as np 
from Grid import Grid, Visualization
from tests import room_square, ChickenTest, RiMEA9, RiMEA4

room_height = 20
room_length = 30
frameSize = 5
height = room_height + 2 * frameSize
length = room_length + 2 * frameSize
grid, door_cells = RiMEA9(1, "dijkstra")


visualization = Visualization(grid)
#region_cord = (frameSize + 4, frameSize+1, frameSize + 5, frameSize+1)
#region_2_cord = (length - frameSize - 5, height - frameSize, length - frameSize - 4, height - frameSize)

#region = grid.select_area_by_coordinates(frameSize + 4, frameSize, frameSize + 5, frameSize)
agent_count_list = []
average_distance_list = [] 
average_speed_list = [] 
density_list = []
densities = []
speeds = []
flows = []
fundamental_data = []
fundamental_data2 = []
timesteps = 10000
grid.update_distance_maps()
agents_crossed = {}  # Dictionary to track agents crossing the boundary
for i in range(40):
    grid.update(target_list=grid.target_cells, timestep=i)
    #Select current area inside of Hallway or Room to see how many agents are still inside (for FundamentalDiagram)
    area = grid.select_area_by_coordinates(frameSize, frameSize, length - frameSize, height - frameSize)
    if i == 0:
        initial_count = len(grid.agents)
        print(f"init{initial_count}")

    #visualization.plot_grid_state(i)
    grid.plot_grid_state(i)
    plt.pause(1)
    print(f"len_agentscrossed:{len(agents_crossed)}")

    # Calculate density, speed, and flow: Set Boundarys to be doorcells (as defined in Rimea), pass current timestep, already_crossed agents and the area for density calculation
    #print(agents_crossed)
    if len(agents_crossed) <= initial_count:
        fd_results = grid.calculate_fundamental_diagram(door_cells, i, agents_crossed, area)
        print(type(fd_results))
        fundamental_data.append(fd_results)
        #print(fundamental_data)
    # Store results for plotting
    print(type(fundamental_data))


    # Update previous positions for the next timestep

    agent_count = len(grid.agents)
    agent_count_list.append(agent_count)




    if agent_count == 0:
        print("All agents have reached their targets. Stopping simulation.")
        break




#Dataprep before plotting


#grid.plot_fundamental_diagram(fundamental_data)
    def plot_fundamental_diagram(data):
        """Generate two separate plots from fundamental diagram data."""

        # Extract data
        timesteps = [entry["timestep"] for entry in data if entry["flow"]>0]
        densities = [entry["density"] for entry in data if entry["flow"]>0]
        avg_speeds = [entry["avg_speed"] for entry in data if entry["flow"]>0]

        # Plot 1: Density over time
        plt.figure(figsize=(10, 6))
        plt.plot(timesteps, densities, marker="o", label="Density over time")
        plt.title("Density Over Time")
        plt.xlabel("Timestep")
        plt.ylabel("Density (agents/m^2)")
        plt.grid(True)
        plt.legend()
        plt.savefig("Density_over_time")
        plt.show()

        # Plot 2: Average speed relative to density
        plt.figure(figsize=(10, 6))
        plt.plot(densities, avg_speeds, marker="s", label="Avg Speed vs. Density", color="red")
        plt.title("Average Speed Relative to Density")
        plt.xlabel("Density (agents/m^2)")
        plt.ylabel("Average Speed (m/s)")
        plt.grid(True)
        plt.legend()
        plt.savefig("Speed_relative_to_density")
        plt.show()

plot = plot_fundamental_diagram(fundamental_data)














































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