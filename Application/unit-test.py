import unittest, math
from Grid import Grid
from Cell import Cell, SpawnCell, TargetCell, Agent, ObstacleCell

#Werden wir später noch in einen dedizierten Testordner verschieben
class TestAgentBehavior(unittest.TestCase):

    def setUp(self):

        # Einfaches 5x5 Grid
        self.grid = Grid(
            rows=5,
            cols=5,
            spawn_cells=[(1, 1)],
            target_cells=[(3, 3)],
            obstacle_cells=[]#Momentan noch keine Kolisionsvermeidung
        )

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
        self.grid.update(self.grid.target_cells)


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
        agent = Agent(2, 2)
        self.grid.grid[2][2] = agent
        self.grid.agents.append(agent)

        # Update bewirkt das er sich Ziel Nähert
        for timestep in range(10):
            self.grid.update(self.grid.target_cells, timestep=timestep)

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


        self.grid = Grid(
            rows=12,
            cols=12,
            spawn_cells=[(6, 6)],
            target_cells=[(2, 5), (8, 9)],
            obstacle_cells=[(4, 2)]#Momentan noch keine Kolisionsvermeidung
        )


class TestCellNeighbors(unittest.TestCase):
    def setUp(self):
        # Create a 5x5 grid for testing
        self.grid = Grid(
            rows=5,
            cols=5,
            spawn_cells=[],
            target_cells=[],
            obstacle_cells=[]
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

if __name__ == '__main__':
    unittest.main()
