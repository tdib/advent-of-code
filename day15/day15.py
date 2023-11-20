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

def get_scanned_row_positions(start_pos, distance, y):
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

def solve_part_1():
  ROW_TO_SCAN = 2000000
  scanned_area = set()
  for sensor in sensors:
    scanned_row_positions = get_scanned_row_positions(sensor, distances[sensor], ROW_TO_SCAN)
    scanned_area = scanned_area.union(scanned_row_positions)
  return count_row(ROW_TO_SCAN, scanned_area)


def solve_part_2():
  MAX_ROW = 4000000
  # For every row, we evaluate the scanned range for each sensor.
  # We are essentially checking which cells are scanned row by row,
  # rather than sensor by sensor
  for row in range(MAX_ROW+1):
    x_ranges = []
    for sensor in sensors:
      distance_to_beacon = distances[sensor]
      x_distance_to_beacon = distance_to_beacon - abs(row - sensor[1])
      if x_distance_to_beacon >= 0:
        x_range = (sensor[0]-x_distance_to_beacon, sensor[0]+x_distance_to_beacon)
        x_ranges.append(x_range)

    # Sort the ranges - by default will use the first element of the tuple
    x_ranges.sort()

    coverage = x_ranges[0]
    for x_range in x_ranges[1:]:
      # If the current x range lower bound is less than our current upper bound,
      # readjust the upper bound to the max of the two.
      # Note that we already know we have the lower bound so we don't need to worry about that
      if x_range[0] <= coverage[1]:
        coverage = (coverage[0], max(coverage[1], x_range[1]))
        continue
      # If this x range is not within our current coverage, we have a gap, and have found the answer
      else:
        return 4000000 * (coverage[1]+1) + row

print(f'Part 1 answer: {solve_part_1()}')
print(f'Part 2 answer: {solve_part_2()}')
