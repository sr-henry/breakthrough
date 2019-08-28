import random

def draw_board(lines, columns, white_positions, black_positions):
    for r in range(lines, 0, -1):
        print(r, end = " ")
        for c in range(1, columns + 1):
            if (r, c) in white_positions:
                print("W", end = " ")
            elif (r, c) in black_positions:
                print("B", end = " ")
            else:
                print(".", end = " ")
        print()
    print("  ", end = "")
    for x in range(1, columns + 1):
        print(x, end = " ")
    print("\n========================================")


def valid_move(move, lines, columns, white_positions, black_positions) :
    ## Se não houver move, então já saia.
    if not move :
        return False
      
    origem, destino = move
    
    ## verificar limites do tabuleiro
    if not 0 < origem[0]  <= lines :
        return False
    if not 0 < destino[0] <= lines :
        return False
    if not 0 < origem[1]  <= columns :
        return False
    if not 0 < destino[1] <= columns :
        return False
    
    ## Verificar se origem é válida.
    if not origem in white_positions :
        return False
      
    ## Verificar se destino é livre de peças brancas
    if destino in white_positions :
        return False
    
    ## Verificar se passagem origem --> destino é válida
    if not (destino[0] - origem[0] == 1 and 
        abs(destino[1] - origem[1]) <= 1) :
        return False
        
    ## Verificar se frente está bloqueada pelo oponente
    if (origem[1] == destino[1]) :
        if destino in black_positions :
            return False
    return True


def perform_move(move, lines, columns, white_positions, black_positions):
    if not valid_move(move, lines, columns, white_positions, black_positions):
        return False
    
    origem, destino = move    
    
    ## Peça moveu, remover origem e adicionar destino
    white_positions.remove(origem)    
    white_positions.append(destino)
    
    ## Se destino estiver na lista de pretas, então deve ser removida.
    if destino in black_positions :
        black_positions.remove(destino)
    return True


def flip_board(lines, columns, white_positions, black_positions):
    new_white = []
    new_black = []
    
    for coord in black_positions :
        new_white.append(
            ( lines-coord[0]+1, columns-coord[1]+1)
        )
    for coord in white_positions :
        new_black.append(
            ( lines-coord[0]+1, columns-coord[1]+1)
        )
    return lines, columns, new_white, new_black


def game(player1, player2, display_board, lines, columns, white_positions, black_positions):
    winners      = [0, 0]
    tabuleiro    = [lines, columns, white_positions, black_positions]

    if display_board:
        draw_board(*tabuleiro)

    while True :
        ## Player 1
        move = player1(*tabuleiro)    
        if not perform_move(move, *tabuleiro) :
            winners[1] += 1
            break

        if display_board:
            draw_board(*tabuleiro)             
        
        if move[1][0] == tabuleiro[0] :
            winners[0] += 1
            break
            
        tabuleiro = flip_board(*tabuleiro)
        
        ## Player 2
        move = player2(*tabuleiro)    
        if not perform_move(move, *tabuleiro) :
            winners[0] += 1
            break
        tabuleiro = flip_board(*tabuleiro)    
        
        if display_board:
            draw_board(*tabuleiro) 

        if move[1][0] == tabuleiro[0] :
            winners[1] += 1
            break            

    return winners


def game_matches(player1, player2, random_game = False):
    n_matches = int(input("Number of matches: "))
    total = [0, 0]
    for i in range(0, n_matches):
        print("playing game %d"%i, end=" => ")
        result = game(player1, player2, False, *generate_game(random_game))
        print(result)
        total[0] += result[0]
        total[1] += result[1]
    print(total)


## Need to modify
def generate_game(random_game = False):
    rows = 8 ## random.randint(2, 8)
    columns = 8 ## random.randint(2, 8)
    middle_rows = int(rows/2)
    middle_columns = int(columns/2)
    half_area = middle_rows * middle_columns
    n_pieces = random.randint(2, half_area)
    white_positions = []
    black_positions = []
    
    if not random_game:
        for c in range(1, columns + 1):
            white_positions.append((1, c))
            white_positions.append((2, c))
            black_positions.append((8, c))
            black_positions.append((7, c))
    else:
        ## white pieces
        wp = 0
        while wp <= n_pieces:
            row = random.randint(1, middle_rows)
            column = random.randint(1, columns)
            position = (row, column)
            if position not in white_positions:
                white_positions.append(position)
                wp += 1
        ## black pieces
        bp = 0
        while bp <= n_pieces:
            row = random.randint(middle_rows, rows)
            column = random.randint(1, columns)
            position = (row, column)
            if position not in black_positions:
                black_positions.append(position)
                bp += 1   

    return rows, columns, white_positions, black_positions


def get_possible_moves(lines, columns, white_positions, black_positions):
    possible_moves = []

    for origin in white_positions:
        destiny = origin[0]+1, origin[1]-1
        if valid_move((origin, destiny), lines, columns, white_positions, black_positions):
            possible_moves.append((origin, destiny))
            
        destiny = origin[0]+1, origin[1]
        if valid_move((origin, destiny), lines, columns, white_positions, black_positions):
            possible_moves.append((origin, destiny))
            
        destiny = origin[0]+1, origin[1]+1
        if valid_move((origin, destiny), lines, columns, white_positions, black_positions):
            possible_moves.append((origin, destiny))

    return possible_moves
