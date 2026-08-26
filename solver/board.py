'''
Board and Cell datamodels and functions.
'''
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

VALID_NUMS = {str(i) for i in range(1, 10)}

class Cell:
    '''
    A single sudoku cell with coordinates x, y. '.' indicates an empty cell.
    '''
    def __init__(self, _x: int, _y: int, _value: str = '.', ) -> None:
        '''Creates a cell with coordinates col x, row y, block z, and an optional value.'''
        self.x = _x # col
        self.y =_y # row
        self.z = self.find_block() # block
        self.value = _value # value
        self.pencil = set() # pencil marks

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
        logger.info("Setting cell at (%d, %d) to %s", self.x, self.y, _value)
        self.value = _value

    def set_pencil(self, _marks: set[str]) -> None:
        '''Update the cell's pencil marks.'''
        self.pencil = _marks


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
                    logger.warning("On %s: %d rows, %d cols, %d blocks.", num, row_count, col_count, block_count)
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

def init_board(board_obj: Board, data:list) -> None:
    '''Fills board with either numbers or .'''
    # Input checks
    assert len(data) == board_obj.n, \
        f"Input data has length {len(data)}."
    assert all(isinstance(item, str) for item in data), \
        "Input data must contain only strings."
    assert all(len(item) == board_obj.n for item in data), \
        "Input data must have 9 items in each string."
    logger.info("Setting board...")
    for i in range(board_obj.n):
        rowdata = list(data[i])
        board_obj.set_row(rowdata, i)


def is_solved(_board: Board) -> bool:
    '''Checks if board is solved (no empty cells and valid).'''
    assert _board.check_board(), f"Error in board!\n{_board}"
    return not any(cell.value == '.' for row in _board.data for cell in row)


def count_list_of_sets(in_list:list) -> dict:
    '''Given a list of sets, find the occurence of each value.'''
    value_counts = {}
    for s in in_list:
        for value in s:
            value_counts[value] = value_counts.get(value, 0) + 1
    return value_counts


def find_unique_set_values(in_list: list) -> list:
    '''Given a list of sets, find the index and values of sets with unique values.'''
    value_counts = count_list_of_sets(in_list)
    # Find sets that contain unique values
    result = []
    for i, s in enumerate(in_list):
        unique_in_set = {value for value in s if value_counts[value] == 1}
        if unique_in_set:
            result.append((i, unique_in_set))
    return result
