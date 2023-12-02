# https://adventofcode.com/2023/day/2

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

RED = "red"
GREEN = "green"
BLUE = "blue"

# Get the max count of each cube colour across all sets in a game
# e.g. Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# turns into {"red": 4, "green": 2, "blue": 6}, where there are
# at most 4 reds, 2 greens, or 6 blues in this game
def get_max_colour_counts(line):
    colours = {
        RED: 0,
        GREEN: 0,
        BLUE: 0,
    }
    # ["Game 1", "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"]
    split = line.split(": ")

    # "Game 1" -> 1
    game_id = int(split[0].split()[-1])

    # ["3 blue, 4 red", "1 red, 2 green", "6 blue, 2 green"]
    game_sets = split[1].split(";")

    for game_set in game_sets:
        # ["3 blue", "4 red"]
        for cube in game_set.split(","):
            # "3", "blue"
            num, colour = cube.split()
            # Check for a higher number of cubes with this colour
            colours[colour] = max(colours[colour], int(num))
    
    return (game_id, colours)

def solve_part_1():
    possibles = []
    # Define the limits of each colour
    maxes = {
        RED: 12,
        GREEN: 13,
        BLUE: 14
    }
    for line in lines:
        game_id, colours = get_max_colour_counts(line)

        # If all max set colours in this game are within the bounds
        if all(colours[c] <= maxes[c] for c in colours):
            # This is a valid/possible game so keep track of the id
            possibles.append(game_id)

    return sum(possibles)


def solve_part_2():
    ans = 0
    for line in lines:
        _, colours = get_max_colour_counts(line)
        
        # Add the product of each colour to the total sum
        ans += colours[RED] * colours[GREEN] * colours[BLUE]

    return ans

print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")

