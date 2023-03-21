from copy import deepcopy
import math
import random
import uuid
from board import Board2048, Move, TILES
from evaluate import EF2048
from visualize_tree import build_tree


# TODO: I dont this that the MCTS is working properly, but i don't see anything wrong; the code just don't give expected results. (Or maybe the algorithm is just bad for this problem)
class MCTSNode:
    def __init__(self, board, parent=None) -> None:
        self.board: Board2048 = board
        self.parent: MCTSNode = parent
        # The child and the move that when made on the parent lead to this child. it used to keep track of the moves
        self.children: list[tuple[MCTSNode, Move]] = []
        self.visits: int = 0
        self.score: float = 0.0
        # Identifier used for tree visualizer
        self.identifier: str = str(uuid.uuid4())


class MCTS:
    # https://www.youtube.com/watch?v=UXW2yZndl7U
    def __init__(self, max_iterations: int, max_simulation_depth: int,  heuristic: EF2048, ubc1_score_c_value: int = 1) -> None:
        self.max_iterations: int = max_iterations
        self.max_simulation_depth: int = max_simulation_depth
        self.heuristic: EF2048 = heuristic
        self.ubc1_score_c_value = ubc1_score_c_value

    def search(self, root_board: Board2048) -> Move:
        """Return the best move for the given board"""
        root = self.MCTS(root_board)
        best_child, move = self.get_best_child(root)
        return move  # return the move that leeds to the best child

    def MCTS(self, root_board: Board2048) -> MCTSNode:
        # sourcery skip: merge-nested-ifs
        """Runs a MCTS algorithm on a given board.
        Returns a node objects that is the hole game tree generated"""
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

        # build_tree(root)

        # After all iterations, return the root with all children and information
        return root

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
            return (node.score / node.visits) + (self.ubc1_score_c_value * math.sqrt(2 * math.log(node.parent.visits) / node.visits))
        except ZeroDivisionError:
            return math.inf

    def evaluate(self, tiles: TILES) -> float:
        """Return the heuristic evaluation of the tiles"""
        return self.heuristic.evaluate(tiles)

    def get_best_child(self, node: MCTSNode) -> tuple[MCTSNode, Move]:
        """Return the child with the greatest average score"""
        return max(node.children, key=lambda x: x[0].score / x[0].visits)



class Expectimax:
    def __init__(self, max_depth: int, heuristic: EF2048) -> None:
        self.max_depth: int = max_depth
        self.heuristic: EF2048 = heuristic
    
    def search(self, root_board: Board2048):
        board = deepcopy(root_board)
        best_score = -math.inf
        best_move = Move.LEFT
        for move in board.available_moves():
            board.tiles = board.get_slid_tiles(move)
            score = self.expectimax(board, False, -math.inf, math.inf, 0)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def expectimax(self, board: Board2048, maximizing: bool, alfa: float, beta: float, depth: int):
        if board.is_terminal() or depth >= self.max_depth:
            return self.heuristic.evaluate(board.tiles)
        
        score = 0
        
        if maximizing:
            score = -math.inf
            for move in board.available_moves():
                # Move the board
                board.tiles = board.get_slid_tiles(move)
                child_score = self.expectimax(board, not maximizing, alfa, beta, depth + 1)
                if child_score > score:
                    score = child_score
                    
                if child_score >= beta:
                    break
                
                if child_score > alfa:
                    alfa = child_score
      
        else:  # Is a chance node
            score = 0
            # for all possible new tiles values and all empty coords... 
            for tile_number in [2, 4]:
                empty_coords = board.empty_spaces_coords()
                for empty_coord in empty_coords:
                    # add the tile to the board
                    board[empty_coord[0], empty_coord[1]] = tile_number
                    score += self.expectimax(board, not maximizing, alfa, beta, depth + 1)
                    # Calculate the average score
                    score = score / (len(empty_coords) * 2)
                    
                    # remove the tile
                    board[empty_coord[0], empty_coord[1]] = 0
        
        return score
    

class Random:
    def search(self, board: Board2048) -> Move:
        return random.choice(board.available_moves())
    
class Simple:
    def __init__(self, heuristic: EF2048) -> None:
        self.heuristic = heuristic
        
    def search(self, board: Board2048) -> Move:
        best = [
            (self.heuristic.evaluate(board.get_slid_tiles(move)), move)
            for move in board.available_moves()
        ]
        return max(best, key=lambda x: x[0])[1]