import copy
import itertools
import random
import numpy as np

TILES = np.ndarray[(4, 4), int]

class Board2048:
    def __init__(self, starting_position: TILES=None):
        if starting_position:
            self.tiles: TILES = starting_position
        else:
            self.tiles: TILES = np.zeros((4, 4), dtype=int)
            self.add_new_tile()
            self.add_new_tile()

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

    def get_slid_board(self, direction: str) -> TILES:
        """Return a copy of the board slid in the specified direction"""
        board_copy = np.copy(self.tiles)  # create a copy to not modify the original
        
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
            row = board[i, :]
            non_zero_tiles = row[row != 0]
            new_row = np.zeros_like(row)
            j = 0
            while j < len(non_zero_tiles):
                if j == len(non_zero_tiles) - 1:
                    new_row[j] = non_zero_tiles[j]
                    break
                if non_zero_tiles[j] == non_zero_tiles[j+1]:
                    new_row[j] = 2 * non_zero_tiles[j]
                    j += 2
                else:
                    new_row[j] = non_zero_tiles[j]
                    j += 1
            board[i, :] = new_row

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

    def is_game_over(self) -> bool:
        return not self.get_valid_moves()

    def get_valid_moves(self) -> list:
        """Return a list of valid moves (up, down, left, right)"""
        moves = []
        for direction in ['up', 'down', 'left', 'right']:
            new_board = self.get_slid_board(direction)
            if np.array_equal(new_board, self.tiles):
                moves.append(direction)
        return moves

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
        return board_str