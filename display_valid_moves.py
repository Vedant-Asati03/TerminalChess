from rich.console import Console

from move_piece.validate_move import ValidateMove
from get_piece_position import GetPiecePosition
from determine_piece_color import DeterminePieceColor


def check_if_piece(piece_moved):
    print(piece_moved)
    # self.params.move.piece_moved[0] = piece_moved


class DisplayValidMoves:

    def __init__(self, params):
        """
        docstring
        """
        self.console = Console()
        self.params = params
        self.validate_move = ValidateMove(self.params)
        # self.piece_colored = DeterminePieceColor(self.params).determine_piece_color()

    def _get_valid_moves(self):
        algebraic_position = GetPiecePosition(self.params).get_piece_position(self.params.saved_game)
        valid_moves = self.validate_move.get_piece_moves(algebraic_position)
