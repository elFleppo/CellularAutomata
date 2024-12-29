import unittest, math
from Grid import Grid
from Cell import Cell, SpawnCell, TargetCell, Agent, ObstacleCell
from concurrent.futures import ThreadPoolExecutor
import numpy as np
#Werden wir später noch in einen dedizierten Testordner verschieben
class TestAgentBehavior(unittest.TestCase):

    def setUp(self):

        # Einfaches 5x5 Grid
        self.grid = Grid(
            length=5,
            height=5,
            cell_size=1,
            spawn_cells=[(1, 1)],
            target_cells=[(3, 3)],
            movement_method="dijkstra",
            obstacle_cells=[]#Momentan noch keine Kolisionsvermeidung
        )
        self.grid.update_distance_maps()
    def test_spawn_agents_restrict_to_neighbors(self):
        spawn_cell = self.grid.grid[1][1]  # Define a spawn cell
        self.assertIsInstance(spawn_cell, SpawnCell, "Expected a SpawnCell at (1, 1)")


        # Spawn agents in the first timestep
        for timestep in range(5):
            self.grid.update(self.grid.target_cells, timestep)

   # one unit test tests only -> each class should test its method, and not via grid.update testing spawn agents. Please check again anc create real unit tests.

    def test_spawn_agents(self):

        #Zu Beginn noch keine Agenten in der Liste
        self.assertEqual(len(self.grid.agents), 0)

        # Update erzeugt neue Agenten
        #self.grid.update(self.grid.target_cells, timestep=1)


        # Verify all agents are in valid spawn neighbor cells
        spawn_neighbors = [
                (0, 0), (0, 1), (0, 2),
                (1, 0), (1, 2),
                (2, 0), (2, 1), (2, 2),
            ]
        agent_positions = [(agent.row, agent.col) for agent in self.grid.agents]

        for pos in agent_positions:
            self.assertIn(pos, spawn_neighbors, "Agent spawned or moved outside valid neighbors.")

    def test_agent_removal_on_arrival(self):
        # Plaziere Agent bei Ziel
        agent = Agent(2, 2, cell_size=self.grid.cell_size)
        self.grid.grid[2][2] = agent
        self.grid.agents.append(agent)

        # Update bewirkt das er sich Ziel Nähert
        for timestep in range(10):
            self.grid.update(self.grid.target_cells, timestep=timestep)
            #self.grid.plot_distance_map(self.grid.dijkstra_distance_maps([(3,3)]))
            self.grid.plot_grid_state(timestep)

        # Verifiziere Löschung
        self.assertNotIn(agent, self.grid.agents, "Agent was not removed after arrival.")
        self.assertNotIsInstance(self.grid.grid[3][3], Agent, "Agent is still present at the target cell.")

    def test_no_multiple_agents_per_cell(self):
        # Run updates for multiple timesteps
        for timestep in range(10):
            self.grid.update(self.grid.target_cells, timestep)

        # Collect all agent positions
        agent_positions = [(agent.row, agent.col) for agent in self.grid.agents]

        # Ensure no duplicates (i.e., no two agents occupy the same cell)
        unique_positions = set(agent_positions)
        self.assertEqual(len(agent_positions), len(unique_positions), "Multiple agents occupy the same cell.")


class TestGrid(unittest.TestCase):
    def setUp(self):

        # Einfaches 5x5 Grid
        self.grid = Grid(
            length=12,
            height=12,
            cell_size=1,
            spawn_cells=[(1, 1)],
            target_cells=[(3, 3)],
            obstacle_cells=[]#Momentan noch keine Kolisionsvermeidung
        )

    def test_select_area_by_coordinates(self):
        grid = Grid(
            length=10,
            height=10,
            spawn_cells=[],
            target_cells=[],
            obstacle_cells=[],
            cell_size=1.0
        )

        # Select an area using real-world coordinates
        selected_cells = grid.select_area_by_coordinates(2.0, 2.0, 4.0, 4.0)

        # Verify the correct number of cells are selected (3x3 area = 9 cells)
        self.assertEqual(len(selected_cells), 9, "Expected 9 cells in the selected area.")

        # Verify all cells are within the correct range
        for cell in selected_cells:
            self.assertTrue(
                2 <= cell.row <= 4 and 2 <= cell.col <= 4,
                f"Cell at ({cell.row}, {cell.col}) is outside the selected area."
            )


