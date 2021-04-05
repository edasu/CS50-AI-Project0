"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                count += 1

    if board == initial_state():
        return X
    if count % 2 == 1:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid Action!!!")

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(new_board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winwin = [[(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]]

    for combine in winwin:
        count_x = 0
        count_o = 0
        for i, j in combine:
            if board[i][j] == X:
                count_x += 1
            if board[i][j] == O:
                count_o += 1
        if count_x == 3:
            return X
        if count_o == 3:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or not actions(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if (winner(board) == X):
        return 1
    elif (winner(board) == O):
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # Optimization by hardcoding the first move
    if board == initial_state():
        return 0, 1

    current_player = player(board)
    Max = float("-inf")
    Min = float("inf")
    best_value = Max if current_player == X else Min

    for action in actions(board):
        new_value = minimax_value(result(board, action), best_value)

        if current_player == X:
            new_value = max(best_value, new_value)

        if current_player == O:
            new_value = min(best_value, new_value)

        if new_value != best_value:
            best_value = new_value
            best_action = action

    return best_action


def minimax_value(board, best_value):
    """
    Returns the best value for each recursive minimax iteration.
    Optimized using Alpha-Beta Pruning: If the new value found is better
    than the best value then return new value without checking the others.
    """
    if terminal(board):
        return utility(board)

    current_player = player(board)
    value = float("-inf") if current_player == X else float("inf")

    for action in actions(board):
        new_value = minimax_value(result(board, action), value)

        if current_player == X:
            if new_value > best_value:
                return new_value
            value = max(value, new_value)

        if current_player == O:
            if new_value < best_value:
                return new_value
            value = min(value, new_value)

    return value
