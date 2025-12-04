# https://adventofcode.com/2025/day/3

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def solve_part_1():
    ans = 0
    for line in lines:
        nums = list(map(int, line))
        highest_num = max(nums)
        highest_num_index = nums.index(highest_num)

        # Scan left
        highest_to_left = -1
        for num in nums[:highest_num_index]:
            temp = int(f"{num}{highest_num}")
            if temp > highest_to_left:
                highest_to_left = temp

        # Can't scan right if the highest number is the last
        if highest_num_index == len(nums):
            ans += highest_to_left
            continue

        # Scan right
        highest_to_right = -1
        for num in nums[highest_num_index + 1 :]:
            temp = int(f"{highest_num}{num}")
            if temp > highest_to_right:
                highest_to_right = temp

        ans += max(highest_to_left, highest_to_right)

    return ans


def solve_part_2():
    N = 12
    ans = 0
    for line in lines:
        nums = list(map(int, line))
        highests = []
        start_idx = 0
        for i in range(N):
            nums_left = N - i
            end_idx = len(nums) - nums_left + 1
            segment = nums[start_idx:end_idx]
            highest_in_segment = max(segment)
            start_idx = nums.index(highest_in_segment, start_idx) + 1

            highests.append(highest_in_segment)
        ans += int("".join(map(str, highests)))

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
