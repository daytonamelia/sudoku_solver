'''
Solver functions and strategies.
'''

from typing import Callable

from .board import Board, VALID_NUMS, find_unique_set_values
from .pencil import find_pencil, update_pencil

def last_digit(_board: Board) -> bool:
    '''Solves for the last digit for rows, columns, and blocks until no more progress can be made.
    Returns True if any changes were made to the board.'''
    def solve_one(_board: Board, get_group: Callable) -> bool:
        '''Solves for all of a board's last digits for a group (rows, columns, or blocks).
        Returns if change to board was made.'''
        changed = False
        for i in range(_board.n):
            group = get_group(i) # Get group
            empty_cells = [cell for cell in group if cell.value == '.']
            if len(empty_cells) == 1: # Only one empty cell
                missing_value = VALID_NUMS.difference({cell.value for cell in group}).pop()
                empty_cells[0].set(missing_value)
                changed = True
        return changed

    total_changed = False
    while True:
        row_changed = solve_one(_board, _board.get_row)
        col_changed = solve_one(_board, _board.get_col)
        block_changed = solve_one(_board, _board.get_block)
        iteration_changed = row_changed or col_changed or block_changed
        total_changed = total_changed or iteration_changed
        if not iteration_changed:
            break
    return total_changed


def naked_single(_board:Board) -> bool:
    '''Solves for naked singles for rows, columns, and blocks until no more progress can be made.
    Returns True if any changes were made to the board.'''
    total_changed = False
    while True:
        iteration_changed = False
        for y in range(_board.n):  # y = row index
            for x in range(_board.n):  # x = column index
                cell = _board.get_cell(x, y)
                if cell.value != '.':
                    continue
                marks = find_pencil(_board, cell)
                if marks == 1:
                    cell.set(cell.pencil.pop())
                    total_changed = True
                    iteration_changed = True
        if not iteration_changed:
            break
    return total_changed


def hidden_single(_board:Board) -> bool:
    '''Solves for hidden singles for rows, columns, and blocks until no more progress can be made.
    Return True if any changes were made to the board.'''
    def solve_hidden(_board:Board, get_group:Callable) -> bool:
        '''Checks and solves for all of a board's hidden singles for a group (rows, columns, or blocks).
        Returns if change to board was made.'''
        changed = False
        for i in range(_board.n):
            group = get_group(i)
            # Get marks for empty cells in group
            cell_marks = []
            for cell in group:
                if cell.value != '.':
                    cell_marks.append({''})
                    continue
                else:
                    cell_marks.append(cell.pencil)
            # Solve for hidden singles
            hidden_singles = find_unique_set_values(cell_marks)
            if len(hidden_singles) > 0:
                for single in hidden_singles:
                    index = single[0]
                    value = single[1].pop()
                    if value not in VALID_NUMS:
                        continue
                    group[index].set(value)
                    changed = True
        return changed

    total_changed = False
    while True:
        update_pencil(_board)
        row_changed = solve_hidden(_board, _board.get_row)
        if row_changed:
            update_pencil(_board)
        col_changed = solve_hidden(_board, _board.get_col)
        if col_changed:
            update_pencil(_board)
        block_changed = solve_hidden(_board, _board.get_block)
        if block_changed:
            update_pencil(_board)
        iteration_changed = row_changed or col_changed or block_changed
        total_changed = total_changed or iteration_changed
        if not iteration_changed:
            break
    return total_changed
