import csv
import itertools
import sys

class Board():

    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self, filename):

        # Initialize all of the variables
        self.n2 = 0 # Length of board
        self.n = 0 # Length of board square
        self.spaces = 0 # Total cells in board
        self.board = None # Mapping dictionary
        self.valsInRows = None # Mapping values to row index
        self.valsInCols = None # Mapping values to column index
        self.valsInBoxes = None # Mapping values to cell
        self.unsolvedSpaces = None # Empty spaces on board

        # Load the file and initialize the in-memory board with the data
        self.loadSudoku(filename)


    # Loads the sudoku board from the given file
    def loadSudoku(self, filename):

        with open(filename) as csvFile:
            self.n = -1
            reader = csv.reader(csvFile)
            for row in reader:

                # Assign the n value and construct the approriately sized dependent data
                if self.n == -1:
                    self.n = int(len(row) ** (1/2))
                    if not self.n ** 2 == len(row):
                        raise Exception('Each row must have n^2 values! (See row 0)')
                    else:
                        self.n2 = len(row)
                        self.spaces = self.n ** 4
                        self.board = {}
                        self.valsInRows = [set() for _ in range(self.n2)]
                        self.valsInCols = [set() for _ in range(self.n2)]
                        self.valsInBoxes = [set() for _ in range(self.n2)]
                        self.unsolvedSpaces = set(itertools.product(range(self.n2), range(self.n2)))

                # Check if each row has the correct number of values
                else:
                    if len(row) != self.n2:
                        raise Exception('Each row must have the same number of values. (See row ' + str(reader.line_num - 1) + ')')

                # Add each value to the correct place in the board; record that the row, col, and box contains value
                for index, item in enumerate(row):
                    if not item == '':
                        self.board[(reader.line_num-1, index)] = int(item)
                        self.valsInRows[reader.line_num-1].add(int(item))
                        self.valsInCols[index].add(int(item))
                        self.valsInBoxes[self.spaceToBox(reader.line_num-1, index)].add(int(item))
                        self.unsolvedSpaces.remove((reader.line_num-1, index))


    ##########################################
    ####   Utility Functions
    ##########################################

    # Converts a given row and column to its inner box number
    def spaceToBox(self, row, col):
        return self.n * (row // self.n) + col // self.n

    # Prints out a command line representation of the board
    def print(self):
        for r in range(self.n2):
            # add row divider
            if r % self.n == 0 and not r == 0:
                if self.n2 > 9:
                    print("  " + "----" * self.n2)
                else:
                    print("  " + "---" * self.n2)

            row = ""

            for c in range(self.n2):

                if (r,c) in self.board:
                    val = self.board[(r,c)]
                else:
                    val = None

                # Add column divider
                if c % self.n == 0 and not c == 0:
                    row += " | "
                else:
                    row += "  "

                # Add value placeholder
                if self.n2 > 9:
                    if val is None: row += "__"
                    else: row += "%2i" % val
                else:
                    if val is None: row += "_"
                    else: row += str(val)
            print(row)


    ##########################################
    ####   Move Functions 
    ##########################################

    # Makes a move, records it in its row, col, and box, and removes the space from unsolvedSpaces
    def makeMove(self, space, value):
        r , c = space # Row, col index
        b = self.spaceToBox(r, c) # Box index
        
        self.board[space] = value # Adds move to board
        self.valsInRows[r].add(value) # Adds move to rows
        self.valsInCols[c].add(value) # Adds move to cols
        self.valsInBoxes[b].add(value) # Adds move to box
        self.unsolvedSpaces.remove(space) # Remove from unsolved

    # Removes the move, its record in its row, col, and box, and adds the space back to unsolvedSpaces
    def undoMove(self, space, value):
        r , c = space # Row, col index
        b = self.spaceToBox(r, c) # Box index
        
        self.board.pop(space) # Removes move
        self.valsInRows[r].remove(value) # Removes move from rows
        self.valsInCols[c].remove(value) # Removes move from cols
        self.valsInBoxes[b].remove(value) # Removes move from box
        self.unsolvedSpaces.add(space) # Add to unsolved

    # Returns True if the space is empty and on the board,
    # and assigning value to it if not blocked by any constraints
    def isValidMove(self, space, value):
        r , c = space # Row, col index
        b = self.spaceToBox(r, c) # Box index
                
        if ( 0 <= r < self.n2  and 0 <= c < self.n2): # On the board
            if (space not in self.board and 0 < value <= self.n2): # Space is empty and value is valid
                row = self.valsInRows[r] # Current values in row
                col = self.valsInCols[c] # Current values in col
                square = self.valsInBoxes[b] # Current values in box
                
                check = [row, col, square]
                
                if any(value in arr for arr in check): # Doesn't pass constraints
                    return False
                else: 
                    return True
        
        return False

    # Helper function for getMostConstrainedUnsolvedSpace
    def evaluateSpace(self, space):
        r , c = space # Row, col index
        b = self.spaceToBox(r, c) # Box index
           
        # Returns all possible values that are not already taken up by the row/col/box
        return {val for val in range(1, self.n2 + 1) if val not in self.valsInRows[r] and
            val not in self.valsInCols[c] and val not in self.valsInBoxes[b]}

    # Gets the unsolved space with the most current constraints
    # Returns None if unsolvedSpaces is empty
    def getMostConstrainedUnsolvedSpace(self):
        if len(self.unsolvedSpaces) == 0:
            return None 
        
        return min(self.unsolvedSpaces, key = lambda space: len(self.evaluateSpace(space)))
                
                
class Solver:
    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self):
        pass

    ##########################################
    ####   Solver
    ##########################################

    # Recursively selects the most constrained unsolved space and attempts
    # to assign a value to it

    # Upon completion, it will leave the board in the solved state (or original
    # state if a solution does not exist)

    # Returns True if a solution exists and False if one does not
    def solveBoard(self, board):
        # Returns list of local spaces related by constraints          
        def getRelatedSpaces(space):
            r , c = space
            b = board.spaceToBox(r, c) # Box index
            
            # Related spaces
            row = [space for space in board.board if space[0] == r]
            col = [space for space in board.board if space[1] == c]
            box = [space for space in board.board if board.spaceToBox(space[0], space[1]) == b]
            
            toCheck = set(row).union(set(col), set(box))
            
            return [space for space in toCheck if space in board.unsolvedSpaces]          
                        
        originalBoard = board # Make a copy of the og board to keep
        
        if len(board.unsolvedSpaces) == 0: # Solved
            return True
        
        space = board.getMostConstrainedUnsolvedSpace()
        
        for val in board.evaluateSpace(space): # Iterate over possible values for current space
            if(board.isValidMove(space, val)):
                board.makeMove(space, val)
                
                # Forward checking
                forwardValid = True
                
                for neighbor in getRelatedSpaces(space):
                    if len(board.evaluteSpace(neighbor)) == 0: # No possible solution
                        forwardValid = False
                        break
                    
                if forwardValid and self.solveBoard(board): # Forward checking passed
                    return True
                
                board.undoMove(space, val) # Backtrack if failure

        board = originalBoard # Revert to origin
        return False # No solution
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
      print("Please enter the name of the csv file to run.\nFor instance, ``python a2.py example.csv``")
    else:
        board = Board(sys.argv[1])
        s = Solver()
        s.solveBoard(board)
        board.print()


