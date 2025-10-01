import unittest
from src.errors import *
from src import sudoku_solver

class TestSudokuSolver(unittest.TestCase):
    def setUp(self):
        self.valid_puzzle = [0, 0, 0, 2, 6, 0, 7, 0, 1, 6, 8, 0, 0, 7, 0, 0, 9, 0, 1, 9, 0, 0, 0, 4, 5, 0, 0, 8, 2, 0, 1, 0,
                        0, 0, 4, 0, 0, 0, 4, 6, 0, 2, 9, 0, 0, 0, 5, 0, 0, 0, 3, 0, 2, 8, 0, 0, 9, 3, 0, 0, 0, 7, 4, 0,
                        4, 0, 0, 5, 0, 0, 3, 6, 7, 0, 3, 0, 1, 8, 0, 0, 0]
        self.solution = [4, 3, 5, 2, 6, 9, 7, 8, 1, 6, 8, 2, 5, 7, 1, 4, 9, 3, 1, 9, 7, 8, 3, 4, 5, 6, 2, 8, 2, 6, 1, 9, 5,
                    3, 4, 7, 3, 7, 4, 6, 8, 2, 9, 1, 5, 9, 5, 1, 7, 4, 3, 6, 2, 8, 5, 1, 9, 3, 2, 6, 8, 7, 4, 2, 4, 8,
                    9, 5, 7, 1, 3, 6, 7, 6, 3, 4, 1, 8, 2, 5, 9]

    def test_backtrack_recursive_solver(self):

        tested_solution = sudoku_solver.backtrack_recursive_solver(self.valid_puzzle)
        self.assertEqual( len(tested_solution), 1)
        self.assertListEqual(tested_solution[0], self.solution)

        invalid_puzzle = [2, 0, 0, 2, 6, 0, 7, 0, 1, 6, 8, 0, 0, 7, 0, 0, 9, 0, 1, 9, 0, 0, 0, 4, 5, 0, 0, 8, 2, 0, 1,
                          0, 0, 0, 4, 0, 0, 0, 4, 6, 0, 2, 9, 0, 0, 0, 5, 0, 0, 0, 3, 0, 2, 8, 0, 0, 9, 3, 0, 0, 0, 7,
                          4, 0, 4, 0, 0, 5, 0, 0, 3, 6, 7, 0, 3, 0, 1, 8, 0, 0, 0]
        with self.assertRaises(InvalidSudokuError):
            sudoku_solver.backtrack_recursive_solver(invalid_puzzle)

    def test_backtrack_iterative_solver(self):
        tested_solution = sudoku_solver.backtrack_iterative_solver(self.valid_puzzle)
        self.assertEqual(len(tested_solution), 1)
        self.assertListEqual(tested_solution[0], self.solution)

        invalid_puzzle = [2, 0, 0, 2, 6, 0, 7, 0, 1, 6, 8, 0, 0, 7, 0, 0, 9, 0, 1, 9, 0, 0, 0, 4, 5, 0, 0, 8, 2, 0, 1, 0,
                        0, 0, 4, 0, 0, 0, 4, 6, 0, 2, 9, 0, 0, 0, 5, 0, 0, 0, 3, 0, 2, 8, 0, 0, 9, 3, 0, 0, 0, 7, 4, 0,
                        4, 0, 0, 5, 0, 0, 3, 6, 7, 0, 3, 0, 1, 8, 0, 0, 0]
        with self.assertRaises(InvalidSudokuError):
            sudoku_solver.backtrack_iterative_solver(invalid_puzzle)