from itertools import groupby; print(sum(sorted([sum(x) for x in [list(g) for k, g in groupby([int(line.strip()) if line != '\n' else None for line in open('input.txt', 'r').readlines()], lambda x: x != None) if k]])[-3:]))