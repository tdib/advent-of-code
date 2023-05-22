use std::fs::read_to_string;

fn main() {
    let input: String = read_to_string("../input.txt").unwrap();

    let mut sum_vec: Vec<usize> = Vec::new();
    let mut curr_sum: usize = 0;
    for line in input.lines() {
        // If we have reached an empty line, we have finished counting for this group
        if line.is_empty() {
            sum_vec.push(curr_sum);
            curr_sum = 0;
        // Otherwise, we add to the current sum
        } else {
            let temp: usize = line.parse().unwrap();
            curr_sum += temp;
        }
    }
    // The last group will not have an empty line after it, so we need to add it manually
    sum_vec.push(curr_sum);

    // Find the max element in the vector
    println!("The answer for part 1 is {}", sum_vec.iter().max().unwrap());

    // Sort the vector in descending order, and take the first 3 elements
    sum_vec.sort_unstable();
    println!(
        "The answer for part 2 is {}",
        sum_vec.iter().rev().take(3).sum::<usize>()
    );
}
