from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich import print
from highlight_moves import HighlightMove
from .place_pieces import PlacePiece


class CreateBoard:
    """
    Represents a Chess Game.

    Attributes:
        updated_chess_pieces (list): The updated list of chess pieces on the board.
        move (str): The move made by the player.
        previous_square (str): The previous square of the moved piece.
        chess_pieces (list): The initial list of chess pieces on the board.
        square_name (list): The list of square names on the board.
        square_color (Style): The style for square color in the console.
        console (Console): The rich.Console object for printing the board.

    Methods:
        set_piece_color: Sets the color of a chess piece.
        highlight_move: Highlights the move on the chessboard.
        set_board_color: Sets the board color and prints the chessboard.
        create_board: Creates the Chessboard.
    """

    def __init__(self, updated_game, move, previous_square, player) -> None:
        # self.color = SetColor(updated_game, move, previous_square, player)
        self.console = Console()
        self.piece = PlacePiece()
        self.highlight_move = HighlightMove(move, previous_square)
        self.square_color = None
        self.updated_game = updated_game
        self.player = player

    def _check_if_game_updated(self):
        if self.updated_game is not None:
            if self.piece.game != self.updated_game:
                self.piece.game = self.updated_game

    def set_piece_color(self, piece):
        """Sets the color of a chess piece.

        Args:
            piece (str): The chess piece.

        Returns:
            str: The formatted piece color.
        """
        if piece.startswith("W"):
            piece = piece.removeprefix("W")
            piece_colored = f"[#BBB3A2]{piece.center(2)}"
        elif piece.startswith("B"):
            piece = piece.removeprefix("B")
            piece_colored = f"[#000000]{piece.center(2)}"
        else:
            piece_colored = f"{piece.center(2)}"
        return piece_colored

    def set_board_color(self):
        """Sets the board color and prints the chessboard."""

        light_color_square = "#EEEED2"
        dark_color_square = "#779756"

        column_tag = list("87654321")

        self._check_if_game_updated()

        for i in range(8):
            print(f"[#F6F4EB on #302E2A]{column_tag[i]} ", end="")
            for j in range(8):
                piece = self.piece.game[i * 8 + j].upper()

                if self.highlight_move.highlight_move(i, j):
                    self.square_color = Style(bgcolor=self.highlight_move.highlight_move(i, j))
                # sets board color
                elif (i + j) % 2 == 0:
                    self.square_color = Style(bgcolor=light_color_square)
                else:
                    self.square_color = Style(bgcolor=dark_color_square)

                self.console.print(
                    self.set_piece_color(piece=piece), style=self.square_color, end=""
                )
            self.console.print()

        self.console.print(
            f"[#EEEDED on #557A46]{self.player.player_white.capitalize()}"
        )


    def create_board(self):
        """Creates the Chessboard."""
        row_tag = list(" abcdefgh")
        chess_board = Table(show_header=False, show_lines=True, show_edge=True)

        self.console.print(
            f"[#000000 on #FFFFE8]{self.player.player_black.capitalize()}"
        )

        for tag, _ in enumerate(row_tag):
            self.console.print(f"[#F6F4EB on #302E2A] {row_tag[tag]}", end="")
        print()

        self.set_board_color()
        self.console.print(chess_board)
