# https://adventofcode.com/2023/day/18
from collections import deque, defaultdict
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
def solve(is_part_one):
    points = []
    boundary = 1
    curr_row = 0
    curr_col = 0
    for line in lines:
        if is_part_one:
            p1_map = {
                "L": (0, -1),
                "R": (0, 1),
                "U": (-1, 0),
                "D": (1, 0)
            }
            # We don't care about hex
            dir, dist, _ = line.split()
            dir = p1_map[dir]
            dist = int(dist)
            # Add this current boundary to the tracking
            boundary += dist
        else:
            p2_map = {
                0: RIGHT,
                1: DOWN,
                2: LEFT,
                3: UP,
            }
            # We only care about the hex value
            _, _, hex = line.split()
            # Extract the value out of the brackets
            hex = hex[2:-1]
            # Convert hex to decimal
            dist = int(hex[:-1], 16)
            # Map last char
            dir = p2_map[int(hex[-1])]
            # Add this current boundary to the tracking
            boundary += dist

        # Track which direction our current position moves to -
        # could be more concise, but kept like this for readability
        if dir == UP: curr_row -= dist
        elif dir == DOWN: curr_row += dist
        elif dir == LEFT: curr_col -= dist
        elif dir == RIGHT: curr_col += dist

        # Add out new point to 
        points.append((curr_row, curr_col))
    
    # do a lil
    # https://en.wikipedia.org/wiki/Shoelace_formula
    total = 0
    for (r1, c1), (r2, c2) in zip(points, [*points[1:], points[0]]):
        total += r1 * c2 - c1 * r2
    
    # Our area is only for the inside of our boundary, so we must add the boundary
    # This acts as if we are expanding our area in each direction by 1
    total = abs(total) + boundary
    # We finish off the shoelace formula by dividing by 2
    total //= 2

    # Add one so the test input works ¯\_(ツ)_/¯
    return total + 1


def solve_part_1():
    return solve(is_part_one = True)

def solve_part_2():
    return solve(is_part_one = False)

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

