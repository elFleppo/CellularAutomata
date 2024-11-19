import random
import math
class Cell:
    #Grundbaustein, jede Zelle kennt seine Position auf dem Grid und den entsprechenden state
    def __init__(self, row, col, state=0):
        self.row = row  # Store the row position
        self.col = col  # Store the column position
        self.state = state  # 0 for dead/inactive, 1 for alive/active

    #Methode welche die naheliegendste Target Zelle anhand einer target list (Tuples aus Koordinaten) sucht
    def find_target(self, target_list):
        min_distance = float('inf')
        nearest_target = None
        #print(target_list)
        #print(self.row)
        for row, col in target_list:
            #print(row, col)
            #print(f"{row}-{self.row} ** 2 + ({col} - {self.col}) ** 2")
            distance = math.sqrt((row - self.row) ** 2 + (col - self.col) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_target = (row, col)
        return nearest_target

    def get_neighbors(self, grid, radius=2):
        """
        Get neighbors in an extended Moore neighborhood up to the specified radius.
        Returns a dictionary where keys are the distance layers (1, 2, ..., radius),
        and values are lists of cells at that distance.
        """
        neighbors = {}  # Store neighbors grouped by distance

        for r in range(1, radius + 1):  # Iterate through each "ring" (distance layer)
            layer_neighbors = []
            for dr in range(-r, r + 1):  # Rows in the ring
                for dc in range(-r, r + 1):  # Columns in the ring
                    # Include only the current ring (distance exactly `r` in any direction)
                    if abs(dr) == r or abs(dc) == r:
                        # Compute the neighbor's coordinates
                        neighbor_row, neighbor_col = self.row + dr, self.col + dc
                        # Check grid bounds and passability
                        if 0 <= neighbor_row < grid.rows and 0 <= neighbor_col < grid.cols:
                            neighbor_cell = grid.grid[neighbor_row][neighbor_col]
                            if neighbor_cell.is_passable():
                                layer_neighbors.append(neighbor_cell)

            neighbors[r] = layer_neighbors  # Group neighbors by distance

        return neighbors



    #Jedes Feld hat einen Potentialwert zu der naheliegendsten Target Zelle
    def potential(self, grid, target_list):
        """Calculate potential based on the negative Euclidean distance to the target cell."""
        target = self.find_target(target_list)
        #print(f"TARGET:{target[0]},{target[1]}")
        #print(f"SELF: {self.row}, {self.col}")

        # Euclidean distance calculation ( Check if row and col are right)
        distance = math.sqrt((target[0] - self.row) ** 2 + (target[1] - self.col) ** 2)

        # Return the negative distance as potential
        return -distance
    #is_passable (Kann ich von einem Agenten besucht werden). Evtl als Variable statt Methode?
    def is_passable(self):
        return True  # Most cells are passable by default
    #Momentane Visualisierung noch in Konsole mit string repr. Für später dann Plots mit Daten aller Timesteps
    def __repr__(self):
        return "0"


# Randzellen die das Feld umschliessen (etwa im Fall eines Raums mit Türen kann ein Border plaziert und danach Targets als Türen auf dem Border definiert werden)
class BorderCell(Cell):
    def __init__(self,row, col):
        super().__init__(state=1, row=row, col=col)  # Border cells are always active


    def is_passable(self):
        return False  # Border cells are impassable

    def __repr__(self):
        return 'B'

#Hindernisse auf dem Feld
class ObstacleCell(Cell):
    def __init__(self, row, col):
        super().__init__(state=4, row=row, col=col)
    def is_passable(self):
        return False #Obstacles are impassable
    def __repr__(self):
        return '%'
# Spawn Zelle. Generiert pro Zeitschritt eine vordefinierte Anzahl agenten auf seinen Moore Nachbar Zellen
class SpawnCell(Cell):
    def __init__(self, row, col):
        super().__init__(state=2, row=row, col=col)  # Spawn cells are active
    #Spawn eine definierte Anzahl Agenten auf deinen Moore Nachbarn und füge die neuen Agenten der grid.agents liste Hinzu
    def spawn_agents(self, grid, max_agents):
        neighbors  = self.get_neighbors(grid, radius=1)
        valid_neighbors = [cell for layer in neighbors.values() for cell in layer]
        """Spawn agents at the spawn cell location and add them to grid's agent list."""

        random.shuffle(valid_neighbors)
        agents_to_spawn = min(max_agents, len(valid_neighbors))

        for _ in range(agents_to_spawn):
            #print("CREATING AGENT")
            cell = valid_neighbors.pop(0)  # Pick a random valid neighbor
            row, col = cell.row, cell.col
            agent = Agent(row, col)  # Create a new agent
            grid.grid[row][col] = agent  # Place agent on the grid
            grid.agents.append(agent)

    def is_passable(self):
        return False  #Agenten können nicht Spawnzellen laufen

    def __repr__(self):
        return 'S'  # Represent spawn cells with 'S'

#Ziele: Agenten bewegen sich auf die Ziele
class TargetCell(Cell):
    def __init__(self, row, col):
        super().__init__(state=3, row=row, col=col)  # Target cells are active

    def is_passable(self):
        return True  # Targets are passable to agents

    def __repr__(self):
        return 'T'  # Represent target cells with 'T'
class Agent(Cell):
    def __init__(self, row, col):
        super().__init__(state=47, row=row, col=col) # Set the agent state as before
        self.arrived = False
        #velocity wird später verwendet um die Gehgeschwindigkeit der einzelnen Agenten zu verändern
        self.velocity = random.uniform(0.75, 1.5)
        self.id = self.__hash__()
 #Momentan nicht in Verwendung da wir Ziele als Liste führen und nicht immer als Grid Search finden müssen
 #   def find_nearest_target(self, grid):
 #       """Find the nearest TargetCell on the grid to this agent's current position."""
 #       min_distance = float('inf')
 #       nearest_target = None
 #
 #       for target_row in range(grid.rows):
 #           for target_col in range(grid.cols):
 #               cell = grid.grid[target_row][target_col]
 #               if isinstance(cell, TargetCell):
 #                   # Calculate Euclidean distance using self.row and self.col
 #                   distance = math.sqrt((target_row - self.row) ** 2 + (target_col - self.col) ** 2)
 #                   if distance < min_distance:
 #                       min_distance = distance
 #                       nearest_target = (target_row, target_col)
 #
 #       return nearest_target  # Returns (target_row, target_col) or None if no TargetCell is found
    def log_state(self, timestep, log_file="agent_states.log"):
        """Log the agent's state to a file."""
        with open(log_file, "a") as logfile:
            logfile.write(
                f"Timestep: {timestep}, Agent ID: {self.id}, Position: ({self.row}, {self.col}), "
                f"State: {self.state}, Arrived: {self.arrived}, Velocity: {self.velocity}\n"
            )

    def is_passable(self):
        return False  # Agents are impassable (to other agents, for instance)

    #Momentan noch nicht in Verwendung aber wird für die Sichtlinie zum Ziel verwendet
    def line_of_sight(self, grid):
        target = self.find_nearest_target(grid)
        """Check if there's a clear line of sight (LoS) between the agent and another cell."""
        line_cells = self.bresenham_line(self.row, self.col, target[0], target[1])

        for row, col in line_cells:
            # If any cell in the line is impassable, return False
            if not grid.grid[row][col].is_passable():
                return False
        return True
    #bresenham_line fürht eine Liste aller Zellen die auf der line_of_sight zum Ziel sind (um Sichtkontakt zum Ziel zu prüfen)
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
        


    def velocity_check(self):
        pass

    #Bewegungslogik
    def move_toward_highest_potential(self, grid, target_list):
        # Der Agent bewegt sich zu der Zelle mit dem besten Potenzial

        neighbors = self.get_neighbors(grid, radius=1)
        valid_neighbors = [cell for layer in neighbors.values() for cell in layer]
        # Wenn der Agent angekommen ist (also mit der nächsten Bewegung im Ziel "verschwindet") entfernen wir ihn
        if self.arrived:
            grid.grid[self.row][self.col] = Cell(self.row, self.col)  # Clear current position
            print(self.__hash__())  #Zum überprüfen der Funktionalität
            if self in grid.agents:
                grid.agents.remove(self)
            return

        # Determine the neighbor with the highest potential
        curr_potential = self.potential(grid, target_list)
        best_move = (self.row, self.col)  # Default to staying in place

        #Wenn ich mich neben dem Ziel (potential -1 oder -1.41 (diagonal momentan noch gleichbehandelt)) befinde, bin ich angekommen und werden in t+1 gelöscht
        if curr_potential == -1 or curr_potential == -1.4142135623730951:
            print("arrived at Target")
            self.arrived = True
        #Vergleiche Potential von Nachbarzellen mit eigener Zelle
        for neighbor_cell in valid_neighbors:
            potential = neighbor_cell.potential(grid, target_list)
            if potential > curr_potential:
                curr_potential = potential
                best_move = (neighbor_cell.row, neighbor_cell.col)

        if best_move != (self.row, self.col):
            grid.grid[self.row][self.col] = Cell(self.row, self.col)  # Clear current position
            grid.grid[best_move[0]][best_move[1]] = self  # Move agent to new position
            self.row, self.col = best_move  # Update agent's position


    def __repr__(self):
        return 'A'  # Represent agent with 'A'