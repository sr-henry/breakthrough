import math
import statistics
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

    #print(current_score)

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


def team_player(lines, columns, white_positions, black_positions):
    move = []
    board = [lines, columns, white_positions, black_positions]
    possible_moves = get_possible_moves(*board)
    best_moves = []

    if possible_moves:
        for current in possible_moves:
            if (current[0][0] + 1, current[0][1] + 1) in white_positions:
                best_moves.append(current)
            if (current[0][0] + 1, current[0][1]) in white_positions:
                best_moves.append(current)
            if (current[0][0] + 1, current[0][1] - 1) in white_positions:
                best_moves.append(current)

            if (current[0][0] + 1, current[0][1] + 1) in black_positions:
                return current  
            if (current[0][0] + 1, current[0][1] - 1) in black_positions:
                return current  
        
        if best_moves:
            index = random.randint(0, abs(len(best_moves) - 1))
            move = possible_moves[index]
        else:
            index = random.randint(0, abs(len(possible_moves) - 1))
            move = possible_moves[index]

    return move


def distance(piece, black_positions):
    distances = []
    for bp in black_positions:
        distances.append(math.sqrt((piece[0] - bp[0])**2 + (piece[1] - bp[1])**2))
    return statistics.mean(distances)


def killer_player(lines, columns, white_positions, black_positions):
    board = [lines, columns, white_positions, black_positions]
    possible_moves = {}
    for move in get_possible_moves(*board):
        possible_moves[move] = distance(move[1], black_positions)

    if possible_moves:
        return min(possible_moves, key = possible_moves.get)

    return []


def zigzag_player(lines, columns, white_positions, black_positions):
    board = [lines, columns, white_positions, black_positions]
    possible_moves = get_possible_moves(*board)

    selected_moves = []

    for move in possible_moves:
        if move[1][0] == lines:
            return move
        if move[1] in black_positions:
            return move
        if move[0][1] % 2 == 0 and move[1][1] % 2 != 0:
            selected_moves.append(move)
        if move[0][1] % 2 != 0 and move[1][1] % 2 == 0:
            selected_moves.append(move)
    
    if selected_moves:
        index = random.randint(0, abs(len(selected_moves) - 1))
        return selected_moves[index]

    return selected_moves


def dodge_player(lines, columns, white_positions, black_positions):
    board = [lines, columns, white_positions, black_positions]
    possible_moves = get_possible_moves(*board)

    selected_moves = []

    for move in possible_moves:
        if move[1][0] == lines:
            return move
        if move[1] in black_positions:
            return move
        if (move[1][0] + 1, move[1][1] - 1) not in black_positions:
            if (move[1][0] + 1, move[1][1] + 1) not in black_positions:
                selected_moves.append(move)

    if selected_moves:
        index = random.randint(0, abs(len(selected_moves) - 1))
        return selected_moves[index]

    return selected_moves


def connectivity(white_positions):
    conn = 0
    for (r,c) in white_positions:
        if (r - 1, c - 1) in white_positions:
            conn += 1
        if (r - 1, c + 1) in white_positions:
            conn += 1
        if (r, c - 1) in white_positions:
            conn -= .3
        if (r , c + 1) in white_positions:
            conn -= .3
    return conn


def conn_player(lines, columns, white_positions, black_positions):
    board = [lines, columns, white_positions, black_positions]
    conn = connectivity(white_positions)

    possible_moves = {}

    for move in get_possible_moves(*board):
        if move[1][0] == lines:
            return move
        wp, bp = simulate_move(move, white_positions, black_positions)
        possible_moves[move] = connectivity(wp) - conn

    if possible_moves:
        max_value = max(possible_moves.values())
        best_moves = list(filter(lambda key: possible_moves[key] == max_value, possible_moves.keys()))
        index = random.randint(0, abs(len(best_moves) - 1))
        return best_moves[index]

    return []


def sup_player(lines, columns, white_positions, black_positions):
    board = [lines, columns, white_positions, black_positions]

    selected_moves = []

    possible_moves = get_possible_moves(*board)

    for move in possible_moves:
        if (move[1][0] - 1, move[1][1] - 1) in white_positions:
            if (move[1][0] - 1, move[1][1] + 1) in white_positions:
                selected_moves.append(move)
    
    if selected_moves:
        index = random.randint(0, abs(len(selected_moves) - 1))
        return selected_moves[index]

    elif possible_moves:
        index = random.randint(0, abs(len(possible_moves) - 1))
        return possible_moves[index]

    return selected_moves


players = [dump_player,evil_player,forward_player,mirror_player,team_player,killer_player,zigzag_player,dodge_player,conn_player,sup_player]


for player in players:
    print(str(player))
    game_matches(player, random_player)
    game_matches(player, dump_player)
    game_matches(player, evil_player)
    game_matches(player, forward_player)
    game_matches(player, mirror_player)
    game_matches(player, team_player)
    game_matches(player, killer_player)
    game_matches(player, zigzag_player)
    game_matches(player, dodge_player)
    game_matches(player, conn_player)
    game_matches(player, sup_player)
    print()