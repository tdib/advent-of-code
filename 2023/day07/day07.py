# https://adventofcode.com/2023/day/7
from collections import Counter

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))


def custom_sort_key(item, l):
    return (-item[0], [l.index(c) for c in item[1]])


def sort_tuples(t, l):
    return sorted(t, key=lambda x: custom_sort_key(x, l))


def solve_part_1():
    labels = "A K Q J T 9 8 7 6 5 4 3 2".split()
    ans = 0
    hand_rankings = []
    for line in lines:
        hand, winnings = line.split()
        winnings = int(winnings)

        c = Counter(hand)
        vals = c.values()

        # Five of a kind
        if 5 in vals:
            hand_rankings.append((7, hand, winnings))
        # Four of a kind
        elif 4 in vals:
            hand_rankings.append((6, hand, winnings))
        # Full house
        elif len(vals) == 2 and 2 in vals and 3 in vals:
            hand_rankings.append((5, hand, winnings))
        # Three of a kind
        elif 3 in vals:
            hand_rankings.append((4, hand, winnings))
        # Two pair
        elif len(vals) == 3 and len(list(filter(lambda x: x == 2, vals))) == 2:
            hand_rankings.append((3, hand, winnings))
        # One pair
        elif len(vals) == 4 and 2 in vals:
            hand_rankings.append((2, hand, winnings))
        # High card
        elif len(vals) == 5:
            hand_rankings.append((1, hand, winnings))

    # Sort them firstly according to their hand strength, and then by cards
    hand_rankings = sort_tuples(hand_rankings, labels)
    for i, (_, _, score) in enumerate(reversed(hand_rankings)):
        ans += score * (i+1)

    return ans


def solve_part_2():
    labels = "A K Q T 9 8 7 6 5 4 3 2 J".split()
    ans = 0
    hand_rankings = []
    for line in lines:
        hand, winnings = line.split()
        winnings = int(winnings)

        c = Counter(hand)
        vals = c.values()

        j_count = 0
        if "J" in c:
            j_count = c["J"]
            del c["J"]

        # No J's - regular logic applies
        if j_count == 0:
            # Five of a kind
            if 5 in vals:
                hand_rankings.append((7, hand, winnings))
            # Four of a kind
            elif 4 in vals:
                hand_rankings.append((6, hand, winnings))
            # Full house
            elif len(vals) == 2 and 2 in vals and 3 in vals:
                hand_rankings.append((5, hand, winnings))
            # Three of a kind
            elif 3 in vals:
                hand_rankings.append((4, hand, winnings))
            # Two pair
            elif len(vals) == 3 and len(list(filter(lambda x: x == 2, vals))) == 2:
                hand_rankings.append((3, hand, winnings))
            # One pair
            elif len(vals) == 4 and 2 in vals:
                hand_rankings.append((2, hand, winnings))
            # High card
            elif len(vals) == 5:
                hand_rankings.append((1, hand, winnings))
        # At least one J - updated logic applies
        else:
            # Five of a kind
            if any(x + j_count == 5 for x in vals) or j_count in [4, 5]:
                hand_rankings.append((7, hand, winnings))
            # Four of a kind
            elif any(x + j_count == 4 for x in vals):
                hand_rankings.append((6, hand, winnings))
            # Full house
            elif len(vals) == 2 and j_count == 1:
                hand_rankings.append((5, hand, winnings))
            # Three of a kind
            elif any(x + j_count == 3 for x in vals):
                hand_rankings.append((4, hand, winnings))
            # Two pair
            elif len(vals) == 3 and len(list(filter(lambda x: x == 2, c.values()))) == 2:
                hand_rankings.append((3, hand, winnings))
            # One pair
            elif len(vals) == 4 and (any(x == 2 for x in c.values()) or j_count == 1):
                hand_rankings.append((2, hand, winnings))
            # High card
            elif all([x == 1 for x in vals]):
                hand_rankings.append((1, hand, winnings))

    hand_rankings = sort_tuples(hand_rankings, labels)
    for i, (_, _, score) in enumerate(reversed(hand_rankings)):
        ans += score * (i+1)
    return ans


print(f"Part 1 answer: {solve_part_1()}")
print(f"Part 2 answer: {solve_part_2()}")


