from collections import defaultdict, deque

with open('input.txt', 'r') as f:
  lines = list(map(str.strip, f.readlines()))

ELEVATION_OFFSET = ord('a')
START_LOCATION = -14
END_LOCATION = -28
start = None
end = None

# Map elevation to ints
# e.g. 'a' -> 0, 'z' -> 25
elevation_map = []
for row_idx, row in enumerate(lines):
  curr_row = []
  for col_idx, elevation in enumerate(row):
    elevation = ord(elevation) - ELEVATION_OFFSET
    if elevation == START_LOCATION:
      start = (row_idx, col_idx)
      elevation = ord('a') - ELEVATION_OFFSET
    if elevation == END_LOCATION:
      end = (row_idx, col_idx)
      elevation = ord('z') - ELEVATION_OFFSET
    curr_row.append(elevation)
  elevation_map.append(curr_row)

# Element-wise tuple addition
def add_tuples(a, b):
  return (a[0]+b[0], a[1]+b[1])

# Perform BFS from a start to end position
def bfs(start, end):
  directions = ((0, 1), (0, -1), (-1, 0), (1, 0))
  predecessors = defaultdict(list)
  q = deque([start])
  v = set()

  while len(q):
    curr = q.popleft()
    # We have reached the target - find the path that got us here
    if curr == end:
      return backtrack(predecessors, curr)
    v.add(curr)

    # Find where we can move from here and add it to the queue
    for direction in directions:
      target = add_tuples(curr, direction)
      if target not in v and target not in q and can_move(curr, target):
        q.append(target)
        predecessors[target].append(curr)
  
  # There is no path that reaches the target
  return []

# Given a list of predecessors, backtrack until we find the start node,
# returning the path that was taken to get to the goal
def backtrack(predecessors, target):
  path = []
  while target in predecessors:
    path.append(target)
    target = predecessors[target][-1]
  return path[::-1]

# Check if it is possible to move from position curr to target. This only checks
# if the movement is possible, not if it has been visited or any other conditions
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
  if elevation_map[target_row][target_col] - elevation_map[curr_row][curr_col] > 1:
    return False

  return True

def solve_part_1():
  # Perform regular BFS from start to end
  answer = len(bfs(start, end))
  print(f'Part 1 answer: {answer}')

def solve_part_2():
  # Find all 'a' positions
  possible_starts = []
  for row_idx, row in enumerate(elevation_map):
    for col_idx in range(len(row)):
      if elevation_map[row_idx][col_idx] == 0:
        possible_starts.append((row_idx, col_idx))

  # Perform a bfs for each start position
  possible_paths = []
  for possible_start in possible_starts:
    possible_paths.append(bfs(possible_start, end))

  # Find the minimum path of those paths
  answer = min(filter(lambda l: l > 0, list(map(len, possible_paths))))
  print(f'Part 2 answer: {answer}')
  

solve_part_1()
solve_part_2()



