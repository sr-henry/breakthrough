from game import *


def random_player(lines, columns, white_positions, black_positions):
    move = []
    board = [lines, columns, white_positions, black_positions]
    possible_moves = get_possible_moves(*board)
    if possible_moves:
        index = random.randint(0, abs(len(possible_moves) - 1))
        move = possible_moves[index]
    return move


def calculate_score_board(lines, columns, white_positions, black_positions):
    scored = {}
    for r in range(lines, 0, -1):
        for c in range(1, columns + 1):
            current_score = r * 10
            if (r, c) in white_positions:
                if r >= lines/2:
                    current_score *= (r * .4)

            if (r, c) in black_positions:
                current_score -= 5
                if r <= lines/2:
                    current_score *= ((8 - r) * .9)

                if (r - 1, c - 1) in white_positions:
                    current_score -= 10

                if (r - 1, c + 1) in white_positions:
                    current_score -= 10

            if (r + 1, c - 1) in black_positions:
                current_score += 10

            if (r + 1, c + 1) in black_positions:
                current_score += 10
            scored[(r,c)] = current_score

    return scored


def dump_player(lines, columns, white_positions, black_positions):
    move = []
    board = [lines, columns, white_positions, black_positions]
    scores = calculate_score_board(*board)
    possible_moves = {}

    for move in get_possible_moves(*board):
        possible_moves[move] = scores[move[0]] - scores[move[1]]

    if possible_moves:
        max_value = max(possible_moves.values())
        best_moves = list(filter(lambda key: possible_moves[key] == max_value, possible_moves.keys()))
        index = random.randint(0, len(best_moves) - 1)
        move = best_moves[index]

    return move


def evaluation(lines, columns, white_positions, black_positions):
    board = [lines, columns, white_positions, black_positions]

    ## Value of Pieces
    value_pieces = 0
    for v in range(1, lines + 1):
        pieces_w = list(filter(lambda pos: pos[0] == v, white_positions))
        pieces_b = list(filter(lambda pos: pos[0] == (9 - v), black_positions))
        value_pieces += v*(len(pieces_w) - len(pieces_b))

    ## Mobility (the number of legal moves)
    white_legal_moves = get_possible_moves(*board) 
    black_legal_moves = get_possible_moves(*flip_board(*board))
    mobility = len(white_legal_moves) - len(black_legal_moves)

    ## Blocked Pieces
    white_origins = set(map(lambda move: move[0], white_legal_moves))
    black_origins = set(map(lambda move: move[0], black_legal_moves))
    white_positions_blocked = len(white_positions) - len(white_origins)
    black_positions_blocked = len(black_positions) - len(black_origins) 
    blocks = white_positions_blocked - black_positions_blocked    

    ## Isolated Pieces
    ## Connectivity

    ## Evaluation
    score = value_pieces + .2*mobility - .5*blocks

    return score
    

def simulate_move(move, white_positions, black_positions):
    origem, destino = move    

    new_white_positions = white_positions.copy()
    new_black_positions = black_positions.copy()

    new_white_positions.remove(origem) 
    new_white_positions.append(destino)

    if destino in new_black_positions :
        new_black_positions.remove(destino)

    return new_white_positions, new_black_positions


def evil_player(lines, columns, white_positions, black_positions):
    move = []
    board = [lines, columns, white_positions, black_positions]
    current_score = evaluation(*board)
    possible_moves = {}

    for move in get_possible_moves(*board):
        if move[1][0] == lines:
            return move
        wp, bp = simulate_move(move, white_positions, black_positions)
        score = evaluation(lines, columns, wp, bp)
        possible_moves[move] = (score - current_score)
        
    if possible_moves:
        max_value = max(possible_moves.values())
        best_moves = list(filter(lambda key: possible_moves[key] == max_value, possible_moves.keys()))
        index = random.randint(0, abs(len(best_moves) - 1))
        move = best_moves[index]

    return move



def forward_player(lines, columns, white_positions, black_positions):
    move = []
    board = [lines, columns, white_positions, black_positions]
    
    possible_moves = get_possible_moves(*board)

    max_line = 0
    best_move = []

    if possible_moves:
        for current_move in possible_moves:
            current_line = current_move[0][0]
            if current_line > max_line:
                max_line = current_line
                best_move = current_move
                if best_move[1] in black_positions:
                    return best_move

        return best_move

    return move


def mirror_player(lines, columns, white_positions, black_positions):
    move = []
    board = [lines, columns, white_positions, black_positions]

    mirrored = flip_board(*board)

    mirror_moves = []

    possible_moves = get_possible_moves(*board)

    if possible_moves:
        for current in possible_moves:
            if current[1] in mirrored[2]:
                mirror_moves.append(current)
        if mirror_moves:
            index = random.randint(0, abs(len(mirror_moves) - 1))
            move = mirror_moves[index]
        else:
            index = random.randint(0, abs(len(possible_moves) - 1))
            move = possible_moves[index]

    return move

#print(mirror_player(*generate_game()))


game_matches(random_player, mirror_player)
