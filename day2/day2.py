# Part 1
# A/X: rock
# B/Y: paper
# C/Z: scissors

# Part 2
# X: lose
# Y: draw
# Z: win

SCORE_WIN = 6
SCORE_DRAW = 3

# A wins against C...
wins = {
  'A': 'C',
  'B': 'A',
  'C': 'B',
}

# A loses against B...
loses = {
  'A': 'B',
  'B': 'C',
  'C': 'A'
}

scores = {
  'A': 1,
  'B': 2,
  'C': 3,
}

char_map = {
  'X': 'A',
  'Y': 'B',
  'Z': 'C'
}

with open('input.txt', 'r') as f:
  lines = f.readlines()

  total = 0
  total_part2 = 0
  for line in lines:
    opp_choice, my_choice = line.strip().split(' ')

    ### Part 2 ###
    match my_choice:
      case 'X': # Lose
        total_part2 += scores[wins[opp_choice]]
      case 'Y': # Draw
        total_part2 += scores[opp_choice] + SCORE_DRAW
      case 'Z': # Win
        total_part2 += scores[loses[opp_choice]] + SCORE_WIN
    ##############

    # Convert X, Y, Z into A, B, C respectively
    my_choice = char_map[my_choice]
    
    # Add the initial score based off my choice
    total += scores[my_choice]
    # Add the bonus score depending on outcome
    if wins[my_choice] == opp_choice: # Win
      total += SCORE_WIN
    if my_choice == opp_choice: # Draw
      total += SCORE_DRAW

  print('Part 1 answer:', total)
  print('Part 2 answer:', total_part2)