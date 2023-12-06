# https://adventofcode.com/2023/day/6
from collections import deque, defaultdict
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def solve_part_1():
    ans = 1
    r = r"(\d+)"
    times = list(map(int, re.findall(r, lines[0])))
    dists = list(map(int, re.findall(r, lines[1])))
    for time, dist_to_beat in zip(times, dists):
        blah = []
        time_left = time
        curr_dist_per_ms = 0
        while time_left > 0:
            curr_dist_per_ms += 1
            time_left -= 1
            end_dist = time_left * curr_dist_per_ms
            if end_dist > dist_to_beat:
                blah.append(end_dist)
        ans *= len(blah)

    return ans


def solve_part_2():
    ans = 1
    r = r"(\d+)"
    times = re.findall(r, lines[0])
    dists = re.findall(r, lines[1])
    time = int(''.join(times))
    dist = int(''.join(dists))
    blah = []
    time_left = time
    curr_dist_per_ms = 0
    while time_left > 0:
        curr_dist_per_ms += 1
        time_left -= 1
        end_dist = time_left * curr_dist_per_ms
        if end_dist > dist:
            blah.append(end_dist)
    ans *= len(blah)

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

