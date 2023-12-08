# https://adventofcode.com/2023/day/8
import time
from collections import deque, defaultdict
from math import gcd, lcm
import math
from functools import reduce
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

class Node():
    def __init__(self, name, left, right):
        self.name = name
        self.children = (left, right)
        # self.left = left
        # self.right = right

    def __repr__(self):
        return self.name + "!"

m = {
    "L": 0,
    "R": 1,
}


def find(nodes, name):
    return next(filter(lambda x: x.name == name, nodes))

def solve_part_1():
    ans = 0
    dirs = lines[0]
    nodes = {}
    # print(dirs)
    for line in lines[2:]:
        s = line.split(" = ")
        name = s[0]
        s = s[1].split(", ")
        left = s[0][1:]
        right = s[1][:-1]
        # nodes.append(Node(name, left, right))
        nodes[name] = (left, right)
    
    # print(nodes)
    curr = "AAA"
    goal = "ZZZ"
    ans = 0
    found = False
    while True:
        for d in dirs:
            # print(curr)
            # print("MOving", d, m[d])
            curr_dir = m[d]
            curr = nodes[curr][curr_dir]
            ans += 1
            if curr == goal:
                found = True
                # print("??")
                break
        if found:
            break
    # print(ans)
    #     print(curr, type(curr))
    #     curr = find(nodes, find(nodes, curr.name).children[curr_dir].name)
    #     print(curr)
    




    return ans


def solve_part_2():
    ans = 0
    dirs = lines[0]
    nodes = {}
    # print(dirs)
    for line in lines[2:]:
        s = line.split(" = ")
        name = s[0]
        s = s[1].split(", ")
        left = s[0][1:]
        right = s[1][:-1]
        # nodes.append(Node(name, left, right))
        nodes[name] = (left, right)
    
    curr_nodes = []
    for node in nodes:
        if node.endswith("A"):
            curr_nodes.append(node)
    print("start", curr_nodes)

    # ans = []
    found = False
    ans = 0
    v = defaultdict(list)
    cycles = {}

    # while True:
    #     found = False
    #     num_steps = 0
    #     for i in range(len(curr_nodes)):
    #         if curr_nodes[i] in cycles:
    #             continue
    #         print("NOW TESTING", curr_nodes[i])
    #         for d in dirs:
    #             print(f"{curr_nodes[i]} -> ", end="")
    #             curr = nodes[curr_nodes[i]][m[d]]
    #             print(f"{curr}")
    #             num_steps += 1
    #             curr_nodes[i] = curr
    #             if curr not in v[curr]:
    #                 v[curr].append(curr)
    #             else:
    #                 if curr not in cycles and curr.endswith("Z"):
    #                     print("HERe")
    #                     # TODO: compute how long this cycle took
    #                     cycles[curr] = num_steps - v[curr].index(curr)
    #                     print("CYCLE FOUND FOR ", curr, cycles[curr])
    #                     found = True
    #                     break
    #         if found:
    #             break
    #     if found:
    #         continue

    for i in range(len(curr_nodes)):
        break
        print("Looking for cycle on ", curr_nodes[i])
        found_cycle = False
        num_steps = 0
        looking = curr_nodes[i]
        while True:
            for char_idx, d in enumerate(dirs):
                # print(f"{curr_nodes[i]} -> ", end="")
                curr = nodes[curr_nodes[i]][m[d]]
                # print(f"{curr}")
                num_steps += 1
                curr_nodes[i] = curr
                if (curr, char_idx) not in v[looking]:
                    # print("adding", curr, "to ", v[looking])
                    v[looking].append((curr, char_idx))
                else:
                    if curr.endswith("Z"):
                        # TODO: compute how long this cycle took
                        cycles[looking] = num_steps - v[looking].index((curr, char_idx)) - 1
                        # print(looking, curr, num_steps, v, v[curr], v[looking].index((curr, char_idx)))
                        # print("CYCLE FOUND FOR ", curr, cycles[looking])
                        found_cycle = True
                        break
            if found_cycle:
                break
        # print()


    # print(cycles, gcd(cycles.values()))
    # print(cycles.values())
    cycles = {'FQA': 18727, 'JSA': 24253, 'GJA': 18113, 'PBA': 22411, 'AAA': 21797, 'NNA': 16271}

    def find_lcm(nums):
        return reduce(lambda x, y: math.lcm(x,y), nums)
    
    # print("!!", find_lcm(list(cycles.values())))
    lcm = find_lcm(list(cycles.values()))
    print("LCM", lcm)

    
    curr_nodes = []
    for node in nodes:
        if node.endswith("A"):
            curr_nodes.append(node)
    # print("start", curr_nodes)
    print(cycles)


    # while not all(node.endswith("Z") for node in curr_nodes):
    #     print(curr_nodes)
    #     # time.sleep(1)
    #     for d in dirs:
    #         for i in range(len(curr_nodes)):
    #             print(curr_nodes[i], "movign", m[d], end='')
    #             curr = nodes[curr_nodes[i]][m[d]]
    #             # If there has not been a cycle
    #             if curr not in v[curr]:
    #                 # Keep track
    #                 v[curr].append(curr)
    #             # There has been a cycle
    #             else:
    #                 # We only want to set this once
    #                 if curr not in cycles:
    #                     # TODO: compute how long this cycle took
    #                     cycles[curr] = ans - v[curr].index(curr)
    #                     print("FOUND CYCLE FOR", curr, "length", cycles[curr])

                    
    #             # curr in 
    #             print(' to', curr)
    #             curr_nodes[i] = curr
    #             print(curr_nodes)
    #         ans += 1
    #         print()
    #         # if found:
    #             # break
    #     # ans.append(node_dist)
    # print(curr_nodes)
        
    # blah = max(ans)
    # print(blah * len(ans))
    print(ans)
    #     print(curr, type(curr))
    #     curr = find(nodes, find(nodes, curr.name).children[curr_dir].name)
    #     print(curr)
    




    return ans



# print(f"Part 1 answer: {solve_part_1()}")
#145518
print(f"Part 2 answer: {solve_part_2()}")

