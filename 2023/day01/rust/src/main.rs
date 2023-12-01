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

        let mut l_num_val: Option<usize> = None;
        let mut r_num_val: Option<usize> = None;
        if !caps.is_empty() {
            if let Some(first_cap) = caps.first() {
                l_num_val = first_cap[0].parse::<usize>().ok();
            }

            if let Some(last_cap) = caps.last() {
                r_num_val = last_cap[0].parse::<usize>().ok();
            }
        }

        let l_num_idx = if let Some(val) = l_num_val {
            line.find(&val.to_string())
        } else {
            None
        };
        let r_num_idx = if let Some(val) = r_num_val {
            line.find(&val.to_string())
        } else {
            None
        };

        let nums = vec![
            "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        ];
        let mut l_str_idx = None;
        let mut l_str_val = None;
        let mut r_str_idx = None;
        let mut r_str_val = None;
        for (char_idx, num_str) in nums.iter().enumerate() {
            if line.contains(num_str) {
                if let Some(find_idx) = line.find(num_str) {
                    if l_str_idx.is_none() || find_idx < l_str_idx.unwrap() {
                        l_str_idx = Some(find_idx);
                        l_str_val = Some(char_idx + 1);
                    }
                }

                if let Some(find_idx) = line.rfind(num_str) {
                    if r_str_idx.is_none() || find_idx > r_str_idx.unwrap() {
                        r_str_idx = Some(find_idx);
                        r_str_val = Some(char_idx + 1);
                    }
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

                r_num = if r_str_idx.unwrap() > r_num_idx.unwrap() {
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

        println!("{line}");
        println!("Nums: {l_num_val:?} ({l_num_idx:?}), {r_num_val:?} ({r_num_idx:?})");
        println!("Strs: {l_str_val:?} ({l_str_idx:?}), {r_str_val:?} ({r_str_idx:?})");
        println!("Selected: {l_num:?} {r_num:?}");
        println!();
        //
        ans += format!("{l_num}{r_num}").parse::<usize>().unwrap();
    }

    ans
}
