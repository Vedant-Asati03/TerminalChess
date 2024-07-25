from determine_piece_color import DeterminePieceColor


class RestrictedInvalidMoves:
    """
    Validates moves for all pieces.

    Attributes:
        move (str): The move to be validated.
        position (str): The position of the moved piece.
        replaced_piece (str): The piece that will be replaced.
        players_piece (str): The current player's piece.
    """

    def __init__(self, params):
        self.params = params
        self.piece_colored = DeterminePieceColor(self.params).determine_piece_color()

        self._get_piece_color_from_piece()

    def _get_piece_color_from_piece(self):
        self.piece_color = "w" if self.piece_colored.startswith("w") else "b"

    def check_for_same_color_piece(self, target_cell_index, replaced_piece):
        """Checks if the move involves replacing a piece of the same color
        (for every move).

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if target_cell_index is None:
            return None

        if replaced_piece is None:
            return None

        target_cell = self.params.cell_name[target_cell_index]

        if (
            replaced_piece[0] == self.piece_color
            and self.params.move.move == target_cell
        ):
            return True

        return None

    def check_for_occupied_squares(self, index: int):
        """Checks if the square is occupied or not
        (for each piece possible moves).

        Returns:
            bool: True if the move is valid, False otherwise.
        """

        target_cell_index = self.params.cell_name.index(index)
        checked_piece_color = self.params.saved_game[target_cell_index][0]

        if self.piece_color == checked_piece_color:
            return False

        return None

    def jumping_over_pieces(self, current_position):
        if self.piece_colored[1] == "n":  # Knights can jump over pieces
            return None

        row_labels = list("abcdefgh")
        current_row, target_row = map(
            row_labels.index, [current_position[0], self.params.move.move[0]]
        )

        column_labels = list("12345678")
        current_column, target_column = map(
            column_labels.index, [current_position[1], self.params.move.move[1]]
        )

        rows_between = range(
            min(current_row, target_row) + 1, max(current_row, target_row)
        )
        columns_between = range(
            min(current_column, target_column) + 1, max(current_column, target_column)
        )

        # Check for horizontal, vertical, and diagonal moves
        if current_row == target_row:
            squares_to_check = [
                row_labels[current_row] + column_labels[col] for col in columns_between
            ]
        elif current_column == target_column:
            squares_to_check = [
                row_labels[row] + column_labels[current_column] for row in rows_between
            ]
        elif abs(current_row - target_row) == abs(current_column - target_column):
            squares_to_check = [
                row_labels[row] + column_labels[col]
                for row, col in zip(rows_between, columns_between)
            ]
        else:
            return True

        for square in squares_to_check:
            square_index = self.params.cell_name.index(square)
            piece_at_square = self.params.saved_game[square_index]

            if piece_at_square != " ":
                return True

        return None
