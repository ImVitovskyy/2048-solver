import math
import random

# Monte Carlo Tree Search high-level overview draft
class MCTSNode:
    def __init__(self, state):
        self.state = state
        self.children = []
        self.visits = 0
        self.score = 0.0

class MCTS:
    def __init__(self, max_iterations):
        self.max_iterations = max_iterations

    def search(self, initial_state):
        root = MCTSNode(initial_state)
        for _ in range(self.max_iterations):
            node = root
            state = initial_state
            
            # Selection
            while node.children:
                node = self.select_child(node)
                state = self.apply_move(state, node.move)
                
            # Expansion
            if untried_moves := self.get_untried_moves(node, state):
                move = random.choice(untried_moves)
                state = self.apply_move(state, move)
                node = self.expand_node(node, state, move)
                
            # Simulation
            while self.get_untried_moves(node, state) == [] and node.children:
                node = self.select_child(node)
                state = self.apply_move(state, node.move)
            score = self.evaluate(state)
            
            # Backpropagation
            while node:
                node.visits += 1
                node.score += score
                node = node.parent
                
        # Choose the move with the highest average score
        best_child = self.get_best_child(root)
        return best_child.move

    def select_child(self, node):
        # select the child with the highest UCB1 score
        return max(node.children, key=self.ucb1_score)

    def ucb1_score(self, node):
        # compute the UCB1 score for a node
        return node.score / node.visits + math.sqrt(2 * math.log(node.parent.visits) / node.visits)

    def get_untried_moves(self, node, state):
        # return the untried moves from a node's state
        return [move for move in self.get_all_moves(state) if move not in node.moves]

    def expand_node(self, node, state, move):
        # expand a node with a new child
        child = MCTSNode(self.get_next_state(state, move))
        child.parent = node
        child.move = move
        node.children.append(child)
        return child

    def get_best_child(self, node):
        # return the child with the highest average score
        return max(node.children, key=lambda c: c.score / c.visits)

    def evaluate(self, state):
        # evaluate the value of a game state
        return self.evaluate_function(state)
    
    # TODO:
    # Implement the following methods to define the game rules and evaluation function:
    # - get_all_moves(state)
    # - apply_move(state, move)
    # - get_next_state(state, move)
    # - evaluate_function(state)


# Expectiminimax high-level overview draft
class Node:
    def __init__(self, state, player, depth, prob=None):
        self.state = state
        self.player = player
        self.depth = depth
        self.prob = prob
        self.value = None

class Expectiminimax:
    def __init__(self, max_depth, eval_terminal, eval_non_terminal):
        self.max_depth = max_depth
        self.eval_terminal = eval_terminal
        self.eval_non_terminal = eval_non_terminal

    def expectiminimax(self, node):
        if node.depth == 0 or self.is_terminal_state(node):
            node.value = self.eval_terminal(node.state, node.player)
            return node.value

        if node.player == MAX_PLAYER:
            best_value = float('-inf')
            for move in self.get_possible_moves(node.state):
                next_state = self.apply_move(node.state, move)
                next_node = Node(next_state, MIN_PLAYER, node.depth - 1)
                value = self.expectiminimax(next_node)
                best_value = max(best_value, value)
            node.value = best_value
        else:
            expected_value = 0
            num_possible_moves = len(self.get_possible_moves(node.state))
            for move in self.get_possible_moves(node.state):
                next_state = self.apply_move(node.state, move)
                next_prob = self.get_next_tile_probabilities(next_state)
                next_node = Node(next_state, MAX_PLAYER, node.depth - 1, next_prob)
                probability = next_prob if node.prob is None else node.prob * next_prob
                value = self.expectiminimax(next_node)
                expected_value += probability * value
            node.value = expected_value

        return node.value

    def get_possible_moves(self, state):
        # Return all possible moves from the current state
        pass

    def apply_move(self, state, move):
        # Apply a move to the current state and return the resulting state
        pass

    def is_terminal_state(self, node):
        # Check if the current state is a terminal state
        pass

    def get_next_tile_probabilities(self, state):
        # Return the probabilities of each possible tile that can be spawned in the next turn
        pass
