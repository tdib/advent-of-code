# https://adventofcode.com/2023/day/13
from collections import deque, defaultdict
import itertools
import re
import functools

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def is_valid(arrangement, nums):
    damaged_re = r"(\#+)"
    damaged = re.findall(damaged_re, arrangement)
    damaged_lens = tuple(map(len, damaged))
    return damaged_lens == nums

def generate_combinations(template, chars):
    # Find the positions of the wildcards
    wildcard_positions = [pos for pos, char in enumerate(template) if char == "?"]

    # Generate all combinations for the wildcards
    for combo in itertools.product(chars, repeat=len(wildcard_positions)):
        # Create a list from the template to modify it
        result = list(template)

        # Replace the wildcards with the characters from the combination
        for pos, replacement in zip(wildcard_positions, combo):
            result[pos] = replacement

        # Yield the joined string
        yield ''.join(result)


def solve_part_1():
    ans = 0
    for line in lines:
        s = line.split()
        record = s[0]
        nums = list(map(int, s[1].split(",")))

        combinations = list(generate_combinations(record, [".", "#"]))
        for c in combinations:
            if get_num_valid_arrangements(c, nums):
                ans += 1

    return ans


# cache = {}
# def get_num_valid_arrangements(arrangement: str, nums: tuple, curr_len: int = 0, built=""):
#     x = f"{built}{arrangement}"
#     key = (arrangement, nums, curr_len)
#     if key in cache:
#         print(x, cache[key], "(cached)")
#         return cache[key]

#     # We have reached the end of the string so if there are no more
#     # numbers to process, this is a valid string
#     if len(arrangement) == 0:
#         cache[key] = 1 if ((len(nums) == 1 and curr_len == nums[0]) or (curr_len == 0 and len(nums) == 0)) else 0
#         # print(x, cache[key], "x")
#         return cache[key]


#     # If we have no numbers left to process, then checking if we have any
#     # remaining "#"s will tell us whether we are in a valid state
#     if len(nums) == 0:
#         cache[key] = int("#" not in arrangement)
#         return cache[key]

#     curr = arrangement[0]

#     # In the case where the current block meets the expected size
#     if curr_len == nums[0]:
#         # We are about to hit something that would make us go over
#         if curr == "#":
#             cache[key] = 0
#             return cache[key]
#         # We can reset
#         else:
#             cache[key] = get_num_valid_arrangements(arrangement[1:], nums[1:], 0, f"{built}.")
#             return cache[key]

#     # encounter a ?
#     # this is where we diverge and must test multiple cases
#     if curr == "?":
#         # for the case where we place a ".", nums does not get shifted because we are resetting
#         # print(f"at {arrangement} ({x}), testing both combos")
#         cache[key] = get_num_valid_arrangements(arrangement[1:], nums, curr_len+1, f"{built}#") +\
#                 get_num_valid_arrangements(arrangement[1:], nums, 0, f"{built}.")
#         # cache[key] = get_num_valid_arrangements(arrangement[1:], nums, 0, f"{built}.") + \
#         #         get_num_valid_arrangements(arrangement[1:], nums, curr_len+1, f"{built}#")

#     # encounter a #
#     if curr == "#":
#         cache[key] = get_num_valid_arrangements(arrangement[1:], nums, curr_len+1, f"{built}#")

#     # encounter a .
#     if curr == ".":
#         cache[key] = get_num_valid_arrangements(arrangement[1:], nums, 0, f"{built}.")

#     # print(x, cache[key])
#     return cache[key]

# cache = {}
# n = ()
# def get_num_valid_arrangements(s, nums, curr_len=0, b=""):
#     x = b+s
#     key = (s, nums, curr_len, b)

#     if key in cache:
#         print("Cache hit")
#         return cache[key]

#     # arrangement is empty
#     if len(s) == 0:
#         # print(x, og_nums)
#         return is_valid(x, n)
#         print(is_valid(x, og_nums))
#         print("returning", x, int((len(nums) == 1 and curr_len == nums[0]) or (curr_len == 0 and len(nums) == 0)))
#         return int((len(nums) == 1 and curr_len == nums[0]) or (curr_len == 0 and len(nums) == 0))


#     # nums is empty
#     if len(nums) == 0:
#         # print(x, og_nums)
#         return is_valid(x, n)
#         print("ret", x, int("#" not in s))
#         return int("#" not in s)
    
#     curr = s[0]
#     if curr_len == nums[0]:
#         if curr == "#":
#             return 0
#         else:
#             cache[key] = get_num_valid_arrangements(s[1:], nums[1:], 0, b+".")
#             return cache[key]
#             # return get_num_valid_arrangements(s[1:], nums[1:], 0, b+".")

#     # normal cases
#     if curr == ".":
#         cache[key] = get_num_valid_arrangements(s[1:], nums, 0, b+".")
#         # return get_num_valid_arrangements(s[1:], nums, 0, b+".")
#     elif curr == "#":
#         cache[key] = get_num_valid_arrangements(s[1:], nums, curr_len + 1, b+"#")
#         # return get_num_valid_arrangements(s[1:], nums, curr_len + 1, b+"#")
#     elif curr == "?":
#         cache[key] = get_num_valid_arrangements(s[1:], nums, 0, b+".") + get_num_valid_arrangements(s[1:], nums, curr_len + 1, b+"#")
#         # return get_num_valid_arrangements(s[1:], nums, 0, b+".") + get_num_valid_arrangements(s[1:], nums, curr_len + 1, b+"#")

#     return cache[key]


###########################
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
##############################


def solve_part_2():
    global n
    ans = 0
    N = 5
    for line in lines:
        s = line.split()
        record = "?".join([s[0]] * N)
        nums = tuple(map(int, s[1].split(","))) * N
        print(record, nums)
        e = get_num_valid_arrangements(record, nums)
        n = nums
        print(e)
        print()
        cache = {}
        ans += e

        # break

    return ans


# print(f"Part 1 answer: {solve_part_1()}")
# > 7084
# < 103311982353087846
print(f"Part 2 answer: {solve_part_2()}")

# a = "?.#"
# b = [1, 1]

# print()
# print(a, b)
# print(get_num_valid_arrangements(a, b))

a = "???.#.##."
b = (1,1,2)
print()
print(a, b)
n = b
print(get_num_valid_arrangements(a, b))
