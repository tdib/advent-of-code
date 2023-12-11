# https://adventofcode.com/2023/day/11

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def sub_tuples(a, b):
    return (a[0] - b[0], a[1] - b[1])

def solve(expansion_factor):
    # Row expansion tracking
    curr_expansion = 0
    row_expansion = []
    for row, line in enumerate(lines):
        if "#" not in line:
            curr_expansion += 1
        row_expansion.append(curr_expansion)
    
    # Col expansion tracking
    transposed_space = list(zip(*lines))
    curr_expansion = 0
    col_expansion = []
    for row, line in enumerate(transposed_space):
        if "#" not in line:
            curr_expansion += 1
        col_expansion.append(curr_expansion)

    # Get coordinates of all galaxies
    galaxies = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                # Add the position of this galaxy, offsetting by the expansion of space
                galaxies.add((
                    row+row_expansion[row]*(expansion_factor-1),
                    col+col_expansion[col]*(expansion_factor-1)
                ))
    

    # Find the distance from every galaxy to every other one
    dists = {}
    for curr in galaxies:
        for other in galaxies:
            # We want to check every other node, not ourself
            if curr == other:
                continue
            else:
                # Order the pair in a consistent way - using python ordering is sufficient,
                # just so the pairs are not counted twice in inverse directions
                pair = (min(curr, other), max(curr, other))
                # Get a tuple representing the vector difference between the pairs
                dist_x, dist_y = sub_tuples(pair[1], pair[0])
                # Sum the values within the vector difference to get the distance between pairs
                # note: abs() is used because we don't care about negatives
                dist = abs(dist_x) + abs(dist_y)
                # Add this distance to the map
                if not pair in dists:
                    dists[pair] = dist
                else:
                    dists[pair] = min(dists[pair], dist)

    # dists now contains all galaxy pairs and the shortest distances between each.
    # Summing the values of this will give use the required answer
    return sum(dists.values())

def solve_part_1():
    return solve(2)

def solve_part_2():
    return solve(100000)

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

