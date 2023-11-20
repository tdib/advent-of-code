with open('/Users/dib/dev/advent-of-code-2022/day14/input.txt', 'r') as f:
  lines = list(map(str.strip, f.readlines()))

CHAR_EMPTY = '.'
CHAR_WALL = '#'
CHAR_SETTLED_SAND = 'o'
CHAR_SAND_SOURCE = '+'
CHAR_VOID_SAND = 'x'

def print_map(walls, settled_sand):
  wall_width_offset = min(walls, key=lambda coord: coord[1])[1]
  wall_max_width = max(walls, key=lambda coord: coord[1])[1]
  wall_max_height = max(walls, key=lambda coord: coord[0])[0]
  PADDING = 2
  VOID_PADDING = 1

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

# Construct wall coordinates
wall_points = []
for line in lines:
  split = line.split(' -> ')
  curr_wall_points = []
  for coord_str in split:
    col, row = map(int, coord_str.split(','))
    curr_wall_points.append((row, col))
  wall_points.append(curr_wall_points)


# Flatten
walls = []
for curr_wall_points in wall_points:
  walls.extend(curr_wall_points)


# Construct all walls
for curr_wall_points in wall_points:
  # wall_coords is a list of points for a given wall
  for i in range(len(curr_wall_points) - 1):
    row, col = curr_wall_points[i]
    next_row, next_col = curr_wall_points[i+1]
    # We have to fill in the cols
    if row == next_row:
      if col > next_col: col, next_col = next_col, col
      fill = [(row, new_col) for new_col in range(col+1, next_col)]
      walls.extend(fill)
    # We have to fill in the rows
    elif col == next_col:
      if row > next_row: row, next_row = next_row, row
      fill = [(new_row, col) for new_row in range(row+1, next_row)]
      walls.extend(fill)
    else:
      print('ERROR')

walls = set(walls)

SAND_SOURCE = (0, 500)

def simulate_sand(walls, settled_sand, start):
  row, col = start
  VOID_PADDING = 2
  void_depth = max(walls, key=lambda coord: coord[0])[0] + VOID_PADDING

  # Move down
  down_pos = (row+1, col)
  while down_pos not in walls and down_pos not in settled_sand:
    if row > void_depth: return (None, None)
    return simulate_sand(walls, settled_sand, (row+1, col))
  
  down_left_pos = (row+1, col-1)
  while down_left_pos not in walls and down_left_pos not in settled_sand:
    return simulate_sand(walls, settled_sand, down_left_pos)

  down_right_pos = (row+1, col+1)
  while down_right_pos not in walls and down_right_pos not in settled_sand:
    # row, col = simulate_sand(walls, settled_sand, down_right_pos)
    return simulate_sand(walls, settled_sand, down_right_pos)
  
  settled_sand.add((row, col))
  return (row, col)

def simulate_step(walls, settled_sand, source):
  print_map(walls, settled_sand)
  while True:
    # input()
    if simulate_sand(walls, settled_sand, source) == (None, None): break
    print_map(walls, settled_sand)
  print_map(walls, settled_sand)



settled_sand = set()
# simulate_step(walls, settled_sand, SAND_SOURCE)
# print(len(settled_sand))

sand_unit_count = 0
while simulate_sand(walls, settled_sand, SAND_SOURCE) != (None, None):
  sand_unit_count += 1

print(f'Part 1 answer: {sand_unit_count}')