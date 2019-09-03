from board import *
import copy


def dodge_player(board):
    possible_moves = board.black_possible_moves()

    selected_moves = []

    for move in possible_moves:
        if move[1][0] == 1:
            return move
        if move[1] in board.white_positions:
            return move
        if (move[1][0] - 1, move[1][1] - 1) not in board.white_positions:
            if (move[1][0] - 1, move[1][1] + 1) not in board.white_positions:
                selected_moves.append(move)

    if selected_moves:
        index = random.randint(0, abs(len(selected_moves) - 1))
        return selected_moves[index]

    return selected_moves


def minimax(board, depth, maximizing):
    if depth == 0 or board.game_is_over(): 
        return board.evaluation(), None

    best_score = None
    best_move = None

    if maximizing:
        for move in board.white_possible_moves():
            new_board = copy.deepcopy(board)
            new_board.perform_white_move(move)

            current_score,_ = minimax(new_board, depth-1, False)

            if best_score is None:
                best_score = current_score
                best_move = move
            elif current_score > best_score:
                best_score = current_score
                best_move = move

    else:
        for move in board.black_possible_moves():
            new_board = copy.deepcopy(board)
            new_board.perform_black_move(move)

            current_score,_ = minimax(new_board, depth-1, True)

            if best_score is None:
                best_score = current_score
                best_move = move
            elif current_score < best_score:
                best_score = current_score
                best_move = move

    
    return best_score, best_move

board = Board(5, 5)

board.display()


while True:

    _, move = minimax(board, 4, True)

    if not board.perform_white_move(move):
        print("minimax lost")
        break

    board.display()

    if move[1][0] == board.lines:
        print("minimax wins")
        break

    move = dodge_player(board)

    if not board.perform_black_move(move):
        print("minimax wins")
        break

    board.display()

    if move[1][0] == 1:
        print("minimax lost")
        break
    
    





