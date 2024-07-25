from enum import Enum


class PieceColor(Enum):
    WHITE = "w"
    BLACK = "b"


class DeterminePieceColor:

    def __init__(self, params):
        self.params = params
    
    def determine_piece_color(self):
        """Determines the color of the current player's piece.

        Returns:
            str: The current player's piece.
        """
        piece_color = (
            f"{PieceColor.WHITE.value}{self.params.move.piece_moved}"
            if self.params.player.playing == self.params.player.player_white
            else f"{PieceColor.BLACK.value}{self.params.move.piece_moved}"
        )

        return piece_color
