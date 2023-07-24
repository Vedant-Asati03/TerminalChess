from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.console import Console


chess_pieces = [
    "bR1", "bN1", "bB1", "bQ", "bK", "bB2", "bN2", "bR2",
    "bP1", "bP2", "bP3", "bP4", "bP5", "bP6", "bP7", "bP8",
    " ", " ", " ", " ", " ", " ", " ", " ",
    " ", " ", " ", " ", " ", " ", " ", " ",
    " ", " ", " ", " ", " ", " ", " ", " ",
    " ", " ", " ", " ", " ", " ", " ", " ",
    "wP1", "wP2", "wP3", "wP4", "wP5", "wP6", "wP7", "wP8",
    "wR1", "wN1", "wB1", "wQ", "wK", "wB2", "wN2", "wR2",
]

squares = [
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
]


class GAME:
    def __init__(self, chess_board) -> None:
        self.board_size = 8
        self.chess_board = chess_board

    def layout(self):
        console = Console()

        for i in range(0, self.board_size**2, self.board_size):
            for j in range(self.board_size):
                square_index = j + i
                square = squares[square_index]
                piece = self.chess_board[square_index]

                if (i // self.board_size + j) % 2 == 0:

                    if piece.startswith("w"):
                        piece = piece.removeprefix("w")
                        console.print(
                            f"[#A8A196 on #FFFFE8]{piece.center(2)}[/]", end=""
                        )
                    elif piece.startswith("b"):
                        piece = piece.removeprefix("b")
                        console.print(
                            f"[#000000 on #FFFFE8]{piece.center(2)}[/]", end=""
                        )
                    else:
                        console.print(
                            f"[#000000 on #FFFFE8]{piece.center(2)}[/]", end=""
                        )

                else:
                    if piece.startswith("w"):
                        piece = piece.removeprefix("w")
                        console.print(
                            f"[#A8A196 on #557A46]{piece.center(2)}[/]", end=""
                        )
                    elif piece.startswith("b"):
                        piece = piece.removeprefix("b")
                        console.print(
                            f"[#000000 on #557A46]{piece.center(2)}[/]", end=""
                        )
                    else:
                        console.print(
                            f"[#000000 on #557A46]{piece.center(2)}[/]", end=""
                        )

            console.print()


class PIECE:
    def __init__(self, piece_to_move, move) -> None:
        self.piece_to_move = piece_to_move
        self.move = move
        self.square = None

    def move_piece(self):
        for position, piece in enumerate(chess_pieces):

            if self.piece_to_move == piece:
                self.position = squares[position]

                for square, move in enumerate(squares):
                    self.square = square
                    if self.move == move:
                        chess_pieces.pop(position)
                        piece_moved = chess_pieces.pop(square)
                        chess_pieces.insert(self.square, self.piece_to_move)
                        chess_pieces.insert(position, piece_moved)

        return chess_pieces

    def pass_to_validate_move(self):
        match self.piece_to_move:

            case "bK" | "wK":
                KING(self.move).validate_move()

            case "bQ" | "wQ":
                QUEEN(self.move).validate_move()

            case "bR1" | "bR2" | "wR1" | "wR2":
                ROOK(self.move).validate_move()

            case "bB1" | "bB2" | "wB1" | "wB2":
                BISHOP(self.move).validate_move()

            case "bN1" | "bN2" | "wN1" | "wN2":
                KNIGHT(self.move).validate_move()

            case "bP1" | "bP2" | "bP3" | "bP4" | "bP5" | "bP6" | "bP7" | "bP8" | "wP1" | "wP2" | "wP3" | "wP4" | "wP5" | "wP6" | "wP7" | "wP8":
                PAWN(self.move).validate_move()

    def validate_move(self):

        pass


class KING(PIECE):
    def __init__(self, move) -> None:
        super().__init__(move)

    def validate_move(self):
        ...


class QUEEN(PIECE):
    def __init__(self, move) -> None:
        super().__init__(move)

    def validate_move(self):
        ...


class ROOK(PIECE):
    def __init__(self, move) -> None:
        super().__init__(move)

    def validate_move(self):
        ...


class BISHOP(PIECE):
    def __init__(self, move) -> None:
        super().__init__(move)

    def validate_move(self):
        ...

class KNIGHT(PIECE):
    def __init__(self, move) -> None:
        super().__init__(move)

    def validate_move(self):
        ...


class PAWN(PIECE):
    def __init__(self, move) -> None:
        super().__init__(move)

    def validate_move(self):
        ...

def main():
    panel = Panel(Text("CHESS", style="#EEEDED on #557A46"), padding=1)
    print(Align(panel, "center"))

    piece, move = input("Make a move: ").split(" ")

    GAME(PIECE(piece_to_move=piece, move=move).move_piece()).layout()


if __name__ == "__main__":
    main()
