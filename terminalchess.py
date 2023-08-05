""" TerminalChess game """

# from enum import Enum
import itertools
from itertools import cycle

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from rich.style import Style
from rich.prompt import Prompt
from rich.console import Console


# class color(Enum):

#     pass


class Game:
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

    def __init__(self, updated_chess_pieces, move, previous_square) -> None:
        self.chess_pieces = [
            "br1",
            "bn1",
            "bb1",
            "bq",
            "bk",
            "bb2",
            "bn2",
            "br2",
            "bp1",
            "bp2",
            "bp3",
            "bp4",
            "bp5",
            "bp6",
            "bp7",
            "bp8",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            "wp1",
            "wp2",
            "wp3",
            "wp4",
            "wp5",
            "wp6",
            "wp7",
            "wp8",
            "wr1",
            "wn1",
            "wb1",
            "wq",
            "wk",
            "wb2",
            "wn2",
            "wr2",
        ]
        self.square_name = [
            "a8",
            "b8",
            "c8",
            "d8",
            "e8",
            "f8",
            "g8",
            "h8",
            "a7",
            "b7",
            "c7",
            "d7",
            "e7",
            "f7",
            "g7",
            "h7",
            "a6",
            "b6",
            "c6",
            "d6",
            "e6",
            "f6",
            "g6",
            "h6",
            "a5",
            "b5",
            "c5",
            "d5",
            "e5",
            "f5",
            "g5",
            "h5",
            "a4",
            "b4",
            "c4",
            "d4",
            "e4",
            "f4",
            "g4",
            "h4",
            "a3",
            "b3",
            "c3",
            "d3",
            "e3",
            "f3",
            "g3",
            "h3",
            "a2",
            "b2",
            "c2",
            "d2",
            "e2",
            "f2",
            "g2",
            "h2",
            "a1",
            "b1",
            "c1",
            "d1",
            "e1",
            "f1",
            "g1",
            "h1",
        ]
        self.updated_chess_pieces = updated_chess_pieces
        self.move = move
        self.previous_square = previous_square
        self.square_color = None
        self.console = Console()

    def set_piece_color(self, piece):
        """Sets the color of a chess piece.

        Args:
            piece (str): The chess piece.

        Returns:
            str: The formatted piece color.
        """

        if piece.startswith("W"):
            piece = piece.removeprefix("W")
            piece_color = f"[#BBB3A2]{piece.center(2)}"
        elif piece.startswith("B"):
            piece = piece.removeprefix("B")
            piece_color = f"[#000000]{piece.center(2)}"
        else:
            piece_color = f"{piece.center(2)}"
        return piece_color

    def highlight_move(self, i, j):
        """Highlights the move on the chessboard.

        Args:
            i (int): Row index.
            j (int): Column index.

        Returns:
            str: The background color for highlighting the move.
        """

        if (
            self.square_name[i * 8 + j] == self.move
            and self.updated_chess_pieces is not None
        ):
            return "#BBCB44"
        if self.square_name[i * 8 + j] == self.previous_square:
            return "#F5F67F"
        return None

    def set_board_color(self):
        """Sets the board color and prints the chessboard."""

        light_color_square = "#EEEED2"
        dark_color_square = "#779756"

        column_tag = list("87654321")

        if self.updated_chess_pieces is not None:
            if self.chess_pieces != self.updated_chess_pieces:
                self.chess_pieces = self.updated_chess_pieces

        for i in range(8):
            print(f"[#F6F4EB on #302E2A]{column_tag[i]} ", end="")
            for j in range(8):
                piece = self.chess_pieces[i * 8 + j].upper()

                if self.highlight_move(i, j):
                    self.square_color = Style(bgcolor=self.highlight_move(i, j))
                # sets board color
                elif (i + j) % 2 == 0:
                    self.square_color = Style(bgcolor=light_color_square)
                else:
                    self.square_color = Style(bgcolor=dark_color_square)

                console.print(
                    self.set_piece_color(piece=piece), style=self.square_color, end=""
                )
            console.print()

    def create_board(self):
        """Creates the Chessboard."""
        row_tag = list(" abcdefgh")
        chess_board = Table(show_header=False, show_lines=True, show_edge=True)

        for tag, _ in enumerate(row_tag):
            self.console.print(f"[#F6F4EB on #302E2A] {row_tag[tag]}", end="")
        print()

        self.set_board_color()
        console.print(chess_board)


class Player:
    """
    Represents a Chess Player.

    Attributes:
        white (str): Name of the white player.
        black (str): Name of the black player.
        playing (str): Name of the player who is currently playing.
    """

    def __init__(self, white, black, playing) -> None:
        self.player_white = white
        self.player_black = black
        self.playing = playing


