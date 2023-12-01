use regex::Regex;
use std::fs::read_to_string;

fn main() {
    let input: String = read_to_string("../../input.txt").unwrap();

    println!("Part 1 answer: {}", solve_part_1(&input));
    println!("Part 2 answer: {}", solve_part_2(&input));
}

fn solve_part_1(input: &str) -> usize {
    let mut ans = 0;
    let re = Regex::new(r"\d").unwrap();
    for line in input.lines() {
        let caps: Vec<_> = re.captures_iter(line).collect();

        if caps.is_empty() {
            continue;
        }

        let mut l: &str = "";
        if let Some(first_cap) = caps.first() {
            l = &first_cap[0];
        }

        let mut r: &str = "";
        if let Some(last_cap) = caps.last() {
            r = &last_cap[0];
        }

        ans += format!("{l}{r}").parse::<usize>().unwrap();
    }

    ans
}

fn solve_part_2(input: &str) -> usize {
    let mut ans = 0;
    let re = Regex::new(r"\d").unwrap();
    for line in input.lines() {
        let caps: Vec<_> = re.captures_iter(line).collect();

        let l_num_val: Option<usize> = caps.first().map(|first| first[0].parse().unwrap());
        let r_num_val: Option<usize> = caps.last().map(|last| last[0].parse().unwrap());

        let l_num_idx = l_num_val.and_then(|val| line.find(&val.to_string()));
        let r_num_idx = r_num_val.and_then(|val| line.rfind(&val.to_string()));

        let nums = [
            "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        ];
        let mut l_str_idx = None;
        let mut l_str_val = None;
        let mut r_str_idx = None;
        let mut r_str_val = None;
        for (char_idx, digit_str) in nums.into_iter().enumerate() {
            if let Some(find_idx) = line.find(digit_str) {
                if l_str_idx.is_none() || find_idx < l_str_idx.unwrap() {
                    l_str_idx = Some(find_idx);
                    l_str_val = Some(char_idx + 1);
                }
            }

            if let Some(find_idx) = line.rfind(digit_str) {
                if r_str_idx.is_none() || find_idx > r_str_idx.unwrap() {
                    r_str_idx = Some(find_idx);
                    r_str_val = Some(char_idx + 1);
                }
            }
        }

        let l_num;
        let r_num;
        match (l_str_idx, l_num_idx) {
            // Both strings and ints
            (Some(_), Some(_)) => {
                l_num = if l_str_idx < l_num_idx {
                    l_str_val.unwrap()
                } else {
                    l_num_val.unwrap()
                };

                r_num = if r_str_idx > r_num_idx {
                    r_str_val.unwrap()
                } else {
                    r_num_val.unwrap()
                };
            }

            // Strings only
            (Some(_), None) => {
                l_num = l_str_val.unwrap();
                r_num = r_str_val.unwrap();
            }

            // Ints only
            (None, Some(_)) => {
                l_num = l_num_val.unwrap();
                r_num = r_num_val.unwrap();
            }

            (None, None) => unreachable!(),
        }

        ans += format!("{l_num}{r_num}").parse::<usize>().unwrap();
    }

    ans
}
