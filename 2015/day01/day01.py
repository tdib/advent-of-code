# https://adventofcode.com/2015/day/1

with open("/Users/dib/dev/advent-of-code/2015/day01/input.txt") as f:
    line = list(map(str.strip, f.readline()))

count = 0
first_basement = None
for i, c in enumerate(line):
    count += 1 if c == '(' else -1
    if count < 0 and not first_basement:
        first_basement = i + 1

print(f'Part 1 answer: {count}')
print(f'Part 2 answer: {first_basement}')
