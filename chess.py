from itertools import cycle

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from rich.style import Style
from rich.prompt import Prompt
from rich.console import Console


class GAME:
    def __init__(self, updated_chess_pieces) -> None:
        self.chess_pieces = [
            "br1", "bn1", "bb1", "bq", "bk", "bb2", "bn2", "br2",
            "bp1", "bp2", "bp3", "bp4", "bp5", "bp6", "bp7", "bp8",
            " ", " ", " ", " ", " ", " ", " ", " ",
            " ", " ", " ", " ", " ", " ", " ", " ",
            " ", " ", " ", " ", " ", " ", " ", " ",
            " ", " ", " ", " ", " ", " ", " ", " ",
            "wp1", "wp2", "wp3", "wp4", "wp5", "wp6", "wp7", "wp8",
            "wr1", "wn1", "wb1", "wq", "wk", "wb2", "wn2", "wr2",
        ]
        self.cell_name = [
                "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
                "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
                "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
                "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
                "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
                "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
                "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
                "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
        ]
        self.updated_chess_pieces = updated_chess_pieces

    def create_board(self):
        console = Console()

        light_color_square = "#FFFFE8"
        dark_color_square = "#557A46"

        # Create a table
        t = Table(show_header=False, show_lines=True, show_edge=True)
        initial_chessboard = set(self.chess_pieces)

        for i in range(8):
            for j in range(8):
                if self.updated_chess_pieces is not None:
                    if initial_chessboard != self.updated_chess_pieces:
                        self.chess_pieces = self.updated_chess_pieces

                piece = self.chess_pieces[i * 8 + j].upper()
                if piece.startswith("W"):
                    piece = piece.removeprefix("W")
                    cell_content = f"[#A8A196]{piece.center(2)}"
                elif piece.startswith("B"):
                    piece = piece.removeprefix("B")
                    cell_content = f"[#000000]{piece.center(2)}"
                else:
                    cell_content = f"{piece.center(2)}"

                cell_style = Style(
                    bgcolor=light_color_square
                    if (i + j) % 2 == 0
                    else dark_color_square
                )
                console.print(cell_content, style=cell_style, end="")
            console.print()

        console.print(t)


class PIECE:
    def __init__(self, white, black, playing, piece_moved, move) -> None:
        self.player_white = white
        self.player_black = black
        self.playing = playing
        self.chess_pieces = GAME(None).chess_pieces
        self.cell_name = GAME(None).cell_name
        self.piece_moved = piece_moved
        self.move = move
        self.square = None

    def move_piece(self):
        validation = {
            "k": KING(self.player_white, self.player_black, self.playing, self.piece_moved, self.move),
            "q": QUEEN(self.player_white, self.player_black, self.playing, self.piece_moved, self.move),
            "r": ROOK(self.player_white, self.player_black, self.playing, self.piece_moved, self.move),
            "b": BISHOP(self.player_white, self.player_black, self.playing, self.piece_moved, self.move),
            "n": KNIGHT(self.player_white, self.player_black, self.playing, self.piece_moved, self.move),
            "p": PAWN(self.player_white, self.player_black, self.playing, self.piece_moved, self.move),
        }

        piece = validation.get(self.piece_moved)

        if piece:
            piece.validate_move()
        else:
            print("Invalid piece!")

        players_piece = (
            f"w{self.piece_moved}" if self.playing == self.player_white else f"b{self.piece_moved}"
        )

        for position, piece in enumerate(self.chess_pieces):

            if players_piece == piece:
                self.position = self.cell_name[position]

                for square, move in enumerate(self.cell_name):
                    self.square = square
                    if self.move == move:
                        self.chess_pieces.pop(position)
                        piece_moved = self.chess_pieces.pop(square)
                        self.chess_pieces.insert(self.square, players_piece)
                        self.chess_pieces.insert(position, piece_moved)

        return self.chess_pieces

    def validate_move(self):
        pass


class KING(PIECE):
    def __init__(self, white, black, playing, piece_moved, move) -> None:
        super().__init__(white, black, playing, piece_moved, move)

    def validate_move(self):
        print("this is king's move validation")


class QUEEN(PIECE):
    def __init__(self, white, black, player, piece_moved, move) -> None:
        super().__init__(white, black, player, piece_moved, move)

    def validate_move(self):
        print("this is queen's move validation")


class ROOK(PIECE):
    def __init__(self, white, black, player, piece_moved, move) -> None:
        super().__init__(white, black, player, piece_moved, move)

    def validate_move(self):
        ...


class BISHOP(PIECE):
    def __init__(self, white, black, player, piece_moved, move) -> None:
        super().__init__(white, black, player, piece_moved, move)

    def validate_move(self):
        ...


class KNIGHT(PIECE):
    def __init__(self, white, black, player, piece_moved, move) -> None:
        super().__init__(white, black, player, piece_moved, move)

    def validate_move(self):
        ...


class PAWN(PIECE):
    def __init__(self, white, black, player, piece_moved, move) -> None:
        super().__init__(white, black, player, piece_moved, move)

    def validate_move(self):
        ...


def main():

    panel = Panel(Text("CHESS", style="#EEEDED on #557A46"), padding=1)
    print(Align(panel, "center"))

    white = Prompt.ask("Enter name [#EEEDED on #557A46]Player01", default="white")
    black = Prompt.ask(
        "Enter name [#000000 on #557A46]Player02", default="black"
    )

    input("Press any key to Start...\n\n")

    game = GAME(None)
    game.create_board()

    player_cycle = cycle([white, black])

    for player in player_cycle:

        color = "[#EEEDED on #557A46]" if player == white else "[#000000 on #FFFFE8]"
        piece, move = (
            console.input(f"\n{color}Make a move: ")
            .strip()
            .casefold()
            .split(" ")
        )

        updated_piece = PIECE(white=white, black=black, playing=player, piece_moved=piece, move=move).move_piece()
        game.updated_chess_pieces = updated_piece
        game.create_board()


if __name__ == "__main__":
    console = Console()
    main()
