# https://adventofcode.com/2023/day/17
from queue import PriorityQueue

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

class State():
    def __init__(self, pos, facing_dir, dist_travelled, consecutive_count, directions_travelled):
        self.pos = pos
        self.facing_dir = facing_dir
        self.dist_travelled = dist_travelled
        self.consecutive_count = consecutive_count
        self.dir_path = directions_travelled
    
    def __lt__(self, other):
        return self.dist_travelled < other.dist_travelled
    
    def __iter__(self):
        yield self.pos
        yield self.facing_dir
        yield self.dist_travelled
        yield self.consecutive_count
        yield self.dir_path


def within_bounds(curr_pos, map_):
    row, col = curr_pos
    return row >= 0 and row < len(map_) and col >= 0 and col < len(map_[0])


def add_tuples(a, b):
    return (a[0] + b[0], a[1] + b[1])


def print_map(directions_travelled):
    path_taken = [(0, 0)]
    symbols = { RIGHT: ">", UP: "^", DOWN: "v", LEFT: "<" }
    dir_symbols = ["S"]
    curr = (0, 0)
    for dir in directions_travelled:
        curr = add_tuples(curr, dir)
        dir_symbols.append(symbols[dir])
        path_taken.append(curr)

    for r, row in enumerate(lava_pool):
        for c in range(len(row)):
            if (r, c) in path_taken:
                print(f"\033[91m{dir_symbols[path_taken.index((r, c))]}\033[0m", end="")
            else:
                print(lava_pool[r][c], end="")
        print()
    print()


# Construct map
lava_pool = [list(map(int, line)) for line in lines]
def travel_crucible(min_blocks, max_blocks):
    # Define which way you can turn when facing a given direction
    turns = {
        UP: (UP, LEFT, RIGHT),
        DOWN: (DOWN, LEFT, RIGHT),
        LEFT: (LEFT, UP, DOWN),
        RIGHT: (RIGHT, UP, DOWN)
    }

    # We don't really care about the starting position, so we can hard set the starts to be the right
    # and bottom of that - probably a better way to do this but if it works it works
    initial_states = [
        State((0, 1), RIGHT, 0, 1, [(0, 1)]),
        State((1, 0), DOWN, 0, 1, [(1, 0)])
    ]

    # Add the initial states into a priority queue
    q = PriorityQueue()
    for s in initial_states:
        q.put((0, s))

    # Define the target position - this is at the bottom right of our map
    target_pos = (len(lines) - 1, len(lines[0]) - 1)

    visited = set()
    min_dist = float('inf')
    min_path = []
    found = False
    while not q.empty() and not found:
        _, (curr_pos, curr_dir, curr_total, consecutive_count, dir_path) = q.get()

        # Add the current heat to a total for the successor states
        row, col = curr_pos
        new_total = curr_total + lava_pool[row][col]

        # We have encountered an end state (and ensured the current consecutive travel is allowed).
        # We can terminate here because we would have found the shortest path.
        if curr_pos == target_pos and consecutive_count >= min_blocks:
            min_dist = new_total
            min_path = dir_path
            found = True
            break
    
        # Caching - our current position, direction, and how many consecutive blocks will give us a unique state
        k = (curr_pos, curr_dir, consecutive_count)
        if k in visited: continue
        visited.add(k)

        for direction in turns[curr_dir]:
            # We are in a state where we cannot perform a turn, so we will just continue
            if consecutive_count < min_blocks and direction != curr_dir:
                continue

            # Given that we travel in X direction, recompute our consecutive count - this increases only if we continue
            # in the same direction that we are travelling in now
            next_pos = add_tuples(curr_pos, direction)
            new_consecutive_count = consecutive_count + 1 if direction == curr_dir else 1

            # If the new state is valid to add, then do it
            new_k = (next_pos, direction, new_consecutive_count)
            if within_bounds(next_pos, lava_pool) and new_consecutive_count <= max_blocks and new_k not in visited:
                new_dir_path = dir_path + [direction]
                new_state = State(next_pos, direction, new_total, new_consecutive_count, new_dir_path)
                q.put((new_total, new_state))

    return min_dist, min_path


def solve_part_1():
    min_dist, directions_travelled = travel_crucible(min_blocks=0, max_blocks=3)
    print("Part 1 path:")
    print_map(directions_travelled)
    return min_dist


def solve_part_2():
    min_dist, directions_travelled = travel_crucible(min_blocks=4, max_blocks=10)
    print("Part 2 path:")
    print_map(directions_travelled)
    return min_dist


p1 = solve_part_1()
p2 = solve_part_2()
print(f"Part 1 answer: {p1}")
print(f"Part 2 answer: {p2}")
