use crate::Position;
use crate::Region;
use std::collections::HashSet;

pub type Grid = Vec<Vec<char>>;

pub struct Map {
    pub grid: Grid,
    width: usize,
    height: usize,
}

impl Map {
    pub fn new(grid: Grid) -> Self {
        let height = grid.len();
        let width = grid.first().map_or(0, |row| row.len());
        Self {
            grid,
            width,
            height,
        }
    }

    pub fn within_bounds(&self, position: &Position) -> bool {
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

    fn flood_fill(&self, from_position: &Position) -> HashSet<Position> {
        let mut visited: HashSet<Position> = HashSet::new();
        let mut stack = vec![*from_position];

        while let Some(curr_position) = stack.pop() {
            if visited.contains(&curr_position) {
                continue;
            } else {
                visited.insert(curr_position);
            }

            let neighbours = curr_position.neighbours(self).clone();

            for neighbour in neighbours {
                if self.get_char_at(&neighbour) == self.get_char_at(from_position) {
                    stack.push(neighbour);
                }
            }
        }

        visited
    }

    pub fn compute_regions(&self) -> Vec<Region> {
        let mut visited_all: HashSet<Position> = HashSet::new();
        let mut regions: Vec<Region> = Vec::new();

        for (ri, row) in self.grid.iter().enumerate() {
            for ci in 0..row.len() {
                let curr_position = Position {
                    row: ri as isize,
                    col: ci as isize,
                };
                if visited_all.contains(&curr_position) {
                    continue;
                } else {
                    let region_positions = self.flood_fill(&curr_position);
                    visited_all.extend(&region_positions);
                    regions.push(Region {
                        positions: region_positions,
                    });
                }
            }
        }

        regions
    }
}
