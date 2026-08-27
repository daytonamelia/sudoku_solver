"""
Shared fixtures and puzzle data for the test suite.

Puzzles are loaded from src/test/puzzles/. Each puzzle pair is two files:
  <name>.txt       — unsolved grid (one row per line, '.' for empty)
  <name>_solved.txt — expected solution
"""
import pathlib
import pytest
from sudoku_solver.board import Board, init_board
from sudoku_solver.solve import solve

_PUZZLE_DIR = pathlib.Path(__file__).parent / "puzzles"

def _load_puzzles() -> dict[str, dict[str, list[str]]]:
    """Load unsolved/solved puzzles from puzzles directory."""
    puzzles: dict[str, dict[str, list[str]]] = {}
    for unsolved_path in sorted(_PUZZLE_DIR.glob("*.txt")):
        if unsolved_path.stem.endswith("_solved"):
            continue
        solved_path = _PUZZLE_DIR / f"{unsolved_path.stem}_solved.txt"
        if solved_path.exists():
            puzzles[unsolved_path.stem] = {
                "unsolved": unsolved_path.read_text().splitlines(),
                "solved": solved_path.read_text().splitlines(),
            }
    return puzzles


PUZZLES = _load_puzzles()


@pytest.fixture
def board():
    """Create and initialise the default (9x9) test board."""
    data = PUZZLES['sudoku_9x9']['unsolved']
    b = Board(len(data))
    init_board(b, data)
    return b


@pytest.fixture
def solved_board(board: Board):
    """Solve and return a board."""
    return solve(board)
