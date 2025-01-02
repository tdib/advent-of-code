use std::collections::HashSet;
use std::fs::read_to_string;

fn main() {
    let input = read_to_string("../input.txt")
        .expect("Input file not found")
        .lines()
        .map(|line| line.chars().collect::<Vec<char>>())
        .collect::<Grid>();
    let map = Map::new(input);

    println!("Part 1 answer: {}", solve_part_1(&map));
    println!("Part 2 answer: {}", solve_part_2(&map));
}

type Grid = Vec<Vec<char>>;
struct Map {
    grid: Grid,
    width: usize,
    height: usize,
}
struct Offset {
    row_offset: isize,
    col_offset: isize,
}
const UP: Offset = Offset {
    row_offset: -1,
    col_offset: 0,
};
const DOWN: Offset = Offset {
    row_offset: 1,
    col_offset: 0,
};
const LEFT: Offset = Offset {
    row_offset: 0,
    col_offset: -1,
};
const RIGHT: Offset = Offset {
    row_offset: 0,
    col_offset: 1,
};
const DIRECTION_OFFSETS: [Offset; 4] = [UP, DOWN, LEFT, RIGHT];

impl Map {
    fn new(grid: Grid) -> Self {
        let height = grid.len();
        let width = grid.first().map_or(0, |row| row.len());
        Self {
            grid,
            width,
            height,
        }
    }

    fn within_bounds(&self, position: &Position) -> bool {
        position.row >= 0
            && position.row < self.height as isize
            && position.col >= 0
            && position.col < self.width as isize
    }

    fn get_char_at(&self, position: &Position) -> Option<char> {
        if self.within_bounds(position) {
            Some(self.grid[position.row as usize][position.col as usize])
        } else {
            None
        }
    }

    fn neighbours(&self, position: &Position) -> Vec<Position> {
        DIRECTION_OFFSETS
            .iter()
            .flat_map(|direction| {
                let neighbour_dir = position.offset(direction);
                if self.within_bounds(&neighbour_dir) {
                    Some(neighbour_dir)
                } else {
                    None
                }
            })
            .collect()
    }
}

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
struct Position {
    row: isize,
    col: isize,
}

impl Position {
    fn offset(&self, offset: &Offset) -> Self {
        Self {
            row: self.row + offset.row_offset,
            col: self.col + offset.col_offset,
        }
    }
}

fn flood_fill(map: &Map, from_position: &Position) -> HashSet<Position> {
    let mut visited: HashSet<Position> = HashSet::new();
    let mut stack = vec![*from_position];

    while let Some(curr_position) = stack.pop() {
        if visited.contains(&curr_position) {
            continue;
        } else {
            visited.insert(curr_position);
        }

        let neighbours = map.neighbours(&curr_position).clone();

        for neighbour in neighbours {
            if map.get_char_at(&neighbour) == map.get_char_at(from_position) {
                stack.push(neighbour);
            }
        }
    }

    visited
}

struct Region {
    positions: HashSet<Position>,
}

impl Region {
    fn get_area(&self) -> usize {
        self.positions.len()
    }

    fn get_perimeter(&self) -> usize {
        fn count_left_to_right(
            positions: &HashSet<Position>,
            min_row: isize,
            min_col: isize,
            max_row: isize,
            max_col: isize,
        ) -> usize {
            let left_start = Position {
                row: min_row,
                col: min_col,
            }
            .offset(&LEFT);

            let mut perimeter = 0;
            let mut curr_pos = left_start;

            // Scan left to right, counting boundaries on the left and right sides
            while curr_pos.row <= max_row {
                let mut prev = false;
                let mut curr;
                // Scan right until we have passed the rightmost column position
                while curr_pos.col <= max_col + 1 {
                    curr = positions.contains(&curr_pos);

                    if prev != curr {
                        perimeter += 1;
                        prev = curr;
                    }

                    curr_pos = curr_pos.offset(&RIGHT);
                }
                curr_pos = curr_pos.offset(&DOWN);
                curr_pos.col = left_start.col;
            }

            perimeter
        }

        fn count_top_to_bottom(
            positions: &HashSet<Position>,
            min_row: isize,
            min_col: isize,
            max_row: isize,
            max_col: isize,
        ) -> usize {
            let top_start = Position {
                row: min_row,
                col: min_col,
            }
            .offset(&UP);

            let mut perimeter = 0;
            let mut curr_pos = top_start;

            // Scan top to bottom, counting boundaries on the top and bottom sides
            while curr_pos.col <= max_col {
                let mut prev = false;
                let mut curr;
                // Scan right until we have passed the rightmost column position
                while curr_pos.row <= max_row + 1 {
                    curr = positions.contains(&curr_pos);

                    if prev != curr {
                        perimeter += 1;
                        prev = curr;
                    }

                    curr_pos = curr_pos.offset(&DOWN);
                }
                curr_pos = curr_pos.offset(&RIGHT);
                curr_pos.row = top_start.row;
            }

            perimeter
        }
        let min_row = self.positions.iter().min_by_key(|pos| pos.row).unwrap().row;
        let max_row = self.positions.iter().max_by_key(|pos| pos.row).unwrap().row;
        let min_col = self.positions.iter().min_by_key(|pos| pos.col).unwrap().col;
        let max_col = self.positions.iter().max_by_key(|pos| pos.col).unwrap().col;

        count_left_to_right(&self.positions, min_row, min_col, max_row, max_col)
            + count_top_to_bottom(&self.positions, min_row, min_col, max_row, max_col)
    }

