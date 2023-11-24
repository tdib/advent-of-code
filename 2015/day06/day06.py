# https://adventofcode.com/2015/day/6
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def solve_part_1():
    DIM = 1000
    m = [[False for _ in range(DIM)] for _ in range(DIM)]
    d = {
        'toggle': lambda x: not x,
        'turn off': lambda _: False,
        'turn on': lambda _: True
    }
    r = r'(toggle|turn off|turn on) (\d+),(\d+) through (\d+),(\d+)'
    for line in lines:
        # Extract info
        matches = re.findall(r, line)[0]
        action = d[matches[0]]
        row1, col1 = map(int, matches[1:3])
        row2, col2 = map(int, matches[3:])

        # Perform action on relevant range
        for row in range(row1, row2+1):
            for col in range(col1, col2+1):
                m[row][col] = action(m[row][col])

    # Count true values
    return sum(sum(row) for row in m)

def solve_part_2():
    DIM = 1000
    m = [[0 for _ in range(DIM)] for _ in range(DIM)]
    d = {
        'toggle': lambda x: x + 2,
        'turn off': lambda x: max(0, x - 1),
        'turn on': lambda x: x + 1
    }
    r = r'(toggle|turn off|turn on) (\d+),(\d+) through (\d+),(\d+)'
    for line in lines:
        # Extract info
        matches = re.findall(r, line)[0]
        action = d[matches[0]]
        row1, col1 = map(int, matches[1:3])
        row2, col2 = map(int, matches[3:])

        # Perform action on relevant range
        for row in range(row1, row2+1):
            for col in range(col1, col2+1):
                m[row][col] = action(m[row][col])

    # Calculate total sum of every element
    return sum(sum(row) for row in m)

print(f'Part 1 answer: {solve_part_1()}')
print(f'Part 2 answer: {solve_part_2()}')

