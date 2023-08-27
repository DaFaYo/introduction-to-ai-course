"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None
DEPTH = 10


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
            if board[i][j] == X:
                count += 1
            elif board[i][j] == O:
                count -= 1

    if count > 0:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    _actions = []
    for i in range(3):
        for j in range(3):
            if not board[i][j]:
                _actions.append((i, j))

    return _actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row, col = action
    if board[row][col]:
        raise Exception("Invalid action.")

    _result = copy.deepcopy(board)
    _result[row][col] = player(board)
    return _result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # first check horizontal
    for option in (X, O):
        for row in board:
            if all(value == option for value in row):
                return option

        transpose = zip(*board)
        for col in transpose:
            if all(value == option for value in col):
                return option

        diagonal_1 = 0
        diagonal_2 = 0
        for i in range(3):
            if board[i][i] == option:
                diagonal_1 += 1

            if board[2 - i][i] == option:
                diagonal_2 += 1

        if diagonal_1 == 3 or diagonal_2 == 3:
            return option


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    return winner(board) or not any(value == EMPTY for row in board for value in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if not (w := winner(board)):
        return 0

    return 1 if w == X else -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    _player = player(board)
    if _player == X:
        _, best_action = minimax_with_pruning_auxiliary(board, None, DEPTH, -math.inf, math.inf, True)
    else:
        _, best_action = minimax_with_pruning_auxiliary(board, None, DEPTH, -math.inf, math.inf, False)
    print(f"Best action is: {best_action}")
    return best_action


def minimax_with_pruning_auxiliary(board, action, depth, alpha, beta, maximizing_player):
    if depth == 0 or terminal(board):
        return utility(board), action
    if maximizing_player:
        value = -math.inf
        best_action = None
        for action in actions(board):
            new_value, _ = minimax_with_pruning_auxiliary(result(board, action),
                                                          action, depth - 1, alpha,
                                                          beta, False)
            if new_value > value:
                value = new_value
                best_action = action
            alpha = max(alpha, value)
            if beta <= alpha:
                break  # beta cutoff
        return value, best_action
    else:
        value = math.inf
        best_action = None
        for action in actions(board):
            new_value, _ = minimax_with_pruning_auxiliary(result(board, action),
                                                          action, depth - 1, alpha,
                                                          beta, True)
            if new_value < value:
                value = new_value
                best_action = action
            beta = min(beta, value)
            if beta <= alpha:
                break  # alpha cutoff
        return value, best_action
