# High-Performance Sudoku Solver

**Author:** Alaeddine Ben Salem | **Email:** alaedbensalem@gmail.com  
**GitHub:** [github.com/alaeddinebensalem](https://github.com/alaeddinebensalem)

## Description
A Python Sudoku solver implementing **backtracking** with **bitmask-based constraint propagation** and a **most-constrained cell search heuristic** for optimized search.

## How to Run

1. Clone the repository.
2. Import `backtrack_iterative_solver` or `backtrack_recursive_solver` from `src.sudoku_solver`.
3. Run the solver on a puzzle.  
   **Puzzle format:** flat list with length 81, with `0` representing empty cells.
   
## Benchmarking the Sudoku Solver

The `benchmark` folder contains scripts to measure the performance of the solver.

### Benchmark Results (17-Clue Puzzles)

- Number of puzzles tested: 1000  
- Average solve time: 0.233 seconds  
- Minimum solve time: 0.003 seconds  
- Maximum solve time: 3.875 seconds  
