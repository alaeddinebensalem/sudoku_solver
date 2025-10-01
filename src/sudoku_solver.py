from src.constraintMap import ConstraintMap
from src import utils
from src.errors import *


def backtrack_recursive_solver(puzzle: list, limit: int = 2) -> list[list]:
    """
    Solve a Sudoku puzzle using recursive backtracking guided by constraints.

    Args:
        puzzle (list): Flat list of 81 integers representing the Sudoku grid.
                       Empty cells should be 0.
        limit (int, optional): Maximum number of solutions to find. Defaults to 2.

    Returns:
        list[list]: A list of solutions (each solution is a list of 81 integers).
                    Stops when the number of solutions reaches 'limit'.
    """
    if not utils.is_valid_sudoku(puzzle):
        raise InvalidSudokuError
    solutions = []
    cm = ConstraintMap(puzzle)
    def _solve(puzzle, idx):
        if len(solutions) == limit:
            return
        if idx == -1:
            solutions.append(list(puzzle))
            return
        digits = utils.gen_digits(cm[idx])
        for digit in digits:
            puzzle[idx] = digit
            cm.update_neighbors(idx, digit)
            _solve(puzzle, cm.pop_most_constrained_cell())
            cm.update_neighbors(idx, digit, remove= True)
        puzzle[idx] = 0
        cm.update_empty_cells(idx, add= True)
    _solve(puzzle, cm.pop_most_constrained_cell())
    return solutions

def backtrack_iterative_solver(puzzle: list, limit: int = 2) -> list[list]:
    """
    Solve a Sudoku puzzle using an iterative backtracking algorithm guided by constraints.

    Args:
        puzzle (list): Flat list of 81 integers representing the Sudoku grid.
                       Empty cells should be 0.
        limit (int, optional): Maximum number of solutions to find. Defaults to 2.

    Returns:
        list[list]: A list of solutions (each solution is a list of 81 integers).
                    Stops when the number of solutions reaches 'limit'.
    """
    if not utils.is_valid_sudoku(puzzle):
        raise InvalidSudokuError
    solutions = []
    cm = ConstraintMap(puzzle)
    idx = cm.pop_most_constrained_cell()
    indices = [None]*81
    iters = [None]*81
    indices[0] = idx
    iters[0] = utils.gen_digits(cm[idx])
    count = 0
    filled_cell_index = 0
    while filled_cell_index > -1:
        try:
            idx = indices[filled_cell_index]
            if puzzle[idx]:
                cm.update_neighbors(idx, puzzle[idx], remove=True)
            digit = next(iters[filled_cell_index])
            puzzle[idx] = digit
            cm.update_neighbors(idx, digit)
            next_idx = cm.pop_most_constrained_cell()
            if next_idx == -1:
                solutions.append(puzzle.copy())
                count += 1
                if count == limit:
                    return solutions
            else:
                filled_cell_index += 1
                digit_iter = utils.gen_digits(cm[next_idx])
                indices[filled_cell_index] = next_idx
                iters[filled_cell_index] = digit_iter
        except StopIteration:
            indices[filled_cell_index] = None
            iters[filled_cell_index] = None
            filled_cell_index -= 1
            puzzle[idx] = 0
            cm.update_empty_cells(idx, add=True)
    return solutions


