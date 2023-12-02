use std::fs::read_to_string;

fn main() {
    let input: String = read_to_string("../../input.txt").expect("Input file not found");

    println!("Part 1 answer: {}", solve_part_1(&input));
    println!("Part 2 answer: {}", solve_part_2(&input));
}

#[derive(Debug)]
struct Game {
    game_id: usize,
    highest_red: usize,
    highest_green: usize,
    highest_blue: usize,
}

#[derive(Debug, Eq, PartialEq, Hash)]
enum Colour {
    Red,
    Green,
    Blue,
}

impl Colour {
    fn from_str(s: &str) -> Self {
        match s.to_lowercase().as_str() {
            "red" => Self::Red,
            "green" => Self::Green,
            "blue" => Self::Blue,
            _ => unreachable!(),
        }
    }
}

fn get_max_colour_counts(line: &str) -> Game {
    let mut red = 0;
    let mut green = 0;
    let mut blue = 0;

    // ["Game 1", "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"]
    let game_split = line.split(": ").collect::<Vec<_>>();
    // "Game 1" -> 1
    let game_id: usize = game_split[0]
        .split(' ')
        .next_back()
        .unwrap()
        .parse()
        .unwrap();

    // ["3 blue, 4 red", "1 red, 2 green", "6 blue, 2 green"]
    let game_sets = game_split[1].split(';').collect::<Vec<_>>();

    // ["3 blue", "4 red"], ["1 red", "2 green"], etc.
    let game_sets = game_sets.iter().map(|set| set.trim().split(", "));
    for set in game_sets {
        for item in set {
            // Parse the colour and amount
            // amount -> 3
            // colour -> Colour::Blue
            let mut parts = item.split(' ');
            let amount = parts.next().unwrap().parse::<usize>().unwrap();
            let colour = Colour::from_str(parts.next().unwrap());

            // Check if this colour amount is higher than our currently stored one
            match colour {
                Colour::Red => red = red.max(amount),
                Colour::Green => green = green.max(amount),
                Colour::Blue => blue = blue.max(amount),
            }
        }
    }

    Game {
        game_id,
        highest_red: red,
        highest_green: green,
        highest_blue: blue,
    }
}

const MAX_RED: usize = 12;
const MAX_GREEN: usize = 13;
const MAX_BLUE: usize = 14;
fn solve_part_1(input: &str) -> usize {
    let mut ans = 0;
    for line in input.lines() {
        let Game {
            game_id,
            highest_red,
            highest_green,
            highest_blue,
        } = get_max_colour_counts(line);

        if highest_red <= MAX_RED && highest_blue <= MAX_BLUE && highest_green <= MAX_GREEN {
            ans += game_id
        }
    }
    ans
}

fn solve_part_2(input: &str) -> usize {
    let mut ans = 0;
    for line in input.lines() {
        let Game {
            game_id: _,
            highest_red,
            highest_green,
            highest_blue,
        } = get_max_colour_counts(line);

        ans += highest_red * highest_green * highest_blue;
    }
    ans
}
