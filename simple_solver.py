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
        '''Creates a cell with coordinates x, y, block, and an optional value.'''
        self.x = _x
        self.y =_y
        self.z = self.find_block()
        self.value = _value
        self.pencil = set()

    def find_block(self) -> int:
        '''Finds which block (z) the cell is in. Returns block number 0-8.'''
        row_block = self.y // 3
        col_block = self.x // 3
        return row_block * 3 + col_block

    def __str__(self) -> str:
        '''Returns cell value as a string.'''
        return str(self.value)

    def set(self, _value:str) -> None:
        '''Sets the value of a cell to a new value.'''
        print(f"INFO: Setting cell at ({self.x}, {self.y}) to {_value}")
        self.value = _value
        
    def set_pencil(self, _marks:set) -> None:
        '''Update the cell's pencil marks.'''
        self.pencil.update(_marks)
        

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
        for i in range(self.n):
            row = self.get_row(i)
            col = self.get_col(i)
            block = self.get_block(i)
            for num in VALID_NUMS:
                row_count = sum(1 for cell in row if cell.value == num)
                col_count = sum(1 for cell in col if cell.value == num)
                block_count = sum(1 for cell in block if cell.value == num)
                if row_count > 1 or col_count > 1 or block_count > 1:
                    print(f"On {num}: {row_count} rows, {col_count} cols, {block_count} blocks.")
                    return False
        return True

    def get_cell(self, x:int, y:int) -> Cell:
        '''Returns a Cell from x and y coordinates.'''
        return self.data[y][x]

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


def solve_one(_board: Board, get_group: Callable) -> bool:
    '''Solves for all of a board's last digits for a group (rows, columns, or blocks).
    Returns if change to board was made.'''
    assert _board.check_board(), f"Error in board!\n{_board}"
    changed = False
    for i in range(_board.n):
        group = get_group(i) # Get group
        empty_cells = [cell for cell in group if cell.value == '.']
        if len(empty_cells) == 1: # Only one empty cell
            missing_value = VALID_NUMS.difference({cell.value for cell in group}).pop()
            empty_cells[0].set(missing_value)
            changed = True
    return changed
    

def find_pencil(_board: Board, _cell: Cell) -> int:
    '''Find pencil marks for a cell.'''
    if _cell.value != '.':
        return 0
    row = set([cell.value for cell in _board.get_row(_cell.y) if cell.value != '.'])
    col = set([cell.value for cell in _board.get_col(_cell.x) if cell.value != '.'])
    block = set([cell.value for cell in _board.get_block(_cell.z) if cell.value != '.'])
    paradox = row.union(col, block)
    marks = VALID_NUMS.difference(paradox)
    _cell.set_pencil(marks)
    return len(marks)


# --- Solver Functions ---
def last_digit(_board: Board) -> bool:
    '''Solves for the last digit for rows, columns, and blocks until no more progress can be made.
    Returns True if any changes were made to the board.'''
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


def hidden_naked_single(_board:Board) -> bool:
    '''Solves for hidden and naked singles for rows, columns, and blocks until no more progress can be made.
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

# --- Main Functions ---
def solver(_board: Board) -> Board:
    '''Main sudoku solver logic.'''
    iter = 0
    while True:
        print('-')
        print(iter)
        iter += 1
        # Check if solved
        if is_solved(_board):
            print("Board solved!")
            return _board
        changed = []
        # Try all solving techniques
        print("Checking for last digits...")
        changed.append(last_digit(_board))
        print("Checking for naked singles...")
        changed.append(hidden_naked_single(_board))
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
    hiddensingle_data = [
        '.28..7...',
        '.16.83.7.',
        '....2.851',
        '13729....',
        '...73....',
        '....463.7',
        '29..7....',
        '...86.14.',
        '...3..7..']
    
    N = 9
    VALID_NUMS = {str(i) for i in range(1, N + 1)}
    main(N, hiddensingle_data)
