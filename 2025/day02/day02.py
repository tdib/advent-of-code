# https://adventofcode.com/2025/day/2

with open("input.txt") as f:
    line = f.readline()


def solve_part_1():
    ans = 0
    # Convert input into list of tuple ranges like [(1, 5), (10-12), ...]
    ranges = [tuple(map(int, r.split("-"))) for r in line.split(",")]
    for start, end in ranges:
        for i in range(start, end + 1):
            s = str(i).lstrip("0")
            mid_index = len(s) // 2
            first_half = s[:mid_index]
            second_half = s[mid_index:]
            if first_half == second_half:
                ans += i

    return ans


def solve_part_2():
    ans = 0
    # Convert input into list of tuple ranges like [(1, 5), (10-12), ...]
    ranges = [tuple(map(int, r.split("-"))) for r in line.split(",")]
    for start, end in ranges:
        for number in range(start, end + 1):
            s = str(number).lstrip("0")
            if (s + s).find(s, 1) != len(s):
                ans += number

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
