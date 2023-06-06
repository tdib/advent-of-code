use regex::Regex;
use std::{
    fs::read_to_string,
    ops::{Deref, DerefMut},
};

#[derive(Clone, Copy)]
struct Crate(char);
impl Deref for Crate {
    type Target = char;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Clone)]
struct Stack(Vec<Crate>);
impl Deref for Stack {
    type Target = Vec<Crate>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
impl DerefMut for Stack {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}
impl Stack {
    fn with_capacity(capacity: usize) -> Self {
        Self(Vec::with_capacity(capacity))
    }
}

struct Ship(Vec<Stack>);
impl Deref for Ship {
    type Target = Vec<Stack>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
impl DerefMut for Ship {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

fn main() {
    let (crates, instructions) = read_to_string("../input.txt")
        .unwrap()
        .split_once("\r\n\r\n")
        .map(|(x, y)| (x.to_string(), y.to_string()))
        .unwrap();

    const CRATE_REPR_WIDTH: usize = 4;

    let num_stacks = (crates.lines().peekable().peek().unwrap().len() + 1) / CRATE_REPR_WIDTH;
    let lines: Vec<&str> = crates.lines().collect();

    let mut original_stacks: Ship = Ship(vec![
        Stack::with_capacity(lines.len() * num_stacks);
        num_stacks
    ]);

    // Convert crates into data structure
    for line in &lines[..lines.len() - 1] {
        let curr_line = line.chars().collect::<Vec<_>>();
        let crate_chars = curr_line.chunks(CRATE_REPR_WIDTH).map(|c| c[1]);
        for (idx, crate_char) in crate_chars.enumerate() {
            if crate_char != ' ' {
                original_stacks[idx].insert(0, Crate(crate_char));
            }
        }
    }

    let mut stacks_part_1 = original_stacks.clone();
    let mut stacks_part_2 = original_stacks.clone();

    // Parse instructions
    for instruction in instructions.lines() {
        let re = Regex::new(r"move (\d+) from (\d+) to (\d+)").unwrap();
        let caps = re.captures(instruction).unwrap();

        let amount: usize = caps[1].parse().unwrap();
        let from: usize = caps[2].parse().unwrap();
        let from = from - 1;
        let to: usize = caps[3].parse().unwrap();
        let to = to - 1;

        // PART 1: Move crates one at a time
        for _ in 0..amount {
            let crate_to_move = stacks_part_1[from].pop().unwrap();
            stacks_part_1[to].push(crate_to_move);
        }

        // PART 2: Move crates all at once
        // Get `amount` crates to move from the top of the `from` stack
        let stack_height = stacks_part_2[from].len();
        let mut crates_to_move = stacks_part_2[from][stack_height - amount..].to_vec();
        // Remove the crates from the `from` stack and add them to the `to` stack
        stacks_part_2[from].truncate(stack_height - amount);
        stacks_part_2[to].append(&mut crates_to_move);
    }

    let top_of_stacks_part_1: String = read_top_of_stacks(&stacks_part_1);
    let top_of_stacks_part_2: String = read_top_of_stacks(&stacks_part_2);

    println!("Answer to part 1: {}", top_of_stacks_part_1);
    println!("Answer to part 2: {}", top_of_stacks_part_2);
}

/// Read the top of each stack and return a string of those crates
fn read_top_of_stacks(stacks: &[Stack]) -> String {
    stacks
        .iter()
        .map(|s| s.last().unwrap())
        .map(|c| c.0)
        .collect()
}
