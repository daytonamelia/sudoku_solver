"""
Sudoku olver functions and strategies.
"""

from typing import Callable

from .board import Board, find_unique_set_values
from .pencil import find_pencil


def last_digit(board: Board, get_group: Callable) -> bool:
    """
    Solves for the last digit for a group until no more progress can be made.
    Returns True if any changes were made to the board.
    """
    changed = False
    for i in range(board.n):
        group = get_group(i) # Get group
        empty_cells = [cell for cell in group if cell.value == '.']
        if len(empty_cells) == 1: # Only one empty cell
            missing_value = board.valid_nums.difference({cell.value for cell in group}).pop()
            empty_cells[0].set(missing_value)
            changed = True
    return changed


def naked_single(board:Board, get_group: Callable) -> bool:
    """
    Solves for naked singles for a group until no more progress can be made.
    Returns True if any changes were made to the board.
    
    Note: get_group is a logic artifact, not used but needs to stay
    """
    total_changed = False
    while True:
        iteration_changed = False
        for row in range(board.n):
            for col in range(board.n):
                cell = board.get_cell(col, row)
                if cell.value != '.':
                    continue
                marks = find_pencil(board, cell)
                if marks == 1:
                    cell.set(cell.pencil.pop())
                    total_changed = True
                    iteration_changed = True
        if not iteration_changed:
            break
    return total_changed


def hidden_single(board:Board, get_group: Callable) -> bool:
    """
    Solves for hidden singles for a group until no more progress can be made.
    Return True if any changes were made to the board.
    """
    changed = False
    for i in range(board.n):
        group = get_group(i)
        # Get marks for empty cells in group
        cell_marks = []
        for cell in group:
            if cell.value != '.':
                cell_marks.append(set()) # keeps correct cell index
            else:
                cell_marks.append(cell.pencil)
        # Solve for hidden singles
        hidden_singles = find_unique_set_values(cell_marks)
        if hidden_singles:
            for single in hidden_singles:
                index = single[0]
                value = single[1].pop()
                group[index].set(value)
                changed = True
    return changed
