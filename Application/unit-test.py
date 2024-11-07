import unittest, math
from Grid import Grid
from Cell import Cell, SpawnCell, TargetCell, Agent

#Werden wir später noch in einen dedizierten Testordner verschieben
class TestGrid(unittest.TestCase):

    def setUp(self):

        # Einfaches 5x5 Grid
        self.grid = Grid(
            rows=5,
            cols=5,
            spawn_cells=[(1, 1)],
            target_cells=[(3, 3)],
            obstacle_cells=[]#Momentan noch keine Kolisionsvermeidung
        )


   # one unit test tests only -> each class should test its method, and not via grid.update testing spawn agents. Please check again anc create real unit tests.

    def test_spawn_agents(self):

        #Zu Beginn noch keine Agenten in der Liste
        self.assertEqual(len(self.grid.agents), 0)

        # Update erzeugt neue Agenten
        self.grid.update(self.grid.target_cells)

        # Check ob Liste gewachsen ist
        self.assertGreater(len(self.grid.agents), 0, "No agents were spawned.")

        # Spawnlocation überprüfen, Valide Zellen sind spawn_neighbors
        spawn_neighbors = [
            (0, 1), (2, 1), (1, 0), (1, 2), (0, 0), (0, 2), (2, 0), (2, 2)
        ]
        #Agenten Position ermitteln
        agent_positions = [(agent.row, agent.col) for agent in self.grid.agents]

        for pos in agent_positions:
            #agenten Position muss in spawn_neighbors sein
            self.assertIn(pos, spawn_neighbors, "Agent spawned in an invalid cell.")

    def test_agent_removal_on_arrival(self):

        # Plaziere Agent bei Ziel
        agent = Agent(2, 2)
        self.grid.grid[2][2] = agent
        self.grid.agents.append(agent)

        # Update bewirkt das er sich Ziel Nähert
        self.grid.update(self.grid.target_cells)

        # Wir lassen sicherheitshalber mehr iterationen als nötig laufen falls sich die 5x5 grösse mal ändert
        #
        for _ in range(10):
            self.grid.update(self.grid.target_cells)

        # Verifiziere Löschung
        self.assertNotIn(agent, self.grid.agents, "Agent was not removed after arrival.")
        self.assertNotIsInstance(self.grid.grid[3][3], Agent, "Agent is still present at the target cell.")

    def test_agent_movement_toward_target(self):

        # Plaziere Agenten
        agent = Agent(0, 0)
        self.grid.grid[0][0] = agent
        self.grid.agents.append(agent)

        # Initial und Ziel Positionen
        initial_position = (agent.row, agent.col)
        target_position = self.grid.target_cells[0] # Zielkoordinaten

        # Initiale Distanz
        initial_distance = math.sqrt((target_position[0] - initial_position[0]) ** 2 +
                                     (target_position[1] - initial_position[1]) ** 2)

        # Bewegung zum Ziel durch Update
        self.grid.update(self.grid.target_cells)

        # Neue Distanz
        new_position = (agent.row, agent.col)
        new_distance = math.sqrt((target_position[0] - new_position[0]) ** 2 +
                                 (target_position[1] - new_position[1]) ** 2)

        # Neue Distanz muss kleiner sein als die vorherige
        self.assertLess(new_distance, initial_distance, "Agent did not move closer to the target.")


if __name__ == '__main__':
    unittest.main()
