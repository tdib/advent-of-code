# https://adventofcode.com/2016/day/1
import re
from collections import deque, defaultdict


with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def process_directions(is_part_2):
    v = set()
    for line in lines:
        dirs = line.split(", ")
        curr_dir_idx = 0
        curr_loc = (0, 0)
        for dir in dirs:
            rot = dir[0]
            amount = int(dir[1:])
            # Rotate clockwise by selecting the next element in the directions
            # (they are in the order up right down left)
            if rot == "R":
                curr_dir_idx = (curr_dir_idx + 1) % len(DIRECTIONS)
            # Anti-clockwise rotation by going the opposite direction
            else:
                curr_dir_idx = (curr_dir_idx - 1) % len(DIRECTIONS)
            
            # Travel x grid locations in the given direction
            for _ in range(amount):
                curr_loc = add(curr_loc, DIRECTIONS[curr_dir_idx])

                if is_part_2:
                    # If we've seen this state before we can return now
                    if curr_loc in v:
                        return sum([abs(curr_loc[0]), abs(curr_loc[1])])
                    # Otherwise we'll add it to visited and move on
                    else:
                        v.add(curr_loc)
    return sum([abs(curr_loc[0]), abs(curr_loc[1])])


def solve_part_1():
    return process_directions(is_part_2=False)


def solve_part_2():
    return process_directions(is_part_2=True)


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
