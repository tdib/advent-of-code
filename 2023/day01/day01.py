# https://adventofcode.com/2023/day/1
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def solve_part_1():
    ans = 0
    for line in lines:
        matches = re.findall(r"\d", line)
        # Check just to ensure no errors happen with inputs not containing numbers (i.e. test data)
        if matches:
            ans += int(matches[0] + matches[-1])
    return ans


def solve_part_2():
    ans = 0
    for line in lines:
        # Find the digit numbers
        matches = (re.findall(r"\d", line))

        # Check just to ensure no errors happen with inputs not containing numbers (i.e. test data)
        if matches:
            # If we have at least one match, we are safe to set both left and right
            num_num_left = matches[0]
            num_num_right = matches[-1]
            num_idx_left = line.index(num_num_left)
            num_idx_right = line.rindex(num_num_right)

        # Find the string numbers
        nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        # These idx variables are used to track the *position* of a given digit string
        str_idx_left = len(line) - 1
        str_idx_right = 0
        # We will use the num variables to track the *value* of a given digit string
        str_num_left = None
        str_num_right = None
        for val, num_str in enumerate(nums):
            # Offset by 1 to allow the index value to match the string we are dealing with
            val += 1
            if num_str in line:
                # We have a new leftmost string index
                if (l_idx := line.index(num_str)) < str_idx_left:
                    str_idx_left = l_idx
                    str_num_left = val
                # We have a new rightmost string index
                if (r_idx := line.rindex(num_str)) > str_idx_right:
                    str_idx_right = r_idx
                    str_num_right = val
        
        # By this point, we will have the leftmost and rightmost strings and digits

        l, r = len(line), 0
        # We have strings
        if str_num_left:
            # We perform comparisons with the strings and digits to find the bounds
            l = str_num_left if str_idx_left < num_idx_left else num_num_left
            r = str_num_right if str_idx_right > num_idx_right else num_num_right
        # We only have numbers
        else:
            l = num_num_left
            r = num_num_right

        ans += int(f"{l}{r}")

    return ans
        

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

