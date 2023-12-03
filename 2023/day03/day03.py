# https://adventofcode.com/2023/day/3
from collections import deque, defaultdict
import itertools
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def add_tuples(a, b):
  return (a[0] + b[0], a[1] + b[1])

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

def print_map(lines, num_positions, symbol_positions, symbol_radii):
    for row_idx, line in enumerate(lines):
        for col_idx, char in enumerate(line):
            pos = (row_idx, col_idx)
            if False:
                pass
            elif pos in symbol_positions:
                print(f"\033[91m{"x"}\033[0m", end="")
                # print("X", end="")
            elif pos in symbol_radii:
                print(f"\033[91m{char}\033[0m", end="")
                # print("o", end="")
            elif pos in num_positions:
                print(f"\033[94m{char}\033[0m", end="")
                # print(char, end="")
            else:
                print(char, end="")
        print()

def solve_part_1():
    symbol_coverage_positions = set()
    new_symbols = set()
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]
    r = r'(\d+)'
    # Map positions to numbers
    position_num_map = {}
    for row_idx, line in enumerate(lines):
        # matches = re.findall(r, line)
        matches = re.finditer(r, line)
        # num_matches = {m: 0 for m in matches}
        for match in matches:
            # match_indexes = list(find_all(line, match))
            # match_idx = match_indexes[num_matches[match]]
            # num_matches[match] += 1
            # match_start = match.start()
            # print(match)
            # print(match)
            # print(match.start())
            # print(match.end())
            # print(match.group(0))
            # match = match.group(1)
            # else:
                # match_idx = line.index(match)
                # line = line[match_idx+1:]
            # print(line, match, match_idx)
            # print(list(find_all(line, match)))
            # print()
            # match_idx = find_nth_occurrence(line, match, match_num)
            # print(x, match_idx)
            # if len(matches) != len(set(matches)):
            # match_idx = [i for i in range(len(line)) if line.startswith(match, i)][match_num]
            if match.group(0) == "889":
                print(match.start(), match.end()-1)
            filled = fill((row_idx, match.start()), (row_idx, match.end()-1))
            match = match.group(0)
            position_num_map[filled] = int(match)

    for row_idx, line in enumerate(lines):
        # Find symbols
        for col_idx, symbol_coverage_pos in enumerate(line):
            if symbol_coverage_pos != "." and not symbol_coverage_pos.isdigit():
                symbol_coverage_positions.add((row_idx, col_idx))
            
    # Expand symbol radii
    for pos in symbol_coverage_positions:
        for dir in directions:
            new_symbols.add(add_tuples(pos, dir))
    symbols = symbol_coverage_positions.copy()
    symbol_coverage_positions = symbol_coverage_positions.union(new_symbols)


    adj = {}
    # Go through every number
    for curr_num_positions, val in position_num_map.items():
        # Go through every place that a symbol covers
        for symbol_coverage_pos in symbol_coverage_positions:
            # If we have an intersection, we can say this value is adjacent
            if symbol_coverage_pos in curr_num_positions:
                # if val == 239:
                #     print(symbol_coverage_pos, curr_num_positions, symbol_coverage_pos in curr_num_positions, val)
                #     pass
                # adj[symbol_coverage_pos] = val
                adj[curr_num_positions] = val
                break
    # print(adj)

    # print_map(lines, position_num_map.keys())
    flat_num_positions = [item for sublist in position_num_map.keys() for item in sublist]
    flat_num_positions = [item for sublist in position_num_map.keys() for item in sublist]
    # print_map(lines, flat_num_positions, symbols, symbol_coverage_positions)

    # for k, v in position_num_map.items():
    #     if v == 239:
    #         print(k, v)
    

    # pos = position_num_map.values()
    # print(set(position_num_map.values()) - set(adj.values()))
    # print(position_num_map.values().adj.values()))
    non_adj = []
    for element in position_num_map.values():
        if element not in adj.values():
            non_adj.append(element)

    adj = adj.values()
    print(adj)

    # print({ k:v for k, v in adj.items() if v == 889})
    # print(list(filter(lambda x: x == 889, adj)))

    return sum(adj)




def solve_part_2():
    symbol_coverage_positions = set()
    new_symbols = set()
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]
    r = r'(\d+)'
    # Map positions to numbers
    position_num_map = {}
    for row_idx, line in enumerate(lines):
        matches = re.finditer(r, line)
        for match in matches:
            filled = fill((row_idx, match.start()), (row_idx, match.end()-1))
            match = match.group(0)
            position_num_map[filled] = int(match)

    for row_idx, line in enumerate(lines):
        # Find symbols
        for col_idx, symbol_coverage_pos in enumerate(line):
            if symbol_coverage_pos != "." and not symbol_coverage_pos.isdigit():
                symbol_coverage_positions.add((row_idx, col_idx))
            
    # Expand symbol radii
    for pos in symbol_coverage_positions:
        for dir in directions:
            new_symbols.add(add_tuples(pos, dir))
    symbols = symbol_coverage_positions.copy()
    symbol_coverage_positions = symbol_coverage_positions.union(new_symbols)


    # for line in lines:
        # print(line)
    ans = 0 
    for symbol in symbols:
        touching = []
        radius_positions = set([symbol])
        # If we find a gear
        if lines[symbol[0]][symbol[1]] != "*":
            continue
        print()
        print("NOW LOOKING AT SYMBOL", symbol)
        
        # Expand its radius
        for dir in directions:
            radius_positions.add(add_tuples(symbol, dir))

        
        # Number of women i've touched
        num_touches = 0
        touches = {}
        # Take each position in the radius
        for r in radius_positions:
            # Check if there is a number that exists in that radius
            for curr_num_positions, val in position_num_map.items():
                found_touch = False
                if r in curr_num_positions:
                # for pos in curr_num_positions:
                    # if pos in radius_positions:
                    touches[curr_num_positions] = val
                    touching.append(val)
                    num_touches += 1
                    found_touch = True
                    break
                
        
        print(symbol, num_touches)
        touches = { k:v for k, v in touches.items() if len(touches) >= 2}
        touches_thing = touches.values()
        print(touches)
        if touches_thing:
            product = 1
            for t in touches_thing:
                product *= t
            print(product)
            ans += product
                # If we have found one from the previous loop
                # 
                # if found_touch:
                    
            
        # if symbol == "*":

    adj = {}
    # Go through every number
    for curr_num_positions, val in position_num_map.items():
        # Go through every place that a symbol covers
        for symbol_coverage_pos in symbol_coverage_positions:
            # If we have an intersection, we can say this value is adjacent
            if symbol_coverage_pos in curr_num_positions:
                # if val == 239:
                #     print(symbol_coverage_pos, curr_num_positions, symbol_coverage_pos in curr_num_positions, val)
                #     pass
                # adj[symbol_coverage_pos] = val
                adj[curr_num_positions] = val
                break
    # print(adj)

    flat_num_positions = [item for sublist in position_num_map.keys() for item in sublist]
    # print_map(lines, flat_num_positions, symbols, symbol_coverage_positions)

    non_adj = []
    for element in position_num_map.values():
        if element not in adj.values():
            non_adj.append(element)

    adj = adj.values()
    print(adj)

    # print({ k:v for k, v in adj.items() if v == 889})
    # print(list(filter(lambda x: x == 889, adj)))

    # 72553360 too high
    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

