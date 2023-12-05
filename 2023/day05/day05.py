# https://adventofcode.com/2023/day/5
from collections import deque, defaultdict
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

# print(lines)

# def solve_part_1():
#     ans = 0
#     seeds = []
#     seed_to_soil = {}
#     soil_to_fertilizer = {}
#     fertilizer_to_water = {}
#     water_to_light = {}
#     light_to_temperature = {}
#     temperature_to_humidity = {}
#     humidity_to_location = {}
#     maps = [seed_to_soil, soil_to_fertilizer, fertilizer_to_water,
#             water_to_light, light_to_temperature, temperature_to_humidity, 
#             humidity_to_location]
#     num_blanks = 0

#     r = r"(\d+)"
#     all_nums = []
#     mods = []
#     num_blanks = 0
#     for line in lines:
#         if line == "":
#             num_blanks += 1
#             continue
#         if ":" in line:
#             continue
#         # nums = list(map(int, re.findall(r, line)))
#         # all_nums.extend(nums)
#         curr_lowest = mods[num_blanks]
#     all_nums = list(filter(lambda x: x != 0, all_nums))
#     # print()
#     # print()
#     # print(sorted(all_nums))
#     # print()
#     # print()
#     mod = min(all_nums)
#     # return


#     seeds = list(map(int, re.findall(r, lines[0])))
#     print("Mapping")
#     for line in lines[2:]:
#         print("Line", line)
#         if line == "":
#             print("BLANK")
#             num_blanks += 1
#             continue
#         if ":" in line:
#             continue

#         target_map = maps[num_blanks]
#         # nums = list(map(int, re.findall(r, line)))
#         dest_range_start, source_range_start, range_len = list(map(int, re.findall(r, line)))
#         # a = dest_range_start // mod
#         # dest_range_start %= mod
#         b = source_range_start
#         b = source_range_start %= 
#         lowest_num = min(dest_range_start, source_range_start, range_len)
#         source_range = range(source_range_start, source_range_start+range_len)
#         dest_range = range(dest_range_start, dest_range_start+range_len)

#         print('here')
#         # 95 58
#         # 96 59
#         # for i, source in enumerate(list(source_range)):
#             # print('a,b', source, dest_range[i])
#             # target_map[source] = dest_range[i]

#         # for a, b in zip(source_range, dest_range):
#         #     target_map[a] = b
    
#         for i in range(range_len):
#             target_map[source_range_start+i] = dest_range_start+i
#         print('good')
#             # print('a,b', a, b)
#         # print(list(source_range))


#     print("COMPLETE")
#     # for k, v in seed_to_soil.items():
#     #     print(k, v)
#     test = 0
#     print(soil_to_fertilizer)
#     locations = []
#     for seed in seeds:
#         print("SEED")
#         # seed_to_soil = {}
#         # soil_to_fertilizer = {}
#         # fertilizer_to_water = {}
#         # water_to_light = {}
#         # light_to_temperature = {}
#         # temperature_to_humidity = {}
#         # humidity_to_location = {}
#         # for m in maps:
#         # print("SEED:", seed)
#         soil = seed_to_soil.get(seed, seed)
#         # print('soil', soil)
#         fertilizer = soil_to_fertilizer.get(soil, soil)
#         # print('fertilizer', fertilizer)
#         water = fertilizer_to_water.get(fertilizer, fertilizer)
#         # print('water', water)
#         light = water_to_light.get(water, water)
#         # print('light', light)
#         temp = light_to_temperature.get(light, light)
#         # print('temp', temp)
#         humidity = temperature_to_humidity.get(temp, temp)
#         # print('humidity', humidity)
#         location = humidity_to_location.get(humidity, humidity)
#         # print('location', location)
#         locations.append(location)


#     print(locations)
#     return min(locations)


def solve_part_1():
    ans = 0
    seeds = []
    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []
    maps = [seed_to_soil, soil_to_fertilizer, fertilizer_to_water,
            water_to_light, light_to_temperature, temperature_to_humidity, 
            humidity_to_location]
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
    
    all_things = []
    for seed in seeds:
        out = seed
        # print()
        # print("SEED", seed)
        # flag = False
        for i, m in enumerate(maps):
            # print("map", i)
            for item in m:
                dest_range_start, source_range_start, range_len = item
                if out >= source_range_start and out < source_range_start + range_len:
                    out = out - (source_range_start - dest_range_start)
                    break
            # print(out)
                    # print(out)
        # break
        # print(out)
        all_things.append(out)
    # print(all_things)
    return min(all_things)
                # print(dest_range_start, source_range_start, range_len)
            # print()
        # print(out)
        # break
        # if not flag:
        #     out = seed
        #     print("NO")

            
        # source_range = range(source_range_start, source_range_start+range_len)
        # dest_range = range(dest_range_start, dest_range_start+range_len)


