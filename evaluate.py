"""Here are classes that are used to evaluate the board"""

import itertools
import math
import numpy as np
from board import TILES

# perfect board be like:
[[131072, 65536, 32768, 16384],
 [8192, 4096, 2048, 1024],
 [512, 256, 128, 64],
 [32, 16, 8, 4]]

# TODO: move this constants
# For normalizing values
MAX_SCORE = 262142
MIN_SCORE = 4
MAX_EMPTY_TILES = 15
MIN_EMPTY_TILES = 0 + 1e-5  # Very small clipping
MAX_TILES_POSITION = 3145704  # TODO: tiles position max and min may be wrong
MIN_TILES_POSITION = 2
MAX_SMOOTHNESS = 234
MIN_SMOOTHNESS = 0 + 1e-5  # Very small clipping
MAX_TILE = 131072
MIN_TILE = 2


def normalize_0to1(val, max, min):
    return (val - min) / (max - min)


class EF2048:  # "EF2048" stands for "Evaluation Function for 2048"
    def evaluate(self, tiles: TILES) -> float:
        """Return the score of the given tiles"""
        pass

# TODO: make good evaluating functions

class EF2048Basic(EF2048):
    def __init__(self) -> None:
        pass

    def evaluate(self, tiles: TILES) -> float:
        return float((np.sum(tiles == 0) + np.sum(tiles) + np.max(tiles)) / 3)


class EF2048Complex(EF2048):
    def __init__(self, weights: dict = None):

        # Default weights
        if weights is None:
            weights = {
                'score': 1,
                'empty_tiles': 1,
                'tiles_position': 1,
                'smoothness': 1,
            }
        self.weights = weights

        self.location_map: TILES = np.array([[1, 2, 3, 4],
                                             [8, 7, 6, 5],
                                             [9, 10, 11, 12],
                                             [16, 15, 14, 13]])

    def evaluate(self, tiles: TILES) -> float:
        """Return the total score of the given tiles"""
        score, empty_tiles, tiles_position, smoothness = self.calculate_factors(
            tiles)

        # Normalize score
        score = normalize_0to1(score,
                                 MAX_SCORE, MIN_SCORE)
        empty_tiles = normalize_0to1(empty_tiles,
                                       MAX_EMPTY_TILES, MIN_EMPTY_TILES)
        tiles_position = normalize_0to1(tiles_position,
                                          MAX_TILES_POSITION, MIN_TILES_POSITION)
        smoothness = normalize_0to1(smoothness,
                                      MAX_SMOOTHNESS, MIN_SMOOTHNESS)

        return self.calculate_total(score, empty_tiles, tiles_position, smoothness)

    def calculate_factors(self, tiles: TILES) -> list:
        """Return the four factors (score, empty_tiles, tiles_position and smoothness)"""
        score = 0
        empty_tiles = 0 + 1e-5  # Very small clipping for normalizing
        tiles_position = 0
        smoothness = 0 + 1e-5  # Very small clipping for normalizing

        # everything can be calculated in one single loop witch is much faster than a separate function for each factor (2x faster)
        for i, j in itertools.product(range(4), range(4)):
            tile = tiles[i][j]

            if tile == 0:
                empty_tiles += 1
                continue

            score += tile

            tiles_position += tile * self.location_map[i][j]

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
                    smoothness += abs(math.log2(tile) -
                                      math.log2(neighbor_value))

        return score, empty_tiles, tiles_position, smoothness

    def calculate_total(self, score, empty_tiles, tiles_position, smoothness) -> float:
        """Return the Weighted Arithmetic Mean"""
        # Note that the smoothness is being removed from the total, since big smoothness score means less desirable board
        return (score * self.weights['score'] +
                empty_tiles * self.weights['empty_tiles'] +
                tiles_position * self.weights['tiles_position'] -
                smoothness * self.weights['smoothness']) / \
            (self.weights['score'] + self.weights['empty_tiles'] +
             self.weights['tiles_position'] + self.weights['smoothness'])
