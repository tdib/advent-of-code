# https://adventofcode.com/2023/day/13
from functools import cache

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

@cache
def get_num_valid_arrangements(s, nums, curr_len=0):
    if not s:
        return not nums and not curr_len
    
    n = 0
    if s[0] in "#?":
        n += get_num_valid_arrangements(s[1:], nums, curr_len + 1)
    if s[0] in ".?" and (nums and nums[0] == curr_len or not curr_len):
        n += get_num_valid_arrangements(s[1:], nums[1:] if curr_len else nums)
    
    return n

def solve(n):
    ans = 0
    for line in lines:
        s = line.split()
        record = "?".join([s[0]] * n) + "."
        nums = tuple(map(int, s[1].split(","))) * n
        ans += get_num_valid_arrangements(record, nums)

    return ans

def solve_part_1():
    return solve(1)

def solve_part_2():
    return solve(5)

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")