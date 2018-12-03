"""
Clone of 2048 game.
"""

#########################################################
# Just for saving script.
# IDE is CodeSkulptor.
# poc_2048_gui is not include in python desktop

import random

import POC_2048_Merge as merge
import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        #initialize the height, width, and grid  
        self._height_ = grid_height
        self._width_ = grid_width
        self._game_grid_ = [ [0 for col in range(self._width_)] 
                         for row in range(self._height_)]
        #create a dictionary for indice
        self._indice_ = {UP: [[0, col] for col in range(self._width_)],
                       DOWN: [[self._height_-1, col] for col in range(self._width_)],
                       LEFT: [[row, 0] for row in range(self._height_)],
                       RIGHT: [[row, self._width_-1] for row in range(self._height_)]}

            

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self.__init__(self._height_,self._width_)
        self.new_tile()
        self.new_tile()
            

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        grim_str = ""
        for row in self._game_grid_:
            for tile in row:
                grim_str += str(tile) + " "
            grim_str += "\n"
        return grim_str

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._height_

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._width_

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        #flag for determining moved or not
        move_or_not = False
        #first loop in range of indices 
        for num in range(len(self._indice_[direction])):
            indice = (self._indice_[direction])[num]
            line_before_move = []
            #second loop along the direction
            if (direction == 3) or (direction == 4):
                num_steps = self._width_
            elif (direction == 1) or (direction == 2):
                num_steps = self._height_
            #retrieve the tile values 
            for step in range(num_steps):
                row = indice[0] + step * (OFFSETS[direction])[0]
                col = indice[1] + step * (OFFSETS[direction])[1]
                line_before_move.append(self.get_tile(row,col))
            #replace these values using def merge()
            line_after_move = merge.merge(line_before_move)
            for step in range(num_steps):
                row = indice[0] + step * (OFFSETS[direction])[0]
                col = indice[1] + step * (OFFSETS[direction])[1]
                self.set_tile(row, col, line_after_move[step])
            #add new tiles if moved
            if line_after_move != line_before_move:
                move_or_not = True
        if move_or_not == True:
            self.new_tile()
        for row in range(self._height_):
            for col in range(self._width_):
                if self._game_grid_[row][col] == 2048:
                    print "YOU GET POC_2048!"
        return move_or_not


    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        #create new tile
        rand_index = random.randrange(0,10)
        if rand_index > 0:
            new_tile = 2
        else:
            new_tile = 4
        #collect coordinates of all empty tiles
        zero_list = []
        for row in range(self._height_):
            for col in range(self._width_):
                if self._game_grid_[row][col] == 0:
                    zero_list.append([row,col])
        #cover a random empty tile by new tile
        rand_pos = random.randrange(0, len(zero_list))
        new_tile_pos=zero_list[rand_pos]
        self.set_tile(new_tile_pos[0], new_tile_pos[1], new_tile)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._game_grid_[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._game_grid_[row][col]

print TwentyFortyEight(4, 4)
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