    fn get_perimeter2(&self) -> usize {
        fn count_left_to_right(
            positions: &HashSet<Position>,
            min_row: isize,
            min_col: isize,
            max_row: isize,
            max_col: isize,
        ) -> usize {
            let left_start = Position {
                row: min_row,
                col: min_col,
            }
            .offset(&LEFT);

            let mut perimeter = 0;
            let mut perimeter_locs: HashSet<(Position, bool)> = HashSet::new();
            let mut curr_pos = left_start;

            // Scan left to right, counting boundaries on the left and right sides
            while curr_pos.row <= max_row {
                let mut prev = false;
                let mut curr;
                // Scan right until we have passed the rightmost column position
                while curr_pos.col <= max_col + 1 {
                    curr = positions.contains(&curr_pos);

                    if prev != curr {
                        if !perimeter_locs.contains(&(curr_pos.offset(&UP), curr)) {
                            perimeter += 1;
                        }
                        perimeter_locs.insert((curr_pos, curr));
                        prev = curr;
                    }

                    curr_pos = curr_pos.offset(&RIGHT);
                }
                curr_pos = curr_pos.offset(&DOWN);
                curr_pos.col = left_start.col;
            }

            perimeter
        }

        fn count_top_to_bottom(
            positions: &HashSet<Position>,
            min_row: isize,
            min_col: isize,
            max_row: isize,
            max_col: isize,
        ) -> usize {
            let top_start = Position {
                row: min_row,
                col: min_col,
            }
            .offset(&UP);

            let mut perimeter = 0;
            let mut curr_pos = top_start;
            let mut perimeter_locs: HashSet<(Position, bool)> = HashSet::new();

            // Scan top to bottom, counting boundaries on the top and bottom sides
            while curr_pos.col <= max_col {
                let mut prev = false;
                let mut curr;
                // Scan right until we have passed the rightmost column position
                while curr_pos.row <= max_row + 1 {
                    curr = positions.contains(&curr_pos);

                    if prev != curr {
                        if !perimeter_locs.contains(&(curr_pos.offset(&LEFT), curr)) {
                            perimeter += 1;
                        }
                        perimeter_locs.insert((curr_pos, curr));
                        prev = curr;
                    }

                    curr_pos = curr_pos.offset(&DOWN);
                }
                curr_pos = curr_pos.offset(&RIGHT);
                curr_pos.row = top_start.row;
            }

            perimeter
        }
        let min_row = self.positions.iter().min_by_key(|pos| pos.row).unwrap().row;
        let max_row = self.positions.iter().max_by_key(|pos| pos.row).unwrap().row;
        let min_col = self.positions.iter().min_by_key(|pos| pos.col).unwrap().col;
        let max_col = self.positions.iter().max_by_key(|pos| pos.col).unwrap().col;

        count_left_to_right(&self.positions, min_row, min_col, max_row, max_col)
            + count_top_to_bottom(&self.positions, min_row, min_col, max_row, max_col)
    }
}

fn solve_part_1(map: &Map) -> usize {
    let mut visited_all: HashSet<Position> = HashSet::new();
    let mut regions: Vec<Region> = Vec::new();

    for (ri, row) in map.grid.iter().enumerate() {
        for ci in 0..row.len() {
            let curr_position = Position {
                row: ri as isize,
                col: ci as isize,
            };
            if visited_all.contains(&curr_position) {
                continue;
            } else {
                let region_positions = flood_fill(map, &curr_position);
                visited_all.extend(&region_positions);
                regions.push(Region {
                    positions: region_positions,
                });
            }
        }
    }

    regions
        .iter()
        .map(|region| region.get_area() * region.get_perimeter())
        .sum()
}

fn solve_part_2(map: &Map) -> usize {
    let mut visited_all: HashSet<Position> = HashSet::new();
    let mut regions: Vec<Region> = Vec::new();

    for (ri, row) in map.grid.iter().enumerate() {
        for ci in 0..row.len() {
            let curr_position = Position {
                row: ri as isize,
                col: ci as isize,
            };
            if visited_all.contains(&curr_position) {
                continue;
            } else {
                let region_positions = flood_fill(map, &curr_position);
                visited_all.extend(&region_positions);
                regions.push(Region {
                    positions: region_positions,
                });
            }
        }
    }

    regions
        .iter()
        .map(|region| region.get_area() * region.get_perimeter2())
        .sum()
}
