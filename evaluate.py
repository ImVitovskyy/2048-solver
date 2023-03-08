"""Here are classes that are used to evaluate the board"""

import itertools
import math
import numpy as np
from board import TILES


class HEF2048:  # "HEF2048" stands for "Heuristic Evaluation Function for 2048"
    def calculate(self, tiles: TILES):
        """Return the score of the given tiles"""
        pass


class HEF2048Basic(HEF2048):
    """Evaluate the tiles giving it a score that represents its desirability.
    The greatest the score the better the tiles are.

    It is based on four factors:
        empty_spaces: Amount of empty cells.
        tiles_score: The sum of all tiles values.
        tiles_position: Evaluate the position of the tiles using a location score map. The point is to reward tiles that are on the edge and corner using their value as a multiplier.
        smoothness: Reward adjacent tiles having similar values.

    The total score is calculated using the equation:
        factor1 * weight1 + factor2 * weight2 + ... + factorN * weightN = total_score
    """

    def __init__(self,
                 empty_spaces_weight: int = 1,
                 tiles_score_weight: int = 1,
                 tiles_position_weight: int = 1,
                 smoothness_weight: int = 1,
                 location_score_map: TILES = np.array([[3, 2, 2, 3],
                                                       [2, 1, 1, 2],
                                                       [2, 1, 1, 2],
                                                       [3, 2, 2, 3]])):
        self.location_score_map = location_score_map

        self.empty_spaces_weight = empty_spaces_weight
        self.tiles_score_weight = tiles_score_weight
        self.tiles_position_weight = tiles_position_weight
        self.smoothness_weight = smoothness_weight

    def calculate(self, tiles: TILES):
        empty_spaces = 0
        tiles_score = 0
        tiles_position = 0
        smoothness = 0

        # everything can be calculated in one single loop
        for i, j in itertools.product(range(4), range(4)):
            tile = tiles[i][j]

            if tile == 0:
                empty_spaces += 1
                continue

            tiles_score += tile

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

        return self._calculate_total_score(empty_spaces, tiles_score, tiles_position, smoothness)

    def _calculate_total_score(self, empty_spaces, tiles_score, tiles_position, smoothness):
        return empty_spaces * self.empty_spaces_weight + \
            tiles_score * self.tiles_score_weight + \
            tiles_position * self.tiles_position_weight + \
            smoothness * self.smoothness_weight
