from math import prod

with open('test.txt', 'r') as f:
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
      print(1, (row, col))
      visible.add((row, col))
      # print(row, col)
    elif tree > tallest_tree:
      
      tallest_tree = tree
      print(2, (row, col), 'tree', tree, 'tallest', tallest_tree)
      print(len(visible))
      visible.add((row, col))
      print(len(visible))

# Right to left
for row, line in enumerate(lines):
  tallest_tree = line[-1]
  for col, tree in enumerate(line[::-1]):
    print('??', tree, tallest_tree)
    if tree > tallest_tree:
      tallest_tree = tree
      print(3, (row, len(line)-col-1))
      visible.add((row, len(line)-col-1))

lines_transposed = [list(x) for x in zip(*lines)]
# Left to right
for row, line in enumerate(lines_transposed):
  tallest_tree = line[0]
  for col, tree in enumerate(line):
    if tree > tallest_tree:
      tallest_tree = tree
      print(4, (col, row))
      visible.add((col, row))

# Right to left
for row, line in enumerate(lines_transposed):
  tallest_tree = line[-1]
  for col, tree in enumerate(line[::-1]):
    if tree > tallest_tree:
      tallest_tree = tree
      print(5, (len(line)-col-1, row))
      visible.add((len(line)-col-1, row))


# for row, line in enumerate(lines):
#   for col, tree in enumerate(line):

def get_scenic_score(tree_pos):
  r, c = tree_pos
  top_diff = r
  bot_diff = len(lines) - r - 1
  left_diff = c
  right_diff = len(lines[0]) - c - 1
  view_score = 1
  print(top_diff, left_diff, bot_diff, right_diff)

  total_up = 0
  for i in range(1, top_diff+1):
    # if len(tops) == 0 or lines[r-i][c] > tops[-1]:
    #   tops.append(lines[r-i][c])
    if not lines[r-i][c] > lines[r][c]:
      total_up += 1
    else:
      break
  
  total_down = 0
  for i in range(1, bot_diff+1):
    if not lines[r+i][c] > lines[r][c]:
      total_down += 1
    else:
      break

  total_left = 0
  for i in range(1, left_diff+1):
    if not lines[r][c-i] > lines[r][c]:
      total_left += 1
    else:
      break
  
  # rights = []
  total_right = 0
  for i in range(1, right_diff+1):
    if not lines[r][c+i] > lines[r][c]:
      total_right += 1
    else:
      break

  # print('top', tops)
  # print('bot', bots)
  # print('left', lefts)
  # print('right', rights)
  # hi = [1, len(tops), len(bots), len(lefts), len(rights)]
  # print('!!!!!!!', r, c, prod(hi))
  # return prod(hi)

  return prod([total_up, total_down, total_left, total_right])

scenic_scores = []
for i in range(len(lines)):
  for j in range(len(lines[i])):
    scenic_scores.append(get_scenic_score((i, j)))

print('Part 1 answer:', len(visible))
print('Part 1 answer:', max(scenic_scores))