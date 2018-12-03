"""
Game of Life demo
"""

"""
Grid class
"""
"""
Game of Life GUI
Click on the canvas to add cells to the simulation
"""

import simplegui
from POC_Zombie_Apocalypse.poc_grid import Grid

# Global constants
CELL_SIZE = 10
EMPTY = 0
FULL = 1

class GolGui:
    """
    Container for interactive content
    """

    def __init__(self, game):
        """
        Create frame and timers, register event handlers
        """
        self.game = game
        self._grid_height = self.game.get_grid_height()
        self._grid_width = self.game.get_grid_width()
        self._frame = simplegui.create_frame("Interactive Game of Life demo",
                                             self._grid_width * CELL_SIZE,  self._grid_height * CELL_SIZE)
        self._frame.set_canvas_background("White")
        self._frame.add_button("Clear all", self.clear, 100)
        self._frame.add_button("Step", self.step, 100)
        self._frame.add_button("Ten steps", self.ten_steps, 100)
        self._frame.set_mousedrag_handler(self.add_cell_index)
        self._frame.set_draw_handler(self.draw)

    def start(self):
        """
        Start frame
        """
        self._frame.start()

    def clear(self):
        """
        Event handler for button that clears everything
        """
        self.game.clear()

    def step(self):
        """
        Event handler for button that updates current game
        """
        self.game.update_gol()

    def ten_steps(self):
        """
        Event handler for button that updates current game by 10 steps
        """
        for dummy_idx in range(10):
            self.game.update_gol()

    def add_cell_index(self, click_position):
        """
        Event handler to add new cell index to the index queue
        """
        cell_index = self.game.get_index(click_position, CELL_SIZE)
        self.game.set_full(cell_index[0], cell_index[1])

    def draw_cell(self, canvas, row, col, color = "Cyan"):
        """
        Draw a cell in the grid
        """
        upper_left = [col * CELL_SIZE, row * CELL_SIZE]
        upper_right = [(col + 1) * CELL_SIZE, row * CELL_SIZE]
        lower_right = [(col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE]
        lower_left = [col * CELL_SIZE, (row + 1) * CELL_SIZE]
        canvas.draw_polygon([upper_left, upper_right, lower_right, lower_left], 1, "Black", color)

    def draw_grid(self, canvas, color = "Cyan"):
        """
        Draw entire grid
        """
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if not self.game.is_empty(row, col):
                    self.draw_cell(canvas, row, col, color)

    def draw(self, canvas):
        """
        Handler for drawing grid
        """
        self.draw_grid(canvas)


# Start interactive simulation
def run_gui(game):
    """
    Encapsulate frame
    """
    gui = GolGui(game)
    gui.start()





class GameOfLife(Grid):
    """
    Extend Grid class to support Game of Life
    """

    def update_gol(self):
        """
        Function that performs one step of the Game of Life
        """

        updated_grid = [[self.update_cell(row, col) \
                            for col in range(self.get_grid_width())] \
                            for row in range(self.get_grid_height())]

        for col in range(self.get_grid_width()):
            for row in range(self.get_grid_height()):
                if updated_grid[row][col] == EMPTY:
                    self.set_empty(row, col)
                else:
                    self.set_full(row, col)


    def update_cell(self, row, col):
        """
        Function that computes the update for one cell in the Game of Life
        """
        # compute number of living neighbors
        neighbors = self.eight_neighbors(row, col)
        living_neighbors = 0
        for neighbor in neighbors:
            if not self.is_empty(neighbor[0], neighbor[1]):
                living_neighbors += 1

        # logic for Game of life
        if (living_neighbors == 3) or (living_neighbors == 2 and not self.is_empty(row, col)):
            return FULL
        else:
            return EMPTY

# run gui
run_gui(GameOfLife(30, 40))