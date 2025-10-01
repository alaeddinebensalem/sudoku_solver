"""
Custom exceptions for the Sudoku solver.

"""
# Raised when a Sudoku rule is violated.
class InvalidSudokuError(Exception):
    pass

# Raised when a cell exceeds the maximum number of constraints.
class ExceededNumConstraintsError(Exception):
    pass