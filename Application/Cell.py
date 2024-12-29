
import random
import math
import numpy as np
from decorator import log_decorator


# one file per cell?
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

    def valid_neighbors(self, neighbors):
        valid_neighbors = [
            cell for layer in neighbors.values()
            for cell in layer
            if cell.is_passable()
        ]
        return valid_neighbors
    @log_decorator
    def euclidean_distance_to(self, other):
       #Euklidische Distanz zwischen Zwei Zellen
        return math.sqrt((self.row - other.row) ** 2  + (self.col - other.col) ** 2) *self.cell_size

    def manhattan_difference_to(self, other_cell):
        """Calculate the height and length difference between this cell and another cell."""
        height_diff = abs(self.row - other_cell.row)
        length_diff = abs(self.col - other_cell.col)
        return height_diff, length_diff


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
 # check naming
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
        valid_neighbors = self.valid_neighbors(self.get_neighbors(grid, radius=1))
        random.shuffle(valid_neighbors)
        chance = random.randrange(0,1)
        agents_to_spawn = min(max_agents, len(valid_neighbors))
        if chance < 0.8:
            for _ in range(agents_to_spawn):
                cell = valid_neighbors.pop(0)
                row, col = cell.row, cell.col
                agent = Agent(row, col, cell_size=self.cell_size)
                agent.group = random.choice([0, 1])  # NEUE ZEILE
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
        #self.velocity = random.uniform(0.5, 1.5)
        self.id = self.__hash__()
        self.route = []
        self.target = None
        self.group = None
        self._original_velocity = random.uniform(0.5, 1.5)
        self._original_movement_range = self.original_velocity
        self.velocity = self._original_velocity
        self.movement_range = self._original_movement_range
        self.idle = None

    def log_state(self, timestep, log_file="logs/agent_states.log"):
        """Log the agent's state to a file."""

        with open(log_file, "a") as logfile:
            logfile.write(
                f"Timestep: {timestep}, Agent ID: {self.id}, Position: (row: {self.row}, col: {self.col}), Route: {self.route}\n "
                f"State: {self.state}, Arrived: {self.arrived}, Velocity: {self.velocity}\n"
            )

    @property
    def original_velocity(self):
        """Access the original velocity."""
        return self._original_velocity

    @property
    def original_movement_range(self):
        """Access the original movement range."""
        return self._original_movement_range
    def restore_velocity(self):
        self.velocity = self._original_velocity
    def restore_movement_range(self):
        self.movement_range = self._original_movement_range


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
        

  #  @log_decorator
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
   # @log_decorator

    def repulsive_force(self, width, height):
        if width == 0:  # Ensure no division by zero for width
            width = 1e-6  # Substitute with a very small number
        repulsive_force = -height + math.exp(1 / (2/width)**2 -1)
        return  repulsive_force
   # @log_decorator
    def social_penalty(self, grid):
        """
        Calculate the social penalty based on agent proximity and movement preference.
        Returns a penalty score to discourage crowding.
        """
        total_penalty = 0
        cutoff_distance = 3.0  # Maximum distance in meters to consider for social penalty
        penalty_decay_factor = 0.5  # Control the steepness of the Gaussian decay
        stay_penalty = 0.5  # Additional penalty for remaining stationary

        # Get neighbors within a cutoff radius
        neighbors = self.get_neighbors(grid, radius=int(cutoff_distance / grid.cell_size))

        for distance, cells in neighbors.items():
            for cell in cells:
                if isinstance(cell, Agent) and not cell.arrived:  # Only consider other agents
                    # Compute Euclidean distance in meters
                    euclidean_distance = self.euclidean_distance_to(cell)

                    if euclidean_distance <= cutoff_distance:
                        # Apply Gaussian decay penalty
                        penalty_contribution = math.exp(-(euclidean_distance ** 2) / (2 * penalty_decay_factor ** 2))
                        total_penalty += penalty_contribution

        # Add penalty for staying in place
        total_penalty += stay_penalty

        return total_penalty


   # @log_decorator
    def adjust_movement_range(self):
        # Methode wird aufgerufen wenn Ziel nicht in einem Zeitschritt erreicht werden kann -->
        # print(self.idle)
        if self.idle:
            # print(f"Original Range{self._original_movement_range} and Original velocity{self._original_velocity}, adjusted velocity was {self.velocity} and movement was {self.movement_range}")
            self.movement_range += self.velocity

            print("MOVEMENT INCREASE")
            print(f"new range is{self.movement_range}")
        elif not self.idle:
            # We enter this part when the agent was able to move after being idle(for example stuck in crowd) --> We reset velocity and movement range to original states
            self.movement_range = self.original_movement_range
            print(f"MOVEMENT RESET: new range is {self.movement_range} and velocity is {self.velocity}")
            self.velocity = self.original_velocity

    def movement_decision(self, grid, precomputed_penalties, agent_index):
        """
        Decide the next move for the agent. Mark as arrived if reaching the target.
        Returns the new position (row, col) or None if no movement.
        """
        if self.arrived:
            return None

        if self.target is None:
            self.target = self.find_target(grid.target_cells)

        if not self.target:
            return None

        target_key = (self.target[0], self.target[1])
        distance_map = grid.dijkstra_distance_maps.get(target_key) or grid.flood_fill_distance_maps.get(target_key)

        if not distance_map:
            return None

        valid_neighbors = self.valid_neighbors(self.get_neighbors(grid, radius=1))
        valid_neighbors.append(self)  # Include staying in place as an option

        best_move = self
        smallest_cost = float('inf')

        for neighbor in valid_neighbors:
            distance_to_target = distance_map[neighbor.row][neighbor.col]
            social_penalty = precomputed_penalties[agent_index]
            staying_penalty = 5 if neighbor == self else 0

            # Reduce weight of social penalties near the target
            if isinstance(grid.grid[neighbor.row][neighbor.col], TargetCell):
                social_penalty *= 0.5  # Halve the effect of social penalties near the target
            random_bias = random.uniform(-0.5, 0.5)
            total_cost = distance_to_target + random_bias + social_penalty + staying_penalty

            if total_cost < smallest_cost:
                smallest_cost = total_cost
                best_move = neighbor
        # Set lowest possible velocity before reducing it any further to 0.40, graceful penalty only
        print(f"Agent{self.id} velocity before penalty is {self.velocity}. Social penalty is {social_penalty}")
        if self.velocity >= 0.40:
            if social_penalty is not None:
                self.velocity = self.velocity - (social_penalty / 2)
                if self.velocity <= 0:
                    # we dont want negative velocities
                    self.velocity = abs(self.velocity)
                self.movement_range = self.velocity

                print(f"new velocity for {agent_index} is {self.velocity}")

        # Mark as arrived if moving onto the target
        if isinstance(grid.grid[best_move.row][best_move.col], TargetCell):
            self.arrived = True
            return None

        return (best_move.row, best_move.col) if best_move != self else None
    #Bewegungslogik
    # sure this method does make sense here from a architectural point of view?
