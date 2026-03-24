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
    # Check puzzle validity
    if not utils.is_valid_sudoku(puzzle):
        raise InvalidSudokuError
    solutions = []
    # Initialize Constraint map
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
    # Check puzzle validity
    if not utils.is_valid_sudoku(puzzle):
        raise InvalidSudokuError

    solutions = []
    # Initialize Constraint map
    cm = ConstraintMap(puzzle)
    # Get most constrained cell
    idx = cm.pop_most_constrained_cell()
    # Initialize synchronized lists for index and iterator of the tested cell
    indices = [None]*81
    iters = [None]*81
    indices[0] = idx
    iters[0] = utils.gen_digits(cm[idx])
    count = 0
    depth = 0
    # depth is equal -1 when the first inserted iterator is exhausted and all paths have been tested.
    # end loop organically when all paths are tested
    while depth > -1:
        try:
            # get last index in the stack
            idx = indices[depth]
            # Undo constraint map changes for previously tested digit in that cell idx
            if puzzle[idx]:
                cm.update_neighbors(idx, puzzle[idx], remove=True)
            # get the next possible digit
            digit = next(iters[depth])
            # insert digit into cell and update constraint map
            puzzle[idx] = digit
            cm.update_neighbors(idx, digit)
            # get most constrained empty cell
            next_idx = cm.pop_most_constrained_cell()
            # cm.pop_most_constrained_cell returns -1 if no more empty cells exist: completion condition.
            if next_idx == -1:
                # update solutions and the count of solutions
                solutions.append(puzzle.copy())
                count += 1
                if count == limit:
                    return solutions
            # If there are remaining empty cells
            else:
                depth += 1
                digit_iter = utils.gen_digits(cm[next_idx])
                indices[depth] = next_idx
                iters[depth] = digit_iter
        # If the current iterator is exhausted
        except StopIteration:
            indices[depth] = None
            iters[depth] = None
            depth -= 1
            puzzle[idx] = 0
            cm.update_empty_cells(idx, add=True)
    return solutions
