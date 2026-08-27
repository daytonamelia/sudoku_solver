"""
End-to-end solver tests.
"""
import pytest
from src.solver.board import Board, init_board
from src.solver.solve import solve
from src.test.conftest import PUZZLES


@pytest.mark.parametrize("puzzle", PUZZLES.values(), ids=PUZZLES.keys())
def test_solve_completes(puzzle):
    """solve leaves no empty cells on a solvable puzzle."""
    board = Board(9)
    init_board(board, puzzle['unsolved'])
    solve(board)
    assert not any(cell.value == '.' for row in board.data for cell in row)


@pytest.mark.parametrize("puzzle", PUZZLES.values(), ids=PUZZLES.keys())
def test_solve_correct(puzzle):
    """solve produces the known correct solution for each puzzle."""
    board = Board(9)
    init_board(board, puzzle['unsolved'])
    solve(board)
    result = [''.join(str(cell) for cell in row) for row in board.data]
    assert result == puzzle['solved']


def test_solve_board_valid(solved_board):
    """The solved board passes the validity check (no duplicate digits)."""
    assert solved_board.check_board()
