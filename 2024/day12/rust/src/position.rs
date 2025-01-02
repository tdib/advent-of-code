use crate::Map;
use crate::Offset;
use crate::DIRECTION_OFFSETS;

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
pub struct Position {
    pub row: isize,
    pub col: isize,
}

impl Position {
    pub fn offset(&self, offset: &Offset) -> Self {
        Self {
            row: self.row + offset.row_offset,
            col: self.col + offset.col_offset,
        }
    }

    pub fn neighbours(&self, map: &Map) -> Vec<Position> {
        DIRECTION_OFFSETS
            .iter()
            .flat_map(|direction| {
                let neighbour_dir = self.offset(direction);
                if map.within_bounds(&neighbour_dir) {
                    Some(neighbour_dir)
                } else {
                    None
                }
            })
            .collect()
    }
}
