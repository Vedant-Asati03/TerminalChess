from enum import Enum
from rich.console import Console

from pieces.king import King
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.pawn import Pawn
from restricted_invalid_moves import RestrictedInvalidMoves
from determine_piece_color import DeterminePieceColor


class Piece(Enum):
    KING = "k"
    QUEEN = "q"
    ROOK = "r"
    BISHOP = "b"
    KNIGHT = "n"
    PAWN = "p"


class ValidateMove:
    """
    Represents a Chess Piece.

    Attributes:
        player (Player): The player owning the piece.
        move (Move): The move to be made.
        chess_pieces (list): The list of chess pieces on the board.
        cell_name (list): The list of square names on the board.
        position (str): The current position of the piece.
    """

    def __init__(self, params) -> None:
        self.position = None
        self.is_valid_move = None
        self.params = params
        self.console = Console()

        self.piece_colored = DeterminePieceColor(self.params).determine_piece_color()

    def _show_piece_cannot_move_message(self):
        self.console.print(
            f"[#C51605]{self.params.move.piece_moved} can't move to {self.params.move.move}"
        )

    def _is_same_color_piece(self, restricted_moves, target_cell_index, replaced_piece):
        return restricted_moves.check_for_same_color_piece(
            target_cell_index, replaced_piece
        )

    def _is_jumping_over_pieces(self, restricted_moves, algebraic_position):
        return restricted_moves.jumping_over_pieces(current_position=algebraic_position)

    def get_piece_moves(self, algebraic_position):
        piece_to_check = self.params.move.piece_moved[0]

        match piece_to_check:
            case Piece.KING.value:
                valid_moves = King(algebraic_position).get_valid_move()
            case Piece.QUEEN.value:
                valid_moves = Queen(algebraic_position).get_valid_move()
            case Piece.ROOK.value:
                valid_moves = Rook(algebraic_position).get_valid_move()
            case Piece.BISHOP.value:
                valid_moves = Bishop(algebraic_position).get_valid_move()
            case Piece.KNIGHT.value:
                valid_moves = Knight(algebraic_position).get_valid_move()
            case Piece.PAWN.value:
                valid_moves = Pawn(
                    algebraic_position, self.piece_colored
                ).get_valid_move()
            case _:
                valid_moves = []

        return valid_moves

    def validate_move(
        self, target_cell_index, replaced_piece, algebraic_position, saved_game
    ):
        """Validates the move made by the player.

        Args:
            target_cell_index (int): The target square index.
            piece_moved (str): The piece to be moved.
            piece_colored (str): The current player's piece.
            algebraic_position (str): The current position of the piece.
            saved_game (list): A temporary copy of chess pieces.

        Returns:
            list: Updated chess pieces and the position of the piece.
        """
        restricted_moves = RestrictedInvalidMoves(self.params)

        if self._is_same_color_piece(
            restricted_moves, target_cell_index, replaced_piece
        ):
            self._show_piece_cannot_move_message()
            return [None, algebraic_position]

        if self._is_jumping_over_pieces(restricted_moves, algebraic_position):
            self._show_piece_cannot_move_message()
            return [None, algebraic_position]

        valid_moves = self.get_piece_moves(algebraic_position)

        if self.params.move.move not in valid_moves:
            self._show_piece_cannot_move_message()
            return [None, algebraic_position]

        return [saved_game, algebraic_position]
