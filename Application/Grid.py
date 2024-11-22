
from Cell import Cell, BorderCell, SpawnCell, Agent, TargetCell, ObstacleCell

import random
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
#Grid Klasse: Auf dem Grid befinden sich Zellobjekte und über das Grid wird das update() der Zellen durchgeführt
class Grid:
    #Im Init wird das grid entsprechend aufgebaut, es können Listen mit Tuplen für die entsprechenden Zell Objekte mitgegeben werden
    def __init__(self, rows, cols, spawn_cells, target_cells, obstacle_cells):
        self.rows = rows
        self.cols = cols
        self.grid = [
            [Cell(row, col) for col in range(cols)] for row in range(rows)
        ]  # Aufbau Grid
        self.spawn_cells = spawn_cells  # Listen für Spawns, Ziele und Hindernisse
        self.target_cells = target_cells
        self.obstacle_cells = obstacle_cells
        self.agents = []  # Liste mit allen Agenten die sich auf dem Feld befinden

        # Aufbau von Spawn, Zielen und Hindernissen
        for row, col in spawn_cells:
            print(row, col)
            self.grid[row][col] = SpawnCell(row=row, col=col)
        for row, col in obstacle_cells:
            self.grid[row][col] = ObstacleCell(row=row, col=col)
        for row, col in target_cells:
            self.grid[row][col] = TargetCell(row=row, col=col)

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
                    self.grid[r][c] = BorderCell()
    #Die Untenstehenden methoden erlauben eine Interaktion mit dem Grid ausserhalb der initialisierung
    def place_spawn_cell(self, row, col):
        """Place a spawn cell at a specific position on the grid"""
        self.grid[row][col] = SpawnCell(row=row, col=col)
        self.spawn_cells.append((row, col))

    def place_target(self, row, col):
        """Place a target cell at a specific position on the grid"""
        self.grid[row][col] = TargetCell(row=row, col=col)
        self.target_cells.append((row, col))

    def place_agent(self, row, col):
        """Place an agent at a specific position on the grid"""
        agent = Agent(row, col)
        self.grid[row][col] = agent
        self.agents.append(agent)

    def place_obstacle(self, row, col):
        self.grid[row][col] = ObstacleCell(row=row, col=col)

    def is_cell_occupied(self, row, col):
        cell = self.grid[row][col]
        return isinstance(cell, Agent)

    # Display Methode: Momentan noch in Konsole, später mit Plots
    def display(self):
        """Print the current state of the grid"""
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))
        print()

    #Update funktion: Wir müssen nur die Agenten bewegen und die Spawns für den nächsten Zeitschritt durchführen
    def update(self, target_list, timestep):

        #Bewege Agenten
        for agent in self.agents:
            #print(agent)
            agent.move_toward_highest_potential(self, target_list=target_list)  # Pass the grid instance
            agent.log_state(timestep)

        #Spawne Agenten (
        for row, col in self.spawn_cells:
            cell = self.grid[row][col]
            if isinstance(cell, SpawnCell):  # Check if the cell at (row, col) is a SpawnCell
                max_agents = 1  # Adjust the number of agents to spawn as needed
                cell.spawn_agents(self, max_agents)
        self.log_grid_state(timestep)

    def create_logfile(self):
        path = f"gridlog-{self.__hash__()}.txt"
        if(os.path.isfile(path)):
            return "File already exists"
        else:
            with open(path, "w") as fp:
                pass
            return "File created"

    def plot_grid_state(grid, timestep):
        """
        Plots the current state of the grid at a given timestep using Plotly.
        Each cell is represented by its `state` value.
        """
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

