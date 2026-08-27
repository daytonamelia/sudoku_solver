"""
Tests for Board and Cell.
"""
from src.solver.board import Board, is_solved


def test_board_dimensions():
    """A fresh 9x9 board has 9 rows each with 9 cells."""
    b = Board(9)
    assert len(b.data) == 9
    assert all(len(row) == 9 for row in b.data)


def test_board_cells_are_empty():
    """A fresh board has all cells set to '.'."""
    b = Board(9)
    assert all(cell.value == '.' for row in b.data for cell in row)


def test_get_row_length(board):
    """get_row returns exactly n cells."""
    assert len(board.get_row(0)) == 9


def test_get_col_length(board):
    """get_col returns exactly n cells."""
    assert len(board.get_col(0)) == 9


def test_get_block_length(board):
    """get_block returns exactly n cells."""
    assert len(board.get_block(0)) == 9


def test_get_row_correct_cells(board):
    """All cells returned by get_row share the same row coordinate."""
    row = board.get_row(2)
    assert all(cell.row == 2 for cell in row)


def test_get_col_correct_cells(board):
    """All cells returned by get_col share the same col coordinate."""
    col = board.get_col(3)
    assert all(cell.col == 3 for cell in col)


def test_get_block_correct_cells(board):
    """All cells in block 4 (center) fall within rows 3-5 and cols 3-5."""
    block = board.get_block(4)
    assert all(3 <= cell.row <= 5 and 3 <= cell.col <= 5 for cell in block)


def test_init_board_places_known_values(board):
    """init_board correctly places given digits (SUDOKU_1 row 0: '...26.7.1')."""
    assert board.get_cell(3, 0).value == '2'
    assert board.get_cell(4, 0).value == '6'
    assert board.get_cell(8, 0).value == '1'


def test_init_board_leaves_empties(board):
    """init_board leaves '.' for blank cells."""
    assert board.get_cell(0, 0).value == '.'


def test_check_board_valid(board):
    """A freshly initialised board passes the validity check."""
    assert board.check_board()


def test_is_solved_false_on_unsolved(board):
    """is_solved returns False when the board still has empty cells."""
    assert not is_solved(board)
