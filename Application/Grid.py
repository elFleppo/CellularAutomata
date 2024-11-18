
from Cell import Cell, BorderCell, SpawnCell, Agent, TargetCell, ObstacleCell

import random
import os
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

    # Display Methode: Momentan noch in Konsole, später mit Plots
    def display(self):
        """Print the current state of the grid"""
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))
        print()

    #Update funktion: Wir müssen nur die Agenten bewegen und die Spawns für den nächsten Zeitschritt durchführen
    def update(self, target_list):

        #Bewege Agenten
        for agent in self.agents:
            #print(agent)
            agent.move_toward_highest_potential(self, target_list=target_list)  # Pass the grid instance


        #Spawne Agenten (
        for row, col in self.spawn_cells:
            cell = self.grid[row][col]
            if isinstance(cell, SpawnCell):  # Check if the cell at (row, col) is a SpawnCell
                max_agents = 1  # Adjust the number of agents to spawn as needed
                cell.spawn_agents(self, max_agents)

    def create_logfile(self):
        path = f"gridlog-{self.__hash__()}.txt"
        if(os.path.isfile(path)):
            return "File already exists"
        else:
            with open(path, "w") as fp:
                pass
            return "File created"

