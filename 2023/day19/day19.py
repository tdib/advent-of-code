# https://adventofcode.com/2023/day/19
import re

with open("input.txt") as f:
    workflows, assignments = f.read().split("\n\n")

def parse_workflow(workflow_name, variables, workflow_map):
    rules = workflow_map[workflow_name]
    for rule in rules:
        if ":" not in rule:
            if rule == "A":
                return True
            elif rule == "R":
                return False
            else:
                return parse_workflow(rule, variables, workflow_map)

        variable_val = variables[rule[0]]
        operation = rule[1]

        num_to_compare, next_workflow = rule[2:].split(":")
        num_to_compare = int(num_to_compare)

        if (operation == ">" and variable_val > num_to_compare) or (operation == "<" and variable_val < num_to_compare):
            if next_workflow == "A": return True
            elif next_workflow == "R": return False
            else: return parse_workflow(next_workflow, variables, workflow_map)


def solve_part_1():
    # Parse workflows
    workflow_map = {}
    for workflow in workflows.split():
        workflow_identifier, rules = workflow[:-1].split("{")
        rules = rules.split(",")
        workflow_map[workflow_identifier] = rules
    
    # Parse variables
    variables = []
    for assignment in assignments.split():
        matches = list(map(int, re.findall(r"(\d+)", assignment)))
        variables.append({
            "x": matches[0],
            "m": matches[1],
            "a": matches[2],
            "s": matches[3]
        })
    
    # For every variable, check the "in" workflow and if it is accepted then add to total
    total = 0
    for var_instance in variables:
        if parse_workflow("in", var_instance, workflow_map):
            total += sum(var_instance.values())
        # print(var_instance)

    return total

def solve_part_2():
    ans = 0
    return ans

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")