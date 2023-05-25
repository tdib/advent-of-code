use std::cmp::Ordering;
use std::{fs::read_to_string, ops::RangeInclusive};

#[derive(Debug)]
struct ElfPair {
    first: RangeInclusive<usize>,
    second: RangeInclusive<usize>,
}

impl ElfPair {
    // Creates a new ElfPair, where the first range is always the larger of the two
    fn new(first: RangeInclusive<usize>, second: RangeInclusive<usize>) -> Self {
        let (first, second) = match first.start().cmp(second.start()) {
            Ordering::Less => (first, second),
            Ordering::Equal => {
                if first.end() > second.end() {
                    (first, second)
                } else {
                    (second, first)
                }
            }
            Ordering::Greater => (second, first),
        };
        ElfPair { first, second }
    }

    fn contains_full_overlap(&self) -> bool {
        self.first.contains(self.second.start()) && self.first.contains(self.second.end())
    }

    fn contains_partial_overlap(&self) -> bool {
        todo!()
    }
}

trait RangeInclusiveExt {
    fn from_str(range_str: &str) -> RangeInclusive<usize>;
}

impl RangeInclusiveExt for RangeInclusive<usize> {
    fn from_str(range_str: &str) -> RangeInclusive<usize> {
        let (lower_bound, upper_bound) = range_str.split_once('-').unwrap();
        lower_bound.parse().unwrap()..=upper_bound.parse().unwrap()
    }
}

fn main() {
    let input = read_to_string("../input.txt").unwrap();

    let part_1_sum = input
        .lines()
        .map(|line| {
            let (first_range, second_range) = line.split_once(',').unwrap();
            let pair: ElfPair = ElfPair::new(
                RangeInclusive::from_str(first_range),
                RangeInclusive::from_str(second_range),
            );
            pair.contains_full_overlap()
        })
        .filter(|&has_overlap| has_overlap)
        .count();

    println!("The answer for part 1 is {}", part_1_sum);
}
