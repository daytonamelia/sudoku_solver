"""
Pytest framework.
"""
import pytest
from src.solver.board import Board, init_board
from src.solver.solve import solve

UNSOLVED = [
    '...26.7.1',
    '68..7..9.',
    '19...45..',
    '82.1...4.',
    '..46.29..',
    '.5...3.28',
    '..93...74',
    '.4..5..36',
    '7.3.18...']

SOLVED = [
    '435269781',
    '682571493',
    '197834562',
    '826195347',
    '374682915',
    '951743628',
    '519326874',
    '248957136',
    '763418259']


@pytest.fixture
def solved_board():
    board = Board(9)
    init_board(board, UNSOLVED)
    solve(board)
    return board


def test_solve(solved_board):
    result = [' '.join(str(cell) for cell in row) for row in solved_board.data]
    expected = [' '.join(row) for row in SOLVED]
    assert result == expected
