use std::collections::HashMap;
use std::fs::read_to_string;

fn main() {
    let input = read_to_string("../input.txt").expect("Input file not found");

    println!("Part 1 answer: {}", solve_part_1(input.trim()));
    println!("Part 2 answer: {}", solve_part_2(input.trim()));
}

fn solve_part_1(input: &str) -> usize {
    let nums = input
        .split_whitespace()
        .flat_map(|num| num.parse::<usize>())
        .collect::<Vec<usize>>();

    let mut updated_stones: Vec<usize> = nums;
    for _ in 0..25 {
        let new_stones = &updated_stones
            .iter()
            .flat_map(|num| {
                let num_str = num.to_string();
                let num_len = num_str.len();
                if *num == 0 {
                    vec![1]
                } else if num_len % 2 == 0 {
                    let (first_half, second_half) = num_str.split_at(num_len / 2);
                    let first_half = first_half
                        .parse::<usize>()
                        .expect("Failed to parse first half of num");
                    let second_half = second_half
                        .parse::<usize>()
                        .expect("Failed to parse second half of num");
                    vec![first_half, second_half]
                } else {
                    vec![num * 2024]
                }
            })
            .collect::<Vec<usize>>();
        updated_stones = new_stones.to_owned();
    }

    updated_stones.len()
}

fn compute_n_blinks(
    num: usize,
    nums_left: usize,
    cache: &mut HashMap<(usize, usize), usize>,
) -> usize {
    let cache_key = (num, nums_left);
    if cache.contains_key(&cache_key) {
        return cache.get_key_value(&cache_key).unwrap().1.to_owned();
    }

    if nums_left == 0 {
        return 1;
    }

    let num_str = num.to_string();
    let num_len = num_str.len();
    let result = if num == 0 {
        compute_n_blinks(1, nums_left - 1, cache)
    } else if num_len % 2 == 0 {
        let (first_half, second_half) = num_str.split_at(num_len / 2);
        let first_half = first_half
            .parse::<usize>()
            .expect("Failed to parse first half of num");
        let second_half = second_half
            .parse::<usize>()
            .expect("Failed to parse second half of num");
        compute_n_blinks(first_half, nums_left - 1, cache)
            + compute_n_blinks(second_half, nums_left - 1, cache)
    } else {
        compute_n_blinks(num * 2024, nums_left - 1, cache)
    };
    cache.insert(cache_key, result);
    result
}

fn solve_part_2(input: &str) -> usize {
    let nums = input
        .split_whitespace()
        .flat_map(|num| num.parse::<usize>())
        .collect::<Vec<usize>>();

    let mut total = 0;
    let nums_to_compute = 75;
    let mut cache = HashMap::new();
    nums.into_iter().for_each(|num| {
        total += compute_n_blinks(num, nums_to_compute, &mut cache);
    });

    total
}
