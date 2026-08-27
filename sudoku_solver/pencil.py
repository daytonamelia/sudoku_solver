"""
Pencil mark logic and strategies.
"""
from .board import Board, Cell

def update_pencil(board:Board) -> None:
    """Update pencil marks for the entire board."""
    for row in range(board.n):
        for col in range(board.n):
            cell = board.get_cell(col, row)
            if cell.value != '.':
                continue
            find_pencil(board, cell)


def find_pencil(board: Board, cell: Cell) -> int:
    """Find pencil marks for a cell and returns how many pencil marks that cell has."""
    if cell.value != '.':
        return 0
    # Set simple pencil marks to start
    marks = simple_pencil(board, cell)
    cell.set_pencil(marks)
    # More advanced logic
    locked_candidates(board, cell)
    return len(cell.pencil)


def simple_pencil(board: Board, cell: Cell) -> set:
    """Given a cell, find which pencil marks are possible with simple logic."""
    row = {cell.value for cell in board.get_row(cell.row) if cell.value != '.'}
    col = {cell.value for cell in board.get_col(cell.col) if cell.value != '.'}
    block = {cell.value for cell in board.get_block(cell.block) if cell.value != '.'}
    marks = row.union(col, block)
    return board.valid_nums.difference(marks)


def locked_candidates(board: Board, cell: Cell) -> None:
    """Given a cell, find locked candiates for pencil marks."""        
    # Type I (pointing) by block
    row = [cell for cell in board.get_row(cell.row) if cell.value == '.']
    col = [cell for cell in board.get_col(cell.col) if cell.value == '.']
    block = [cell for cell in board.get_block(cell.block) if cell.value == '.']
    for candidate in cell.pencil: # only other cells' pencils are modified
        # Type I (pointing): If candidate in block is confined to one row/col
        candidate_cells = [cell for cell in block if candidate in cell.pencil]
        if len(candidate_cells) > 1:
            if all(cell.row == candidate_cells[0].row for cell in candidate_cells):
                for cell in row:
                    if cell.block != candidate_cells[0].block:
                        cell.pencil.discard(candidate)
            elif all(cell.col == candidate_cells[0].col for cell in candidate_cells):
                for cell in col:
                    if cell.block != candidate_cells[0].block:  # different block
                        cell.pencil.discard(candidate)

        # Type II (claiming): If candidate in row/col is confined to one block
        row_cells = [cell for cell in row if candidate in cell.pencil]
        if len(row_cells) > 1 and all(cell.block == row_cells[0].block for cell in row_cells):
            for cell in block:
                if cell.row != row_cells[0].row:
                    cell.pencil.discard(candidate)
        col_cells = [cell for cell in col if candidate in cell.pencil]
        if len(col_cells) > 1 and all(cell.block == col_cells[0].block for cell in col_cells):
            for cell in block:
                if cell.col != col_cells[0].col:
                    cell.pencil.discard(candidate)


def hidden_subsets(_board: Board, _cell: Cell) -> None:
    """Given a cell find hidden subsets (pairs, triples, quadruples) for that cell."""
    # TODO: Hidden pair
    row = [cell for cell in _board.get_row(_cell.row) if cell.value == '.']
    col = [cell for cell in _board.get_col(_cell.col) if cell.value == '.']
    block = [cell for cell in _board.get_block(_cell.block) if cell.value == '.']
