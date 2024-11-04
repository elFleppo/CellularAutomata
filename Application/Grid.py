
from Cell import Cell, BorderCell, SpawnCell, Agent, TargetCell, ObstacleCell

import random
class Grid:
    def __init__(self, rows, cols, spawn_cells, target_cells, obstacle_cells):
        self.rows = rows
        self.cols = cols
        self.grid = [
            [Cell(row, col) for col in range(cols)] for row in range(rows)
        ]  # Initialize with coordinates
        self.spawn_cells = spawn_cells  # List to keep track of spawn cells
        self.target_cells = target_cells
        self.obstacle_cells = obstacle_cells
        self.agents = []  # List to keep track of all agents on the grid

        # Place spawn, target, and obstacle cells
        for row, col in spawn_cells:
            print(row, col)
            self.grid[row][col] = SpawnCell(row=row, col=col)
        for row, col in obstacle_cells:
            self.grid[row][col] = ObstacleCell(row=row, col=col)
        for row, col in target_cells:
            self.grid[row][col] = TargetCell(row=row, col=col)

    def place_border(self):
        """Place a border around the grid"""
        for r in range(self.rows):
            for c in range(self.cols):
                if r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1:
                    self.grid[r][c] = BorderCell()

    def place_spawn_cell(self, row, col):
        """Place a spawn cell at a specific position on the grid"""
        self.grid[row][col] = SpawnCell()
        self.spawn_cells.append((row, col))

    def place_target(self, row, col):
        """Place a target cell at a specific position on the grid"""
        self.grid[row][col] = TargetCell()
        self.target_cells.append((row, col))

    def place_agent(self, row, col):
        """Place an agent at a specific position on the grid"""
        agent = Agent(row, col)
        self.grid[row][col] = agent
        self.agents.append(agent)

    def place_obstacle(self, row, col):
        self.grid[row][col] = ObstacleCell()

    def display(self):
        """Print the current state of the grid"""
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))
        print()

    def update(self, target_list):
        """Update the grid: move agents, spawn new agents"""
        for agent in self.agents:
            print(agent)
            agent.move_toward_highest_potential(self, target_list=target_list)  # Pass the grid instance

            # Spawn agents from spawn cells
        for row, col in self.spawn_cells:
            print(row, col)
            max_agents = 1  # One agent per spawn cell for simplicity
            if isinstance(self, SpawnCell):
                self.grid[row][col].spawn_agents(self, max_agents)