#    def movement_towards_target(self, grid):
#        """
#        Decide movement based on target proximity and social penalties.
#        """
#        if self.arrived:
#            return
#
#        # Determine the target and select the distance map
#        target = self.find_target(grid.target_cells)
#        if not target:
#            return
#
#        target_key = (target[0], target[1])
#        if grid.movement_method == "dijkstra":
#            distance_map = grid.dijkstra_distance_maps.get(target_key)
#        elif grid.movement_method == "floodfill":
#            distance_map = grid.flood_fill_distance_maps.get(target_key)
#
#        if not distance_map:
#            return  # Ensure the distance map is available
#
#        # Get valid neighbors
#        valid_neighbors = self.valid_neighbors(self.get_neighbors(grid, radius=1))
#        valid_neighbors.append(self)  # Include the current position as a fallback
#        social_penalties = {
#            (neighbor.row, neighbor.col): self.social_penalty(grid)
#            for neighbor in valid_neighbors
#        }
#
#        # Determine the best move
#        best_move = self
#        smallest_cost = float('inf')
#
#        for neighbor in valid_neighbors:
#            # Cache distance to target for efficiency
#            distance_to_target = distance_map[neighbor.row][neighbor.col]
#
#            # Fetch precomputed social penalty
#            penalty = social_penalties[(neighbor.row, neighbor.col)]
#
#            # Add penalty for staying in place
#            staying_penalty = 1.0 if neighbor == self else 0
#
#            total_cost = distance_to_target + penalty + staying_penalty
#
#            if total_cost < smallest_cost:
#                smallest_cost = total_cost
#                best_move = neighbor
#
#        # Check if the best move is onto the target
#        if (best_move.row, best_move.col) == target:
#            self.arrived = True
#            grid.agents.remove(self)
#            # Leave the target cell unchanged
#            grid.grid[self.row][self.col] = Cell(self.row, self.col, cell_size=self.cell_size)
#            return
#
#        # Move to the best neighbor
#        #print(f"agent id{self.id} has {self.euclidean_distance_to(best_move)} distance to best_move and {self.movement_range} movement_range")
#        if best_move != self and self.euclidean_distance_to(best_move)<=self.movement_range:
#            grid.grid[self.row][self.col] = Cell(self.row, self.col, cell_size=self.cell_size)
#            grid.grid[best_move.row][best_move.col] = self
#            self.row, self.col = best_move.row, best_move.col
#            self.idle = False
#            self.adjust_movement_range()
#        elif best_move != self and self.euclidean_distance_to(best_move)>self.movement_range:
#            self.idle = True
#            print(f"agent{self.id} is idle: {self.idle}")
#            self.adjust_movement_range()
#            print(f"increase of movement range to {self.movement_range}")
#        if smallest_cost == 0:  # If reached the target
#            self.arrived = True
#            grid.agents.remove(self)
#            grid.grid[self.row][self.col] = Cell(self.row, self.col, cell_size=self.cell_size)
    def movement_towards_target(self, grid, precomputed_penalties, index):
        if self.arrived:
            return

        target = self.find_target(grid.target_cells)
        # print(f"Agent {self.id} moving towards target {target}")

        valid_neighbors = self.valid_neighbors(self.get_neighbors(grid, radius=1))
        if not valid_neighbors:
            # print(f"Agent {self.id} has no valid neighbors and is stuck.")
            return

        best_move = self

        new_best_move = self.movement_decision(grid, precomputed_penalties, index)
        if new_best_move is None:
            print(f"Agent {self.id} at position {self.row, self.col} has no best move")
            return
        # print(new_best_move)
        # print(self.euclidean_distance_to(grid.grid[new_best_move[0]][new_best_move[1]]))
        if new_best_move != self and self.euclidean_distance_to(
                grid.grid[new_best_move[0]][new_best_move[1]]) <= self.movement_range:
            grid.grid[self.row][self.col] = Cell(self.row, self.col, cell_size=self.cell_size)
            grid.grid[new_best_move[0]][new_best_move[1]] = self
            self.row, self.col = new_best_move[0], new_best_move[1]
            # print(f"Agent {self.id} moved to ({self.row}, {self.col})")
            self.idle = False
            self.adjust_movement_range()

        elif new_best_move != self:
            self.idle = True
            print(
                f"Agent{self.id}: Range {self.movement_range} to short, adjusting. Distance is{self.euclidean_distance_to(grid.grid[new_best_move[0]][new_best_move[1]])}")
            self.adjust_movement_range()









    def __repr__(self):
        return 'A'  # Represent agent with 'A'