class Move:
    """
    Represents a Chess Move.

    Attributes:
        piece_moved (str): The piece to be moved.
        move (str): The target square for the move.
    """

    def __init__(self, piece_moved, move) -> None:
        self.piece_moved = piece_moved
        self.move = move


class Parameters:
    """
    Takes parameters for Move validation.

    ... Existing docstring ...

    Attributes:
        move (str): The move.
        position (str): The position of the piece.
        replaced_piece (str): The piece that will be replaced.
        players_piece (str): The current player's piece.
        temp_chess_pieces (list): A temporary copy of chess pieces.
        square_name (list): The list of square names on the board.
    """

    def __init__(
        self,
        move,
        position,
        replaced_piece,
        players_piece,
        temp_chess_pieces,
        square_name,
    ) -> None:
        self.move = move
        self.position = position
        self.replaced_piece = replaced_piece
        self.players_piece = players_piece
        self.temp_chess_pieces = temp_chess_pieces
        self.square_name = square_name


class ValidationForAllPieces:
    """
    Validates moves for all pieces.

    Attributes:
        move (str): The move to be validated.
        position (str): The position of the moved piece.
        replaced_piece (str): The piece that will be replaced.
        players_piece (str): The current player's piece.
    """

    def __init__(self, parameters) -> None:
        self.parameters = parameters

    def check_for_same_color_piece(self):
        """Checks if the move involves replacing a piece of the same color
        (for every move).

        Returns:
            bool: True if the move is valid, False otherwise.
        """

        piece_color = "w" if self.parameters.players_piece.startswith("w") else "b"

        if (
            self.parameters.replaced_piece[0] == piece_color
            and self.parameters.move == self.parameters.position
        ):
            return False

    def check_for_occupied_squares(self, index: int):
        """Checks if the square is occupied or not
        (for each piece possible moves).

        Returns:
            bool: True if the move is valid, False otherwise.
        """

        square = self.parameters.square_name.index(index)
        check_piece_color = self.parameters.temp_chess_pieces[square][0]
        piece_color = "w" if self.parameters.players_piece.startswith("w") else "b"

        if piece_color == check_piece_color:
            return False


class Piece:
    """
    Represents a Chess Piece.

    Attributes:
        player (Player): The player owning the piece.
        move (Move): The move to be made.
        chess_pieces (list): The list of chess pieces on the board.
        cell_name (list): The list of square names on the board.
        position (str): The current position of the piece.
    """

    def __init__(self, player, move, chess_pieces, cell_name) -> None:
        self.player = player
        self.move = move
        self.chess_pieces = chess_pieces
        self.cell_name = cell_name
        self.position = None
        self.is_valid_move = None

    def determine_piece_color(self):
        """Determines the color of the current player's piece.

        Returns:
            str: The current player's piece.
        """

        players_piece = (
            f"w{self.move.piece_moved}"
            if self.player.playing == self.player.player_white
            else f"b{self.move.piece_moved}"
        )

        return players_piece

    def get_piece_position(self, temp_chess_pieces, players_piece):
        """Gets the current position of the piece.

        Args:
            temp_chess_pieces (list): A temporary copy of chess pieces.
            players_piece (str): The current player's piece.

        Returns:
            str: The current position of the piece.
        """

        position = self.cell_name[temp_chess_pieces.index(players_piece)]

        return position

    def validate_move(
        self, square, piece_moved, players_piece, position_of_piece, temp_chess_pieces
    ):
        """Validates the move made by the player.

        Args:
            square (int): The target square index.
            piece_moved (str): The piece to be moved.
            players_piece (str): The current player's piece.
            position_of_piece (str): The current position of the piece.
            temp_chess_pieces (list): A temporary copy of chess pieces.

        Returns:
            list: Updated chess pieces and the position of the piece.
        """
        parameters = Parameters(
            move=self.move.move,
            position=self.cell_name[square],
            replaced_piece=piece_moved,
            players_piece=players_piece,
            temp_chess_pieces=self.chess_pieces,
            square_name=self.cell_name,
        )

        validation_for_all_pieces = ValidationForAllPieces(parameters)

        validation_check_for_same_color_piece = (
            validation_for_all_pieces.check_for_same_color_piece()
        )

        if validation_check_for_same_color_piece is False:
            console.print(
                f"[#C51605]{self.move.piece_moved} can't move to {self.move.move}"
            )
            return [None, position_of_piece]

        piece_to_check = self.move.piece_moved[0]

        if piece_to_check == "k":
            valid_moves = King(
                validating_for_all_parameters=parameters,
                current_square=position_of_piece,
            ).get_valid_move()
        elif piece_to_check == "q":
            valid_moves = Queen(
                validating_for_all_parameters=parameters,
                current_square=position_of_piece,
            ).get_valid_move()
        elif piece_to_check == "r":
            valid_moves = Rook(
                validating_for_all_parameters=parameters,
                current_square=position_of_piece,
            ).get_valid_move()
        elif piece_to_check == "b":
            valid_moves = Bishop(
                validating_for_all_parameters=parameters,
                current_square=position_of_piece,
            ).get_valid_move()
        elif piece_to_check == "n":
            valid_moves = Knight(
                validating_for_all_parameters=parameters,
                current_square=position_of_piece,
            ).get_valid_move()
        elif piece_to_check == "p":
            valid_moves = Pawn(
                validating_for_all_parameters=parameters,
                current_square=position_of_piece,
                players_piece=players_piece,
            ).get_valid_move()
        else:
            valid_moves = []

        if self.move.move not in valid_moves:
            console.print(
                f"[#C51605]{self.move.piece_moved} can't move to {self.move.move}"
            )
            return [None, position_of_piece]

        return [temp_chess_pieces, position_of_piece]

    def move_piece(self):
        """Moves the chess piece on the board.

        Returns:
            list: Updated chess pieces and the position of the piece.
        """

        temp_chess_pieces = list(self.chess_pieces)

        players_piece = self.determine_piece_color()
        position_of_piece = self.get_piece_position(temp_chess_pieces, players_piece)

        position = temp_chess_pieces.index(players_piece)
        square = self.cell_name.index(self.move.move)

        piece_moved = temp_chess_pieces.pop(square)
        temp_chess_pieces.insert(square, players_piece)
        temp_chess_pieces.pop(position)
        temp_chess_pieces.insert(position, piece_moved)

        return self.validate_move(
            square,
            piece_moved,
            players_piece,
            position_of_piece,
            temp_chess_pieces,
        )

    def check_valid_move(self):
        """Checks if the move made is valid"""


