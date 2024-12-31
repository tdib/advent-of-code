use crate::coordinate::Coordinate;

use std::collections::HashSet;

const START_VAL: usize = 0;
const END_VAL: usize = 9;

pub type TopographicMap = Vec<Vec<usize>>;

pub struct PathResult {
    pub distinct_paths: usize,
    pub unique_endpoints: HashSet<Coordinate>,
}

pub trait TopographicMapExtensions {
    fn get_map_char(&self, coordinate: &Coordinate) -> usize;
    fn find_trailheads(&self) -> Vec<Coordinate>;
    fn find_paths(
        &self,
        curr_loc: Coordinate,
        visited: HashSet<Coordinate>,
        visited_endpoints: &mut HashSet<Coordinate>,
    ) -> PathResult;
}

impl TopographicMapExtensions for TopographicMap {
    fn get_map_char(&self, coordinate: &Coordinate) -> usize {
        *self
            .get(coordinate.row)
            .expect("Row coordinate out of bounds")
            .get(coordinate.col)
            .expect("Col coordinate out of bounds")
    }

    fn find_trailheads(&self) -> Vec<Coordinate> {
        self.iter()
            .enumerate()
            .flat_map(|(ri, row)| {
                row.iter().enumerate().filter_map(move |(ci, ch)| {
                    if *ch == START_VAL {
                        Some(Coordinate { row: ri, col: ci })
                    } else {
                        None
                    }
                })
            })
            .collect()
    }

    fn find_paths(
        &self,
        curr_loc: Coordinate,
        mut visited: HashSet<Coordinate>,
        visited_endpoints: &mut HashSet<Coordinate>,
    ) -> PathResult {
        let curr_map_char = self.get_map_char(&curr_loc);
        if curr_map_char == END_VAL {
            visited_endpoints.insert(curr_loc);
            return PathResult {
                distinct_paths: 1,
                unique_endpoints: visited_endpoints.clone(),
            };
        }

        visited.insert(curr_loc.clone());
        let mut total = 0;
        let neighbours = curr_loc.neighbours(self.len(), self.get(0).unwrap().len());
        for neighbour in neighbours {
            if visited.contains(&neighbour) {
                continue;
            }
            let neighbour_map_char = self.get_map_char(&neighbour);
            if neighbour_map_char == curr_map_char + 1 {
                let sub_results = self.find_paths(neighbour, visited.clone(), visited_endpoints);
                total += sub_results.distinct_paths;
                visited_endpoints.extend(sub_results.unique_endpoints);
            }
        }
        PathResult {
            distinct_paths: total,
            unique_endpoints: visited_endpoints.clone(),
        }
    }
}
