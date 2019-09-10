import player
import breakthrough
import copy

def optimize_bot(winner, player1, player2):
    if winner == player1.player:
        player1.on_reward(1)
        player2.on_reward(-0.5)
    else:
        player1.on_reward(-0.5)
        player2.on_reward(1)


def train(epochs, p1, p2):
    for i in range(epochs):
        print("training {}".format(i))

        board = breakthrough.Board()

        board.display()

        while not board.is_game_over():
            white_move = p1.select_move_n(board)
            board.perform_white_move(white_move)

            board.display()

            black_move = p2.select_move_n(board)
            board.perform_black_move(black_move)

            board.display()

        optimize_bot(board.winner, p1, p2)
        p1.reset_player()
        p2.reset_player()


def evaluation(board):

        ## Value of Pieces
        value = 0.0
        for v in range(1, board.rows + 1):
            pieces_w = list(filter(lambda pos: pos[0] == v, board.white_positions))
            pieces_b = list(filter(lambda pos: pos[0] == ((board.rows + 1) - v), board.black_positions))
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
            if move[1][0] == board.rows:
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



def main():
    p1 = player.Player(1)
    p2 = player.Player(-1)

    train(50000, p1, p2)

    game = breakthrough.Board()

    p2.get_serious()

    game.display()

    while not game.is_game_over():
        
        white_move = p1.select_move(game)

        game.perform_white_move(white_move)

        game.display()

        _,black_move = computer_minimax(game, 2, -10000, 10000, False, {})
        game.perform_black_move(black_move)

        game.display()
    
    if game.winner == 1:
        print("reinfoecement wins")
    else:
        print("minimax wins")

p1 = player.Player(1)
p2 = player.Player(-1)
train(10, p1, p2)
