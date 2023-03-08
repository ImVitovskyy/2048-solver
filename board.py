import itertools
import random
import numpy as np

TILES = np.ndarray[(4, 4), int]

class Board2048:
    def __init__(self, starting_position: TILES=None):
        if starting_position is None:  # new board
            self.tiles: TILES = np.zeros((4, 4), dtype=int)
            self.add_new_tile()
            self.add_new_tile()
        else:  # pre-made board
            self.tiles: TILES = starting_position

    def get_empty_spaces(self) -> list[tuple[int, int]]:
        return [
            (row, col)
            for row, col in itertools.product(range(4), range(4))
            if self[row, col] == 0
        ]

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
        board_str = '+-----+-----+-----+-----+\n'
        for i in range(4):
            board_str += '|'
            for j in range(4):
                board_str += f'{self.tiles[i][j]:^5}|'
            board_str += '\n'
            board_str += '+-----+-----+-----+-----+\n'
        return board_str    moves = []
    for direction in ['up', 'down', 'left', 'right']:
        new_board = self.get_slid_board(direction)
        if np.array_equal(new_board, self.tiles):
            moves.append(direction)
    return moves
"""