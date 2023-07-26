import json
import logging
import random
import time
from dataclasses import asdict, dataclass
from datetime import date, datetime
from enum import UNIQUE, Enum, StrEnum, auto, verify
from itertools import cycle
from pathlib import Path
from threading import Thread
from typing import Optional

from rich import print
from rich.align import Align
from rich.console import Console
from rich.emoji import Emoji
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.style import Style
from rich.table import Table
from rich.text import Text

# emoji constants
TADA_EMOJI = ":tada:"
PENSIVE_FACE_EMOJI = ":pensive_face:"
VICTORY_HAND_EMOJI = ":victory_hand:"
QUESTION_MARK_EMOJI = ":white_question_mark:"
BLUE_CIRCLE_EMOJI = ":blue_circle:"
CROSS_MARK_EMOJI = ":cross_mark:"


@verify(UNIQUE)
class Cell(Enum):
    EMPTY = 0
    COMPUTER = 1
    PLAYER = 2


@verify(UNIQUE)
class Difficulty(StrEnum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()


class GameplayError(Exception):
    """
    Raised when there's an internal logic error in game.
    """


@dataclass(frozen=True, order=True)
class CheckWinResult:
    """
    Represents a result returned by `TicTacToe().check_win`.
    """

    victory: bool
    winner: Optional[str] = None
    coordinates: list[tuple[int, int]] = None


@dataclass(frozen=True, order=True)
class Move:
    """
    Represents a move on the board.
    """

    pos: int
    marker: str


@dataclass(frozen=True, order=True)
class RecordingData:
    """
    RecordingData represents the recording of a tic tac toe game.
    """

    grid_size: int
    moves: list[Move]
    vs: str
    winner: str
    when: str


LOG_FILE_LOCATION = ""


class TicTacToe:
    """
    Gameplay class.

    as per the Cell enum defined above
    0 -> empty
    1 -> filled by computer
    2 -> filled by player
    """

    def __init__(self, difficulty: Difficulty, grid_size: int) -> None:
        """
        Constructs the game.
        """
        self.difficulty = difficulty
        self.grid_size = grid_size
        self.board = self.create_board()

        self.position_to_coordinates = {}
        for pos in range(1, (self.grid_size**2) + 1):
            floor = pos // grid_size
            actual = pos / grid_size

            row = floor
            if floor == actual:
                row -= 1

            rem = pos % grid_size
            col = rem - 1
            if rem == 0:
                col = grid_size - 1

            self.position_to_coordinates[pos] = (row, col)

        self.coordinates_to_position = {
            v: k for k, v in self.position_to_coordinates.items()
        }

        # keep a record of moves for recordings
        self.moves: list[Move] = []

        self.app_dir = self.init_dirs()

        today = date.today().strftime("%d-%m-%y")
        global LOG_FILE_LOCATION
        LOG_FILE_LOCATION = Path.home() / ".tictactoe" / "logs" / f"{today}.log"
        logging.basicConfig(
            filename=str(LOG_FILE_LOCATION),
            filemode="a",
            level=logging.DEBUG,
            format="%(asctime)s %(name)s %(levelname)s: %(message)s",
            datefmt="%H:%M:%S",
        )

        t = Thread(target=self.purge_logs, name="log purger", daemon=False)
        t.start()

    @staticmethod
    def init_dirs() -> Path:
        """
        Makes required directories and returns the app_dir.
        """
        app_dir = Path.home() / ".tictactoe"
        app_dir.mkdir(exist_ok=True)

        logs_dir = app_dir / "logs"
        logs_dir.mkdir(exist_ok=True)

        recordings_dir = app_dir / "recordings"
        recordings_dir.mkdir(exist_ok=True)

        return app_dir

    def purge_logs(self, limit: int = 30):
        """
        Purges logs older than `limit` days.
        """
        app_dir = self.app_dir
        logs_dir = app_dir / "logs"
        days_to_seconds = limit * 24 * 60 * 60
        for file in logs_dir.iterdir():
            conditions = (
                file.is_file(),
                file.name.endswith(".log"),
                (time.time() - file.stat().st_mtime)
                > days_to_seconds,  # file older than limit days
            )
            if all(conditions):
                file.unlink()

    def create_board(self) -> list[list[Cell]]:
        """
        Creates the initial board.
        """
        board = []
        for _ in range(self.grid_size):
            board.append([Cell.EMPTY for _ in range(self.grid_size)])

        return board

    def get_board_row(self, row_number: int) -> list[Cell]:
        """
        Returns the given row number from the board.
        Requested row number must be between 1 and self.grid_size inclusive.
        """
        if row_number not in range(1, self.grid_size + 1):
            raise GameplayError(
                f"Requested get_board_row({row_number}) which is out of bounds. 1 <= row_number <= {self.grid_size}."
            )

        row_number -= 1
        return self.board[row_number]

    def get_board_column(self, col_number: int) -> list[Cell]:
        """
        Returns the given column number from the board.
        Requested column number must be between 1 and 3 inclusive.
        """
        if col_number not in range(1, self.grid_size + 1):
            raise GameplayError(
                f"Requested get_board_column({col_number}) which is out of bounds. 1 <= col_number <= {self.grid_size}."
            )

        col_number -= 1
        board = self.board
        return [board[nrow][col_number] for nrow in range(0, self.grid_size)]

    def get_board_diagonal(self, diagonal_number: int) -> list[Cell]:
        """
        Returns the given diagonal number from the board.
        diagonal_number must be 1 for left to right diagonal and -1 for right to left diagonal.
        """
        if diagonal_number == 1:
            board = self.board
            length = len(board)
            return [board[i][i] for i in range(length)]

        elif diagonal_number == -1:
            board = self.board
            length = len(board)
            return [board[i][length - i - 1] for i in range(length)]

        else:
            raise GameplayError(
                f"Requested get_board_diagonal({diagonal_number}) which is out of bounds. Diagonal number belongs to {{-1, 1}}."
            )

    def get_empty_cells(self) -> list[tuple[int, int]]:
        """
        Returns list of coordinates of the board where cells are empty.
        """
        available = []
        for nrow, row in enumerate(self.board):
            for ncol, col in enumerate(row):
                if col == Cell.EMPTY:
                    available.append((nrow, ncol))

        if len(available) == 0:
            raise GameplayError(
                "no empty cells in the board to fill. game should be over by now"
            )

        return available

    def get_corner_cells(self) -> list[tuple[int, int]]:
        """
        Returns a list of coordinates of the corner cells.
        """
        grid_size = self.grid_size - 1
        return [(0, 0), (0, grid_size), (grid_size, 0), (grid_size, grid_size)]

    def set_mark_by_coordinates(self, coordinates: tuple[int, int], mark: Cell) -> None:
        """
        Sets a mark on the game board and does a couple of checks. Appends the move (if applicable) to self.moves too.

        Raises `GameplayError` if the checks fail.
        """
        if mark == Cell.EMPTY:
            raise GameplayError(
                f"request for setting empty mark on coordinates {coordinates}"
            )

        row, col = coordinates
        bounds = range(0, self.grid_size)
        if row not in bounds or col not in bounds:
            raise GameplayError(f"either {row=} or {col=} is not in bounds")

        if self.board[row][col] != Cell.EMPTY:
            raise GameplayError(
                f"attempt to overwrite cell value with {mark=} on {coordinates=}"
            )

        if len(self.moves) != 0:
            last_move = self.moves[-1]
            if last_move.marker == mark:
                raise GameplayError(
                    f"consecutive request to set {mark=} at {coordinates=}. last request was at coordinates={self.position_to_coordinates[last_move.pos]}"
                )

        self.board[row][col] = mark
        self.moves.append(Move(self.coordinates_to_position[coordinates], mark.name))

    def set_mark_by_position(self, pos: int, mark: Cell) -> None:
        """
        Wrapper for self.set_mark_by_coordinates.
        """
        self.set_mark_by_coordinates(self.position_to_coordinates[pos], mark)

    def fill_player_cell(self, position: int) -> None:
        """
        Fills the board with Cell.Player at the given position.

        Position ranges from 1 to self.grid_size. Raises an error otherwise.

        Returns True if the entered position can be filled.
        """
        self.set_mark_by_position(position, Cell.PLAYER)

    def _fill_computer_cell_easy(self) -> tuple[int, int]:
        logging.debug("filling computer cell easy")
        # choose random empty cell
        available = self.get_empty_cells()
        choice = random.choice(available)
        self.set_mark_by_coordinates(choice, Cell.COMPUTER)
        return choice

    def _fill_computer_cell_medium(self, hard: bool = False) -> tuple[int, int]:
        for i in range(2):
            # check for ways to win first, and then preventing the player
            for nrow in range(1, self.grid_size + 1):
                row = self.get_board_row(nrow)
                conditions = [
                    # winning
                    row.count(Cell.COMPUTER) > (self.grid_size - 2)
                    and row.count(Cell.PLAYER) == 0,
                    # preventing
                    (
                        row.count(Cell.PLAYER) > (self.grid_size - 2)
                        and row.count(Cell.EMPTY) != 0
                    ),
                ]
                if conditions[i]:  # first check all winning conditions, then preventing
                    ncol = row.index(Cell.EMPTY)
                    self.set_mark_by_coordinates((nrow - 1, ncol), Cell.COMPUTER)
                    if i == 0:
                        logging.debug(
                            f"filling pos {self.coordinates_to_position[(nrow-1, ncol)]} to offend"
                        )
                    else:
                        logging.debug(
                            f"filling pos {self.coordinates_to_position[(nrow-1, ncol)]} to defend"
                        )
                    return (nrow - 1, ncol)

            for ncol in range(1, self.grid_size + 1):
                col = self.get_board_column(ncol)
                conditions = [
                    col.count(Cell.COMPUTER) > (self.grid_size - 2)
                    and col.count(Cell.PLAYER) == 0,
                    col.count(Cell.PLAYER) > (self.grid_size - 2)
                    and col.count(Cell.EMPTY) != 0,
                ]
                if conditions[i]:
                    nrow = col.index(Cell.EMPTY)
                    self.set_mark_by_coordinates((nrow, ncol - 1), Cell.COMPUTER)
                    if i == 0:
                        logging.debug(
                            f"filling pos {self.coordinates_to_position[(nrow, ncol-1)]} to offend"
                        )
                    else:
                        logging.debug(
                            f"filling pos {self.coordinates_to_position[(nrow, ncol-1)]} to defend"
                        )
                    return (nrow, ncol - 1)

            for ndiag in range(-1, 2, 2):
                diag = self.get_board_diagonal(ndiag)
                conditions = [
                    diag.count(Cell.COMPUTER) > (self.grid_size - 2)
                    and diag.count(Cell.PLAYER) == 0,
                    diag.count(Cell.PLAYER) > (self.grid_size - 2)
                    and diag.count(Cell.EMPTY) != 0,
                ]
                if conditions[i]:
                    if ndiag == 1:
                        # nrow and ncol equal in this case, i.e., (0, 0), (1, 1), (2, 2)
                        nrow = diag.index(Cell.EMPTY)
                        self.set_mark_by_coordinates((nrow, nrow), Cell.COMPUTER)
                        if i == 0:
                            logging.debug(
                                f"filling pos {self.coordinates_to_position[(nrow, nrow)]} to offend"
                            )
                        else:
                            logging.debug(
                                f"filling pos {self.coordinates_to_position[(nrow, nrow)]} to defend"
                            )
                        return (nrow, nrow)
                    else:
                        # (nrow, matrix_size-nrow-1)
                        nrow = diag.index(Cell.EMPTY)
                        self.set_mark_by_coordinates(
                            (nrow, self.grid_size - nrow - 1), Cell.COMPUTER
                        )
                        if i == 0:
                            logging.debug(
                                f"filling pos {self.coordinates_to_position[(nrow, self.grid_size-nrow-1)]} to offend"
                            )
                        else:
                            logging.debug(
                                f"filling pos {self.coordinates_to_position[(nrow, self.grid_size-nrow-1)]} to defend"
                            )
                        return (nrow, self.grid_size - nrow - 1)

        # try for middle most cell or corners
        if hard:
            middle_pos = ((self.grid_size**2) // 2) + 1
            middle_row, middle_col = self.position_to_coordinates.get(middle_pos)
            if self.board[middle_row][middle_col] == Cell.EMPTY:
                self.set_mark_by_coordinates((middle_row, middle_col), Cell.COMPUTER)
                logging.debug("filling middle cell")
                return (middle_row, middle_col)
            else:
                # if no cell was filled and middle position is not empty, try corners
                # filter empty corner cells
                corner_coordinates = list(
                    filter(
                        lambda x: self.board[x[0]][x[1]] == Cell.EMPTY,
                        self.get_corner_cells(),
                    )
                )
                if len(corner_coordinates) <= 3:
                    return self._fill_computer_cell_easy()
                else:
                    choice = random.choice(corner_coordinates)
                    self.set_mark_by_coordinates(choice, Cell.COMPUTER)
                    logging.debug("filling corner cell")
                    return choice
        else:
            return self._fill_computer_cell_easy()

    def get_score(self, maximizing_player: Cell):
        # Check for rows
        for i in range(1, self.grid_size + 1):
            row = self.get_board_row(i)
            if len(set(row)) == 1 and Cell.EMPTY not in row:
                score = 1 if row[0] == maximizing_player else -1
                return score

        # Check for columns
        for i in range(1, self.grid_size + 1):
            column = self.get_board_column(i)
            if len(set(column)) == 1 and Cell.EMPTY not in column:
                score = 1 if column[0] == maximizing_player else -1
                return score

        # check for diagonals
        for i in range(-1, 2, 2):
            diagonal = self.get_board_diagonal(i)
            diagonal = set(diagonal)
            if len(diagonal) == 1 and Cell.EMPTY not in diagonal:
                score = 1 if diagonal.pop() == maximizing_player else -1
                return score

        return 0  # Tie

    def minimax(self, current_player: Cell, maximizing_player: Cell, depth: int):
        minimizing_player = Cell.PLAYER if maximizing_player == Cell.COMPUTER else Cell.COMPUTER
        # not using self.game_outcome because it displays board too
        if self.check_completion() or self.check_win().victory:
            return None, self.get_score(maximizing_player)

        best_score = float("-inf") if current_player == maximizing_player else float("inf")
        best_move = None

        available_moves = []
        try:
            available_moves = self.get_empty_cells()
        except GameplayError:
            pass

        for move in available_moves:
            # make the move
            self.board[move[0]][move[1]] = current_player

            # recursively call minimax for other player
            opp_player = Cell.PLAYER if current_player == Cell.COMPUTER else Cell.COMPUTER
            _, score = self.minimax(opp_player, maximizing_player, depth + 1)
            # score += depth

            # undo the move
            self.board[move[0]][move[1]] = Cell.EMPTY
            if (current_player == maximizing_player and score > best_score) or (current_player == minimizing_player and score < best_score):
                best_score = score
                best_move = move

        return best_move, best_score

    def _fill_computer_cell_hard(self, minimax: bool = True, maximizing_player: Cell = Cell.COMPUTER) -> tuple[int, int]:
        if minimax:
            move, score = self.minimax(maximizing_player, maximizing_player, 1)
            logging.debug(
                f"filling pos {self.coordinates_to_position[move]} by minimax ({score=})"
            )
            self.set_mark_by_coordinates(move, Cell.COMPUTER)
            return move
        else:
            return self._fill_computer_cell_medium(True)

    def fill_computer_cell(self) -> None:
        """
        Fills computer cell.
        """
        if self.difficulty == Difficulty.EASY:
            self._fill_computer_cell_easy()

        elif self.difficulty == Difficulty.MEDIUM:
            self._fill_computer_cell_medium()

        elif self.difficulty == Difficulty.HARD:
            self._fill_computer_cell_hard()

        else:
            raise GameplayError(f"Unknown difficulty level: {self.difficulty}")

    def check_completion(self) -> bool:
        """
        Checks if the board is filled, to finish the game in case of a draw.
        """
        counter = 0
        for row in self.board:
            if row.count(Cell.EMPTY) == 0:
                counter += 1

        return counter == self.grid_size

    def check_win(self) -> CheckWinResult:
        """
        Checks the board vertically, horizontally and diagonally for win.
        """
        # horizontal check
        for i in range(1, self.grid_size + 1):
            row = self.get_board_row(i)
            if len(set(row)) == 1 and Cell.EMPTY not in row:
                winner = "computer" if row[0] == Cell.COMPUTER else "player"
                return CheckWinResult(
                    victory=True,
                    winner=winner,
                    coordinates=[(i - 1, j) for j in range(0, self.grid_size)],
                )

        # vertical check
        for i in range(1, self.grid_size + 1):
            column = self.get_board_column(i)
            if len(set(column)) == 1 and Cell.EMPTY not in column:
                winner = "computer" if next(iter(column)) == Cell.COMPUTER else "player"
                return CheckWinResult(
                    victory=True,
                    winner=winner,
                    coordinates=[(j, i - 1) for j in range(0, self.grid_size)],
                )

        # diagonal check
        for i in range(-1, 2, 2):
            diagonal = self.get_board_diagonal(i)
            diagonal = set(diagonal)
            if len(diagonal) == 1 and Cell.EMPTY not in diagonal:
                winner = (
                    "computer" if next(iter(diagonal)) == Cell.COMPUTER else "player"
                )

                if i == 1:  # top left to bottom right diagonal
                    return CheckWinResult(
                        victory=True,
                        winner=winner,
                        coordinates=[(j, j) for j in range(0, 3)],
                    )
                else:  # top right to bottom left diagonal
                    return CheckWinResult(
                        victory=True,
                        winner=winner,
                        coordinates=[
                            (j, self.grid_size - j - 1)
                            for j in range(0, self.grid_size)
                        ],
                    )

        return CheckWinResult(victory=False)

    def display_board(self, result: Optional[CheckWinResult] = None):
        """
        Prints the current board on the console.

        The result param is optional. Pass it to highlight the row/column/diagonal for winning ref.
        """
        emoji_mappings = {
            Cell.EMPTY: QUESTION_MARK_EMOJI,
            Cell.COMPUTER: CROSS_MARK_EMOJI,
            Cell.PLAYER: BLUE_CIRCLE_EMOJI,
        }

        t = Table(show_lines=True, show_header=False)
        for i in range(1, self.grid_size + 1):
            t.add_column(str(i))

        for nrow, row in enumerate(self.board):
            table_row = list(map(lambda x: emoji_mappings.get(x), row))

            # only when the game has a winner
            # since result.coordinates is not provided in draw condition
            if result and result.coordinates:
                for ncol in range(0, self.grid_size):
                    if (nrow, ncol) in result.coordinates:
                        prev = Text(Emoji.replace(table_row[ncol]))
                        prev.stylize(Style(bgcolor="yellow"))
                        table_row[ncol] = prev

            t.add_row(*table_row)

        print(t)

    def position_input(self, prompt: str = "Choose position") -> int:
        """
        Uses rich to nicely ask the user about position.
        """
        pos = Prompt.ask(
            prompt,
            choices=[
                f"{self.coordinates_to_position.get(i)}" for i in self.get_empty_cells()
            ],
        )
        return int(pos)

    def game_outcome(self) -> tuple[bool, CheckWinResult]:
        """
        Checks if the game is over, either by a draw or a victory.
        """
        result = self.check_win()
        if result.victory:
            self.display_board(result=result)
            if result.winner == "player":
                print(f"[green]{TADA_EMOJI} Congratulations! You win the game. [/]")
            else:
                print(
                    f"[red]{PENSIVE_FACE_EMOJI} Oh no, you lost! Better luck next time.[/]"
                )
            return True, result

        if self.check_completion():
            self.display_board(result=result)
            print(f"{VICTORY_HAND_EMOJI} It's a draw. Better luck next time.")
            return True, None

        return False, None

    def play(self):
        """
        Main game loop.
        """
        # computer starting the game has a probability of 30%
        starter = "computer" if random.randint(1, 10) % 3 == 0 else "player"
        print(
            f"[cyan bold][underline]{starter.capitalize()}[/] is making the first move.[/]"
        )

        if starter == "computer":
            self.fill_computer_cell()

        while True:
            self.display_board()
            pos = self.position_input()

            self.fill_player_cell(pos)

            # check if player won
            finished, result = self.game_outcome()
            if finished:
                save = Confirm.ask("Would you like to save the game recording?")
                if save:
                    if result:
                        self.save_recording("computer", result.winner)
                    else:
                        self.save_recording("computer", "draw")
                break

            self.fill_computer_cell()

            finished, result = self.game_outcome()
            if finished:
                save = Confirm.ask("Would you like to save the game recording?")
                if save:
                    if result:
                        self.save_recording("computer", result.winner)
                    else:
                        self.save_recording("computer", "draw")
                break

    def save_recording(self, vs: str, winner: str):
        recordings_dir = self.app_dir / "recordings"
        now = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        moves = [asdict(i) for i in self.moves]
        recording_data = RecordingData(
            self.grid_size,
            moves,
            vs,
            winner,
            now,
        )

        # because colons are not allowed in filenames
        date_, time_ = now.split(" ")
        time_ = time_.replace(":", "-")

        recording_json = json.dumps(asdict(recording_data))
        filename = recordings_dir / f"{date_} {time_}.record"
        with open(str(filename), "w") as f:
            f.write(recording_json)


class RecordingPlayer(TicTacToe):
    """
    Recording Player inherits the TicTacToe class and uses the game engine to execute moves
    saved in the recording.
    """

    def __init__(self, speed: int = 1) -> None:
        self.recordings_dir = TicTacToe.init_dirs() / "recordings"
        self.speed = speed
        self.console = Console()

    def show_recordings_table(self) -> dict:
        t = Table(title="Available Recordings")
        t.add_column("S. No.", justify="center")
        t.add_column("Played At", justify="center", style="cyan")
        t.add_column("VS", justify="center", style="magenta")
        t.add_column("Winner", justify="center", style="purple")
        t.add_column("Grid Size", justify="center", style="green")

        rows = {}

        for i, recording in enumerate(self.recordings_dir.iterdir()):
            if not recording.name.endswith(".record"):
                continue
            with open(str(recording.absolute())) as f:
                content = json.load(f)
            grid_size = content["grid_size"]

            t.add_row(
                str(i + 1),
                content["when"],
                content["vs"],
                content["winner"],
                f"{grid_size}x{grid_size}",
            )
            rows[i + 1] = content

        if len(rows) == 0:
            print("[yellow]No playable recording found![/]")
            exit(0)

        print(Align(t, "center"))

        recording_index = Prompt.ask(
            "Which recording to watch? (by S. No.)",
            choices=[str(i) for i in rows],
            show_choices=False,  # with a lot of recordings the input will get cluttered
        )
        recording_index = int(recording_index)
        return rows[recording_index]

    def display_board(self, result: CheckWinResult | None = None):
        super().display_board(result)
        time.sleep(1 / self.speed)
        self.console.clear()

    def play_recording(self):
        content = self.show_recordings_table()
        moves = content["moves"]
        # difficulty doesnt matter
        super().__init__(Difficulty.HARD, content["grid_size"])
        self.display_board()
        for move in moves:
            position = move["pos"]
            coordinate = self.position_to_coordinates[position]
            self.set_mark_by_coordinates(coordinate, Cell[move["marker"]])

            finished, _ = self.game_outcome()
            if finished:
                break
            else:
                # to highlight the last move played
                dummy_result = CheckWinResult(True, coordinates=[coordinate])
                self.display_board(dummy_result)


class LMPTicTacToe(TicTacToe):
    """
    Local multiplayer variant of tic tac toe.
    """

    def __init__(self, player1: str, player2: str, grid_size: int) -> None:
        self.player1 = player1
        self.player2 = player2

        # difficulty doesn't matter here
        super().__init__(Difficulty.MEDIUM, grid_size)

    def fill_player_cell(self, player: str, pos: int):
        if player == self.player1:
            self.set_mark_by_position(pos, Cell.COMPUTER)
        elif player == self.player2:
            self.set_mark_by_position(pos, Cell.PLAYER)
        else:
            raise GameplayError(f"Unknown player {player}!")

    def game_outcome(self) -> tuple[bool, CheckWinResult]:
        """
        Checks if the game is over, either by a draw or a victory.
        """
        result = self.check_win()
        if result.victory:
            self.display_board(result=result)
            winner = self.player2 if result.winner == "player" else self.player1
            print(f"[green]{TADA_EMOJI} {winner} wins the game. [/]")
            return True, CheckWinResult(True, winner)

        if self.check_completion():
            self.display_board(result=result)
            print(f"{VICTORY_HAND_EMOJI} It's a draw. Better luck next time.")
            return True, None

        return False, None

    def play(self):
        starter = self.player1 if random.randint(1, 10) % 2 == 0 else self.player2
        print(
            f"[cyan bold][underline]{starter.capitalize()}[/] is making the first move.[/]"
        )
        other_player = self.player2 if starter == self.player1 else self.player1
        player_cycle = cycle([starter, other_player])

        for player in player_cycle:
            self.display_board()
            color = "red" if player == self.player1 else "blue"
            pos = self.position_input(f"Choose position [{color}]({player})[/]")

            self.fill_player_cell(player, pos)

            # check if any player won
            finished, result = self.game_outcome()
            if finished:
                save = Confirm.ask("Would you like to save the game recording?")
                if save:
                    if result:
                        self.save_recording("computer", result.winner)
                    else:
                        self.save_recording("computer", "draw")
                break


def main():
    panel = Panel(Text("Tic Tac Toe", style="#e5eb34 on #3492eb"), padding=1)
    print(Align(panel, "center"))

    mode = Prompt.ask(
        "What to do? \n1. Play game \n2. Watch past recordings \n",
        choices=list("12"),
        default="1",
    )
    if mode == "2":
        recording_player = RecordingPlayer()
        recording_player.play_recording()
        exit(0)

    vs = Prompt.ask(
        "1. Player vs Computer \n2. Player vs Player \n", choices=list("12")
    )

    if vs == "2":
        player1 = Prompt.ask("Enter name for player1", default="player1")
        player2 = Prompt.ask("Enter name for player2", default="player2")
    else:
        player1 = "computer"
        player2 = "player"
        difficulty = Prompt.ask(
            "Choose the difficulty level",
            choices=list(Difficulty),
            default=Difficulty.MEDIUM,
        )

    grid_size = Prompt.ask(
        "Choose the grid size", choices=[str(i) for i in range(3, 6)], default="3"
    )
    grid_size = int(grid_size)

    print("\n[bold blue underline]Before you proceed:[/]")

    print(f"{QUESTION_MARK_EMOJI} -> empty cell, can be chosen to place marker")
    print(f"{CROSS_MARK_EMOJI} -> cell filled by {player1}")
    print(f"{BLUE_CIRCLE_EMOJI} -> cell filled by {player2} \n")

    print("[bold blue underline]Positions:[/]")

    t = Table("a", "b", "c", show_lines=True, show_header=False)
    for i in range(1, (grid_size**2) + 1, grid_size):
        t.add_row(*[f"{j}" for j in range(i, i + grid_size)])

    print(t)
    input("Press enter once you've read the instructions.")

    while True:
        if vs == "1":
            game = TicTacToe(Difficulty(difficulty), grid_size)
        else:
            game = LMPTicTacToe(player1, player2, grid_size)
        game.play()

        play_again = Confirm.ask("Wanna play again?")
        if play_again:
            continue
        break


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("[green]\nbyeee[/]")

    except GameplayError as g:
        print("[red]fatal gameplay error, this should never happen.[/]")
        print(
            f"[yellow]A log file with error information is created at the location `{LOG_FILE_LOCATION}`. [/]"
        )
        logging.exception(g)

    except Exception as e:
        print("[red]fatal error![/]")
        print(
            f"[yellow]A log file with error information is created at the location `{LOG_FILE_LOCATION}`.[/]"
        )
        logging.exception(e)
