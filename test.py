from rich.console import Console
from rich.style import Style

def main():
    # Create a console
    console = Console()

    # Define colors for the light and dark squares
    light_square_color = "#FFFFE8"
    dark_square_color = "#557A46"
    chessboard = [
        "♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜",
        "♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟",
        " ", " ", " ", " ", " ", " ", " ", " ",
        " ", " ", " ", " ", " ", " ", " ", " ",
        " ", " ", " ", " ", " ", " ", " ", " ",
        " ", " ", " ", " ", " ", " ", " ", " ",
        "♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙",
        "♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖",
    ]

    # Print the chessboard
    for i in range(8):
        for j in range(8):
            piece = chessboard[i * 8 + j]
            cell_style = Style(
                bgcolor=light_square_color if (i + j) % 2 == 0 else dark_square_color
            )
            cell_content = f"{piece.center(2)}"
            console.print(cell_content, style=cell_style, end="")
        console.print()

if __name__ == "__main__":
    main()
