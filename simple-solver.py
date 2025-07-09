"""
Simple soduku solver.
"""

VALID_NUMS = {'1','2','3','4','5','6','7','8','9'}
VALID_INPUT = {'1','2','3','4','5','6','7','8','9', '.'}

class Cell:
    def __init__(self, _x: int, _y: int, _value: str = '.', ) -> None:
        '''Creates a cell with coordinates x,  y and an optional value.'''
        self.x = _x
        self.y =_y
        self.value = _value
    
    def __str__(self) -> str:
        '''Returns cell value as a string.'''
        return str(self.value)
    
    def set(self, _value:str) -> None:
        '''Sets the value of a cell to a new value.'''
        print(f"Setting cell at ({self.x}, {self.y}) to {_value}")
        self.value = _value

class Board:
    def __init__(self) -> None:
        '''Creates an empty board of nine lists of Cells within a list.'''
        self.data = [[Cell(x, y) for x in range(9)] for y in range(9)]
    
    def __str__(self) -> str:
        '''Returns board as space-delineated string with each row as a new line.'''
        board_rows = [' '.join(str(cell) for cell in row) for row in self.data]
        return '\n'.join(board_rows)
    
    def set_cell(self, value:str, x:int, y:int) -> None:
        '''Given coordinates, fills a single cell on the board.'''
        self.data[y][x].set(value)
        
    def set_row(self, values:list, _y:int) -> None:
        '''Given a y-coordinate, fill the row with a list of values.'''
        [self.set_cell(values[i], i, _y) for i in range(9)]
    
    def check_board(self) -> bool:
        '''Checks if board is valid.'''
        for i in range(9):
            row = self.get_row(i)
            col = self.get_col(i)
            block = self.get_block(i)
            for num in VALID_NUMS:
                row_count = row.count(num)
                col_count = col.count(num)
                block_count = block.count(num)
                if row_count > 1 or col_count > 1 or block_count:
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
    
    def solve_one(self, get_group: callable) -> None:
        '''Solves for all of a group (rows, columns, or blocks) that has one cell empty.'''
        assert self.check_board(), f"Error in board!"
        for i in range(9):
            group = get_group(i) # Get group
            empty_cells = [cell for cell in group if cell.value == '.']
            if len(empty_cells) == 1:  # Only one empty cell
                missing_value = VALID_NUMS.difference({cell.value for cell in group}).pop()
                empty_cells[0].set(missing_value)

def init_board(board: Board, data:list) -> None:
    '''Given a board and a list of nine strings of either numbers or ., input list into the board.'''
    # Input checks
    assert len(data) == 9, f"Input data has length {len(data)}."
    assert all(isinstance(item, str) for item in data), f"Input data must contain only strings."
    assert all(len(item) == 9 for item in data), f"Input data must have 9 items in each string."
    for i in range(9):
        rowdata = list(data[i])
        board.set_row(rowdata, i)

board = Board()
unsolved_data = ['...26.7.1',
        '68..7..9.',
        '19...45..',
        '82.1...4.',
        '..46.29..',
        '.5...3.28',
        '..93...74',
        '.4..5..36',
        '7.3.18...']

solved_data = ['435269781',
        '682571493',
        '197834562',
        '826195347',
        '374682915',
        '951743628',
        '519326874',
        '248957136',
        '763418259']

test_data = ['4352697.1',
        '68.571493',
        '197834562',
        '82619.347',
        '374682915',
        '95.743628',
        '519326874',
        '24895.136',
        '763418259']

init_board(board, test_data)
print('---')
print(board)
board.solve_one(board.get_block)
print('---')
print(board)