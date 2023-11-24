# https://adventofcode.com/2015/day/7
from collections import deque

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def is_int(val):
    try:
        _ = int(val)
        return True
    except:
        return False

def parse_line(line, memory, buffer, part=1):
    operation_str, target_wire  = line.split(' -> ')
    s = operation_str.split()

    ### PART 2 ###
    # Hard wire b to answer to part 1
    if target_wire == 'b' and part == 2:
        memory[target_wire] = solve_part_1()
        return
    ##############

    match len(s):
        # We are assigning a value, e.g. 123 -> x
        case 1:
            try:
                val = int(s[0])
                memory[target_wire] = val
            except:
                if s[0] in memory:
                    memory[target_wire] = memory[s[0]]
                else:
                    buffer.append(line)
                    return None

        # We have a NOT operation, e.g. NOT x -> y
        case 2:
            # TODO: we don't ever need the try
            try:
                val = int(s[1])
                memory[target_wire] = ~val % 2**16
            except:
                val = s[1]
                if val in memory:
                    memory[target_wire] = ~memory[val] % 2**16
                else:
                    buffer.append(line)
                    return None

        # We have one of the other operations
        case 3:
            val_a = s[0]
            operation = op_map[s[1]]
            val_b = s[2]

            # Handle conversion of this value
            # If it is an int, then cast it
            if is_int(val_a):
                val_a = int(val_a)
            # We know it isn't an int, so if it isn't in memory,
            # just append it to our buffer and move on
            elif val_a not in memory:
                buffer.append(line)
                return None
            # We know we have some value in memory
            else:
                val_a = memory[val_a]
            
            # Same conversion process as above
            if is_int(val_b):
                val_b = int(val_b)
            elif val_b not in memory:
                buffer.append(line)
                return None
            else:
                val_b = memory[val_b]

            # At this point we have two integer values for a and b
            # so we can perform our operation
            memory[target_wire] = operation(val_a, val_b)

        # We should never reach this
        case _:
            print('ERROR')
            return None

    return True

op_map  = {
    'RSHIFT': lambda x, y: x >> y,
    'LSHIFT': lambda x, y: x << y,
    'NOT': lambda x: ~x % 65536,
    'AND': lambda x, y: x & y,
    'OR': lambda x, y: x | y
}

def solve_part_1():
    memory = {}
    buffer = deque()
    for line in lines:
        buffer.append(line)

    while len(buffer):
        parse_line(buffer.popleft(), memory, buffer)

    return memory['a']


def solve_part_2():
    memory = {}
    buffer = deque()
    for line in lines:
        buffer.append(line)

    while len(buffer):
        parse_line(buffer.popleft(), memory, buffer, part=2)
    
    return memory['a']

print(f'Part 1 answer: {solve_part_1()}')
print(f'Part 2 answer: {solve_part_2()}')
