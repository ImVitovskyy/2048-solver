import itertools
import random
import numpy as np
from enum import Enum
import re

TILES = np.ndarray[(4, 4), int]


class Move(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


class Board2048:
    def __init__(self, starting_position: TILES = None):
        if starting_position is None:  # new board
            self.tiles: TILES = np.zeros((4, 4), dtype=int)
            self.add_new_random_tile()
            self.add_new_random_tile()

        else:  # pre-made board
            self.tiles: TILES = starting_position

    def add_new_random_tile(self) -> bool:
        """Add a new tile with a value of either 2 (90% probability) or 4 (10% probability) to a randomly-chosen empty space on the board"""
        empty_spaces = self.empty_spaces_coords()
        if not empty_spaces:
            return False  # board is full
        row, col = random.choice(empty_spaces)
        # 90% chance of 2, 10% chance of 4
        self[row, col] = 2 if random.random() < 0.9 else 4
        return True

    def empty_spaces_coords(self) -> list[tuple[int, int]]:
        """Return a list of all empty coordinates of the board"""
        return [(row, col)
                for row, col in itertools.product(range(4), range(4))
                if self[row, col] == 0]

    def get_slid_tiles(self, move: Move) -> TILES:
        """Return a copy of the board slid in the specified direction"""
        # create a copy to not modify the original
        board_copy = np.copy(self.tiles)

        # Rotate board so that direction corresponds to moving left as each row can be treated independently
        match move:
            case move.LEFT:
                board = board_copy
            case move.UP:
                board = np.rot90(board_copy, move.UP.value)
            case move.RIGHT:
                board = np.rot90(board_copy, move.RIGHT.value)
            case move.DOWN:
                board = np.rot90(board_copy, move.DOWN.value)

        # Slide tiles
        for i in range(4):
            row = board[i]
            # Remove any zeros in the row
            row = row[row != 0]
            # Combine adjacent tiles that have the same value
            for j in range(len(row)-1):
                if row[j] == row[j+1]:
                    row[j] *= 2
                    row[j+1] = 0
            # Move any remaining tiles to the left
            row = row[row != 0]
            row = np.pad(row, (0, 4-len(row)), 'constant')
            board[i] = row

        # Rotate board back to its original orientation
        match move:
            case move.LEFT:
                board = board
            case move.UP:
                board = np.rot90(board, 4 - move.UP.value)
            case move.RIGHT:
                board = np.rot90(board, 4 - move.RIGHT.value)
            case move.DOWN:
                board = np.rot90(board, 4 - move.DOWN.value)

        return board

    def available_moves(self) -> list[Move]:
        """Return a list of available moves that can be made on the board"""
        available = []
        for move in Move:
            slid_tiles = self.get_slid_tiles(move)
            if not np.array_equal(slid_tiles, self.tiles):
                available.append(move)

        return available

    def is_terminal(self) -> bool:
        """Return True if there is no available moves in the board"""
        return not self.available_moves()

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
                s = f'{self.tiles[i][j]:^5}|'
                board_str += re.sub(r"(?<!\d)0(?!\d)", ' ', s)
            board_str += '\n'
            board_str += '+-----+-----+-----+-----+\n'
        return board_str