import random
import math
from decorator import log_decorator
class Cell:
    #Grundbaustein, jede Zelle kennt seine Position auf dem Grid und den entsprechenden state
    def __init__(self, row, col,cell_size, state=0):
        self.row = row  # Store the row position
        self.col = col  # Store the column position
        self.state = state  # 0 for dead/inactive, 1 for alive/active
        self.cell_size = cell_size

    #Methode welche die naheliegendste Target Zelle anhand einer target list (Tuples aus Koordinaten) sucht
    @log_decorator
    def find_target(self, target_list):
        min_distance = float('inf')
        nearest_target = None
        #print(target_list)
        #print(self.row)
        for row, col in target_list:
            #print(row, col)
            #print(f"{row}-{self.row} ** 2 + ({col} - {self.col}) ** 2")
            distance = math.sqrt((row - self.row) ** 2 + (col - self.col) ** 2)*self.cell_size
            if distance < min_distance:
                min_distance = distance
                nearest_target = (row, col)
        return nearest_target
    @log_decorator
    def get_neighbors(self, grid, radius=2):
        """
        Get neighbors in an extended Moore neighborhood up to the specified radius.
        Returns a dictionary where keys are the distance layers (1, 2, ..., radius),
        and values are lists of cells at that distance.
        """
        if grid is None:  # Ensure the grid is not None
            return {}

        neighbors = {}  # Store neighbors grouped by distance

        for r in range(1, radius + 1):  # Iterate through each "ring" (distance layer)
            layer_neighbors = []  # Neighbors in the current ring
            for dr in range(-r, r + 1):  # Rows within the distance
                for dc in range(-r, r + 1):  # Columns within the distance
                    # Include only cells at the exact distance 'r' (Manhattan distance, creating rings)
                    if abs(dr) == r or abs(dc) == r:
                        neighbor_row, neighbor_col = self.row + dr, self.col + dc
                        # Ensure neighbors are within grid bounds
                        if 0 <= neighbor_row < grid.rows and 0 <= neighbor_col < grid.cols:
                            neighbor_cell = grid.grid[neighbor_row][neighbor_col]
                            if neighbor_cell:  # Check if the cell exists
                                layer_neighbors.append(neighbor_cell)

            neighbors[r] = layer_neighbors  # Store the current layer of neighbors

        return neighbors
    @log_decorator
    def euclidean_distance_to(self, other):
       #Euklidische Distanz zwischen Zwei Zellen
        return math.sqrt((self.row - other.row) ** 2 + (self.col - other.col) ** 2)*self.cell_size


    #Jedes Feld hat einen Potentialwert zu der naheliegendsten Target Zelle
    @log_decorator
    def potential(self, grid, target_list):
        """Calculate potential based on the negative Euclidean distance to the target cell."""
        target = self.find_target(target_list)
        #print(f"TARGET:{target[0]},{target[1]}")
        #print(f"SELF: {self.row}, {self.col}")

        # Euclidean distance calculation ( Check if row and col are right)
        distance = self.euclidean_distance_to(target)

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
    def __init__(self,row, col, cell_size):
        super().__init__(state=1, row=row, col=col, cell_size=cell_size)  # Border cells are always active


    def is_passable(self):
        return False  # Border cells are impassable

    def __repr__(self):
        return 'B'

#Hindernisse auf dem Feld
class ObstacleCell(Cell):
    def __init__(self, row, col, cell_size):
        super().__init__(state=4, row=row, col=col, cell_size=cell_size)
    def is_passable(self):
        return False #Obstacles are impassable
    def __repr__(self):
        return '%'
# Spawn Zelle. Generiert pro Zeitschritt eine vordefinierte Anzahl agenten auf seinen Moore Nachbar Zellen
class SpawnCell(Cell):
    def __init__(self, row, col, cell_size):
        super().__init__(state=2, row=row, col=col, cell_size=cell_size)  # Spawn cells are active
    #Spawn eine definierte Anzahl Agenten auf deinen Moore Nachbarn und füge die neuen Agenten der grid.agents liste Hinzu

    def spawn_agents(self, grid, max_agents):
        neighbors = self.get_neighbors(grid, radius=1)
        valid_neighbors = [
            cell for layer in neighbors.values()
            for cell in layer
            if not grid.is_cell_occupied(cell.row, cell.col)
        ]

        random.shuffle(valid_neighbors)

        agents_to_spawn = min(max_agents, len(valid_neighbors))
        for _ in range(agents_to_spawn):
            cell = valid_neighbors.pop(0)
            row, col = cell.row, cell.col
            agent = Agent(row, col, cell_size=self.cell_size)
            grid.grid[row][col] = agent
            grid.agents.append(agent)

    def is_passable(self):
        return False  #Agenten können nicht Spawnzellen laufen

    def __repr__(self):
        return 'S'  # Represent spawn cells with 'S'

