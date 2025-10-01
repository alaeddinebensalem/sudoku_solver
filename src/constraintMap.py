from src.errors import *
from src.constants import *


class ConstraintMap:
    """
    Represents Sudoku cell constraints using a bitmask.

    Bitmask layout for each cell:
        - Lowest 4 bits: total number of constrained digits
        - Each subsequent 2-bit field: constraint count for digits 1–9

    Attributes:
        _cmap (list[int]): Bitmask for each cell.
        neighbors (list[set[int]]): Neighbor indices for each cell (row, column, box).
    """

    neighbors = None

    def __init__(self, puzzle: list[int]= None):
        """
        Initialize solver state with a puzzle.

        Sets up `_cmap`, `_empty_cells`, and neighbor relations.
        Populates constraints if a puzzle is provided.
        """
        self._cmap = [0] * SUDOKU_SIZE  # the internal constraints map
        self._empty_cells = set()  # the set of empty cells within the puzzle
        self._neighbors = NEIGHBOR_MAP
        if puzzle:
            self.update_constraint_map(puzzle)

    def __getitem__(self, index: int) -> int:
        """
        Get the bitmask of the constraints for a cell.
        Args:
            index (int): Index of the cell.
        Returns:
            int: Bitmask representing the constraints for the cell.
        """
        return self._cmap[index]

    def _get_index_most_constrained(self) -> int:
        """
        Find the index of the most constrained empty cell.

        Returns the index of a cell with 8 constrained digits immediately
        (only one candidate left). Returns -1 if no empty cells remain.
        """
        max_digits = 0
        max_index = -1
        for i in self._empty_cells:
            num_digits = self._cmap[i] & COUNT_OF_DIGITS
            if num_digits == SUDOKU_LENGTH - 1:
                return i
            elif num_digits > max_digits:
                max_digits = num_digits
                max_index = i
        return max_index

    def update_empty_cells(self, index: int, *, add: bool = False):
        """
        Update the set of empty cells.
        Arg:
            index (int): The cell index to add or remove.
        Kwarg:
            add (bool, optional): If True, the index is added.
            If False, the index is removed (unless index == -1).
            Defaults to False.
        Raises:
            IndexError: If `add=True` and index is not in [0, 80].
        """
        if add:
            if 80 < index or index < 0:
                raise IndexError("index out of range")
            self._empty_cells.add(index)
        elif index != -1:
            self._empty_cells.discard(index)

    def pop_most_constrained_cell(self) -> int:
        """
        Return and remove the most constrained empty cell.

        Uses `_get_index_most_constrained` to select the cell and then
        removes it from `self._empty_cells`. Returns -1 if no valid cell.
        """
        max_index = self._get_index_most_constrained()
        self.update_empty_cells(max_index)
        return max_index

    def _add_constraint_neighbor(self, idx: int, val: int):
        """
        Increment the constraint count for digit 'val' in neighbor cell 'idx'.

        If 'val' was not previously constrained, the total number of constrained
        digits in the cell is incremented.

        Args:
            idx (int): Index of the neighbor cell.
            val (int): Digit to add to constraints.

        Raises:
            InvalidSudokuError: If the digit would exceed the maximum allowed constraints.
        """
        mask = self._cmap[idx]
        dig_mask = (mask >> (DIGIT_MASK * (val - 1) + DIGIT_SHIFT)) & 0b11
        if dig_mask < 3:
            dig_mask += 1
        else:
            raise InvalidSudokuError(f"Cell {idx} exceeded number of constraints for digit {val}")
        mask += 1 << (DIGIT_MASK * (val - 1) + DIGIT_SHIFT)
        if dig_mask == 1:
            mask += 1
        self._cmap[idx] = mask

    def _remove_constraint_neighbor(self, idx: int, val: int):
        """
        Decrement the constraint count for digit 'val' in neighbor cell 'idx'.

        If 'val' had only one constraint, the total number of constrained digits
        in the cell is decremented.

        Args:
            idx (int): Index of the neighbor cell.
            val (int): Digit to remove from constraints.

        Raises:
            InvalidSudokuError: If the digit has no existing constraints.
        """
        mask = self._cmap[idx]
        dig_mask = (mask >> (DIGIT_MASK * (val - 1) + DIGIT_SHIFT)) & 0b11
        if dig_mask > 0:
            dig_mask -= 1
        else:
            #print(bin(self._cmap[idx]))
            raise InvalidSudokuError(f"Cell {idx} has no constraints for digit {val}")
        mask -= 1 << (DIGIT_MASK * (val - 1) + DIGIT_SHIFT)
        if dig_mask == 0:
            mask -= 1
        self._cmap[idx] = mask

    def update_neighbors(self, idx: int, val: int, remove: bool = False):
        """
        Update constraints for all empty neighbors of a cell.
        Skips neighbors that are not in _empty_cells.

        Args:
            idx (int): Index of the cell whose neighbors will be updated.
            val (int): Digit to add or remove from neighbor constraints.
            remove (bool, optional): If True, remove the constraint; otherwise add. Defaults to False.
        """
        for i in self._neighbors[idx]:
            if i not in self._empty_cells:
                continue
            if remove:
                self._remove_constraint_neighbor(i, val)
            else:
                self._add_constraint_neighbor(i, val)

    def update_constraint_map(self, puzzle: list):
        """
        Initialize or refresh the constraint map from a Sudoku puzzle.
        For each non-empty cell, adds its value as a constraint to all empty neighbors.

        Args:
           puzzle (list): Flat list of 81 integers representing the Sudoku grid.
        """
        self._empty_cells = {i for i in range(SUDOKU_SIZE)}
        for idx, val in enumerate(puzzle):
            if not val:
                continue
            self._empty_cells.remove(idx)
            if 0 < val <= SUDOKU_LENGTH:
                for i in self._neighbors[idx]:
                    if not puzzle[i]:
                        self._add_constraint_neighbor(i, val)
