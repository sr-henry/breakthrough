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
            selected_moves.append(move)
        if (move[1][0] - 1, move[1][1] + 1) not in board.white_positions:
            selected_moves.append(move)

    if selected_moves:
        index = random.randint(0, abs(len(selected_moves) - 1))
        return selected_moves[index]

    return selected_moves


def evaluation(board):

        ## Value of Pieces
        value = 0.0
        for v in range(1, board.lines + 1):
            pieces_w = list(filter(lambda pos: pos[0] == v, board.white_positions))
            pieces_b = list(filter(lambda pos: pos[0] == ((board.lines + 1) - v), board.black_positions))
            value += v*(len(pieces_w) - len(pieces_b))


        ## Mobility (the number of legal moves)
        white_legal_moves = board.white_possible_moves()
        black_legal_moves = board.black_possible_moves()
        value += 0.1*(len(white_legal_moves) - len(black_legal_moves))

        ## Blocked Pieces
        white_origins = set(map(lambda move: move[0], white_legal_moves))
        black_origins = set(map(lambda move: move[0], black_legal_moves))
        white_positions_blocked = len(board.white_positions) - len(white_origins)
        black_positions_blocked = len(board.black_positions) - len(black_origins) 
        value -= 0.1*(white_positions_blocked - black_positions_blocked)    

        ## Connectivity

        return value


def computer_minimax(board, depth, alpha, beta, maximizing, memo):
    if depth == 0 or board.is_game_over():
        return evaluation(board), None
    
    best_move = None

    if maximizing:
        best_score = -10000
        for move in board.white_possible_moves():
            if move[1][0] == board.lines:
                return 99999, move

            nboard = copy.deepcopy(board)
            nboard.perform_white_move(move)

            nboard_key = nboard.serialize_board()

            if nboard_key not in memo.keys():
                current_score, _ = computer_minimax(nboard, depth-1, alpha, beta, False, memo)
                memo[nboard_key] = current_score
            else:
                current_score = memo[nboard_key]
            
            if current_score > best_score:
                best_score = current_score
                best_move = move
            
            alpha = max(best_score, alpha)
            
            if alpha >= beta:
                break
                
    else:
        best_score = 10000
        for move in board.black_possible_moves():
            if move[1][0] == 1:
                return -99999, move

            nboard = copy.deepcopy(board)
            nboard.perform_black_move(move)

            nboard_key = nboard.serialize_board()

            if nboard_key not in memo.keys():
                current_score, _ = computer_minimax(nboard, depth-1, alpha, beta, True, memo)
                memo[nboard_key] = current_score
            else:
                current_score = memo[nboard_key]

            if current_score < best_score:
                best_score = current_score
                best_move = move

            beta = min(best_score, beta)
            
            if alpha >= beta:
                break

    return best_score, best_move


board = Board(8, 8)

board.display()

while True:

    s, move = computer_minimax(board, 2, -10000, 10000, True, {})

    print(str(move) + " : " + str(s))

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
    
    





