class Queen:
    """
    Represents a Chess Queen.

    Attributes:
        current_square (str): The current square of the Queen.
    """

    def __init__(self, current_square) -> None:
        self.current_square = current_square

    def get_valid_move(self):
        """Checks if the move made by the player is valid for the Queen."""

        columns = list("87654321")
        rows = list("abcdefgh")

        row_index = rows.index(self.current_square[0])
        column_index = columns.index(self.current_square[1])

        queen_moves = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),  # Horizontal and Vertical moves
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),  # Diagonal moves
        ]

        possible_moves = []
        for row_offset, column_offset in queen_moves:
            row, col = row_index, column_index
            while True:
                row += row_offset
                col += column_offset
                if 0 <= row < len(rows) and 0 <= col < len(columns):
                    possible_moves.append(rows[row] + columns[col])
                else:
                    break

        return possible_moves
