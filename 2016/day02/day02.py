# https://adventofcode.com/2016/day/2

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

m = {
    "L": (0, -1),
    "R": (0, 1),
    "U": (-1, 0),
    "D": (1, 0)
}


def add(a, b):
    return [a[0]+b[0], a[1]+b[1]]


def traverse_keypad(keypad, start_pos):
    ans = []
    curr = start_pos

    for line in lines:
        for dir_char in line:
            pre = curr
            direction = list(m[dir_char])
            curr = add(curr, direction)
            # Check the bounds and limit our movement to stay within the keypad
            # Up
            if curr[0] < 0:
                curr[0] = 0
            # Down
            if curr[0] >= len(keypad):
                curr[0] = len(keypad) - 1
            # Left
            if curr[1] < 0:
                curr[1] = 0
            # Right
            if curr[1] >= len(keypad[0]):
                curr[1] = len(keypad[0]) - 1
            # Not a specific bound, but a bound set by None. Encountering a None
            # value means we should set the value back to what it was before hitting it
            if keypad[curr[0]][curr[1]] == None:
                curr = pre
        else:
            ans.append(keypad[curr[0]][curr[1]])

    return "".join(map(str, ans))

def solve_part_1():
    keypad = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    curr = [1, 1]
    return traverse_keypad(keypad, curr)


def solve_part_2():
    keypad = [
        [None, None, 1, None, None],
        [None, 2, 3, 4, None],
        [5, 6, 7, 8, 9],
        [None, "A", "B", "C", None],
        [None, None, "D", None, None]
    ]
    curr = [2, 0]
    return traverse_keypad(keypad, curr)


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

