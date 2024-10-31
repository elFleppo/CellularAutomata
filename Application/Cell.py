import random
import math
class Cell:
    #Standard Cell is just empty and can be visited
    def __init__(self, state=0):
        self.state = state  # 0 for dead/inactive, 1 for alive/active

    def is_passable(self):
        return True  # Most cells are passable by default

    def __repr__(self):
        return " "


# Define BorderCell class, which limits movement on the grid edges
class BorderCell(Cell):
    def __init__(self):
        super().__init__(state=1)  # Border cells are always active

    def is_passable(self):
        return False  # Border cells are impassable

    def __repr__(self):
        return 'B'

class ObstacleCell(Cell):
    def __init__(self):
        super().__init__(state=4)

    def is_passable(self):
        return False #Obstacles are impassable
    def __repr__(self):
        return '%'
# Define SpawnCell class, which spawns agents
class SpawnCell(Cell):
    def __init__(self):
        super().__init__(state=2)  # Spawn cells are active

    def spawn_agents(self, grid, max_agents):
        """Spawn agents at the spawn cell location."""
        empty_cells = [(r, c) for r in range(grid.rows) for c in range(grid.cols) if isinstance(grid.grid[r][c], Cell)]
        random.shuffle(empty_cells)
        agents_to_spawn = min(max_agents, len(empty_cells))

        for _ in range(agents_to_spawn):
            row, col = empty_cells.pop(0)
            grid.grid[row][col] = Agent()

    def __repr__(self):
        return 'S'  # Represent spawn cells with 'S'
class TargetCell(Cell):
    def __init__(self):
        super().__init__(state=3)  # Target cells are active

    def is_passable(self):
        return True  # Targets are passable to agents

    def __repr__(self):
        return 'T'  # Represent target cells with 'T'
class Agent(Cell):
    def __init__(self, row, col):
        super().__init__(state=47)  # Set the agent state as before
        self.row = row  # Store the agent's row position
        self.col = col  # Store the agent's column position

    def find_nearest_target(self, grid):
        """Find the nearest TargetCell on the grid to this agent's current position."""
        min_distance = float('inf')
        nearest_target = None

        for target_row in range(grid.rows):
            for target_col in range(grid.cols):
                cell = grid.grid[target_row][target_col]
                if isinstance(cell, TargetCell):
                    # Calculate Euclidean distance using self.row and self.col
                    distance = math.sqrt((target_row - self.row) ** 2 + (target_col - self.col) ** 2)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_target = (target_row, target_col)

        return nearest_target  # Returns (target_row, target_col) or None if no TargetCell is found

    def move(self, grid, new_row, new_col):
        """Move the agent to a new position if it's passable, updating its coordinates."""
        if grid.grid[new_row][new_col].is_passable():
            grid.grid[self.row][self.col] = Cell()  # Clear current position
            grid.grid[new_row][new_col] = self  # Move agent to new position
            self.row, self.col = new_row, new_col  # Update agent's stored position

    def is_passable(self):
        return False  # Agents are impassable (to other agents, for instance)

    def line_of_sight(self, grid):
        target = self.find_nearest_target(grid)
        """Check if there's a clear line of sight (LoS) between the agent and another cell."""
        line_cells = self.bresenham_line(self.row, self.col, target[0], target[1])

        for row, col in line_cells:
            # If any cell in the line is impassable, return False
            if not grid.grid[row][col].is_passable():
                return False
        return True

    def bresenham_line(self, x1, y1, x2, y2):
        """Bresenham's Line Algorithm to calculate all cells between two points."""
        cells = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            cells.append((x1, y1))  # Append the current cell
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return cells
        
    def move(self, grid, row, col):
        """Move the agent to a neighboring cell if it's passable."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
        random.shuffle(directions)  # Randomize movement

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            # Check if the new position is within the grid and passable
            if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols:
                if grid.grid[new_row][new_col].is_passable():
                    # Move the agent
                    grid.grid[new_row][new_col] = Agent()
                    grid.grid[row][col] = Cell()  # Empty the old position
                    break

    def potential(self, grid):
        """Calculate potential based on the negative Euclidean distance to the target cell."""
        target = self.find_nearest_target(grid)

        # Euclidean distance calculation ( Check if row and col are right)
        distance = math.sqrt((target[0] - self.row) ** 2 + (target[1] - self.col) ** 2)

        # Return the negative distance as potential
        return -distance

    def __repr__(self):
        return 'A'  # Represent agent with 'A'