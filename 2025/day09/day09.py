# https://adventofcode.com/2025/day/09
import re
from cmath import rect
from collections import defaultdict, deque
from typing import cast

import shapely

from util.util import C, Notable, fill_area, print_map, read_as_lines

positions_lines = read_as_lines("input.txt")
positions: list[tuple[int, int]] = cast(
    list[tuple[int, int]],
    list(map(lambda line: tuple(map(int, line.split(","))), positions_lines)),
)
# Restructure for row, col instead of the opposite
# positions: list[tuple[int, int]] = cast(
#     list[tuple[int, int]], [(p[1], p[0]) for p in positions_nums]
# )


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
    grid = [["." for _ in range(10)] for _ in range(13)]

    # Compute boundary of the red tiles. This should form some enclosed shape
    boundary = set()
    boundary_edges = set()
    for p1, p2 in zip(positions, positions[1:] + [positions[0]]):
        edge = fill_area(p1, p2)
        boundary_edges.add((p1, p2))
        boundary.update(edge)
    # print(boundary_edges)

    p = shapely.Polygon(positions)
    # print("area (should be 16)", p.area, p.is_closed, p.is_valid)
    # print("length (should be 30)", p.length)
    # return
    for i, pos in enumerate(positions):
        for j, other_pos in enumerate(positions):
            # print(i, j, "(", len(positions), ")")
            # Calculate the size first

            corner1 = pos
            corner2 = (pos[0], other_pos[1])
            corner3 = other_pos
            corner4 = (other_pos[0], pos[1])
            print("Getting size for", corner1, corner2, corner3, corner4)
            p2 = shapely.Polygon([corner1, corner2, corner3, corner4])

            if p.contains(p2):
                print("CONTAINS")
                size = (abs(pos[0] - other_pos[0]) + 1) * (
                    abs(pos[1] - other_pos[1]) + 1
                )
                print("size", size)
                if size > ans:
                    print("ANS")
                    ans = size

            # # If it's big enough to show interest, walk the edge?
            # if size > ans:
            #     corner1 = pos
            #     corner2 = (pos[0], other_pos[1])
            #     corner3 = other_pos
            #     corner4 = (other_pos[0], pos[1])

            # candidate_boundary = fill_area(pos, other_pos)
            # print_map(
            #     grid,
            #     [
            #         Notable(
            #             candidate_boundary.intersection(boundary),
            #             symbol="X",
            #             colour=C.BLUE,
            #         ),
            #         Notable(candidate_boundary, symbol="o", colour=C.BLUE),
            #         Notable(boundary),
            #     ],
            # )

            # print("corners:", corner1, corner2, corner3, corner4)
            # All corners are in bounds
            # a = raycast_bound_check(corner1, boundary_edges)
            # b = raycast_bound_check(corner2, boundary_edges)
            # c = raycast_bound_check(corner3, boundary_edges)
            # d = raycast_bound_check(corner4, boundary_edges)
            # if not all(
            #     [
            #         raycast_bound_check(corner1, boundary_edges),
            #         raycast_bound_check(corner2, boundary_edges),
            #         raycast_bound_check(corner3, boundary_edges),
            #         raycast_bound_check(corner4, boundary_edges),
            #     ]
            # ):
            #     continue
            # print("CORNERS WITHIN BOUNDS...")
            # edge1 = (corner1, corner2)
            # edge2 = (corner2, corner3)
            # edge3 = (corner3, corner4)
            # edge4 = (corner4, corner1)
            # for boundary_edge in boundary_edges:
            #     w = edges_intersect(edge1, boundary_edge)
            #     x = edges_intersect(edge2, boundary_edge)
            #     y = edges_intersect(edge3, boundary_edge)
            #     z = edges_intersect(edge4, boundary_edge)
            #     if not any([w, x, y, z]):
            #         print("found area of size", size)
            #         ans = size

            # intersects_any = False
            # for boundary_edge in boundary_edges:
            #     for rectangle_edge in [edge1, edge2, edge3, edge4]:
            #         print(
            #             "checking if",
            #             boundary_edge,
            #             "intersects",
            #             rectangle_edge,
            #         )
            #         if edges_intersect(rectangle_edge, boundary_edge):
            #             print("it DOES")
            #             intersects_any = True
            #             break
            #     if intersects_any:
            #         break
            # if not intersects_any:
            #     print("found area of size", size)
            #     ans = size

            #

    # 4595056840 too high
    # 1534701749 too low
    return ans


