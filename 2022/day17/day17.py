# https://adventofcode.com/2022/day/17
from collections import deque

with open('input.txt') as f:
    line = f.readline().strip()

LINE = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [1, 1, 1, 1],
]

PLUS = [
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [1, 1, 1, 0],
    [0, 1, 0, 0],
]
L = [
    [0, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [1, 1, 1, 0],
]
VERT_LINE = [
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
]
SQUARE = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [1, 1, 0, 0],
    [1, 1, 0, 0],
]

rocks = [LINE, PLUS, L, VERT_LINE, SQUARE]
RIGHT = '>'
LEFT = '<'
m = {
    RIGHT: (1, 0),
    LEFT: (-1, 0)
}
CAVE_WIDTH = 7
HEIGHT_PADDING = 4

def add_tuples(a, b):
    return (a[0]+b[0], a[1]+b[1])

def flood_fill(start, settled_rock_positions):
    q = deque([start])
    # We don't need to check up because we are starting at the top
    # and the piece cannot travel up so it won't matter
    directions = [(-1, 0), (1, 0), (0, -1)]
    important_rock = set()
    v = set()

    while q:
        curr = q.popleft()
        v.add(curr)
        for d in directions:
            next = add_tuples(curr, d)
            # We have hit a bound
            if next in settled_rock_positions:
                important_rock.add(next)
            # We have an empty area so we can continue the search
            elif next[0] >= 0 and next[0] < CAVE_WIDTH and next[1] >= 0 and next not in v and next not in q:
                q.append(next)

    return important_rock



PRINT_FLAG = False
def print_map(curr_rock_positions, rock_positions, print_flag=PRINT_FLAG):
    if not print_flag: return

    if len(rock_positions | curr_rock_positions):
        max_height = max(rock_positions | curr_rock_positions, key=lambda rock: rock[1])[1] + 1
    else:
        max_height = HEIGHT_PADDING

    for y in range(max_height):
        y = max_height - y - 1
        print('|', end='')
        for x in range(CAVE_WIDTH):
            if (x, y) in curr_rock_positions:
                print('@', end='')
            elif (x, y) in rock_positions:
                print('#', end='')
            else:
                print('.', end='')
            pass
        print('|')
    print('+' + '-'*CAVE_WIDTH + '+')
    print()
    input()

