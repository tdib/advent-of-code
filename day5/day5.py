with open('input.txt', 'r') as f:
  lines = f.readlines()

stacks = []
stacks_part2 = []
parsed_blocks = False

for line in lines:
  # Horizontally parse each row at a time
  row = []
  # We are on a line that contains a block
  if '[' in line or ']' in line:
    # Compute how many blocks there are in the line
    line_length = len(line[:-1])
    for i in range((line_length-line_length//4) // 3):
      # Scan through each block in the row
      block = line[i+i*3:i+i*3+3]
      # Strip the block (of format "[X]") to just the character (e.g. "X")
      row.append(block[1:-1])
    stacks.append(row)
    continue
  # The current line does not contain a block
  else:
    # Do the following once
    if not parsed_blocks:
      # Transpose stacks (i.e. each stack should be its own array)
      stacks = [list(x) for x in zip(*stacks)]
      # Remove blank blocks from arrays
      for idx, stack in enumerate(stacks):
        if ' ' in stack:
          stack = list(filter(lambda x: x != ' ', stack))
          stacks[idx] = stack
      # Copy the stack for part 2 (as the crane actions work differently)
      stacks_part2 = stacks.copy()
      # Ensure the above computations only occur once
      parsed_blocks = True
      continue
    
    # Dividing line between stacks and instructions
    if line == '\n':
      continue

  # Extract information from current instruction
  _, how_many, _, from_stack, _, to_stack = line.strip().split(' ')
  how_many = int(how_many)
  from_stack = int(from_stack)-1
  to_stack = int(to_stack)-1

  # Calculate which blocks should be moved
  moving_blocks = list(reversed(stacks[from_stack][:how_many]))
  # Remove blocks from origin stack
  stacks[from_stack] = stacks[from_stack][how_many:]
  # Add stacks to new stack
  stacks[to_stack] = [*moving_blocks, *stacks[to_stack]]

  ### Part 2 ###
  # Calculate which blocks should be moved
  moving_blocks_part2 = stacks_part2[from_stack][:how_many]
  # Remove blocks from origin stack
  stacks_part2[from_stack] = stacks_part2[from_stack][how_many:]
  # Add stacks to new stack
  stacks_part2[to_stack] = [*moving_blocks_part2, *stacks_part2[to_stack]]
  ##############

print('Part 1 answer:', ''.join([stack[0] for stack in stacks]))
print('Part 2 answer:', ''.join([stack[0] for stack in stacks_part2]))