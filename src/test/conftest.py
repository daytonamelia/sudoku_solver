"""
Shared fixtures and puzzle data for the test suite.
"""
import pytest
from src.solver.board import Board, init_board
from src.solver.solve import solve

PUZZLES = {
    'SUDOKU_1': {
        'unsolved': [
            '...26.7.1',
            '68..7..9.',
            '19...45..',
            '82.1...4.',
            '..46.29..',
            '.5...3.28',
            '..93...74',
            '.4..5..36',
            '7.3.18...'],
        'solved': [
            '435269781',
            '682571493',
            '197834562',
            '826195347',
            '374682915',
            '951743628',
            '519326874',
            '248957136',
            '763418259'],
        }
    }


@pytest.fixture
def board():
    """Create a 9x9 board."""
    b = Board(9)
    init_board(b, PUZZLES['SUDOKU_1']['unsolved'])
    return b


@pytest.fixture
def solved_board(board):
    """Solve and return a board."""
    solve(board)
    return board
