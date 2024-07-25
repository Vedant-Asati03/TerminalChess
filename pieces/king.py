import itertools


class King:
    """
    Represents a Chess King.

    Attributes:
        current_square (str): The current square of the King.
    """

    def __init__(self, current_square) -> None:
        self.current_square = current_square

    def get_valid_move(self):
        """Checks if the move made by the player is valid for the King."""

        columns = list("87654321")
        rows = list("abcdefgh")

        row_index = rows.index(self.current_square[0])
        column_index = columns.index(self.current_square[1])

        row_offsets = [-1, 0, 1]
        column_offsets = [-1, 0, 1]

        # Generate all possible combinations of row and column offsets
        possible_moves = [
            rows[row_index + row_offset] + columns[column_index + column_offset]
            for row_offset, column_offset in itertools.product(
                row_offsets, column_offsets
            )
            if 0 <= row_index + row_offset < len(rows)
            and 0 <= column_index + column_offset < len(columns)
            and (row_offset, column_offset) != (0, 0)
        ]

        return possible_moves
