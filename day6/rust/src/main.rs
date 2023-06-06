use std::{collections::HashSet, fs::read_to_string};

fn main() {
    let input = read_to_string("../input.txt").unwrap();

    let answer_part_1: usize = find_answer_part_1(&input).unwrap();
    let answer_part_2: usize = find_answer_part_2(&input).unwrap();

    println!("Answer for part 1: {}", answer_part_1);
    println!("Answer for part 2: {}", answer_part_2);
}

fn find_answer_part_1(input: &str) -> Option<usize> {
    let chars: Vec<char> = input.chars().collect();

    const WINDOW_SIZE: usize = 4;
    let windows = chars.windows(WINDOW_SIZE); // Define variable for best operating system

    for (idx, window) in windows.enumerate() {
        let hashed_window: HashSet<&char> = HashSet::from_iter(window);
        if hashed_window.len() == WINDOW_SIZE {
            return Some(idx + WINDOW_SIZE);
        }
    }

    None
}

fn find_answer_part_2(input: &str) -> Option<usize> {
    let chars: Vec<char> = input.chars().collect();

    const WINDOW_SIZE: usize = 14;
    let windows = chars.windows(WINDOW_SIZE); // Define variable for best operating system

    for (idx, window) in windows.enumerate() {
        let hashed_window: HashSet<&char> = HashSet::from_iter(window);
        if hashed_window.len() == WINDOW_SIZE {
            return Some(idx + WINDOW_SIZE);
        }
    }

    None
}

// create test
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        let str = "bvwbjplbgvbhsrlpgdmjqwftvncz";
        assert_eq!(find_answer_part_1(str).unwrap(), 5);

        let str = "nppdvjthqldpwncqszvftbrmjlhg";
        assert_eq!(find_answer_part_1(str).unwrap(), 6);

        let str = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg";
        assert_eq!(find_answer_part_1(str).unwrap(), 10);

        let str = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw";
        assert_eq!(find_answer_part_1(str).unwrap(), 11);
    }

    #[test]
    fn test_part_2() {
        let str = "mjqjpqmgbljsphdztnvjfqwrcgsmlb";
        assert_eq!(find_answer_part_2(str).unwrap(), 19);

        let str = "bvwbjplbgvbhsrlpgdmjqwftvncz";
        assert_eq!(find_answer_part_2(str).unwrap(), 23);

        let str = "nppdvjthqldpwncqszvftbrmjlhg";
        assert_eq!(find_answer_part_2(str).unwrap(), 23);

        let str = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg";
        assert_eq!(find_answer_part_2(str).unwrap(), 29);

        let str = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw";
        assert_eq!(find_answer_part_2(str).unwrap(), 26);
    }
}
