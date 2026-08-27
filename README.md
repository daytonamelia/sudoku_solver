# sudoku_solver

A logical sudoku solver that works for any perfect-square board size (4×4, 9×9, 16×16, ...)

Current Supported Strategies: Last digit, naked single, hidden single, locked candidates.

[Find more information on Sudoku strategies from Bernhard Hobiger's HoDoKu page.](https://hodoku.sourceforge.net/en/techniques.php)

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
