'''
Solver orchestrator.
'''
import logging

from .board import Board, is_solved
from .strategies import last_digit, naked_single, hidden_single

logger = logging.getLogger(__name__)


def solve(_board: Board) -> Board:
    '''Main sudoku solver logic.'''
    i = 0
    while True:
        logger.debug("--- iteration %d", i)
        i += 1
        if is_solved(_board):
            logger.info("Board solved!")
            return _board
        changed = []

        logger.debug("Checking for last digits...")
        changed.append(last_digit(_board))
        logger.debug("Checking for naked singles...")
        changed.append(naked_single(_board))
        logger.debug("Checking for hidden singles...")
        changed.append(hidden_single(_board))

        assert _board.check_board(), f"Error in board!\n{_board}"
        if not any(changed):
            logger.warning("Board cannot be solved with current logic!")
            return _board