class TestCellNeighbors(unittest.TestCase):
    def setUp(self):

        # Einfaches 5x5 Grid
        self.grid = Grid(
            length=5,
            height=5,
            cell_size=1,
            spawn_cells=[(1, 1)],
            target_cells=[(3, 3)],
            obstacle_cells=[]#Momentan noch keine Kolisionsvermeidung
        )
        # Place a Cell in the middle for normal case and edges for edge cases
        self.central_cell = self.grid.grid[2][2]  # Center of the grid
        self.corner_cell = self.grid.grid[0][0]  # Top-left corner
        self.edge_cell = self.grid.grid[0][2]    # Top edge

    def test_central_cell_neighbors_radius_1(self):
        neighbors = self.central_cell.get_neighbors(self.grid, radius=1)
        total_neighbors = sum(len(cells) for cells in neighbors.values())
        self.assertEqual(total_neighbors, 8, "Central cell should have 8 neighbors for radius=1.")

    def test_central_cell_neighbors_radius_2(self):
        neighbors = self.central_cell.get_neighbors(self.grid, radius=2)
        total_neighbors = sum(len(cells) for cells in neighbors.values())
        self.assertEqual(total_neighbors, 24, "Central cell should have 24 neighbors for radius=2.")

    def test_corner_cell_neighbors_radius_1(self):
        neighbors = self.corner_cell.get_neighbors(self.grid, radius=1)
        total_neighbors = sum(len(cells) for cells in neighbors.values())
        self.assertEqual(total_neighbors, 3, "Corner cell should have 3 neighbors for radius=1.")

    def test_edge_cell_neighbors_radius_1(self):
        neighbors = self.edge_cell.get_neighbors(self.grid, radius=1)
        total_neighbors = sum(len(cells) for cells in neighbors.values())
        self.assertEqual(total_neighbors, 5, "Edge cell should have 5 neighbors for radius=1.")

    def test_corner_cell_neighbors_radius_2(self):
        neighbors = self.corner_cell.get_neighbors(self.grid, radius=2)
        total_neighbors = sum(len(cells) for cells in neighbors.values())
        self.assertEqual(total_neighbors, 8, "Corner cell should have 8 neighbors for radius=2.")

    def test_edge_cell_neighbors_radius_2(self):
        neighbors = self.edge_cell.get_neighbors(self.grid, radius=2)
        total_neighbors = sum(len(cells) for cells in neighbors.values())
        self.assertEqual(total_neighbors, 14, "Edge cell should have 14 neighbors for radius=2.")

class TestDistanceMaps(unittest.TestCase):
    def setUp(self):
        """
        Set up a 5x5 grid for testing distance maps.
        """
        self.grid = Grid(
            length=5,
            height=5,
            spawn_cells=[],
            target_cells=[(2, 2), (4, 4)],
            obstacle_cells=[(3, 3)],
            cell_size=1.0,
            movement_method="dijkstra"
        )

    def test_dijkstra_distance_map(self):
        # Create a grid with a target at (4, 4)
        grid = Grid(
            length=5,
            height=5,
            spawn_cells=[],
            target_cells=[(4, 4)],
            obstacle_cells=[],
            cell_size=1.0,
            movement_method="dijkstra"
        )

        # Expected distance map
        expected_map = [
            [5.657, 5.0, 4.472, 4.123, 4.0],
            [5.0, 4.243, 3.606, 3.162, 3.0],
            [4.472, 3.606, 2.828, 2.236, 2.0],
            [4.123, 3.162, 2.236, 1.414, 1.0],
            [4.0, 3.0, 2.0, 1.0, 0.0]
        ]

        # Compute the distance map
        grid.update_distance_maps()
        distance_map = grid.dijkstra_distance_maps[(4, 4)]

        # Print the distance map for debugging
        print("Corrected Dijkstra Distance Map:")
        for row in distance_map:
            print(["{:.3f}".format(cell) if cell != float('inf') else "inf" for cell in row])

        # Validate the computed map
        for row in range(5):
            for col in range(5):
                self.assertAlmostEqual(
                    distance_map[row][col], expected_map[row][col], delta=0.01,
                    msg=f"Mismatch in Dijkstra distance map for target (4, 4) at ({row}, {col})"
                )
        grid.plot_distance_map(distance_map)

    def test_flood_fill_distance_map(self):
        # Create a simple 5x5 grid with a target at (2, 2)
        grid = Grid(
            length=5,
            height=5,
            spawn_cells=[],
            target_cells=[(2, 2)],
            obstacle_cells=[],
            cell_size=1.0,
            movement_method="floodfill"
        )

        # Compute the distance map
        target_row, target_col = 2, 2
        distance_map = grid.flood_fill(target_row, target_col, target_state=3)

        # Expected distance map
        expected_map = [
            [4.0, 3.0, 2.0, 3.0, 4.0],
            [3.0, 2.0, 1.0, 2.0, 3.0],
            [2.0, 1.0, 0.0, 1.0, 2.0],
            [3.0, 2.0, 1.0, 2.0, 3.0],
            [4.0, 3.0, 2.0, 3.0, 4.0],
        ]

        # Print the distance map for debugging
        print("Corrected Flood Fill Distance Map:")
        for row in distance_map:
            print(["{:.1f}".format(cell) if cell != float('inf') else "inf" for cell in row])

        # Validate the result
        for row in range(5):
            for col in range(5):
                self.assertAlmostEqual(
                    distance_map[row][col], expected_map[row][col], delta=0.01,
                    msg=f"Mismatch in Flood Fill distance map for target ({target_row}, {target_col}) at ({row}, {col})"
                )
        grid.plot_distance_map(distance_map)
