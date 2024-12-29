
from Cell import Cell, BorderCell, SpawnCell, Agent, TargetCell, ObstacleCell

import random
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import heapq
import matplotlib.colors as mcolors
import math
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#Helper function for convert
def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)
#Grid Klasse: Auf dem Grid befinden sich Zellobjekte und über das Grid wird das update() der Zellen durchgeführt
class Grid:
    #Im Init wird das grid entsprechend aufgebaut, es können Listen mit Tuplen für die entsprechenden Zell Objekte mitgegeben werden
    def __init__(self, length, height, spawn_cells, target_cells, obstacle_cells, cell_size=1.0, movement_method="dijkstra"):
        self.length = length
        self.height = height
        self.cell_size = cell_size
        self.rows = int(height / cell_size)
        self.cols = int(length / cell_size)
        self.grid = [
            [Cell(row, col, cell_size=cell_size) for col in range(self.cols)] for row in range(self.rows)
        ]  # Aufbau Grid
        self.spawn_cells = spawn_cells  # Listen für Spawns, Ziele und Hindernisse
        self.target_cells = target_cells
        self.obstacle_cells = obstacle_cells
        self.agents = []  # Liste mit allen Agenten die sich auf dem Feld befinden
        self.movement_method = movement_method
        self.density_data = []
        self.speed_data = []
        self.flow_data = []

        # Aufbau von Spawn, Zielen und Hindernissen
        for row, col in spawn_cells:
            #print(row, col)
            self.grid[row][col] = SpawnCell(row=row, col=col, cell_size=cell_size)
        if obstacle_cells is not None:
            for row, col in obstacle_cells:
                #print(obstacle_cells)
                self.grid[row][col] = ObstacleCell(row=row, col=col, cell_size=cell_size)
        for row, col in target_cells:
            self.grid[row][col] = TargetCell(row=row, col=col, cell_size=cell_size)

    def meter_to_rowcol(self, x, y):
        col = clamp(int(x / self.cell_size), 0, self.cols - 1)
        row = clamp(int(y/ self.cell_size), 0, self.rows - 1)
        return row, col
    def log_grid_state(self, timestep, log_file="logs/grid_states.log"):
        """Log the entire grid's state for visualization."""
        with open(log_file, "a") as logfile:
            logfile.write(f"Timestep: {timestep}\n")
            for row in self.grid:
                logfile.write(" ".join(str(cell) for cell in row) + "\n")
            logfile.write("\n")  # Add a newline for clarity

    def select_area_by_coordinates(self, start_x, start_y, end_x, end_y):
        """
        Selects a rectangular area of cells based on real-world coordinates (meters).
        Converts coordinates to grid indices and returns the cells in the selected area.

        Parameters:
            start_x (float): Starting x-coordinate (meters).
            start_y (float): Starting y-coordinate (meters).
            end_x (float): Ending x-coordinate (meters).
            end_y (float): Ending y-coordinate (meters).

        Returns:
            List[Cell]: A list of Cell objects within the selected area.
        """
        # Convert coordinates to grid indices using clamp
        start_row, start_col = self.meter_to_rowcol(start_x, start_y)
        end_row, end_col = self.meter_to_rowcol(end_x, end_y)


        # Ensure start indices are less than or equal to end indices
        if start_row > end_row or start_col > end_col:
            raise ValueError("Start coordinates must be less than or equal to end coordinates.")

        # Collect the cells in the selected area
        selected_cells = [
            self.grid[row][col]
            for row in range(start_row, end_row + 1)
            for col in range(start_col, end_col + 1)
        ]

        return selected_cells

    def get_agents_in_rectangular_roi(self, start_x, start_y, end_x, end_y):
        """
        Get all agents within a rectangular ROI defined by real-world coordinates.
        Parameters:
            start_x, start_y (float): Bottom-left corner of the rectangle in meters.
            end_x, end_y (float): Top-right corner of the rectangle in meters.
        Returns:
            List[Agent]: List of agents within the ROI.
        """
        selected_cells = self.select_area_by_coordinates(start_x, start_y, end_x, end_y)
        agents_in_roi = [cell for cell in selected_cells if isinstance(cell, Agent)]
        return agents_in_roi
    #Plaziere Wand um Feld
    def place_border(self):
        """Place a border around the grid"""
        for r in range(self.rows):
            for c in range(self.cols):
                if r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1:
                    self.grid[r][c] = BorderCell(cell_size=self.cell_size)
    #Die Untenstehenden methoden erlauben eine Interaktion mit dem Grid ausserhalb der initialisierung
    def place_spawn_cell(self, row,col):
        """Place a spawn cell at a specific position on the grid"""
        #row, col = self.meter_to_rowcol(x, y)
        self.grid[row][col] = SpawnCell(row=row, col=col, cell_size=self.cell_size)
        self.spawn_cells.append((row, col))

    def place_empty_cell(self, row,col):
        """Place a spawn cell at a specific position on the grid"""
        #row, col = self.meter_to_rowcol(x, y)
        self.grid[row][col] = Cell(row=row, col=col, cell_size=self.cell_size)

    def place_target(self, row, col):
        """Place a target cell at a specific position on the grid"""
       # row, col = self.meter_to_rowcol(x, y)
        self.grid[row][col] = TargetCell(row=row, col=col, cell_size=self.cell_size)
        self.target_cells.append((row, col))

    def place_agent(self, row,col):
        """Place an agent at a specific position on the grid"""
        #row, col = self.meter_to_rowcol(x, y)
        agent = Agent(row, col, cell_size=self.cell_size)
        if isinstance(self.grid[row][col], Cell) and not isinstance(self.grid[row][col], TargetCell):
            self.grid[row][col] = agent
            self.agents.append(agent)

    def place_obstacle(self, row,col):
       # row, col = self.meter_to_rowcol(x, y)
        self.grid[row][col] = ObstacleCell(row=row, col=col, cell_size=self.cell_size)

    def is_cell_occupied(self,row,col):
       # row, col = self.meter_to_rowcol(x, y)
        cell = self.grid[row][col]
        return isinstance(cell, Agent)


    #Helper Methode für Djkstra Algorithmus

    def compute_distance_map(self, target):
        """
        Compute the shortest path distances from the target to all cells using Dijkstra's algorithm.
        This version allows setting distances on Agent cells but prohibits Obstacle cells.
        Parameters:
            target (tuple): Coordinates of the target cell as (row, col).
        Returns:
            List[List[float]]: A 2D distance map where each cell contains the shortest distance to the target.
        """
        rows, cols = self.rows, self.cols

        # Initialize the distance map with infinity
        distance_map = [[float('inf')] * cols for _ in range(rows)]

        # Set the distance of the target cell to 0
        target_row, target_col = target
        distance_map[target_row][target_col] = 0

        # Priority queue for processing cells (distance, row, col)
        queue = [(0, target_row, target_col)]

        while queue:
            # Get the cell with the smallest distance
            current_distance, current_row, current_col = heapq.heappop(queue)

            # Skip processing if we've already found a shorter path to this cell
            if current_distance > distance_map[current_row][current_col]:
                continue

            # Get neighbors of the current cell
            neighbors = self.grid[current_row][current_col].get_neighbors(self, radius=1)

            for layer in neighbors.values():
                for neighbor in layer:
                    neighbor_row, neighbor_col = neighbor.row, neighbor.col

                    # Skip obstacle cells
                    if isinstance(self.grid[neighbor_row][neighbor_col], ObstacleCell):
                        continue

                    # Allow distances on Agent cells
                    if isinstance(self.grid[neighbor_row][neighbor_col], Agent):
                        pass  # Agents are treated as passable for distance purposes

                    # Calculate the direct Euclidean distance
                    direct_distance = math.sqrt((target_row - neighbor_row) ** 2 + (target_col - neighbor_col) ** 2)

                    # Update the neighbor's distance if this path is shorter
                    if direct_distance < distance_map[neighbor_row][neighbor_col]:
                        distance_map[neighbor_row][neighbor_col] = direct_distance
                        heapq.heappush(queue, (direct_distance, neighbor_row, neighbor_col))

        return distance_map

    #Helper Methode für Flood Fill, returned Distance map

    def flood_fill(self, target_row, target_col, target_state):
        """
        Perform reverse flood-fill starting from the target (target_row, target_col).
        Computes a distance map where cells closer to the target have smaller values.
        Skips impassable cells (e.g., obstacles, borders).
        Parameters:
            target_row (int): Row index of the target.
            target_col (int): Column index of the target.
            target_state (int): State of the target cell.
        Returns:
            List[List[float]]: A 2D distance map with Manhattan distances to the target.
        """
        # Ensure the target cell is valid
        if not (0 <= target_row < self.rows and 0 <= target_col < self.cols):
            raise ValueError("Target coordinates are out of grid bounds.")

        target_cell = self.grid[target_row][target_col]

        # Early exit if the target cell doesn't match the target state or is impassable
        if target_cell.state != target_state or not target_cell.is_passable():
            raise ValueError("Target cell is invalid or impassable.")

        # Initialize the distance map with infinity
        distance_map = [[float('inf')] * self.cols for _ in range(self.rows)]
        distance_map[target_row][target_col] = 0  # Target cell has distance 0

        # Initialize the queue for BFS with the target cell
        queue = [(target_row, target_col)]

        # Directions for the 4-connected neighborhood (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            current_row, current_col = queue.pop(0)
            current_distance = distance_map[current_row][current_col]

            for dr, dc in directions:
                neighbor_row, neighbor_col = current_row + dr, current_col + dc

                # Skip out-of-bounds cells
                if not (0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols):
                    continue

                neighbor_cell = self.grid[neighbor_row][neighbor_col]

                # Skip obstacle cells
                if isinstance(neighbor_cell, ObstacleCell):
                    continue

                # Allow distances on Agent cells
                if isinstance(neighbor_cell, Agent):
                    pass  # Agents are treated as passable for flood-fill purposes

                # Update the distance for the neighbor if not visited
                if distance_map[neighbor_row][neighbor_col] == float('inf'):
                    distance_map[neighbor_row][neighbor_col] = current_distance + 1
                    queue.append((neighbor_row, neighbor_col))

        return distance_map

    # Display Methode: Momentan noch in Konsole, später mit Plots
    def display(self):
        """Print the current state of the grid"""
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))
        print()

    def compute_social_penalties(grid, cutoff_distance=2.0, penalty_decay_factor=0.5):
        """
        Compute social penalties for all agents using a vectorized approach.
        Parameters:
            grid (Grid): The simulation grid.
            cutoff_distance (float): Maximum distance in meters to consider for social penalties.
            penalty_decay_factor (float): Controls the steepness of the Gaussian decay.
        Returns:
            np.ndarray: Social penalties for all agents.
        """
        positions = grid.get_agent_positions()  # Shape: (num_agents, 2)
        # If positions is 1D, reshape it
        if positions.ndim == 1:
            positions = positions.reshape(-1, 2)
        #print(f"Position : None :{positions[:, None, :]}")
        #print(f"Position  None ::{positions[None, :, :]}")
        arrived = grid.get_agent_arrival_status()  # Shape: (num_agents,)
        num_agents = positions.shape[0]
        #print(num_agents)
        # Compute pairwise Euclidean distances (broadcasting)
        deltas = positions[:, None, :] - positions[None, :, :]  # Shape: (num_agents, num_agents, 2)
        distances = np.linalg.norm(deltas, axis=2)  # Shape: (num_agents, num_agents)

        # Apply cutoff distance (set penalties to 0 beyond this distance)
        mask = (distances <= cutoff_distance) & ~np.eye(num_agents, dtype=bool)  # Ignore self-distances
        distances[~mask] = np.inf

        # Apply Gaussian decay penalty
        penalties = np.exp(-(distances ** 2) / (2 * penalty_decay_factor ** 2))  # Shape: (num_agents, num_agents)
        penalties[~mask] = 0  # Ensure penalties are 0 for distances > cutoff

        # Sum penalties for each agent
        total_penalties = penalties.sum(axis=1)  # Shape: (num_agents,)

        # Add a small penalty for staying in place
        stay_penalty = 0.5
        total_penalties += stay_penalty

        return total_penalties




    #Update funktion: Wir müssen nur die Agenten bewegen und die Spawns für den nächsten Zeitschritt durchführen
 #  def update(self, target_list, timestep):
 #
 #      if timestep == 0:
 #          self.update_distance_maps()
 #
 #      #Bewege Agenten
 #      for agent in self.agents:
 #          if agent.arrived == True:
 #              self.agents.remove(agent)
 #
 #          #print(agent)
 #          if self.movement_method == "floodfill":
 #              agent.movement_towards_target(self)
 #          elif self.movement_method == "dijkstra":
 #              agent.movement_towards_target(self)  # Pass the grid instance
 #
 #          agent.log_state(timestep)
 #      densities, speeds, flows = self.calculate_density_speed_flow()
 #      self.density_data.append(densities)
 #      self.speed_data.append(speeds)
 #      self.flow_data.append(flows)
 #      #Spawne Agenten (
 #      for row, col in self.spawn_cells:
 #          cell = self.grid[row][col]
 #          if isinstance(cell, SpawnCell):  # Check if the cell at (row, col) is a SpawnCell
 #              max_agents = 1  # Adjust the number of agents to spawn as needed
 #              cell.spawn_agents(self, max_agents)
 #
 #      self.log_grid_state(timestep)
    def update(self, target_list, timestep):
        """
        Update the grid by moving agents and handling arrivals.
        """
        if timestep == 0:
            self.update_distance_maps()

        # Compute social penalties
        precomputed_penalties = self.compute_social_penalties()

        # List to track agents to remove
        agents_to_remove = []

        for i, agent in enumerate(self.agents[:]):  # Iterate over a copy of the agents list
            if agent.arrived:
                agents_to_remove.append(agent)
                continue

            new_position = agent.movement_decision(self, precomputed_penalties, i)
            if new_position:
                current_row, current_col = agent.row, agent.col
                new_row, new_col = new_position

                # Update grid: Move the agent
                if not isinstance(self.grid[new_row][new_col], TargetCell):
                    self.grid[new_row][new_col] = agent

                # Restore the current cell
                self.grid[current_row][current_col] = (
                    TargetCell(current_row, current_col, self.cell_size)
                    if (current_row, current_col) in target_list
                    else Cell(current_row, current_col, self.cell_size)
                )

                # Update agent position
                agent.row, agent.col = new_row, new_col

        # Remove agents that have arrived
        for agent in agents_to_remove:
            print(f"Removing agent {agent} from ({agent.row}, {agent.col})")
            self.agents.remove(agent)

            # Restore target cell explicitly
            if (agent.row, agent.col) in target_list:
                self.grid[agent.row][agent.col] = TargetCell(agent.row, agent.col, self.cell_size)
            else:
                self.grid[agent.row][agent.col] = Cell(agent.row, agent.col, self.cell_size)

        # Spawn new agents
        for row, col in self.spawn_cells:
            cell = self.grid[row][col]
            if isinstance(cell, SpawnCell):
                max_agents = 1
                cell.spawn_agents(self, max_agents)

        self.log_grid_state(timestep)

    def calculate_movement(self,agent):
        if not agent.arrived:
            # Store the agent's movement decision (current and next position)
            return (agent, agent.movement_decision(self))  # New method to compute move
        return None

    def update_p(self, target_list, timestep):
        """
            Parallelized update for agent movements with resolved self references.
            """

        # Helper function to calculate an agent's movement
        def calculate_movement(agent, grid):
            if not agent.arrived:
                return (agent, agent.movement_decision(grid))
            return None

        # Step 1: Compute movements in parallel
        move_decisions = []
        with ThreadPoolExecutor() as executor:
            move_decisions = list(
                filter(
                    None,
                    executor.map(lambda agent: calculate_movement(agent, self), self.agents),
                )
            )

        # Step 2: Apply movements sequentially to update the grid
        for agent, new_position in move_decisions:
            if new_position:
                # Clear the agent's current position
                self.grid[agent.row][agent.col] = Cell(agent.row, agent.col, cell_size=self.cell_size)
                # Move the agent to the new position
                self.grid[new_position[0]][new_position[1]] = agent
                agent.row, agent.col = new_position

        # Remove agents that arrived at their targets
        self.agents = [agent for agent in self.agents if not agent.arrived]

        print(f"Timestep {timestep} complete. Active agents: {len(self.agents)}")

    def update_distance_maps(self):
        """
        Compute and store both flood-fill and Dijkstra-based distance maps for all targets.
        """
        # Initialize dictionaries to store both types of maps
        self.flood_fill_distance_maps = {}
        self.dijkstra_distance_maps = {}

        for row, col in self.target_cells:

            # Flood-fill distance map
            if self.movement_method == "floodfill":

                self.flood_fill_distance_maps[(row, col)] = self.flood_fill(row, col, target_state=3)
            elif self.movement_method == "dijkstra":

            # Dijkstra distance map
                self.dijkstra_distance_maps[(row, col)] = self.compute_distance_map((row, col))

    def plot_distance_map(self, distance_map, title="Distance Map"):
        """
        Plots the given distance map as a heatmap using matplotlib and seaborn.

        Parameters:
            distance_map (List[List[float]]): The 2D distance map to plot.
            title (str): Title for the heatmap.
        """


        # Convert distance map to a numpy array for easier handling
        distance_array = np.array(distance_map)

        # Determine color scale limits for better visualization
        finite_values = distance_array[np.isfinite(distance_array)]  # Exclude inf values
        vmin = finite_values.min() if len(finite_values) > 0 else 0
        vmax = finite_values.max() if len(finite_values) > 0 else 1

        # Create a heatmap using seaborn
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            distance_array,
            annot=False,  # No annotations inside the cells
            cmap="coolwarm",  # Color map for gradient
            cbar=True,  # Display color bar
            square=True,  # Ensure square cells
            linewidths=0,  # Remove lines between cells
            vmin=vmin,  # Set minimum value for color scale
            vmax=vmax  # Set maximum value for color scale
        )

        # Add title and labels
        plt.title(title)
        plt.xlabel("Columns")
        plt.ylabel("Rows")
        plt.show()



    def plot_grid_state(grid, timestep):
        #Plot Ausgabe für klarere Visualisierung, momentan noch über States für Farbwahl: Evtl besser mit cell.color?
        # Convert grid to a DataFrame for easy visualization
        data = [[cell.state for cell in row] for row in grid.grid]
        # Define a custom color map for the cell states
        custom_colors = {
            0: 'white',  # Empty cells
            1: 'yellow',  # Border cells
            2: 'green',  # Spawn cells
            3: 'red',  # Target cells
            4: 'gray',  # Obstacles
            47: 'blue'  # Agents
        }

        # Create a colormap with `matplotlib.colors`
        cmap = mcolors.ListedColormap([custom_colors[key] for key in sorted(custom_colors.keys())])
        bounds = list(sorted(custom_colors.keys())) + [max(custom_colors.keys()) + 1]  # Add bounds for each state
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        # Plot with Seaborn
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            data,
            cmap=cmap,
            norm=norm,
            linewidths=0.5,
            linecolor='black',  # Gridlines for better clarity
            cbar=False,  # Disable default color bar
            xticklabels=False,  # Remove x-axis labels
            yticklabels=False  # Remove y-axis labels
        )
        plt.title(f"Grid State at Timestep {timestep}")
        plt.xlabel("Columns")
        plt.ylabel("Rows")
        plt.show()



    def get_agent_positions(self):
        """
        Extract the positions of all agents as a NumPy array.
        Returns:
            np.ndarray: Array of shape (num_agents, 2) with rows [row, col].
        """
        return np.array([[agent.row, agent.col] for agent in self.agents])

    def get_agent_arrival_status(self):
        """
        Extract whether each agent has arrived.
        Returns:
            np.ndarray: Boolean array of shape (num_agents,) indicating arrival status.
        """
        return np.array([agent.arrived for agent in self.agents])

    def get_agent_velocities(self):
        """
        Extract the velocities of all agents.
        Returns:
            np.ndarray: Array of shape (num_agents,) with agent velocities.
        """
        return np.array([agent.velocity for agent in self.agents])

   # def plot_fundamental_diagram(self):
   #     """
   #     Plot the fundamental diagram with density vs speed and flow.
   #     """
   #
   #
   #     densities = self.density_data
   #     speeds = self.speed_data
   #     flows = self.flow_data
   #
   #     fig, ax1 = plt.subplots()
   #
   #     ax1.set_xlabel("Density (agents/unit area)")
   #     ax1.set_ylabel("Speed (units/time)", color="blue")
   #     ax1.plot(densities, speeds, label="Speed", color="blue")
   #     ax1.tick_params(axis="y", labelcolor="blue")
   #
   #     ax2 = ax1.twinx()  # instantiate a second y-axis that shares the same x-axis
   #     ax2.set_ylabel("Flow (agents/unit time)", color="red")
   #     ax2.plot(densities, flows, label="Flow", color="red")
   #     ax2.tick_params(axis="y", labelcolor="red")
   #
   #     fig.tight_layout()  # ensure everything fits without overlap
   #     plt.title("Fundamental Diagram")
   #     plt.show()

    def calculate_fundamental_diagram(self, boundary, timestep, agents_crossed, area):
        """
        Calculate and plot the Fundamental Diagram.

        Parameters:
            grid (Grid): The simulation grid.
            boundary (list): A list of (row, col) tuples representing the boundary.
            timestep (int): The current simulation timestep.
            agents_crossed (dict): A dictionary tracking agents that crossed the boundary.


        Returns:
            dict: Contains density, flow, and average speed for the timestep.
        """
        # Step 1: Calculate Flow (Agents crossing the boundary in this timestep)
        current_crossed_agents = []
        for coordinates in boundary:
            cell = self.grid[coordinates.row][coordinates.col]
            if isinstance(cell, Agent) and cell.id not in agents_crossed:
                current_crossed_agents.append(cell)
                agents_crossed[cell.id] = timestep  # Track the agent's crossing

        flow = len(current_crossed_agents)  # Number of agents crossing the boundary

        # Step 2: Calculate Density (Agents per square meter in the Room or Hallway)
       # region_in_front = self.select_area_by_coordinates(*region_coordinates)
        agent_count = 0
        agent_count = sum(
            1 for cell in area if isinstance(cell, Agent)
        )
        print(f"agent count{agent_count}")
        area_squared = sum(
            self.cell_size**2 for cell in area if(cell.cell_size>0)
        )
       # print(area_squared)
    # Area of region in m^2

        density = agent_count / area_squared if area_squared > 0 else 0
        print(f"density:{density}")
        # Step 3: Calculate Average Speed (of agents crossing the boundary)
        avg_speed = (
            sum(agent.velocity for agent in current_crossed_agents) / len(current_crossed_agents)
            if current_crossed_agents else 0
        )

        # Step 4: Return and log the results
        results = {
            "density": density,
            "flow": flow,
            "avg_speed": avg_speed,
            "timestep": timestep,
        }

        print(f"Timestep {timestep}: Density={density:.2f}, Flow={flow:.2f}, AvgSpeed={avg_speed:.2f}")
        return results

    def plot_fundamental_diagram(self, data):
        """
        Plot the Fundamental Diagram based on collected data.

        Parameters:
            data (list): A list of dictionaries containing density, flow, and average speed values.
        """
        densities = [entry["density"] for entry in data]
        flows = [entry["flow"] for entry in data]
        avg_speeds = [entry["avg_speed"] for entry in data]

        fig, ax1 = plt.subplots()

        # Plot Flow vs. Density
        ax1.plot(densities, flows, 'b-o', label="Flow")
        ax1.set_xlabel("Density (agents/m^2)")
        ax1.set_ylabel("Flow (agents/s)", color="blue")
        ax1.tick_params(axis='y', labelcolor="blue")

        # Plot Avg Speed vs. Density
        ax2 = ax1.twinx()
        ax2.plot(densities, avg_speeds, 'r-s', label="Average Speed")
        ax2.set_ylabel("Average Speed (m/s)", color="red")
        ax2.tick_params(axis='y', labelcolor="red")

        fig.tight_layout()
        plt.title("Fundamental Diagram")
        plt.show()
    


    def create_logfile(self):
        path = f"gridlog-{self.__hash__()}.txt"
        if(os.path.isfile(path)):
            return "File already exists"
        else:
            with open(path, "w") as fp:
                pass
            return "File created"

class Visualization:
    def __init__(self, grid):
        self.grid = grid
        self.fig, self.ax = plt.subplots()

    def plot_grid_state(self, timestep):
        data = [[cell.state for cell in row] for row in self.grid.grid]

        custom_colors = {
            0: 'white',  # Empty cells
            1: 'yellow',  # Border cells
            2: 'green',  # Spawn cells
            3: 'red',  # Target cells
            4: 'gray',  # Obstacles
            47: 'blue'  # Agents
        }

        cmap = mcolors.ListedColormap([custom_colors[key] for key in sorted(custom_colors.keys())])
        bounds = list(sorted(custom_colors.keys())) + [max(custom_colors.keys()) + 1]  
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        self.ax.clear()
        self.ax.imshow(data, cmap=cmap, norm=norm)

        
        self.ax.set_title(f"Grid State at Timestep {timestep}")
        self.ax.set_xlabel("Columns")
        self.ax.set_ylabel("Rows")

    def animate_grid_states(self, timesteps):
        def update(frame):
            self.grid.update(target_list=self.grid.target_cells, timestep=frame)
            self.plot_grid_state(frame)

        ani = animation.FuncAnimation(self.fig, update, frames=timesteps, interval=10)
        plt.show()
