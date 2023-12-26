import re
from collections import deque
from itertools import combinations

with open('input.txt') as f:
  lines = list(map(str.strip, f.readlines()))

# Parse nodes and collate them
flows = {}
neighbours = {}
for line in lines:
  r = r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)'
  matches = re.findall(r, line)[0]
  name = matches[0]
  curr_flow = int(matches[1])
  connected_tunnels = matches[2].split(', ')

  flows[name] = curr_flow
  neighbours[name] = connected_tunnels


# Get shortest distance from each node to any other non-zero node
dists = {}
START_VALVE = 'AA'
for curr_valve in neighbours:
  # Ignore 0 flow nodes (excluding start node)
  if flows[curr_valve] == 0 and curr_valve != START_VALVE:
    continue

  # Set distance to itself and start node to 0
  dists[curr_valve] = { curr_valve: 0, START_VALVE: 0 }

  queue = deque([(curr_valve, 0)])
  visited = set(curr_valve)
  while queue:
    name, dist = queue.popleft()
    for neighbour in neighbours[name]:
      # If this neighbour is in visited, it means we already have a shorter path to it
      if neighbour in visited:
        continue
      # We haven't seen it yet, so consider it visited
      else:
        visited.add(neighbour)
      
      # We compute the distance from curr_valve to this neighbour and add it to dists to keep track
      new_dist = dist + 1
      if flows[neighbour] > 0:
        dists[curr_valve][neighbour] = new_dist
      
      # This neighbour could potentially have neighbours that we do not have a distance tracked
      # for curr_valve so we append it to the queue to ensure we reach all nodes
      queue.append((neighbour, new_dist))
    
  # We don't need to know how far we are from ourself, it will always be 0
  del dists[curr_valve][curr_valve]
  # We don't need to know how far the start node is, its value is 0
  if curr_valve != START_VALVE:
    del dists[curr_valve][START_VALVE]


dp = {}
def dfs(time_left, start_valve=START_VALVE, opened_valves=set()):
  # We have had this exact case before
  if (time_left, start_valve, str(opened_valves)) in dp:
    return dp[(time_left, start_valve, str(opened_valves))]

  # For every neighbour of the start valve we evaluate how good it is
  heuristic = 0
  for valve, cost in dists[start_valve].items():
    # The valve will not give us any value since it is already opened
    if valve in opened_valves:
      continue

    # Travelling to this node and turning it on will have no benefit due to time
    new_time_left = time_left - cost - 1
    if new_time_left <= 0:
      continue
  
    # Here we have a worthy valve. Open it and continue.
    # When the recursion finishes we will find out if this was worth it
    heuristic = max(heuristic, dfs(new_time_left, valve, opened_valves | {valve} ) + flows[valve] * new_time_left)
    
  dp[(time_left, start_valve, str(opened_valves))] = heuristic
  return heuristic


print(f'Part 1 answer: {dfs(30)}')


# Naively attempt every combination of valves between yourself and the elephant by doing two
# searches with different visited lists (which emulates starting in the middle of the search)
# Note: we only need to go to half of len(dists) because the two subsets are indistinguishable,
# i.e. we don't need to try the same set twice because a + b is the same as b + a
max_pressure = 0
for i in range((len(dists)+1) // 2):
  # Generate a combination of distances with length i, and then use its complement
  # as the elephant's visited list
  for combination in combinations(dists, i):
    subset_1 = set(combination)
    subset_2 = set(dists) - subset_1
    # Run two searches and check if this combination of visited is higher than we currently have
    max_pressure = max(max_pressure, dfs(26, opened_valves=subset_1) + dfs(26, opened_valves=subset_2))


print(f'Part 2 answer: {max_pressure}')