pub struct Offset {
    pub row_offset: isize,
    pub col_offset: isize,
}
pub const UP: Offset = Offset {
    row_offset: -1,
    col_offset: 0,
};
pub const DOWN: Offset = Offset {
    row_offset: 1,
    col_offset: 0,
};
pub const LEFT: Offset = Offset {
    row_offset: 0,
    col_offset: -1,
};
pub const RIGHT: Offset = Offset {
    row_offset: 0,
    col_offset: 1,
};
pub const DIRECTION_OFFSETS: [Offset; 4] = [UP, DOWN, LEFT, RIGHT];
