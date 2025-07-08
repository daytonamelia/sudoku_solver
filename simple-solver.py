"""
Simple soduku solver.
"""

VALID_NUMS = {'1','2','3','4','5','6','7','8','9'}
VALID_INPUT = {'1','2','3','4','5','6','7','8','9', '.'}

class Board:
    def __init__(self) -> None:
        '''Creates an empty board of 9 lists within a list.'''
        self.data = []
        for row in range(9):
            self.data.append([])
    
    def init_cell(self, value:str, x:int, y:int) -> None:
        '''Given coordinates, fills a single cell on the board.'''
        self.data[y][x] = value
        
    def init_row(self, values:list, y:int) -> None:
        '''Given a y-coordinate, fill the row with a list of values.'''
        self.data[y] = values
    
    def __str__(self) -> str:
        '''Returns board as space-delineated string with each row as a new line.'''
        board_rows = [' '.join(row) for row in self.data]
        return '\n'.join(board_rows)
    
    def blank(self) -> None:
        '''Blanks the board with an empty '.' in every spot.'''
        for row in range(9):
            self.data[row] = ['.' for cell in range(9)]
    
    def get_row(self, y:int) -> list:
        '''Returns a row as a list.'''
        return self.data[y]
    
    def get_col(self, x:int) -> list:
        '''Returns a column as a list.'''
        return [row[x] for row in self.data]
    
    def get_block(self, z:int) -> list:
        '''Returns a block as a list. Z must be between 0-8 inclusive and starts from top-left of the board.'''
        block = []
        row_index = {0: [0,1,2],
                     1: [0,1,2],
                     2: [0,1,2],
                     3: [3,4,5],
                     4: [3,4,5],
                     5: [3,4,5],
                     6: [6,7,8],
                     7: [6,7,8],
                     8: [6,7,8]}
        col_index = {0: [0,1,2],
                     1: [3,4,5],
                     2: [6,7,8],
                     3: [0,1,2],
                     4: [3,4,5],
                     5: [6,7,8],
                     6: [0,1,2],
                     7: [3,4,5],
                     8: [6,7,8]}
        rows = [self.get_row(i) for i in row_index[z]]
        for row in rows:
            for i in col_index[z]:
                block.append(row[i])
        return block
    
    def check_board(self) -> bool:
        '''Checks if board is valid.'''
        for i in range(9):
            row = self.get_row(i)
            col = self.get_col(i)
            block = self.get_block(i)
            for num in VALID_NUMS:
                if row.count(num) > 1 or col.count(num) > 1 or block.count(num):
                    return False
        return True
    
    def solve_one(self) -> bool:
        '''Solves for any row, column, or block that has one cell empty.'''
        if not self.check_board: # There's an error!
            return False
        for i in range(9):
            # SOLVE ROW
            row = self.get_row(i)
            if row.count('.') == 1:
                value = VALID_NUMS.difference(set(row)).pop() # get the missing value
                x = row.index(".")
                y = i
                self.init_cell(value,x,y)
            # SOLVE COL
            col = self.get_col(i)
            if col.count('.') == 1:
                value = VALID_NUMS.difference(set(col)).pop() # get the missing value
                x = i
                y = col.index(".")
                self.init_cell(value,x,y)
            # SOLVE BLOCK
            block = self.get_block(i)
            if block.count('.') == 1:
                index = block.index(".")
                value = VALID_NUMS.difference(set(block)).pop() # get the missing value
                x = (i%3)*3 + (index%3)
                y = (i//3)*3 + (index//3)
                self.init_cell(value,x,y)
        return True

def init_board(board: Board, data:list) -> None:
    '''Given a board and a list of 9 strings of either 9 numbers or . to input into the board.'''
    # Input checks
    assert len(data) == 9, f"Input data has length {len(data)}."
    assert all(isinstance(item, str) for item in data), f"Input data must contain only strings."
    assert all(len(item) == 9 for item in data), f"Input data must have 9 items in each string."
    for i in range(9):
        rowdata = list(data[i])
        board.init_row(rowdata, i)

board = Board()
board.blank()
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
board.solve_one()
print('---')
print(board)