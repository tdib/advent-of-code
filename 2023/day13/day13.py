with open("input.txt") as f:
    lines = f.read()

grids = list(map(lambda x: x.split("\n"), lines.split("\n\n")))

def solve_part_1():
    ans = 0
    for g in grids:
        found = False
        vert_mirror = True
        # Rows
        for i, (r1, r2) in enumerate(zip(g, g[1:])):
            mirror_size = min(len(g[:i]), len(g[i+2:]))
            top = g[:i]
            bot = g[i+2:]
            if len(top) > len(bot):
                top = list(reversed(list(reversed(top))[:mirror_size]))
            elif len(bot) > len(top):
                bot = bot[:mirror_size]

            if r1 == r2 and top == list(reversed(bot)):
                ans += 100 * (i + 1)
                found = True
                vert_mirror = False
                break
        
        if vert_mirror == False:
            continue

        g = list(zip(*g))
        for i, f in enumerate(g):
            g[i] = ''.join(f)

        # Cols
        for i, (c1, c2) in enumerate(list(zip(g, g[1:]))):
            mirror_size = min(len(g[:i]), len(g[i+2:]))
            top = g[:i]
            bot = g[i+2:]
            if len(top) > len(bot):
                top = list(reversed(list(reversed(top))[:mirror_size]))
            elif len(bot) > len(top):
                bot = bot[:mirror_size]

            if c1 == c2 and top == list(reversed(bot)):
                found = True
                ans += i + 1
                break
        
        if not found:
            raise RuntimeError("Mirror not found")
        
    return ans

def count_diff(a, b):
    diff = 0
    for x, y in zip(a, b):
        for i, j in zip(x, y):
            if i != j: diff += 1
    return diff

def solve_part_2():
    ans = 0
    for g in grids:
        found = False
        vert_mirror = True
        print("\n".join(g))
        # Rows
        print("rows")
        for i, (c1, c2) in enumerate(zip(g, g[1:])):
            mirror_size = min(len(g[:i]), len(g[i+2:]))
            top = g[:i]
            bot = g[i+2:]
            if len(top) > len(bot):
                top = list(reversed(list(reversed(top))[:mirror_size]))
            elif len(bot) > len(top):
                bot = bot[:mirror_size]
            
            row_diff = count_diff(c1, c2)

            if (c1 == c2 and count_diff(top, list(reversed(bot))) == 1) or (row_diff == 1 and count_diff(top, list(reversed(bot))) == 0):
                print("FOUND ROW", i+1)
                ans += 100 * (i + 1)
                found = True
                vert_mirror = False
                break
        print("rows complete")
        
        if vert_mirror == False:
            print("EARLY RETURN")
            print()
            continue
        
        print()
        g = list(zip(*g))
        for i, f in enumerate(g):
            g[i] = ''.join(f)

        print("cols")

        # Cols
        for i, (c1, c2) in enumerate(list(zip(g, g[1:]))):
            mirror_size = min(len(g[:i]), len(g[i+2:]))
            top = g[:i]
            bot = g[i+2:]
            if len(top) > len(bot):
                top = list(reversed(list(reversed(top))[:mirror_size]))
            elif len(bot) > len(top):
                bot = bot[:mirror_size]

            row_diff = count_diff(c1, c2)

            if (c1 == c2 and count_diff(top, list(reversed(bot))) == 1) or (row_diff == 1 and count_diff(top, list(reversed(bot))) == 0):
                print("FOUND COL", i+1)
                found = True
                ans += i + 1
                break
        
        if not found:
            raise RuntimeError("Mirror not found")
        
    return ans


# > 18765
# > 17765
print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")