mod map;
mod offset;
mod position;
mod region;

use map::*;
use offset::*;
use position::*;
use region::*;

use std::fs::read_to_string;

fn main() {
    let input = read_to_string("../input.txt")
        .expect("Input file not found")
        .lines()
        .map(|line| line.chars().collect::<Vec<char>>())
        .collect::<Grid>();
    let regions = Map::new(input).compute_regions();

    println!("Part 1 answer: {}", solve_part(1, &regions));
    println!("Part 2 answer: {}", solve_part(2, &regions));
}

fn solve_part(part: usize, regions: &[Region]) -> usize {
    regions
        .iter()
        .map(|region| region.get_area() * region.get_perimeter(part))
        .sum()
}
