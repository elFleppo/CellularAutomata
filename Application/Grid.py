
from Cell import Cell, BorderCell, SpawnCell, Agent, TargetCell, ObstacleCell

import random
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import heapq
import matplotlib.colors as mcolors

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

        # Aufbau von Spawn, Zielen und Hindernissen
        for row, col in spawn_cells:
            print(row, col)
            self.grid[row][col] = SpawnCell(row=row, col=col, cell_size=cell_size)
        if obstacle_cells is not None:
            for row, col in obstacle_cells:
                print(obstacle_cells)
                self.grid[row][col] = ObstacleCell(row=row, col=col, cell_size=cell_size)
        for row, col in target_cells:
            self.grid[row][col] = TargetCell(row=row, col=col, cell_size=cell_size)


    def log_grid_state(self, timestep, log_file="logs/grid_states.log"):
        """Log the entire grid's state for visualization."""
        with open(log_file, "a") as logfile:
            logfile.write(f"Timestep: {timestep}\n")
            for row in self.grid:
                logfile.write(" ".join(str(cell) for cell in row) + "\n")
            logfile.write("\n")  # Add a newline for clarity
    #Plaziere Wand um Feld
    def place_border(self):
        """Place a border around the grid"""
        for r in range(self.rows):
            for c in range(self.cols):
                if r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1:
                    self.grid[r][c] = BorderCell(cell_size=self.cell_size)
    #Die Untenstehenden methoden erlauben eine Interaktion mit dem Grid ausserhalb der initialisierung
    def place_spawn_cell(self, x,y):
        """Place a spawn cell at a specific position on the grid"""
        row = clamp(int(y / self.cell_size), 0, self.rows - 1)
        col = clamp(int(x / self.cell_size), 0, self.cols - 1)
        self.grid[row][col] = SpawnCell(row=row, col=col, cell_size=self.cell_size)
        self.spawn_cells.append((row, col))

    def place_target(self, x, y):
        """Place a target cell at a specific position on the grid"""
        row = clamp(int(x / self.cell_size), 0, self.rows - 1)
        col = clamp(int(y / self.cell_size), 0, self.cols - 1)
        self.grid[row][col] = TargetCell(row=row, col=col, cell_size=self.cell_size)
        self.target_cells.append((row, col))

    def place_agent(self, x,y):
        """Place an agent at a specific position on the grid"""
        row = clamp(int(y / self.cell_size), 0, self.rows - 1)
        col = clamp(int(x / self.cell_size), 0, self.cols - 1)
        agent = Agent(row, col, cell_size=self.cell_size)
        if isinstance(self.grid[row][col], Cell) and not isinstance(self.grid[row][col], TargetCell):
            self.grid[row][col] = agent
            self.agents.append(agent)

    def place_obstacle(self, x,y):
        row = clamp(int(y / self.cell_size), 0, self.rows - 1)
        col = clamp(int(x / self.cell_size), 0, self.cols - 1)
        self.grid[row][col] = ObstacleCell(row=row, col=col, cell_size=self.cell_size)

    def is_cell_occupied(self,x,y):
        row = clamp(int(y / self.cell_size), 0, self.rows - 1)
        col = clamp(int(x / self.cell_size), 0, self.cols - 1)
        cell = self.grid[row][col]
        return isinstance(cell, Agent)


    #Helper Methode für Djkstra Algorithmus
    def compute_distance_map(grid, target):
        """
        Compute the shortest path distances from the target to all cells using Dijkstra's algorithm.
        Neighbors are retrieved using the `get_neighbors(radius=1)` method.
        """
        # Get grid dimensions
        rows, cols = grid.rows, grid.cols

        # Initialize distance map with "infinity" (unreachable by default)
        distance_map = [[float('inf')] * cols for _ in range(rows)]

        # Set the distance of the target cell to 0
        target_row, target_col = target
        distance_map[target_row][target_col] = 0

        # Priority queue for processing cells (distance, row, column)
        queue = [(0, target_row, target_col)]

        while queue:
            # Get the next cell with the smallest distance
            current_distance, current_row, current_col = heapq.heappop(queue)

            # Skip if we've already found a shorter distance for this cell
            if current_distance > distance_map[current_row][current_col]:
                continue

            # Get the neighbors using the `get_neighbors` method
            current_cell = grid.grid[current_row][current_col]
            neighbors = current_cell.get_neighbors(grid, radius=1)

            # Flatten the dictionary of neighbors into a single list of cells
            neighbor_cells = [
                neighbor
                for layer in neighbors.values()  # Iterate over neighbor layers (distance 1)
                for neighbor in layer
            ]

            # Explore each neighbor
            for neighbor in neighbor_cells:
                neighbor_row, neighbor_col = neighbor.row, neighbor.col

                # Skip if the neighbor is an obstacle
                if isinstance(neighbor, ObstacleCell):
                    continue

                # Calculate the distance to this neighbor
                new_distance = current_distance + grid.grid[current_row][current_col].cell_size

                # Update the distance map and queue if we've found a shorter path
                if new_distance < distance_map[neighbor_row][neighbor_col]:
                    distance_map[neighbor_row][neighbor_col] = new_distance
                    heapq.heappush(queue, (new_distance, neighbor_row, neighbor_col))

        return distance_map

    #Helper Methode für Flood Fill, returned Distance map
    def flood_fill(self, target_row, target_col, target_state):
        """
        Perform reverse flood-fill starting from the target (target_row, target_col).
        Computes a distance map where cells closer to the target have smaller values.
        Skips impassable cells (e.g., obstacles, borders).
        Returns the distance map.
        """
        # Ensure the target cell is valid
        if not (0 <= target_row < self.rows and 0 <= target_col < self.cols):
            print("target out of bounds")
            return None  # Invalid target position

        target_cell = self.grid[target_row][target_col]

        # Early exit if the target cell doesn't match the target state
        if target_cell.state != target_state or not target_cell.is_passable():
            print("no targets found")
            return None

        # Initialize the distance map with infinity
        distance_map = [[float('inf')] * self.cols for _ in range(self.rows)]
        distance_map[target_row][target_col] = 0  # Target cell has distance 0

        # Initialize the queue for BFS with the target cell
        queue = [(target_row, target_col)]

        while queue:
            current_row, current_col = queue.pop(0)
            current_cell = self.grid[current_row][current_col]
            current_distance = distance_map[current_row][current_col]

            # Get neighbors of the current cell
            neighbors = current_cell.get_neighbors(self, radius=1)

            for layer in neighbors.values():
                for neighbor in layer:
                    neighbor_row, neighbor_col = neighbor.row, neighbor.col

                    # Skip if the neighbor:
                    # - Is already visited (has a valid distance)
                    # - Is impassable (e.g., obstacle, border)
                    if distance_map[neighbor_row][neighbor_col] != float('inf') or not neighbor.is_passable():
                        continue

                    # Update the distance to this neighbor
                    distance_map[neighbor_row][neighbor_col] = current_distance + current_cell.cell_size
                    # Add the neighbor to the queue for further exploration
                    queue.append((neighbor_row, neighbor_col))

        return distance_map

    # Display Methode: Momentan noch in Konsole, später mit Plots
    def display(self):
        """Print the current state of the grid"""
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))
        print()

    #Update funktion: Wir müssen nur die Agenten bewegen und die Spawns für den nächsten Zeitschritt durchführen
    def update(self, target_list, timestep):

        self.update_distance_maps()
        #Bewege Agenten
        for agent in self.agents:
            if agent.arrived == True:
                self.agents.remove(agent)
            #print(agent)
            if self.movement_method == "floodfill":
                agent.movement_towards_target(self)
            elif self.movement_method == "dijkstra":
                agent.movement_towards_target(self)  # Pass the grid instance

            agent.log_state(timestep)

        #Spawne Agenten (
        for row, col in self.spawn_cells:
            cell = self.grid[row][col]
            if isinstance(cell, SpawnCell):  # Check if the cell at (row, col) is a SpawnCell
                max_agents = 1  # Adjust the number of agents to spawn as needed
                cell.spawn_agents(self, max_agents)

        self.log_grid_state(timestep)

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

    def create_logfile(self):
        path = f"gridlog-{self.__hash__()}.txt"
        if(os.path.isfile(path)):
            return "File already exists"
        else:
            with open(path, "w") as fp:
                pass
            return "File created"

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

class Visualization:
    def __init__(self, grid):
        self.grid = grid
        self.fig, self.ax = plt.subplots()

    def plot_grid_state(self, timestep):
        data = [[cell.state for cell in row] for row in self.grid.grid]

        cmap = plt.cm.get_cmap('binary')

        self.ax.clear()
        self.ax.imshow(data, cmap=cmap)
        
        self.ax.set_xticks(range(self.grid.cols))
        self.ax.set_yticks(range(self.grid.rows))
        
        self.ax.set_title(f"Grid State at Timestep {timestep}")
        self.ax.set_xlabel("Columns")
        self.ax.set_ylabel("Rows")

    def animate_grid_states(self, timesteps):
        def update(frame):
            self.grid.update(target_list=self.grid.target_cells, timestep=frame)
            self.plot_grid_state(frame)

        ani = animation.FuncAnimation(self.fig, update, frames=timesteps, interval=100)
        plt.show()
 
