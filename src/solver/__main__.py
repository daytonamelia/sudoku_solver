"""
Simple sudoku solver.
https://hodoku.sourceforge.net/en/techniques.php
"""
import argparse
import logging

from .board import Board, BoardError, init_board
from .solve import solve

def arg_parse() -> argparse.Namespace:
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Solve a sudoku puzzle from a file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Usage:
        python -m solver test/puzzles/sudoku_9x9.txt
        python -m solver test/puzzles/sudoku_9x9.txt --debug
        python -m solver --help
        """,
        )
    parser.add_argument(
        "file", type=str,
        help="Path to puzzle file (one row per line, '.' for empty cells).",
        )
    parser.add_argument(
        "--debug", action="store_true",
        help="Show solve steps.",
        )
    return parser.parse_args()


def main(puzzle_data: list[str], debug: bool = False) -> None:
    """Orchestrator and printing."""
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s")
    board = Board(len(puzzle_data))
    init_board(board, puzzle_data)
    print('\n---\n')
    print(board)
    print('\n')
    board = solve(board)
    print('\n---\n')
    print(board)


if __name__ == '__main__':
    args = arg_parse()

    with open(args.file, encoding="utf-8") as f:
        data = [line.strip() for line in f if line.strip()]

    try:
        main(data, debug=args.debug)
    except BoardError as e:
        print(f"Error: {e}")
