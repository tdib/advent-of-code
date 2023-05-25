use std::fs::read_to_string;

#[derive(Debug)]
struct ElfPair {
    first: CustomRange,
    second: CustomRange,
}

impl ElfPair {
    fn contains_full_overlap(&self) -> bool {
        // First completely contains second
        (self.first.start <= self.second.start && self.first.end >= self.second.end)
        // Second completely contains first
        || (self.second.start <= self.first.start && self.second.end >= self.first.end)
    }
}

#[derive(Debug)]
struct CustomRange {
    start: usize,
    end: usize,
}

impl CustomRange {
    fn from_str(range_str: &str) -> Self {
        let mut range = range_str.split('-').map(|x| x.parse::<usize>().unwrap());
        CustomRange {
            start: range.next().unwrap(),
            end: range.next().unwrap(),
        }
    }
}

fn main() {
    let input = read_to_string("../input.txt").unwrap();

    let part_1_sum: usize = input
        .lines()
        .map(|line| {
            let (first_range, second_range) = line.split_once(',').unwrap();
            let pair: ElfPair = ElfPair {
                first: CustomRange::from_str(first_range),
                second: CustomRange::from_str(second_range),
            };
            pair.contains_full_overlap()
        })
        .filter(|&has_overlap| has_overlap)
        .count();

    println!("The answer for part 1 is {}", part_1_sum);
}
