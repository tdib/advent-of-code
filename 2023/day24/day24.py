# https://adventofcode.com/2023/day/24
from util import *

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

# Thank you :) https://en.wikipedia.org/wiki/Line-line_intersection
def check_intersection(p1, p2, v1, v2):
    # First line
    l1 = (p1, add_tuples(p1, v1))
    (x1, y1), (x2, y2) = l1

    # Second line
    l2 = (p2, add_tuples(p2, v2))
    (x3, y3), (x4, y4) = l2

    denominator = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    # When the two lines are parallel or coincident, the denominator is zero.
    # We can assume we will never have coincident lines, so return False
    if denominator == 0:
        return None

    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4))/denominator
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4))/denominator

    return (px, py)

MIN_VAL = 200000000000000
MAX_VAL = 400000000000000
def solve_part_1():
    positions = []
    for line in lines:
        position, velocity = line.split(" @ ")
        px, py, _ = map(int, position.split(", "))
        vx, vy, _ = map(int, velocity.split(", "))
        positions.append(((px, py), (vx, vy)))
    
    hailstones = 0
    for i, (p1, v1) in enumerate(positions):
        for p2, v2 in positions[i+1:]:
            intersection = check_intersection(p1, p2, v1, v2)
            if intersection:
                intersect_x, intersect_y = intersection
                slope_y1 = v1[1]
                slope_y2 = v2[1]
                y1 = p1[1]
                y2 = p2[1]
                if (intersect_x >= MIN_VAL and intersect_x <= MAX_VAL and # x is within range
                    intersect_y >= MIN_VAL and intersect_y <= MAX_VAL and # y is within range
                    not ( # The intersection happened in the past
                        (slope_y1 > 0 and intersect_y <= y1) or
                        (slope_y2 > 0 and intersect_y <= y2) or
                        (slope_y1 < 0 and intersect_y >= y1) or
                        (slope_y2 < 0 and intersect_y >= y2)
                    )
                ):
                    hailstones += 1

    return hailstones

print(f"Part 1 answer: {solve_part_1()}")

