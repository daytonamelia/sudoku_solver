"""
Simple sudoku solver.
https://hodoku.sourceforge.net/en/techniques.php
"""
import logging

from .board import Board, init_board
from .solve import solve

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


def main(n: int, data: list) -> None:
    """Orchestrator and printing."""
    board = Board(n)
    init_board(board, data)
    print('\n---\n')
    print(board)
    print('\n')
    board = solve(board)
    print('\n---\n')
    print(board)


if __name__ == '__main__':
    unsolved = [
        '...26.7.1',
        '68..7..9.',
        '19...45..',
        '82.1...4.',
        '..46.29..',
        '.5...3.28',
        '..93...74',
        '.4..5..36',
        '7.3.18...']
    main(9, unsolved)
