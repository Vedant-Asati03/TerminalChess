class GenerateAlgebraicNotation:

    def __init__(self):
        self.generate_algebraic_notation()

    def generate_algebraic_notation(self):
        self.square_algebraic_notation = []

        for rank in range(8, 0, -1):
            for file in ["a", "b", "c", "d", "e", "f", "g", "h"]:
                self.square_algebraic_notation.append(f"{file}{rank}")


class HighlightMove:

    def __init__(self, move, previous_square):
        self.move = move
        self.previous_square = previous_square
        self.algebraic_notation = GenerateAlgebraicNotation()

    def highlight_move(self, i, j):
        """Highlights the move on the chessboard.

        Args:
            i (int): Row index.
            j (int): Column index.

        Returns:
            str: The background color for highlighting the move.
        """

        if self.previous_square is None:
            return None

        if (
            self.algebraic_notation.square_algebraic_notation[i * 8 + j] == self.move
            and self.updated_game is not None
        ):
            return "#BBCB44"
        if (
            self.algebraic_notation.square_algebraic_notation[i * 8 + j]
            == self.previous_square
        ):
            return "#F5F67F"
        return None
