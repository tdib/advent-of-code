f = open('input.txt', 'r')
lines = f.readlines()

all_sums = []
subtotal = 0
for line in lines:
  if line == '\n':
    all_sums.append(subtotal)
    subtotal = 0
  else:
    subtotal += int(line)

n = 3
answer = sum(sorted(all_sums)[-n:])
print(answer)

f.close()