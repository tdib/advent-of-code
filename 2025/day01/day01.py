# https://adventofcode.com/2025/day/1

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def solve_part_1():
    ans = 0
    dial = 50
    for line in lines:
        num = int(line[1:])
        if line.startswith("L"):
            dial -= num
        else:
            dial += num
        dial %= 100
        if dial == 0:
            ans += 1
    return ans


def solve_part_2():
    ans = 0
    dial = 50
    for line in lines:
        num = int(line[1:])
        prev_dial = dial
        if line.startswith("L"):
            dial -= num
        else:
            dial += num

        # For larger rotations (above 100), we can guarantee passing 0, n times
        ans += num // 100
        # Mod the rotation by 100 so we will always be dealing with the remainder after guaranteed rotations
        num %= 100
        if prev_dial != 0 and (
            dial % 100 == 0
            or (line.startswith("R") and (prev_dial + num) % 100 != prev_dial + num)
            or (line.startswith("L") and (prev_dial - num) % 100 != prev_dial - num)
        ):
            ans += 1
        dial %= 100
    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
