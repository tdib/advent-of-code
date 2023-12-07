# https://adventofcode.com/2023/day/7
from collections import deque, defaultdict, Counter
import re

with open("input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

def is5(hand):
    return all([x == hand[0] for x in hand])

def blah(s, n):
    return re.search(f"(.)\1{n}", s) is not None

# labels = list(reversed("A K Q J T 9 8 7 6 5 4 3 2".split()))
def custom_sort_key(item, l):
    return (item[0], [l.index(c) for c in item[1]])

def sort_tuples(t, l):
    return sorted(t, key=lambda x: custom_sort_key(x, l))

def solve_part_1():
    labels = "A K Q J T 9 8 7 6 5 4 3 2".split()
    ans = 0
    hand_rankings = []
    for line in lines:
        hand, winnings = line.split()
        # hand = ''.join(sorted(hand))
        winnings = int(winnings)
        # print(hand, winnings)

        c = Counter(hand)

        # QQQJA
        # T55J5
        # KK677
        # KTJJT
        # 32T3K

        # Five of a kind
        if any(x == 5 for x in c.values()):
            hand_rankings.append((1, hand, winnings))
            # print("five of a kind")
        # Four of a kind
        elif any(x == 4 for x in c.values()):
            hand_rankings.append((2, hand, winnings))
            # print("four of a kind")
        # Full house
        elif len(c.values()) == 2:
            if any(x ==2 for x in c.values()) and any(x ==3 for x in c.values()):
                hand_rankings.append((3, hand, winnings))
                # print("full house")
        # Three of a kind
        elif any(x == 3 for x in c.values()):
            hand_rankings.append((4, hand, winnings))
            # print("three of a kind")
        # Two pair
        elif len(c.values()) == 3:
            if len(list(filter(lambda x: x == 2, c.values()))) == 2:
                hand_rankings.append((5, hand, winnings))
                # print("two pair")
        # One pair
        elif len(c.values()) == 4:
            if any(x == 2 for x in c.values()):
                hand_rankings.append((6, hand, winnings))
        # High card
        elif all([x == 1 for x in c.values()]):
            hand_rankings.append((7, hand, winnings))
            # print("high card")
        # print()

        # pass
    # print(sorted(hand_rankings))
    hand_rankings = sort_tuples(hand_rankings, labels)
    for i, (a, b, score) in enumerate(reversed(hand_rankings)):
        # print(f"{ans} += {score=} * ({i+1})")
        ans += (score * (i+1))
        # print(i, b, c)
    return ans


def solve_part_2():
    labels = "A K Q T 9 8 7 6 5 4 3 2 J".split()
    ans = 0
    hand_rankings = []
    for line in lines:
        hand, winnings = line.split()
        # hand = ''.join(sorted(hand))
        winnings = int(winnings)

        c = Counter(hand)

        j_count = 0
        if "J" in c:
            j_count = c["J"]
            del c["J"]
            # print(f"HAS {j_count} Js")
        
        if j_count == 0:
            # Five of a kind
            print(hand, winnings)
            print("NO J")
            if any(x == 5 for x in c.values()):
                hand_rankings.append((1, hand, winnings))
                print("five of a kind")
            # Four of a kind
            elif any(x == 4 for x in c.values()):
                hand_rankings.append((2, hand, winnings))
                print("four of a kind")
            # Full house
            elif len(c.values()) == 2:
                if any(x ==2 for x in c.values()) and any(x ==3 for x in c.values()):
                    hand_rankings.append((3, hand, winnings))
                    print("full house")
            # Three of a kind
            elif any(x == 3 for x in c.values()):
                hand_rankings.append((4, hand, winnings))
                print("three of a kind")
            # Two pair
            elif len(c.values()) == 3:
                if len(list(filter(lambda x: x == 2, c.values()))) == 2:
                    hand_rankings.append((5, hand, winnings))
                    print("two pair")
            # One pair
            elif len(c.values()) == 4:
                if any(x == 2 for x in c.values()):
                    hand_rankings.append((6, hand, winnings))
                    print("one pair")
            # High card
            elif all([x == 1 for x in c.values()]):
                hand_rankings.append((7, hand, winnings))
                print("high card")
            print()
        else:
            print(hand, winnings)
            # JJ8JJ 91
            # AA3J5 31

            # Five of a kind
            if j_count in [5, 4] or any(x + j_count == 5 for x in c.values()):
                hand_rankings.append((1, hand, winnings))
                print("five of a kind")
            # Four of a kind
            elif any(x + j_count == 4 for x in c.values()):
                hand_rankings.append((2, hand, winnings))
                print("four of a kind")
            # Full house
            elif len(c.values()) == 2:
                if j_count == 1:
                    hand_rankings.append((3, hand, winnings))
                    print("full house")
                elif j_count == 2 or j_count == 3:
                    print("???????????? we should have 4 of a kind")
                    return 999999
                # if any(x == 2 for x in c.values()) and any(x == 3 for x in c.values()):
                #     hand_rankings.append((3, hand, winnings))
                #     print("full house")
            
            # elif len(c.values()) == 2:
                # for i in range(1, j_count+1):
                #     if any(x == 2 - i for x in c.values()) and any(x == 3 for x in c.values()):
                #         hand_rankings.append((3, hand, winnings))
                #         break
                #         print("full house")
            # Three of a kind
            elif any(x + j_count == 3 for x in c.values()):
                hand_rankings.append((4, hand, winnings))
                print("three of a kind")
            # Two pair
            elif len(c.values()) == 3 and len(list(filter(lambda x: x == 2, c.values()))) == 2:
                hand_rankings.append((5, hand, winnings))
                print("two pair")
            # One pair
            elif len(c.values()) == 4 and any(x == 2 for x in c.values()) or j_count == 1:
                hand_rankings.append((6, hand, winnings))
                print("one pair")
            # High card
            elif all([x == 1 for x in c.values()]):
                if j_count == 1:
                    return 999973248
                hand_rankings.append((7, hand, winnings))
                print("high card")
            else:
                return 99999
            print()

    # print(sorted(hand_rankings))
    hand_rankings = sort_tuples(hand_rankings, labels)
    print(hand_rankings)
    for i, (a, b, score) in enumerate(reversed(hand_rankings)):
        ans += score * (i+1)
        # print(i, b, c)
    return ans



print(f"Part 1 answer: {solve_part_1()}")
# > 196287077
# < 251041900
print(f"Part 2 answer: {solve_part_2()}")


