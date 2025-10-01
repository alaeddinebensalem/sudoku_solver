import unittest
from src import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_coord(self):
        self.assertEqual(utils.get_coord(0), (0, 0, 0))
        self.assertEqual(utils.get_coord(80), (8, 8, 8))
        self.assertEqual(utils.get_coord(31), (3, 4, 4))
        self.assertEqual(utils.get_coord(22), (2, 4, 1))

    def test_gen_neighbor_cells(self):
        neighbors = utils.gen_neighbor_cells()
        neighbor_of_37 = {36, 38, 39, 40, 41, 42, 43, 44, 1, 10, 19, 28, 46, 55, 64, 73, 27, 29, 45, 47}
        self.assertSetEqual(neighbors[37], neighbor_of_37)

    def test_is_valid_sudoku(self):
        valid_sudoku = [4,3,0,0,7,0,0,0,0,
                        6,0,0,1,9,4,0,0,0,
                        0,9,8,0,0,0,0,6,0,
                        8,0,0,0,6,0,0,0,3,
                        5,0,0,8,0,3,0,0,1,
                        7,0,0,0,2,0,0,0,6,
                        0,6,0,0,0,0,2,8,0,
                        0,0,0,5,1,9,0,0,4,
                        0,0,0,0,8,0,0,7,9]
        invalid_sudoku =   [9,3,0,0,7,0,0,0,0,
                            5,0,0,1,8,6,0,0,0,
                            0,8,9,0,0,0,0,5,0,
                            9,0,0,0,5,0,0,0,3,
                            4,0,0,9,0,3,0,0,1,
                            7,0,0,0,2,0,0,0,5,
                            0,5,0,0,0,0,2,9,0,
                            0,0,0,4,1,8,0,0,6,
                            0,0,0,0,9,0,0,7,8]
        self.assertTrue(utils.is_valid_sudoku(valid_sudoku))
        self.assertFalse(utils.is_valid_sudoku(invalid_sudoku))

    def test_gen_digits(self):
        bitmask1 = 0b0 # all digits are available
        bitmask2 = 0b1111111111111111111001 # no digits available
        bitmask3 = 0b0011111111110011000101# 1, 3 and 9 are available

        self.assertListEqual(list(utils.gen_digits(bitmask1)), [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertListEqual(list(utils.gen_digits(bitmask2)), [])
        self.assertListEqual(list(utils.gen_digits(bitmask3)), [1, 3, 9])

        
    
