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
    let map = Map::new(input);

    println!("Part 1 answer: {}", solve_part_1(&map));
    println!("Part 2 answer: {}", solve_part_2(&map));
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