def edges_intersect(edge_a, edge_b):
    intersects = False
    (edge_a_start_row, edge_a_start_col), (edge_a_dest_row, edge_a_dest_col) = edge_a
    (edge_b_start_row, edge_b_start_col), (edge_b_dest_row, edge_b_dest_col) = edge_b

    # Normalise edge a rows
    if edge_a_start_row > edge_a_dest_row:
        edge_a_start_row, edge_a_dest_row = edge_a_dest_row, edge_a_start_row

    # Normalise edge a cols
    if edge_a_start_col > edge_a_dest_col:
        edge_a_start_col, edge_a_dest_col = edge_a_dest_col, edge_a_start_col

    # Normalise edge b rows
    if edge_b_start_row > edge_b_dest_row:
        edge_b_start_row, edge_b_dest_row = edge_b_dest_row, edge_b_start_row

    # Normalise edge b cols
    if edge_b_start_col > edge_b_dest_col:
        edge_b_start_col, edge_b_dest_col = edge_b_dest_col, edge_b_start_col

    edge_a_horizontal = edge_a_start_row == edge_a_dest_row
    edge_b_horizontal = edge_b_start_row == edge_b_dest_row

    # Parallel lines
    if (edge_a_horizontal and edge_b_horizontal) or (
        not edge_a_horizontal and not edge_b_horizontal
    ):
        return False

    # Edge a is horizontal, edge b is vertical
    if edge_a_horizontal:
        intersects = (edge_a_start_col < edge_b_start_col < edge_a_dest_col) and (
            edge_b_start_row <= edge_a_start_row < edge_b_dest_row
        )
    # Edge a is vertical, edge b is horizontal
    else:
        # Intersection condition
        intersects = (edge_a_start_row < edge_b_start_row < edge_a_dest_row) and (
            edge_b_start_col <= edge_a_start_col < edge_b_dest_col
        )

    return intersects


def raycast_bound_check(target, boundary_edges):
    # print("Checking if", target, "within bounds")
    target_row, target_col = target

    in_bound = False

    for p1, p2 in boundary_edges:
        # print("Checking boundary", p1, p2)
        if target == p1 or target == p2:
            # print("target is ON the boundary. immediately returning true")
            # print("ON bound:", True)
            return True

        p1_row, p1_col = p1
        p2_row, p2_col = p2

        # Make sure that p2 is larger than p1
        if p1_row > p2_row:
            p1_row, p2_row = p2_row, p1_row

        if p1_col > p2_col:
            p1_col, p2_col = p2_col, p1_col

        # We are on a horizontal edge border
        # if target_row == p1_row and target_col >= p1_col and target_col <= p2_col:
        # return True
        if p1_row == p2_row and target_row == p1_row and p1_col <= target_col <= p2_col:
            return True

        # The x positions differ so this can't be a vertical line
        if p1_col != p2_col:
            # print("Not a vertical line")
            continue

        # We are on a vertical edge border
        # if target_col == p1_col and target_row >= p1_row and target_row <= p2_row:
        #     return True
        if p1_col == p2_col and target_col == p1_col and p1_row <= target_row <= p2_row:
            return True

        # Our target y is outside the y position of this boundary edge
        if not (p1_row <= target_row < p2_row):
            # if p1_row > target_row or p2_row < target_row:
            # print("target y is outside of range")
            continue

        # We have a vertical edge that we are in the correct y-range for
        # and the line occurs to the left of (or on) our target
        # if target_col > p1_col:
        if p1_col > target_col:
            # print("crossed over")
            in_bound = not in_bound

    # print("in bound:", in_bound)
    # print()

    return in_bound


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