#Ziele: Agenten bewegen sich auf die Ziele
class TargetCell(Cell):
    def __init__(self, row, col, cell_size):
        super().__init__(state=3, row=row, col=col, cell_size=cell_size)  # Target cells are active

    def is_passable(self):
        return True  # Targets are passable to agents

    def __repr__(self):
        return 'T'  # Represent target cells with 'T'
class Agent(Cell):
    def __init__(self, row, col, cell_size):
        super().__init__(state=47, row=row, col=col, cell_size=cell_size) # Set the agent state as before
        self.arrived = False
        #velocity wird später verwendet um die Gehgeschwindigkeit der einzelnen Agenten zu verändern
        self.velocity = random.uniform(0.75, 1.5)
        self.id = self.__hash__()
        self.route = []
        self.movement_range = self.velocity
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
    def log_state(self, timestep, log_file="logs/agent_states.log"):
        """Log the agent's state to a file."""

        with open(log_file, "a") as logfile:
            logfile.write(
                f"Timestep: {timestep}, Agent ID: {self.id}, Position: (row: {self.row}, col: {self.col}), Route: {self.route}\n "
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
            # Check if the cell at (row, col) is an obstacle
            cell = grid.grid[row][col]
            if isinstance(cell, ObstacleCell):
                return False  # Line of sight is blocked by an obstacle

        return True  # Line of sight is clear

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
        

    @log_decorator
    def social_force(self, grid):
        print("entering social force")
        neighbors = self.get_neighbors(grid, radius=2)  # Get neighbors within the radius
        total_neighbors = sum(len(cells) for cells in neighbors.values())
        penalty = 0  # Initialize the penalty accumulator
        penalty_factor = 0.6
        agent_cells = []  # List to store agent cells
        for distance, cells in neighbors.items():  # neighbors are grouped by distance layers
            for cell in cells:
                if isinstance(cell, Agent):  # Check if the cell contains an agent
                    agent_cells.append(cell)

            # Calculate the percentage of agents among all neighbors


        #Sollten wir wo anders abfangen, bei get_neighbors --> darf nicht 0 returnen
        if total_neighbors == 0:  # Avoid division by zero
            return 0  # No penalty if no neighbors
        agent_percentage = len(agent_cells) / total_neighbors

        # Apply penalty only if at least 40% of neighbors are agents
       # if agent_percentage < 0.2:
       #    return 0  # No penalty applied if less than 40% are agents

        # Calculate penalty
        penalty = 0  # Initialize the penalty accumulator
        for agent in agent_cells:
            euclidean_distance = self.euclidean_distance_to(agent)  # Calculate distance

            if euclidean_distance > 0:  # Avoid division by zero for self
                penalty_contribution = 1 / euclidean_distance  # Inverse distance penalty
                penalty += penalty_contribution
        print(f"Social force penalty for {self.__hash__()} is {penalty}")
        return penalty


    @log_decorator
    def increase_movement_range(self):
        #Methode wird aufgerufen wenn Ziel nicht in einem Zeitschritt erreicht werden kann -->
        self.movement_range = self.velocity + self.movement_range
        return self.movement_range


    #Bewegungslogik
    def move_toward_highest_potential(self, grid, target_list):
       #Denke den brauchen wir gar nicht da nach self.arrived = True das Grid den Agenten löscht
        if self.arrived:
            return

        # Ziel auswählen --> Ziel auswahl muss pro Zelle stattfinden. Aber die Distance map könnten wir wahrscheinlich wo anders setzen um Rechenzeit zu sparen / Redundanz zu verhindern
        target = self.find_target(target_list)
        if not target:
            return  # No target available

        # Compute distance map from the target
        distance_map = grid.compute_distance_map(target)

        # Moore nachbarn die nicht besetzt oder Hindernis sind.
        neighbors = self.get_neighbors(grid, radius=1)
        valid_neighbors = [
            cell for layer in neighbors.values()
            for cell in layer
            if not isinstance(cell, ObstacleCell) and not grid.is_cell_occupied(cell.row, cell.col)
        ]

        # Include the agent's current position as an option
        valid_neighbors.append(self)

        # Suche besten Nachbar aus basierend auf Distance map
        best_move = self
        smallest_distance = distance_map[self.row][self.col]

        for neighbor in valid_neighbors:
            distance = distance_map[neighbor.row][neighbor.col]
            if distance < smallest_distance:
                smallest_distance = distance
                best_move = neighbor

        # Bewegung
        if best_move != self:
            grid.grid[self.row][self.col] = Cell(self.row, self.col, cell_size=self.cell_size)  # Clear current position
            grid.grid[best_move.row][best_move.col] = self  # Move agent
            self.row, self.col = best_move.row, best_move.col

        # Agent ist angekommen und wird entsprechend entfernt
        if smallest_distance == 1:
            self.arrived = True
            grid.agents.remove(self)  # Remove the agent from active list
            grid.grid[self.row][self.col] = Cell(self.row, self.col, cell_size=self.cell_size)
            print(f"Agent at ({self.row}, {self.col}) is adjacent to the target and has arrived.")




    def __repr__(self):
        return 'A'  # Represent agent with 'A'