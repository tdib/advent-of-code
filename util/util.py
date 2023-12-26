from typing import Callable
from collections import deque
import re

class C:
    RED = "\033[91m"
    ORANGE = "\033[38;5;208m"
    YELLOW = "\033[38;5;220m"
    GREEN = "\033[92m"
    CYAN = "\033[36m"
    BLUE = "\033[94m"
    PINK = "\033[38;5;207m"
    PURPLE = "\033[38;5;93m"

    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    ENDC = "\033[0m"

# Alias print to d() to allow for quicker typing :^)
d = print

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

dir_to_str = { UP: "up", DOWN: "down", LEFT: "left", RIGHT: "right" }

dir_to_symbol = { UP: "^", DOWN: "v", LEFT: "<", RIGHT: ">" }
symbol_to_dir = { v: k for k, v in dir_to_symbol.items() }

WALL = "#"
EMPTY = "."

def get_nums(line: str) -> list[int]:
    """
    Given a line with numbers, return a list of all numbers (negatives included).
    """
    return list(map(int, re.findall(r"(-?\d+)", line)))

def limit_tuple(tup: tuple[int], magnitude: int, use_abs_value: bool = False) -> tuple[int]:
    """
    Given an n-dimensional tuple, limit the magnitude of its components. For example, given
    (1, 6, 3) with magnitude 5, the output would be (1, 5, 3).

    By default, the function ignores negatives, so (1, -6, 3) with magnitude 5 would output (1, -6, 3).
    If `use_abs_value` is set to true, the output would instead be (1, -5, 3).
    """
    if use_abs_value:
        return tuple(-1 * min(abs(t), magnitude) if t < 0 else min(abs(t), magnitude) for t in tup)
    else:
        return tuple(min(t, magnitude) for t in tup)

def add_tuples(t1: tuple[int], t2: tuple[int]) -> tuple[int]:
    """
    Add two n-dimensional tuples.

    ```
    t1 = (1, 2, 3)
    t2 = (0, 6, -2)
    assert add_tuples(t1, t2) == (1, 8, 1)
    ```
    """
    return tuple(elem1 + elem2 for elem1, elem2 in zip(t1, t2))

def subtract_tuples(t1: tuple[int], t2: tuple[int]) -> tuple[int]:
    """
    Subtract two n-dimensional tuples.

    ```
    t1 = (1, 2, 3)
    t2 = (0, 6, -2)
    assert subtract_tuples(t1, t2) == (1, -4, 5)
    ```
    """
    return tuple(elem1 - elem2 for elem1, elem2 in zip(t1, t2))

def multiply_tuples(t1: tuple[int], t2: tuple[int]) -> tuple[int]:
    """
    Multiply two n-dimensional tuples.

    ```
    t1 = (1, 2, 3)
    t2 = (0, 6, -2)
    assert multiply_tuples(t1, t2) == (0, 12, -6)
    ```
    """
    return tuple(elem1 * elem2 for elem1, elem2 in zip(t1, t2))

