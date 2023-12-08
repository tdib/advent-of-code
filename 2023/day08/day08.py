# https://adventofcode.com/2023/day/8
from collections import defaultdict
import math
from functools import reduce

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

DIRECTION_MAP = {
    "L": 0,
    "R": 1,
}

def generate_nodes(lines):
    nodes = {}
    for line in lines:
        s = line.split(" = ")
        name = s[0]
        s = s[1].split(", ")
        left = s[0][1:]
        right = s[1][:-1]
        nodes[name] = (left, right)
    return nodes


def solve_part_1():
    ans = 0
    dirs = lines[0]
    nodes = generate_nodes(lines[2:])
    
    curr = "AAA"
    goal = "ZZZ"
    found = False
    while not found:
        for d in dirs:
            # Move our current node in the specified direction
            curr = nodes[curr][DIRECTION_MAP[d]]
            ans += 1
            # If we have reached ZZZ, we can terminate the loop
            if curr == goal:
                found = True
                break

    return ans


def solve_part_2():
    dirs = lines[0]
    nodes = generate_nodes(lines[2:])
    
    # Find the starting nodes
    curr_nodes = [node for node in nodes if node.endswith("A")]

    # visited = defaultdict(list)
    cycles = {}

    # Find how long each node takes to go from a possible end node back to another possible end node
    # i.e. "AAZ" -> "AAZ", where the nodes end with Z
    for curr_node_idx in range(len(curr_nodes)):
        found_cycle = False
        num_steps = 0
        looking = curr_nodes[curr_node_idx]
        # We go until we find a cycle for this node
        while not found_cycle:
            for dir in dirs:
                num_steps += 1
                # Where do we move to? Left or right?
                curr = nodes[curr_nodes[curr_node_idx]][DIRECTION_MAP[dir]]
                curr_nodes[curr_node_idx] = curr
                # If we come across an end node, stop the search
                # No idea why this works, but it's faster than my prev solution :) thanks Stefan
                if curr.endswith("Z"):
                    cycles[curr] = num_steps
                    found_cycle = True
                    break

    # The LCM of all cycle lengths will give us the number of iterations required for all of them
    # to end in Z
    return reduce(lambda x, y: math.lcm(x,y), list(cycles.values()))


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

