use std::collections::HashSet;
use std::fs::read_to_string;

fn main() {
    let input: String = read_to_string("../input.txt").unwrap();

    let rucksacks: Vec<&str> = input.lines().collect();

    // Split each rucksack into two halves, find the common characters, and sum the value across all characters
    let part_1_sum: usize = rucksacks
        .clone()
        .into_iter()
        .map(|rucksack| {
            get_char_score(
                *get_common_char(
                    vec![
                        &rucksack[0..rucksack.len() / 2],
                        &rucksack[rucksack.len() / 2..],
                    ]
                    .as_slice(),
                )
                .iter()
                .next()
                .unwrap(),
            )
        })
        .sum();

    // Split all rucksacks into chunks of 3, find the common characters, and sum the value across all characters
    const CHUNK_SIZE: usize = 3;
    let part_2_sum: usize = rucksacks
        .chunks(CHUNK_SIZE)
        .map(|chunk| get_char_score(*get_common_char(chunk).iter().next().unwrap()))
        .sum();

    println!("The answer for part 1 is {}", part_1_sum);
    println!("The answer for part 2 is {}", part_2_sum);
}

///
/// Computes the score of a character using the format:
/// a=1, b=2, ..., z=26, A=27, B=28, ..., Z=52
///
/// # Arguments
/// * `c` - A character to compute the score of
///
/// # Example
/// ```
/// let score = get_char_score('a'); // returns 1
/// let score = get_char_score('z'); // returns 26
/// let score = get_char_score('A'); // returns 27
/// let score = get_char_score('Z'); // returns 52
/// ```
fn get_char_score(c: char) -> usize {
    const LOWERCASE_OFFSET: usize = 96;
    const UPPERCASE_OFFSET: usize = 38;
    match c {
        'a'..='z' => c as usize - LOWERCASE_OFFSET,
        'A'..='Z' => c as usize - UPPERCASE_OFFSET,
        _ => panic!("Invalid char"),
    }
}

/// Computes the intersection character(s) of multiple strings
///
/// # Arguments
/// * `strings` - A slice of strings to compute the intersection of
///
/// # Example
/// ```
/// let strings = vec!["abc", "bcd", "cde"];
/// let intersection = get_common_char(strings); // returns 'c'
/// assert_eq!(intersection, HashSet::from_iter(vec!['c'].iter()));
/// ```
///
/// ```
/// let strings = vec!["abc", "bdd"];
/// let intersection = get_common_char(strings); // returns 'b'
/// assert_eq!(intersection, HashSet::from_iter(vec!['b'].iter()));
/// ```
///
fn get_common_char(strings: &[&str]) -> HashSet<char> {
    strings
        .iter()
        .map(|str| HashSet::from_iter(str.chars()))
        .reduce(|acc, val| acc.intersection(&val).cloned().collect())
        .unwrap_or_default()
}
