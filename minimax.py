import math
import copy
import breakthrough as game
from heuristics import *

def evaluation(board):
    f1 = fov_evaluation(board)
    f2 = piece_value_evaluation(board)
    f3 = mobility_evaluation(board)
    f4 = number_of_pieces(board)
    score = f1 + .9*f2 + .4*f3 + .5*f4
    return score

def minimax(board, depth, alpha, beta, maximizing, memo):
    if board.is_gameover() or depth == 0:
        return evaluation(board), None

    best_move = None

    if maximizing:
        best_score = -math.inf
        for move in board.possible_moves(game.WHITE):
            new_board = copy.deepcopy(board)
            new_board.perform_move(move)

            key = new_board.serialise()

            if key not in memo:
                current_score, _ = minimax(
                    new_board, depth-1, alpha, beta, False, memo)
                memo[key] = current_score
            else:
                current_score = memo[key]

            if current_score > best_score:
                best_score = current_score
                best_move = move

            alpha = max(best_score, alpha)

            if alpha >= beta:
                break
    else:
        best_score = math.inf
        for move in board.possible_moves(game.BLACK):
            new_board = copy.deepcopy(board)
            new_board.perform_move(move)

            key = new_board.serialise()

            if key not in memo:
                current_score, _ = minimax(
                    new_board, depth-1, alpha, beta, True, memo)
                memo[key] = current_score
            else:
                current_score = memo[key]

            if current_score < best_score:
                best_score = current_score
                best_move = move

            beta = min(best_score, beta)

            if alpha >= beta:
                break

    return best_score, best_move