#!
class King:
    """
    Represents a Chess King.

    Attributes:
        current_square (str): The current square of the King.
    """

    def __init__(self, validating_for_all_parameters, current_square) -> None:
        self.parameter = validating_for_all_parameters
        self.current_square = current_square

    def get_valid_move(self):
        """Checks if the move made by the player is valid for the King."""

        columns = list("87654321")
        rows = list("abcdefgh")

        row_index = rows.index(self.current_square[0])
        column_index = columns.index(self.current_square[1])

        row_offsets = [-1, 0, 1]
        column_offsets = [-1, 0, 1]

        # Generate all possible combinations of row and column offsets
        possible_moves = [
            rows[row_index + row_offset] + columns[column_index + column_offset]
            for row_offset, column_offset in itertools.product(
                row_offsets, column_offsets
            )
            if 0 <= row_index + row_offset < len(rows)
            and 0 <= column_index + column_offset < len(columns)
            and (row_offset, column_offset) != (0, 0)
        ]

        return possible_moves


class Queen:
    """
    Represents a Chess Queen.

    Attributes:
        current_square (str): The current square of the Queen.
    """

    def __init__(self, validating_for_all_parameters, current_square) -> None:
        self.parameter = validating_for_all_parameters
        self.current_square = current_square

    def get_valid_move(self):
        """Checks if the move made by the player is valid for the Queen."""

        columns = list("87654321")
        rows = list("abcdefgh")

        row_index = rows.index(self.current_square[0])
        column_index = columns.index(self.current_square[1])

        queen_moves = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),  # Horizontal and Vertical moves
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),  # Diagonal moves
        ]

        possible_moves = []
        for row_offset, column_offset in queen_moves:
            row, col = row_index, column_index
            while True:
                row += row_offset
                col += column_offset
                if 0 <= row < len(rows) and 0 <= col < len(columns):

                    if (
                        ValidationForAllPieces(
                            parameters=self.parameter
                        ).check_for_occupied_squares(rows[row] + columns[col])
                        is not False
                    ):
                        possible_moves.append(rows[row] + columns[col])
                else:
                    break

        return possible_moves


