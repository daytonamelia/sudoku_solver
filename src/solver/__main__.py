'''
Simple sudoku solver.
https://hodoku.sourceforge.net/en/techniques.php
'''
import logging

from .board import Board, init_board
from .solve import solve

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


def main(n: int, data: list) -> None:
    '''
    Orchestrator and printing.
    '''
    board = Board(n)
    init_board(board, data)
    print('\n---\n')
    print(board)
    print('\n')
    board = solve(board)
    print('\n---\n')
    print(board)


if __name__ == '__main__':
    from test.test_solver import UNSOLVED
    main(9, UNSOLVED)
