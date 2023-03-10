import math
import random
from board import Board2048


class MCTSNode:
    def __init__(self, board, parent=None):
        self.board: Board2048 = board
        self.parent: MCTSNode = parent
        self.children: list[tuple[MCTSNode, str]] = []
        self.visits: int = 0
        self.score: float = 0.0


class MCTS:
    def __init__(self, max_iterations, heuristic):
        self.max_iterations = max_iterations
        self.heuristic = heuristic

    def search(self, initial_state):
        root = MCTSNode(initial_state)
        for _ in range(self.max_iterations):
            node = root

            # Selection
            # select a child node until there is no more children
            while node.children:
                node = self.select_child(node)

            # Expansion
            # create and get a child node with a untried move
            if untried_moves := self.get_untried_moves(node):
                node = self.expand_node(node, random.choice(untried_moves))

            # Simulation
            while not self.get_untried_moves(node) and node.children:
                node = self.select_child(node)
            score = self.evaluate(node)

            # Backpropagation
            while node:
                node.visits += 1
                node.score += score
                node = node.parent

        # Choose the move with the highest average score
        best_child = self.get_best_child(root)
        return best_child[1]

    def select_child(self, node: MCTSNode) -> MCTSNode:
        # select the child with the highest UCB1 score
        return max(node.children, key=lambda x: self.ucb1_score(x[0]))[0]

    def ucb1_score(self, node: MCTSNode) -> float:
        # compute the UCB1 score for a node
        return node.score / node.visits + 2 * math.sqrt(2 * math.log(node.parent.visits) / node.visits)

    def expand_node(self, node: MCTSNode, move: str) -> MCTSNode:
        # expand a node with a new child for each move
        new_board = Board2048(node.board.get_slid_tiles(move))
        new_board.add_new_random_tile()
        child = MCTSNode(new_board, node)
        node.children.append((child, move))
        return child

    def get_untried_moves(self, node: MCTSNode):
        # return the untried moves from a node's state
        tried = list(node.children)
        return [move for move in node.board.MOVES if move not in tried]

    def evaluate(self, node: MCTSNode):
        # evaluate the value of a game state
        return self.heuristic.calculate(node.board.tiles)

    def get_best_child(self, node: MCTSNode):
        # return the child with the highest average score
        return max(node.children, key=lambda c: c[0].score / c[0].visits)
