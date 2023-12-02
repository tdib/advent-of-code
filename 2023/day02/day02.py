# https://adventofcode.com/2023/day/2
from collections import deque, defaultdict
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def solve_part_1():
    MAX_RED = 12
    MAX_GREEN = 13
    MAX_BLUE = 14
    ans = 0
    possibles = []
    for line in lines:
        colours = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        split = line.split(":")
        game_id = split[0].split()[-1]
        sets = split[1].split(";")
        print("gmae id", game_id)
        # print(sets)
        for s in sets:
            print(s)
            s = list(map(str.strip, s.split(",")))
            for c in s:
                num, colour = c.split()
                if int(num) > colours[colour]:
                    colours[colour] = int(num)
                # if int(num) > mins[colour]:
                #     mins[colour] = int(num)
            
        
        blah = colours["red"] * colours["green"] * colours["blue"]
        ans += blah
        print("blah", blah)
        # print(colours)
        print()


                # print(num, colour)
        if colours["red"] > MAX_RED:
            continue
        if colours["blue"] > MAX_BLUE:
            continue
        if colours["green"] > MAX_GREEN:
            continue
    
        possibles.append(int(game_id))

    print(possibles)
    print(ans)
    return sum(possibles)


def solve_part_2():
    ans = 0
    for line in lines:
        pass


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

