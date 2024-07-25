class PlacePiece:
    def __init__(self) -> None:
        self.game = None
        # self.pieces = {
        #     "bq": "♛",
        #     "bk": "♚",
        #     "bb": "♝",
        #     "bn": "♞",
        #     "br": "♜",
        #     "bp": "♟",
        #     "wq": "♕",
        #     "wk": "♔",
        #     "wb": "♗",
        #     "wn": "♘",
        #     "wr": "♖",
        #     "wp": "♙",
        # }

        self._place_chess_pieces()

    def _place_chessmen(self, prefix: str):
        chessmen = list("rnbqkbnr")

        for index, piece in enumerate(chessmen):
            suffix = "1" if index < 3 else ("2" if index > 4 else "")
            self.game.append(f"{prefix}{piece}{suffix}")
            # self.game.append(f"{self.pieces.get(prefix+piece)}")

    def _place_pawns(self, prefix: str):
        for index in range(1, 9):
            self.game.append(f"{prefix}p{index}")
            # self.game.append(f"{self.pieces.get(prefix+"p")}")

        if prefix == "b":
            self.game.extend(" " * 32)

    def _place_chess_pieces(self):
        self.game = []

        for i in range(2):
            prefix = "w" if i == 1 else "b"

            if i == 0:
                self._place_chessmen(prefix)
                self._place_pawns(prefix)

            else:
                self._place_pawns(prefix)
                self._place_chessmen(prefix)
