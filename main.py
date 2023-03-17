from states import *  # File with numpy arrays representing a board state. Used for testing
import board
import evaluate
import ai

# TODO: create a game class

basic_weights = {'score': 0, 'empty_tiles': 1,
                 'tiles_position': 0, 'smoothness': 1}


def main() -> int:
    board1 = board.Board2048(test_tiles3)
    heuristic = evaluate.EF2048Basic()
    mcts = ai.MCTS(32, 16, heuristic, 2)
    while not board1.is_terminal():
        print(board1)
        print(heuristic.evaluate(board1.tiles))
        move = mcts.search(board1)
        board1.tiles = board1.get_slid_tiles(move)
        board1.add_new_random_tile()

    print(board1)
    print(np.sum(board1.tiles))


if __name__ == '__main__':
    main()
