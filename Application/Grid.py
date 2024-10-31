
from Cell import Cell, BorderCell, SpawnCell, Agent, TargetCell, ObstacleCell

import random
class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.spawn_cells = []  # List to keep track of spawn cells

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

    def place_agent(self, row, col):
        """Place an agent at a specific position on the grid"""
        agent = Agent(row, col)
        self.grid[row][col] = agent

    def place_obstacle(self, row, col):
        self.grid[row][col] = ObstacleCell()

    def display(self):
        """Print the current state of the grid"""
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))
        print()

    def update(self):
        """Update the grid: move agents, spawn new agents"""
        # Move existing agents
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if isinstance(cell, Agent):
                    cell.move(self, row, col)

        # Spawn agents from spawn cells
        for row, col in self.spawn_cells:
            max_agents = 1  # One agent per spawn cell for simplicity
            self.grid[row][col].spawn_agents(self, max_agents)


