# https://adventofcode.com/2025/day/08
import math
from functools import cache
from typing import cast

from util.util import read_as_lines

# Read in the input as a list of 3d positions
points: list[tuple[int, int, int]] = cast(
    list[tuple[int, int, int]],
    list(
        map(lambda line: tuple(map(int, line.split(","))), read_as_lines("input.txt"))
    ),
)


@cache
def make_graph():
    """
    Construct a graph for point (A -> B) that maps to its distance.
    Note that this does not consider the same point backwards (i.e. B -> A),
    just the first way that is found across the points
    """
    graph = {}
    for point in points:
        for other_point in points:
            if (
                point == other_point
                or (point, other_point) in graph
                or (other_point, point) in graph
            ):
                continue
            dist = math.sqrt(
                (point[0] - other_point[0]) ** 2
                + (point[1] - other_point[1]) ** 2
                + (point[2] - other_point[2]) ** 2
            )
            assert point != other_point
            graph[(point, other_point)] = dist
    return graph


def find_circuit_idx(circuits, target):
    """
    Finds the index of a target position within the circuits list.
    e.g. given [[a], [b], [c], [d, e], [f]], searching for `e` will
    output index 3
    """
    for i, circuit in enumerate(circuits):
        if target in circuit:
            return i
    raise AssertionError("unreachable")


def merge_circuits(circuits, i, j):
    """
    Merge two circuit lists. e.g. given circuits [[a], [b], [c], [d, e], [f]],
    merging 0 and 3 will output [[a, d, e], [b], [c], [f]]. Attempting to merge
    two indexes that are already in the same circuit will do nothing
    """
    if i == j:
        return circuits
    circuits[i] = circuits[i] + circuits[j]
    del circuits[j]
    return circuits


def solve_part_1():
    graph = make_graph()
    sorted_min_dist = sorted(graph.items(), key=lambda kv: kv[1])

    circuits = [[p] for p in points]
    for i, (k, _) in enumerate(sorted_min_dist):
        source_idx = find_circuit_idx(circuits, k[0])
        target_idx = find_circuit_idx(circuits, k[1])
        if i == 1000:
            if source_idx != target_idx:
                circuits = merge_circuits(circuits, source_idx, target_idx)
            break

        if source_idx == target_idx:
            continue
        circuits = merge_circuits(circuits, source_idx, target_idx)

    sorted_largest_circuits = sorted(
        [len(circuit) for circuit in circuits], reverse=True
    )
    ans = 1
    for circuit_length in sorted_largest_circuits[:3]:
        ans *= circuit_length

    return ans


def solve_part_2():
    graph = make_graph()
    sorted_min_dist = sorted(graph.items(), key=lambda kv: kv[1])

    circuits = [[p] for p in points]
    for k, _ in sorted_min_dist:
        source_idx = find_circuit_idx(circuits, k[0])
        target_idx = find_circuit_idx(circuits, k[1])

        if source_idx == target_idx:
            continue

        # We are merging the final two circuits
        if len(circuits) == 2:
            return k[0][0] * k[1][0]
        circuits = merge_circuits(circuits, source_idx, target_idx)

    return None


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
