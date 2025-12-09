# https://adventofcode.com/2025/day/09
from typing import cast

import shapely

from util.util import read_as_lines

positions: list[tuple[int, int]] = cast(
    list[tuple[int, int]],
    list(
        map(lambda line: tuple(map(int, line.split(","))), read_as_lines("input.txt"))
    ),
)


def solve_part_1():
    ans = 0
    for pos in positions:
        for other_pos in positions:
            size = (abs(pos[0] - other_pos[0]) + 1) * (abs(pos[1] - other_pos[1]) + 1)
            if size > ans:
                ans = size

    return ans


def solve_part_2():
    ans = 0

    tile_polygon = shapely.Polygon(positions)
    for pos in positions:
        for other_pos in positions:
            candidate_polygon = shapely.box(
                min(pos[0], other_pos[0]),
                min(pos[1], other_pos[1]),
                max(pos[0], other_pos[0]),
                max(pos[1], other_pos[1]),
            )

            if tile_polygon.contains(candidate_polygon):
                size = (abs(pos[0] - other_pos[0]) + 1) * (
                    abs(pos[1] - other_pos[1]) + 1
                )
                if size > ans:
                    ans = size

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
