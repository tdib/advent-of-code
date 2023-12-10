# https://adventofcode.com/2023/day/10
from collections import deque, defaultdict
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def add_tuples(a, b):
    return (a[0] + b[0], a[1] + b[1])

def solve_part_1():
    ans = 0
    adj = defaultdict(set)
    m = {
        "F": [(1, 0), (0, 1)],
        "7": [(0, -1), (1, 0)],
        "|": [(-1, 0), (1, 0)],
        "-": [(0, -1), (0, 1)],
        "L": [(-1, 0), (0, 1)],
        "J": [(-1, 0), (0, -1)],
    }
    start = None
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "S":
                print("FOUND S", row, col)
                start = (row, col)
                for dir in m["F"]:
                    adj[(row, col)].add(add_tuples((row, col), dir))
                # break
                continue

            if char != ".":
                for dir in m[char]:
                    adj[(row, col)].add(add_tuples((row, col), dir))
    
    farthest = 0
    # start = (1, 1)
    # start = (2, 0)
    # start = (90, 62)
    v = set()
    q = deque([start])
    dists = {start: 0}
    curr = start

    while q:
        curr = q.popleft()
        # print("curr", curr)
        v.add(curr)

        for child in adj[curr]:
            # print("child", child)
            if child not in v and child not in q and child[0] >= 0 and child[0] < len(lines) and child[1] >= 0 and child[1] < len(lines[0]):
                # print("Here")
                q.append(child)
                dists[child] = dists[curr] + 1
    # print(v)

    # print(start)
    # print(adj)
    # print("VisitEd", v)
    # print(dists)


    return max(dists.values())


def print_map(lines, visited):
    for i, row in enumerate(lines):
        for j, col in enumerate(row):
            if (i, j) in visited:
                print(f"\033[91m{col}\033[0m", end="")
            else:
                print(col, end="")
        print()
    print()


def is_valid_position(expanded_map, pos):
    y = expanded_map[pos[0]][pos[1]]
    # print(f"{y} at {pos}") if y == "." else None
    # print(pos)
    # print(pos, len(expanded_map), len(expanded_map[0]))
    if expanded_map[pos[0]][pos[1]] not in ".#":
        # print(f"{y} ({pos}) not in .#")
        # print()
        return False
    # Up
    # print("checking up")
    temp = add_tuples(pos, (-1, 0))
    if (temp[0] >= 0 and temp[0] < len(expanded_map) and temp[1] >= 0 and temp[1] < len(expanded_map[0])):
        # print(1)
        # return False
        if expanded_map[temp[0]][temp[1]] in "|F7":
            # print("UP")
            return False

    # Down
    # print("checking down")
    temp = add_tuples(pos, (1, 0))
    if (temp[0] >= 0 and temp[0] < len(expanded_map) and temp[1] >= 0 and temp[1] < len(expanded_map[0])):
        # print(2)
        if expanded_map[temp[0]][temp[1]] in "|JL":
            # print("DoWn")
            return False

    # Left
    # print("checking left")
    temp = add_tuples(pos, (0, -1))
    # print(pos, (0, -1), temp)
    if (temp[0] >= 0 and temp[0] < len(expanded_map) and temp[1] >= 0 and temp[1] < len(expanded_map[0])):
        # print(f"{temp[0] >= 0}")
        # print(f"{temp[0] < len(expanded_map)}")
        # print(f"{temp[1] >= 0}")
        # print(f"{temp[1] < len(expanded_map[0])}")
        # print(3)
        if expanded_map[temp[0]][temp[1]] in "-LF":
            # print("left")
            return False

    # Right
    # print("checking right")
    temp = add_tuples(pos, (0, 1))
    if (temp[0] >= 0 and temp[0] < len(expanded_map) and temp[1] >= 0 and temp[1] < len(expanded_map[0])):
        # print(4)
        if expanded_map[temp[0]][temp[1]] in "-7J":
            # print("right")
            return False

    return True


