'''
Simple soduku solver.
https://hodoku.sourceforge.net/en/techniques.php
'''
# --- Imports ---
from typing import Callable

# --- Classes ---
class Cell:
    '''
    A single sudoku cell with coordinates x, y. '.' indicates an empty cell.
    '''
    def __init__(self, _x: int, _y: int, _value: str = '.', ) -> None:
        '''Creates a cell with coordinates x,  y and an optional value.'''
        self.x = _x
        self.y =_y
        self.value = _value
        self.pencil = None if self.value != '.' else []

    def __str__(self) -> str:
        '''Returns cell value as a string.'''
        return str(self.value)

    def set(self, _value:str) -> None:
        '''Sets the value of a cell to a new value.'''
        print(f"INFO: Setting cell at ({self.x}, {self.y}) to {_value}")
        self.value = _value
        
    def set_pencil(self, marks:list) -> None:
        '''Set the cell's pencil marks.'''
        self.pencil = marks


class Board:
    '''
    A square sudoku board of nxn Cell objects.
    '''
    def __init__(self, _n:int=9) -> None:
        '''Creates an empty square board of n lists of Cells within a list.'''
        self.n = _n
        self.data = [[Cell(x, y) for x in range(self.n)] for y in range(self.n)]

    def __str__(self) -> str:
        '''Returns board as space-delineated string with each row as a new line.'''
        board_rows = [' '.join(str(cell) for cell in row) for row in self.data]
        return '\n'.join(board_rows)

    def set_cell(self, value:str, x:int, y:int) -> None:
        '''Given coordinates, fills a single cell on the board.'''
        self.data[y][x].set(value)

    def set_row(self, values:list, _y:int) -> None:
        '''Given a y-coordinate, fill the row with a list of values.'''
        for i in range(self.n):
            self.set_cell(values[i], i, _y)

    def check_board(self) -> bool:
        '''Checks if board is valid.'''
        valid_nums = {str(i) for i in range(1, self.n + 1)}
        for i in range(self.n):
            row = self.get_row(i)
            col = self.get_col(i)
            block = self.get_block(i)
            for num in valid_nums:
                row_count = sum(1 for cell in row if cell.value == num)
                col_count = sum(1 for cell in col if cell.value == num)
                block_count = sum(1 for cell in block if cell.value == num)
                if row_count > 1 or col_count > 1 or block_count > 1:
                    print(f"On {num}: {row_count} rows, {col_count} cols, {block_count} blocks.")
                    return False
        return True

    def get_row(self, y: int) -> list:
        '''Returns a row as a list of Cell objects.'''
        return self.data[y]

    def get_col(self, x: int) -> list:
        '''Returns a column as a list of Cell objects.'''
        return [row[x] for row in self.data]

    def get_block(self, z: int) -> list:
        '''Returns a block as a list of Cell objects. 
        Z must be between 0-8 inclusive and starts from top-left of the board.'''
        block = []
        start_row = (z // 3) * 3
        start_col = (z % 3) * 3
        for y in range(start_row, start_row + 3):
            for x in range(start_col, start_col + 3):
                block.append(self.data[y][x])
        return block

# --- Helper Functions ---
def init_board(board_obj: Board, data:list) -> None:
    '''Fills board with either numbers or .'''
    # Input checks
    assert len(data) == board_obj.n, f"Input data has length {len(data)}."
    assert all(isinstance(item, str) for item in data), "Input data must contain only strings."
    assert all(len(item) == board_obj.n for item in data), "Input data must have 9 items in each string."
    print('Setting board...')
    for i in range(board_obj.n):
        rowdata = list(data[i])
        board_obj.set_row(rowdata, i)


def is_solved(_board: Board) -> bool:
    '''Checks if board is solved (no empty cells and valid).'''
    assert _board.check_board(), f"Error in board!\n{_board}"
    return not any(cell.value == '.' for row in _board.data for cell in row)


# --- Solver Functions ---
def last_digit(_board: Board) -> bool:
    '''Solves for the last digit for rows, columns, and blocks until no more progress can be made.
    Returns True if any changes were made to the board.'''
    
    def solve_one(_board: Board, get_group: Callable) -> bool:
        '''Solves for all of a board's last digits for a group (rows, columns, or blocks).
        Returns if change to board was made.'''
        assert _board.check_board(), f"Error in board!\n{_board}"
        changed = False
        valid_nums = {str(i) for i in range(1, _board.n + 1)}
        for i in range(_board.n):
            group = get_group(i) # Get group
            empty_cells = [cell for cell in group if cell.value == '.']
            if len(empty_cells) == 1: # Only one empty cell
                missing_value = valid_nums.difference({cell.value for cell in group}).pop()
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


# --- Main Functions ---
def solver(_board: Board) -> Board:
    '''Main sudoku solver logic.'''
    print('Solving board...')
    while True:
        # Check if solved
        if is_solved(_board):
            print("Board solved!")
            return _board
        changed = []
        # Try all solving techniques
        changed.append(last_digit(_board))
        # If nothing changed then unsolvable with current logic
        if not any(changed):
            print("Board cannot be solved with current logic!")
            return _board


def main(_n:int, _data:list) -> None:
    '''Main function that handles print output.'''
    board = Board(_n)
    init_board(board, _data)
    print('\n---\n')
    print(board)
    print('\n')
    board = solver(board)
    print('\n---\n')
    print(board)


if __name__ == '__main__':
    '''Run at init'''
    unsolved_data = [
        '...26.7.1',
        '68..7..9.',
        '19...45..',
        '82.1...4.',
        '..46.29..',
        '.5...3.28',
        '..93...74',
        '.4..5..36',
        '7.3.18...']
    solved_data = [
        '435269781',
        '682571493',
        '197834562',
        '826195347',
        '374682915',
        '951743628',
        '519326874',
        '248957136',
        '763418259']
    test_data = [
        '4352697.1',
        '68.571493',
        '197834562',
        '82619.347',
        '374682915',
        '95.743628',
        '519326874',
        '24895.136',
        '763418259']
    
    main(9, test_data)
