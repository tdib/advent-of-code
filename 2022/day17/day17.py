# https://adventofcode.com/2022/day/17

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
    MAX_NUM_ROCKS = 2022
    OFFSET_FROM_LEFT = 2
    settled_rock_positions = set()
    curr_rock_positions = set()
    num_placed = 0
    turn = 0

    while num_placed <= MAX_NUM_ROCKS:
        # We are on a turn where we need to spawn a new rock
        if not curr_rock_positions:
            # Compute 4 above the highest rock
            spawn_height = max(settled_rock_positions, key=lambda r: r[1])[1] + HEIGHT_PADDING if len(settled_rock_positions) else HEIGHT_PADDING - 1
            bottom_left_pos = (OFFSET_FROM_LEFT, spawn_height)
            # Compute where the new rock will spawn, anchoring on the bottom left position
            rock_idx = num_placed % len(rocks)
            for row_idx, row in enumerate(rocks[rock_idx][::-1]):
                for col_idx, col in enumerate(row):
                    if col:
                        curr_rock_positions.add(add_tuples(bottom_left_pos, (col_idx, row_idx)))
            print_map(curr_rock_positions, settled_rock_positions)

        new_rock_positions = set()
        direction = m[line[turn % len(line)]]
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
            curr_rock_positions = new_rock_positions.copy()
            pass
        print_map(curr_rock_positions, settled_rock_positions)
        
        new_rock_positions = set()
        DOWN = (0, -1)
        for pos in curr_rock_positions:
            new_pos = add_tuples(pos, DOWN)
            # We need to settle the rock where it currently is due to landing on something
            if new_pos in settled_rock_positions or new_pos[1] < 0:
                settled_rock_positions.update(curr_rock_positions)
                curr_rock_positions = set()
                num_placed += 1
                break
            new_rock_positions.add(new_pos)
        # The new position is valid, so shift the rock down
        else:
            curr_rock_positions = new_rock_positions.copy()
        print_map(curr_rock_positions, settled_rock_positions)


        if num_placed == MAX_NUM_ROCKS:
            tallest_rock_pos = max(settled_rock_positions, key=lambda r: r[1])[1]
            return tallest_rock_pos + 1

        turn += 1


def solve_part_2():
    ans = 0

print(f'Part 1 answer: {solve_part_1()}')
print(f'Part 2 answer: {solve_part_2()}')


