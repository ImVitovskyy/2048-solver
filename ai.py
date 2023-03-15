import math
import random
from board import Board2048, Move, TILES
from evaluate import EF2048

# TODO: optimize the code

class MCTSNode:
    def __init__(self, board, parent=None) -> None:
        self.board: Board2048 = board
        self.parent: MCTSNode = parent
        # the child and the mode that made on the parent lead to this child
        self.children: list[tuple[MCTSNode, Move]] = []
        self.visits: int = 0
        self.score: float = 0.0


class MCTS:
    # https://www.youtube.com/watch?v=UXW2yZndl7U
    def __init__(self, max_iterations: int, max_simulation_depth: int,  heuristic: EF2048) -> None:
        self.max_iterations: int = max_iterations
        self.max_simulation_depth: int = max_simulation_depth
        self.heuristic: EF2048 = heuristic

    def search(self, root_board: Board2048) -> Move:
        # sourcery skip: merge-nested-ifs
        """Return the best move for the given board"""
        root = MCTSNode(root_board)
        for _ in range(self.max_iterations):
            node = root

            # If the node has a child it is not a leaf node,
            # so we select the node child until it is a leaf node.
            # When out of this loop, the current node is a leaf node
            while node.children:
                node = self.selection(node)

            # If the node has been visited before, expand it
            if node.visits != 0:
                if self.expansion(node):
                    # if the node was expanded (children was created), select a child
                    node = self.selection(node)
                # if the node was not expanded, just proceed to the score and backpropagation

            # If the node has not been visited before, simulate it (rollout)
            if node.visits == 0:
                node = self.simulation(node)

            score = self.evaluate(node.board.tiles)

            # After expansion or simulation, do backpropagation
            self.backpropagation(node, score)

        # After all iterations, choose the move with the highest average score (get_best_child)
        best_child = self.get_best_child(root)
        return best_child[1]  # return the move that leeds to the best child

    def selection(self, node: MCTSNode) -> MCTSNode:
        """Return the child of the given node that has the highest ucb1 score"""
        return max(node.children, key=lambda x: self.ucb1_score(x[0]))[0]

    def expansion(self, node: MCTSNode) -> bool:
        """Create all possible children for the node.
        If the node already has children, its possible that this function will create duplicate children because of existent children.
        Return True if at least one child was created, otherwise, False"""
        if node.board.is_terminal():
            return False

        for move in node.board.available_moves():
            # create a new board from the move and add the random tile
            new_board = Board2048(node.board.get_slid_tiles(move))
            new_board.add_new_random_tile()

            # create a child with a parent and add the child to the parent
            child = MCTSNode(new_board, node)
            node.children.append((child, move))
        return True

    def simulation(self, node: MCTSNode) -> MCTSNode:  # rollout
        """Returns the deepest child in a random simulation"""
        # The deepest child is a terminal child or a child of max depth
        for _ in range(self.max_simulation_depth):
            if node.board.is_terminal():
                break

            # create a new board from a random move and add the random tile
            move = random.choice(node.board.available_moves())
            new_board = Board2048(node.board.get_slid_tiles(move))
            new_board.add_new_random_tile()

            # create a child with a parent
            child = MCTSNode(new_board, node)

            # Do not add the child to the parent.
            # Children should not be added during simulation, only during expansion

            node = child
        return node

    def backpropagation(self, node: MCTSNode, score: float) -> None:
        """Backpropagate through all parent nodes modifying its score and visits until gets to the root node.
        Returns the root node."""
        while node:
            node.visits += 1
            node.score += score
            # When in the root node the parent is None, so we get out of the loop
            node = node.parent
        return node

    def ucb1_score(self, node: MCTSNode) -> float:
        """Return the UCB1 score for a node"""
        # If the node has zero visits, the ucb1 score will have a ZeroDivisionError, what is essentially infinity.
        # The ucb1 score must prioritize nodes with no visits
        try:
            return node.score / node.visits + math.sqrt(2 * math.log(node.parent.visits) / node.visits)
        except ZeroDivisionError:
            return math.inf

    def evaluate(self, tiles: TILES) -> float:
        """Return the heuristic evaluation of the tiles"""
        return self.heuristic.evaluate(tiles)

    def get_best_child(self, node: MCTSNode) -> tuple[MCTSNode, Move]:
        """Return the child with the greatest average score"""
        return max(node.children, key=lambda x: x[0].score / x[0].visits)


# # Expectiminimax high-level overview draft
# class Node:
#     def __init__(self, state, player, depth, prob=None):
#         self.state = state
#         self.player = player
#         self.depth = depth
#         self.prob = prob
#         self.value = None


# class Expectiminimax:
#     def __init__(self, max_depth, eval_terminal, eval_non_terminal):
#         self.max_depth = max_depth
#         self.eval_terminal = eval_terminal
#         self.eval_non_terminal = eval_non_terminal

#     def expectiminimax(self, node):
#         if node.depth == 0 or self.is_terminal_state(node):
#             node.value = self.eval_terminal(node.state, node.player)
#             return node.value

#         if node.player == MAX_PLAYER:
#             best_value = float('-inf')
#             for move in self.get_possible_moves(node.state):
#                 next_state = self.apply_move(node.state, move)
#                 next_node = Node(next_state, MIN_PLAYER, node.depth - 1)
#                 value = self.expectiminimax(next_node)
#                 best_value = max(best_value, value)
#             node.value = best_value
#         else:
#             expected_value = 0
#             num_possible_moves = len(self.get_possible_moves(node.state))
#             for move in self.get_possible_moves(node.state):
#                 next_state = self.apply_move(node.state, move)
#                 next_prob = self.get_next_tile_probabilities(next_state)
#                 next_node = Node(next_state, MAX_PLAYER,
#                                  node.depth - 1, next_prob)
#                 probability = next_prob if node.prob is None else node.prob * next_prob
#                 value = self.expectiminimax(next_node)
#                 expected_value += probability * value
#             node.value = expected_value

#         return node.value

#     def get_possible_moves(self, state):
#         # Return all possible moves from the current state
#         pass

#     def apply_move(self, state, move):
#         # Apply a move to the current state and return the resulting state
#         pass

#     def is_terminal_state(self, node):
#         # Check if the current state is a terminal state
#         pass

#     def get_next_tile_probabilities(self, state):
#         # Return the probabilities of each possible tile that can be spawned in the next turn
#         pass
