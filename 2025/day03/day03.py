# https://adventofcode.com/2025/day/3

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def solve(n):
    ans = 0
    for line in lines:
        nums = list(map(int, line))
        highests = []
        start_idx = 0
        for i in range(n):
            nums_left = n - i
            end_idx = len(nums) - nums_left + 1
            segment = nums[start_idx:end_idx]
            highest_in_segment = max(segment)
            start_idx = nums.index(highest_in_segment, start_idx) + 1

            highests.append(highest_in_segment)
        ans += int("".join(map(str, highests)))

    return ans


def solve_part_1():
    return solve(2)


def solve_part_2():
    return solve(12)


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
