mod map;
mod offset;

use map::*;
use offset::*;

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

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
pub struct Position {
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

    fn neighbours(&self, map: &Map) -> Vec<Position> {
        DIRECTION_OFFSETS
            .iter()
            .flat_map(|direction| {
                let neighbour_dir = self.offset(direction);
                if map.within_bounds(&neighbour_dir) {
                    Some(neighbour_dir)
                } else {
                    None
                }
            })
            .collect()
    }
}

pub struct Region {
    positions: HashSet<Position>,
}

impl Region {
    fn get_area(&self) -> usize {
        self.positions.len()
    }

    fn get_perimeter(&self, part: usize) -> usize {
        let mut perimeter = 0;
        let mut curr_pos;
        let mut perimeter_locs;

        let min_row = self.positions.iter().min_by_key(|pos| pos.row).unwrap().row;
        let max_row = self.positions.iter().max_by_key(|pos| pos.row).unwrap().row;
        let min_col = self.positions.iter().min_by_key(|pos| pos.col).unwrap().col;
        let max_col = self.positions.iter().max_by_key(|pos| pos.col).unwrap().col;

        // Raster scan (left -> right for each row), counting all boundaries on left and right sides
        let left_start = Position {
            row: min_row,
            col: min_col,
        }
        .offset(&LEFT);
        curr_pos = left_start;
        perimeter_locs = HashSet::new();
        while curr_pos.row <= max_row {
            let mut prev = false;
            // let mut curr;
            // Scan right until we have passed the rightmost column position
            while curr_pos.col <= max_col + 1 {
                let curr = self.positions.contains(&curr_pos);

                if prev != curr {
                    match part {
                        1 => perimeter += 1,
                        2 => {
                            if !perimeter_locs.contains(&(curr_pos.offset(&UP), curr)) {
                                perimeter += 1;
                            }
                            perimeter_locs.insert((curr_pos, curr));
                        }
                        _ => unreachable!(),
                    }
                    prev = curr;
                }

                curr_pos = curr_pos.offset(&RIGHT);
            }
            curr_pos = curr_pos.offset(&DOWN);
            curr_pos.col = left_start.col;
        }

        // Vertical raster scan (top -> bottom for each col), counting all boundaries on top and bottom sides
        let top_start = Position {
            row: min_row,
            col: min_col,
        }
        .offset(&UP);

        curr_pos = top_start;
        perimeter_locs = HashSet::new();
        while curr_pos.col <= max_col {
            let mut prev = false;
            // Scan right until we have passed the rightmost column position
            while curr_pos.row <= max_row + 1 {
                let curr = self.positions.contains(&curr_pos);

                if prev != curr {
                    match part {
                        1 => perimeter += 1,
                        2 => {
                            if !perimeter_locs.contains(&(curr_pos.offset(&LEFT), curr)) {
                                perimeter += 1;
                            }
                            perimeter_locs.insert((curr_pos, curr));
                        }
                        _ => unreachable!(),
                    }
                    prev = curr;
                }

                curr_pos = curr_pos.offset(&DOWN);
            }
            curr_pos = curr_pos.offset(&RIGHT);
            curr_pos.row = top_start.row;
        }

        perimeter
    }
}

fn solve_part_1(map: &Map) -> usize {
    map.compute_regions()
        .iter()
        .map(|region| region.get_area() * region.get_perimeter(1))
        .sum()
}

fn solve_part_2(map: &Map) -> usize {
    map.compute_regions()
        .iter()
        .map(|region| region.get_area() * region.get_perimeter(2))
        .sum()
}