class Knight:
    """
    Represents a Chess Knight.

    Attributes:
        current_square (str): The current square of the Knight.
    """

    def __init__(self, current_square) -> None:
        self.current_square = current_square

    def get_valid_move(self):
        """Checks if the move made by the player is valid for the Knight."""

        columns = list("87654321")
        rows = list("abcdefgh")

        row_index = rows.index(self.current_square[0])
        column_index = columns.index(self.current_square[1])

        knight_moves = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]

        possible_moves = [
            rows[row_index + row_offset] + columns[column_index + column_offset]
            for row_offset, column_offset in knight_moves
            if 0 <= row_index + row_offset < len(rows)
            and 0 <= column_index + column_offset < len(columns)
        ]

        return possible_moves
