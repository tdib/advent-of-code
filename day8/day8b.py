from math import prod

with open('input.txt', 'r') as f:
  lines = f.readlines()

lines = [list(map(int, [*line.strip()])) for line in lines]

for l in lines:
  print(l)

visible = set()
# Left to right
for row, line in enumerate(lines):
  tallest_tree = line[0]
  for col, tree in enumerate(line):
    # Outer trees
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

lines_transposed = [list(x) for x in zip(*lines)]
# Left to right
for row, line in enumerate(lines_transposed):
  tallest_tree = line[0]
  for col, tree in enumerate(line):
    if tree > tallest_tree:
      tallest_tree = tree
      visible.add((col, row))

# Right to left
for row, line in enumerate(lines_transposed):
  tallest_tree = line[-1]
  for col, tree in enumerate(line[::-1]):
    if tree > tallest_tree:
      tallest_tree = tree
      visible.add((len(line)-col-1, row))


# for row, line in enumerate(lines):
#   for col, tree in enumerate(line):

def get_scenic_score(tree_pos):
  r, c = tree_pos
  top_diff = r
  bot_diff = len(lines) - r - 1
  left_diff = c
  right_diff = len(lines[0]) - c - 1

  total_up = 0
  tops = []
  for i in range(1, top_diff+1):
    # if len(tops) == 0 or lines[r-i][c] < lines[r][c] or tops[0] < lines[r][c]:
      # tops.append(lines[r-i][c])
      # total_up += 1

    if lines[r-i][c] < lines[r][c]:
      print('up', lines[r-i][c])
      total_up += 1
    else:
      total_up += 1
      break
  
  total_down = 0
  bots = []
  for i in range(1, bot_diff+1):
    # if len(bots) == 0 or lines[r+i][c] < lines[r][c] or bots[0] < lines[r][c]:
    #   bots.append(lines[r+i][c])
    #   total_down += 1

    if lines[r+i][c] < lines[r][c]:
      print('down', lines[r+i][c])
      total_down += 1
    else:
      total_down += 1
      break

  total_left = 0
  lefts = []
  for i in range(1, left_diff+1):
    # if len(lefts) == 0 or lines[r][c-i] < lines[r][c] or lefts[0] < lines[r][c]:
    if lines[r][c-i] < lines[r][c]:
      # print('left', lines[r][c-i])
      lefts.append(lines[r][c-i])
      total_left += 1
    else:
      total_left += 1
      break
  
  rights = []
  total_right = 0
  for i in range(1, right_diff+1):
    # if len(rights) == 0 or lines[r][c+i] < lines[r][c] or rights[0] < lines[r][c]:
    if lines[r][c+i] < lines[r][c]:
      rights.append(lines[r][c+i])
      print('right', lines[r][c+i])
      total_right += 1
    else:
      total_right += 1
      break

  x = prod([total_up, total_down, total_left, total_right])
  print(f'Pos {tree_pos}, u={total_up} d={total_down} l={total_left} r={total_right} x={x}')
  # return prod(hi)

  return prod([total_up, total_down, total_left, total_right])

scenic_scores = []
for i in range(len(lines)):
  for j in range(len(lines[i])):
    scenic_scores.append(get_scenic_score((i, j)))

print('Part 1 answer:', len(visible))
print('Part 2 answer:', max(scenic_scores))