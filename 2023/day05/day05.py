# https://adventofcode.com/2023/day/5
from collections import deque, defaultdict
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def solve_part_1():
    maps = [[] for _ in range(7)]
    num_blanks = 0

    r = r"(\d+)"
    seeds = list(map(int, re.findall(r, lines[0])))
    for line in lines[2:]:
        if line == "":
            num_blanks += 1
            continue
        if ":" in line:
            continue

        target_map = maps[num_blanks]
        target_map.append(list(map(int, re.findall(r, line))))
    
    locations = []
    for seed in seeds:
        out = seed
        for m in maps:
            for dest_range_start, source_range_start, range_len in m:
                if out >= source_range_start and out < source_range_start + range_len:
                    out = out - (source_range_start - dest_range_start)
                    break
        locations.append(out)

    return min(locations)
    
def solve_part_2():
    seeds = []
    maps = [[] for _ in range(7)]
    num_blanks = 0

    r = r"(\d+)"
    seeds = list(map(int, re.findall(r, lines[0])))

    # Get seed ranges from seeds line
    seed_ranges = []
    for i in range(0, len(seeds), 2):
        seed_ranges.append((seeds[i], seeds[i] + seeds[i+1]))

    for line in lines[2:]:
        if line == "":
            num_blanks += 1
            continue
        if ":" in line:
            continue
        target_map = maps[num_blanks]
        target_map.append(list(map(int, re.findall(r, line))))
    
    for m in maps:
        # At every stage we map our current seed ranges into the next
        temp_seed_ranges = []
        while len(seed_ranges):
            seed_start, seed_end = seed_ranges.pop()

            for dest_range_start, source_range_start, range_len in m:
                # Compute if there is a range overlap between the source range and our seed range
                overlap_start = max(seed_start, source_range_start)
                overlap_end = min(seed_end, source_range_start + range_len)

                # We have a valid overlap
                if overlap_start < overlap_end:
                    # There are non-overlapping elements on the left
                    if overlap_start > seed_start:
                        # This is added back to seed ranges - there still may exist a source/dest map that affects this group
                        seed_ranges.append((seed_start, overlap_start))
                    
                    # The overlapping elements are affected by the current "rule", so should be adjusted accordingly
                    temp_seed_ranges.append(
                        (overlap_start - (source_range_start - dest_range_start), overlap_end - (source_range_start - dest_range_start))
                    )

                    # There are non-overlapping elements on the right
                    if overlap_end < seed_end:
                        # This is added back to seed ranges - there still may exist a source/dest map that affects this group
                        seed_ranges.append((overlap_end, seed_end))

                    break # my heart
            # There was no overlap in any of the ranges within this map - pass our values through
            else:
                temp_seed_ranges.append((seed_start, seed_end))

        # Once we have built the new seed ranges (by exhausting our current seeds)
        # we can assign it back and repeat
        seed_ranges = temp_seed_ranges

    return sorted(seed_ranges)[0][0]

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

