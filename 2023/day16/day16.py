# https://adventofcode.com/2023/day/16
from collections import deque, defaultdict
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
ENERGISED = "#"
EMPTY = "."

def print_map(m, obstacles, energised=set()):
    height = len(m)
    width = len(m[0])
    for i in range(height):
        for j in range(width):

            if (i, j) in energised:
                print(ENERGISED, end="")
            elif (i, j) in obstacles:
                print(lines[i][j], end="")
            else:
                print(EMPTY, end="")
        print()
    print()

def within_bounds(pos):
    row, col = pos
    return row >= 0 and row < len(lines) and col >= 0 and col < len(lines[0])

def add_tuples(a, b):
    return (a[0] + b[0], a[1] + b[1])

m = {
    "/": [(UP, RIGHT), (LEFT, DOWN), (RIGHT, UP), (DOWN, LEFT)],
    "\\": [(UP, LEFT), (RIGHT, DOWN), (LEFT, UP), (DOWN, RIGHT)],
    "-": [(DOWN, LEFT), (DOWN, RIGHT), (UP, LEFT), (UP, RIGHT), (RIGHT, RIGHT), (LEFT, LEFT)],
    "|": [(LEFT, DOWN), (LEFT, UP), (RIGHT, UP), (RIGHT, DOWN), (UP, UP), (DOWN, DOWN)],
    ".": [(LEFT, LEFT), (RIGHT, RIGHT), (UP, UP), (DOWN, DOWN)]
}

def solve_part_1():
    START = ((0, 0), RIGHT)
    curr_beams = [START]
    obstacles = set()
    energised = set()
    for row_idx, line in enumerate(lines):
        for col_idx, ch in enumerate(line):
            if ch in m:
                obstacles.add((row_idx, col_idx))

    v = set()
    has_change = True
    while len(curr_beams) and has_change:
        temp = []
        has_change = False
        for curr_beam in curr_beams[:]:
            if curr_beam in v:
                continue
            else:
                has_change = True
                v.add(curr_beam)
            curr_pos, curr_dir = curr_beam
            energised.add(curr_pos)

            curr_symbol = lines[curr_pos[0]][curr_pos[1]]


            dir_map = m[curr_symbol]
            next_dir = [d[1] for d in dir_map if d[0] == curr_dir]
            if len(next_dir) == 2:
                for n in next_dir:
                    next_pos = add_tuples(curr_pos, n)
                    if within_bounds(next_pos):
                        temp.append((next_pos, n))
            else:
                next_dir = next_dir[0]
                next_pos = add_tuples(curr_pos, next_dir)
                if within_bounds(next_pos):
                    temp.append((next_pos, next_dir))
            curr_beams = temp

    return len(energised)


def solve_part_2():
    obstacles = set()
    for row_idx, line in enumerate(lines):
        for col_idx, ch in enumerate(line):
            if ch in m:
                obstacles.add((row_idx, col_idx))

    top_starts = [((0, col), DOWN) for col in range(len(lines[0]))]
    bot_starts = [((len(lines)-1, col), UP) for col in range(len(lines[0]))]
    left_starts = [((row, 0), RIGHT) for row in range(len(lines))]
    right_starts = [((row, len(lines[0])-1), LEFT) for row in range(len(lines))]
    starts = [*top_starts, *bot_starts, *left_starts, *right_starts]

    max_energised = 0
    for start in starts:
        v = set()
        energised = set()
        has_change = True
        curr_beams = [start]
        while has_change:
            temp = []
            has_change = False
            for curr_beam in curr_beams[:]:
                if curr_beam in v:
                    continue
                else:
                    has_change = True
                    v.add(curr_beam)
                curr_pos, curr_dir = curr_beam
                energised.add(curr_pos)

                curr_symbol = lines[curr_pos[0]][curr_pos[1]]

                dir_map = m[curr_symbol]
                next_dir = [d[1] for d in dir_map if d[0] == curr_dir]
                for n in next_dir:
                    next_pos = add_tuples(curr_pos, n)
                    if within_bounds(next_pos):
                        temp.append((next_pos, n))
                curr_beams = temp
        max_energised = max(max_energised, len(energised))

    return max_energised


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