def solve_part_1():
    # MAX_NUM_ROCKS = 2023
    # MAX_NUM_ROCKS = 1_000_000
    MAX_NUM_ROCKS = 1_000_000_000_000
    OFFSET_FROM_LEFT = 2
    settled_rock_positions = set()
    curr_rock_positions = set()
    abs_max_height = -1 # Index of absolute max height
    rel_max_height = -1 # Index of highest block, AFTER offsetting has taken place
    num_placed = 0
    turn = 0
    height_offset = 0 # How much have we offset by (i.e. how many redundant heights have we removed)
    seen_states = {}
    found_cycle = False
    temp = 0


    while num_placed <= MAX_NUM_ROCKS:
        print('placed', num_placed)
        # We are on a turn where we need to spawn a new rock
        if not curr_rock_positions:
            # Compute 4 above the highest rock
            bottom_left_pos = (OFFSET_FROM_LEFT, rel_max_height + HEIGHT_PADDING)
            # Compute where the new rock will spawn, anchoring on the bottom left position
            rock_idx = num_placed % len(rocks)
            curr_rock_shape = rocks[rock_idx]
            # curr_rock_shape = rocks[0]
            for row_idx, row in enumerate(curr_rock_shape[::-1]):
                for col_idx, col in enumerate(row):
                    if col:
                        curr_rock_positions.add(add_tuples(bottom_left_pos, (col_idx, row_idx)))
            print_map(curr_rock_positions, settled_rock_positions)

        new_rock_positions = set()
        str_idx = turn % len(line)
        direction = m[line[str_idx]]
        # Check if left/right is a valid move
        for pos in curr_rock_positions:
            new_pos = add_tuples(pos, direction)
            # We have found an invalid configuration due to hitting rock or being out of bounds
            # if new_pos in settled_rock_positions or new_pos[0] < 0 or new_pos[0] >= CAVE_WIDTH:
            if new_pos[0] < 0 or new_pos[0] >= CAVE_WIDTH or new_pos in settled_rock_positions:
                break
            new_rock_positions.add(new_pos)
        # The new position is valid, so shift our current rock there
        # This is only evaluated if we don't break out of the above loop
        else:
            curr_rock_positions = new_rock_positions
        print_map(curr_rock_positions, settled_rock_positions)
        
        new_rock_positions = set()
        DOWN = (0, -1)
        for pos in curr_rock_positions:
            new_pos = add_tuples(pos, DOWN)
            # We need to settle the rock where it currently is due to landing on something
            # print(':)', new_pos)
            if new_pos in settled_rock_positions or new_pos[1] < 0:
                settled_rock_positions.update(curr_rock_positions)
                tallest_in_curr = max(curr_rock_positions, key=lambda rock: rock[1])[1]
                abs_max_height = max(abs_max_height, tallest_in_curr + height_offset)
                rel_max_height = abs_max_height - height_offset
                curr_rock_positions = set()

                # Perform flood fill to find only rocks that are relevant to new blocks
                pruned = flood_fill((0, rel_max_height + 1), settled_rock_positions)
                # Out of these new rocks, find the one with the lowest y value
                min_height = min(pruned, key=lambda rock: rock[1])[1]
                # Offset each of the pruned rocks heights to 0 so we don't have to deal with large values
                height_offset += min_height
                pruned = set(map(lambda x: (x[0], x[1] - min_height), pruned))
                rel_max_height = abs_max_height - height_offset

                # TODO
                N = 100
                top_n_pruned_rows = set(filter(lambda pos: rel_max_height - pos[1] > rel_max_height - N, pruned))

                state_key = (rock_idx, str_idx, frozenset(top_n_pruned_rows))
                if state_key in seen_states and not found_cycle:
                    # print('found', state_key, num_placed)
                    # return
                    # A cycle must consider going from state A -> state A, so we need to know some information about
                    # the original state A such as the height, which can differ across cycles
                    prev_max_height, prev_num_placed = seen_states[state_key]

                    # What is the height of each cycle? i.e. how many rows before we reach the next
                    cycle_height = abs_max_height - prev_max_height
                    # How many pieces are placed in this cycle? i.e. how many pieces before we reach the next
                    cycle_num_placed = num_placed - prev_num_placed

                    # How many times do we need to repeat this cycle before we get (very close) to the end
                    # We find how many rocks are left (after what we've placed) and divide by the cycle size
                    num_repeats = (MAX_NUM_ROCKS - num_placed) // cycle_num_placed

                    # Adjust our tracking to emulate having placed this many pieces
                    temp += num_repeats * cycle_height

                    num_placed += num_repeats * cycle_num_placed
                    # abs_max_height += num_repeats * cycle_height
                    # height_offset = abs_max_height - cycle_num_placed
                    # rel_max_height = abs_max_height - height_offset

                    print(f'{MAX_NUM_ROCKS=}, {abs_max_height=}, {num_placed=}, {num_repeats=}')

                    ####
                    # num_repeats = MAX_NUM_ROCKS // num_placed
                    # num_placed *= num_repeats
                    # abs_max_height *= num_repeats
                    ####
                    found_cycle = True
                    # abs_max_height *= num_repeats
                    # return abs_max_height
                elif not found_cycle:
                    # seen_states.add((rock_idx, str_idx, frozenset(top_n_pruned_rows)))
                    seen_states[state_key] = (abs_max_height, num_placed)

                # input()
                # print('seen', {(s[0], s[1], bin(s[2])[2:]) for s in seen_states})
                # print('top n', top_n_pruned_rows)
                # print('seen', seen_states)
                ######
                # bitmask = 0
                # for x, y in top_n_pruned_rows:
                #     bitmask |= 1 << (y * CAVE_WIDTH + x)
                # if (rock_idx, str_idx, bitmask) in seen_states:
                #     print('!!!!!!!!!!!!!!!!!')
                #     return 99999
                # seen_states.add((rock_idx, turn, bitmask))
                ######
                # After offsetting, where is our new tallest point
                # Remove unnecessary settled rocks by replacing them with the pruned ones
                settled_rock_positions = pruned
                num_placed += 1
                break
            new_rock_positions.add(new_pos)
        # The new position is valid, so shift the rock down
        else:
            curr_rock_positions = new_rock_positions
        print_map(curr_rock_positions, settled_rock_positions)

        print('what', abs_max_height, num_placed)
        if num_placed == MAX_NUM_ROCKS:
            print('?')
            # return abs_max_height + 1
            return abs_max_height + temp + 1


        turn += 1


def solve_part_2():
    ans = 0

# 1514288 for 1_000_000
# part 2 > 1554166666188
#          1566272188779
# part 2 > 1566272188799
#          1566272189352
print(f'Part 1 answer: {solve_part_1()} (1514288 for 1m)')
print(f'Part 2 answer: {solve_part_2()}')


