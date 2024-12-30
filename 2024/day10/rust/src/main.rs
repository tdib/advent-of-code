mod coordinate;
mod parseable;
mod topographic_map;

use crate::topographic_map::TopographicMapExtensions;
use parseable::Parseable;

use std::collections::HashSet;
use std::fs::read_to_string;

fn main() {
    let map = read_to_string("../input.txt")
        .expect("Input file not found")
        .parse();

    let mut total_1 = 0;
    let mut total_2 = 0;
    let trailheads = map.find_trailheads();
    for trailhead in trailheads {
        let result = map.find_paths(trailhead.clone(), HashSet::new(), &mut HashSet::new());
        total_1 += result.unique_endpoints.len();
        total_2 += result.distinct_paths;
    }
    println!("Part 1 answer: {total_1}");
    println!("Part 2 answer: {total_2}");
}
