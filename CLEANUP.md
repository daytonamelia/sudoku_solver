# Code Cleanup Notes

## `board.py`


### 5. `assert` used for runtime validation
`assert` is silently stripped when Python runs with `-O` (optimize flag). The asserts in
`init_board` and `is_solved` guard real error conditions — use `if not ... raise ValueError(...)`
instead so they're always active.

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

### 13. `_n` parameter implies generality that doesn't exist
`main(_n, _data)` takes `_n` as a parameter, but block size is hardcoded to 3 and
`VALID_NUMS` is always 1–9. Either remove `_n` and hardcode `9`, or make board size
truly configurable end-to-end.
