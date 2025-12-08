# https://adventofcode.com/2025/day/7

from functools import lru_cache

from util.util import (
    DOWN,
    LEFT,
    RIGHT,
    add_tuples,
    read_as_lines,
    read_grid_positions,
)

lines = read_as_lines("input.txt")
start, splitters = read_grid_positions(
    lines,
    ["S", "^"],
)


def solve_part_1():
    ans = 0
    beam_locs = set(start)

    for _ in range(len(lines)):
        new_beam_locs = set()
        for loc in beam_locs:
            next = add_tuples(loc, DOWN)
            if next in splitters:
                new_beam_locs.add(add_tuples(next, LEFT))
                new_beam_locs.add(add_tuples(next, RIGHT))
                ans += 1
            else:
                new_beam_locs.add(next)
        beam_locs = new_beam_locs

    return ans


def solve_part_2():
    curr = list(start)[0]
    # Go down until the first split
    while curr not in splitters:
        curr = add_tuples(curr, DOWN)
    return compute_split(curr)


@lru_cache(None)
def compute_split(position) -> int:
    """
    Given a splitting position, compute the number of paths it creates
    using a cache that stores previously computed values
    """
    queue = [
        add_tuples(position, LEFT),
        add_tuples(position, RIGHT),
    ]
    num = 0

    while len(queue):
        curr = queue.pop()
        while curr[0] < len(lines):
            curr = add_tuples(curr, DOWN)

            if curr in splitters:
                num += compute_split(curr)
                break

        if curr[0] == len(lines):
            num += 1

    return num


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
