# https://adventofcode.com/2023/day/1
import re

print(f"Part 1 answer: {sum([int(f"{re.findall(r"\d", line)[0]}{re.findall(r"\d", line)[-1]}") for line in open("input.txt").readlines()])}")
print(f"Part 2 answer: {sum([int(f"{re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)[0] if re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)[0].isdigit() else ['one','two','three','four','five','six','seven','eight','nine'].index(re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)[0]) + 1}{re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)[-1] if re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)[-1].isdigit() else ['one','two','three','four','five','six','seven','eight','nine'].index(re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)[-1]) + 1}") for line in open("input.txt").readlines()])}")
