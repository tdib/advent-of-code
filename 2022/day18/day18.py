# https://adventofcode.com/2022/day/18
from collections import deque

with open('input.txt') as f:
    lines = list(map(str.strip, f.readlines()))

DIRECTIONS = ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1))

def add_vector(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def get_cubes():
    cubes = set()
    for line in lines:
        x, y, z = map(int, line.split(','))
        cubes.add((x, y, z))
    return cubes

def get_exposed_faces(cubes):
    exposed_faces = 0
    for cube in cubes:
        faces = 6
        for n in DIRECTIONS:
            if add_vector(cube, n) in cubes:
                faces -= 1
        exposed_faces += faces

    return exposed_faces

def bfs(start, air, cubes):
    out_of_range = False
    q = deque([start])
    v = set()

    while q:
        curr = q.popleft()
        v.add(curr)

        # Air is defined at the bounds of our cubes, so if this
        # condition is true, it means we are in space where a search
        # is unnecessary - setting the out of range flag indicates that
        # we are not searching inside of an air pocket
        if curr not in air and curr not in cubes:
            out_of_range = True
            continue
        
        # Expand from this current position
        for dir in DIRECTIONS:
            next = add_vector(curr, dir)
            if next not in v and next not in q and next not in cubes:
                q.append(next)

    # If this flag is true, it means we have visited ONLY the exterior
    # air which is irrelevant - remove it all and return True.
    # The calling function will not continue because we are returning True
    if out_of_range:
        outside_air = v.intersection(air)
        air.difference_update(outside_air)
        return True

def solve_part_1():
    cubes = get_cubes()
    return get_exposed_faces(cubes)

def solve_part_2():
    cubes = get_cubes()
    exposed_faces = get_exposed_faces(cubes)

    # Find the bounds of each axis
    min_x, min_y, min_z = [min(cubes, key=lambda cube: cube[i])[i] - 1 for i in range(3)]
    max_x, max_y, max_z = [max(cubes, key=lambda cube: cube[i])[i] + 1 for i in range(3)]

    # Create ranges for each axis
    x_range = range(min_x, max_x+1)
    y_range = range(min_y, max_y+1)
    z_range = range(min_z, max_z+1)

    # Compute all positions within the bounds
    all_positions = {(x, y, z) for x in x_range for y in y_range for z in z_range}

    # The difference of all position and cubes is air
    air = all_positions - cubes
    for cube in air:
        # We search from the given point to find all the connected air.
        # If bfs returns true, it means we are on the exterior, and the
        # search would have removed all connected air blocks, leaving us
        # with only (placed/filled) cubes
        if bfs(cube, air, cubes): break

    # Now that we have only air pockets, we can search through each of them
    # quite efficiently
    for air_pocket in air:
        # If any of the neighbouring blocks are cubes, we have one less
        # exposed face
        for dir in DIRECTIONS:
            if add_vector(air_pocket, dir) in cubes:
                exposed_faces -= 1

    return exposed_faces

print(f'Part 1 answer: {solve_part_1()}')
print(f'Part 2 answer: {solve_part_2()}')
