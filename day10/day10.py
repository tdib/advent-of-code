with open('/Users/dib/dev/advent-of-code-2022/day10/input.txt', 'r') as f:
  lines = map(str.strip, f.readlines())

# Function for addx instruction
# Adds the specified value to the register, and moves the sprite position
# Note: This is only called after the 2 cycles have completed
def addx(val):
  global register
  register += val
  # move_sprite_pos_to(register)

# Function for the noop instruction
# This does nothing
# Note: This is only called after the 1 cycle has passed
def noop(_):
  return

# Compute a string representing the current sprite position
def get_sprite_pos(register):
  return ''.join(['1' if i in range(register-1, register+2) else '0' for i in range(40)])

# Check if we need to take special action on a given cycle
def check_notable_cycle(cycle):
  # Part 1: Get the signal strength for this cycle
  if cycle in notable_cycles:
    signal_strengths.append(cycle * register)

  # Part 2: Get the CRT row for this cycle
  global current_crt_row
  if cycle in notable_crt_cycles:
    crt_rows.append(current_crt_row)
    current_crt_row = ''

# Step by step, display the output of the current sprite position
# and CRT row to ensure everything is being computed properly
def debug_part_2():
  print(f'{curr_cycle=}')
  print(f'{register=}')
  sprite_pos = get_sprite_pos(register)
  print(sprite_pos, len(sprite_pos))

  print(''.join(current_crt_row) + '?')
  input()

### Part 1 ###
# Current value of the register
register = 1
# Current cycle
curr_cycle = 0
# Map strings to the instruction functions and number of cycles to complete
instructions = {
  'addx': (addx, 2),
  'noop': (noop, 1),
}
# Buffer used for determining which instruction is being completed
# In the format [<instruction_function>, <num_cycles_to_complete>, <argument>]
buffer = None
# Notable cycles for part 1
# Used to compute the sum of signal strengths
notable_cycles = [20, 60, 100, 140, 180, 220, 260]
# Store each of the signal strengths
signal_strengths = []
##############

### Part 2 ###
# Temporarily store the current CRT row
current_crt_row = ''
# The full screen after having constructed each row
crt_rows = []
# Which cycles will we have a completed CRT row?
notable_crt_cycles = [41, 81, 121, 161, 201]
# Characters to define how the CRT is diaplyed
CHAR_FILLED = '#'
CHAR_EMPTY = '.'
##############

for line in lines:
  # Parse the instruction and argument of the current line
  split = line.split(' ')
  instruction = split[0]
  argument = int(split[1]) if len(split) == 2 else None
  # Add the necessary information to the buffer
  buffer = [instructions[instruction][0], instructions[instruction][1], argument]

  # If we have something in our buffer
  while buffer is not None:
    # Decrement the current instruction wait time
    buffer[1] -= 1
    # Increase the clock cycle
    curr_cycle += 1
    # Check if anything interesting should happen in this cycle
    check_notable_cycle(curr_cycle)

    # Uncomment for a more visual interpretation of part 2
    # including the sprite position and CRT row construction
    # debug_part_2()

    # Determine what character needs to be added to the CRT row
    if get_sprite_pos(register)[curr_cycle % 40 - 1] == '1':
      current_crt_row += CHAR_FILLED
    else:
      current_crt_row += CHAR_EMPTY

    # If the instruction countdown has completed, execute it and reset the buffer
    if buffer[1] == 0:
      buffer[0](buffer[2])
      buffer = None

print('Part 1 answer:')
print(sum(signal_strengths))

print()

print('Part 2 answer:')
crt_rows.append(current_crt_row)
for crt_row in crt_rows:
  print(''.join(crt_row))
