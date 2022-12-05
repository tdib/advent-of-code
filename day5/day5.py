with open('input.txt', 'r') as f:
  lines = f.readlines()

stacks = []
for line in lines:
  row = []
  if '[' in line or ']' in line:
    # print('HEY', line)
    for i in range(len(line) // (3 + len(line) % 3) ):
      cargo = line[i+i*3:i+i*3+3:]
      row.append(cargo.strip('[]'))

    stacks.append(row[:-1])
    continue

  if '[' not in line or ']' not in line:
    stacks = [list(x) for x in zip(*stacks)]
    for idx, stack in enumerate(stacks):
      # print('stack', stack)
      if '   ' in stack:
        stack = list(filter(lambda x: x != '   ', stack))
        stacks[idx] = stack
    for stack in stacks:
      print(stack)
  if line == '\n' or '[' not in line or ']' not in line:
    break

marker = False
for line in lines:
  if line == '\n':
    marker = True
    continue

  if marker:
    _, how_many, _, from_stack, _, to_stack = line.strip().split(' ')
    how_many = int(how_many)
    from_stack = int(from_stack)-1
    to_stack = int(to_stack)-1
    # print(stacks)
    # moving_blocks = list(reversed(stacks[from_stack][:how_many])) # Part 1

    ### Part 2 ###
    moving_blocks = stacks[from_stack][:how_many]
    ##############

    stacks[from_stack] = stacks[from_stack][how_many:]
    stacks[to_stack] = [*moving_blocks, *stacks[to_stack]]
  

# print('stacks', stacks)
# print([stacks[i][0] for i in range(len(stacks))])
for i in range(len(stacks)):
  print(stacks[i][0])

# print('Part 1 answer:', total)
# print('Part 2 answer:', total_part2)