# def solve_part_2():
#     ans = 0
#     seeds = []
#     seed_to_soil = []
#     soil_to_fertilizer = []
#     fertilizer_to_water = []
#     water_to_light = []
#     light_to_temperature = []
#     temperature_to_humidity = []
#     humidity_to_location = []
#     maps = [seed_to_soil, soil_to_fertilizer, fertilizer_to_water,
#             water_to_light, light_to_temperature, temperature_to_humidity, 
#             humidity_to_location]
#     num_blanks = 0

#     r = r"(\d+)"
#     seeds = list(map(int, re.findall(r, lines[0])))

#     seed_ranges = []

#     # Get seed ranges from seeds line
#     for i in range(0, len(seeds), 2):
#         # seed_ranges.append(range(seeds[i], seeds[i] + seeds[i+1]))
#         seed_ranges.append((seeds[i], seeds[i] + seeds[i+1]))

#     print(seed_ranges)
#     print()

#     for line in lines[2:]:
#         if line == "":
#             num_blanks += 1
#             continue
#         if ":" in line:
#             continue
#         target_map = maps[num_blanks]
#         target_map.append(list(map(int, re.findall(r, line))))
    
#     j = 0
#     for i, m in enumerate(maps):
#         print()
#         print()
#         print("map", i, "with seed ranges", seed_ranges)
#         j += 1
#     # for seed_range in seed_ranges:
#         # max of starts
#         # min of ends
#         # At every stage we map our current seed ranges into the next
#         temp_seed_ranges = []
#         while len(seed_ranges):
#             seed_start, seed_end = seed_ranges.pop()
#             # if seed_start == 0 or seed_end == 0:
#             #     print("ZERO", (seed_start, seed_end))
#             print("SEED RANGE ->", seed_start, seed_end)
#             for dest_range_start, source_range_start, range_len in m:
#                 print("checking:", dest_range_start, source_range_start, range_len, (source_range_start, source_range_start+range_len))
#                 """
#                           ============   source
#                 --------                 seeds

#                 ~~~~~~~~~             dest
#                        ============   source
#                 --------------        seeds

#                        ========     source
#                 ------------------  seeds
#                 """
#                 overlap_start = max(seed_start, source_range_start)
#                 overlap_end = min(seed_end, source_range_start + range_len)
#                 # print(f"source range {(source_range_start, source_range_start + range_len)}")
#                 # print(f"dest range {(dest_range_start, dest_range_start + range_len)}")

#                 # print("BLAH", dest_range_start, source_range_start, range_len)
#                 # We have a valid overlap
#                 # means we have a left and right of overlap - could be length 0
#                 if overlap_start < overlap_end:
#                     # Left of overlap
#                     # (54, 100)
#                     if overlap_start > seed_start: # we have a left range
#                         print("    left", (seed_start, overlap_start))
#                         # temp_seed_ranges.append((source_range_start, overlap_start))
#                         temp_seed_ranges.append((seed_start, overlap_start))
#                     else:
#                         print("    no left")
#                     # overlap means we are in the current item range so we compute
#                     # the offset ranges
#                     res = (overlap_start - (source_range_start - dest_range_start), overlap_end - (source_range_start - dest_range_start))
#                     # if res[0] == 0:
#                     print("    overlap", (overlap_start, overlap_end), "maps to", res)
#                     # if overlap_start == 0:
#                         # print("    mapping", (overlap_start, overlap_end), "to", res)
#                     temp_seed_ranges.append(
#                         (overlap_start - (source_range_start - dest_range_start), overlap_end - (source_range_start - dest_range_start))
#                     )

#                     # if overlap_end < source_range_start + range_len:
#                     if overlap_end < seed_end:
#                         # temp_seed_ranges.append((overlap_end, source_range_start + range_len)) # calculate right
#                         print("    right", (overlap_end, seed_end))
#                         temp_seed_ranges.append((overlap_end, seed_end)) # calculate right
#                     else:
#                         print("    no right")
#                     # print()
#                     break #TODO
#                 # else:
#                 #     print("    ---")
#                 #     print()
#             # no overlap in any of the ranges within this map - pass our values through
#             else:
#                 print('    no overlap', (seed_start, seed_end))
#                 # print()
#                 temp_seed_ranges.append((seed_start, seed_end))
#             # print()

