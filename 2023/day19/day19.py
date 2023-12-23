# https://adventofcode.com/2023/day/19
from collections import deque
import re

with open("input.txt") as f:
    workflows, assignments = f.read().split("\n\n")

def parse_workflow(workflow_name, variables, workflow_map):
    rules = workflow_map[workflow_name]
    for rule in rules:
        if ":" not in rule:
            if rule == "A": return True
            elif rule == "R": return False
            else: return parse_workflow(rule, variables, workflow_map)

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

    return total

def solve_part_2():
    # Parse workflows
    workflow_map = {}
    for workflow in workflows.split():
        workflow_identifier, rules = workflow[:-1].split("{")
        rules = rules.split(",")
        workflow_map[workflow_identifier] = rules

    # Parse variables
    q = deque([("in", {
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000),
    })])
    accepted_assignment_ranges = []

    while q:
        curr_workflow, curr_assignment_ranges = q.popleft()

        # We don't actually have a workflow, we have an outcome, so handle accordingly
        if curr_workflow == "A":
            accepted_assignment_ranges.append(curr_assignment_ranges)
            continue
        elif curr_workflow == "R":
            continue

        rules = workflow_map[curr_workflow]
        for rule in rules:
            # If we're at a fallback, either accept the workflow, reject by doing nothing, or call the next workflow
            if ":" not in rule:
                if rule == "A": accepted_assignment_ranges.append(curr_assignment_ranges)
                elif rule != "R": q.append((rule, curr_assignment_ranges))
                continue

            # Rule parsing
            # "s<1351:px" -> "s"
            relevant_var = rule[0]
            # Finds the current range of the above variable we are dealing with.
            # For example, we start at (1, 4000), and will iteratively split into different ranges
            variable_min, variable_max = curr_assignment_ranges[relevant_var]
            # "s<1351:px" -> "<"
            operation = rule[1]
            # "s<1351:px" -> (1351, "px")
            num_to_compare, next_workflow = rule[2:].split(":")
            num_to_compare = int(num_to_compare)

            # Split the current range into multiple
            if operation == ">":
                new_range = (num_to_compare + 1, variable_max)
                remaining = (variable_min, num_to_compare)
            elif operation == "<":
                new_range = (variable_min, num_to_compare - 1)
                remaining = (num_to_compare, variable_max)

            # Add the new range to the next workflow
            new_assignment_ranges = curr_assignment_ranges.copy()
            new_assignment_ranges[relevant_var] = new_range
            q.append((next_workflow, new_assignment_ranges))

            # Whatever is left over replaces our assignment so we can send it
            # to a different workflow (which we can't access just yet)
            curr_assignment_ranges[relevant_var] = remaining

    # Sum the products of each accepted range allocation
    total = 0
    for a in accepted_assignment_ranges:
        sub = 1
        for v in a.values():
            sub *= v[1] - v[0] + 1
        total += sub

    return total

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")