import re

with open('input.txt', 'r') as f:
  lines = list(map(str.strip, f.readlines()))

def add_tuples(a, b):
  return (a[0]+b[0], a[1]+b[1])

def get_distance(a, b):
  return abs(a[0]-b[0]) + abs(a[1]-b[1])

def print_map(sensors, beacons, visited):
  locations = sensors.union(beacons)
  min_width = min(locations, key=lambda location: location[0])[0]
  max_width = max(locations, key=lambda location: location[0])[0]
  min_height = min(locations, key=lambda location: location[1])[1]
  max_height = max(locations, key=lambda location: location[1])[1]
  PADDING = 3

  for y in range(min_height-PADDING, max_height+PADDING+1):
    for x in range(min_width-PADDING, max_width+PADDING+1):
      if (x, y) in sensors:
        print('S', end='')
      elif (x, y) in beacons:
        print('B', end='')
      elif (x, y) in visited:
        print('#', end='')
      else:
        print('.', end='')
    print()

def get_diamond_positions(start_pos, distance, y):
  col, _ = start_pos
  positions = set()
  for horizontal in range(col-distance, col+distance+1):
    if get_distance(start_pos, (horizontal, y)) <= distance:
      positions.add((horizontal, y))
  return positions

def count_row(y, scanned_area):
  scanned_area_filtered = set(filter(lambda s: s[1] == y, scanned_area))
  scanned_area_filtered.difference_update(beacons)
  scanned_area_filtered.difference_update(sensors)

  return len(scanned_area_filtered)

m = {}
sensors = set()
beacons = set()
distances = {}
for line in lines:
  r = r'x=(-?\d+), y=(-?\d+)'
  sensor_pos, beacon_pos = [(int(a), int(b)) for a, b in re.findall(r, line)]
  sensors.add(sensor_pos)
  beacons.add(beacon_pos)
  distances[sensor_pos] = get_distance(sensor_pos, beacon_pos)

ROW_TO_SCAN = 2000000
scanned_area = set()
for sensor in sensors:
  print(sensor)
  scanned_area = scanned_area.union(get_diamond_positions(sensor, distances[sensor], ROW_TO_SCAN))


print(f'Part 1 answer: {count_row(ROW_TO_SCAN, scanned_area)}')

# print('about to print map')
# print_map(sensors, beacons, scanned_area)