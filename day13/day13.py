from itertools import zip_longest

with open('/Users/dib/dev/advent-of-code-2022/day13/input.txt', 'r') as f:
  lines = list(map(str.strip, f.readlines()))

def recursive_compare(l, r):
  print(type(l), l)
  print(type(r), r)

  if type(l) == list and type(r) == int:
    print(l, r, 'converting r')
    r = [r]
  elif type(l) == int and type(r) == list:
    print(l, r, 'converting l')
    l = [l]

  # Left ran out of elements before right
  if l is None and r is not None:
    print('Correct order - mixed')
    return True
  # Right ran out of elements before left
  if l is not None and r is None:
    print('Incorrect order - mixed')
    return False

  # Both lists
  if type(l) == list and type(r) == list:
    print(l, r, 'both lists')
    # recursive_compare(*l, *r)
    if l == [] and r == []:
      return
    for l, r in zip_longest(l, r):
      print(':)', l, r, type(l), type(r))
      x = recursive_compare(l, r)
      if x != None:
        return x
    
  # Both ints
  if type(l) == int and type(r) == int:
    print(l, r, 'both ints')
    if l < r:
      print('Correct order - int')
      return True
    elif l == r:
      print('Indeterminate order - int')
      return
    else:
      print('Incorrect order - int')
      return False


chunks = [lines[i:i+2] for i in range(0, len(lines), 3)]
indices = []
for idx, chunk in enumerate(chunks):
  left = eval(chunk[0])
  right = eval(chunk[1])

  for l, r in zip_longest(left, right):
    res = recursive_compare(l, r)
    # res = compare(l, r)
    if res == True:
      indices.append(idx+1)
    if res != None:
      print('res', res)
      print('-------------')
      break



    print()
  print()

print(indices)
print(len(indices))
print(sum(indices))
