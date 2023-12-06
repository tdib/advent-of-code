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
    for time_left, dist_to_beat in zip(times, dists):
        winning_dists = []
        curr_dist_per_ms = 0
        while time_left > 0:
            curr_dist_per_ms += 1
            time_left -= 1
            if (end_dist := time_left * curr_dist_per_ms) > dist_to_beat:
                winning_dists.append(end_dist)
        ans *= len(winning_dists)

    return ans


def solve_part_2():
    ans = 1
    r = r"(\d+)"
    time_left = int(''.join(re.findall(r, lines[0])))
    dist_to_beat = int(''.join(re.findall(r, lines[1])))
    winning_dists = []
    curr_dist_per_ms = 0
    while time_left > 0:
        curr_dist_per_ms += 1
        time_left -= 1
        if (end_dist := time_left * curr_dist_per_ms) > dist_to_beat:
            winning_dists.append(end_dist)
    ans *= len(winning_dists)

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

