pub trait Parseable {
    fn parse(&self) -> Vec<Vec<usize>>;
}

impl Parseable for String {
    fn parse(&self) -> Vec<Vec<usize>> {
        self.lines()
            .map(|row| {
                row.chars()
                    .filter_map(|char| char.to_digit(10))
                    .map(|num| num as usize)
                    .collect::<Vec<usize>>()
            })
            .collect()
    }
}
