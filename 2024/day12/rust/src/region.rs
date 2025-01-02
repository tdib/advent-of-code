use crate::offset::*;
use crate::Position;

use std::collections::HashSet;

pub struct Region {
    pub positions: HashSet<Position>,
}

impl Region {
    pub fn get_area(&self) -> usize {
        self.positions.len()
    }

    pub fn get_perimeter(&self, part: usize) -> usize {
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
