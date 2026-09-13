class Pawn:
    """
    Represents a Chess Pawn.

    Attributes:
        current_square (str): The current square of the Pawn.
    """

    def __init__(
        self, current_square, players_piece, saved_game, cell_name
    ) -> None:
        self.current_square = current_square
        self.piece_color = players_piece[0]
        self.saved_game = saved_game
        self.cell_name = cell_name

    def _piece_at(self, square):
        return self.saved_game[self.cell_name.index(square)]

    def get_valid_move(self):
        """Checks if the move made by the player is valid for the Pawn."""
        pawn_offsets = {"w": -1, "b": 1}
        opt = pawn_offsets.get(self.piece_color)

        columns = list("87654321")
        rows = list("abcdefgh")

        row_index = rows.index(self.current_square[0])
        column_index = columns.index(self.current_square[1])

        possible_moves = []

        forward_one = rows[row_index] + columns[column_index + opt]
        if self._piece_at(forward_one) == " ":
            possible_moves.append(forward_one)

            if column_index in (1, 6):
                forward_two = rows[row_index] + columns[column_index + 2 * opt]
                if self._piece_at(forward_two) == " ":
                    possible_moves.append(forward_two)

        return possible_moves
