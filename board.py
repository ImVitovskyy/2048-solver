import itertools
import random
import numpy as np
from nptyping import NDArray, Int, Shape

TILES = NDArray[Shape["4, 4"], Int]

class Board2048:
    def __init__(self, starting_position: TILES=None):
        if starting_position is None:  # new board
            self.tiles: TILES = np.zeros((4, 4), dtype=int)
            self.add_new_tile()
            self.add_new_tile()
        else:  # pre-made board
            self.tiles: TILES = starting_position

    def get_empty_spaces(self) -> list[tuple[int, int]]:
        """Return a list of all empty coordinates of the board"""
        return [
            (row, col)
            for row, col in itertools.product(range(4), range(4))
            if self[row, col] == 0]

    def add_new_tile(self) -> bool:
        """Add a new tile with a value of either 2 (90% probability) or 4 (10% probability) to a randomly-chosen empty space on the board"""
        empty_spaces = self.get_empty_spaces()
        if not empty_spaces:
            return False  # board is full
        row, col = random.choice(empty_spaces)
        self[row, col] = 2 if random.random() < 0.9 else 4  # 90% chance of 2, 10% chance of 4
        return True

    def __getitem__(self, pos):
        """Get the value of the tile at the specified position"""
        row, col = pos
        return self.tiles[row][col]

    def __setitem__(self, pos, value):
        """Set the value of the tile at the specified position"""
        row, col = pos
        self.tiles[row][col] = value

    def __str__(self):
        """String representation of the board formatted to look good on the terminal"""
        board_str = '+-----+-----+-----+-----+\n'
        for i in range(4):
            board_str += '|'
            for j in range(4):
                board_str += f'{self.tiles[i][j]:^5}|'
            board_str += '\n'
            board_str += '+-----+-----+-----+-----+\n'
        return board_str
    