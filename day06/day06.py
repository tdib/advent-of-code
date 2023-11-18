with open('input.txt', 'r') as f:
  packet = f.readline()

def answer(n):
  for i in range(len(packet)):
    chars = packet[i:i+n]
    if len(set(chars)) == n:
      return i+n

print('Part 1 answer:', answer(4))
print('Part 2 answer:', answer(14))
