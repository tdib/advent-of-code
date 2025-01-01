use std::collections::HashMap;
use std::fs::read_to_string;

fn main() {
    let nums = read_to_string("../input.txt")
        .expect("Input file not found")
        .split_whitespace()
        .flat_map(|num| num.parse::<usize>())
        .collect::<Vec<usize>>();
    let mut cache = HashMap::new();
    println!("Part 1 answer: {}", solve(nums.clone(), &mut cache, 25));
    println!("Part 2 answer: {}", solve(nums.clone(), &mut cache, 75));
}

fn solve(nums: Vec<usize>, cache: &mut HashMap<(usize, usize), usize>, iterations: usize) -> usize {
    let mut total = 0;
    nums.iter().for_each(|num| {
        total += compute_n_blinks(*num, iterations, cache);
    });

    total
}

fn compute_n_blinks(
    num: usize,
    iterations_left: usize,
    cache: &mut HashMap<(usize, usize), usize>,
) -> usize {
    let cache_key = (num, iterations_left);
    if let Some(kv) = cache.get_key_value(&cache_key) {
        return kv.1.to_owned();
    }

    if iterations_left == 0 {
        return 1;
    }

    let num_str = num.to_string();
    let num_len = num_str.len();
    let result = if num == 0 {
        compute_n_blinks(1, iterations_left - 1, cache)
    } else if num_len % 2 == 0 {
        let (first_half, second_half) = num_str.split_at(num_len / 2);
        compute_n_blinks(
            first_half
                .parse::<usize>()
                .expect("Failed to parse first half of num"),
            iterations_left - 1,
            cache,
        ) + compute_n_blinks(
            second_half
                .parse::<usize>()
                .expect("Failed to parse second half of num"),
            iterations_left - 1,
            cache,
        )
    } else {
        compute_n_blinks(num * 2024, iterations_left - 1, cache)
    };
    cache.insert(cache_key, result);
    result
}
