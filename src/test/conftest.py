"""
Shared fixtures and puzzle data for the test suite.
"""
import pytest
from src.solver.board import Board, init_board
from src.solver.solve import solve

PUZZLES = {
    'SUDOKU_9x9': {
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
        },
    'SUDOKU_4x4': {
        'unsolved': [
            '12.4',
            '.412',
            '21.3',
            '432.'],
        'solved': [
            '1234',
            '3412',
            '2143',
            '4321'],
        },
    }


@pytest.fixture
def board():
    """Create and initialise the default (9x9) test board."""
    data = PUZZLES['SUDOKU_9x9']['unsolved']
    b = Board(len(data))
    init_board(b, data)
    return b


@pytest.fixture
def solved_board(board: Board):
    """Solve and return a board."""
    return solve(board)
