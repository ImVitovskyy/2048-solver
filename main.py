from time import sleep
from states import *  # File with numpy arrays representing a board state. Used for testing
from board import Board2048
from evaluate import EF2048Simple
from ai import MCTS


def main() -> int:
    board1 = Board2048(test_tiles3)
    heuristic1 = EF2048Simple()
    mcts1 = MCTS(32, 16, heuristic1)

    while not board1.is_terminal():
        print(board1)
        move = mcts1.search(board1)
        board1.tiles = board1.get_slid_tiles(move)
        board1.add_new_random_tile()

    print(heuristic1.evaluate(board1.tiles))
    return 0


if __name__ == '__main__':
    main()
