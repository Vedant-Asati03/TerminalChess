""" TerminalChess game """

from itertools import cycle

from rich import print
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt
from rich.console import Console
# from prompt_toolkit import prompt
# from prompt_toolkit.validation import Validator

from create_board.create_board import CreateBoard
from highlight_moves import GenerateAlgebraicNotation
from move_piece.params import Params
from move_piece.move_piece import MovePiece
# from display_valid_moves import DisplayValidMoves


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


def main():
    console = Console()
    panel = Panel(Text("CHESS", style="#EEEDED on #557A46"), padding=1)
    print(Align(panel, "center"))

    white = Prompt.ask("[#F6F4EB on #302E2A]Enter name", default="white")
    black = Prompt.ask("[#F6F4EB on #302E2A]Enter name", default="black")

    input("Press enter to Start...\n\n")

    player_cycle = cycle([white, black])

    game = CreateBoard(None, None, None, Player(white, black, None))
    game.create_board()

    for player in player_cycle:
        color = "[#EEEDED on #557A46]" if player == white else "[#000000 on #FFFFE8]"
        while True:
            piece, move = (
                console.input(f"\n{color}Make a move: ").strip().casefold().split(" ")
            )

            # validator = Validator.from_callable(
            #     DisplayValidMoves(
            #         Params(
            #             Player(white, black, player),
            #             Move(None, None),
            #             saved_game=game.piece.game,
            #             cell_name=GenerateAlgebraicNotation().square_algebraic_notation,
            #         )
            #     )._check_if_piece()
            # )

            # piece, move = (
            #     prompt(console.print(f"\n{color}Make a move: "), validator=validator)
            #     .strip()
            #     .casefold()
            #     .split(" ")
            # )

            params = Params(
                Player(white, black, player),
                Move(piece, move),
                saved_game=game.piece.game,
                cell_name=GenerateAlgebraicNotation().square_algebraic_notation,
            )

            updated_piece = MovePiece(params).move_piece()

            if updated_piece[0] is not None:
                game.updated_game = updated_piece[0]
                game.previous_square = updated_piece[1]
                game.move = move
                game.player = Player(white, black, player)
                game.create_board()
                break


if __name__ == "__main__":
    main()
