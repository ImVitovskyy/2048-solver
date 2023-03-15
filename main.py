from time import sleep
from states import *  # File with numpy arrays representing a board state. Used for testing
from board import Board2048
import evaluate
from ai import MCTS

# TODO: create a game class

def main() -> int:
    board1 = Board2048(test_tiles3)
    weights = {
        'score': 1,
        'empty_tiles': 0,
        'tiles_position': 0,
        'smoothness': 0,
    }
    heuristic1 = evaluate.EF2048Basic(weights)
    mcts1 = MCTS(32, 32, heuristic1)

    while not board1.is_terminal():
        print(board1)
        print(heuristic1.evaluate(board1.tiles))
        move = mcts1.search(board1)
        board1.tiles = board1.get_slid_tiles(move)
        board1.add_new_random_tile()

    print(np.sum(board1.tiles))
    print(weights)
    return 0


if __name__ == '__main__':
    main()
