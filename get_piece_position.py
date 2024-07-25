from determine_piece_color import DeterminePieceColor


class GetPiecePosition:

    def __init__(self, params) -> None:
        self.params = params
        self.piece_colored = DeterminePieceColor(self.params).determine_piece_color()

    def get_piece_position(self, saved_game):
        """Gets the current position of the piece.

        Args:
            temp_chess_pieces (list): A temporary copy of chess pieces.
            players_piece (str): The current player's piece.

        Returns:
            str: The current position of the piece.
        """

        position = self.params.cell_name[saved_game.index(self.piece_colored)]

        return position
