# https://adventofcode.com/2015/day/5

with open("/Users/dib/dev/advent-of-code/2015/day05/input.txt") as f:
    lines = list(map(str.strip, f.readlines()))

vowels = set('aeiou')
not_good = ['ab', 'cd', 'pq', 'xy']
def solve_part_1():
    ans = 0
    for line in lines:
        # Check if we have any character combos we shouldn't
        is_no_good = False
        for no in not_good:
            if no in line:
                is_no_good = True
        if is_no_good: continue

        # Check if we have any letter twice consecutively
        letter_twice = False
        for i in range(len(line[:-1])):
            if line[i] == line[i+1]:
                letter_twice = True
                break

        # Check that we have at least
        vowel_count = 0
        enough_vowels = True
        for c in line:
            vowel_count += c in vowels
        if vowel_count < 3:
            enough_vowels = False

        ans += enough_vowels and letter_twice and not is_no_good

    return ans

def solve_part_2():
    ans = 0
    for line in lines:
        # Check if we have a character that sandwiches another
        # e.g. xyx, aba...
        has_sandwich_char = False
        for i in range(len(line[:-2])):
            if line[i] == line[i+2]:
                has_sandwich_char = True
                break
        
        # Check if a pair is contained twice - starts index 0
        found_pair = False
        for i in range(0, len(line[:-1]), 2):
            pair = line[i:i+2]
            if pair in line[i+2:]:
                found_pair = True
                break
                
        # Check if a pair is contained twice - starts index 1
        # We only check this if we haven't found one from above
        if not found_pair:
            for i in range(1, len(line[:-1]), 2):
                pair = line[i:i+2]
                if pair in line[i+2:]:
                    found_pair = True
                    break

        ans += has_sandwich_char and found_pair

    return ans

print(f'Part 1 answer: {solve_part_1()}')
print(f'Part 2 answer: {solve_part_2()}')
