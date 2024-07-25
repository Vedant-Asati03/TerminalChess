class Pawn:
    """
    Represents a Chess Pawn.

    Attributes:
        current_square (str): The current square of the Pawn.
    """

    def __init__(
        self, current_square, players_piece
    ) -> None:
        self.current_square = current_square
        self.piece_color = players_piece[0]

    def get_valid_move(self):
        """Checks if the move made by the player is valid for the Pawn."""
        pawn_offsets = {"w": -1, "b": 1}
        opt = pawn_offsets.get(self.piece_color)

        columns = list("87654321")
        rows = list("abcdefgh")

        row_index = rows.index(self.current_square[0])
        column_index = columns.index(self.current_square[1])

        possible_moves = []

        if column_index in (1, 6):
            moves = [
                rows[row_index] + columns[column_index + opt],
                rows[row_index] + columns[column_index + 2 * opt],
            ]
            possible_moves.extend(moves)
        else:
            possible_moves.append(rows[row_index] + columns[column_index + opt])

        return possible_moves
