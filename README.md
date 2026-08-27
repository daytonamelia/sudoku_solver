# sudoku-solver

A sudoku solver that works for any perfect-square board size (4×4, 9×9, 16×16, ...).

## Usage

Puzzle files are plain text with one row per line and `.` for empty cells:

```
...26.7.1
68..7..9.
19...45..
...
```

Run the solver:

```bash
python -m sudoku_solver path/to/puzzle.txt
```

Show solve steps:

```bash
python -m sudoku_solver path/to/puzzle.txt --debug
```

Sample puzzles in `tests/puzzles/`.

## Current Supported Strategies
Last digit, naked single, hidden single, locked candidates.

## Tests

```bash
python -m pytest src/test/
```

To add a new puzzle, drop two files in `tests/puzzles/`:

- `mypuzzle.txt` — unsolved grid
- `mypuzzle_solved.txt` — expected solution

The test suite discovers and runs them automatically.
