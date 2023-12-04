# https://adventofcode.com/2023/day/4
from collections import deque, defaultdict
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def parse(line):
    # Find card id (left of ":")
    s = line.split(":")
    card_id = int(s[0].split()[1])

    # Find the winning numbers and our picks
    s = s[1].split("|")
    winning = set(map(int, s[0].split()))
    mine = set(map(int, s[1].split()))

    # Length of intersection between our picks and the winning numbers
    # will be the number of matches
    intersection = winning.intersection(mine)
    num_winning_nums = len(intersection)

    return card_id, num_winning_nums


def solve_part_1():
    ans = 0
    for line in lines:
        _, num_winning_nums = parse(line)

        if num_winning_nums:
            ans += 1 << num_winning_nums - 1
        
    return ans

def solve_part_2():
    ans = 0
    m = defaultdict(lambda: 1)
    for line in lines:
        card_id, num_winning_nums = parse(line)

        # Each of the next n elements should have as many copies
        # as we do of the current element - e.g. if we have 3 copies
        # of the current card, the next element will end up being copied 3 times
        for i in range(card_id+1, card_id+num_winning_nums+1):
            m[i] += m[card_id]
        
        ans += m[card_id]
        
    return ans

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

