# https://adventofcode.com/2023/day/9
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def construct_diffs(line):
    r = r"(-?\d+)"
    nums = list(map(int, re.findall(r, line)))
    diffs = [nums]
    while not all(x == 0 for x in diffs[-1]):
        temp = []
        curr = diffs[-1]
        for i in range(1, len(curr)):
            temp.append(curr[i] - curr[i-1])
        diffs.append(temp)
    return diffs


def solve_part_1():
    ans = 0
    for line in lines:
        diffs = construct_diffs(line)
        diffs[-1].append(0)

        # Iterate from 0 diffs upwards to original history and
        # append to diffs at each stage (adding as necessary)
        for i in range(len(diffs)-2, -1, -1):
            prev = diffs[i+1][-1]
            curr = diffs[i][-1]
            diffs[i].append(prev + curr)

        # diffs[0] is the original history, and we want the last element
        ans += diffs[0][-1]

    return ans


def solve_part_2():
    ans = 0
    for line in lines:
        diffs = construct_diffs(line)
        # This doesn't have to be inserted since the whole array is 0s
        # but for completeness we will do this :)
        diffs[-1].insert(0, 0)

        # Once again iterate from our 0 diffs towards history and do what we need
        for i in range(len(diffs)-2, -1, -1):
            # This time we take the first element of each, and INSERT it instead of append
            prev = diffs[i+1][0]
            curr = diffs[i][0]
            diffs[i].insert(0, curr - prev)

        # Take the first element of our history and add to answer
        ans += diffs[0][0]

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

