use std::fs::read_to_string;

fn main() {
    let input: String = read_to_string("../input.txt").unwrap();

    #[derive(PartialEq)]
    enum Outcome {
        Win,
        Draw,
        Lose,
    }

    impl Outcome {
        // Score based on the outcome of the game
        fn score(&self) -> usize {
            match self {
                Outcome::Win => 6,
                Outcome::Draw => 3,
                Outcome::Lose => 0,
            }
        }

        // Convert an outcome to a move based on the opponent's move
        fn to_move(&self, their_move: &Move) -> Move {
            match self {
                Outcome::Win => their_move.loses_against(),
                Outcome::Draw => their_move.clone(),
                Outcome::Lose => their_move.wins_against(),
            }
        }
    }

    #[derive(PartialEq, Clone)]
    enum Move {
        Rock,
        Paper,
        Scissors,
    }

    impl Move {
        // Determine the outcome of a game given both moves
        fn get_outcome(&self, other: &Move) -> Outcome {
            if self == other {
                Outcome::Draw
            } else if self.beats(other) {
                Outcome::Win
            } else {
                Outcome::Lose
            }
        }

        // Find the move that this move wins against
        fn wins_against(&self) -> Move {
            match self {
                Move::Rock => Move::Scissors,
                Move::Paper => Move::Rock,
                Move::Scissors => Move::Paper,
            }
        }

        // Find the move that this move loses against
        fn loses_against(&self) -> Move {
            match self {
                Move::Rock => Move::Paper,
                Move::Paper => Move::Scissors,
                Move::Scissors => Move::Rock,
            }
        }

        // Determine if this move beats the other move
        fn beats(&self, other: &Move) -> bool {
            return self.wins_against() == *other;
        }

        // Score based on the move
        fn score(&self) -> usize {
            match self {
                Move::Rock => 1,
                Move::Paper => 2,
                Move::Scissors => 3,
            }
        }
    }

    // Convert chars (given as input) to Move enum
    fn char_to_move(c: &char) -> Move {
        match c {
            'A' | 'X' => Move::Rock,
            'B' | 'Y' => Move::Paper,
            'C' | 'Z' => Move::Scissors,
            _ => panic!("Invalid move"),
        }
    }

    // Convert chars (given as input) to Outcome enum as defined in part 2
    fn char_to_outcome(c: &char) -> Outcome {
        match c {
            'X' => Outcome::Lose,
            'Y' => Outcome::Draw,
            'Z' => Outcome::Win,
            _ => panic!("Invalid move"),
        }
    }

    // Play a game of rock paper scissors, return the score
    fn play_game(my_move: &Move, their_move: &Move) -> usize {
        let outcome = my_move.get_outcome(their_move);
        return my_move.score() + outcome.score();
    }

    let mut part_1_sum: usize = 0;
    let mut part_2_sum: usize = 0;
    for line in input.lines() {
        // let parts: Vec<char> = line.split_whitespace().collect();
        let parts: Vec<char> = line.chars().filter(|&c| !c.is_whitespace()).collect();

        if let [their_char, my_char] = parts.as_slice() {
            let their_move = char_to_move(their_char);
            let my_move_part1 = char_to_move(my_char);

            let game_outcome = char_to_outcome(my_char);
            let my_move_part2 = game_outcome.to_move(&their_move);

            part_1_sum += play_game(&my_move_part1, &their_move);
            part_2_sum += play_game(&my_move_part2, &their_move)
        }
    }

    println!("The answer for part 1 is {}", part_1_sum);
    println!("The answer for part 2 is {}", part_2_sum);
}
