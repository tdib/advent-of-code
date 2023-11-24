# https://adventofcode.com/2015/day/8

with open('input.txt') as f:
    lines = list(map(str.strip, f.readlines()))

def solve_part_1():
    ans = 0
    for line in lines:
        # Using eval gives us the regular string after escapes
        # (i.e. does not include escaped characters)
        str_length = len(eval(line))
        # The line length is the number of characters in the line
        text_length = len(line)
        # Compute difference and add it
        ans += text_length - str_length
    
    return ans

def solve_part_2():
    ans = 0
    for line in lines:
        # Escape back slashes
        escaped = line.encode('unicode-escape').decode()
        # Add additional \ in front of "
        escaped = escaped.replace('"', '\\"')
        # Compute difference; +2 is used to account for the
        # \" at the start and end of the string
        ans += len(escaped) + 2 - len(line)

    return ans

print(f'Part 1 answer: {solve_part_1()}')
print(f'Part 2 answer: {solve_part_2()}')
