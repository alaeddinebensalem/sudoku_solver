"""
Benchmarking script for the Sudoku solver.

Measures average, minimum, and maximum solve times for puzzles
stored in a JSON file. Supports limiting the number of puzzles
processed for quick testing.

JSON format expected:
{
    "puzzles": ["003020600...", "060500400...", ...]
}
"""
import json
from typing import Any, Generator
import pathlib

from src import sudoku_solver
from time import perf_counter

def get_puzzle(filename: str) -> Generator[list[int], None, None]:
    """Yields Sudoku puzzles from a JSON file as lists of integers."""
    with open(filename, "r") as f:
        json_data = json.load(f)
        for puzzle_string in json_data["puzzles"]:
            yield [int(cell) for cell in puzzle_string]

def benchmark(filename: str,*, limit: int = float("inf")) -> None:
    """
    Benchmarks the backtrack_iterative_solver on a set of puzzles.

    Args:
        filename (str): Path to the JSON file containing puzzles.
        limit (int, optional): Maximum number of puzzles to solve. Defaults to infinity.

    Prints:
        - Number of puzzles solved
        - Average solve time
        - Minimum solve time
        - Maximum solve time
    """
    total_time = 0
    min_solve = float("inf")
    min_index = -1
    max_solve = 0
    max_index = -1
    count = 0
    for puzzle in get_puzzle(filename):
        count += 1
        start_solve = perf_counter()
        sol =  sudoku_solver.backtrack_iterative_solver(puzzle)
        solve_time = perf_counter() - start_solve
        total_time += solve_time
        if len(sol) > 1:
            print(f"Puzzle {count-1} is not unique.")
        # print(f"Solving puzzle #{count}")
        # print(f"there is {len(sol)} solutions")
        # print()
        if solve_time < min_solve:
            min_solve = solve_time
            min_index = count-1
        if max_solve < solve_time:
            max_solve = solve_time
            max_index = count-1
        if count >= limit:
            break
    print(f"{count} puzzles were solved.")
    print(f"The average solve time is: {total_time/count:.3f} seconds.")
    print(f'The maximum solve time is: {max_solve: 0.3f} seconds for puzzle #{max_index}')
    print(f'The minimum solve time is: {min_solve: 0.3f} seconds for puzzle #{min_index}')

PUZZLE_FILE_17= pathlib.Path(__file__).parent.parent/"data"/ "17_clue_puzzles.json"
if __name__ == '__main__':
    # 500 puzzle benchmark from the Gordon Royle 17-clue puzzle list
    benchmark(PUZZLE_FILE_17, limit=500)

