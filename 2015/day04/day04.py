# https://adventofcode.com/2015/day/4
from hashlib import md5

line = 'iwrupvqb'

part_1_found = False
i = 0
while True:
    inp = line + str(i)
    if md5(inp.encode()).hexdigest().startswith('0'*6):
        print(f'Part 2 answer {i}')
        break
    elif md5(inp.encode()).hexdigest().startswith('0'*5) and not part_1_found:
        print(f'Part 1 answer {i}')
        part_1_found = True
    i += 1