class TestPenalties(unittest.TestCase):

    def setUp(self):
        """Set up a grid for testing."""
        # Create a 5x5 grid with cell size 1.0
        self.grid = Grid(
            length=5.0, height=5.0,
            spawn_cells=[],
            target_cells=[(4, 4)],
            obstacle_cells=[],
            cell_size=1.0
        )
        # Place a target at (4, 4)
        self.grid.place_target(4, 4)
        # Place an agent at (0, 0)
        self.grid.place_agent(0, 0)
        self.agent = self.grid.agents[0]

    def test_precomputed_penalties(self):
        """Test that precomputed social penalties are calculated correctly."""
        # Place multiple agents in the grid
        self.grid.place_agent(1, 1)
        self.grid.place_agent(2, 2)

        # Compute social penalties using the precomputed method
        penalties = self.grid.compute_social_penalties()

        # Ensure penalties are calculated for each agent
        self.assertEqual(len(penalties), len(self.grid.agents))

        # Verify that penalties are non-zero and consistent with agent positions
        positions = np.array([[agent.row, agent.col] for agent in self.grid.agents])
        for i, penalty in enumerate(penalties):
            self.assertGreater(penalty, 0)

            # Check penalty consistency with distances
            deltas = positions - positions[i]
            distances = np.linalg.norm(deltas, axis=1)
            within_cutoff = distances <= 2.0

            # Penalty should be influenced by nearby agents within cutoff distance
            expected_penalty = sum(
                np.exp(-(distances[j] ** 2) / (2 * 0.5 ** 2))
                for j in range(len(distances))
                if within_cutoff[j] and i != j
            ) + 0.5  # Include stay penalty

            self.assertAlmostEqual(penalty, expected_penalty, places=2)

    def test_update_with_precomputed_penalties(self):
        """Test that the update method uses precomputed penalties correctly."""
        # Place a second agent near the first agent
        self.grid.place_agent(0, 1)
        self.grid.update_distance_maps()
        # Run the update method
        self.grid.update(self.grid.target_cells, timestep=1)

        # Verify penalties were used in movement decisions
        precomputed_penalties = self.grid.compute_social_penalties()
        for i, agent in enumerate(self.grid.agents):
            penalty = precomputed_penalties[i]
            self.assertGreater(penalty, 0)