#         # Once we have built the new seed ranges (by exhausing our current seeds)
#         # we can assign it back and repeat
#         seed_ranges = temp_seed_ranges
#         x = list(filter(lambda y: y[0] == 0 or y[1] == 0, seed_ranges))
#         # print("seed ranges:::::::: ", seed_ranges)
#         print("seeds with 0", x)
#         # print()
#         # if j == 2:
#         #     break
#                     #right of overlap
#     # print(len(seed_ranges), f"{(27)}")
#     # print(len(seed_ranges), "(27)")
#     seed_ranges.sort()
#     # print(seed_ranges[:10])
#     print()
#     # > 92743746
#     print(seed_ranges)
#     return seed_ranges[0][0]
#     # print(seed_ranges)

    
def solve_part_2():
    ans = 0
    seeds = []
    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []
    maps = [seed_to_soil, soil_to_fertilizer, fertilizer_to_water,
            water_to_light, light_to_temperature, temperature_to_humidity, 
            humidity_to_location]
    num_blanks = 0

    r = r"(\d+)"
    seeds = list(map(int, re.findall(r, lines[0])))

    seed_ranges = []

    # Get seed ranges from seeds line
    for i in range(0, len(seeds), 2):
        # seed_ranges.append(range(seeds[i], seeds[i] + seeds[i+1]))
        seed_ranges.append((seeds[i], seeds[i] + seeds[i+1]))

    print(seed_ranges)
    print()

    for line in lines[2:]:
        if line == "":
            num_blanks += 1
            continue
        if ":" in line:
            continue
        target_map = maps[num_blanks]
        target_map.append(list(map(int, re.findall(r, line))))
    
    for m in maps:
        print(m)
    
    j = 0
    for i, m in enumerate(maps):
        print()
        print()
        print("map", i, "with seed ranges", seed_ranges)
        j += 1
    # for seed_range in seed_ranges:
        # max of starts
        # min of ends
        # At every stage we map our current seed ranges into the next
        temp_seed_ranges = []
        while len(seed_ranges):
            seed_start, seed_end = seed_ranges.pop()
            # if seed_start == 0 or seed_end == 0:
            #     print("ZERO", (seed_start, seed_end))
            print("SEED RANGE ->", seed_start, seed_end)
            for dest_range_start, source_range_start, range_len in m:
                print("checking:", dest_range_start, source_range_start, range_len, (source_range_start, source_range_start+range_len))
                """
                          ============   source
                --------                 seeds

                ~~~~~~~~~             dest
                       ============   source
                --------------        seeds

                       ========     source
                ------------------  seeds
                """
                overlap_start = max(seed_start, source_range_start)
                overlap_end = min(seed_end, source_range_start + range_len)
                # print(f"source range {(source_range_start, source_range_start + range_len)}")
                # print(f"dest range {(dest_range_start, dest_range_start + range_len)}")

                # print("BLAH", dest_range_start, source_range_start, range_len)
                # We have a valid overlap
                # means we have a left and right of overlap - could be length 0
                if overlap_start < overlap_end:
                    # Left of overlap
                    # (54, 100)
                    if overlap_start > seed_start: # we have a left range
                        print("    left", (seed_start, overlap_start))
                        # temp_seed_ranges.append((source_range_start, overlap_start))
                        seed_ranges.append((seed_start, overlap_start))
                    else:
                        print("    no left")
                    # overlap means we are in the current item range so we compute
                    # the offset ranges
                    # res = (overlap_start - (source_range_start - dest_range_start), overlap_end - (source_range_start - dest_range_start))
                    res = (overlap_start - (source_range_start - dest_range_start), overlap_end - (source_range_start - dest_range_start))
                    # if res[0] == 0:
                    print("    overlap", (overlap_start, overlap_end), "maps to", res)
                    # if overlap_start == 0:
                        # print("    mapping", (overlap_start, overlap_end), "to", res)
                    temp_seed_ranges.append(res)

                    # if overlap_end < source_range_start + range_len:
                    if overlap_end < seed_end:
                        # temp_seed_ranges.append((overlap_end, source_range_start + range_len)) # calculate right
                        print("    right", (overlap_end, seed_end))
                        seed_ranges.append((overlap_end, seed_end)) # calculate right
                    else:
                        print("    no right")
                    # print()
                    break #TODO
                # else:
                #     print("    ---")
                #     print()
            # no overlap in any of the ranges within this map - pass our values through
            else:
                print('    no overlap', (seed_start, seed_end))
                # print()
                temp_seed_ranges.append((seed_start, seed_end))
            # print()

        # Once we have built the new seed ranges (by exhausing our current seeds)
        # we can assign it back and repeat
        seed_ranges = temp_seed_ranges
        x = list(filter(lambda y: y[0] == 0 or y[1] == 0, seed_ranges))
        # print("seed ranges:::::::: ", seed_ranges)
        print("seeds with 0", x)
        # print()
        # if j == 2:
        #     break
                    #right of overlap
    # print(len(seed_ranges), f"{(27)}")
    # print(len(seed_ranges), "(27)")
    seed_ranges.sort()
    # print(seed_ranges[:10])
    print()
    print(seed_ranges)
    return seed_ranges[0][0]
    # print(seed_ranges)

print(f"Part 1 answer: {solve_part_1()}")
# > 92743746
# > 23652296
print(f"Part 2 answer: {solve_part_2()}")

