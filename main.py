from time import sleep
from states import *  # File with numpy arrays representing a board state. Used for testing
from board import Board2048
from evaluate import EF2048Basic
from ai import MCTS


def main() -> int:
    board1 = Board2048(test_tiles0)
    heuristic = EF2048Basic()
    mcts = MCTS(20, heuristic)

    while not board1.is_over():
        move = mcts.search(board1)
        new_board = Board2048(board1.get_slid_tiles(move))
        new_board.add_new_random_tile()
        board1 = new_board
        print(board1)
        sleep(0.3)

    print(np.sum(board1.tiles))
    return 0


if __name__ == '__main__':
    main()
