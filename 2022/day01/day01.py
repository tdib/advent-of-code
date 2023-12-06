with open("input.txt") as f:
  lines = list(map(str.strip, f.readlines()))

all_sums = []
subtotal = 0
for line in lines:
    if not line:
        all_sums.append(subtotal)
        subtotal = 0
    else:
        subtotal += int(line)
# We will not encounter a newline at the end of the file so we must add the last number
# This is not necessary but here for completeness
all_sums.append(subtotal)

N = [1, 3]
a, b = [sum(sorted(all_sums)[-n:]) for n in N]
print(f"Part 1 answer: {a}")
print(f"Part 2 answer: {b}")
