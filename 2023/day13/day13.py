with open("input.txt") as f:
    lines = list(map(lambda x: x.splitlines(), f.read().split("\n\n")))

def find_mirror(g, is_part_2=False):
    for i in range(1, len(g)):
        top = g[:i][::-1]
        bot = g[i:]

        # Truncate longer array
        top = top[:len(bot)]
        bot = bot[:len(top)]

        if (not is_part_2 and top == bot) or (is_part_2 and count_diff(top, bot) == 1):
            return i

    return 0

def count_diff(a, b):
    diff = 0
    for x, y in zip(a, b):
        for i, j in zip(x, y):
            if i != j: diff += 1
    return diff

def solve_part_1():
    ans = 0
    for g in lines:
        # Check rows
        if res := find_mirror(g):
            ans += 100 * res
            continue
        
        # Check cols (by transposing grid)
        ans += find_mirror(list(zip(*g)))

    return ans

def solve_part_2():
    ans = 0
    for g in lines:
        # Check rows
        if res := find_mirror(g, is_part_2=True):
            ans += 100 * res
        
        # Check cols (by transposing grid)
        ans += find_mirror(list(zip(*g)), is_part_2=True)

    return ans

print(f"Part 1 answer: {solve_part_1()}, (36448)")
print(f"Part 2 answer: {solve_part_2()}")