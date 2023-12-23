# https://adventofcode.com/2023/day/23
from collections import deque

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def add_tuples(a, b):
    return (a[0] + b[0], a[1] + b[1])

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

START = (0, 1)
END = (len(lines) - 1, len(lines[0]) - 2)

# Map chars to a direction
m = {
    ">": RIGHT,
    "<": LEFT,
    "^": UP,
    "v": DOWN
}

def parse_map_positions():
    paths = set()
    slopes = {}

    # Parse grid positions - find all path and slopes
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            curr = (r, c)
            if ch == ".":
                paths.add(curr)
            elif ch in m:
                slopes[curr] = m[ch]
    
    return paths, slopes

def construct_graph(paths, slopes, is_part_2):
    intersections = {}
    for p in paths:
        num_connections = 0
        for d in DIRECTIONS:
            next_pos = add_tuples(p, d)
            if not is_part_2 and next_pos in slopes and d != slopes[next_pos]:
                continue
            if next_pos in paths or next_pos in slopes:
                num_connections += 1
        
        # If we have a start position or an intersection, then keep track of it
        if num_connections != 2:
            intersections[p] = num_connections
    
    # Create state reduced graph by flood filling from every intersection to every other intersection.
    # We keep track of the cost to travel between states, so no graph cost data is lost
    graph = {}
    for intersection in intersections:
        s = deque([(intersection, 0)])
        v = set()
        graph[intersection] = []

        while s:
            curr, dist = s.pop()
            v.add(curr)

            # We are about to expand another intersection node - we don't want to do this
            if curr in intersections and curr != intersection:
                graph[intersection].append((curr, dist))
                continue

            # Continue travelling in the direction we have not yet explored
            for d in DIRECTIONS:
                next_pos = add_tuples(curr, d)
                if not is_part_2 and next_pos in slopes and d != slopes[next_pos]:
                    continue
                if (next_pos in paths or next_pos in slopes) and next_pos not in v:
                    s.append((next_pos, dist + 1))
    
    return graph

def dfs(graph, paths, slopes):
    # Perform a DFS from the start to the other waypoints/intersections and keep track of the highest
    # cost path so far. This still takes a few seconds but is viable because of the state reduction.
    highest_cost = 0
    s = deque([(START, 0, set())])
    while s:
        curr, curr_cost, v = s.pop()
        v.add(curr)

        # We have a path that has reached the end and it is a longer one than we know about
        if curr == END and curr_cost > highest_cost:
            highest_cost = curr_cost
        
        # Continue traversing
        for neighbour, cost in graph[curr]:
            if (neighbour in paths or neighbour in slopes) and neighbour not in v:
                new_path = curr_cost + cost
                s.append((neighbour, new_path, v | {neighbour} ))

    return highest_cost

def solve_part_1():
    paths, slopes = parse_map_positions()
    graph = construct_graph(paths, slopes, is_part_2=False)
    longest_dist = dfs(graph, paths, slopes)
    
    return longest_dist

def solve_part_2():
    paths, slopes = parse_map_positions()
    graph = construct_graph(paths, slopes, is_part_2=True)
    longest_dist = dfs(graph, paths, slopes)
    
    return longest_dist

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
