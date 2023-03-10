import itertools
import random
import numpy as np
from nptyping import NDArray, Int, Shape

TILES = NDArray[Shape["4, 4"], Int]


class Board2048:
    MOVES = ['up', 'down', 'left', 'right']

    def __init__(self, starting_position: TILES = None):
        if starting_position is None:  # new board
            self.tiles: TILES = np.zeros((4, 4), dtype=int)
            self.add_new_random_tile()
            self.add_new_random_tile()
        else:  # pre-made board (generally used for testing)
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
        return [
            (row, col)
            for row, col in itertools.product(range(4), range(4))
            if self[row, col] == 0]

    def get_slid_tiles(self, direction: str) -> TILES:
        """Return a copy of the board slid in the specified direction"""
        board_copy = np.copy(
            self.tiles)  # create a copy to not modify the original

        # Rotate board so that direction corresponds to moving left as each row can be treated independently
        match direction:
            case 'up':
                board = np.rot90(board_copy, 1)
            case 'down':
                board = np.rot90(board_copy, 3)
            case 'left':
                board = board_copy
            case 'right':
                board = np.rot90(board_copy, 2)

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
            row = np.pad(row, (0, board.shape[1]-len(row)), 'constant')
            board[i] = row

        # Rotate board back to its original orientation
        match direction:
            case 'up':
                board = np.rot90(board, 3)
            case 'down':
                board = np.rot90(board, 1)
            case 'left':
                board = board
            case 'right':
                board = np.rot90(board, 2)

        return board

    def available_moves(self) -> list:
        available = []
        for move in self.MOVES:
            slid_tiles = self.get_slid_tiles(move)
            if not np.array_equal(slid_tiles, self.tiles):
                available.append(move)
                
        return available

    def is_over(self) -> bool:
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
                board_str += f'{self.tiles[i][j]:^5}|'.replace('0', ' ')
            board_str += '\n'
            board_str += '+-----+-----+-----+-----+\n'
        return board_str
