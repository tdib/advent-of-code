# https://adventofcode.com/2022/day/9

# Element-wise tuple addition
# e.g. (1, 0) + (4, 2) = (5, 2)
def add_tuples(tup1, tup2):
  return tuple(i + j for i, j in zip(tup1, tup2))


# How does pos1 have to move to get the pos2?
def get_relative_direction(pos1, pos2):
  x1, y1 = pos1
  x2, y2 = pos2
  return (x2-x1, y2-y1)

# Given an index, alter the position of the element at said index according to
# the element in front of it (and whether it needs to move)
def follow_leader(idx, rope_positions, visited):
  # Find out how far the current index must travel to reach the item in front (i.e. leader)
  curr_pos = rope_positions[idx]
  leader_pos = rope_positions[idx-1]
  relative_direction = get_relative_direction(curr_pos, leader_pos)

  # If the leader is not an immediate neighbour/is 2+ positions away
  relative_x, relative_y = relative_direction
  if abs(relative_x) > 1 or abs(relative_y) > 1:
    # We move the current index towards that position
    move(idx, relative_direction, rope_positions, visited)

# Move a rope element at a given axis using a move vector
# Note: the move vector only defines the *direction*, not the amount.
# Every element will be capped at 1 cell movement either orthogonally diagonally
def move(idx, move_vector, rope_positions, visited):
  # Cap the movement to 1 cell
  # e.g. (-2, 3) -> (-1, 1)
  # The absolute value of each value is reduced to 1
  move_x, move_y = move_vector
  capped_relative_direction = (max(min(1, move_x), -1), max(min(1, move_y), -1))

  # Move the current index in the specified direction
  rope_positions[idx] = add_tuples(rope_positions[idx], capped_relative_direction)

  # Perform tail tracking
  if idx == len(rope_positions) - 1:
    visited.add(rope_positions[idx])


# Do file parsing stuff
with open('input.txt', 'r') as f:
  lines = f.readlines()
# Remove newlines
lines = [line.strip() for line in lines]
# Split strings into tuples, e.g. ('R', '1')
lines = list(map(lambda instruction: tuple(instruction.split(' ')), lines))
# Map second elements into ints, e.g. ('R', 1)
lines = list(map(lambda move: (move[0], int(move[1])), lines))

# Generic function to solve for any length of rope
def solve(rope_length):
  # Keep track of the elements that are visited
  # (0, 0) is already contained because the tail starts here and the tracking
  # only occurs during a move
  visited = set((0, 0))

  # Map a direction character to tuples
  # This is only used for the head, as the rest of the elements
  # simply compute the tuple directly for their movement
  direction_map = {
    'R': (1, 0),
    'U': (0, 1),
    'L': (-1, 0),
    'D': (0, -1),
  }
  # Define the positions of each point in the rope
  # Position 0 is the head, and the last is the tail
  rope_positions = [(0, 0)] * rope_length

  # Every line has a direction to travel, and amount to travel in that direction
  for direction, amount in lines:
    # For the current direction, we do it x times
    for _ in range(amount):
      # Move the head (index 0)
      move(0, direction_map[direction], rope_positions, visited)
      # For every other element in the rope (i.e. everything but the head),
      # we adjust its position according to the element in front of it
      for idx in range(1, len(rope_positions)):
        follow_leader(idx, rope_positions, visited)
  
  return len(visited)

print(solve(2))
print(solve(10))