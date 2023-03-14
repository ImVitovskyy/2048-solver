"""Here are classes that are used to evaluate the board"""

import itertools
import math
import numpy as np
from board import TILES

MAX_SCORE = 262142
MAX_TILE = 131072
MAX_EMPTY_SPACES = 16
MAX_SMOOTHNESS = -234  # smaller values are better


def normalize_0to1(val, max, min):
    return (val - min) / (max - min)


class EF2048:  # "EF2048" stands for "Evaluation Function for 2048"
    def evaluate(self, tiles: TILES) -> float:
        """Return the score of the given tiles"""
        pass


class EF2048Simple(EF2048):
    def __init__(self) -> None:
        pass

    def evaluate(self, tiles: TILES) -> float:
        return np.sum(tiles)


class EF2048Basic(EF2048):
    """Evaluate the tiles giving it a score that represents its desirability.
    The greatest the score the better the tiles are.

    It is based on four factors:
        score: The sum of all tiles values.
        empty_spaces: Amount of empty cells.
        tiles_position: Evaluate the position of the tiles using a location score map. The point is to reward tiles that are on the edge and corner using their value as a multiplier.
        smoothness: Reward adjacent tiles having similar values.

    The total score is calculated using the equation:
        factor1 * weight1 + factor2 * weight2 + ... + factorN * weightN = total_score
    """

    def __init__(self, weights: dict = {'score': 1,
                                        'empty_tiles': 2.7,
                                        'tiles_position': 1,
                                        'smoothness': 0.1},
                 location_score_map: TILES = np.array([[6, 3, 3, 6],
                                                       [3, 1, 1, 3],
                                                       [3, 1, 1, 3],
                                                       [6, 3, 3, 6]])):

        self.weights = weights
        self.location_score_map = location_score_map

    def evaluate(self, tiles: TILES):
        factors = self.calculate_factors(tiles)

        return self.calculate_total_score()  # todo: finish this

    def calculate_factors(self, tiles: TILES) -> list:
        score = 0
        empty_spaces = 0
        tiles_position = 0
        smoothness = 0

        # everything can be calculated in one single loop
        for i, j in itertools.product(range(4), range(4)):
            tile = tiles[i][j]

            if tile == 0:
                empty_spaces += 1
                continue

            score += tile

            tiles_position += tile * self.location_score_map[i][j]

            # smoothness calculation
            if j == 3 or i == 3:  # prevents index 4 is out of bounds error
                continue

            for dx, dy in [(0, 1), (1, 0)]:
                x = i + dx
                y = j + dy
                neighbor_value = tiles[x][y]
                if x < 4 and y < 4 and neighbor_value != 0:
                    # The intuition behind this is that adjacent tiles with similar
                    # values will have logarithms that are close together, resulting in
                    # values near (or equal) zero. Tiles with different values will lead to
                    # values very small. The more small the values are, the more penalized
                    # the smoothness score will be.
                    smoothness -= abs(math.log2(tile) -
                                      math.log2(neighbor_value))

        return [score, empty_spaces, tiles_position, smoothness]

    def calculate_total_score(self, empty_spaces, tiles_score, tiles_position, smoothness):
        return empty_spaces * self.weights['empty_tiles'] + \
            tiles_score * self.weights['score'] + \
            tiles_position * self.weights['tiles_position'] + \
            smoothness * self.weights['smoothness']
