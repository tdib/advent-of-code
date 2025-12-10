# https://adventofcode.com/2025/day/10
from dataclasses import dataclass

import z3

from util.util import read_as_lines

lines = read_as_lines("input.txt")


@dataclass
class Machine:
    light_target: list[bool]
    buttons: list[list[bool]]
    joltage_targets: list[int]


machines: list[Machine] = []
longest_target = 0
for line in lines:
    if (longest := len(line.split()[0].strip("[]"))) > longest_target:
        longest_target = longest

for line in lines:
    light_target, *buttons, joltages = line.split()
    light_target_new = [False] * longest_target
    for i, c in enumerate(light_target.strip("[]")):
        if c == "#":
            light_target_new[i] = True
    light_target = [c == "#" for c in light_target.strip("[]")]
    buttons_new = [[False] * longest_target for _ in range(len(buttons))]
    for button_i, button_possibilities in enumerate(buttons):
        indices = [int(b) for b in button_possibilities.strip("()").split(",")]
        for idx in indices:
            buttons_new[button_i][idx] = True

    joltage_targets = [int(j) for j in joltages.strip("{}").split(",")]
    machines.append(Machine(light_target_new, buttons_new, joltage_targets))


def solve_part_1():
    ans = 0

    for machine in machines:
        optimiser = z3.Optimize()
        button_vars = [z3.Bool(f"b{i}") for i in range(len(machine.buttons))]

        # Go through each light and construct an expression
        for target_idx in range(longest_target):
            # Light always starts as off
            expr = z3.BoolVal(False)

            # Find any button that affects the current light
            for button_idx, button_groups in enumerate(machine.buttons):
                if button_groups[target_idx]:
                    # Pressing this button performs an XOR operation on the light
                    expr = z3.Xor(expr, button_vars[button_idx])

            # Add a constraint that the XOR of all pressed buttons must equal the
            # target value (i.e. the button is in the target state after all the toggles)
            optimiser.add(expr == z3.BoolVal(machine.light_target[target_idx]))

        # Minimise the number of button presses
        optimiser.minimize(z3.Sum(z3.If(b, 1, 0) for b in button_vars))

        check = optimiser.check()
        assert check == z3.sat

        model = optimiser.model()
        pressed = [i for i, b in enumerate(button_vars) if model[b] == z3.BoolVal(True)]
        ans += len(pressed)

    return ans


def solve_part_2():
    ans = 0

    for machine in machines:
        optimiser = z3.Optimize()
        button_vars = [z3.Int(f"b{i}") for i in range(len(machine.buttons))]

        # Ensure the optimiser doesn't just choose negatives
        for b in button_vars:
            optimiser.add(b >= 0)

        # Create expression for one joltage at a time
        for target_idx in range(len(machine.joltage_targets)):
            # Initial will always be 0
            expr = z3.IntVal(0)

            # Find buttons that will affect the current joltage and add them
            # as an expression
            for button_idx, button_group in enumerate(machine.buttons):
                if button_group[target_idx]:
                    expr += button_vars[button_idx]

            # Add equality constraint so the int values should add up to the joltage target
            optimiser.add(expr == z3.IntVal(machine.joltage_targets[target_idx]))

        # Pick the smallest sum of button presses
        optimiser.minimize(z3.Sum(button_vars))

        check = optimiser.check()
        assert check == z3.sat

        model = optimiser.model()
        ans += sum([model[b].as_long() for b in button_vars])

    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
