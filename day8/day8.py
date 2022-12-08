# with open('./test.txt', 'r') as f:
with open(0) as f:
  lines = f.readlines()

for l in lines:
  print(l, end='')
print()
visible = set()

# left to right
for row, line in enumerate(lines):
  max_height = int(line[0])
  for col, tree in enumerate(line.strip()):
    print('CHECKIGN', (row, col), len(lines)-1, len(line)-1)
    if row == 0 or row == len(lines)-1:
      print('adding', (row, col))
      visible.add((row, col))
    elif col == 0 or col == len(line.strip())-1:
      print('adding', (row, col))
      visible.add((row, col))
    elif int(tree) > max_height:
      print('adding 3', (row, col))
      max_height = int(tree)
      visible.add((row, col))
    
# right to left
for row, line in enumerate(lines):
  if row == 0 or row == len(lines)-1:
    continue
  max_height = int(line.strip()[-1])
  for col, tree in enumerate(line[::-1].strip()):
    if int(tree) > max_height:
      max_height = int(tree)
      print('adding', (row, col))
      visible.add((row, col))


blah = [list(map(int, x)) for x in zip(*lines)]
print()
for b in blah:
  print(b)
# top to bottom
for row, line in enumerate(blah):
  max_height = int(line[0])
  for col, tree in enumerate(line):
    if int(tree) > max_height:
      print('adding', (col, row))
      max_height = int(tree)
      visible.add((col, row))
    
# bottom to top
for row, line in enumerate(blah):
  max_height = int(line[-1])
  for col, tree in enumerate(line[::-1]):
    if int(tree) > max_height:
      print('adding', (col, row))
      max_height = int(tree)
      visible.add((col, row))

for l in lines:
  print(l, end='')
print()

print(visible, len(visible))
print('Part 1 answer:', 0)
print('Part 2 answer:', 0)