class Rook:
    """
    Represents a Chess Rook.

    Attributes:
        current_square (str): The current square of the Rook.
    """

    def __init__(self, validating_for_all_parameters, current_square) -> None:
        self.parameter = validating_for_all_parameters
        self.current_square = current_square

    def get_valid_move(self):
        """Checks if the move made by the player is valid for the Rook."""

        columns = list("87654321")
        rows = list("abcdefgh")

        row_index = rows.index(self.current_square[0])
        column_index = columns.index(self.current_square[1])

        rook_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Horizontal and Vertical moves

        possible_moves = []
        for row_offset, column_offset in rook_moves:
            row, col = row_index, column_index
            while True:
                row += row_offset
                col += column_offset
                if 0 <= row < len(rows) and 0 <= col < len(columns):
                    if (
                        ValidationForAllPieces(
                            parameters=self.parameter
                        ).check_for_occupied_squares(rows[row] + columns[col])
                        is not False
                    ):
                        possible_moves.append(rows[row] + columns[col])
                else:
                    break

        return possible_moves


class Bishop:
    """
    Represents a Chess Bishop.

    Attributes:
        current_square (str): The current square of the Bishop.
    """

    def __init__(self, validating_for_all_parameters, current_square) -> None:
        self.parameter = validating_for_all_parameters
        self.current_square = current_square

    def get_valid_move(self):
        """Checks if the move made by the player is valid for the Bishop."""

        columns = list("87654321")
        rows = list("abcdefgh")

        row_index = rows.index(self.current_square[0])
        column_index = columns.index(self.current_square[1])

        bishop_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonal moves

        possible_moves = []
        for row_offset, column_offset in bishop_moves:
            row, col = row_index, column_index
            while True:
                row += row_offset
                col += column_offset
                if 0 <= row < len(rows) and 0 <= col < len(columns):
                    if (
                        ValidationForAllPieces(
                            parameters=self.parameter
                        ).check_for_occupied_squares(rows[row] + columns[col])
                        is not False
                    ):
                        possible_moves.append(rows[row] + columns[col])
                else:
                    break

        return possible_moves


#!
class Knight:
    """
    Represents a Chess Knight.

    Attributes:
        current_square (str): The current square of the Knight.
    """

    def __init__(self, validating_for_all_parameters, current_square) -> None:
        self.parameter = validating_for_all_parameters
        self.current_square = current_square

    def get_valid_move(self):
        """Checks if the move made by the player is valid for the Knight."""

        columns = list("87654321")
        rows = list("abcdefgh")

        row_index = rows.index(self.current_square[0])
        column_index = columns.index(self.current_square[1])

        knight_moves = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]

        possible_moves = [
            rows[row_index + row_offset] + columns[column_index + column_offset]
            for row_offset, column_offset in knight_moves
            if 0 <= row_index + row_offset < len(rows)
            and 0 <= column_index + column_offset < len(columns)
        ]

        return possible_moves


class Pawn:
    """
    Represents a Chess Pawn.

    Attributes:
        current_square (str): The current square of the Pawn.
    """

    def __init__(
        self, validating_for_all_parameters, current_square, players_piece
    ) -> None:
        self.parameter = validating_for_all_parameters
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

        if (
            ValidationForAllPieces(
                parameters=self.parameter
            ).check_for_occupied_squares(rows[row_index] + columns[column_index + opt])
            is not False
        ):
            if column_index in (1, 6):
                moves = [
                    rows[row_index] + columns[column_index + opt],
                    rows[row_index] + columns[column_index + 2 * opt],
                ]
                possible_moves.extend(moves)
            else:
                possible_moves.append(rows[row_index] + columns[column_index + opt])

        return possible_moves


def main():

    panel = Panel(Text("CHESS", style="#EEEDED on #557A46"), padding=1)
    print(Align(panel, "center"))

    white = Prompt.ask("[#F6F4EB on #302E2A]Enter name", default="white")
    black = Prompt.ask("[#F6F4EB on #302E2A]Enter name", default="black")

    input("Press enter to Start...\n\n")

    game = Game(None, None, None)
    game.create_board()

    player_cycle = cycle([white, black])

    for player in player_cycle:
        color = "[#EEEDED on #557A46]" if player == white else "[#000000 on #FFFFE8]"
        while True:
            piece, move = (
                console.input(f"\n{color}Make a move: ").strip().casefold().split(" ")
            )

            updated_piece = Piece(
                Player(white, black, player),
                Move(piece, move),
                chess_pieces=game.chess_pieces,
                cell_name=game.square_name,
            ).move_piece()

            if updated_piece[0] is not None:
                game.updated_chess_pieces = updated_piece[0]
                game.previous_square = updated_piece[1]
                game.move = move
                game.create_board()
                break


if __name__ == "__main__":
    console = Console()
    main()
