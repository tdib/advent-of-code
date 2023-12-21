# https://adventofcode.com/2023/day/21
from collections import deque

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def add_tuples(a, b):
    return (a[0] + b[0], a[1] + b[1])

def within_bounds(pos):
    row, col = pos
    return row >= 0 and row < len(lines) and col >= 0 and col < len(lines[0])

def print_map(m, visited):
    for r, row in enumerate(m):
        for c in range(len(row)):
            if (r, c) in visited:
                print(VISITED, end="")
            else:
                print(m[r][c], end="")
        print()
    print()

GARDEN = "."
ROCK = "#"
VISITED = "O"
START = "S"
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
def solve_part_1():
    curr = None
    rocks = set()
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch == ROCK:
                rocks.add((r, c))
            elif ch == START:
                curr = (r, c)

    q = deque([curr])
    step = 0
    NUM_STEPS = 64
    num_steps_even = NUM_STEPS % 2 == 0

    all_v = set([curr])
    v = set([curr]) if num_steps_even else set()

    new_q = q
    while step < NUM_STEPS:
        q = new_q.copy()
        step += 1
        while q:
            curr_pos = q.popleft()

            for d in DIRECTIONS:
                next_pos = add_tuples(curr_pos, d)
                if within_bounds(next_pos) and next_pos not in rocks and next_pos not in all_v:
                    new_q.append(next_pos)
                    all_v.add(next_pos)
                    if (num_steps_even and step % 2 == 0) or (not num_steps_even and step % 2 != 0):
                        v.add(next_pos)

    return len(v)


def solve_part_2():
    ans = 0
    for line in lines:
        pass
    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

