# https://adventofcode.com/2025/day/4

from util import (
    MOORE_DIRECTIONS,
    add_tuples,
    read_as_lines,
    read_grid_positions,
)

grid = read_as_lines("input.txt")


def solve_part_1():
    ans = 0
    chars = ["@"]
    [paper_roll_positions] = read_grid_positions(grid, chars)
    for paper_roll_position in paper_roll_positions:
        num_paper_neighbours = 0
        for direction in MOORE_DIRECTIONS:
            neighbour = add_tuples(paper_roll_position, direction)
            if neighbour in paper_roll_positions:
                num_paper_neighbours += 1
        if num_paper_neighbours < 4:
            ans += 1

    return ans


def solve_part_2():
    ans = 0
    chars = ["@"]
    grid_copy = grid.copy()

    dirty = True
    while dirty:
        dirty = False
        [paper_roll_positions] = read_grid_positions(grid_copy, chars)
        for paper_roll_position in paper_roll_positions:
            num_paper_neighbours = 0
            for direction in MOORE_DIRECTIONS:
                neighbour = add_tuples(paper_roll_position, direction)
                if neighbour in paper_roll_positions:
                    num_paper_neighbours += 1
            if num_paper_neighbours < 4:
                (row, col) = paper_roll_position
                target_row = list(grid_copy[row])
                target_row[col] = "x"
                grid_copy[row] = "".join(target_row)
                dirty = True
                ans += 1

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
