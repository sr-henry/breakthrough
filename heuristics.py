def sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def is_inside(pt, v1, v2, v3):
    d1 = sign(pt, v1, v2)
    d2 = sign(pt, v2, v3)
    d3 = sign(pt, v3, v1)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)

def piece_in_fov(board, piece_type):
    piece_positions = board.white_positions if piece_type else board.black_positions
    points_to_count = board.black_positions if piece_type else board.white_positions

    if piece_type:
        v1, v2 = (board.lines, 1), (board.lines, board.columns)
    else:
        v1, v2 = (1, 1), (1, board.columns)

    n_points = 0

    for v3 in piece_positions:
        for pt in points_to_count:
            if is_inside(pt, v1, v2, v3):
                n_points += 1

    return n_points

def fov_evaluation(board):
    score = 0.0
    score -= piece_in_fov(board, True)
    score += piece_in_fov(board, False)
    return score

def piece_value_evaluation(board):
    score = 0.0
    for w in board.white_positions:
        score += w[0]
    for b in board.black_positions:
        score -= (board.lines - b[0]) +1 
    return score

def mobility_evaluation(board):
    score = 0.0
    score += len(board.possible_moves(True))
    score -= len(board.possible_moves(False))
    return score

def number_of_pieces(board):
    return float(len(board.white_positions) - len(board.black_positions))