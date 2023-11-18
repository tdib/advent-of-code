from collections import defaultdict

with open('/Users/dib/dev/advent-of-code-2022/day12/input.txt', 'r') as f:
  lines = list(map(str.strip, f.readlines()))

START_LOCATION = -14
END_LOCATION = -28
start = None
end = None

# Map elevation to ints
elevation_map = []
for row_idx, row in enumerate(lines):
  curr_row = []
  for col_idx, elevation in enumerate(row):
    elevation = ord(elevation) - ord('a')
    if elevation == START_LOCATION:
      start = (row_idx, col_idx)
    if elevation == END_LOCATION:
      end = (row_idx, col_idx)
    curr_row.append(elevation)
  elevation_map.append(curr_row)

elevation_map[start[0]][start[1]] = ord('a') - ord('a')
elevation_map[end[0]][end[1]] = ord('z') - ord('a')

  
def add_tuples(a, b):
  return (a[0]+b[0], a[1]+b[1])

def bfs(start, end):
  predecessors = defaultdict(list)
  directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
  direction_map = {
    (0, -1): 'left',
    (0, 1): 'right',
    (-1, 0): 'up',
    (1, 0): 'down'
  }
  curr = start
  q = [curr]
  v = []

  while len(q):
    # input()
    # for i, row in enumerate(elevation_map):
    #   for j, elevation in enumerate(row):
    #     if (i, j) in v:
    #       print('#', end='')
    #     else:
    #       print(lines[i][j], end='')
    #   print()
    # print('q', q)
    curr = q.pop(0)
    if curr == end:
      print('right before end', curr)
      return backtrack(predecessors, curr)
    v.append(curr)

    # Find where we can move from here and add it to the queue
    for direction in directions:
      # print(f'checking {direction_map[direction]}')
      target = add_tuples(curr, direction)
      # print('target', target)
      if target not in v and can_move(curr, target):
        # print(f'can move {direction_map[direction]} ({direction}) from {curr}')
        if target not in q:
          q.append(target)
          if curr not in predecessors[target]:
            predecessors[target].append(curr)
  print('man')
  return []

def backtrack(predecessors, target):
  # print('pre', predecessors[(2, 5)])
  # print()
  path = []
  while target in predecessors:
    path.append(target)
    # print('path', path)
    target = predecessors[target][-1]
    # print('target', target)
  return path[::-1]

def can_move(curr, target):
  curr_row, curr_col = curr
  target_row, target_col = target
  # Row is out of bounds
  if target_row < 0 or target_row >= len(elevation_map):
    return False
  # Col is out of bounds
  if target_col < 0 or target_col >= len(elevation_map[0]):
    return False
  # The elevation jump is too high
  # print(elevation_map[target_row][target_col], elevation_map[curr_row][curr_col], abs(elevation_map[target_row][target_col] - elevation_map[curr_row][curr_col]))
  if elevation_map[target_row][target_col] - elevation_map[curr_row][curr_col] > 1:
    return False

  # print('e')
  return True
  
possible_starts = []
for row_idx, row in enumerate(elevation_map):
  for col_idx, elevation in enumerate(row):
    if elevation_map[row_idx][col_idx] == 0:
      possible_starts.append((row_idx, col_idx))

possible_paths = []
for possible_start in possible_starts:
  print(f'Trying path from {possible_start}...')
  possible_paths.append(bfs(possible_start, end))
  print(f'Result: {len(possible_paths[-1])}')
  print()

print(list(map(len, possible_paths)))
print(min(filter(lambda l: l > 0, list(map(len, possible_paths)))))



