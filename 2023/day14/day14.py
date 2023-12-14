# https://adventofcode.com/2023/day/14

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def add_tuples(a, b):
    return (a[0] + b[0], a[1] + b[1])

CUBE_SYMBOL = "#"
ROUND_SYMBOL = "O"
EMPTY_SYMBOL = "."
def print_map(rounds, cubes, width=len(lines[0]), height=len(lines)):
    for r in range(height):
        for c in range(width):
            curr = (r, c)
            if curr in rounds:
                print(ROUND_SYMBOL, end="")
            elif curr in cubes:
                print(CUBE_SYMBOL, end="")
            else:
                print(EMPTY_SYMBOL, end="")
        print()
    print()

def within_bounds(pos, width=len(lines[0]), height=len(lines)):
    row, col = pos
    return row >= 0 and row < height and col >= 0 and col < width

def get_map_positions():
    round_rock_positions = set()
    cube_rock_positions = set()
    for row_idx, line in enumerate(lines):
        for col_idx, ch in enumerate(line):
            if ch == ROUND_SYMBOL:
                round_rock_positions.add((row_idx, col_idx))
            elif ch == CUBE_SYMBOL:
                cube_rock_positions.add((row_idx, col_idx))
    
    return round_rock_positions, cube_rock_positions

def solve_part_1():
    ans = 0
    round_rock_positions, cube_rock_positions = get_map_positions()
    
    UP = (-1, 0)
    # We will iterate until a given iteration does not have any possible changes
    has_change = True
    while has_change:
        has_change = False
        # This is used to shift one rock position at a time
        temp = set()
        # Go through every round rock and attempt to move it up
        for curr_pos in round_rock_positions:
            up_pos = add_tuples(curr_pos, UP)
            # Check if up is a valid position (is not out of bounds and not overlapping with a different rock)
            if within_bounds(up_pos) and up_pos not in round_rock_positions and up_pos not in cube_rock_positions:
                temp.add(up_pos)
                # Mark this change
                has_change = True
            # The position above is invalid - add the current rock back to our set
            else:
                temp.add(curr_pos)
            
        # Overwrite our positions with the new ones
        round_rock_positions = temp.copy()

    # The difference between the height of the map and the row index of a given rock is our rock weight
    for round_rock in round_rock_positions:
        ans += len(lines) - round_rock[0]

    return ans

def solve_part_2():
    ans = 0
    round_rock_positions, cube_rock_positions = get_map_positions()
    
    DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    MAX_CYCLES = 1000000000
    count = 0
    visited = {}
    found_cycle = False
    while count < MAX_CYCLES:
        # We must now go in every direction (up, left, down, right)
        for dir in DIRECTIONS:
            # Essentially repeat part 1, moving each rock one at a time until we cannot move any more
            has_change = True
            while has_change:
                has_change = False
                temp = set()
                for curr_pos in round_rock_positions:
                    new_pos = add_tuples(curr_pos, dir)
                    if within_bounds(new_pos) and new_pos not in round_rock_positions and new_pos not in cube_rock_positions:
                        temp.add(new_pos)
                        has_change = True
                    else:
                        temp.add(curr_pos)
                
                round_rock_positions = temp.copy()

        # At this point we have moved the rocks as much as we can in each direction, so we have completed a cycle
        count += 1

        # Check for states we have seen before (cycles of cycles)
        key = str(round_rock_positions)
        # Only consider this part if we have not yet found a cycle
        if not found_cycle:
            if key in visited:
                # Find the difference of our current count and the last time we were at this point
                prev_count = visited[key]
                cycle_length = count - prev_count

                # We can compute how many times we need to repeat by taking the remaining cycles to go, and
                # dividing by our cycle length
                num_repeats = (MAX_CYCLES - count) // cycle_length

                # num_repeats * cycle_length will put our count very close to the end, and we know that the state
                # at that count will be the same as what we have now, so we don't need to compute everything in-between
                count += num_repeats * cycle_length

                # Since we have found the cycle, there is no point adding anything further to our visited or recomputing
                # our count, so mark it as found
                found_cycle = True
            else:
                # Add the current state to our visited set - we must keep track of the count so we can
                # compute the difference when we come across this state again
                visited[key] = count

    for round_rock in round_rock_positions:
        ans += len(lines) - round_rock[0]

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

