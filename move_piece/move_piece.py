from rich.console import Console

from .validate_move import ValidateMove
from determine_piece_color import DeterminePieceColor
from get_piece_position import GetPiecePosition


class MovePiece:

    def __init__(self, params) -> None:
        self.console = Console()
        self.params = params

        self.validate_move = ValidateMove(self.params)
        self.piece_colored = DeterminePieceColor(self.params).determine_piece_color()
        self.get_piece_position = GetPiecePosition(self.params)

    def _swap_pieces(self, square, position, saved_game):
        piece_to_move = saved_game[square]
        saved_game[square] = self.piece_colored
        saved_game[position] = piece_to_move

        return piece_to_move

    def move_piece(self):
        """Moves the chess piece on the board.

        Returns:
            list: Updated chess pieces and the position of the piece.
        """

        saved_game = list(self.params.saved_game)

        algebraic_position = self.get_piece_position.get_piece_position(saved_game)

        position_index = saved_game.index(self.piece_colored)
        target_cell_index = self.params.cell_name.index(self.params.move.move)

        piece_to_move = self._swap_pieces(target_cell_index, position_index, saved_game)

        return self.validate_move.validate_move(
            target_cell_index,
            piece_to_move,
            algebraic_position,
            saved_game,
        )
