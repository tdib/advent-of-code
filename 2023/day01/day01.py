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
            # Both matches will be strings, so we can use + to concatenate them and then cast to int
            ans += int(matches[0] + matches[-1])
    return ans


def solve_part_2():
    ans = 0
    nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for line in lines:
        # Find all instances of any of the digit strings, or real digits
        matches = re.findall(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line)

        # Find the leftmost and rightmost digits/strings by using the matches found above
        l = matches[0]
        r = matches[-1]

        # If we have a string like "one", we must convert it to its value. We do this by using
        # the array index + 1 (to offset for 0-based indexing), e.g. "one" is at index 0, "two"
        # is at 1, and so on.
        l = int(l) if l.isdigit() else nums.index(l) + 1
        r = int(r) if r.isdigit() else nums.index(r) + 1

        # We can use this method if we have two ints. This essentially takes the leftmost value
        # and places it in the 10s column where it belongs, and then adds the rightmost (in the ones)
        ans += 10 * l + r
        # We can use this method if we have not casted our values to ints,
        # e.g. if we had something like "1" as opposed to 1
        # ans += int(f"{l}{r}")

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

