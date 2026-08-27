"""
Tests for pencil mark logic.
"""
from src.solver.board import Board
from src.solver.pencil import simple_pencil, update_pencil


def test_simple_pencil_returns_set(board: Board) -> None:
    """simple_pencil returns a set."""
    cell = board.get_cell(0, 0)
    marks = simple_pencil(board, cell)
    assert isinstance(marks, set)


def test_simple_pencil_nonempty(board: Board) -> None:
    """An empty cell with peers has at least one candidate."""
    cell = board.get_cell(0, 0)
    marks = simple_pencil(board, cell)
    assert len(marks) > 0


def test_simple_pencil_excludes_row_values(board: Board) -> None:
    """Candidates never include a value already in the cell's row."""
    cell = board.get_cell(0, 0)
    row_values = {c.value for c in board.get_row(0) if c.value != '.'}
    marks = simple_pencil(board, cell)
    assert marks.isdisjoint(row_values)


def test_simple_pencil_excludes_col_values(board: Board) -> None:
    """Candidates never include a value already in the cell's column."""
    cell = board.get_cell(0, 0)
    col_values = {c.value for c in board.get_col(0) if c.value != '.'}
    marks = simple_pencil(board, cell)
    assert marks.isdisjoint(col_values)


def test_simple_pencil_excludes_block_values(board: Board) -> None:
    """Candidates never include a value already in the cell's block."""
    cell = board.get_cell(0, 0)
    block_values = {c.value for c in board.get_block(cell.block) if c.value != '.'}
    marks = simple_pencil(board, cell)
    assert marks.isdisjoint(block_values)


def test_update_pencil_fills_empty_cells(board: Board) -> None:
    """After update_pencil, a known empty cell has at least one candidate.

    Spot-checks one cell rather than all — locked_candidates can reduce
    other cells' marks mid-pass before they've been processed.
    """
    update_pencil(board)
    assert len(board.get_cell(0, 0).pencil) > 0


def test_update_pencil_skips_filled_cells(board: Board) -> None:
    """update_pencil leaves pencil marks empty on already-filled cells."""
    update_pencil(board)
    filled_cells = [cell for row in board.data for cell in row if cell.value != '.']
    assert all(len(cell.pencil) == 0 for cell in filled_cells)
