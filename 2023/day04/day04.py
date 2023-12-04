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
    m = defaultdict(lambda: int(0))
    for line in lines:
        card_id, num_winning_nums = parse(line)

        # Keep track of the next n cards (that we must duplicate)
        for i in range(card_id+1, card_id+num_winning_nums+1):
            m[i] += 1

        # For every duplicate
        while m[card_id]:
            # Calculate the next duplicates from the curent win
            for i in range(card_id+1, card_id+num_winning_nums+1):
                m[i] += 1
            
            # Decrement because we just handled one instance of this dupe
            m[card_id] -= 1
            
            # Count the current duplicate
            ans += 1
        
        # Count the current card (does not matter whether it wins or not)
        ans += 1

    return ans

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

