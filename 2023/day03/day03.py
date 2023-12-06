# https://adventofcode.com/2023/day/3
import re
from math import prod

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def add_tuples(a, b):
  return (a[0] + b[0], a[1] + b[1])


# Given two tuples like (1, 0), (5, 0), return a list of
# tuples that fill in between these points
# e.g. (1, 0), (5, 0) -> [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
# Note: This function assumes that start and end share an axis
def fill(start, end):
    filled = set([start, end])
    # Row is the same - fill col
    if start[0] == end[0]:
        s = start[1]
        e = end[1]
        for new_col in range(s+1, e):
            filled.add((start[0], new_col))
    # Col is the same - fill row
    else:
        s = start[0]
        e = end[0]
        for new_row in range(s+1, e):
            filled.add((new_row, start[1]))

    return tuple(filled)


def solve_part_1():
    r = r'(\d+)'
    # Map positions to numbers
    position_num_map = {}
    symbol_coverage_positions = set()
    for row_idx, line in enumerate(lines):
        # Find integers and positions
        matches = re.finditer(r, line)
        for match in matches:
            filled = fill((row_idx, match.start()), (row_idx, match.end()-1))
            match = match.group(0)
            position_num_map[filled] = int(match)
        
        # Find symbol positions
        for col_idx, symbol_coverage_pos in enumerate(line):
            if symbol_coverage_pos != "." and not symbol_coverage_pos.isdigit():
                symbol_coverage_positions.add((row_idx, col_idx))
            
    # Expand symbol radii
    new_symbols = set()
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]
    for pos in symbol_coverage_positions:
        for dir in directions:
            new_symbols.add(add_tuples(pos, dir))
    symbol_coverage_positions |= new_symbols

    adj = {}
    # Go through every number
    for curr_num_positions, val in position_num_map.items():
        # Go through every place that a symbol covers
        for symbol_coverage_pos in symbol_coverage_positions:
            # If we have an intersection, we can say this value is adjacent
            if symbol_coverage_pos in curr_num_positions:
                adj[curr_num_positions] = val
                break

    return sum(adj.values())


def solve_part_2():
    ans = 0 
    r = r'(\d+)'
    # Map positions to numbers
    position_num_map = {}
    symbol_coverage_positions = set()
    for row_idx, line in enumerate(lines):
        # Find integers and positions
        matches = re.finditer(r, line)
        for match in matches:
            filled = fill((row_idx, match.start()), (row_idx, match.end()-1))
            match = match.group(0)
            position_num_map[filled] = int(match)
        
        # Find symbol positions
        for col_idx, symbol_coverage_pos in enumerate(line):
            if symbol_coverage_pos != "." and not symbol_coverage_pos.isdigit():
                symbol_coverage_positions.add((row_idx, col_idx))
            
    # Expand symbol radii
    new_symbols = set()
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]
    for pos in symbol_coverage_positions:
        for dir in directions:
            new_symbols.add(add_tuples(pos, dir))
    symbol_coverage_positions |= new_symbols

    for symbol in symbol_coverage_positions:
        # If this is not a gear, we don't care and can continue
        if lines[symbol[0]][symbol[1]] != "*":
            continue
        
        # Expand its radius (inefficient because we've already computed this but it's fine)
        radius_positions = set([symbol])
        for dir in directions:
            radius_positions.add(add_tuples(symbol, dir))

        valid_gears = {}
        # Take each position in the radius
        for radius_position in radius_positions:
            # Check if there is a number that exists in that radius
            for curr_num_positions, val in position_num_map.items():
                # The current number we are scanning has a digit within this radius
                # so we can track this and move on to the next radius position
                if radius_position in curr_num_positions:
                    valid_gears[curr_num_positions] = val
                    break

        valid_gears = { k:v for k, v in valid_gears.items() if len(valid_gears) >= 2}
        if valid_gears:
            ans += prod(valid_gears.values())

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

