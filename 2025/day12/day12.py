# https://adventofcode.com/2025/day/12
from dataclasses import dataclass

from util.util import read_as_chunks


@dataclass
class Region:
    width: int
    height: int
    quantities: list[int]

    def area(self):
        return self.width * self.height

    def area_required(self, shapes):
        required = 0
        for idx, quantity in enumerate(self.quantities):
            required += get_shape_size(shapes[idx]) * quantity
        return required


*shapes, regions_raw = read_as_chunks("input.txt")
shapes = [line[1:] for line in shapes]

regions = []
for region in regions_raw:
    size, quantities = region.split(": ")
    quantities = list(map(int, quantities.split()))
    width, height = map(int, size.split("x"))
    regions.append(Region(width, height, quantities))


def get_shape_size(shape):
    count = 0
    for row in shape:
        count += row.count("#")

    return count


# Size of a shape assuming there is no empty space (3x3)
SHAPE_BLOCK_AREA = 9


def solve_part_1():
    ans = 0

    for region in regions:
        # Region is too small for the shapes it needs to pack
        if region.area_required(shapes) > region.area():
            continue

        # If you were to assume each shape is a full 3x3, could we still fit it?
        # Effectively slice off any "unusable" parts of the area, e.g. if it was 4 wide,
        # we could only fit one block of 3 across
        placeable_naive_blocks = (region.width // 3) * (region.height // 3)
        naive_area_required = placeable_naive_blocks * SHAPE_BLOCK_AREA
        if naive_area_required > region.area():
            continue

        # This also seems to work for the input but I think it's technically less correct?
        # num_shapes_to_fit = sum(region.quantities)
        # naive_area_required = num_shapes_to_fit * SHAPE_BLOCK_AREA
        # if naive_area_required > region.area():
        #     continue

        ans += 1

    return ans


print(f"Part 1 answer: {solve_part_1()}")
