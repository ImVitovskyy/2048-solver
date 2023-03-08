"""Here are classes that are used to evaluate the board"""

import itertools
import math
import numpy as np
from board import Board2048


class Heuristic:
    """Evaluate the board giving it a score that represents its desirability.
    The greatest the score the better the board is.

    It is based on four factors:
        empty_spaces: Amount of empty cells.
        tiles_score: The sum of all values on the board.
        tiles_position: Evaluate the position of the tiles using a location score map. The point is to reward tiles that are on the edge and corner using their value as a multiplier.
        smoothness: Reward adjacent tiles having similar values.

    The total score is calculated using the equation:
        factor1 * weight1 + factor2 * weight2 + ... + factorN * weightN = total_score
    """

    def __init__(self, board: Board2048,
                 empty_spaces_weight: int = 1,
                 tiles_score_weight: int = 1,
                 edge_distance_weight: int = 1,
                 smoothness_weight: int = 1,
                 location_score_map: np.ndarray[(4, 4), int] = np.array([[3, 2, 2, 3],
                                                                         [2, 1, 1, 2],
                                                                         [2, 1, 1, 2],
                                                                         [3, 2, 2, 3]])):
        self.location_score_map = location_score_map
        self.board = board

        self.empty_spaces = 0
        self.tiles_score = 0
        self.tiles_position = 0
        self.smoothness = 0

        self.total_score = self._calculate_total_score(empty_spaces_weight,
                                                       tiles_score_weight,
                                                       edge_distance_weight,
                                                       smoothness_weight)

    def _calculate_factors(self):
        # everything can be calculated in one single loop
        for i, j in itertools.product(range(4), range(4)):
            tile = self.board[i, j]

            if tile == 0:
                self.empty_spaces += 1
                continue

            self.tiles_score += tile

            self.tiles_position += tile * self.location_score_map[i][j]

            # smoothness calculation
            if j == 3 or i == 3:  # prevents index 4 is out of bounds error
                continue
            for dx, dy in [(0, 1), (1, 0)]:
                x = i + dx
                y = j + dy
                neighbor_value = self.board[x, y]
                if x < 4 and y < 4 and neighbor_value != 0:
                    # The intuition behind this is that adjacent tiles with similar
                    # values will have logarithms that are close together, resulting in
                    # values near (or equal) zero. Tiles with different values will lead to
                    # values very small. The more small the values are, the more penalized
                    # the smoothness score will be.
                    self.smoothness -= abs(math.log2(tile) -
                                           math.log2(neighbor_value))

    def _calculate_total_score(self,
                               empty_spaces_weight,
                               tiles_score_weight,
                               tiles_position_weight,
                               smoothness_weight):

        self._calculate_factors()
        return self.empty_spaces * empty_spaces_weight + \
            self.tiles_score * tiles_score_weight + \
            self.tiles_position * tiles_position_weight + \
            self.smoothness * smoothness_weight