def solve_part_2():
    ans = 0
    adj = defaultdict(set)
    m = {
        "F": [(1, 0), (0, 1)],
        "7": [(0, -1), (1, 0)],
        "|": [(-1, 0), (1, 0)],
        "-": [(0, -1), (0, 1)],
        "L": [(-1, 0), (0, 1)],
        "J": [(-1, 0), (0, -1)],
    }
    start = None
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "S":
                print("FOUND S")
                start = (row, col)
                for dir in m["F"]:
                # for dir in m["F"]:
                    adj[(row, col)].add(add_tuples((row, col), dir))
                # break
                continue

            if char != ".":
                for dir in m[char]:
                    adj[(row, col)].add(add_tuples((row, col), dir))
    
    v = set()
    q = deque([start])
    dists = {start: 0}
    curr = start

    while q:
        curr = q.popleft()
        v.add(curr)

        for child in adj[curr]:
            if child not in v and child not in q and child[0] >= 0 and child[0] < len(lines) and child[1] >= 0 and child[1] < len(lines[0]):
                q.append(child)
                dists[child] = dists[curr] + 1
    # print_map(lines, v)

    print("original")
    for l in lines:
        print(l)
    print()

    print("visited")
    print_map(lines, v)

    new_lines = []
    for i, row in enumerate(lines):
        temp_row = []
        for j, col in enumerate(row):
            if (i, j) in v:
                temp_row.append(col)
            else:
                temp_row.append(".")
        new_lines.append(''.join(temp_row))
            
    print("pruned w/ visited")
    for l in new_lines:
        print(l)
    print()


    EXPAND = "#"
    expanded_map = []
    # Top row
    expanded_map.append(EXPAND*(len(new_lines[0]*2)+1))
    for l in new_lines:
        expanded_map.append(EXPAND + ''.join([f"{c}{EXPAND}" for c in l]))
        expanded_map.append(EXPAND*(len(l*2)+1))
        # expanded_map.append(''.join([f"{c}{EXPAND}" for c in l]))
        # expanded_map.append(EXPAND*(len(l*2)))

    for l in expanded_map:
        print(l)
    print()


    # start = (0, 0)
    starts = []
    # Top
    starts.extend((0, x) for x in range(len(expanded_map[0])))
    # print(starts)
    # Bottom
    starts.extend((len(expanded_map)-1, x) for x in range(len(expanded_map[0])))
    # Left
    starts.extend((x, 0) for x in range(len(expanded_map)))
    # Right
    starts.extend((x, len(expanded_map[0])-1) for x in range(len(expanded_map)))

    # print(starts)

    v2 = set()
    for start in starts:

        # start = (12, 4)
        q = deque([start])
        while q:
            curr = q.popleft()
            v2.add(curr)

            dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            nexts = [add_tuples(curr, d) for d in dirs]
            for child in nexts:
                # input(f"Child={child}, {expanded_map[child[0]][child[1]]}")
                # print("child", child)
                # print(is_valid_position(expanded_map, child))
                # if child in [(5,5),(6,5),(5,13),(6,13)]:
                #     print("HERERERERKLJELKRJERL", child)
                #     print(child not in v2, child not in q, child[0] >= 0, child[0] < len(expanded_map), child[1] >= 0,
                #           child[1] < len(expanded_map[0]), is_valid_position(expanded_map, child))
                # print()
                if child not in v2 and child not in q and\
                    child[0] >= 0 and child[0] < len(expanded_map) and\
                    child[1] >= 0 and child[1] < len(expanded_map[0]) and\
                        is_valid_position(expanded_map, child):
                    
                    # print("here?????????????????")
                    # print(child, len(expanded_map), len(expanded_map[0]))
                    # input(f"adding {child} ({expanded_map[child[0]][child[1]]})")
                    # print()
                    q.append(child)
                    # print_map(expanded_map, v2)
                    # input(f"Moving from {curr} to {child}")
                    # dists[child] = dists[curr] + 1
                # print()

    # print_map(expanded_map, v2)
    # filtered_map = [expanded_map[x[0]][x[1]] for x in v2 if expanded_map[x[0]][x[1]] == "."]
    # print()
    # print()
    # print(v)
    # print()
    # print(filtered_map)
    # print(expanded_map)
    # for x in v:
    #     print(expanded_map[x[0]][x[1]])

    # print(start)
    # print(adj)
    # print("VisitEd", v)
    # print(dists)
    min_row = min(v2, key=lambda x: x[0])[0]
    max_row = max(v2, key=lambda x: x[0])[0]

    min_col = min(v2, key=lambda x: x[1])[1]
    max_col = max(v2, key=lambda x: x[1])[1]
    # print((min_row, min_col))
    # print((max_row, max_col))
    row_range = range(min_row, max_row+1)
    col_range = range(min_col, max_col+1)
    possible_range = set()
    for r in row_range:
        for c in col_range:
            possible_range.add((r, c))


    # # print(len(possible_range))
    possible_range = possible_range - v2
    temp = [expanded_map[x[0]][x[1]] for x in possible_range if expanded_map[x[0]][x[1]] == "."]
    print(len(temp))

    print_map(expanded_map, v2)
    # outside_start = (min_row-1, min_col-1)
    # q2 = deque([outside_start])
    # # while q2:
    # #     curr = q2.popleft()
    # #     dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    # #     for d in dirs:
    # #         next = add_tuples(curr, d)
    # #         if next not in v:
    # # print(len(possible_range))
    # # print(possible_range)

    return len(temp)



# 13591
print(f"Part 1 answer: {solve_part_1()}")
# < 489
print(f"Part 2 answer: {solve_part_2()}")

