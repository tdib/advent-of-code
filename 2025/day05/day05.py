# https://adventofcode.com/2025/day/5

import util

fresh_id_ranges_raw, ingredient_ids_raw = util.read_as_chunks("input.txt")
fresh_id_ranges = [tuple(map(int, r.split("-"))) for r in fresh_id_ranges_raw]
ingredient_ids = map(int, ingredient_ids_raw)


def solve_part_1():
    ans = 0
    ranges = [range(r[0], r[1] + 1) for r in fresh_id_ranges]

    for id in ingredient_ids:
        if any(id in r for r in ranges):
            ans += 1

    return ans


def solve_part_2():
    ans = 0
    sorted_fresh_id_ranges = sorted(fresh_id_ranges)
    non_overlapping = [sorted_fresh_id_ranges[0]]
    curr_ptr = sorted_fresh_id_ranges[0][1] + 1
    for r in sorted_fresh_id_ranges[1:]:
        if curr_ptr > r[1]:
            continue

        # If there was overlap, we simply cut off the start of this range
        # If there was no overlap, we don't need to change the start of this range
        if curr_ptr in range(r[0], r[1] + 1):
            new_start = curr_ptr
        else:
            new_start = r[0]

        non_overlapping.append((new_start, r[1]))
        curr_ptr = r[1] + 1

    for r in non_overlapping:
        ans += r[1] - r[0] + 1

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