class TestAgentSocialPenalty(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(
            length=5,
            height=5,
            cell_size=1,
            spawn_cells=[],
            target_cells=[],
            obstacle_cells=[]
        )
        self.agent = Agent(2, 2, cell_size=1)
        self.grid.grid[2][2] = self.agent

    def test_social_penalty(self):
        # Place other agents around the main agent
        self.grid.grid[1][1] = Agent(1, 1, cell_size=1)
        self.grid.grid[1][3] = Agent(1, 3, cell_size=1)
        self.grid.grid[3][1] = Agent(3, 1, cell_size=1)
        self.grid.grid[3][3] = Agent(3, 3, cell_size=1)

        # Calculate the social penalty
        penalty = self.agent.social_penalty(self.grid)

        # Verify the penalty is calculated correctly
        self.assertLess(penalty, 0, "Penalty should be smaller than 0 when there are neighboring agents.")

class TestRepulsiveForceAndSocialPenalty(unittest.TestCase):
    def setUp(self):
        # Create a 5x5 grid with agents and targets
        self.grid = Grid(
            length=5,
            height=5,
            spawn_cells=[],
            target_cells=[(4, 4)],
            obstacle_cells=[],
            cell_size=1.0,
            movement_method="dijkstra"
        )
        self.grid.update_distance_maps()

        # Place agents
        self.agent1 = Agent(2, 2, cell_size=1.0)
        self.agent2 = Agent(2, 3, cell_size=1.0)
        self.grid.grid[2][2] = self.agent1
        self.grid.grid[2][3] = self.agent2
        self.grid.agents.extend([self.agent1, self.agent2])

    def test_social_penalty_computation(self):
        penalty = self.agent1.social_penalty(self.grid)
        self.assertGreater(penalty, 0, "Social penalty should be positive with nearby agents.")

    def test_repulsive_force_computation(self):
        height, width = self.agent1.manhattan_difference_to(self.agent2)
        repulsive_force = self.agent1.repulsive_force(width, height)
        self.assertGreater(repulsive_force, 0, "Repulsive force should be positive for neighboring agents.")

    def test_agent_avoids_high_penalty(self):
        # Add additional agents to simulate crowding
        additional_agents = [
            Agent(1, 1, cell_size=1.0),
            Agent(1, 2, cell_size=1.0),
            Agent(1, 3, cell_size=1.0)
        ]
        for agent in additional_agents:
            self.grid.grid[agent.row][agent.col] = agent
            self.grid.agents.append(agent)

        # Update and ensure agent1 moves to minimize penalty
        self.grid.update(self.grid.target_cells, timestep=1)
        self.assertNotEqual((self.agent1.row, self.agent1.col), (2, 2), "Agent should move away from high-penalty area.")

    def test_agent_movement_with_penalties(self):
        original_position = (self.agent1.row, self.agent1.col)
        self.grid.update(self.grid.target_cells, timestep=1)
        new_position = (self.agent1.row, self.agent1.col)
        self.assertNotEqual(original_position, new_position, "Agent should move considering both distance and penalties.")

class TestParallelizedAgentMovement(unittest.TestCase):
    def setUp(self):
        """
        Set up a small grid with multiple agents for testing parallelization.
        """
        self.grid = Grid(
            length=5,
            height=5,
            spawn_cells=[],
            target_cells=[(4, 4)],
            obstacle_cells=[],
            cell_size=1.0,
            movement_method="dijkstra"
        )
        self.grid.update_distance_maps()

        # Add agents
        self.agent1 = Agent(0, 0, cell_size=1.0)
        self.agent2 = Agent(0, 1, cell_size=1.0)
        self.agent3 = Agent(1, 0, cell_size=1.0)
        self.grid.grid[0][0] = self.agent1
        self.grid.grid[0][1] = self.agent2
        self.grid.grid[1][0] = self.agent3
        self.grid.agents.extend([self.agent1, self.agent2, self.agent3])

    def test_unique_agent_positions_after_update(self):
        """
        Ensure no two agents occupy the same cell after an update.
        """
        def move_agent(agent):
            if not agent.arrived:
                agent.movement_towards_target(self.grid)

        # Parallelize agent movement
        with ThreadPoolExecutor() as executor:
            executor.map(move_agent, self.grid.agents)

        # Collect agent positions
        positions = [(agent.row, agent.col) for agent in self.grid.agents]
        unique_positions = set(positions)

        # Ensure all positions are unique
        self.assertEqual(len(positions), len(unique_positions), "Agents occupy the same cell after update.")

    def test_correct_movement_logic(self):
        """
        Verify each agent independently follows the correct movement logic.
        """
        initial_positions = [(agent.row, agent.col) for agent in self.grid.agents]

        def move_agent(agent):
            if not agent.arrived:
                agent.movement_towards_target(self.grid)

        with ThreadPoolExecutor() as executor:
            executor.map(move_agent, self.grid.agents)

        new_positions = [(agent.row, agent.col) for agent in self.grid.agents]

        # Ensure agents have moved and are closer to the target
        for i, (old_pos, new_pos) in enumerate(zip(initial_positions, new_positions)):
            self.assertNotEqual(old_pos, new_pos, f"Agent {i} did not move.")
            self.assertLess(
                self.grid.dijkstra_distance_maps[(4, 4)][new_pos[0]][new_pos[1]],
                self.grid.dijkstra_distance_maps[(4, 4)][old_pos[0]][old_pos[1]],
                f"Agent {i} did not move closer to the target."
            )

    def test_grid_consistency_after_update(self):
        """
        Ensure grid consistency after parallel updates.
        """
        def move_agent(agent):
            if not agent.arrived:
                agent.movement_towards_target(self.grid)

        with ThreadPoolExecutor() as executor:
            executor.map(move_agent, self.grid.agents)

        # Verify grid reflects agent positions correctly
        for agent in self.grid.agents:
            cell = self.grid.grid[agent.row][agent.col]
            self.assertIs(agent, cell, f"Grid inconsistency: Agent not correctly placed at ({agent.row}, {agent.col}).")

    def test_arrived_agents_removed_correctly(self):
        """
        Verify agents that arrive at the target are removed from the grid and agent list.
        """
        # Place one agent directly on the target
        target_agent = Agent(4, 4, cell_size=1.0)
        self.grid.grid[4][4] = target_agent
        self.grid.agents.append(target_agent)

        def move_agent(agent):
            if not agent.arrived:
                agent.movement_towards_target(self.grid)

        with ThreadPoolExecutor() as executor:
            executor.map(move_agent, self.grid.agents)

        # Ensure the agent is removed
        self.assertNotIn(target_agent, self.grid.agents, "Arrived agent was not removed.")
        self.assertNotIsInstance(self.grid.grid[4][4], Agent, "Arrived agent is still present in the target cell.")

if __name__ == "__main__":
    unittest.main()