def fill_volume(pos1: tuple[int, int, int], pos2: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    """
    Given two positions in 3d space, fills all positions that exist between the two points.
    For example, given (0, 0, 0), and (0, 1, 2), the function returns
    {(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 0), (0, 1, 1), (0, 1, 2)}
    """
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    filled = set()

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                filled.add((x, y, z))
    
    return filled

def fill_area(pos1: tuple[int, int], pos2: tuple[int, int]) -> set[tuple[int, int]]:
    """
    Given two positions in 2d space, fills all positions that exist between the two points.
    For example, given (0, 0), and (2, 2), the function returns
    {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)}
    """
    x1, y1 = pos1
    x2, y2 = pos2
    filled = set()

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            filled.add((x, y))
    
    return filled

class SearchResult:
    """
    Defines a search result that contains information about the search including the path taken from start to finish, the
    distances from the start for each node, and the nodes that were visited.
    """
    def __init__(self, path: list[tuple[int, int]], dists: dict[tuple[int, int], int], visited: set[tuple[int, int]]):
        self.path = path
        self.dists = dists
        self.visited = visited
    
    def __iter__(self):
        yield self.path
        yield self.dists
        yield self.visited

def search(map: list[str], start: tuple[int, int], position_predicate: Callable[[tuple[int, int]], bool] = lambda x: x, target: tuple[int, int] = None, mode: str = "bfs") -> SearchResult:
    """
    Given a list of strings representing the rows in a map, performs a search from the start position.

    If a position predicate is not provided, the search simply search traverses the entire map (disregarding any "walls").

    If a target is not provided, the search will be exhaustive.

    If a mode is not provided, the search will default to BFS. Options for mode are "bfs" and "dfs"

    Returns:
    A set of visited positions, and the distances to each of those nodes
    """
    queue = deque([start])
    visited = set()
    dists = { start: 0 }
    curr_pos = start
    predecessors = { start: None }
    while queue:
        if mode == "bfs":
            curr_pos = queue.popleft()
        elif mode == "dfs":
            curr_pos = queue.pop()
        else:
            raise RuntimeError(f"Mode {mode} was not recognised as a valid search type.")

        visited.add(curr_pos)

        if curr_pos == target:
            path = []
            while curr_pos is not None:
                path.append(curr_pos)
                curr_pos = predecessors[curr_pos]
            
            return SearchResult(list(reversed(path)), dists, visited)

        for direction in DIRECTIONS:
            next_pos = add_tuples(curr_pos, direction)
            if next_pos not in visited and within_bounds(next_pos, map) and position_predicate(next_pos):
                queue.append(next_pos)
                dists[next_pos] = dists[curr_pos] + 1
                predecessors[next_pos] = curr_pos
        
    path = []
    while curr_pos is not None:
        path.append(curr_pos)
        curr_pos = predecessors[curr_pos]
    return SearchResult(list(reversed(path)), dists, visited)

# Simply checks if the given position falls within the bounds of the provided array
def within_bounds(pos: tuple[int, int], arr: list[str]) -> bool:
    """
    Checks if the given position falls within the bounds of the provided array.

    Returns True if the position is within the bounds, False otherwise
    """
    row, col = pos
    return row >= 0 and row < len(arr) and col >= 0 and col < len(arr[0])

def read_grid_positions(grid: list[str], chars: list[str]) -> list[set[tuple[int, int]]]:
    """
    Given a list of strings representing a grid, and a list of chars to search for, returns a
    list of positions of the given characters.

    Note: The returned list will correspond to the chars list provided

    ```
    grid = [
     [..X.],
     [XX..],
     [.S..],
    ]
    chars = ["S", "X"]

    assert read_grid_positions(grid, chars) == [{(0, 2), (1, 0), (1, 1)}, {(2, 1)}]
    ```
    """
    positions = [set() for _ in range(len(chars))]
    for row_idx, row in enumerate(grid):
        for col_idx, ch in enumerate(row):
            if ch in chars:
                positions[chars.index(ch)].add((row_idx, col_idx))
    return positions

class Notable:
    """
    Defines a "notable" element on a map. For example, given the positions of all "walls" in a map,
    you can provide the positions to this class, and define how they will be displayed when visualising
    the map.

    For example, you may wish to print your visited nodes using a different symbol, or in a different colour.
    """
    def __init__(self, positions: set[tuple[int]], symbol: str = "X", colour: str = C.RED):
        self.positions = positions
        self.symbol = symbol
        self.colour = colour

def print_map(grid: list[str], notables: list[Notable] = [], print_index: bool = True):
    """
    Print a visualisation of the provided grid. A list of notables may be passed in to display
    different elements in a different colour.

    Note: The notables passed in should contain highest -> lowest precedence, as the first match
    to a position will be printed, and the others ignored. This is only relevant if you have the same position
    in multiple sets (e.g. all_positions and visited_positions).
    """
    if print_index:
        print(''.join([str(i)[:1] for i in range(len(grid[0]))]))
    for row_idx, row in enumerate(grid):
        for col_idx, ch in enumerate(row):
            curr = (row_idx, col_idx)
            for notable in notables:
                if curr in notable.positions:
                    print(f"{notable.colour}{notable.symbol}{C.ENDC}", end="")
                    break
            else:
                print(ch, end="")
        print(f" {row_idx}" if print_index else "")
    print()

def read_as_chunks(file_name):
    """
    Given a file that contains portions/chunks separated by newlines, read the input
    into various chunks.
    """
    with open(file_name) as f:
        chunks = list(map(str.splitlines, f.read().split("\n\n")))
    return chunks
    
def read_as_lines(file_name):
    """
    Given a file that contains numerous lines of the same format, read each line into its own string in a list
    """
    with open(file_name) as f:
        lines = list(map(str.strip, f.readlines()))
    return lines

def read_as_single_line(file_name):
    """
    Given a single line file, read the single line into a string
    """
    with open(file_name) as f:
        line = f.readline()
    return line

if __name__ == "__main__":
    ###
    d(f"{C.BOLD}{C.UNDERLINE}COLOURS & STYLES:{C.ENDC}")
    d(f"{C.RED}Red{C.ENDC}", end=" ")
    d(f"{C.ORANGE}Orange{C.ENDC}", end=" ")
    d(f"{C.YELLOW}Yellow{C.ENDC}", end=" ")
    d(f"{C.GREEN}Green{C.ENDC}", end=" ")
    d(f"{C.CYAN}Cyan{C.ENDC}", end=" ")
    d(f"{C.BLUE}Blue{C.ENDC}", end=" ")
    d(f"{C.PINK}Pink{C.ENDC}", end=" ")
    d(f"{C.PURPLE}Purple{C.ENDC}", end=" ")
    d(f"{C.BOLD}Bold{C.ENDC}", end=" ")
    d(f"{C.UNDERLINE}Underline{C.ENDC}", end=" ")
    d(f"{C.ITALIC}Italic{C.ENDC}")
    d()

    ###
    d(f"{C.BOLD}{C.UNDERLINE}DIRECTIONS:{C.ENDC}")
    d(f"Up:    {dir_to_symbol[UP]} {UP} {dir_to_str[UP]}")
    d(f"Down:  {dir_to_symbol[DOWN]} {DOWN}  {dir_to_str[DOWN]}")
    d(f"Left:  {dir_to_symbol[LEFT]} {LEFT} {dir_to_str[LEFT]}")
    d(f"Right: {dir_to_symbol[RIGHT]} {RIGHT}  {dir_to_str[RIGHT]}")
    d()

    ###
    d(f"{C.BOLD}{C.UNDERLINE}TUPLE MANIPULATION:{C.ENDC}")
    magnitude = 50

    t = (1, 56, 3)
    d(f"Limiting {t=} to a magnitude of {magnitude}:                 {t} -> {limit_tuple(t, magnitude)}")

    t = (1, -56, 3)
    d(f"Limiting {t=} to a magnitude of {magnitude} (w/ abs value): {t} -> {limit_tuple(t, magnitude, use_abs_value=True)}")

    t1 = (1, 2, 3)
    t2 = (5, -6, 0)
    d(f"Adding tuples:      {t1} + {t2} = {add_tuples(t1, t2)}")
    d(f"Subtracting tuples: {t1} - {t2} = {subtract_tuples(t1, t2)}")
    d(f"Multiplying tuples: {t1} * {t2} = {multiply_tuples(t1, t2)}")

    d()

    ###
    d(f"{C.BOLD}{C.UNDERLINE}POSITION FILLING:{C.ENDC}")
    p1 = (0, 0, 0)
    p2 = (0, 1, 2)
    d(f"Volume fill: {p1}, {p2} =")
    d(f"             {sorted(fill_volume(p1, p2))}")

    p1 = (0, 0)
    p2 = (2, 2)
    d(f"Area fill:   {p1}, {p2} =")
    d(f"             {sorted(fill_area(p1, p2))}")
    d()

    ###
    d(f"{C.BOLD}{C.UNDERLINE}INPUT PARSING:{C.ENDC}")
    line = read_as_single_line("single_line_sample.txt")
    d(f"Single line: read_as_single_line(\"file.txt\") =")
    d(f"             {line}")

    lines = read_as_lines("grid_sample.txt")
    d(f"Multi-line:  read_as_lines(\"file.txt\") =")
    for line in lines:
        d(f"             {line}")
    
    chunks = read_as_chunks("chunks_sample.txt")
    d(f"Chunks:      read_as_chunks(\"file.txt\") =")
    for chunk in chunks:
        d(f"             {chunk}")

    d()

    ###
    d(f"{C.BOLD}{C.UNDERLINE}GRID PARSING:{C.ENDC}")
    grid = lines
    start, end, walls = read_grid_positions(grid, ["S", "E", "#"])
    d(f"Parse positions: start, end, walls = read_grid_positions(grid, [\"S\", \"E\", \"#\"])")
    d(f"                 {start=}, {end=}")
    d("                 walls={", end="")
    i = 0
    for idx, wall in enumerate(walls):
        if i == 8:
            i = 0
            d()
            d("                       ", end="")
        if idx == len(walls) - 1:
            d(f"{wall}", end="}")
            d()
        else:
            d(f"{wall}", end=", ")
        i += 1
    
    ###
    d(f"{C.BOLD}{C.UNDERLINE}MAP PRINTING:{C.ENDC}")
    d("print_map(grid)")
    print_map(grid)

    d("""print_map(grid, [
    Notable(positions=start, colour=C.GREEN),
    Notable(positions=end, colour=C.RED),
    Notable(positions=walls, symbol="█", colour=C.ENDC)
])""")
    print_map(grid, [
        Notable(positions=start, colour=C.GREEN),
        Notable(positions=end, colour=C.RED),
        Notable(positions=walls, symbol="█", colour=C.ENDC)
    ])

    ###
    d(f"{C.BOLD}{C.UNDERLINE}SEARCHING:{C.ENDC}")
    start = list(start)[0]
    end = list(end)[0]

    d("BFS - printing visited nodes")
    d("""res = search(grid, start, position_predicate=lambda pos: grid[pos[0]][pos[1]] != WALL, target=end, mode="bfs")
print_map(grid, [
    Notable(positions=res.visited)
])""")
    res = search(grid, start, position_predicate=lambda pos: grid[pos[0]][pos[1]] != WALL, target=end, mode="bfs")
    print_map(grid, [
        Notable(positions=res.visited)
    ])

    d("DFS - printing visited nodes")
    d("""res = search(grid, start, position_predicate=lambda pos: grid[pos[0]][pos[1]] != WALL, target=end, mode="dfs")
print_map(grid, [
    Notable(positions=res.visited)
])""")
    res = search(grid, start, position_predicate=lambda pos: grid[pos[0]][pos[1]] != WALL, target=end, mode="dfs")
    print_map(grid, [
        Notable(positions=res.visited)
    ])

    d("BFS - printing backtracked path")
    d("""res = search(grid, start, position_predicate=lambda pos: grid[pos[0]][pos[1]] != WALL, target=end, mode="bfs")
print_map(grid, [
    Notable(positions=res.path)
])""")
    res = search(grid, start, position_predicate=lambda pos: grid[pos[0]][pos[1]] != WALL, target=end, mode="bfs")
    print_map(grid, [
        Notable(positions=res.path)
    ])

    ###
    d(f"{C.BOLD}{C.UNDERLINE}GENERAL UTIL:{C.ENDC}")
    s = "This is my 1 line with -3 numbers and 3 something 44."
    nums = get_nums(s)
    d(f"{s} -> {nums}")

