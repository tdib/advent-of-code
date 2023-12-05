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
        print()
        print("SEED", seed)
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
        print(out)
        all_things.append(out)
    print(all_things)
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


def solve_part_2():
    ans = 0
    for line in lines:
        pass
    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

