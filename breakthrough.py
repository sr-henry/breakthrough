from game import *


def random_player(lines, columns, white_positions, black_positions):
    move = []
    board = [lines, columns, white_positions, black_positions]
    possible_moves = get_possible_moves(*board)
    if possible_moves:
        index = random.randint(0, abs(len(possible_moves) - 1))
        move = possible_moves[index]
    return move