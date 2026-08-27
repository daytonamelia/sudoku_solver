'''
Board and Cell datamodels and functions.
'''
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

class Cell:
    '''
    A single sudoku cell with coordinates col, row. '.' indicates an empty cell.
    '''
    def __init__(self, col: int, row: int, value: str = '.', ) -> None:
        '''Creates a cell with coordinates (col, row, block), and an optional value.'''
        self.col = col
        self.row = row
        self.block = self.find_block()
        self.value = value
        self.pencil = set()

    def find_block(self) -> int:
        '''Finds which block the cell is in. Returns block number 0-8.'''
        return (self.row // 3) * 3 + (self.col // 3)

    def __str__(self) -> str:
        '''Returns cell value as a string.'''
        return str(self.value)

    def set(self, value:str) -> None:
        '''Sets the value of a cell to a new value.'''
        logger.info("Setting cell at (%d, %d) to %s", self.col, self.row, value)
        self.value = value

    def set_pencil(self, marks: set[str]) -> None:
        '''Update the cell's pencil marks.'''
        self.pencil = marks


class Board:
    '''
    A square sudoku board of nxn Cell objects.
    '''
    def __init__(self, n:int=9) -> None:
        '''Creates an empty square board of n lists of Cells within a list.'''
        self.n = n
        self.valid_nums = {str(i) for i in range(1, n+1)}
        self.data = [[Cell(col, row) for col in range(self.n)] for row in range(self.n)]

    def __str__(self) -> str:
        '''Returns board as space-delineated string with each row as a new line.'''
        board_rows = [' '.join(str(cell) for cell in row) for row in self.data]
        return '\n'.join(board_rows)

    def set_cell(self, value:str, col:int, row:int) -> None:
        '''Given coordinates, fill a single cell on the board.'''
        self.data[row][col].set(value)

    def set_row(self, values:list, row:int) -> None:
        '''Given a row, fill with list of values.'''
        for i in range(self.n):
            self.set_cell(values[i], i, row)

    def check_board(self) -> bool:
        '''Checks if board is valid.'''
        for i in range(self.n):
            row = self.get_row(i)
            col = self.get_col(i)
            block = self.get_block(i)
            for num in self.valid_nums:
                row_count = sum(1 for cell in row if cell.value == num)
                col_count = sum(1 for cell in col if cell.value == num)
                block_count = sum(1 for cell in block if cell.value == num)
                if row_count > 1 or col_count > 1 or block_count > 1:
                    logger.warning("On %s: %d rows, %d cols, %d blocks.",
                                   num, row_count, col_count, block_count)
                    return False
        return True

    def get_cell(self, col:int, row:int) -> Cell:
        '''Returns a Cell from coordinates.'''
        return self.data[row][col]

    def get_row(self, row: int) -> list:
        '''Returns a row as a list of Cell objects.'''
        return self.data[row]

    def get_col(self, col: int) -> list:
        '''Returns a column as a list of Cell objects.'''
        return [row[col] for row in self.data]

    def get_block(self, n: int) -> list:
        '''
        Returns a block as a list of Cell objects. 
        Z must be between 0-8 inclusive and starts from top-left of the board.
        '''
        start_row = (n // 3) * 3
        start_col = (n % 3) * 3
        return [self.data[row][col]
                for row in range(start_row, start_row + 3)
                for col in range(start_col, start_col + 3)]


def init_board(board: Board, data:list) -> None:
    '''Fills board with either numbers or .'''
    # Input checks
    assert len(data) == board.n, \
        f"Input data has length {len(data)}."
    assert all(isinstance(item, str) for item in data), \
        "Input data must contain only strings."
    assert all(len(item) == board.n for item in data), \
        f"Input data must have {board.n} items in each string."
    logger.info("Setting board...")
    for i in range(board.n):
        rowdata = list(data[i])
        board.set_row(rowdata, i)


def is_solved(board: Board) -> bool:
    '''Checks if board is solved (no empty cells and valid).'''
    assert board.check_board(), f"Error in board!\n{board}"
    return not any(cell.value == '.' for row in board.data for cell in row)


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
    result = []
    for i, s in enumerate(in_list):
        unique_in_set = {value for value in s if value_counts[value] == 1}
        if unique_in_set:
            result.append((i, unique_in_set))
    return result
