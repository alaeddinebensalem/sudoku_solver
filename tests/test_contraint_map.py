import unittest

from src.errors import *
from src.constraintMap import ConstraintMap

class TestConstraint(unittest.TestCase):

    def setUp(self):
        self.cm = ConstraintMap()

    def tearDown(self):
        pass

    def test_update_neighbors(self):
        self.cm.update_constraint_map([0]*81)
        # Testing adding constraints
        self.cm.update_neighbors(0, 9)
        self.assertEqual(self.cm[1], 0b0100000000000000000001,
                         f"expected {0b0100000000000000000001:#b}, got {self.cm._cmap[1]:#b}")
        self.cm.update_neighbors(0, 9)
        self.assertEqual(self.cm[1], 0b1000000000000000000001,
                         f"expected {0b1000000000000000000001:#b}, got {self.cm._cmap[1]:#b}")
        self.cm.update_neighbors(0, 9)
        self.assertEqual(self.cm[1], 0b1100000000000000000001,
                         f"expected {0b1100000000000000000001:#b}, got {self.cm._cmap[1]:#b}")
        # Testing forcing error
        with self.assertRaises(InvalidSudokuError):
            self.cm.update_neighbors(1, 9)
        # Testing removing constraints
        self.cm.update_neighbors(0, 9, remove=True)
        self.assertEqual(self.cm[1], 0b1000000000000000000001,
                         f"expected {0b1000000000000000000001:#b}, got {self.cm._cmap[1]:#b}")
        self.cm.update_neighbors(0, 9, remove=True)
        self.assertEqual(self.cm[1], 0b100000000000000000001,
                         f"expected {0b100000000000000000001:#b}, got {self.cm._cmap[1]:#b}")
        self.cm.update_neighbors(0, 9, remove=True)
        self.assertEqual(self.cm[1], 0b000000000000000000000,
                         f"expected {0b000000000000000000000:#b}, got {self.cm._cmap[1]:#b}")
        # Testing forcing error
        with self.assertRaises(InvalidSudokuError):
            self.cm.update_neighbors(1, 9, remove= True)

    def test_update_constraintMap(self):
        # Testing that update method works correctly for an empty puzzle
        puzzle = [0]*81
        expected_map = [0] * 81
        self.cm.update_constraint_map(puzzle)
        self.assertListEqual(self.cm._cmap, expected_map)

        # Testing that update method works correctly for a partially filled puzzle
        puzzle[0] = 1
        puzzle[8] = 3
        puzzle[50] = 3
        #updating the expected constraint map for digit 1
        for i in [9,10,11,18,19,20,27,36,54,63,72]:
            expected_map[i] = 0b10001
        # updating the expected constraint map for digit 3
        for i in [14,15,16,17,23,24,25,26,30,31,32,35,39,40,41,44,46,47,48,49,51,52,59,62,68,71,77,80]:
            expected_map[i] = 0b100000001
        # updating the expected constraint map for digits 1 and 3
        for i in [1,2,3,4,6,7,45]:
            expected_map[i] =0b100010010
        # updating the expected constraint map for the overlap of 1 and 3 and 3
        expected_map[5] = 0b1000010010
        # updating the expected constraint map for the overlap of 3 and 3
        expected_map[53] = 0b1000000001
        self.cm.update_constraint_map(puzzle)
        self.assertListEqual(self.cm._cmap, expected_map)
        empty_cells = set(i for i in range(81))
        empty_cells.difference_update({0,8,50})
        self.assertSetEqual(self.cm._empty_cells, empty_cells)

    def test_pop_most_constrained_cell(self):
        puzzle = [0]*81
        puzzle[0] = 1
        puzzle[8] = 3
        puzzle[50] = 3
        puzzle[41] = 4
        # cell 5 has the most amount of constraints: 1,3 and 5.
        self.cm.update_constraint_map(puzzle)
        self.assertEqual(self.cm.pop_most_constrained_cell(), 5)
        empty_cells = set(i for i in range(81))
        empty_cells.difference_update({0, 8, 50, 41, 5})
        self.assertSetEqual(self.cm._empty_cells, empty_cells)







