# https://adventofcode.com/2023/day/7
from collections import Counter

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def custom_sort_key(item, l):
    return (-item[0], [l.index(c) for c in item[1]])


def sort_tuples(t, l):
    return sorted(t, key=lambda x: custom_sort_key(x, l))


def classify_hand(hand, is_part_2):
    counts = Counter(hand)
    vals = counts.values()
    j_count = counts.get("J", 0)
    if is_part_2:
        del counts["J"]
    else:
        j_count = 0
    
    if 5 - j_count in vals or j_count >= 4:
        return 7
    elif 4 - j_count in vals:
        return 6
    elif (len(list(filter(lambda x: x == 2, vals))) == 2 and j_count == 1) or (3 in vals and 2 in vals):
        return 5
    elif 3 - j_count in vals:
        return 4
    elif len(list(filter(lambda x: x == 2, vals))) == 2:
        return 3
    elif 2 - j_count in vals:
        return 2
    else:
        return 1


def solve(labels, is_part_2):
    hand_rankings = []
    for line in lines:
        hand, winnings = line.split()
        hand_rankings.append((classify_hand(hand, is_part_2), hand, int(winnings)))
    # Sort them firstly according to their hand strength, and then by cards
    hand_rankings = sort_tuples(hand_rankings, labels)

    ans = 0
    for i, (_, _, score) in enumerate(reversed(hand_rankings)):
        ans += score * (i+1)

    return ans


def solve_part_1():
    labels = "A K Q J T 9 8 7 6 5 4 3 2".split()
    return solve(labels, is_part_2=False)


def solve_part_2():
    labels = "A K Q T 9 8 7 6 5 4 3 2 J".split()
    return solve(labels, is_part_2=True)


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")


