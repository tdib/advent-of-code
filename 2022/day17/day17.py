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

def print_map(curr_rock_positions, rock_positions, print_flag=True):
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

rocks = [LINE, PLUS, L, VERT_LINE, SQUARE]
m = {
    '>': (1, 0),
    '<': (-1, 0)
}
OFFSET_FROM_LEFT = 2
CAVE_WIDTH = 7
HEIGHT_PADDING = 4
# If set to true, will display a visual output of the cave, and allow you to step through each turn
PRINT_FLAG = False
def solve(num_rocks):
    settled_rock_positions = set()
    curr_rock_positions = set()
    abs_max_height = -1 # Index of absolute max height
    rel_max_height = -1 # Index of highest block, AFTER offsetting has taken place
    found_cycle = False
    height_offset = 0 # How much have we offset by (i.e. how many redundant heights have we removed)
    seen_states = {}
    num_placed = 0
    skip = 0
    turn = 0 # A turn is defined as a movement by jet, and down

    while num_placed <= num_rocks:
        # We are on a turn where we need to spawn a new rock
        if not curr_rock_positions:
            # Compute a padded amount above the highest rock and from the left of the cave
            bottom_left_pos = (OFFSET_FROM_LEFT, rel_max_height + HEIGHT_PADDING)
            # Compute where the new rock will spawn, anchoring on the bottom left position
            rock_idx = num_placed % len(rocks)

            # Spawn a new rock (of the current shape) in our current positions
            for row_idx, row in enumerate(rocks[rock_idx][::-1]):
                for col_idx, col in enumerate(row):
                    if col:
                        curr_rock_positions.add(add_tuples(bottom_left_pos, (col_idx, row_idx)))
            print_map(curr_rock_positions, settled_rock_positions, PRINT_FLAG)

        new_rock_positions = set()
        str_idx = turn % len(line)
        direction = m[line[str_idx]]
        # Check if left/right is a valid move
        for pos in curr_rock_positions:
            new_pos = add_tuples(pos, direction)
            # We have found an invalid configuration due to hitting rock or being out of bounds
            if new_pos in settled_rock_positions or new_pos[0] < 0 or new_pos[0] >= CAVE_WIDTH:
                break
            new_rock_positions.add(new_pos)
        # The new position is valid, so shift our current rock there
        # This is only evaluated if we don't break out of the above loop
        else:
            curr_rock_positions = new_rock_positions
        print_map(curr_rock_positions, settled_rock_positions, PRINT_FLAG)
        
        new_rock_positions = set()
        for pos in curr_rock_positions:
            # Calculate the position below this one
            new_pos = add_tuples(pos, (0, -1))

            # We need to settle the rock where it currently is due to landing on something
            if new_pos in settled_rock_positions or new_pos[1] < 0:
                # Since this is a valid place to land, we add the current rock to our settled pieces
                settled_rock_positions.update(curr_rock_positions)
                # Check if the rock we just placed is taller than our current tallest
                tallest_in_curr = max(curr_rock_positions, key=lambda rock: rock[1])[1]
                abs_max_height = max(abs_max_height, tallest_in_curr + height_offset)
                curr_rock_positions = set()

                # Perform flood fill to find only rocks that are relevant to new blocks. If this isn't
                # done, we will end up with many pieces that will never have an effect on the simulation
                rel_max_height = abs_max_height - height_offset
                pruned = flood_fill((0, rel_max_height + 1), settled_rock_positions)

                # Out of these new rocks, find the one with the lowest y value
                min_height = min(pruned, key=lambda rock: rock[1])[1]

                # Offset each of the pruned rocks heights to 0 so we don't have to deal with large values
                height_offset += min_height
                pruned_offset = set(map(lambda x: (x[0], x[1] - min_height), pruned))

                # Adjust our max height according to the new pruned rocks
                rel_max_height = abs_max_height - height_offset

                # Filter our rocks to only give us the last n rows, used for detecting cycles
                # In the input, setting this to 1 works fine (as we use other factors to detect cycles),
                # although this is set to 50 as this would be more robust for other inputs
                NUM_CYCLE_ROWS = 50
                top_rows = filter(lambda pos: rel_max_height - pos[1] > rel_max_height - NUM_CYCLE_ROWS, pruned_offset)

                # Our current state can be defined as the current rock shape, the current progress/index of the
                # instructions, and the position of rocks last n rows
                state_key = (rock_idx, str_idx, frozenset(top_rows))

                # If we have stumbled across a state that has been seen before for the first time
                if state_key in seen_states and not found_cycle and num_rocks:
                    found_cycle = True

                    # A cycle must consider going from state A -> state A, so we need to know some information about
                    # the original state A such as the height, which can differ across cycles
                    prev_max_height, prev_num_placed = seen_states[state_key]

                    # What is the height of each cycle? i.e. how many rows before we reach the next
                    cycle_height = abs_max_height - prev_max_height
                    # How many pieces are placed in this cycle? i.e. how many pieces before we reach the next
                    cycle_num_placed = num_placed - prev_num_placed

                    # How many times do we need to repeat this cycle before we get (very close) to the end
                    # We find how many rocks are left (after what we've placed) and divide by the cycle size
                    num_repeats = (num_rocks - num_placed) // cycle_num_placed

                    # How many placements can we skip due to the cycle
                    skip += num_repeats * cycle_height

                    # Adjust our tracking to emulate having placed this many pieces
                    num_placed += num_repeats * cycle_num_placed

                # We only need to track states if we have not already found a cycle
                elif not found_cycle:
                    seen_states[state_key] = (abs_max_height, num_placed)

                # After offsetting, where is our new tallest point
                # Remove unnecessary settled rocks by replacing them with the pruned ones
                settled_rock_positions = pruned_offset
                num_placed += 1
                break
            new_rock_positions.add(new_pos)
        # The new position is valid, so shift the rock down
        else:
            curr_rock_positions = new_rock_positions
        print_map(curr_rock_positions, settled_rock_positions, PRINT_FLAG)

        if num_placed == num_rocks:
            # Whatever our greatest height was, plus all the height we can skip, 1 to offset 0-based indexing
            return abs_max_height + skip + 1

        turn += 1

print(f'Part 1 answer: {solve(2022)}')
print(f'Part 2 answer: {solve(1_000_000_000_000)}')


