with open('input.txt', 'r') as f:
  lines = f.readlines()

  num_redundant = 0
  num_overlap = 0
  for line in lines:
    # Separate the assignment pairs
    assignment_1, assignment_2 = line.strip().split(',')
    # Separate each of the assignments into upper and lower values
    lower_1, upper_1 = map(int, assignment_1.split('-'))
    lower_2, upper_2 = map(int, assignment_2.split('-'))
    # Create ranges for the respective assignments
    range_1 = range(lower_1, upper_1+1)
    range_2 = range(lower_2, upper_2+1)

    # Increment redundant counter if one range fully encapsulates another
    if (lower_1 <= lower_2 and upper_1 >= upper_2) or (lower_2 <= lower_1 and upper_2 >= upper_1):
      num_redundant += 1

    ### Part 2 ###
    # Find the intersecting elements of the ranges
    assignment_intersection = set(range_1).intersection(range_2)
    # If there are any elements in the intersecting set, we have found an overlap
    if len(assignment_intersection):
      num_overlap += 1
    ##############

  print('Part 1 answer:', num_redundant)
  print('Part 2 answer:', num_overlap)