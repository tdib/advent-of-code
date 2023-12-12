# https://adventofcode.com/2023/day/13

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

cache = {}
def get_num_valid_arrangements(s, nums, curr_len=0):
    key = (s, nums, curr_len)
    if key in cache:
        return cache[key]

    if len(s) == 0:
        return int((len(nums) == 1 and curr_len == nums[0]) or (curr_len == 0 and len(nums) == 0))

    if sum(nums) == 0:
        return "#" not in s
    
    curr = s[0]

    if curr_len == nums[0]:
        # We are about to hit something that would make us go over
        if curr == "#":
            cache[key] = 0
            return cache[key]
        # We can reset
        else:
            cache[key] = get_num_valid_arrangements(s[1:], nums[1:])
            return cache[key]

    if curr == "#":
        cache[key] = get_num_valid_arrangements(s[1:], nums, curr_len + 1)
        return cache[key]
    
    if curr == ".":
        # We have not hit enough springs
        if curr_len > 0:
            cache[key] = 0
        # We HAVE hit enough springs
        else:
            cache[key] = get_num_valid_arrangements(s[1:], nums, 0)
        return cache[key]
    
    if curr == "?":
        # We are currently counting something
        if curr_len > 0:
            cache[key] = get_num_valid_arrangements(s[1:], nums, curr_len + 1)
        # We are not counting anything, so lets trial both a . and #
        else:
            cache[key] = get_num_valid_arrangements(s[1:], nums, 0) + get_num_valid_arrangements(s[1:], nums, curr_len + 1)
        return cache[key]

def solve(n):
    ans = 0
    for line in lines:
        s = line.split()
        record = "?".join([s[0]] * n)
        nums = tuple(map(int, s[1].split(","))) * n
        ans += get_num_valid_arrangements(record, nums)

    return ans

def solve_part_1():
    return solve(1)

def solve_part_2():
    return solve(5)

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")