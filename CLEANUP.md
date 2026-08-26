# Code Cleanup Notes

## `board.py`

### 1. Inconsistent parameter naming
Parameters mix conventions: `_board`, `_cell` use a leading underscore, but `board_obj`, `in_list`, `data` don't.
The leading underscore is unusual in Python — it typically signals "private" or "intentionally unused". Pick one style.
Plain names (`board`, `cell`, `value`) are most idiomatic.

### 2. `set([...])` → `{...}` in `simple_pencil`
`set([cell.value for cell in ...])` builds an intermediate list then converts it.
Use a set comprehension directly: `{cell.value for cell in ... if cell.value != '.'}`.

### 3. `x`, `y`, `z` attribute names
`z` for block number is non-obvious. The inline comments `# col`, `# row`, `# block` only exist
because the names don't communicate their meaning. Consider renaming to `col`, `row`, `block`
so the comments become unnecessary everywhere these attributes are used.

### 4. `get_block` uses a loop + `append`
This is a natural fit for a list comprehension:
```python
return [self.data[y][x] for y in range(start_row, start_row + 3)
                         for x in range(start_col, start_col + 3)]
```

### 5. `assert` used for runtime validation
`assert` is silently stripped when Python runs with `-O` (optimize flag). The asserts in
`init_board` and `is_solved` guard real error conditions — use `if not ... raise ValueError(...)`
instead so they're always active.

---

## `strategies.py`

### 6. `{''}` placeholder in `hidden_single`
`solve_hidden` appends `{''}` (a set containing an empty string) as a placeholder for filled cells,
then filters it out downstream with `if value not in VALID_NUMS`. Use `set()` instead —
an empty set contributes nothing to `find_unique_set_values` and needs no guard.

### 7. `if len(hidden_singles) > 0`
`if hidden_singles:` is the idiomatic Python way to check a non-empty list.

---

## `pencil.py`

### 8. Mutation note in `locked_candidates`
The loop iterates `_cell.pencil` while discarding from *other* cells' pencil sets — not `_cell.pencil`
itself, so it's safe. But it looks like a mutation-during-iteration bug at first glance.
Worth a short comment to save the next reader the worry.

---

## `solve.py`

### 9. Iteration counter is off by one
`i` increments before `is_solved` is checked, so the logged iteration number doesn't match
the actual loop pass. Increment at the end of the loop, or restructure with `enumerate`.

### 10. `changed` list → strategy list (see pseudocode below)
`changed` collects booleans just for `any()`. This works, but see the pseudocode section
below for an approach that makes adding new strategies easier.

### 11. `assert` for board validity check
Same as note 5 — `assert _board.check_board()` will be silently skipped with `-O`.
Use a proper `if/raise`.

---

## `__main__.py`

### 12. Typo: "soduku" → "sudoku"
In the module docstring. Also appears in `src/test/test_solver.py`.

### 13. `_n` parameter implies generality that doesn't exist
`main(_n, _data)` takes `_n` as a parameter, but block size is hardcoded to 3 and
`VALID_NUMS` is always 1–9. Either remove `_n` and hardcode `9`, or make board size
truly configurable end-to-end.

### 14. `__main__.py` imports from the test suite
`from test.test_solver import UNSOLVED` is a reversed dependency — source code should
never import from tests. Move the puzzle data into `__main__.py` (or a `data.py`),
and have the test import from there.

---

## Pseudocode: programmatic strategy dispatch

Instead of calling each strategy explicitly and maintaining the `changed` list by hand,
register strategies in a list and loop over them. Adding a new technique is then just
appending to `STRATEGIES` — the solve loop doesn't need to change.

```
STRATEGIES = [last_digit, naked_single, hidden_single]

function solve(board):
    while True:
        if is_solved(board):
            return board

        changed = False
        for strategy in STRATEGIES:
            if strategy(board):
                changed = True

        if not changed:
            log "Board cannot be solved with current logic"
            return board
```

A more advanced version runs strategies in priority order and restarts from the cheapest
strategy whenever progress is made (since a `last_digit` find might unlock more `last_digit`
finds before needing `naked_single`):

```
STRATEGIES = [last_digit, naked_single, hidden_single]  # ordered cheapest → most expensive

function solve(board):
    while not is_solved(board):
        for strategy in STRATEGIES:
            if strategy(board):
                break          # restart from cheapest strategy
        else:
            # completed loop with no progress from any strategy
            log "Board cannot be solved with current logic"
            return board
    return board
```

The `for/else` construct in Python runs the `else` block only if the loop completed
without hitting a `break` — which here means no strategy made progress.
```
