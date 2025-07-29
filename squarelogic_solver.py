'''
Sudoku solver for the kenken/calcudoku video game Everyday Genius: SquareLogic.
https://store.steampowered.com/app/32150/Everyday_Genius_SquareLogic/
'''
# --- Imports ---
import time
from PIL import Image
import cv2
import numpy as np
import pyautogui
import pytesseract
import pygetwindow

# --- Global variables ---
WINDOW_CAPTURE = "Everyday Genius: SquareLogic"

# --- Classes ---
class Cell:
    '''
    A single sudoku cell with coordinates x, y. '.' indicates an empty cell.
    '''
    def __init__(self, _x: int, _y: int, _value: str = '.', ) -> None:
        '''Creates a cell with coordinates col x, row y, block z, and an optional value.'''
        self.x = _x # col
        self.y =_y # row
        self.value = _value # value
        self.pencil = set() # pencil marks

    def __str__(self) -> str:
        '''Returns cell value as a string.'''
        return str(self.value)

    def set(self, _value:str) -> None:
        '''Sets the value of a cell to a new value.'''
        print(f"INFO: Setting cell at ({self.x}, {self.y}) to {_value}")
        self.value = _value
 
    def set_pencil(self, _marks:set) -> None:
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


# --- Helper functions ---
def show_image(_image: Image) -> None:
    '''Shows image until any button is pressed.'''
    image_cv = np.array(_image) # To numpy
    cv2.imshow("Image Display", image_cv)
    cv2.waitKey(0) # Quit on any button press
    cv2.destroyAllWindows()


# --- Main functions ---
def screenshot_window(_window: str, save: bool = False, save_path: str = './data/sc.png') -> Image:
    '''Given a window program, take a screenshot and save to a path.'''
    try:
        window = pygetwindow.getWindowsWithTitle(_window)[0]
        left, top, width, height = window.left, window.top, window.width, window.height
        window.activate()
        time.sleep(0.5)  # Give time for the window to become active
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        if save:
            screenshot.save(save_path)
            print(f"Screenshot of '{_window}' saved to: {save_path}")
        return screenshot

    except IndexError:
        print(f"Error: Window with title '{_window}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def trim_image(_image: Image) -> Image:
    '''Given an image, trim to sudoku board.'''
    image_cv = np.array(_image) # To numpy
    image_gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY) # To grayscale
    _, thres = cv2.threshold(image_gray, 1, 255, cv2.THRESH_BINARY_INV) # Inverse binary threshold
    countours, _ = cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Find contours
    contours = sorted(countours, key = cv2.contourArea, reverse=True) # Sort to find largest
    # Get bounding box of largest
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w < 100 or h < 100: # Avoid noise contours
            continue
        # Crop
        cropped = image_cv[y:y+h, x:x+w]
        return Image.fromarray(cropped)


def divide_cells(_image: Image):
    '''Divides an image into sudoku cells.'''


def main(_path: str = None) -> None:
    '''Main function.'''
    if path:
        screenshot = Image.open(_path)
    else:
        screenshot = screenshot_window(WINDOW_CAPTURE)
    screenshot = trim_image(screenshot)
    
    show_image(screenshot)


if __name__ == '__main__':
    '''Run at init'''
    path = './data/sc.png'
    N = 4
    VALID_NUMS = {str(i) for i in range(1, N + 1)}
    main(path)
