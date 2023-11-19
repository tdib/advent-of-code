from itertools import zip_longest

with open('/Users/dib/dev/advent-of-code-2022/day13/input.txt', 'r') as f:
  lines = list(map(str.strip, f.readlines()))

# Compares two elements, returning true if they are in the correct order,
# and false otherwise
def recursive_compare(l, r):
  # One of the elements is an int and we must convert it to a list
  if type(l) == list and type(r) == int: r = [r]
  elif type(l) == int and type(r) == list: l = [l]

  # Left ran out of elements before right - correct order
  if l is None and r is not None: return True
  # Right ran out of elements before left - incorrect order
  if l is not None and r is None: return False

  # Both lists
  if type(l) == list and type(r) == list:
    for l, r in zip_longest(l, r):
      res = recursive_compare(l, r)
      if res != None: return res
    
  # Both ints
  if type(l) == int and type(r) == int:
    if l < r: return True
    elif l > r: return False

### Part 1 ###
chunks = [lines[i:i+2] for i in range(0, len(lines), 3)]
indices = []
for idx, chunk in enumerate(chunks):
  left = eval(chunk[0])
  right = eval(chunk[1])
  for l, r in zip_longest(left, right):
    res = recursive_compare(l, r)
    if res == True: indices.append(idx+1)
    if res != None: break

print(f'Part 1 answer: {sum(indices)}')
##############


### Part 2 ###
DISTRESS_1 = [[2]]
DISTRESS_2 = [[6]]
packets = [eval(line) for line in lines if line] + [DISTRESS_1, DISTRESS_2]

# Sort the packets, using recursive_compare as the comparison function
is_sorted = False
while not is_sorted:
  is_sorted = True
  for i in range(len(packets) - 1):
    # Current and next element are not in order - swap them
    if not recursive_compare(packets[i], packets[i+1]):
      packets[i], packets[i+1] = packets[i+1], packets[i]
      is_sorted = False

distress_idx_1 = packets.index(DISTRESS_1) + 1
distress_idx_2 = packets.index(DISTRESS_2) + 1
print(f'Part 2 answer: {distress_idx_1 * distress_idx_2}')
##############
