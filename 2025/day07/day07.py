# https://adventofcode.com/2025/day/7

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
    def compute_split(position) -> int:
        """
        Given a splitting position, compute the number of paths it creates
        using a cache that stores previously computed values
        """
        if position in v:
            return v[position]

        queue = [
            add_tuples(position, LEFT),
            add_tuples(position, RIGHT),
        ]
        num = 0

        while len(queue):
            curr = queue.pop()

            while curr[0] < len(lines):
                curr = add_tuples(curr, DOWN)
                if curr in v:
                    num += v[curr]
                    break

                if curr in splitters:
                    result = compute_split(curr)
                    num += result
                    v[curr] = result
                    break

            if curr[0] == len(lines):
                num += 1

        v[position] = num
        return num

    curr = list(start)[0]
    v = {}

    # Go down until the first split
    while curr not in splitters:
        curr = add_tuples(curr, DOWN)

    return compute_split(curr)


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
