# Map a-z to 1-26 and A-Z to 27-52 respectively
def map_char_priority(char):
  LOWERCASE_OFFSET = 96
  UPPERCASE_OFFSET = 38
  return ord(char) - UPPERCASE_OFFSET if char.isupper() else ord(char) - LOWERCASE_OFFSET

with open('input.txt', 'r') as f:
  lines = f.readlines()

  ### Part 1 ###
  total = 0
  for line in lines:
    # Split rucksack into two equal portions and find common elements (characters)
    first_compartment = line[:len(line)//2]
    second_compartment = line[len(line)//2:]
    common_items = set(first_compartment) & set(second_compartment)

    # Add each of the item priorities to the total
    for item in common_items:
      total += map_char_priority(item)
  ##############


  ### Part 2 ###
  total_part2 = 0

  # Sliding window value for part 2
  n = 3

  # Split input into n groups
  for i in range(0, len(lines)//n):
    curr_group = []

    # Sliding window for groups - add each rucksack in a window to the array
    for line in lines[i*n:i*n+n]:
      curr_group.append(line.strip())

    # Find the character that intersects all n rucksacks
    group_char = next(iter(set.intersection(*map(set, curr_group))))

    # Extract the priority and add to the total
    total_part2 += map_char_priority(group_char)
  ##############

  print('Part 1 answer:', total)
  print('Part 2 answer:', total_part2)