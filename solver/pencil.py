'''
Pencil mark logic and strategies.
'''
from .board import Board, Cell, VALID_NUMS

def update_pencil(_board:Board) -> None:
    '''Update pencil marks for the entire board.'''
    for y in range(_board.n):  # y = row index
        for x in range(_board.n):  # x = column index
            cell = _board.get_cell(x, y)
            if cell.value != '.':
                continue
            find_pencil(_board, cell)


def find_pencil(_board: Board, _cell: Cell) -> int:
    '''Find pencil marks for a cell and returns how many pencil marks that cell has.'''
    if _cell.value != '.':
        return 0
    # Set simple pencil marks to start
    marks = simple_pencil(_board, _cell)
    _cell.set_pencil(marks)
    # More advanced logic
    locked_candidates(_board, _cell)
    return len(_cell.pencil)


def simple_pencil(_board: Board, _cell: Cell) -> set:
    '''Given a cell, find which pencil marks are possible with simple logic.'''
    row = set([cell.value for cell in _board.get_row(_cell.y) if cell.value != '.'])
    col = set([cell.value for cell in _board.get_col(_cell.x) if cell.value != '.'])
    block = set([cell.value for cell in _board.get_block(_cell.z) if cell.value != '.'])
    marks = row.union(col, block)
    return VALID_NUMS.difference(marks)


def locked_candidates(_board: Board, _cell: Cell) -> None:
    '''Given a cell, find locked candiates for pencil marks.'''        
    # Type I (pointing) by block
    row = [cell for cell in _board.get_row(_cell.y) if cell.value == '.']
    col = [cell for cell in _board.get_col(_cell.x) if cell.value == '.']
    block = [cell for cell in _board.get_block(_cell.z) if cell.value == '.']
    for candidate in _cell.pencil:
        # Type I (pointing): If candidate in block is confined to one row/col
        candidate_cells = [cell for cell in block if candidate in cell.pencil]
        if len(candidate_cells) > 1:
            if all(cell.y == candidate_cells[0].y for cell in candidate_cells):  # same row
                for cell in row:
                    if cell.z != candidate_cells[0].z:  # different block
                        cell.pencil.discard(candidate)
            elif all(cell.x == candidate_cells[0].x for cell in candidate_cells):  # same col
                for cell in col:
                    if cell.z != candidate_cells[0].z:  # different block
                        cell.pencil.discard(candidate)

        # Type II (claiming): If candidate in row/col is confined to one block
        row_cells = [cell for cell in row if candidate in cell.pencil]
        if len(row_cells) > 1 and all(cell.z == row_cells[0].z for cell in row_cells):
            for cell in block:
                if cell.y != row_cells[0].y:  # different row
                    cell.pencil.discard(candidate)
        col_cells = [cell for cell in col if candidate in cell.pencil]
        if len(col_cells) > 1 and all(cell.z == col_cells[0].z for cell in col_cells):
            for cell in block:
                if cell.x != col_cells[0].x:  # different col
                    cell.pencil.discard(candidate)


def hidden_subsets(_board: Board, _cell: Cell) -> None:
    '''Given a cell find hidden subsets (pairs, triples, quadruples) for that cell.'''
    # TODO: Hidden pair
    row = [cell for cell in _board.get_row(_cell.y) if cell.value == '.']
    col = [cell for cell in _board.get_col(_cell.x) if cell.value == '.']
    block = [cell for cell in _board.get_block(_cell.z) if cell.value == '.']
