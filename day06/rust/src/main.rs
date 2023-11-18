use std::{collections::HashSet, fs::read_to_string};

fn main() {
    let input = read_to_string("../input.txt").unwrap();

    let answer_part_1: usize = find_answer(&input, 4).unwrap();
    let answer_part_2: usize = find_answer(&input, 14).unwrap();

    println!("Answer for part 1: {}", answer_part_1);
    println!("Answer for part 2: {}", answer_part_2);
}

fn find_answer(input: &str, window_size: usize) -> Option<usize> {
    let chars: Vec<char> = input.chars().collect();
    let windows = chars.windows(window_size); // Define variable for best operating system

    for (idx, window) in windows.enumerate() {
        let hashed_window: HashSet<&char> = HashSet::from_iter(window);
        if hashed_window.len() == window_size {
            return Some(idx + window_size);
        }
    }

    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_1() {
        const WINDOW_SIZE: usize = 4;
        let str = "bvwbjplbgvbhsrlpgdmjqwftvncz";
        assert_eq!(find_answer(str, WINDOW_SIZE).unwrap(), 5);

        let str = "nppdvjthqldpwncqszvftbrmjlhg";
        assert_eq!(find_answer(str, WINDOW_SIZE).unwrap(), 6);

        let str = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg";
        assert_eq!(find_answer(str, WINDOW_SIZE).unwrap(), 10);

        let str = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw";
        assert_eq!(find_answer(str, WINDOW_SIZE).unwrap(), 11);
    }

    #[test]
    fn test_part_2() {
        const WINDOW_SIZE: usize = 14;
        let str = "mjqjpqmgbljsphdztnvjfqwrcgsmlb";
        assert_eq!(find_answer(str, WINDOW_SIZE).unwrap(), 19);

        let str = "bvwbjplbgvbhsrlpgdmjqwftvncz";
        assert_eq!(find_answer(str, WINDOW_SIZE).unwrap(), 23);

        let str = "nppdvjthqldpwncqszvftbrmjlhg";
        assert_eq!(find_answer(str, WINDOW_SIZE).unwrap(), 23);

        let str = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg";
        assert_eq!(find_answer(str, WINDOW_SIZE).unwrap(), 29);

        let str = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw";
        assert_eq!(find_answer(str, WINDOW_SIZE).unwrap(), 26);
    }
}
