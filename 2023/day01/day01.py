# https://adventofcode.com/2023/day/1
from collections import deque, defaultdict
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def solve_part_1():
    ans = 0
    for line in lines:
        matches = re.findall(r'\d', line)
        ans +=  int(matches[0] + matches[-1])

    return ans
        


def solve_part_2():
    ans = 0
    for line in lines:
        nums = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9
        }
        r = r'(\d)'
        matches = (re.findall(r, line))
        if matches:
            num_num_left = matches[0]
            num_num_right = matches[-1]
            num_idx_left = line.index(num_num_left)
            num_idx_right = line.rindex(num_num_right)
        else:
            num_num_left = None
            num_num_right = None
        
        str_idx_left = len(line) - 1
        str_num_left = None
        str_idx_right = 0
        str_num_right = None
        for num, val in nums.items():
            if num in line:
                if (idx := line.index(num)) < str_idx_left:
                    str_idx_left = idx
                    str_num_left = val
            
                if (idx := line.rindex(num)) > str_idx_right:
                    str_idx_right = idx
                    str_num_right = val

        # We have both strs and nums
        x, y = len(line), 0
        if str_num_left and str_num_left:
            if str_idx_left < num_idx_left:
                x = str_num_left
            else:
                x = num_num_left

            if str_idx_right > num_idx_right:
                y = str_num_right
            else:
                y = num_num_right
        # We have no numbers
        elif str_num_left and not num_num_left:
            x = num_num_left
            y = num_num_right
        # We have no strs
        elif not str_num_left and num_num_left:
            x = num_num_left
            y = num_num_right

        ans += int(f"{x}{y}")

    return ans
        

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

