# Sudoku-Solver

## Overview
This project implements a Sudoku solver using constraint satisfaction and backtracking techniques. The solver reads an input Sudoku board from a CSV file and attempts to solve it using a depth-first search (DFS) approach with forward checking and backtracking.

## Features
- Reads and initializes a Sudoku board from a CSV file.
- Implements a board representation tracking values in rows, columns, and boxes.
- Uses constraint propagation to efficiently determine valid moves.
- Implements backtracking and forward checking to improve search efficiency.
- Prints the solved board in a formatted grid.

## Getting Started

### Prerequisites
- Python 3.x

### Running the Solver
To run the solver, execute the following command in a terminal:

```
python3 solver.py <filename.csv>
```

Replace `<filename.csv>` with the path to your Sudoku board file.
Depending on which Python you're using, you may need to replace the ```python3``` command with ```python ``` 

### Input Format
The input Sudoku board must be a CSV file where:
- Each row represents a line of the Sudoku grid.
- Empty spaces are represented by empty cells in the CSV.

Example CSV (4x4 Sudoku):
```
1, , , 4
 , ,3,
 ,2, ,
3, , ,1
```

## Code Structure
### `Board` Class
- **`__init__(filename)`**: Initializes the board by reading a CSV file.
- **`loadSudoku(filename)`**: Reads and processes the board from a CSV file.
- **`print()`**: Displays the board in a readable format.
- **`makeMove(space, value)`**: Places a value on the board.
- **`undoMove(space, value)`**: Removes a value and restores constraints.
- **`isValidMove(space, value)`**: Checks if a move is valid.
- **`getMostConstrainedUnsolvedSpace()`**: Finds the most constrained empty space.

### `Solver` Class
- **`solveBoard(board)`**: Implements DFS with backtracking and forward checking to solve the Sudoku board.

## Example Output
Given the following input:
```
python3 main.py example.csv  
```

The program will output a solved Sudoku board in the terminal.
```
  5  7  3 | 2  6  4 | 8  9  1
  8  1  6 | 3  5  9 | 7  2  4
  9  4  2 | 7  1  8 | 6  5  3
  ---------------------------
  6  8  1 | 9  3  5 | 2  4  7
  2  5  7 | 1  4  6 | 9  3  8
  3  9  4 | 8  7  2 | 1  6  5
  ---------------------------
  7  6  8 | 4  2  3 | 5  1  9
  4  2  9 | 5  8  1 | 3  7  6
  1  3  5 | 6  9  7 | 4  8  2
```

## Notes
- The program raises an exception if the CSV format is incorrect.
- If no solution exists, the board remains unchanged.


