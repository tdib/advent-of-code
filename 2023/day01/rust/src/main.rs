use fancy_regex::{Captures, Regex};
use std::fs::read_to_string;

const NUMS: [&str; 9] = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
];

fn main() {
    let input: String = read_to_string("../../input.txt").expect("Input file not found");

    println!("Part 1 answer: {}", solve_part_1(&input));
    println!("Part 2 answer: {}", solve_part_2(&input));
}

/// Generic solve method that finds all regex matches in the input,
/// and sums the first and last matches for each line.
/// *Note: The regex must contain a positive lookahead to work properly*
///
/// The sum of the first and last number of each line, across all lines
fn solve(input: &str, pattern: Regex) -> usize {
    let mut ans = 0;
    for line in input.lines() {
        let caps: Vec<_> = pattern.captures_iter(line).collect();

        // Check to ensure all types of inputs work
        if !caps.is_empty() {
            // Leftmost match
            let l = parse_capture(caps.first());
            // Rightmost match
            let r = parse_capture(caps.last());
            ans += 10 * l + r;
        }
    }

    ans
}

fn solve_part_1(input: &str) -> usize {
    // Match any digits in a string
    // Note: positive lookahead is not strictly necessary for the problem,
    // but is included to make the generic parse method work
    let re = Regex::new(r"(?=(\d))").unwrap();
    solve(input, re)
}

fn solve_part_2(input: &str) -> usize {
    // Match any digit or string representation of a digit
    let re = Regex::new(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))").unwrap();
    solve(input, re)
}

/// Given a captures_iter option, parse it such that we return a usize of the digit matched
/// (e.g. "1" -> 1), or a usize corresponding to a string representation (e.g. "one" -> 1)
fn parse_capture(cap: Option<&Result<Captures, fancy_regex::Error>>) -> usize {
    cap.unwrap()
        .as_ref()
        .unwrap()
        .get(1)
        .map(|m| {
            // Check if we have a digit like "1", or a string representation like "one"
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
