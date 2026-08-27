"""
Sudoku solver orchestrator.
"""
import logging
from typing import Callable

from .board import Board, is_solved
from .strategies import last_digit, naked_single, hidden_single

logger = logging.getLogger(__name__)


def solve_groups(board: Board, solver: Callable) -> bool:
    """
    Uses a solver function on every group until no more progress can be made.
    Returns True if any changes were made to the board.
    """
    total_changed = False
    while True:
        row_changed = solver(board, board.get_row)
        col_changed = solver(board, board.get_col)
        block_changed = solver(board, board.get_block)
        iteration_changed = row_changed or col_changed or block_changed
        total_changed = total_changed or iteration_changed
        if not iteration_changed:
            break
    return total_changed


def solve(board: Board) -> Board:
    """Main sudoku solver logic."""
    # strategies ordered cheapest -> most expensive
    strategies = [
        last_digit,
        naked_single,
        hidden_single,
    ]
    i = 0
    while not is_solved(board):
        logger.debug("--- iteration %d ---", i)
        i +=1
        for strategy in strategies:
            if solve_groups(board, strategy):
                break # something changed, restart from cheapest

        else:
            # completed loop with no progress
            logger.warning("Board cannot be solved with current logic!")
            return board
    return board
