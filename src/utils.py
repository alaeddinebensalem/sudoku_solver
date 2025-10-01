"""
Utility functions for Sudoku constraint management and grid handling.

Provides helper functions for:
- Converting between cell indices and (row, column, box) coordinates.
- Generating neighbor cell sets for constraint propagation.
- Iterating over available digits from a cell's bitmask.
- Counting constraints encoded in a cell's bitmask.
- Printing Sudoku grids in a readable format.
"""

from src.constants import *
from src.errors import *

def get_coord(cell: int) -> tuple[int, int, int]:
    """
    Return the row, column, and box indices for a given cell in a Sudoku grid.
    Args:
        cell (int): The index of the cell in a flat list (0–SUDOKU_SIZE**2-1).
    Returns:
        tuple[int, int, int]: A tuple containing:
            - row (int): Row index of the cell.
            - column (int): Column index of the cell.
            - box (int): Box index of the cell.
    """
    row = cell // SUDOKU_LENGTH
    col = cell % SUDOKU_LENGTH
    box = BOX_LENGTH * (cell // (BOX_LENGTH*SUDOKU_LENGTH)) + (cell % SUDOKU_LENGTH) // BOX_LENGTH
    return row, col, box

def gen_neighbor_cells():
    """
    Generate the neighbor cells for each cell in a Sudoku grid.
    Each cell's neighbors are all other cells in the same row, column, or box,
    excluding the cell itself.

    Returns:
        dict[int, set[int]]: A dictionary mapping each cell index (0–SUDOKU_SIZE-1)
        to a set of indices representing its neighbors.
    """
    row_map = [set() for _ in range(SUDOKU_LENGTH)]
    col_map = [set() for _ in range(SUDOKU_LENGTH)]
    box_map = [set() for _ in range(SUDOKU_LENGTH)]
    for cell in range(SUDOKU_SIZE):
        row, col, box = get_coord(cell)
        row_map[row].add(cell)
        col_map[col].add(cell)
        box_map[box].add(cell)
    neighbor_cells = {}
    for cell in range(SUDOKU_SIZE):
        row, col, box = get_coord(cell)
        neighbor_cells[cell] = (row_map[row] | col_map[col] | box_map[box]) - {cell}
    return neighbor_cells

def is_valid_sudoku(puzzle: list[int]) -> bool:
    """
    Check if a Sudoku puzzle is valid.

    A puzzle is valid if no two identical numbers appear
    in the same row, column, or 3x3 box.

    Args:
        puzzle: A flat list of 81 integers (0 = empty, 1–9 = digits).

    Returns:
        True if the puzzle is valid, False otherwise.
    """
    neighbors = NEIGHBOR_MAP
    for cell, val in enumerate(puzzle):
        if val: # ignore empty cells
            if any(val == puzzle[neighbor] for neighbor in neighbors[cell]):
                return False
    return True


def gen_digits(bitmask: int):
    """
    Yield all digits from 1 to 9 that are not yet constrained in a cell.
    Each cell's constraints are encoded in a bitmask, where each 2-bit field
    represents the number of constraints for the corresponding digit. A field
    value of less than 3 indicates the digit is available.

    Args:
    bitmask (int): The bitmask encoding the cell's digit constraints.

    Yields:
    int: Each unconstrained digit from 1 to 9, in ascending order.
    """
    bitmask >>= DIGIT_SHIFT
    for i in range(1,10):
        if bitmask& 0b11 == 0:
            yield i
        bitmask >>= DIGIT_MASK

def num_constraints(bitmask: int) -> int:
    """
    Return the number of constrained digits in a cell.

    Args:
        bitmask (int): The cell's constraint bitmask.
    Returns:
        int: Number of constrained digits.
    Raises:
        ExceededNumConstraintsError: If the count exceeds maximum number of constrained digits.
    """
    mask = COUNT_OF_DIGITS
    res = bitmask&mask
    if res > SUDOKU_LENGTH:
        raise ExceededNumConstraintsError
    return bitmask&mask

def print_grid(grid: list[int]):
    """
    Print a Sudoku grid in a 9x9 format.

    Args:
        grid (list[int]): Flat list of 81 integers representing the Sudoku grid.
    """
    for i in range(SUDOKU_SIZE):
        if i % SUDOKU_LENGTH == 0:
            print()
        print(grid[i], end=" ")
    print()


