# https://adventofcode.com/2023/day/22
from collections import deque, defaultdict
import re
import pickle
from util import *

colours = [C.RED, C.ORANGE, C.YELLOW, C.GREEN, C.CYAN, C.BLUE, C.PINK, C.PURPLE]

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

# Gnarly print method
def print_map(question_flag = False):
    items = Global.get_flattened_brick_positions()
    brick_volumes = Global.get_volume_map()

    max_x = max([x for x, _, _ in items])
    max_y = max([y for _, y, _ in items])
    max_z = max([z for _, _, z in items])

    print(" " * (max_x // 2) + "x" + " " * ((max_x // 2) + 1), end="")
    print("      ", end="")
    print(" " * (max_y // 2) + "y" + " " * (max_y // 2))
    for x in range(max_x + 1):
        print(str(x)[-1], end="")
    print("      ", end="")
    for x in range(max_y + 1):
        print(str(x)[-1], end="")
    print()
    for z in range(max_z, 0, -1):
        for x in range(max_x + 1):
            matches = [key for key, val in brick_volumes.items() for i, j, k in val if i==x and k==z]
            if len(matches) == 1 or (len(matches) and question_flag == False):
                symbol = f"{colours[matches[0] % len(colours)]}{str(matches[0])[-1]}{C.ENDC}"
                print(symbol, end="")
            elif len(matches) > 1 and question_flag == True:
                if not all(a == b for a, b in zip(matches, [*matches[1:], matches[0]])):
                    print(f"{C.BOLD}?{C.ENDC}", end="")
                else:
                    symbol = f"{colours[matches[0] % len(colours)]}{str(matches[0])[-1]}{C.ENDC}"
                    print(symbol, end="")
            else:
                print(".", end="")
        print(f" {z:3}  ", end="")
        for y in range(max_y + 1):
            matches = [key for key, val in brick_volumes.items() for i, j, k in val if j==y and k==z]
            if len(matches) == 1 or (len(matches) and question_flag == False):
                symbol = f"{colours[matches[0] % len(colours)]}{str(matches[0])[-1]}{C.ENDC}"
                print(symbol, end="")
            elif len(matches) > 1 and question_flag == True:
                if not all(a == b for a, b in zip(matches, [*matches[1:], matches[0]])):
                    print(f"{C.BOLD}?{C.ENDC}", end="")
                else:
                    symbol = f"{colours[matches[0] % len(colours)]}{str(matches[0])[-1]}{C.ENDC}"
                    print(symbol, end="")
            else:
                print(".", end="")
        print()

    for x in range(max_x + 1):
        print("-", end="")
    print("   0  ", end="")
    for x in range(max_y + 1):
        print("-", end="")
    print()


class Global:
    bricks = {}

    def get_flattened_brick_positions():
        """
        Return flattened structure containing all occupied positions globally.

        e.g. { (0, 1, 0), (0, 2, 0), (0, 3, 0), (1, 0, 0), (2, 0, 0) }
        """
        brick_positions = [b.volume for b in Global.bricks.values()]
        flattened_brick_positions = set(p for positions in brick_positions for p in positions)
        return flattened_brick_positions
    
    def get_volume_map():
        """
        Return { id: volume } map for all bricks
        """
        return { b.id: b.volume for _, b in Global.bricks.items() }

    def position_occupied(pos):
        brick_positions = [b.volume for b in Global.bricks.values()]
        flattened_brick_positions = [p for positions in brick_positions for p in positions]
        return pos in flattened_brick_positions

    def get_brick_id_at_pos(pos):
        for brick_id, brick_positions in Global.get_volume_map().items():
            if pos in brick_positions:
                return brick_id
        return None



class Pos:
    def __init__(self, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
    
    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def __lt__(self, other):
        a = (self.x, self.y, self.z)
        b = (other.x, other.y, other.z)
        return a < b

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __hash__(self):
        return hash(tuple(self))
    
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

class Brick:
    # brick_num = "A"
    brick_num = 1
    def __init__(self, start_pos, end_pos):
        self.x1, self.y1, self.z1 = start_pos
        self.x2, self.y2, self.z2 = end_pos
        self.id = Brick.brick_num
        # Brick.brick_num = chr(ord(Brick.brick_num) + 1)
        Brick.brick_num += 1
        self.volume = self.fill_volume()
        self.depends_on_me = []

    def __hash__(self):
        return hash(self.volume)

    def will_fall(self, brick_positions):
        new_z1 = self.z1 - 1
        new_z2 = self.z2 - 1
        curr_key = self.volume

        if new_z1 >= 1 and new_z2 >= 1:
            new_filled = self.fill_dropped_volume()

            new_pos = set([*new_filled])
            flat_keys = set(pos for key in brick_positions for pos in key)

            return not new_pos.intersection(flat_keys.difference(curr_key))
        return False

    def fall(self):
        # print("falling with bricks", all_brick_positions)
        new_z1 = self.z1 - 1
        new_z2 = self.z2 - 1
        curr_key = self.volume

        if new_z1 >= 1 and new_z2 >= 1:
            new_key = self.fill_dropped_volume()

            flat_keys = Global.get_flattened_brick_positions()
            if set([*new_key]).intersection(flat_keys.difference(curr_key)):
                return False
            else:
                self.z1 = new_z1
                self.z2 = new_z2
                self.volume = new_key
                return True
        return False
    
    def __repr__(self):
        # return f"ID: {self.id} ({self.x1}, {self.y1}, {self.z1}) -> ({self.x2}, {self.y2}, {self.z2})"
        return f"ID: {self.id} {self.fill_volume()}"

    def fill_volume(self):
        return fill(Pos(self.x1, self.y1, self.z1), Pos(self.x2, self.y2, self.z2))

    def fill_dropped_volume(self):
        return fill(Pos(self.x1, self.y1, self.z1 - 1), Pos(self.x2, self.y2, self.z2 - 1))

def fill(a, b):
    x1, y1, z1 = a
    x2, y2, z2 = b
    ret = set()

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                ret.add(Pos(x, y, z))
    
    return tuple(sorted(ret))


def solve_part_1(use_pickle = False):
    i = 0
    print("Processing bricks...")
    for line in lines:
        i += 1
        coord1, coord2 = line.split("~")
        pos1 = Pos(*coord1.split(","))
        pos2 = Pos(*coord2.split(","))
        brick = Brick(pos1, pos2)

        Global.bricks[brick.id] = brick

    print("Simluating fall...")
    # The code is horribly unoptimise so not using pickle will result in the code taking a few minutes to run
    if use_pickle:
        with open("simulated_bricks.pkl", "rb") as f:
            Global.bricks = pickle.load(f)
    else:
        lowest_to_highest_bricks = list(sorted(Global.bricks.values(), key=lambda b: min(b.z1, b.z2)))
        for brick in lowest_to_highest_bricks:
            print("Falling:", brick)
            while brick.fall():
                pass
        with open("simulated_bricks.pkl", "wb") as f:
            pickle.dump(Global.bricks, f)


    print("Getting dependencies...")
    for brick in Global.bricks.values():
        max_z = max([pos.z for pos in brick.volume])
        top_layer = [pos for pos in brick.volume if pos.z == max_z]
        above_top = [Pos(x, y, z + 1) for x, y, z in top_layer]

        flattened_brick_positions = Global.get_flattened_brick_positions()
        for above_top_pos in above_top:
            if above_top_pos in flattened_brick_positions:
                above_brick_id = Global.get_brick_id_at_pos(above_top_pos)
                if above_brick_id not in brick.depends_on_me:
                    brick.depends_on_me.append(above_brick_id)
        

    # Go through each brick and temporarily remove it. Check each of the dependent bricks
    # to see if they would fall as a result - if so, then we can't disintegrate the current
    # brick, otherwise we can.
    print("Testing disintigration...")
    bricks_to_disintegrate = 0
    for brick in Global.bricks.values():
        # print("brick", brick)
        temp_bricks = Global.bricks.copy()
        del temp_bricks[brick.id]
        dependent_brick_ids = brick.depends_on_me
        dependent_bricks = [Global.bricks[brick_id] for brick_id in dependent_brick_ids]
        
        positions = [p.volume for p in temp_bricks.values()]
        if all(not b.will_fall(positions) for b in dependent_bricks):
            bricks_to_disintegrate += 1

    return bricks_to_disintegrate


def solve_part_2():
    ans = 0
    for line in lines:
        pass
    return ans


print(f"Part 1 answer: {solve_part_1(use_pickle=True)}")
print(f"Part 2 answer: {solve_part_2()}")
