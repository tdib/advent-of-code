with open('input.txt', 'r') as f:
  lines = list(map(str.strip, f.readlines()))

# Print a visual representation of the current map, including
# walls, sand, and sand source
def print_map(walls, settled_sand):
  # Figure out how much we can offset the width by (so we don't have to deal)
  # with values as large as 500 for indexing
  wall_width_offset = min(walls, key=lambda coord: coord[1])[1]

  # Find out how wide and tall the map should print
  # This computes the bounds of the walls
  wall_max_width = max(walls, key=lambda coord: coord[1])[1]
  wall_max_height = max(walls, key=lambda coord: coord[0])[0]
  PADDING = 2
  VOID_PADDING = 1

  # Do the printing
  for row in range(wall_max_height + PADDING + VOID_PADDING):
    for col in range(-PADDING, wall_max_width - wall_width_offset + PADDING + 1):
      pos = (row, col + wall_width_offset)
      if pos in walls:
        print(CHAR_WALL, end='')
      elif pos == SAND_SOURCE:
        print(CHAR_SAND_SOURCE, end='')
      elif pos in settled_sand:
        print(CHAR_SETTLED_SAND, end='')
      else:
        print(CHAR_EMPTY, end='')
    print()

# Recursively compute where the sand should be positioned for the next step
def simulate_sand(walls, settled_sand, start, floor_depth=None):
  row, col = start
  
  # How far under the lowest wall can we fall before being considered the void
  VOID_PADDING = 2
  void_depth = max(walls, key=lambda coord: coord[0])[0] + VOID_PADDING

  # If we provide a depth for the floor (like part 2), the floor will dynamically
  # generate under the current sand column position so we can never fall into the void
  if floor_depth:
    walls.add((floor_depth, col-1))
    walls.add((floor_depth, col))
    walls.add((floor_depth, col+1))

  # If we have filled up so much sand that there is a settled sand in the start
  # position, we should stop now
  if start in settled_sand:
    return (None, None)

  # First direction - move directly down
  down_pos = (row+1, col)
  while down_pos not in walls and down_pos not in settled_sand:
    if row > void_depth: return (None, None)
    return simulate_sand(walls, settled_sand, down_pos, floor_depth)
  
  # Second direction - down and left
  down_left_pos = (row+1, col-1)
  while down_left_pos not in walls and down_left_pos not in settled_sand:
    return simulate_sand(walls, settled_sand, down_left_pos, floor_depth)

  # Third direction - down and right
  down_right_pos = (row+1, col+1)
  while down_right_pos not in walls and down_right_pos not in settled_sand:
    # row, col = simulate_sand(walls, settled_sand, down_right_pos)
    return simulate_sand(walls, settled_sand, down_right_pos, floor_depth)
  
  # Reaching here means we have settled in a position - add it to settled positions
  settled_sand.add((row, col))
  return (row, col)

# A visual way to see what is happening
# Takes user input so you can analyse each step as it happens
def simulate_step(walls, settled_sand, source, floor_depth=None):
  if not settled_sand: print_map(walls, settled_sand)
  input()
  sand_pos = simulate_sand(walls, settled_sand, source, floor_depth)
  print_map(walls, settled_sand)
  return sand_pos

# Define symbols used for printing the map
CHAR_EMPTY = '.'
CHAR_WALL = '#'
CHAR_SETTLED_SAND = 'o'
CHAR_SAND_SOURCE = '+'

# Construct wall coordinates
# e.g. [[(0, 0), (0, 5), (5, 5)], [(10, 15), (15, 15)]]
wall_points = []
for line in lines:
  split = line.split(' -> ')
  curr_wall_points = []
  for coord_str in split:
    col, row = map(int, coord_str.split(','))
    curr_wall_points.append((row, col))
  wall_points.append(curr_wall_points)

# Construct all walls by filling in the gaps and flattening structure
# e.g. [(0, 0), (0, 3)] -> [(0, 0), (0, 1), (0, 2), (0, 3)]
# e.g [[(0, 0), (0, 1)], [(1, 1)]] -> [(0, 0), (0, 1), (1, 1)]
walls = set()
for curr_wall_points in wall_points:
  walls.update(curr_wall_points)
  for i in range(len(curr_wall_points) - 1):
    # We assume the current and next rows will connect in some way
    row, col = curr_wall_points[i]
    next_row, next_col = curr_wall_points[i+1]
    # We have to fill in the cols
    if row == next_row:
      # Ensure our range works and the first number is smaller
      if col > next_col: col, next_col = next_col, col
      # Fill the gaps
      fill = [(row, new_col) for new_col in range(col+1, next_col)]
      walls.update(fill)
    # We have to fill in the rows
    elif col == next_col:
      # Ensure our range works and the first number is smaller
      if row > next_row: row, next_row = next_row, row
      # Fill the gaps
      fill = [(new_row, col) for new_row in range(row+1, next_row)]
      walls.update(fill)

SAND_SOURCE = (0, 500)

### Part 1 ###
sand_unit_count = 0
settled_sand = set()
while simulate_sand(walls, settled_sand, SAND_SOURCE) != (None, None):
  sand_unit_count += 1
print(f'Part 1 answer: {sand_unit_count}')
##############

### Part 2 ###
FLOOR_DEPTH_PADDING = 2
floor_depth = max(walls, key=lambda coord: coord[0])[0] + FLOOR_DEPTH_PADDING
sand_unit_count = 0
settled_sand = set()
while simulate_sand(walls, settled_sand, SAND_SOURCE, floor_depth) != (None, None):
  sand_unit_count += 1
print(f'Part 2 answer: {sand_unit_count}')
##############
