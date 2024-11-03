import random
from Grid import Grid
from Cell import Cell, SpawnCell, ObstacleCell, TargetCell, Agent

rows = 10
cols = 10
grid = Grid(rows, cols)
grid.place_border() 

num_spawn_cells = 1
spawn_cells_placed = 0
while spawn_cells_placed < num_spawn_cells:
    spawn_row = random.randint(1, rows - 2) 
    spawn_col = random.randint(1, cols - 2)
    if isinstance(grid.grid[spawn_row][spawn_col], Cell): 
        grid.place_agent(spawn_row, spawn_col)
        spawn_cells_placed += 1

num_obstacles = 3
obstacles_placed = 0
while obstacles_placed < num_obstacles:
    obstacle_row = random.randint(1, rows - 2) 
    obstacle_col = random.randint(1, cols - 2)
    if isinstance(grid.grid[obstacle_row][obstacle_col], Cell): 
        grid.place_obstacle(obstacle_row, obstacle_col)
        obstacles_placed += 1

num_target_cells = 3
target_cells_placed = 0
while target_cells_placed < num_target_cells:
    target_row = random.randint(1, rows - 2) 
    target_col = random.randint(1, cols - 2)
    if isinstance(grid.grid[target_row][target_col], Cell): 
        grid.place_target(target_row, target_col)
        target_cells_placed += 1

print("Initial Grid State:")
grid.display()

iteration = 0
max_iterations = 10

nearest_target_sum = []
line_of_sight_sum = []
potential_sum = []

while iteration < max_iterations:
    for i in range(grid.rows):
        for j in range(grid.cols):
            if isinstance(grid.grid[i][j], Agent): 
                agent = grid.grid[i][j]
                print(agent.find_nearest_target(grid))
                nearest_target_sum.append(agent.find_nearest_target(grid))
                print(agent.line_of_sight(grid))
                line_of_sight_sum.append(agent.line_of_sight(grid))
                print(agent.potential(grid))
                potential_sum.append(agent.potential(grid))


    grid.update()
    print("Updated Grid State:")
    grid.display()
    iteration += 1

print(nearest_target_sum)
print(line_of_sight_sum)
print(potential_sum)