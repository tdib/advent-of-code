# https://adventofcode.com/2015/day/2

with open("/Users/dib/dev/advent-of-code/2015/day02/input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

ans = 0
ans2 = 0
for line in lines:
    l, w, h = map(int, line.split('x'))
    formula = 2*l*w + 2*w*h + 2*h*l
    ans += formula + min(l*w, w*h, h*l)

    a, b, _ = sorted([l, w, h])
    present_ribbon = a + a + b + b
    bow_ribbon = l * w * h
    ans2 += present_ribbon + bow_ribbon

print(f'Part 1 answer: {ans}')
print(f'Part 2 answer: {ans2}')
