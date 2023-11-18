import copy

with open('/Users/dib/dev/advent-of-code-2022/day11/test.txt', 'r') as f:
  lines = list(map(str.strip, f.readlines()))

class Monkey:
  def __init__(self, items, inspect_op, inspect_value, divisor, true_monkey, false_monkey):
    self.items = items
    self.inspect_op = inspect_op
    self._inspect_value = inspect_value
    self.divisor = int(divisor)
    self.true_monkey = int(true_monkey)
    self.false_monkey = int(false_monkey)
  
  def inspect_value(self):
    return self.items[0] if self._inspect_value == 'old' else int(self._inspect_value)

  def get_next_recipient(self, monkeys):
    if self.items[0] % self.divisor == 0:
      recipient_monkey_idx = self.true_monkey
    else:
      recipient_monkey_idx = self.false_monkey

    recipient_monkey = monkeys[recipient_monkey_idx]
    return recipient_monkey
  
  def pass_item(self, recipient):
    recipient.items.append(self.items.pop(0))

  def inspect_item(self, will_get_bored, mod):
    if will_get_bored:
      self.items[0] = (self.inspect_op(self.items[0], self.inspect_value()) // 3) % mod
    else:
      self.items[0] = (self.inspect_op(self.items[0], self.inspect_value())) % mod

# Parse file to create list of monkey objects
# Used to reset the question to the original state for part 1/2
def populate_data():
  monkeys = []
  curr_monkey_data = []

  # Map string operations to their respective functions
  op_map = {
    '+': int.__add__,
    '*': int.__mul__,
  }

  for idx, line in enumerate(lines):
    # When we hit a newline or end of file, we should process the data we have
    if not line or idx == len(lines)-1:
      # If we are on the last line of the file
      if idx == len(lines) - 1:
        curr_monkey_data.append(line)

      _, items, operation, test_condition, if_true, if_false = curr_monkey_data

      # List of starting items for monkey e.g. [79, 98]
      items = list(map(int, items.split(': ')[1].split(', ')))

      # e.g. [..., '=', 'old', '*', '19']
      operation_split = operation.split(' ')
      # Operation function for manipulating the item value, e.g. __mul__
      operation = op_map[operation_split[-2]]
      # Value to manipulate the item by, e.g. 19
      relevant_value = operation_split[-1]

      # Divisor for the test, e.g. test if item is divisible by 23
      divisor = test_condition.split(' ')[-1]

      # Monkey to pass to if the item is divisible by the divisor
      monkey_if_true = if_true.split(' ')[-1]
      # Monkey to pass to if the item is not divisible by the divisor
      monkey_if_false = if_false.split(' ')[-1]
    
      # Create a monkey object
      monkeys.append(
        Monkey(
          items,
          operation,
          relevant_value,
          divisor,
          monkey_if_true,
          monkey_if_false
        )
      )
      # Reset for the next iteration
      curr_monkey_data = []
    else:
      curr_monkey_data.append(line)
    
  return monkeys


def solve(part, num_rounds, will_get_bored):
  monkeys = populate_data()
  num_inspections = [0] * len(monkeys)

  # Compute the mod as the product of all test divisors
  # This changes nothing about the divisibility checks, but keeps
  # the values small enough which is necessary to optimise the speed
  # for this problem
  mod = 1
  for m in monkeys:
    mod *= m.divisor

  # Go for x rounds
  for _ in range(num_rounds):
    # Go through each monkey
    for i, monkey in enumerate(monkeys):
      # Go through each item - we use _ because the current item
      # will always be index 0, which is handled by the Monkey class
      for _ in range(len(monkey.items)):
        num_inspections[i] += 1
        # Run the computation on the value, and pass it to the next monkey
        monkey.inspect_item(will_get_bored, mod)
        monkey.pass_item(monkey.get_next_recipient(monkeys))

  num_inspections.sort()
  print(f'Part {part} answer: {num_inspections[-1] * num_inspections[-2]}')

solve(1, 20, True)
solve(2, 10000, False)