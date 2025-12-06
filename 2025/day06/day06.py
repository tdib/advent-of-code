# https://adventofcode.com/2025/day/6
import re

import util
from util.util import transpose

lines = util.read_as_lines("input.txt", strip_lines=True)


def solve_part_1():
    ans = 0
    nums = []
    for line in lines[:-1]:
        nums.append(list(map(int, line.split())))
    ops = lines[-1].split()
    nums = transpose(nums)

    for num_list, op in zip(nums, ops):
        temp = num_list[0]
        for num in num_list[1:]:
            if op == "*":
                temp *= num
            elif op == "+":
                temp += num

        ans += temp

    return ans


def solve_part_2():
    ans = 0

    # Positions of each column break (based on the operator locations)
    column_boundaries = list(
        map(lambda x: x.start() - 1, re.finditer("\\s+", lines[-1]))
    )
    # Add one more boundary for the very right side - just find the length of the longest line
    column_boundaries.append(len(max(lines[:-1], key=lambda line: len(line))))

    # Go through each number line (so exclude the last line), and put all the numbers into a list,
    # INCLUDING their whitespace. This is so we know if it is a left or right aligned number later on
    num_strs_with_whitespace = []
    for line in lines[:-1]:
        nums_in_line = []
        for prev_boundary, curr_boundary in zip(
            column_boundaries, column_boundaries[1:]
        ):
            # HACK: For the last number in a row, add a bunch of spaces so we don't go out of range
            # since `curr_boundary` is the index of the rightmost character + 1 of any line (so some
            # lines won't be that long)
            if curr_boundary == column_boundaries[-1]:
                nums_in_line.append(line[prev_boundary:].rstrip("\n").ljust(50, " "))
            else:
                nums_in_line.append(line[prev_boundary : curr_boundary - 1])
        num_strs_with_whitespace.append(nums_in_line)

    # Now that we've formatted the strings as we want, we can transpose the list and do similar logic to p1
    num_strs_with_whitespace = transpose(num_strs_with_whitespace)

    # Go through each set of numbers, and construct our new numbers, based on the columns.
    # e.g. ["123", " 45", " 67"], first iteration we will only find "3", then the second we will find
    # "2", "4", and "6", and the final we will find "3", "5", and "7"
    new_nums = []
    for num_list_str in num_strs_with_whitespace:
        # Longest number in this set - used when we iterate over the columns.
        # Could probs use the length of the 0th element but oh well
        largest_num_len = len(max(num_list_str, key=len))
        new_num_list = []
        # Go through the columns, and construct our new number
        for i in range(largest_num_len):
            constructed_num = []
            for num in num_list_str:
                # This check is what guards us from adding numbers from a different column, and is why we kept the spaces
                if num[i] != " ":
                    constructed_num.append(num[i])
            # HACK: Because I added a bunch of spaces to the last column, not having this breaks some stuff :P
            if constructed_num == []:
                break
            new_num_list.append("".join(constructed_num))

        new_nums.append(new_num_list)

    # Final stretch - we convert those strings into ints, and do the same logic as p1
    new_nums = list(map(lambda x: list(map(int, x)), new_nums))
    ops = lines[-1].split()
    for num_list, op in zip(new_nums, ops):
        temp = num_list[0]
        for num in num_list[1:]:
            if op == "*":
                temp *= num
            elif op == "+":
                temp += num
        ans += temp

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
