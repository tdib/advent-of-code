# https://adventofcode.com/2023/day/10
from collections import deque, defaultdict

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def add_tuples(a, b):
    return (a[0] + b[0], a[1] + b[1])

# Define the directions each symbol can go
EMPTY = "."
START = "S"
DOWN_RIGHT = "F"
DOWN_LEFT = "7"
UP_DOWN = "|"
UP_RIGHT = "L"
UP_LEFT = "J"
LEFT_RIGHT = "-"
direction_map = {
    DOWN_RIGHT: [(1, 0), (0, 1)],
    DOWN_LEFT: [(0, -1), (1, 0)],
    UP_DOWN: [(-1, 0), (1, 0)],
    LEFT_RIGHT: [(0, -1), (0, 1)],
    UP_RIGHT: [(-1, 0), (0, 1)],
    UP_LEFT: [(-1, 0), (0, -1)],
}
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def build_graph(_map):
    # Adjacency list - graph representation
    adj = defaultdict(set)

    # Build our graph
    start = None
    for row, line in enumerate(_map):
        for col, char in enumerate(line):
            curr = (row, col)
            # Compute the directions it is possible to travel in
            if char == START and start == None:
                start = curr
                for dir in DIRECTIONS:
                    possible = add_tuples(curr, dir)
                    for transitive_dir in direction_map[_map[possible[0]][possible[1]]]:
                        if curr == add_tuples(possible, transitive_dir):
                            adj[curr].add(possible)
                continue

            # We need to find pipes, and see get what they are connected to
            if char != EMPTY:
                for dir in direction_map[char]:
                    adj[curr].add(add_tuples(curr, dir))
    return start, adj


def bfs(_map):
    start, adj = build_graph(_map)
    q = deque([start])
    v = set()
    dists = {start: 0}
    curr = start
    while q:
        curr = q.popleft()
        v.add(curr)

        for child in adj[curr]:
            if child not in v and within_bounds(child, _map):
                q.append(child)
                dists[child] = dists[curr] + 1
        
    return v, dists


# Perform a flood fill from a given start node. This function assumes the map has been expanded, and uses
# is_valid_position as a predicate for assessing a valid successor position
def flood_fill(_map, start):
    v = set()
    q = deque([start])
    while q:
        curr = q.popleft()
        v.add(curr)

        nexts = [add_tuples(curr, d) for d in DIRECTIONS]
        for child in nexts:
            if child not in v and child not in q and within_bounds(child, _map) and is_valid_position(_map, child):
                q.append(child)
    return v



def print_map(lines, visited):
    for i, row in enumerate(lines):
        for j, col in enumerate(row):
            if (i, j) in visited:
                print(f"\033[91m{col}\033[0m", end="")
            else:
                print(col, end="")
        print()
    print()


# Simply checks if the given position falls within the bounds of the provided array
def within_bounds(pos, arr):
    return pos[0] >= 0 and pos[0] < len(arr) and pos[1] >= 0 and pos[1] < len(arr[0])


# For a given position in the expanded map, if our current position connects to any other pipes,
# the position is then invalid. This is because as our map expands, we don't fill in the pipes,
# so this scenario is the same as travelling onto a pipe (which is not allowed).
def is_valid_position(expanded_map, pos):
    # If we encounter a pipe, it is an invalid position
    if expanded_map[pos[0]][pos[1]] not in ".#":
        return False
    
    # Can we connect to the above position?
    up = add_tuples(pos, (-1, 0))
    if within_bounds(up, expanded_map) and expanded_map[up[0]][up[1]] in "|F7":
        return False

    # Can we connect to the below position?
    down = add_tuples(pos, (1, 0))
    if within_bounds(down, expanded_map) and expanded_map[down[0]][up[1]] in "|JL":
        return False

    # Can we connect to the left position?
    left = add_tuples(pos, (0, -1))
    if within_bounds(left, expanded_map) and expanded_map[left[0]][left[1]] in "-LF":
        return False

    # Can we connect to the right position?
    right = add_tuples(pos, (0, 1))
    if within_bounds(right, expanded_map) and expanded_map[right[0]][right[1]] in "-7J":
        return False

    return True


def solve_part_1():
    _, dists = bfs(lines)

    return max(dists.values())


def solve_part_2():
    flooded_visited, _ = bfs(lines)

    # After having performed a search from the start node, get rid of any pipes
    # that were not reached, and instead turn them into empty characters
    new_lines = []
    for row, line in enumerate(lines):
        temp_row = []
        for col, char in enumerate(line):
            if (row, col) in flooded_visited:
                temp_row.append(char)
            else:
                temp_row.append(EMPTY)
        new_lines.append(''.join(temp_row))

    # Fill every second row and column with a new symbol (#)
    # This will be used to evaluate which positions we can "squeeze" into
    EXPAND = "#"
    expanded_map = []
    expanded_map.append(EXPAND*(len(new_lines[0])*2+1))
    for l in new_lines:
        expanded_map.append(EXPAND + ''.join([f"{c}{EXPAND}" for c in l]))
        expanded_map.append(EXPAND*(len(l*2)+1))
    
    flooded_visited = flood_fill(expanded_map, (0, 0))


    # Get a map of every position
    max_row = max(flooded_visited, key=lambda x: x[0])[0]
    max_col = max(flooded_visited, key=lambda x: x[1])[1]
    all_positions = set()
    for r in range(max_row):
        for c in range(max_col):
            all_positions.add((r, c))

    # Get all positions which were NOT visited by the flood fill
    # These positions will either be pipe that was part of the BFS, or empty positions
    non_flooded_positions = all_positions - flooded_visited

    # Filter our positions for those that are empty
    encased_empty_positions = [pos for pos in non_flooded_positions if expanded_map[pos[0]][pos[1]] == EMPTY]

    return len(encased_empty_positions)

a = solve_part_1()
b = solve_part_2()
print(f"Part 1 answer: {a}")
print(f"Part 2 answer: {b}")

