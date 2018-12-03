"""
Loydruldrul's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

# helper function to move tiles
def position_tile(zero_pos, sol_pos):
    """
    :param sol_pos: position of target tile
    :param zero_pos: position of zero tile, the target position of targe tile
    :return: move string
    """
    (sol_row, sol_col) = sol_pos
    (zero_row, zero_col) = zero_pos
    move_string = ''
    # step 1:  move the zero tile up to the row of the target tile
    while sol_row < zero_row and sol_col != zero_col:
        move_string += 'u'
        zero_row -= 1
    # step 2:  move the target tile horizentally to its solved column
    # use dict to decrease branches just to pass the owl test
    move_dict = {'a_move': {True: 'l', False: 'r'}, 'move_cal': {True: 1, False: -1},
                'row0_circle': {True: 'drrul', False: 'dllur'}, 'row0_back': {True: 'dru', False: 'dlu'},
                'circle': {True:  'urrdl', False: 'ulldr'}, 'back': {True: 'ur', False: 'ul'}}

    if zero_col == sol_col:
        while zero_row > sol_row:
            move_string += 'u'
            zero_row -= 1
        sol_row += 1
    else:
        flag = zero_col > sol_col
        while zero_col != sol_col:
            move_string += move_dict['a_move'][flag]
            zero_col -= move_dict['move_cal'][flag]
        sol_col += move_dict['move_cal'][flag]
        if sol_row == 0:
            back_string = move_dict['row0_back'][flag]
            while sol_col != zero_pos[1]:
                move_string += move_dict['row0_circle'][flag]
                sol_col += move_dict['move_cal'][flag]
                zero_col += move_dict['move_cal'][flag]
        else:
            back_string = move_dict['back'][flag]
            while sol_col != zero_pos[1]:
                move_string += move_dict['circle'][flag]
                sol_col += move_dict['move_cal'][flag]
                zero_col += move_dict['move_cal'][flag]

        # special case: target tile is to the left of zero tile
        if sol_col == zero_pos[1] and sol_row == zero_pos[0]:
            return move_string
        move_string += back_string
        if sol_row == 0:
            sol_row += 1
    # step 3: move down the target tile to its solved row
    while sol_row != zero_pos[0]:
        move_string += 'lddru'
        sol_row += 1
    move_string += 'ld'
    return move_string

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # Invariant:
        # 1. Tile zero is positioned at (i, j).
        # 2. All tiles in row i to the right of position (i, j) are positioned at their solved location.
        # 3. All tiles in rows i+1 or below are positioned at their solved location.

        # check #1
        if self._grid[target_row][target_col] != 0:
            return False
        row = target_row
        col = target_col
        # check #2 and #3
        while True:
            if col == self._width - 1:
                if row == self._height - 1:
                    break
                else:
                    row += 1
                    col = 0
            else:
                col += 1
            if self._grid[row][col] != (col + self._width * row):
                return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # assert self.lower_row_invariant(target_row, target_col), "Wrong Zero Tile:(" + str(target_row) + ", " + str(target_col) + ")"
        move_string = position_tile((target_row, target_col), (self.current_position(target_row, target_col)))
        self.update_puzzle(move_string)
        # assert self.lower_row_invariant(target_row, target_col - 1), "Wrong Zero Tile:(" + str(target_row) + ", " + str(target_col) + ")"
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        target_col = 0
        move_string = ''
        # assert self.lower_row_invariant(target_row, target_col), "Wrong Zero Tile:(" + str(target_row) + ", " + str(target_col) + ")"
        (sol_row, sol_col) = self.current_position(target_row, target_col)
        # lucky case: target tile is just on the above of zero tile
        move_string += 'ur'
        if sol_row == target_row - 1 and sol_col == 0:
            for _ in range(self._width - 2):
                move_string += 'r'
            self.update_puzzle(move_string)
            return move_string
        # normal case. Step 1: Reposition the target tile to position (i-1,1) and
        # zero tile to position (i-1,0) using a process similar to solve_interior_tile
        move_string += position_tile((target_row - 1, target_col + 1), (sol_row, sol_col))
        # Step 2: apply a fixed move string that move the target tile on right position (i, 0)
        # and zero tile on (i -1 , 1)
        move_string += 'ruldrdlurdluurddlur'
        # Step 3: moving tile zero to the right end of row i-1.
        for _ in range(self._width - 2):
            move_string += 'r'
        self.update_puzzle(move_string)
        # assert self.lower_row_invariant(target_row - 1, self._width), "Wrong Zero Tile:(" + str(target_row) + ", " + str(target_col) + ")"
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        for row in range(2, self._height):
            for col in range(self._width):
                if self._grid[row][col] != col + row * self._width:
                    return False
        if self._grid[0][target_col] != 0 or self._grid[1][target_col] != self._width + target_col:
            return False
        if target_col == self._width - 1:
            return True
        for tile in range(target_col + 1, self._width):
            if self._grid[0][tile] != tile or self._grid[1][tile] != self._width + tile:
                return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        for row in range(2, self._height):
            for col in range(self._width):
                if self._grid[row][col] != col + row * self._width :
                    return False
        if self._grid[1][target_col] != 0:
            return False
        if target_col == self._width - 1:
            return True
        for tile in range(target_col + 1, self._width):
            if self._grid[1][tile] != self._width + tile:
                return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # assert self.row0_invariant(target_col), "Wrong Zero Tile:(0, " + str(target_col) + ")"
        (sol_row, sol_col) = self.current_position(0, target_col)
        move_string = 'ld'
        if sol_row == 0 and sol_col == target_col - 1:
            self.update_puzzle(move_string)
            return move_string
        move_string += position_tile((1, target_col - 1), (sol_row, sol_col))
        move_string += 'urdlurrdluldrruld'
        self.update_puzzle(move_string)
        # assert self.row1_invariant(target_col + 1), "Wrong Zero Tile:(1, " + str(target_col + 1) + ")"
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        # assert self.row1_invariant(target_col), "Wrong Zero Tile:(1, " + str(target_col) + ")"
        move_string = position_tile((1, target_col), self.current_position(1, target_col))
        move_string += 'ur'
        self.update_puzzle(move_string)
        # assert self.row0_invariant(target_col), "Wrong Zero Tile:(0, " + str(target_col) + ")"
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # assert self.row1_invariant(1), "Wrong Zero Tile:(1, 1)"
        move_string = ''
        if self._grid[0][1] == 1:
            move_string += 'lu'
        elif self._grid[0][0] == 1:
            move_string += 'ul'
        else:
            move_string += 'lurdlu'
        self.update_puzzle(move_string)
        return move_string

    def init_move(self):
        """
        Find the first wrong positioned tile from the right bottom and move the zero tile there
        """
        move_string = ''
        find_zero = False
        consistant = True
        init_row = self._height - 1
        init_col = self._width
        move_dict = {'a_move': {True: 'l', False: 'r'}, 'move_cal': {True: 1, False: -1}}
        for row in range(self._height -1, -1, -1):
            if find_zero:
                break
            for col in range(self._width -1, -1, -1):
                if self._grid[row][col] == 0:
                    find_zero = True
                    zero_row, zero_col = row, col
                    break
                if consistant and row > 1 and self.current_position(row, col) == (row, col):
                    init_row, init_col = row, col
                    continue
                else:
                    consistant = False
        if init_col == 0:
            init_col = self._width - 1
            init_row -= 1
        else:
            init_col -= 1
        # 1. move the zero tile to the right column.
        while zero_col != init_col:
            move_string += move_dict['a_move'][zero_col > init_col]
            zero_col -= move_dict['move_cal'][zero_col > init_col]
        # 2. move it to the right row
        while zero_row != init_row:
            move_string += 'd'
            zero_row += 1
        if len(move_string) != 0:
            self.update_puzzle(move_string)
        return move_string, init_row, init_col




    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # move the zero tile to the initial position
        move_string, zero_row, zero_col = self.init_move()
        # main processing for m x n tiles
        while True:
            # Step 1 : Solve the bottom m - 2 rows
            if zero_row > 1:
                # branch: Solve for all positions except for the left column
                if zero_col > 0:
                    assert self.lower_row_invariant(zero_row, zero_col), "Wrong Zero Tile: (" + str(zero_row) + ", " + str(zero_col) + ")"
                    move_string += self.solve_interior_tile(zero_row, zero_col)
                    zero_col -= 1
                # branch: Solve the leftmost column
                else:
                    assert self.lower_row_invariant(zero_row, zero_col), "Wrong Zero Tile: (" + str(zero_row) + ", " + str(zero_col) + ")"
                    move_string += self.solve_col0_tile(zero_row)
                    zero_row -= 1
                    zero_col = self._width - 1
            # Step 2 : Solve the rightmost n - 2 columns of the top two rows
            elif zero_col > 1:
                if zero_row == 1:
                    assert self.row1_invariant(zero_col), "Wrong Zero Tile: (1, " + str(zero_col) + ")"
                    move_string += self.solve_row1_tile(zero_col)
                    zero_row = 0
                elif zero_row == 0:
                    assert self.row0_invariant(zero_col), "Wrong Zero Tile: (0, " + str(zero_col) + ")"
                    move_string += self.solve_row0_tile(zero_col)
                    zero_row = 1
                    zero_col -= 1
            # Step 3: Solve the upper left 2 x 2 portion of the puzzle directly
            else:
                assert self.row1_invariant(1), "Wrong Zero Tile: (1, 1)"
                move_string += self.solve_2x2()
                break

        return move_string


# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(2, 2))

# p1 = Puzzle(3, 3, [[3, 2, 1], [5, 4, 0], [6, 7, 8]])
# p2 = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
# p3 = Puzzle(3, 3, [[2, 4, 0], [3, 1, 5], [6, 7, 8]])
# p4 = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
# p5 = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
# p6 =  Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
# print p2.init_move()
# print p2
# print p2.solve_puzzle()
# print p2
# print p1.solve_col0_tile(2)
# print p1.row1_invariant(2)
# print p1
# print p5
# print p5.solve_2x2()
# print p5
# print p3.solve_row0_tile(2)
# print p1
# print p6
# print p6.solve_col0_tile(3)
# print p6
# p7 = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0, 7, 8]])
# print p7
# print p7.solve_col0_tile(2)
# print p7
# p8 = Puzzle(4, 5, [[1, 2, 0, 3, 4], [6, 5, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
# print p8
# print p8.solve_row0_tile(2)
# print p8
# p9 = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
# print p9
# print p9.solve_row1_tile(2)
# print p9
p10 = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
print p10
print p10.init_move()
# print p10.solve_puzzle()
print p10