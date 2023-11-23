# https://adventofcode.com/2015/day/3

with open("input.txt") as f:
    line = list(map(str.strip, f.readline()))

def add(a, b):
    return (a[0]+b[0], a[1]+b[1])

m = {
    '^': (0, 1),
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, -1)
}

def solve_part_1():
    santa = (0, 0)
    v = {(0, 0)}
    for c in line:
        santa = add(santa, m[c])
        v.add(santa)
    return len(v)

def solve_part_2():
    santa = (0, 0)
    robo = (0, 0)
    v = {(0, 0)}
    for i, c in enumerate(line):
        if i % 2 == 0:
            santa = add(santa, m[c])
            v.add(santa)
        else:
            robo = add(robo, m[c])
            v.add(robo)
    return len(v)

print(f'Part 1 answer {solve_part_1()}')
print(f'Part 2 answer {solve_part_2()}')
