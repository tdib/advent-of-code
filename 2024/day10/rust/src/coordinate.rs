#[derive(Debug, Eq, PartialEq, Hash, Clone)]
pub struct Coordinate {
    pub row: usize,
    pub col: usize,
}

impl Coordinate {
    fn up(&self) -> Option<Coordinate> {
        if self.row > 0 {
            Some(Coordinate {
                row: self.row - 1,
                col: self.col,
            })
        } else {
            None
        }
    }

    fn down(&self, max_rows: usize) -> Option<Coordinate> {
        if self.row + 1 < max_rows {
            Some(Coordinate {
                row: self.row + 1,
                col: self.col,
            })
        } else {
            None
        }
    }

    fn left(&self) -> Option<Coordinate> {
        if self.col > 0 {
            Some(Coordinate {
                row: self.row,
                col: self.col - 1,
            })
        } else {
            None
        }
    }

    fn right(&self, max_cols: usize) -> Option<Coordinate> {
        if self.col + 1 < max_cols {
            Some(Coordinate {
                row: self.row,
                col: self.col + 1,
            })
        } else {
            None
        }
    }

    pub fn neighbours(&self, max_rows: usize, max_cols: usize) -> Vec<Coordinate> {
        [
            self.up(),
            self.down(max_rows),
            self.left(),
            self.right(max_cols),
        ]
        .into_iter()
        .flatten()
        .collect()
    }
}
