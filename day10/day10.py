
with open('/Users/dib/dev/advent-of-code-2022/day10/input.txt', 'r') as f:
  lines = f.readlines()

# Remove newlines
lines = list(map(str.strip, lines))

def addx(arg):
  global register
  global sprite_position
  global sprite_position_str
  register += arg
  move_sprite_pos_to(register)

def noop(arg):
  pass

register = 1
instructions = {
  'addx': (addx, 2),
  'noop': (noop, 1),
}
curr_cycle = 0
buffer = None
notable_cycles = [20, 60, 100, 140, 180, 220, 260]
signal_strengths = []
current_crt_row = ''
crt_rows = []
sprite_position_str = '1'*3 + '0'*37

def move_sprite_pos_to(idx):
  global sprite_position_str
  sprite_position_str = '0' * 40
  if 0 < idx < 40:
    sprite_position_str = sprite_position_str[:idx-1] + '1'*3 + sprite_position_str[idx+2:]
  elif idx == 0:
    sprite_position_str = '1'*2 + '0'*38
  elif idx == -1:
    sprite_position_str = '1' + '0'*39



def check_notable_cycle(cycle):
  global current_crt_row
  if cycle in notable_cycles:
    signal_strengths.append(cycle * register)

  if (cycle-1) % 40 == 0:
    crt_rows.append(current_crt_row)
    current_crt_row = ''
  
def thing():
  print('cycle', curr_cycle)
  print(f'register {register}')
  print(sprite_position_str, len(sprite_position_str))
  print(''.join(current_crt_row)+'?')

for line in lines:
  while buffer is not None and buffer[1] != 0:

    buffer[1] -= 1
    curr_cycle += 1
    check_notable_cycle(curr_cycle)
    # print(f'{register=}')
    # thing()
    # input()

    if sprite_position_str[curr_cycle%40-1] == '1':
      current_crt_row += '#'
    else:
      current_crt_row += '.'

    if buffer[1] == 0:
      buffer[0](buffer[2])
      buffer = None
    
  split = line.split(' ')
  instruction = split[0]
  argument = int(split[1]) if len(split) == 2 else None
  buffer = [instructions[instruction][0], instructions[instruction][1], argument]

print(signal_strengths)
print(sum(signal_strengths))

crt_rows.append(current_crt_row)
for crt_row in crt_rows:
  print(''.join(crt_row))
