from math import prod

with open('input.txt', 'r') as f:
  lines = f.readlines()

# Read input as a 2d array, converting each of the characters to int
lines = [list(map(int, [*line.strip()])) for line in lines]

# Keep track of all trees that are visible from any direction
visible = set()

# Left to right
for row, line in enumerate(lines):
  tallest_tree = line[0]
  for col, tree in enumerate(line):
    # Outer trees - these are always visible
    if row == 0 or col == 0 or row == len(lines)-1 or col == len(line)-1:
      visible.add((row, col))
    elif tree > tallest_tree:
      tallest_tree = tree
      visible.add((row, col))

# Right to left
for row, line in enumerate(lines):
  tallest_tree = line[-1]
  for col, tree in enumerate(line[::-1]):
    if tree > tallest_tree:
      tallest_tree = tree
      visible.add((row, len(line)-col-1))

# Transpose the lines and repeat the above process -
# this acts as if we were traversing top to bottom and bottom to top
lines_transposed = [list(x) for x in zip(*lines)]

# Top to bottom
for row, line in enumerate(lines_transposed):
  tallest_tree = line[0]
  for col, tree in enumerate(line):
    if tree > tallest_tree:
      tallest_tree = tree
      visible.add((col, row))

# Bottom to top
for row, line in enumerate(lines_transposed):
  tallest_tree = line[-1]
  for col, tree in enumerate(line[::-1]):
    if tree > tallest_tree:
      tallest_tree = tree
      visible.add((len(line)-col-1, row))

### Part 2 ###
def get_scenic_score(tree_pos):
  # Extract row and column index from tree_pos tuple
  r, c = tree_pos

  # Compute the difference between the given position and the top, bottom, left, right
  top_diff = r
  bottom_diff = len(lines) - r - 1
  left_diff = c
  right_diff = len(lines[0]) - c - 1

  total_up = 0
  for i in range(1, top_diff+1):
    if lines[r-i][c] < lines[r][c]:
      total_up += 1
    else:
      total_up += 1
      break
  
  total_down = 0
  for i in range(1, bottom_diff+1):
    if lines[r+i][c] < lines[r][c]:
      total_down += 1
    else:
      total_down += 1
      break

  total_left = 0
  for i in range(1, left_diff+1):
    if lines[r][c-i] < lines[r][c]:
      total_left += 1
    else:
      total_left += 1
      break
  
  total_right = 0
  for i in range(1, right_diff+1):
    if lines[r][c+i] < lines[r][c]:
      total_right += 1
    else:
      total_right += 1
      break

  return prod([total_up, total_down, total_left, total_right])

# Iterate through each of the trees, finding the highest scenic score overall
highest_scenic_score = max([get_scenic_score((i, j)) for i in range(len(lines)) for j in range(len(lines[i]))])
##############

print('Part 1 answer:', len(visible))
print('Part 2 answer:', highest_scenic_score)