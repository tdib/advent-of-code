# https://adventofcode.com/2023/day/15
from collections import defaultdict, OrderedDict

with open("input.txt") as f:
    line = f.readlines()

def hash(s):
    curr = 0
    for ch in s:
        ascii = ord(ch)
        curr += ascii
        curr *= 17
        curr %= 256
    return curr

def solve_part_1():
    ans = 0
    global line
    lines = line[0].split(",")
    for l in lines:
        ans += hash(l)

    return ans

def solve_part_2():
    ans = 0
    global line
    h = defaultdict(OrderedDict)
    lines = line[0].split(",")
    for l in lines:
        curr = 0
        # true if =, false if -
        flag = "=" in l
        split = l.split("=" if flag else "-")
        string = split[0]
        hsh = hash(string)

        # have =
        if flag:
            val = split[1]
            # We already have this, we must replace
            if string in h[hsh].keys():
                h[hsh][string] = val
            # Just add it
            else:
                h[hsh].update({ string: val })
        # we have a -
        else:
            if string in h[hsh].keys():
                h[hsh].pop(string)

    for box_idx, box in h.items():
        if len(box) <= 0: continue
        for i, val in enumerate(box.values()):
            ans += (box_idx + 1) * (i + 1) * int(val)
        ans += curr

    return ans

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

