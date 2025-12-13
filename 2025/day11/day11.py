# https://adventofcode.com/2025/day/11
from functools import cache

from util.util import read_as_lines

lines = read_as_lines("input.txt")
graph = {}
for line in lines:
    source, dests = line.split(": ")
    graph[source] = dests.split()


def solve_part_1():
    ans = 0

    if "you" not in graph:
        print("Input not compatible with part 1")
        return -1
    start = graph["you"]
    queue = [*start]

    while len(queue):
        curr = queue.pop()
        if curr == "out":
            ans += 1
            continue

        queue.extend(graph[curr])

    return ans


def solve_part_2():
    # Between start node and "node of interest". We only consider paths
    # that do NOT include the other node of interest (i.e. directly to one)
    # so we don't have any overlap
    svr_fft = count_paths_between("svr", "fft", exclude="dac")
    svr_dac = count_paths_between("svr", "dac", exclude="fft")

    # Between nodes of interest
    fft_dac = count_paths_between("fft", "dac")
    dac_fft = count_paths_between("dac", "fft")

    # Nodes of interest to end. Similar to above, when we count "fft" to "out" paths,
    # we only want to consider cases where "fft" came second, so we ignore "dac" and
    # vice versa
    fft_out = count_paths_between("fft", "out", exclude="dac")
    dac_out = count_paths_between("dac", "out", exclude="fft")

    # Compute how many paths there are based on the subsets above
    # If A -> B has 15 paths, and B -> C has 20, then you can "combine"
    # them by multiplying
    fft_dac_path_count = svr_fft * fft_dac * dac_out
    dac_fft_path_count = svr_dac * dac_fft * fft_out

    return fft_dac_path_count + dac_fft_path_count


@cache
def count_paths_between(source: str, dest: str, exclude: str | None = None):
    """
    Count paths between `source` and `dest` nodes. `exclude` is used to early
    terminate the search when you don't want that node. For example:

    `count_paths_between("a", "c", "b")` will count the paths between "a" and
    "c", where "b" does NOT exist between them
    """
    if source == exclude:
        return 0

    if source == dest:
        return 1

    if source not in graph:
        return 0

    paths = 0
    for next in graph[source]:
        paths += count_paths_between(next, dest, exclude)

    return paths


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")
