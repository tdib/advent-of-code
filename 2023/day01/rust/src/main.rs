use fancy_regex::{Captures, Regex};
use std::fs::read_to_string;

fn main() {
    let input: String = read_to_string("../../input.txt").expect("Input file not found");

    println!("Part 1 answer: {}", solve_part_1(&input));
    println!("Part 2 answer: {}", solve_part_2(&input));
}

fn solve(input: &str, pattern: Regex) -> usize {
    let mut ans = 0;
    for line in input.lines() {
        let caps: Vec<_> = pattern.captures_iter(line).collect();

        // Check to ensure all types of inputs work
        if !caps.is_empty() {
            let l = parse_capture(caps.first());
            let r = parse_capture(caps.last());
            ans += 10 * l + r;
        }
    }

    ans
}

fn solve_part_1(input: &str) -> usize {
    // Positive lookahead is not strictly necessary for the problem, but is included to make the
    // generic parse method work
    let re = Regex::new(r"(?=(\d))").unwrap();
    solve(input, re)
}

fn solve_part_2(input: &str) -> usize {
    let re = Regex::new(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))").unwrap();
    solve(input, re)
}

const NUMS: [&str; 9] = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
];
fn parse_capture(cap: Option<&Result<Captures, fancy_regex::Error>>) -> usize {
    cap.unwrap()
        .as_ref()
        .unwrap()
        .get(1)
        .map(|m| {
            let m = m.as_str();
            if NUMS.contains(&m) {
                Ok(NUMS.iter().position(|item| item == &m).unwrap() + 1)
            } else {
                m.parse()
            }
        })
        .unwrap()
        .unwrap()
}
