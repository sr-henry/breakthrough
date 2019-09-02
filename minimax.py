from board import Board
import copy


board = Board(3, 3)


def depth_first_search(node_board, depth, maximizing):

    if depth == 0 or node_board.over():
        return node_board.evaluation(), None
    
    best_score = None

    if maximizing:
        best_move = None
        for move in node_board.white_possible_moves():
            new_board = copy.deepcopy(node_board)
            new_board.perform_white_move(move)

            score, _ = depth_first_search(new_board, depth-1, False)
            
            if best_score is None:
                best_score = score
            elif score > best_score:
                best_score = score
                best_move = move
        print(str(best_score) + ":" + str(best_move))
    
    else:
        best_move = None
        for move in node_board.black_possible_moves():
            new_board = copy.deepcopy(node_board)
            new_board.perform_black_move(move)

            score, _ = depth_first_search(new_board, depth-1, True)

            if best_score is None:
                best_score = score
            elif score < best_score:
                best_score = score
                best_move = move
        print(str(best_score) + ":" + str(best_move))
        
    return best_score, best_move


    

print(depth_first_search(board, 5, True))