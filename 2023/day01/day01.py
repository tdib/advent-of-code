# https://adventofcode.com/2023/day/1
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def solve_part_1():
    ans = 0
    for line in lines:
        matches = re.findall(r"\d", line)
        # Check just to ensure no errors happen with inputs not containing numbers (i.e. test data)
        if matches:
            ans += int(matches[0] + matches[-1])
    return ans


def solve_part_2():
    ans = 0
    nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for line in lines:
        # Find the digit numbers
        matches = re.findall(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line)

        l = matches[0]
        r = matches[-1]

        l = int(l) if l.isdigit() else nums.index(l) + 1
        r = int(r) if r.isdigit() else nums.index(r) + 1

        ans += int(f"{l}{r}")

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

