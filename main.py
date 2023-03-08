from board import Board2048
from evaluate import Heuristic
from states import *  # File with numpy arrays representing a board state. Used for testing


def main() -> int:
    board1 = Board2048(test_tiles1)
    evaluation1 = Heuristic(board1)

    print(evaluation1.total_score)
    return 0


if __name__ == '__main__':
    main()
