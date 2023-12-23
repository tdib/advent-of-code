# https://adventofcode.com/2023/day/23
from collections import deque, defaultdict
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def add_tuples(a, b):
    return (a[0] + b[0], a[1] + b[1])

def within_bounds(pos):
    row, col = pos
    return row >= 0 and row < len(lines) and col >= 0 and col < len(lines[0])

def print_map(v):
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            curr = (r, c)
            if curr in v:
                print("O", end="")
            else:
                print(ch, end="")
        print()
    print()

def find_longest_path(start, target):
    longest_path = []
    s = deque([(start, [start])])
    i = 0
    while s:
        curr, path = s.pop()
        if curr == target and len(path) > len(longest_path):
            # print_map(path)
            longest_path = path
            print("NEW LONGEST", len(longest_path))

        # if i % 10_000 == 0:
            # print(path)
            # input()
            # print_map(path)
        
        DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
        for d in DIRECTIONS:
            next_pos = add_tuples(curr, d)
            if (next_pos in paths or next_pos in slopes) and within_bounds(next_pos) and next_pos not in path:
            # if next_pos not in path and within_bounds(next_pos):
                new_path = path + [next_pos]
                s.append((next_pos, new_path))

    return longest_path - 1

forest = set()
paths = set()
slopes = {}
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
def solve_part_1():
    m = {
        ">": RIGHT,
        "<": LEFT,
        "^": UP,
        "v": DOWN
    }
    ans = 0
    START = (0, 1)
    END = (len(lines) - 1, len(lines[0]) - 2)
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            curr = (r, c)
            if ch == "#":
                forest.add(curr)
            elif ch == ".":
                paths.add(curr)
            else:
                slopes[curr] = m[ch]
    


    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
    waypoints = {}
    for p in paths:
        num_connections = 0
        connections = set()
        for d in DIRECTIONS:
            next_pos = add_tuples(p, d)
            if next_pos in paths or next_pos in slopes:
                connections.add(next_pos)
                num_connections += 1
        
        # if len(connections) >= 2:
        if num_connections > 2 or num_connections == 1:
            waypoints[p] = num_connections
    
    for k, v in waypoints.items():
        print(k, v)
    
    graph = {}
    for w in waypoints:
        q = deque([(w, 0)])
        v = set()
        graph[w] = []

        while q:
            curr, dist = q.pop()
            v.add(curr)

            if curr in waypoints and curr != w:
                graph[w].append((curr, dist))
                continue

            for d in DIRECTIONS:
                next_pos = add_tuples(curr, d)
                if (next_pos in paths or next_pos in slopes) and next_pos not in v:
                    q.append((next_pos, dist + 1))

    # print("GRAPH")
    # for k, v in graph.items():
    #     print(k, v)

    highest_cost = 0
    s = deque([(START, 0, set())])
    i = 0
    while s:
        curr, curr_cost, v = s.pop()
        if curr == END and curr_cost > highest_cost:
            # print_map(path)
            highest_cost = curr_cost
            print("NEW LONGEST", curr_cost)
        
        v.add(curr)

        # if i % 10_000 == 0:
            # print(path)
            # input()
            # print_map(path)
        
        # print(curr)
        for neighbour, cost in graph[curr]:
            if (neighbour in paths or neighbour in slopes) and within_bounds(neighbour) and neighbour not in v:
            # if next_pos not in path and within_bounds(next_pos):
                new_path = curr_cost + cost
                s.append((neighbour, new_path, v | {neighbour} ))

    return highest_cost

    return 0
    # longest = find_longest_path(START, END)
    # print(longest)
    # return len(longest)
            

    q = deque([(START, set())])

    longest = 0
    longest_v = set()
    while q:
        # print(len(q))
        curr, v = q.popleft()

        # print_map(v)
        if len(v) > longest and curr == END:
            longest = len(v)
            longest_v = v
            print_map(v)
            print("Longest", longest)

        for d in DIRECTIONS:
            next_pos = add_tuples(curr, d)
            if (next_pos in paths or next_pos in slopes) and within_bounds(next_pos) and next_pos not in v and next_pos not in q:
                # if next_pos in slopes:
                #     if d != slopes[next_pos]:
                #         continue
                q.append((next_pos, v | {curr}))
    
    print_map(longest_v)







    return longest


def solve_part_2():
    ans = 0
    for line in lines:
        pass
    return ans


print(f"Part 1 answer: {solve_part_1()}")
# != 6149
# > 6223
print(f"Part 2 answer: {solve_part_2()}")

